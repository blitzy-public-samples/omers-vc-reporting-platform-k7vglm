"""
Test module for MetricsInput API endpoints.

This module contains test cases for the CRUD operations on MetricsInput records.
It ensures that the API endpoints for creating, reading, updating, and deleting
MetricsInput records are functioning correctly and handling various scenarios appropriately.

Requirements addressed:
- REST API Service (2. REST API Service/F-002)
- Data Validation (2. SYSTEM ARCHITECTURE/2.2 Component Description/2.2.1 Application Layer)
- Testing (5. TESTING AND QUALITY ASSURANCE)
"""

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import uuid4
from datetime import date, timedelta
from decimal import Decimal

from src.backend.tests.conftest import client, db
from src.backend.models.metrics_input import MetricsInput
from src.backend.schemas.metrics_input import MetricsInputCreate, MetricsInputUpdate
from src.backend.models.company import Company

@pytest.mark.asyncio
async def test_create_metrics_input(client: AsyncClient, db: AsyncSession):
    """
    Test creating a new metrics input record.
    
    Requirements addressed:
    - REST API Service (2. REST API Service/F-002)
    - Data Validation (2. SYSTEM ARCHITECTURE/2.2 Component Description/2.2.1 Application Layer)
    """
    # Create a test company in the database
    company = Company(id=uuid4(), name="Test Company", reporting_status="Active", reporting_currency="USD")
    db.add(company)
    await db.commit()

    # Prepare test data for creating a metrics input record
    metrics_data = {
        "company_id": str(company.id),
        "currency": "USD",
        "total_revenue": "1000000.00",
        "recurring_revenue": "800000.00",
        "gross_profit": "600000.00",
        "sales_marketing_expense": "200000.00",
        "total_operating_expense": "500000.00",
        "ebitda": "300000.00",
        "net_income": "250000.00",
        "cash_burn": "50000.00",
        "cash_balance": "1000000.00",
        "debt_outstanding": "0.00",
        "employees": 50,
        "customers": 100,
        "fiscal_reporting_date": str(date.today()),
        "fiscal_reporting_quarter": 1,
        "reporting_year": date.today().year,
        "reporting_quarter": 1
    }

    # Send a POST request to the metrics input endpoint
    response = await client.post("/api/v1/metrics/input", json=metrics_data)

    # Assert that the response status code is 201 (Created)
    assert response.status_code == 201

    # Verify that the returned data matches the input data
    created_data = response.json()
    for key, value in metrics_data.items():
        if isinstance(value, str) and key not in ["company_id", "fiscal_reporting_date"]:
            assert Decimal(value) == Decimal(str(created_data[key]))
        elif key == "fiscal_reporting_date":
            assert value == created_data[key]
        else:
            assert value == created_data[key]

    # Check that the record was actually created in the database
    db_record = await db.get(MetricsInput, created_data["id"])
    assert db_record is not None
    assert str(db_record.company_id) == metrics_data["company_id"]

