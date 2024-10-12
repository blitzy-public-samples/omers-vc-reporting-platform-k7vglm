import pytest
from pydantic import ValidationError
from datetime import date, datetime
from uuid import UUID
from decimal import Decimal

# Import the schemas to be tested
from src.database.schemas.company import Company, CompanyCreate, CompanyUpdate, CompanyInDB
from src.database.schemas.metrics_input import MetricsInput, MetricsInputCreate, MetricsInputUpdate, MetricsInputInDB
from src.database.schemas.reporting_financials import ReportingFinancials, ReportingFinancialsCreate, ReportingFinancialsUpdate, ReportingFinancialsInDB
from src.database.schemas.reporting_metrics import ReportingMetrics, ReportingMetricsCreate, ReportingMetricsUpdate, ReportingMetricsInDB

# Test for Company schema
def test_company_schema(test_data):
    """
    Test the Company schema for correct validation and serialization.
    
    Requirements addressed:
    - Data Validation Testing (2. SYSTEM ARCHITECTURE/2.2 Component Description/2.2.1 Application Layer)
    - API Schema Validation (3. SYSTEM DESIGN/3.3 API DESIGN)
    """
    # Create a valid Company instance using test data
    company_data = test_data['company']
    company = Company(**company_data)

    # Verify that all fields are correctly set
    assert company.name == company_data['name']
    assert company.reporting_status == company_data['reporting_status']
    assert company.reporting_currency == company_data['reporting_currency']
    assert company.fund == company_data['fund']
    assert company.location_country == company_data['location_country']
    assert company.customer_type == company_data['customer_type']
    assert company.revenue_type == company_data['revenue_type']
    assert company.equity_raised == company_data['equity_raised']
    assert company.post_money_valuation == company_data['post_money_valuation']
    assert company.year_end_date == company_data['year_end_date']

    # Test serialization to dict and JSON
    company_dict = company.dict()
    assert isinstance(company_dict, dict)
    company_json = company.json()
    assert isinstance(company_json, str)

    # Test deserialization from dict and JSON
    company_from_dict = Company.parse_obj(company_dict)
    assert company_from_dict == company
    company_from_json = Company.parse_raw(company_json)
    assert company_from_json == company

    # Test validation errors for invalid data
    with pytest.raises(ValidationError):
        Company(name="", reporting_status="Invalid")

    # Test CompanyCreate
    company_create = CompanyCreate(**company_data)
    assert isinstance(company_create, CompanyCreate)

    # Test CompanyUpdate
    company_update = CompanyUpdate(name="Updated Company")
    assert company_update.name == "Updated Company"

    # Test CompanyInDB
    company_in_db_data = {**company_data, "id": UUID("12345678-1234-5678-1234-567812345678"), "created_date": datetime.now(), "created_by": "test_user"}
    company_in_db = CompanyInDB(**company_in_db_data)
    assert isinstance(company_in_db.id, UUID)
    assert isinstance(company_in_db.created_date, datetime)

    # Test currency validation
    with pytest.raises(ValidationError):
        Company(**{**company_data, "reporting_currency": "INVALID"})

    # Test that reporting_currency is converted to uppercase
    company_lower_currency = Company(**{**company_data, "reporting_currency": "usd"})
    assert company_lower_currency.reporting_currency == "USD"

