import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date
from decimal import Decimal
from uuid import uuid4

from src.backend.models.reporting_metrics import ReportingMetrics
from src.backend.schemas.reporting_metrics import ReportingMetricsCreate, ReportingMetricsUpdate
from src.backend.models.company import Company
from src.backend.core.security import create_access_token
from src.backend.core.config import settings

# Pytest fixture for creating a test company
@pytest.fixture
async def test_company(db: AsyncSession):
    company = Company(
        id=uuid4(),
        name="Test Company",
        reporting_status="Active",
        reporting_currency="USD",
        fund="Test Fund",
        location_country="USA",
        customer_type="B2B",
        revenue_type="Subscription",
        year_end_date=date(2023, 12, 31)
    )
    db.add(company)
    await db.commit()
    return company

# Pytest fixture for creating test users with different roles
@pytest.fixture
def test_users():
    admin_token = create_access_token({"sub": "admin@example.com", "role": "admin"})
    analyst_token = create_access_token({"sub": "analyst@example.com", "role": "analyst"})
    company_user_token = create_access_token({"sub": "company@example.com", "role": "company_user"})
    return {
        "admin": admin_token,
        "analyst": analyst_token,
        "company_user": company_user_token
    }

@pytest.mark.asyncio
async def test_create_reporting_metrics(client: AsyncClient, db: AsyncSession, test_company, test_users):
    """
    Test creating a new reporting metrics entry.
    Addresses requirement: REST API Service (2. REST API Service/F-002)
    """
    metrics_data = {
        "company_id": str(test_company.id),
        "currency": "USD",
        "enterprise_value": 1000000,
        "arr": 500000,
        "recurring_percentage_revenue": 80,
        "revenue_per_fte": 200000,
        "gross_profit_per_fte": 150000,
        "employee_growth_rate": 10,
        "change_in_cash": 50000,
        "revenue_growth": 20,
        "monthly_cash_burn": 30000,
        "runway_months": 18,
        "ev_by_equity_raised_plus_debt": 2.5,
        "sales_marketing_percentage_revenue": 30,
        "total_operating_percentage_revenue": 70,
        "gross_profit_margin": 60,
        "valuation_to_revenue": 5,
        "yoy_growth_revenue": 25,
        "yoy_growth_profit": 30,
        "yoy_growth_employees": 15,
        "yoy_growth_ltm_revenue": 22,
        "ltm_total_revenue": 2000000,
        "ltm_gross_profit": 1200000,
        "ltm_sales_marketing_expense": 600000,
        "ltm_gross_margin": 60,
        "ltm_operating_expense": 1400000,
        "ltm_ebitda": 600000,
        "ltm_net_income": 400000,
        "ltm_ebitda_margin": 30,
        "ltm_net_income_margin": 20,
        "fiscal_reporting_date": "2023-03-31",
        "fiscal_reporting_quarter": 1,
        "reporting_year": 2023,
        "reporting_quarter": 1
    }

    headers = {"Authorization": f"Bearer {test_users['admin']}"}
    response = await client.post("/api/v1/reporting-metrics/", json=metrics_data, headers=headers)
    assert response.status_code == 201
    created_metrics = response.json()

    assert created_metrics["company_id"] == str(test_company.id)
    assert created_metrics["currency"] == "USD"
    assert Decimal(created_metrics["enterprise_value"]) == Decimal("1000000")
    assert Decimal(created_metrics["arr"]) == Decimal("500000")

    # Verify that the created entry exists in the database
    db_metrics = await db.get(ReportingMetrics, created_metrics["id"])
    assert db_metrics is not None
    assert db_metrics.company_id == test_company.id
    assert db_metrics.currency == "USD"
    assert db_metrics.enterprise_value == Decimal("1000000")
    assert db_metrics.arr == Decimal("500000")