@pytest.mark.asyncio
async def test_get_metrics_input(client: AsyncClient, db: AsyncSession):
    """
    Test retrieving a metrics input record.
    
    Requirements addressed:
    - REST API Service (2. REST API Service/F-002)
    """
    # Create a test company and metrics input record in the database
    company = Company(id=uuid4(), name="Test Company", reporting_status="Active", reporting_currency="USD")
    db.add(company)
    await db.commit()

    metrics_input = MetricsInput(
        id=uuid4(),
        company_id=company.id,
        currency="USD",
        total_revenue=Decimal("1000000.00"),
        recurring_revenue=Decimal("800000.00"),
        gross_profit=Decimal("600000.00"),
        sales_marketing_expense=Decimal("200000.00"),
        total_operating_expense=Decimal("500000.00"),
        ebitda=Decimal("300000.00"),
        net_income=Decimal("250000.00"),
        cash_burn=Decimal("50000.00"),
        cash_balance=Decimal("1000000.00"),
        debt_outstanding=Decimal("0.00"),
        employees=50,
        customers=100,
        fiscal_reporting_date=date.today(),
        fiscal_reporting_quarter=1,
        reporting_year=date.today().year,
        reporting_quarter=1,
        created_by="test_user"
    )
    db.add(metrics_input)
    await db.commit()

    # Send a GET request to the metrics input endpoint with the record's ID
    response = await client.get(f"/api/v1/metrics/input/{metrics_input.id}")

    # Assert that the response status code is 200 (OK)
    assert response.status_code == 200

    # Verify that the returned data matches the created record
    retrieved_data = response.json()
    assert str(metrics_input.id) == retrieved_data["id"]
    assert str(metrics_input.company_id) == retrieved_data["company_id"]
    assert metrics_input.currency == retrieved_data["currency"]
    assert str(metrics_input.total_revenue) == retrieved_data["total_revenue"]
    assert str(metrics_input.recurring_revenue) == retrieved_data["recurring_revenue"]
    assert str(metrics_input.gross_profit) == retrieved_data["gross_profit"]
    assert str(metrics_input.sales_marketing_expense) == retrieved_data["sales_marketing_expense"]
    assert str(metrics_input.total_operating_expense) == retrieved_data["total_operating_expense"]
    assert str(metrics_input.ebitda) == retrieved_data["ebitda"]
    assert str(metrics_input.net_income) == retrieved_data["net_income"]
    assert str(metrics_input.cash_burn) == retrieved_data["cash_burn"]
    assert str(metrics_input.cash_balance) == retrieved_data["cash_balance"]
    assert str(metrics_input.debt_outstanding) == retrieved_data["debt_outstanding"]
    assert metrics_input.employees == retrieved_data["employees"]
    assert metrics_input.customers == retrieved_data["customers"]
    assert str(metrics_input.fiscal_reporting_date) == retrieved_data["fiscal_reporting_date"]
    assert metrics_input.fiscal_reporting_quarter == retrieved_data["fiscal_reporting_quarter"]
    assert metrics_input.reporting_year == retrieved_data["reporting_year"]
    assert metrics_input.reporting_quarter == retrieved_data["reporting_quarter"]

@pytest.mark.asyncio
async def test_update_metrics_input(client: AsyncClient, db: AsyncSession):
    """
    Test updating an existing metrics input record.
    
    Requirements addressed:
    - REST API Service (2. REST API Service/F-002)
    - Data Validation (2. SYSTEM ARCHITECTURE/2.2 Component Description/2.2.1 Application Layer)
    """
    # Create a test company and metrics input record in the database
    company = Company(id=uuid4(), name="Test Company", reporting_status="Active", reporting_currency="USD")
    db.add(company)
    await db.commit()

    metrics_input = MetricsInput(
        id=uuid4(),
        company_id=company.id,
        currency="USD",
        total_revenue=Decimal("1000000.00"),
        recurring_revenue=Decimal("800000.00"),
        gross_profit=Decimal("600000.00"),
        sales_marketing_expense=Decimal("200000.00"),
        total_operating_expense=Decimal("500000.00"),
        ebitda=Decimal("300000.00"),
        net_income=Decimal("250000.00"),
        cash_burn=Decimal("50000.00"),
        cash_balance=Decimal("1000000.00"),
        debt_outstanding=Decimal("0.00"),
        employees=50,
        customers=100,
        fiscal_reporting_date=date.today(),
        fiscal_reporting_quarter=1,
        reporting_year=date.today().year,
        reporting_quarter=1,
        created_by="test_user"
    )
    db.add(metrics_input)
    await db.commit()

    # Prepare update data for the metrics input record
    update_data = {
        "total_revenue": "1100000.00",
        "recurring_revenue": "900000.00",
        "gross_profit": "650000.00",
        "employees": 55,
        "customers": 110
    }

    # Send a PUT request to the metrics input endpoint with the record's ID
    response = await client.put(f"/api/v1/metrics/input/{metrics_input.id}", json=update_data)

    # Assert that the response status code is 200 (OK)
    assert response.status_code == 200

    # Verify that the returned data reflects the updates
    updated_data = response.json()
    for key, value in update_data.items():
        if isinstance(value, str):
            assert Decimal(value) == Decimal(str(updated_data[key]))
        else:
            assert value == updated_data[key]

    # Check that the record was actually updated in the database
    db_record = await db.get(MetricsInput, metrics_input.id)
    assert db_record is not None
    assert db_record.total_revenue == Decimal("1100000.00")
    assert db_record.recurring_revenue == Decimal("900000.00")
    assert db_record.gross_profit == Decimal("650000.00")
    assert db_record.employees == 55
    assert db_record.customers == 110

