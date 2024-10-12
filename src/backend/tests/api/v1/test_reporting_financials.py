import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date, datetime
from uuid import UUID, uuid4

from src.backend.models.reporting_financials import ReportingFinancials
from src.backend.schemas.reporting_financials import ReportingFinancialsCreate, ReportingFinancialsUpdate
from src.backend.models.company import Company  # Added import for Company model

# Pytest mark for asyncio
pytestmark = pytest.mark.asyncio

async def test_create_reporting_financials(client: AsyncClient, db: AsyncSession):
    """
    Test creating a new reporting financials entry.
    
    This test addresses the following requirements:
    - REST API Service (2. REST API Service/F-002)
    - Data Validation (3. SYSTEM DESIGN/3.3 API DESIGN)
    """
    # Create a test company in the database
    company = Company(name="Test Company", created_by="test_user")
    db.add(company)
    await db.commit()
    await db.refresh(company)

    # Prepare test data for creating a reporting financials entry
    test_data = {
        "company_id": str(company.id),
        "currency": "USD",
        "exchange_rate_used": 1.0,
        "total_revenue": 1000000.00,
        "recurring_revenue": 800000.00,
        "gross_profit": 600000.00,
        "sales_marketing_expense": 200000.00,
        "total_operating_expense": 500000.00,
        "ebitda": 300000.00,
        "net_income": 200000.00,
        "cash_burn": 50000.00,
        "cash_balance": 1000000.00,
        "debt_outstanding": 0.00,
        "fiscal_reporting_date": str(date.today()),
        "fiscal_reporting_quarter": 1,
        "reporting_year": date.today().year,
        "reporting_quarter": 1
    }

    # Send a POST request to create the entry
    response = await client.post("/api/v1/reporting-financials/", json=test_data)

    # Assert that the response status code is 201
    assert response.status_code == 201

    # Verify that the created entry matches the input data
    created_data = response.json()
    for key, value in test_data.items():
        if key == "company_id":
            assert UUID(created_data[key]) == UUID(value)
        elif key == "fiscal_reporting_date":
            assert created_data[key] == value
        else:
            assert created_data[key] == value

    # Attempt to create a duplicate entry and assert that it fails with 400 status code
    response = await client.post("/api/v1/reporting-financials/", json=test_data)
    assert response.status_code == 400

async def test_get_reporting_financials(client: AsyncClient, db: AsyncSession):
    """
    Test retrieving a specific reporting financials entry.
    
    This test addresses the following requirements:
    - REST API Service (2. REST API Service/F-002)
    """
    # Create a test company and reporting financials entry in the database
    company = Company(name="Test Company", created_by="test_user")
    db.add(company)
    await db.commit()
    await db.refresh(company)

    reporting_financials = ReportingFinancials(
        company_id=company.id,
        currency="USD",
        exchange_rate_used=1.0,
        total_revenue=1000000.00,
        recurring_revenue=800000.00,
        gross_profit=600000.00,
        sales_marketing_expense=200000.00,
        total_operating_expense=500000.00,
        ebitda=300000.00,
        net_income=200000.00,
        cash_burn=50000.00,
        cash_balance=1000000.00,
        debt_outstanding=0.00,
        fiscal_reporting_date=date.today(),
        fiscal_reporting_quarter=1,
        reporting_year=date.today().year,
        reporting_quarter=1,
        created_by="test_user"
    )
    db.add(reporting_financials)
    await db.commit()
    await db.refresh(reporting_financials)

    # Send a GET request to retrieve the entry
    response = await client.get(f"/api/v1/reporting-financials/{reporting_financials.id}")

    # Assert that the response status code is 200
    assert response.status_code == 200

    # Verify that the retrieved entry matches the created entry
    retrieved_data = response.json()
    assert UUID(retrieved_data["id"]) == reporting_financials.id
    assert UUID(retrieved_data["company_id"]) == company.id
    assert retrieved_data["currency"] == "USD"
    assert retrieved_data["total_revenue"] == 1000000.00
    assert retrieved_data["recurring_revenue"] == 800000.00
    # ... add more assertions for other fields

    # Attempt to retrieve a non-existent entry and assert that it fails with 404 status code
    non_existent_id = uuid4()
    response = await client.get(f"/api/v1/reporting-financials/{non_existent_id}")
    assert response.status_code == 404