# Test for MetricsInput schema
def test_metrics_input_schema(test_data):
    """
    Test the MetricsInput schema for correct validation and serialization.
    
    Requirements addressed:
    - Data Validation Testing (2. SYSTEM ARCHITECTURE/2.2 Component Description/2.2.1 Application Layer)
    - API Schema Validation (3. SYSTEM DESIGN/3.3 API DESIGN)
    """
    # Create a valid MetricsInput instance using test data
    metrics_input_data = test_data['metrics_input']
    metrics_input = MetricsInput(**metrics_input_data)

    # Verify that all fields are correctly set
    assert metrics_input.company_id == metrics_input_data['company_id']
    assert metrics_input.currency == metrics_input_data['currency']
    assert metrics_input.total_revenue == metrics_input_data['total_revenue']
    assert metrics_input.recurring_revenue == metrics_input_data['recurring_revenue']
    assert metrics_input.gross_profit == metrics_input_data['gross_profit']
    assert metrics_input.sales_marketing_expense == metrics_input_data['sales_marketing_expense']
    assert metrics_input.total_operating_expense == metrics_input_data['total_operating_expense']
    assert metrics_input.ebitda == metrics_input_data['ebitda']
    assert metrics_input.net_income == metrics_input_data['net_income']
    assert metrics_input.cash_burn == metrics_input_data['cash_burn']
    assert metrics_input.cash_balance == metrics_input_data['cash_balance']
    assert metrics_input.debt_outstanding == metrics_input_data['debt_outstanding']
    assert metrics_input.employees == metrics_input_data['employees']
    assert metrics_input.customers == metrics_input_data['customers']
    assert metrics_input.fiscal_reporting_date == metrics_input_data['fiscal_reporting_date']
    assert metrics_input.fiscal_reporting_quarter == metrics_input_data['fiscal_reporting_quarter']
    assert metrics_input.reporting_year == metrics_input_data['reporting_year']
    assert metrics_input.reporting_quarter == metrics_input_data['reporting_quarter']

    # Test serialization to dict and JSON
    metrics_input_dict = metrics_input.dict()
    assert isinstance(metrics_input_dict, dict)
    metrics_input_json = metrics_input.json()
    assert isinstance(metrics_input_json, str)

    # Test deserialization from dict and JSON
    metrics_input_from_dict = MetricsInput.parse_obj(metrics_input_dict)
    assert metrics_input_from_dict == metrics_input
    metrics_input_from_json = MetricsInput.parse_raw(metrics_input_json)
    assert metrics_input_from_json == metrics_input

    # Test validation errors for invalid data
    with pytest.raises(ValidationError):
        MetricsInput(company_id="invalid-uuid", total_revenue=-1000)

    # Test MetricsInputCreate
    metrics_input_create = MetricsInputCreate(**metrics_input_data)
    assert isinstance(metrics_input_create, MetricsInputCreate)

    # Test MetricsInputUpdate
    metrics_input_update = MetricsInputUpdate(total_revenue=1000000)
    assert metrics_input_update.total_revenue == 1000000

    # Test MetricsInputInDB
    metrics_input_in_db_data = {**metrics_input_data, "id": UUID("12345678-1234-5678-1234-567812345678")}
    metrics_input_in_db = MetricsInputInDB(**metrics_input_in_db_data)
    assert isinstance(metrics_input_in_db.id, UUID)

    # Test currency validation
    with pytest.raises(ValidationError):
        MetricsInput(**{**metrics_input_data, "currency": "INVALID"})

    # Test that currency is converted to uppercase
    metrics_input_lower_currency = MetricsInput(**{**metrics_input_data, "currency": "usd"})
    assert metrics_input_lower_currency.currency == "USD"

    # Test recurring revenue validation
    with pytest.raises(ValidationError):
        MetricsInput(**{**metrics_input_data, "recurring_revenue": metrics_input_data['total_revenue'] + 1})

    # Test total operating expense validation
    with pytest.raises(ValidationError):
        MetricsInput(**{**metrics_input_data, "total_operating_expense": metrics_input_data['sales_marketing_expense'] - 1})