@pytest.mark.asyncio
async def test_delete_metrics_input(client: AsyncClient, db: AsyncSession):
    """
    Test deleting a metrics input record.
    
    Requirements addressed:
    - REST API Service (2. REST API Service/F-002)
    """
    # Create a test company and metrics input record in the database
    company = Company(id=uuid4(), name="Test Company", reporting_status="Active", reporting_currency="USD")
    db.add(company)
    await db.commit()

    metrics_input = MetricsInput(
        id=uuid4(),
        company_id=company.id,
        currency="USD",
        total_revenue=Decimal("1000000.00"),
        recurring_revenue=Decimal("800000.00"),
        gross_profit=Decimal("600000.00"),
        sales_marketing_expense=Decimal("200000.00"),
        total_operating_expense=Decimal("500000.00"),
        ebitda=Decimal("300000.00"),
        net_income=Decimal("250000.00"),
        cash_burn=Decimal("50000.00"),
        cash_balance=Decimal("1000000.00"),
        debt_outstanding=Decimal("0.00"),
        employees=50,
        customers=100,
        fiscal_reporting_date=date.today(),
        fiscal_reporting_quarter=1,
        reporting_year=date.today().year,
        reporting_quarter=1,
        created_by="test_user"
    )
    db.add(metrics_input)
    await db.commit()

    # Send a DELETE request to the metrics input endpoint with the record's ID
    response = await client.delete(f"/api/v1/metrics/input/{metrics_input.id}")

    # Assert that the response status code is 204 (No Content)
    assert response.status_code == 204

    # Verify that the record no longer exists in the database
    db_record = await db.get(MetricsInput, metrics_input.id)
    assert db_record is None

@pytest.mark.asyncio
async def test_get_metrics_inputs(client: AsyncClient, db: AsyncSession):
    """
    Test retrieving a list of metrics input records.
    
    Requirements addressed:
    - REST API Service (2. REST API Service/F-002)
    """
    # Create multiple test metrics input records in the database
    company = Company(id=uuid4(), name="Test Company", reporting_status="Active", reporting_currency="USD")
    db.add(company)
    await db.commit()

    metrics_inputs = []
    for i in range(3):
        metrics_input = MetricsInput(
            id=uuid4(),
            company_id=company.id,
            currency="USD",
            total_revenue=Decimal(f"{1000000 + i * 100000}.00"),
            recurring_revenue=Decimal(f"{800000 + i * 80000}.00"),
            gross_profit=Decimal(f"{600000 + i * 60000}.00"),
            sales_marketing_expense=Decimal(f"{200000 + i * 20000}.00"),
            total_operating_expense=Decimal(f"{500000 + i * 50000}.00"),
            ebitda=Decimal(f"{300000 + i * 30000}.00"),
            net_income=Decimal(f"{250000 + i * 25000}.00"),
            cash_burn=Decimal(f"{50000 + i * 5000}.00"),
            cash_balance=Decimal(f"{1000000 + i * 100000}.00"),
            debt_outstanding=Decimal("0.00"),
            employees=50 + i * 5,
            customers=100 + i * 10,
            fiscal_reporting_date=date.today() - timedelta(days=i * 90),
            fiscal_reporting_quarter=1,
            reporting_year=date.today().year,
            reporting_quarter=1,
            created_by="test_user"
        )
        db.add(metrics_input)
        metrics_inputs.append(metrics_input)
    await db.commit()

    # Send a GET request to the metrics input list endpoint
    response = await client.get("/api/v1/metrics/input")

    # Assert that the response status code is 200 (OK)
    assert response.status_code == 200

    # Verify that the returned data is a list of metrics input records
    retrieved_data = response.json()
    assert isinstance(retrieved_data, list)
    assert len(retrieved_data) >= 3

    # Check that the number of returned records matches the expected count
    assert len(retrieved_data) >= len(metrics_inputs)

    # Verify that the created records are in the returned data
    created_ids = {str(mi.id) for mi in metrics_inputs}
    retrieved_ids = {item["id"] for item in retrieved_data}
    assert created_ids.issubset(retrieved_ids)