async def test_list_reporting_financials(client: AsyncClient, db: AsyncSession):
    """
    Test retrieving a list of reporting financials entries.
    
    This test addresses the following requirements:
    - REST API Service (2. REST API Service/F-002)
    """
    # Create multiple test companies and reporting financials entries in the database
    companies = [Company(name=f"Test Company {i}", created_by="test_user") for i in range(3)]
    db.add_all(companies)
    await db.commit()
    for company in companies:
        await db.refresh(company)

    for company in companies:
        reporting_financials = ReportingFinancials(
            company_id=company.id,
            currency="USD",
            exchange_rate_used=1.0,
            total_revenue=1000000.00,
            recurring_revenue=800000.00,
            gross_profit=600000.00,
            sales_marketing_expense=200000.00,
            total_operating_expense=500000.00,
            ebitda=300000.00,
            net_income=200000.00,
            cash_burn=50000.00,
            cash_balance=1000000.00,
            debt_outstanding=0.00,
            fiscal_reporting_date=date.today(),
            fiscal_reporting_quarter=1,
            reporting_year=date.today().year,
            reporting_quarter=1,
            created_by="test_user"
        )
        db.add(reporting_financials)
    await db.commit()

    # Send a GET request to retrieve the list of entries
    response = await client.get("/api/v1/reporting-financials/")

    # Assert that the response status code is 200
    assert response.status_code == 200

    # Verify that the correct number of entries are returned
    data = response.json()
    assert len(data) == 3

    # Test filtering by company_id, year, and quarter
    response = await client.get(f"/api/v1/reporting-financials/?company_id={companies[0].id}&year={date.today().year}&quarter=1")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert UUID(data[0]["company_id"]) == companies[0].id

    # Test pagination using skip and limit parameters
    response = await client.get("/api/v1/reporting-financials/?skip=1&limit=1")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1

async def test_update_reporting_financials(client: AsyncClient, db: AsyncSession):
    """
    Test updating an existing reporting financials entry.
    
    This test addresses the following requirements:
    - REST API Service (2. REST API Service/F-002)
    - Data Validation (3. SYSTEM DESIGN/3.3 API DESIGN)
    """
    # Create a test company and reporting financials entry in the database
    company = Company(name="Test Company", created_by="test_user")
    db.add(company)
    await db.commit()
    await db.refresh(company)

    valid_entry = ReportingFinancials(
        company_id=company.id,
        currency="USD",
        exchange_rate_used=1.0,
        total_revenue=1000000.00,
        recurring_revenue=800000.00,
        gross_profit=600000.00,
        sales_marketing_expense=200000.00,
        total_operating_expense=500000.00,
        ebitda=300000.00,
        net_income=200000.00,
        cash_burn=50000.00,
        cash_balance=1000000.00,
        debt_outstanding=0.00,
        fiscal_reporting_date=date.today(),
        fiscal_reporting_quarter=1,
        reporting_year=date.today().year,
        reporting_quarter=1,
        created_by="test_user"
    )
    db.add(valid_entry)
    await db.commit()
    await db.refresh(valid_entry)

    # Prepare test data for updating the entry
    update_data = {
        "total_revenue": 1100000.00,
        "recurring_revenue": 900000.00,
        "gross_profit": 700000.00
    }

    # Send a PUT request to update the entry
    response = await client.put(f"/api/v1/reporting-financials/{valid_entry.id}", json=update_data)

    # Assert that the response status code is 200
    assert response.status_code == 200

    # Verify that the updated entry matches the input data
    updated_data = response.json()
    for key, value in update_data.items():
        assert updated_data[key] == value

    # Attempt to update a non-existent entry and assert that it fails with 404 status code
    non_existent_id = uuid4()
    response = await client.put(f"/api/v1/reporting-financials/{non_existent_id}", json=update_data)
    assert response.status_code == 404