# Test for ReportingFinancials schema
def test_reporting_financials_schema(test_data):
    """
    Test the ReportingFinancials schema for correct validation and serialization.
    
    Requirements addressed:
    - Data Validation Testing (2. SYSTEM ARCHITECTURE/2.2 Component Description/2.2.1 Application Layer)
    - API Schema Validation (3. SYSTEM DESIGN/3.3 API DESIGN)
    """
    # Create a valid ReportingFinancials instance using test data
    reporting_financials_data = test_data['reporting_financials']
    reporting_financials = ReportingFinancials(**reporting_financials_data)

    # Verify that all fields are correctly set
    assert reporting_financials.company_id == reporting_financials_data['company_id']
    assert reporting_financials.currency == reporting_financials_data['currency']
    assert reporting_financials.exchange_rate_used == reporting_financials_data['exchange_rate_used']
    assert reporting_financials.total_revenue == reporting_financials_data['total_revenue']
    assert reporting_financials.recurring_revenue == reporting_financials_data['recurring_revenue']
    assert reporting_financials.gross_profit == reporting_financials_data['gross_profit']
    assert reporting_financials.debt_outstanding == reporting_financials_data['debt_outstanding']
    assert reporting_financials.sales_marketing_expense == reporting_financials_data['sales_marketing_expense']
    assert reporting_financials.total_operating_expense == reporting_financials_data['total_operating_expense']
    assert reporting_financials.ebitda == reporting_financials_data['ebitda']
    assert reporting_financials.net_income == reporting_financials_data['net_income']
    assert reporting_financials.cash_burn == reporting_financials_data['cash_burn']
    assert reporting_financials.cash_balance == reporting_financials_data['cash_balance']
    assert reporting_financials.fiscal_reporting_date == reporting_financials_data['fiscal_reporting_date']
    assert reporting_financials.fiscal_reporting_quarter == reporting_financials_data['fiscal_reporting_quarter']
    assert reporting_financials.reporting_year == reporting_financials_data['reporting_year']
    assert reporting_financials.reporting_quarter == reporting_financials_data['reporting_quarter']

    # Test serialization to dict and JSON
    reporting_financials_dict = reporting_financials.dict()
    assert isinstance(reporting_financials_dict, dict)
    reporting_financials_json = reporting_financials.json()
    assert isinstance(reporting_financials_json, str)

    # Test deserialization from dict and JSON
    reporting_financials_from_dict = ReportingFinancials.parse_obj(reporting_financials_dict)
    assert reporting_financials_from_dict == reporting_financials
    reporting_financials_from_json = ReportingFinancials.parse_raw(reporting_financials_json)
    assert reporting_financials_from_json == reporting_financials

    # Test validation errors for invalid data
    with pytest.raises(ValidationError):
        ReportingFinancials(company_id="invalid-uuid", exchange_rate_used=-1.0)

    # Test ReportingFinancialsCreate
    reporting_financials_create = ReportingFinancialsCreate(**reporting_financials_data)
    assert isinstance(reporting_financials_create, ReportingFinancialsCreate)

    # Test ReportingFinancialsUpdate
    reporting_financials_update = ReportingFinancialsUpdate(total_revenue=2000000)
    assert reporting_financials_update.total_revenue == 2000000

    # Test ReportingFinancialsInDB
    reporting_financials_in_db_data = {**reporting_financials_data, "id": UUID("12345678-1234-5678-1234-567812345678"), "created_date": datetime.now(), "created_by": "test_user"}
    reporting_financials_in_db = ReportingFinancialsInDB(**reporting_financials_in_db_data)
    assert isinstance(reporting_financials_in_db.id, UUID)
    assert isinstance(reporting_financials_in_db.created_date, datetime)

    # Test currency validation
    with pytest.raises(ValidationError):
        ReportingFinancials(**{**reporting_financials_data, "currency": "INVALID"})

    # Test that currency is converted to uppercase
    reporting_financials_lower_currency = ReportingFinancials(**{**reporting_financials_data, "currency": "usd"})
    assert reporting_financials_lower_currency.currency == "USD"