@pytest.mark.asyncio
async def test_create_metrics_input_validation(client: AsyncClient, db: AsyncSession):
    """
    Test input validation when creating a metrics input record.
    
    Requirements addressed:
    - REST API Service (2. REST API Service/F-002)
    - Data Validation (2. SYSTEM ARCHITECTURE/2.2 Component Description/2.2.1 Application Layer)
    """
    # Create a test company in the database
    company = Company(id=uuid4(), name="Test Company", reporting_status="Active", reporting_currency="USD")
    db.add(company)
    await db.commit()

    # Prepare invalid test data for creating a metrics input record
    invalid_data = {
        "company_id": str(company.id),  # Valid company_id
        "currency": "INVALID",
        "total_revenue": "-1000.00",
        "recurring_revenue": "not-a-number",
        "gross_profit": "600000.00",
        "sales_marketing_expense": "200000.00",
        "total_operating_expense": "500000.00",
        "ebitda": "300000.00",
        "net_income": "250000.00",
        "cash_burn": "50000.00",
        "cash_balance": "1000000.00",
        "debt_outstanding": "0.00",
        "employees": -5,
        "customers": "not-a-number",
        "fiscal_reporting_date": "invalid-date",
        "fiscal_reporting_quarter": 5,
        "reporting_year": date.today().year,
        "reporting_quarter": 0
    }

    # Send a POST request to the metrics input endpoint with invalid data
    response = await client.post("/api/v1/metrics/input", json=invalid_data)

    # Assert that the response status code is 422 (Unprocessable Entity)
    assert response.status_code == 422

    # Verify that the response contains appropriate error messages
    error_data = response.json()
    assert "detail" in error_data
    errors = {error["loc"][-1]: error["msg"] for error in error_data["detail"]}
    
    assert "currency" in errors
    assert "total_revenue" in errors
    assert "recurring_revenue" in errors
    assert "employees" in errors
    assert "customers" in errors
    assert "fiscal_reporting_date" in errors
    assert "fiscal_reporting_quarter" in errors
    assert "reporting_quarter" in errors

    # Check specific error messages
    assert "invalid currency" in errors["currency"].lower()
    assert "ensure this value is greater than 0" in errors["total_revenue"].lower()
    assert "value is not a valid decimal" in errors["recurring_revenue"].lower()
    assert "ensure this value is greater than 0" in errors["employees"].lower()
    assert "value is not a valid integer" in errors["customers"].lower()
    assert "invalid date format" in errors["fiscal_reporting_date"].lower()
    assert "ensure this value is less than or equal to 4" in errors["fiscal_reporting_quarter"].lower()
    assert "ensure this value is greater than or equal to 1" in errors["reporting_quarter"].lower()

# Additional tests can be added here to cover more scenarios and edge cases