@pytest.mark.asyncio
async def test_read_reporting_metrics(client: AsyncClient, db: AsyncSession, test_company, test_users):
    """
    Test retrieving reporting metrics for a company.
    Addresses requirement: REST API Service (2. REST API Service/F-002)
    """
    # Create a test reporting metrics entry
    metrics = ReportingMetrics(
        company_id=test_company.id,
        currency="USD",
        enterprise_value=Decimal("1000000"),
        arr=Decimal("500000"),
        recurring_percentage_revenue=Decimal("80"),
        fiscal_reporting_date=date(2023, 3, 31),
        fiscal_reporting_quarter=1,
        reporting_year=2023,
        reporting_quarter=1,
        created_by="test_user"
    )
    db.add(metrics)
    await db.commit()

    headers = {"Authorization": f"Bearer {test_users['analyst']}"}
    response = await client.get(f"/api/v1/reporting-metrics/{test_company.id}", headers=headers)
    assert response.status_code == 200
    retrieved_metrics = response.json()

    assert len(retrieved_metrics) == 1
    assert retrieved_metrics[0]["company_id"] == str(test_company.id)
    assert retrieved_metrics[0]["currency"] == "USD"
    assert Decimal(retrieved_metrics[0]["enterprise_value"]) == Decimal("1000000")
    assert Decimal(retrieved_metrics[0]["arr"]) == Decimal("500000")

@pytest.mark.asyncio
async def test_update_reporting_metrics(client: AsyncClient, db: AsyncSession, test_company, test_users):
    """
    Test updating an existing reporting metrics entry.
    Addresses requirement: REST API Service (2. REST API Service/F-002)
    """
    # Create a test reporting metrics entry
    metrics = ReportingMetrics(
        company_id=test_company.id,
        currency="USD",
        enterprise_value=Decimal("1000000"),
        arr=Decimal("500000"),
        recurring_percentage_revenue=Decimal("80"),
        fiscal_reporting_date=date(2023, 3, 31),
        fiscal_reporting_quarter=1,
        reporting_year=2023,
        reporting_quarter=1,
        created_by="test_user"
    )
    db.add(metrics)
    await db.commit()

    update_data = {
        "enterprise_value": 1200000,
        "arr": 600000,
        "recurring_percentage_revenue": 85
    }

    headers = {"Authorization": f"Bearer {test_users['admin']}"}
    response = await client.put(f"/api/v1/reporting-metrics/{metrics.id}", json=update_data, headers=headers)
    assert response.status_code == 200
    updated_metrics = response.json()

    assert Decimal(updated_metrics["enterprise_value"]) == Decimal("1200000")
    assert Decimal(updated_metrics["arr"]) == Decimal("600000")
    assert Decimal(updated_metrics["recurring_percentage_revenue"]) == Decimal("85")

    # Verify that the updated entry in the database reflects the changes
    db_metrics = await db.get(ReportingMetrics, metrics.id)
    assert db_metrics.enterprise_value == Decimal("1200000")
    assert db_metrics.arr == Decimal("600000")
    assert db_metrics.recurring_percentage_revenue == Decimal("85")

@pytest.mark.asyncio
async def test_delete_reporting_metrics(client: AsyncClient, db: AsyncSession, test_company, test_users):
    """
    Test deleting a reporting metrics entry.
    Addresses requirement: REST API Service (2. REST API Service/F-002)
    """
    # Create a test reporting metrics entry
    metrics = ReportingMetrics(
        company_id=test_company.id,
        currency="USD",
        enterprise_value=Decimal("1000000"),
        arr=Decimal("500000"),
        recurring_percentage_revenue=Decimal("80"),
        fiscal_reporting_date=date(2023, 3, 31),
        fiscal_reporting_quarter=1,
        reporting_year=2023,
        reporting_quarter=1,
        created_by="test_user"
    )
    db.add(metrics)
    await db.commit()

    headers = {"Authorization": f"Bearer {test_users['admin']}"}
    response = await client.delete(f"/api/v1/reporting-metrics/{metrics.id}", headers=headers)
    assert response.status_code == 200

    # Verify that the deleted entry no longer exists in the database
    db_metrics = await db.get(ReportingMetrics, metrics.id)
    assert db_metrics is None