# Test for ReportingMetrics schema
def test_reporting_metrics_schema(test_data):
    """
    Test the ReportingMetrics schema for correct validation and serialization.
    
    Requirements addressed:
    - Data Validation Testing (2. SYSTEM ARCHITECTURE/2.2 Component Description/2.2.1 Application Layer)
    - API Schema Validation (3. SYSTEM DESIGN/3.3 API DESIGN)
    """
    # Create a valid ReportingMetrics instance using test data
    reporting_metrics_data = test_data['reporting_metrics']
    reporting_metrics = ReportingMetrics(**reporting_metrics_data)

    # Verify that all fields are correctly set
    assert reporting_metrics.company_id == reporting_metrics_data['company_id']
    assert reporting_metrics.currency == reporting_metrics_data['currency']
    assert reporting_metrics.enterprise_value == Decimal(str(reporting_metrics_data['enterprise_value']))
    assert reporting_metrics.arr == Decimal(str(reporting_metrics_data['arr']))
    assert reporting_metrics.recurring_percentage_revenue == Decimal(str(reporting_metrics_data['recurring_percentage_revenue']))
    assert reporting_metrics.revenue_per_fte == Decimal(str(reporting_metrics_data['revenue_per_fte']))
    assert reporting_metrics.gross_profit_per_fte == Decimal(str(reporting_metrics_data['gross_profit_per_fte']))
    assert reporting_metrics.employee_growth_rate == Decimal(str(reporting_metrics_data['employee_growth_rate']))
    assert reporting_metrics.change_in_cash == Decimal(str(reporting_metrics_data['change_in_cash']))
    assert reporting_metrics.revenue_growth == Decimal(str(reporting_metrics_data['revenue_growth']))
    assert reporting_metrics.monthly_cash_burn == Decimal(str(reporting_metrics_data['monthly_cash_burn']))
    assert reporting_metrics.runway_months == Decimal(str(reporting_metrics_data['runway_months']))
    assert reporting_metrics.ev_by_equity_raised_plus_debt == Decimal(str(reporting_metrics_data['ev_by_equity_raised_plus_debt']))
    assert reporting_metrics.sales_marketing_percentage_revenue == Decimal(str(reporting_metrics_data['sales_marketing_percentage_revenue']))
    assert reporting_metrics.total_operating_percentage_revenue == Decimal(str(reporting_metrics_data['total_operating_percentage_revenue']))
    assert reporting_metrics.gross_profit_margin == Decimal(str(reporting_metrics_data['gross_profit_margin']))
    assert reporting_metrics.valuation_to_revenue == Decimal(str(reporting_metrics_data['valuation_to_revenue']))
    assert reporting_metrics.yoy_growth_revenue == Decimal(str(reporting_metrics_data['yoy_growth_revenue']))
    assert reporting_metrics.yoy_growth_profit == Decimal(str(reporting_metrics_data['yoy_growth_profit']))
    assert reporting_metrics.yoy_growth_employees == Decimal(str(reporting_metrics_data['yoy_growth_employees']))
    assert reporting_metrics.yoy_growth_ltm_revenue == Decimal(str(reporting_metrics_data['yoy_growth_ltm_revenue']))
    assert reporting_metrics.ltm_total_revenue == Decimal(str(reporting_metrics_data['ltm_total_revenue']))
    assert reporting_metrics.ltm_gross_profit == Decimal(str(reporting_metrics_data['ltm_gross_profit']))
    assert reporting_metrics.ltm_sales_marketing_expense == Decimal(str(reporting_metrics_data['ltm_sales_marketing_expense']))
    assert reporting_metrics.ltm_gross_margin == Decimal(str(reporting_metrics_data['ltm_gross_margin']))
    assert reporting_metrics.ltm_operating_expense == Decimal(str(reporting_metrics_data['ltm_operating_expense']))
    assert reporting_metrics.ltm_ebitda == Decimal(str(reporting_metrics_data['ltm_ebitda']))
    assert reporting_metrics.ltm_net_income == Decimal(str(reporting_metrics_data['ltm_net_income']))
    assert reporting_metrics.ltm_ebitda_margin == Decimal(str(reporting_metrics_data['ltm_ebitda_margin']))
    assert reporting_metrics.ltm_net_income_margin == Decimal(str(reporting_metrics_data['ltm_net_income_margin']))
    assert reporting_metrics.fiscal_reporting_date == reporting_metrics_data['fiscal_reporting_date']
    assert reporting_metrics.fiscal_reporting_quarter == reporting_metrics_data['fiscal_reporting_quarter']
    assert reporting_metrics.reporting_year == reporting_metrics_data['reporting_year']
    assert reporting_metrics.reporting_quarter == reporting_metrics_data['reporting_quarter']

    # Test serialization to dict and JSON
    reporting_metrics_dict = reporting_metrics.dict()
    assert isinstance(reporting_metrics_dict, dict)
    reporting_metrics_json = reporting_metrics.json()
    assert isinstance(reporting_metrics_json, str)

    # Test deserialization from dict and JSON
    reporting_metrics_from_dict = ReportingMetrics.parse_obj(reporting_metrics_dict)
    assert reporting_metrics_from_dict == reporting_metrics
    reporting_metrics_from_json = ReportingMetrics.parse_raw(reporting_metrics_json)
    assert reporting_metrics_from_json == reporting_metrics

    # Test validation errors for invalid data
    with pytest.raises(ValidationError):
        ReportingMetrics(company_id="invalid-uuid", arr=-1000)

    # Test ReportingMetricsCreate
    reporting_metrics_create = ReportingMetricsCreate(**reporting_metrics_data)
    assert isinstance(reporting_metrics_create, ReportingMetricsCreate)

    # Test ReportingMetricsUpdate
    reporting_metrics_update = ReportingMetricsUpdate(arr=Decimal('1000000'))
    assert reporting_metrics_update.arr == Decimal('1000000')

    # Test ReportingMetricsInDB
    reporting_metrics_in_db_data = {**reporting_metrics_data, "id": UUID("12345678-1234-5678-1234-567812345678"), "created_date": datetime.now(), "created_by": "test_user"}
    reporting_metrics_in_db = ReportingMetricsInDB(**reporting_metrics_in_db_data)
    assert isinstance(reporting_metrics_in_db.id, UUID)
    assert isinstance(reporting_metrics_in_db.created_date, datetime)

    # Test currency validation
    with pytest.raises(ValidationError):
        ReportingMetrics(**{**reporting_metrics_data, "currency": "INVALID"})

    # Test that currency is converted to uppercase
    reporting_metrics_lower_currency = ReportingMetrics(**{**reporting_metrics_data, "currency": "usd"})
    assert reporting_metrics_lower_currency.currency == "USD"

    # Test percentage validations
    with pytest.raises(ValidationError):
        ReportingMetrics(**{**reporting_metrics_data, "recurring_percentage_revenue": Decimal('101')})
    
    with pytest.raises(ValidationError):
        ReportingMetrics(**{**reporting_metrics_data, "sales_marketing_percentage_revenue": Decimal('101')})
    
    with pytest.raises(ValidationError):
        ReportingMetrics(**{**reporting_metrics_data, "total_operating_percentage_revenue": Decimal('101')})

