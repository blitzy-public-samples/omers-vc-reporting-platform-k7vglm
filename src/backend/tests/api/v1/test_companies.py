import pytest
from httpx import AsyncClient
from uuid import UUID
from datetime import date, datetime
from decimal import Decimal

from src.backend.schemas.company import Company, CompanyCreate, CompanyUpdate
from src.backend.models.company import ReportingStatus, CustomerType, RevenueType

# pytest.mark.asyncio decorator is used to mark async test functions
pytestmark = pytest.mark.asyncio

async def test_create_company(client: AsyncClient, admin_user: dict):
    """
    Test creating a new company.
    
    Requirements addressed:
    - REST API Service Testing (2. REST API Service/F-002)
    - Data Validation Testing (3. SYSTEM DESIGN/3.3 API DESIGN/3.3.5 API Authentication and Authorization)
    """
    company_data = {
        "name": "Test Company",
        "reporting_status": ReportingStatus.ACTIVE.value,
        "reporting_currency": "USD",
        "fund": "Test Fund",
        "location_country": "United States",
        "customer_type": CustomerType.SMB.value,
        "revenue_type": RevenueType.SAAS.value,
        "equity_raised": "1000000.00",
        "post_money_valuation": "5000000.00",
        "year_end_date": str(date.today())
    }

    response = await client.post("/api/v1/companies/", json=company_data, headers={"Authorization": f"Bearer {admin_user['access_token']}"})

    assert response.status_code == 201

    created_company = Company(**response.json())

    assert created_company.name == company_data["name"]
    assert created_company.reporting_status == ReportingStatus(company_data["reporting_status"])
    assert created_company.reporting_currency == company_data["reporting_currency"]
    assert created_company.fund == company_data["fund"]
    assert created_company.location_country == company_data["location_country"]
    assert created_company.customer_type == CustomerType(company_data["customer_type"])
    assert created_company.revenue_type == RevenueType(company_data["revenue_type"])
    assert created_company.equity_raised == Decimal(company_data["equity_raised"])
    assert created_company.post_money_valuation == Decimal(company_data["post_money_valuation"])
    assert created_company.year_end_date == date.fromisoformat(company_data["year_end_date"])
    assert isinstance(created_company.id, UUID)
    assert isinstance(created_company.created_date, datetime)
    assert created_company.created_by is not None

async def test_get_company(client: AsyncClient, admin_user: dict, test_company: Company):
    """
    Test retrieving a specific company.
    
    Requirements addressed:
    - REST API Service Testing (2. REST API Service/F-002)
    """
    response = await client.get(f"/api/v1/companies/{test_company.id}", headers={"Authorization": f"Bearer {admin_user['access_token']}"})

    assert response.status_code == 200

    retrieved_company = Company(**response.json())

    assert retrieved_company == test_company

async def test_get_companies(client: AsyncClient, admin_user: dict, test_companies: list[Company]):
    """
    Test retrieving a list of companies.
    
    Requirements addressed:
    - REST API Service Testing (2. REST API Service/F-002)
    """
    response = await client.get("/api/v1/companies/", headers={"Authorization": f"Bearer {admin_user['access_token']}"})

    assert response.status_code == 200

    companies = [Company(**company) for company in response.json()]

    assert len(companies) == len(test_companies)

    test_company_ids = {company.id for company in test_companies}
    retrieved_company_ids = {company.id for company in companies}
    assert test_company_ids == retrieved_company_ids

async def test_update_company(client: AsyncClient, admin_user: dict, test_company: Company):
    """
    Test updating an existing company.
    
    Requirements addressed:
    - REST API Service Testing (2. REST API Service/F-002)
    - Data Validation Testing (3. SYSTEM DESIGN/3.3 API DESIGN/3.3.5 API Authentication and Authorization)
    """
    update_data = {
        "name": "Updated Test Company",
        "reporting_status": ReportingStatus.INACTIVE.value,
        "equity_raised": "2000000.00",
        "post_money_valuation": "10000000.00"
    }

    response = await client.put(f"/api/v1/companies/{test_company.id}", json=update_data, headers={"Authorization": f"Bearer {admin_user['access_token']}"})

    assert response.status_code == 200

    updated_company = Company(**response.json())

    assert updated_company.id == test_company.id
    assert updated_company.name == update_data["name"]
    assert updated_company.reporting_status == ReportingStatus(update_data["reporting_status"])
    assert updated_company.equity_raised == Decimal(update_data["equity_raised"])
    assert updated_company.post_money_valuation == Decimal(update_data["post_money_valuation"])
    assert updated_company.reporting_currency == test_company.reporting_currency
    assert updated_company.fund == test_company.fund
    assert updated_company.location_country == test_company.location_country
    assert updated_company.customer_type == test_company.customer_type
    assert updated_company.revenue_type == test_company.revenue_type
    assert updated_company.year_end_date == test_company.year_end_date
    assert updated_company.last_update_date is not None
    assert updated_company.last_updated_by is not None