@pytest.mark.asyncio
async def test_read_reporting_metrics_with_filters(client: AsyncClient, db: AsyncSession, test_company, test_users):
    """
    Test retrieving reporting metrics with various filters.
    Addresses requirement: REST API Service (2. REST API Service/F-002)
    """
    # Create multiple test reporting metrics entries
    metrics1 = ReportingMetrics(
        company_id=test_company.id,
        currency="USD",
        enterprise_value=Decimal("1000000"),
        arr=Decimal("500000"),
        recurring_percentage_revenue=Decimal("80"),
        fiscal_reporting_date=date(2023, 3, 31),
        fiscal_reporting_quarter=1,
        reporting_year=2023,
        reporting_quarter=1,
        created_by="test_user"
    )
    metrics2 = ReportingMetrics(
        company_id=test_company.id,
        currency="USD",
        enterprise_value=Decimal("1100000"),
        arr=Decimal("550000"),
        recurring_percentage_revenue=Decimal("82"),
        fiscal_reporting_date=date(2023, 6, 30),
        fiscal_reporting_quarter=2,
        reporting_year=2023,
        reporting_quarter=2,
        created_by="test_user"
    )
    db.add_all([metrics1, metrics2])
    await db.commit()

    headers = {"Authorization": f"Bearer {test_users['analyst']}"}

    # Test filtering by date range
    response = await client.get("/api/v1/reporting-metrics/?start_date=2023-01-01&end_date=2023-03-31", headers=headers)
    assert response.status_code == 200
    filtered_metrics = response.json()
    assert len(filtered_metrics) == 1
    assert filtered_metrics[0]["fiscal_reporting_date"] == "2023-03-31"

    # Test filtering by currency
    response = await client.get("/api/v1/reporting-metrics/?currency=USD", headers=headers)
    assert response.status_code == 200
    filtered_metrics = response.json()
    assert len(filtered_metrics) == 2
    assert all(m["currency"] == "USD" for m in filtered_metrics)

    # Test filtering by reporting year and quarter
    response = await client.get("/api/v1/reporting-metrics/?reporting_year=2023&reporting_quarter=2", headers=headers)
    assert response.status_code == 200
    filtered_metrics = response.json()
    assert len(filtered_metrics) == 1
    assert filtered_metrics[0]["reporting_year"] == 2023
    assert filtered_metrics[0]["reporting_quarter"] == 2

@pytest.mark.asyncio
async def test_reporting_metrics_validation(client: AsyncClient, db: AsyncSession, test_company, test_users):
    """
    Test input validation for reporting metrics operations.
    Addresses requirement: Data Validation (3. SYSTEM DESIGN/3.3 API DESIGN)
    """
    # Test invalid data for create operation
    invalid_data = {
        "company_id": str(test_company.id),
        "currency": "INVALID",
        "enterprise_value": "not a number",
        "arr": -1000,
        "recurring_percentage_revenue": 150,
        "fiscal_reporting_date": "2023-13-31",
        "fiscal_reporting_quarter": 5,
        "reporting_year": 2023,
        "reporting_quarter": 0
    }

    headers = {"Authorization": f"Bearer {test_users['admin']}"}
    response = await client.post("/api/v1/reporting-metrics/", json=invalid_data, headers=headers)
    assert response.status_code == 422
    errors = response.json()["detail"]
    assert any(error["loc"] == ["body", "currency"] for error in errors)
    assert any(error["loc"] == ["body", "enterprise_value"] for error in errors)
    assert any(error["loc"] == ["body", "arr"] for error in errors)
    assert any(error["loc"] == ["body", "recurring_percentage_revenue"] for error in errors)
    assert any(error["loc"] == ["body", "fiscal_reporting_date"] for error in errors)
    assert any(error["loc"] == ["body", "fiscal_reporting_quarter"] for error in errors)
    assert any(error["loc"] == ["body", "reporting_quarter"] for error in errors)

    # Test invalid data for update operation
    valid_metrics = ReportingMetrics(
        company_id=test_company.id,
        currency="USD",
        enterprise_value=Decimal("1000000"),
        arr=Decimal("500000"),
        recurring_percentage_revenue=Decimal("80"),
        fiscal_reporting_date=date(2023, 3, 31),
        fiscal_reporting_quarter=1,
        reporting_year=2023,
        reporting_quarter=1,
        created_by="test_user"
    )
    db.add(valid_metrics)
    await db.commit()

    invalid_update_data = {
        "enterprise_value": "not a number",
        "arr": -1000,
        "recurring_percentage_revenue": 150
    }

    response = await client.put(f"/api/v1/reporting-metrics/{valid_metrics.id}", json=invalid_update_data, headers=headers)
    assert response.status_code == 422
    errors = response.json()["detail"]
    assert any(error["loc"] == ["body", "enterprise_value"] for error in errors)
    assert any(error["loc"] == ["body", "arr"] for error in errors)
    assert any(error["loc"] == ["body", "recurring_percentage_revenue"] for error in errors)