def test_schema_relationships(test_data):
    """
    Test the relationships between different schemas.
    
    Requirements addressed:
    - Data Validation Testing (2. SYSTEM ARCHITECTURE/2.2 Component Description/2.2.1 Application Layer)
    - API Schema Validation (3. SYSTEM DESIGN/3.3 API DESIGN)
    """
    # Create instances of all schema models using test data
    company = Company(**test_data['company'])
    metrics_input = MetricsInput(**test_data['metrics_input'])
    reporting_financials = ReportingFinancials(**test_data['reporting_financials'])
    reporting_metrics = ReportingMetrics(**test_data['reporting_metrics'])

    # Verify that company_id is consistent across related schemas
    assert metrics_input.company_id == company.id
    assert reporting_financials.company_id == company.id
    assert reporting_metrics.company_id == company.id

    # Test creation of ReportingFinancials using data from MetricsInput
    reporting_financials_from_input = ReportingFinancialsCreate(
        company_id=metrics_input.company_id,
        currency=metrics_input.currency,
        exchange_rate_used=1.0,  # Assuming local currency
        total_revenue=metrics_input.total_revenue,
        recurring_revenue=metrics_input.recurring_revenue,
        gross_profit=metrics_input.gross_profit,
        debt_outstanding=metrics_input.debt_outstanding,
        sales_marketing_expense=metrics_input.sales_marketing_expense,
        total_operating_expense=metrics_input.total_operating_expense,
        ebitda=metrics_input.ebitda,
        net_income=metrics_input.net_income,
        cash_burn=metrics_input.cash_burn,
        cash_balance=metrics_input.cash_balance,
        fiscal_reporting_date=metrics_input.fiscal_reporting_date,
        fiscal_reporting_quarter=metrics_input.fiscal_reporting_quarter,
        reporting_year=metrics_input.reporting_year,
        reporting_quarter=metrics_input.reporting_quarter
    )
    assert isinstance(reporting_financials_from_input, ReportingFinancialsCreate)

    # Test creation of ReportingMetrics using data from ReportingFinancials
    reporting_metrics_from_financials = ReportingMetricsCreate(
        company_id=reporting_financials.company_id,
        currency=reporting_financials.currency,
        enterprise_value=company.post_money_valuation,
        arr=Decimal(str(reporting_financials.recurring_revenue)) * 4,  # Assuming quarterly data
        recurring_percentage_revenue=Decimal(str(reporting_financials.recurring_revenue / reporting_financials.total_revenue * 100)),
        gross_profit_margin=Decimal(str(reporting_financials.gross_profit / reporting_financials.total_revenue * 100)),
        ltm_total_revenue=Decimal(str(reporting_financials.total_revenue)) * 4,  # Assuming quarterly data
        ltm_gross_profit=Decimal(str(reporting_financials.gross_profit)) * 4,  # Assuming quarterly data
        ltm_sales_marketing_expense=Decimal(str(reporting_financials.sales_marketing_expense)) * 4,  # Assuming quarterly data
        ltm_operating_expense=Decimal(str(reporting_financials.total_operating_expense)) * 4,  # Assuming quarterly data
        ltm_ebitda=Decimal(str(reporting_financials.ebitda)) * 4,  # Assuming quarterly data
        ltm_net_income=Decimal(str(reporting_financials.net_income)) * 4,  # Assuming quarterly data
        fiscal_reporting_date=reporting_financials.fiscal_reporting_date,
        fiscal_reporting_quarter=reporting_financials.fiscal_reporting_quarter,
        reporting_year=reporting_financials.reporting_year,
        reporting_quarter=reporting_financials.reporting_quarter,
        # Add other required fields with placeholder values
        revenue_per_fte=Decimal('0'),
        gross_profit_per_fte=Decimal('0'),
        employee_growth_rate=Decimal('0'),
        change_in_cash=Decimal('0'),
        revenue_growth=Decimal('0'),
        monthly_cash_burn=Decimal('0'),
        runway_months=Decimal('0'),
        ev_by_equity_raised_plus_debt=Decimal('0'),
        sales_marketing_percentage_revenue=Decimal('0'),
        total_operating_percentage_revenue=Decimal('0'),
        valuation_to_revenue=Decimal('0'),
        yoy_growth_revenue=Decimal('0'),
        yoy_growth_profit=Decimal('0'),
        yoy_growth_employees=Decimal('0'),
        yoy_growth_ltm_revenue=Decimal('0'),
        ltm_gross_margin=Decimal('0'),
        ltm_ebitda_margin=Decimal('0'),
        ltm_net_income_margin=Decimal('0')
    )
    assert isinstance(reporting_metrics_from_financials, ReportingMetricsCreate)

    # Verify that the created instances have consistent data
    assert reporting_financials_from_input.total_revenue == metrics_input.total_revenue
    assert reporting_metrics_from_financials.arr == Decimal(str(reporting_financials.recurring_revenue)) * 4

# Add more tests as needed to cover edge cases and specific business logic