async def test_create_company_validation_error(client: AsyncClient, admin_user: dict):
    """
    Test creating a company with invalid data.
    
    Requirements addressed:
    - Data Validation Testing (3. SYSTEM DESIGN/3.3 API DESIGN/3.3.5 API Authentication and Authorization)
    """
    invalid_company_data = {
        "name": "",  # Invalid: empty name
        "reporting_status": "INVALID_STATUS",  # Invalid: not a valid ReportingStatus
        "reporting_currency": "INVALID",  # Invalid: not a valid currency code
        "fund": "Test Fund",
        "location_country": "United States",
        "customer_type": CustomerType.SMB.value,
        "revenue_type": RevenueType.SAAS.value,
        "equity_raised": "-1000.00",  # Invalid: negative value
        "post_money_valuation": "not_a_number",  # Invalid: not a valid decimal
        "year_end_date": "2023-13-01"  # Invalid: not a valid date
    }

    response = await client.post("/api/v1/companies/", json=invalid_company_data, headers={"Authorization": f"Bearer {admin_user['access_token']}"})

    assert response.status_code == 422

    error_response = response.json()
    assert "detail" in error_response
    assert isinstance(error_response["detail"], list)
    assert len(error_response["detail"]) > 0
    for error in error_response["detail"]:
        assert "loc" in error
        assert "msg" in error
        assert "type" in error

async def test_get_company_not_found(client: AsyncClient, admin_user: dict):
    """
    Test retrieving a non-existent company.
    
    Requirements addressed:
    - REST API Service Testing (2. REST API Service/F-002)
    """
    non_existent_id = UUID('12345678-1234-5678-1234-567812345678')

    response = await client.get(f"/api/v1/companies/{non_existent_id}", headers={"Authorization": f"Bearer {admin_user['access_token']}"})

    assert response.status_code == 404

    error_response = response.json()
    assert "detail" in error_response
    assert error_response["detail"] == "Company not found"

async def test_create_company_unauthorized(client: AsyncClient, analyst_user: dict):
    """
    Test creating a company with unauthorized user.
    
    Requirements addressed:
    - Authentication and Authorization Testing (6. SECURITY CONSIDERATIONS/6.1 AUTHENTICATION AND AUTHORIZATION)
    """
    company_data = {
        "name": "Unauthorized Company",
        "reporting_status": ReportingStatus.ACTIVE.value,
        "reporting_currency": "USD",
        "fund": "Test Fund",
        "location_country": "United States",
        "customer_type": CustomerType.SMB.value,
        "revenue_type": RevenueType.SAAS.value,
        "equity_raised": "1000000.00",
        "post_money_valuation": "5000000.00",
        "year_end_date": str(date.today())
    }

    response = await client.post("/api/v1/companies/", json=company_data, headers={"Authorization": f"Bearer {analyst_user['access_token']}"})

    assert response.status_code == 403

    error_response = response.json()
    assert "detail" in error_response
    assert error_response["detail"] == "Not enough permissions"

async def test_delete_company(client: AsyncClient, admin_user: dict, test_company: Company):
    """
    Test deleting an existing company.
    
    Requirements addressed:
    - REST API Service Testing (2. REST API Service/F-002)
    """
    response = await client.delete(f"/api/v1/companies/{test_company.id}", headers={"Authorization": f"Bearer {admin_user['access_token']}"})

    assert response.status_code == 204

    # Verify that the company has been deleted
    get_response = await client.get(f"/api/v1/companies/{test_company.id}", headers={"Authorization": f"Bearer {admin_user['access_token']}"})
    assert get_response.status_code == 404

async def test_partial_update_company(client: AsyncClient, admin_user: dict, test_company: Company):
    """
    Test partial update of an existing company.
    
    Requirements addressed:
    - REST API Service Testing (2. REST API Service/F-002)
    - Data Validation Testing (3. SYSTEM DESIGN/3.3 API DESIGN/3.3.5 API Authentication and Authorization)
    """
    update_data = {
        "name": "Partially Updated Company",
        "equity_raised": "3000000.00"
    }

    response = await client.patch(f"/api/v1/companies/{test_company.id}", json=update_data, headers={"Authorization": f"Bearer {admin_user['access_token']}"})

    assert response.status_code == 200

    updated_company = Company(**response.json())

    assert updated_company.id == test_company.id
    assert updated_company.name == update_data["name"]
    assert updated_company.equity_raised == Decimal(update_data["equity_raised"])
    # Check that other fields remain unchanged
    assert updated_company.reporting_status == test_company.reporting_status
    assert updated_company.reporting_currency == test_company.reporting_currency
    assert updated_company.fund == test_company.fund
    assert updated_company.location_country == test_company.location_country
    assert updated_company.customer_type == test_company.customer_type
    assert updated_company.revenue_type == test_company.revenue_type
    assert updated_company.post_money_valuation == test_company.post_money_valuation
    assert updated_company.year_end_date == test_company.year_end_date
    assert updated_company.last_update_date is not None
    assert updated_company.last_updated_by is not None