@pytest.mark.asyncio
async def test_reporting_metrics_authentication(client: AsyncClient, db: AsyncSession):
    """
    Test authentication requirements for reporting metrics endpoints.
    Addresses requirement: Security and Compliance (5. Security and Compliance/F-005)
    """
    # Attempt to access endpoints without authentication
    response = await client.get("/api/v1/reporting-metrics/")
    assert response.status_code == 401

    response = await client.post("/api/v1/reporting-metrics/", json={})
    assert response.status_code == 401

    response = await client.put("/api/v1/reporting-metrics/123", json={})
    assert response.status_code == 401

    response = await client.delete("/api/v1/reporting-metrics/123")
    assert response.status_code == 401

    # Test with invalid authentication token
    headers = {"Authorization": "Bearer invalid_token"}
    response = await client.get("/api/v1/reporting-metrics/", headers=headers)
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_reporting_metrics_authorization(client: AsyncClient, db: AsyncSession, test_company, test_users):
    """
    Test authorization rules for reporting metrics endpoints.
    Addresses requirement: Security and Compliance (5. Security and Compliance/F-005)
    """
    # Create a test reporting metrics entry
    metrics = ReportingMetrics(
        company_id=test_company.id,
        currency="USD",
        enterprise_value=Decimal("1000000"),
        arr=Decimal("500000"),
        recurring_percentage_revenue=Decimal("80"),
        fiscal_reporting_date=date(2023, 3, 31),
        fiscal_reporting_quarter=1,
        reporting_year=2023,
        reporting_quarter=1,
        created_by="test_user"
    )
    db.add(metrics)
    await db.commit()

    # Test admin access (should have full access)
    headers = {"Authorization": f"Bearer {test_users['admin']}"}
    response = await client.get("/api/v1/reporting-metrics/", headers=headers)
    assert response.status_code == 200

    response = await client.post("/api/v1/reporting-metrics/", json={}, headers=headers)
    assert response.status_code == 422  # Validation error, but not authorization error

    response = await client.put(f"/api/v1/reporting-metrics/{metrics.id}", json={}, headers=headers)
    assert response.status_code == 422  # Validation error, but not authorization error

    response = await client.delete(f"/api/v1/reporting-metrics/{metrics.id}", headers=headers)
    assert response.status_code == 200

    # Test analyst access (should only have read access)
    headers = {"Authorization": f"Bearer {test_users['analyst']}"}
    response = await client.get("/api/v1/reporting-metrics/", headers=headers)
    assert response.status_code == 200

    response = await client.post("/api/v1/reporting-metrics/", json={}, headers=headers)
    assert response.status_code == 403

    response = await client.put(f"/api/v1/reporting-metrics/{metrics.id}", json={}, headers=headers)
    assert response.status_code == 403

    response = await client.delete(f"/api/v1/reporting-metrics/{metrics.id}", headers=headers)
    assert response.status_code == 403

    # Test company user access (should not have access to reporting metrics endpoints)
    headers = {"Authorization": f"Bearer {test_users['company_user']}"}
    response = await client.get("/api/v1/reporting-metrics/", headers=headers)
    assert response.status_code == 403

    response = await client.post("/api/v1/reporting-metrics/", json={}, headers=headers)
    assert response.status_code == 403

    response = await client.put(f"/api/v1/reporting-metrics/{metrics.id}", json={}, headers=headers)
    assert response.status_code == 403

    response = await client.delete(f"/api/v1/reporting-metrics/{metrics.id}", headers=headers)
    assert response.status_code == 403

# Add more tests as needed to cover edge cases and additional scenarios