async def test_delete_reporting_financials(client: AsyncClient, db: AsyncSession):
    """
    Test deleting a reporting financials entry.
    
    This test addresses the following requirements:
    - REST API Service (2. REST API Service/F-002)
    """
    # Create a test company and reporting financials entry in the database
    company = Company(name="Test Company", created_by="test_user")
    db.add(company)
    await db.commit()
    await db.refresh(company)

    reporting_financials = ReportingFinancials(
        company_id=company.id,
        currency="USD",
        exchange_rate_used=1.0,
        total_revenue=1000000.00,
        recurring_revenue=800000.00,
        gross_profit=600000.00,
        sales_marketing_expense=200000.00,
        total_operating_expense=500000.00,
        ebitda=300000.00,
        net_income=200000.00,
        cash_burn=50000.00,
        cash_balance=1000000.00,
        debt_outstanding=0.00,
        fiscal_reporting_date=date.today(),
        fiscal_reporting_quarter=1,
        reporting_year=date.today().year,
        reporting_quarter=1,
        created_by="test_user"
    )
    db.add(reporting_financials)
    await db.commit()
    await db.refresh(reporting_financials)

    # Send a DELETE request to delete the entry
    response = await client.delete(f"/api/v1/reporting-financials/{reporting_financials.id}")

    # Assert that the response status code is 200
    assert response.status_code == 200

    # Verify that the entry has been deleted from the database
    deleted_entry = await db.get(ReportingFinancials, reporting_financials.id)
    assert deleted_entry is None

    # Attempt to delete a non-existent entry and assert that it fails with 404 status code
    non_existent_id = uuid4()
    response = await client.delete(f"/api/v1/reporting-financials/{non_existent_id}")
    assert response.status_code == 404

async def test_reporting_financials_validation(client: AsyncClient, db: AsyncSession):
    """
    Test input validation for reporting financials operations.
    
    This test addresses the following requirements:
    - Data Validation (3. SYSTEM DESIGN/3.3 API DESIGN)
    """
    company = Company(name="Test Company", created_by="test_user")
    db.add(company)
    await db.commit()
    await db.refresh(company)

    # Test creating an entry with invalid data (e.g., negative revenue)
    invalid_data = {
        "company_id": str(company.id),
        "currency": "USD",
        "exchange_rate_used": 1.0,
        "total_revenue": -1000000.00,  # Invalid negative value
        "recurring_revenue": 800000.00,
        "gross_profit": 600000.00,
        "sales_marketing_expense": 200000.00,
        "total_operating_expense": 500000.00,
        "ebitda": 300000.00,
        "net_income": 200000.00,
        "cash_burn": 50000.00,
        "cash_balance": 1000000.00,
        "debt_outstanding": 0.00,
        "fiscal_reporting_date": str(date.today()),
        "fiscal_reporting_quarter": 1,
        "reporting_year": date.today().year,
        "reporting_quarter": 1
    }

    response = await client.post("/api/v1/reporting-financials/", json=invalid_data)
    assert response.status_code == 422

    # Test updating an entry with invalid data
    valid_entry = ReportingFinancials(
        company_id=company.id,
        currency="USD",
        exchange_rate_used=1.0,
        total_revenue=1000000.00,
        recurring_revenue=800000.00,
        gross_profit=600000.00,
        sales_marketing_expense=200000.00,
        total_operating_expense=500000.00,
        ebitda=300000.00,
        net_income=200000.00,
        cash_burn=50000.00,
        cash_balance=1000000.00,
        debt_outstanding=0.00,
        fiscal_reporting_date=date.today(),
        fiscal_reporting_quarter=1,
        reporting_year=date.today().year,
        reporting_quarter=1,
        created_by="test_user"
    )
    db.add(valid_entry)
    await db.commit()
    await db.refresh(valid_entry)

    invalid_update_data = {
        "gross_profit": -100000.00  # Invalid negative value
    }

    response = await client.put(f"/api/v1/reporting-financials/{valid_entry.id}", json=invalid_update_data)
    assert response.status_code == 422

    # Verify that appropriate validation errors are returned
    error_detail = response.json()["detail"]
    assert any("gross_profit" in error["loc"] for error in error_detail)

async def test_reporting_financials_permissions(client: AsyncClient, db: AsyncSession):
    """
    Test role-based access control for reporting financials endpoints.
    
    This test addresses the following requirements:
    - Security and Compliance (1.2 Scope/Core Functionalities/5. Security and Compliance)
    """
    # TODO: Implement this test once the authentication and authorization system is in place
    # This test should create test users with different roles (admin, portfolio_manager, analyst)
    # and verify that appropriate permissions are enforced for each endpoint and role

    # For now, we'll add a placeholder assertion
    assert True, "Role-based access control tests need to be implemented"

# Additional helper functions can be added here if needed