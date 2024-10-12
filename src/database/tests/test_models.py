import pytest
from decimal import Decimal
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from src.database.models.company import Company
from src.database.models.metrics_input import MetricsInput
from src.database.models.reporting_financials import ReportingFinancials
from src.database.models.reporting_metrics import ReportingMetrics
from datetime import date, datetime

# Requirement: Data Model Testing
# Location: 3. SYSTEM COMPONENTS ARCHITECTURE/3.2 SEQUENCE DIAGRAMS
# Description: Implement unit tests for database models to ensure data integrity and correct relationships

# Requirement: Data Validation
# Location: 6. SECURITY CONSIDERATIONS/6.2 DATA SECURITY
# Description: Ensure that data models enforce proper constraints and validations

def test_company_model(db_session):
    """Test the Company model creation and constraints"""
    company = Company(
        name="Test Company",
        reporting_status="Active",
        reporting_currency="USD",
        fund="Test Fund",
        location_country="USA",
        customer_type="B2B",
        revenue_type="Subscription",
        year_end_date=date(2023, 12, 31),
        created_by="test_user"
    )
    db_session.add(company)
    db_session.commit()

    # Assert that the Company object has the correct attributes
    assert company.name == "Test Company"
    assert company.reporting_status == "Active"
    assert company.reporting_currency == "USD"
    
    # Test unique constraints on company name
    with pytest.raises(IntegrityError):
        duplicate_company = Company(
            name="Test Company",
            reporting_status="Active",
            reporting_currency="USD",
            fund="Test Fund",
            location_country="USA",
            customer_type="B2B",
            revenue_type="Subscription",
            year_end_date=date(2023, 12, 31),
            created_by="test_user"
        )
        db_session.add(duplicate_company)
        db_session.commit()
    db_session.rollback()
    
    # Test non-nullable fields
    with pytest.raises(IntegrityError):
        invalid_company = Company(
            name=None,
            reporting_status="Active",
            reporting_currency="USD",
            fund="Test Fund",
            location_country="USA",
            customer_type="B2B",
            revenue_type="Subscription",
            year_end_date=date(2023, 12, 31),
            created_by="test_user"
        )
        db_session.add(invalid_company)
        db_session.commit()
    db_session.rollback()

def test_metrics_input_model(db_session):
    """Test the MetricsInput model creation and constraints"""
    company = Company(
        name="Test Company",
        reporting_status="Active",
        reporting_currency="USD",
        fund="Test Fund",
        location_country="USA",
        customer_type="B2B",
        revenue_type="Subscription",
        year_end_date=date(2023, 12, 31),
        created_by="test_user"
    )
    db_session.add(company)
    db_session.commit()

    metrics_input = MetricsInput(
        company_id=company.id,
        currency="USD",
        total_revenue=1000000.0,
        recurring_revenue=800000.0,
        gross_profit=600000.0,
        sales_marketing_expense=200000.0,
        total_operating_expense=800000.0,
        ebitda=200000.0,
        net_income=150000.0,
        cash_burn=50000.0,
        cash_balance=500000.0,
        employees=100,
        fiscal_reporting_date=date(2023, 3, 31),
        fiscal_reporting_quarter=1,
        reporting_year=2023,
        reporting_quarter=1
    )
    db_session.add(metrics_input)
    db_session.commit()
    
    # Assert that the MetricsInput object has the correct attributes
    assert metrics_input.company_id == company.id
    assert metrics_input.total_revenue == 1000000.0
    assert metrics_input.recurring_revenue == 800000.0
    
    # Test foreign key constraint with Company model
    with pytest.raises(IntegrityError):
        invalid_metrics_input = MetricsInput(
            company_id=company.id + 1,  # Non-existent company_id
            currency="USD",
            total_revenue=1000000.0,
            recurring_revenue=800000.0,
            gross_profit=600000.0,
            sales_marketing_expense=200000.0,
            total_operating_expense=800000.0,
            ebitda=200000.0,
            net_income=150000.0,
            cash_burn=50000.0,
            cash_balance=500000.0,
            employees=100,
            fiscal_reporting_date=date(2023, 3, 31),
            fiscal_reporting_quarter=1,
            reporting_year=2023,
            reporting_quarter=1
        )
        db_session.add(invalid_metrics_input)
        db_session.commit()
    db_session.rollback()
    
    # Test non-nullable fields
    with pytest.raises(IntegrityError):
        invalid_metrics_input = MetricsInput(
            company_id=company.id,
            currency="USD",
            total_revenue=None,  # This field is non-nullable
            recurring_revenue=800000.0,
            gross_profit=600000.0,
            sales_marketing_expense=200000.0,
            total_operating_expense=800000.0,
            ebitda=200000.0,
            net_income=150000.0,
            cash_burn=50000.0,
            cash_balance=500000.0,
            employees=100,
            fiscal_reporting_date=date(2023, 3, 31),
            fiscal_reporting_quarter=1,
            reporting_year=2023,
            reporting_quarter=1
        )
        db_session.add(invalid_metrics_input)
        db_session.commit()
    db_session.rollback()

def test_reporting_financials_model(db_session):
    """Test the ReportingFinancials model creation and constraints"""
    company = Company(
        name="Test Company",
        reporting_status="Active",
        reporting_currency="USD",
        fund="Test Fund",
        location_country="USA",
        customer_type="B2B",
        revenue_type="Subscription",
        year_end_date=date(2023, 12, 31),
        created_by="test_user"
    )
    db_session.add(company)
    db_session.commit()

    reporting_financials = ReportingFinancials(
        company_id=company.id,
        currency="USD",
        exchange_rate_used=Decimal('1.0'),
        total_revenue=Decimal('1000000.00'),
        recurring_revenue=Decimal('800000.00'),
        gross_profit=Decimal('600000.00'),
        sales_marketing_expense=Decimal('200000.00'),
        total_operating_expense=Decimal('800000.00'),
        ebitda=Decimal('200000.00'),
        net_income=Decimal('150000.00'),
        cash_burn=Decimal('50000.00'),
        cash_balance=Decimal('500000.00'),
        fiscal_reporting_date=date(2023, 3, 31),
        fiscal_reporting_quarter=1,
        reporting_year=2023,
        reporting_quarter=1,
        created_date=date.today(),
        created_by="test_user"
    )
    db_session.add(reporting_financials)
    db_session.commit()
    
    # Assert that the ReportingFinancials object has the correct attributes
    assert reporting_financials.company_id == company.id
    assert reporting_financials.total_revenue == Decimal('1000000.00')
    assert reporting_financials.gross_profit == Decimal('600000.00')
    
    # Test foreign key constraint with Company model
    with pytest.raises(IntegrityError):
        invalid_reporting_financials = ReportingFinancials(
            company_id=company.id + 1,  # Non-existent company_id
            currency="USD",
            exchange_rate_used=Decimal('1.0'),
            total_revenue=Decimal('1000000.00'),
            recurring_revenue=Decimal('800000.00'),
            gross_profit=Decimal('600000.00'),
            sales_marketing_expense=Decimal('200000.00'),
            total_operating_expense=Decimal('800000.00'),
            ebitda=Decimal('200000.00'),
            net_income=Decimal('150000.00'),
            cash_burn=Decimal('50000.00'),
            cash_balance=Decimal('500000.00'),
            fiscal_reporting_date=date(2023, 3, 31),
            fiscal_reporting_quarter=1,
            reporting_year=2023,
            reporting_quarter=1,
            created_date=date.today(),
            created_by="test_user"
        )
        db_session.add(invalid_reporting_financials)
        db_session.commit()
    db_session.rollback()
    
    # Test non-nullable fields
    with pytest.raises(IntegrityError):
        invalid_reporting_financials = ReportingFinancials(
            company_id=company.id,
            currency="USD",
            exchange_rate_used=Decimal('1.0'),
            total_revenue=None,  # This field is non-nullable
            recurring_revenue=Decimal('800000.00'),
            gross_profit=Decimal('600000.00'),
            sales_marketing_expense=Decimal('200000.00'),
            total_operating_expense=Decimal('800000.00'),
            ebitda=Decimal('200000.00'),
            net_income=Decimal('150000.00'),
            cash_burn=Decimal('50000.00'),
            cash_balance=Decimal('500000.00'),
            fiscal_reporting_date=date(2023, 3, 31),
            fiscal_reporting_quarter=1,
            reporting_year=2023,
            reporting_quarter=1,
            created_date=date.today(),
            created_by="test_user"
        )
        db_session.add(invalid_reporting_financials)
        db_session.commit()
    db_session.rollback()
    
    # Test currency field constraints
    with pytest.raises(IntegrityError):
        invalid_reporting_financials = ReportingFinancials(
            company_id=company.id,
            currency="INVALID",  # Invalid currency code
            exchange_rate_used=Decimal('1.0'),
            total_revenue=Decimal('1000000.00'),
            recurring_revenue=Decimal('800000.00'),
            gross_profit=Decimal('600000.00'),
            sales_marketing_expense=Decimal('200000.00'),
            total_operating_expense=Decimal('800000.00'),
            ebitda=Decimal('200000.00'),
            net_income=Decimal('150000.00'),
            cash_burn=Decimal('50000.00'),
            cash_balance=Decimal('500000.00'),
            fiscal_reporting_date=date(2023, 3, 31),
            fiscal_reporting_quarter=1,
            reporting_year=2023,
            reporting_quarter=1,
            created_date=date.today(),
            created_by="test_user"
        )
        db_session.add(invalid_reporting_financials)
        db_session.commit()
    db_session.rollback()

def test_reporting_metrics_model(db_session):
    """Test the ReportingMetrics model creation and constraints"""
    company = Company(
        name="Test Company",
        reporting_status="Active",
        reporting_currency="USD",
        fund="Test Fund",
        location_country="USA",
        customer_type="B2B",
        revenue_type="Subscription",
        year_end_date=date(2023, 12, 31),
        created_by="test_user"
    )
    db_session.add(company)
    db_session.commit()

    reporting_metrics = ReportingMetrics(
        company_id=company.id,
        currency="USD",
        arr=Decimal('960000.00'),
        gross_profit_margin=Decimal('60.00'),
        fiscal_reporting_date=date(2023, 3, 31),
        fiscal_reporting_quarter=1,
        reporting_year=2023,
        reporting_quarter=1,
        created_date=date.today(),
        created_by="test_user"
    )
    db_session.add(reporting_metrics)
    db_session.commit()
    
    # Assert that the ReportingMetrics object has the correct attributes
    assert reporting_metrics.company_id == company.id
    assert reporting_metrics.arr == Decimal('960000.00')
    assert reporting_metrics.gross_profit_margin == Decimal('60.00')
    
    # Test foreign key constraint with Company model
    with pytest.raises(IntegrityError):
        invalid_reporting_metrics = ReportingMetrics(
            company_id=company.id + 1,  # Non-existent company_id
            currency="USD",
            arr=Decimal('960000.00'),
            gross_profit_margin=Decimal('60.00'),
            fiscal_reporting_date=date(2023, 3, 31),
            fiscal_reporting_quarter=1,
            reporting_year=2023,
            reporting_quarter=1,
            created_date=date.today(),
            created_by="test_user"
        )
        db_session.add(invalid_reporting_metrics)
        db_session.commit()
    db_session.rollback()
    
    # Test non-nullable fields
    with pytest.raises(IntegrityError):
        invalid_reporting_metrics = ReportingMetrics(
            company_id=company.id,
            currency="USD",
            arr=None,  # This field is non-nullable
            gross_profit_margin=Decimal('60.00'),
            fiscal_reporting_date=date(2023, 3, 31),
            fiscal_reporting_quarter=1,
            reporting_year=2023,
            reporting_quarter=1,
            created_date=date.today(),
            created_by="test_user"
        )
        db_session.add(invalid_reporting_metrics)
        db_session.commit()
    db_session.rollback()
    
    # Test currency field constraints
    with pytest.raises(IntegrityError):
        invalid_reporting_metrics = ReportingMetrics(
            company_id=company.id,
            currency="INVALID",  # Invalid currency code
            arr=Decimal('960000.00'),
            gross_profit_margin=Decimal('60.00'),
            fiscal_reporting_date=date(2023, 3, 31),
            fiscal_reporting_quarter=1,
            reporting_year=2023,
            reporting_quarter=1,
            created_date=date.today(),
            created_by="test_user"
        )
        db_session.add(invalid_reporting_metrics)
        db_session.commit()
    db_session.rollback()

def test_model_relationships(db_session):
    """Test the relationships between models"""
    company = Company(
        name="Test Company",
        reporting_status="Active",
        reporting_currency="USD",
        fund="Test Fund",
        location_country="USA",
        customer_type="B2B",
        revenue_type="Subscription",
        year_end_date=date(2023, 12, 31),
        created_by="test_user"
    )
    db_session.add(company)
    db_session.commit()

    metrics_input = MetricsInput(
        company_id=company.id,
        currency="USD",
        total_revenue=1000000.0,
        recurring_revenue=800000.0,
        gross_profit=600000.0,
        sales_marketing_expense=200000.0,
        total_operating_expense=800000.0,
        ebitda=200000.0,
        net_income=150000.0,
        cash_burn=50000.0,
        cash_balance=500000.0,
        employees=100,
        fiscal_reporting_date=date(2023, 3, 31),
        fiscal_reporting_quarter=1,
        reporting_year=2023,
        reporting_quarter=1
    )
    db_session.add(metrics_input)

    reporting_financials = ReportingFinancials(
        company_id=company.id,
        currency="USD",
        exchange_rate_used=Decimal('1.0'),
        total_revenue=Decimal('1000000.00'),
        recurring_revenue=Decimal('800000.00'),
        gross_profit=Decimal('600000.00'),
        sales_marketing_expense=Decimal('200000.00'),
        total_operating_expense=Decimal('800000.00'),
        ebitda=Decimal('200000.00'),
        net_income=Decimal('150000.00'),
        cash_burn=Decimal('50000.00'),
        cash_balance=Decimal('500000.00'),
        fiscal_reporting_date=date(2023, 3, 31),
        fiscal_reporting_quarter=1,
        reporting_year=2023,
        reporting_quarter=1,
        created_date=date.today(),
        created_by="test_user"
    )
    db_session.add(reporting_financials)

    reporting_metrics = ReportingMetrics(
        company_id=company.id,
        currency="USD",
        arr=Decimal('960000.00'),
        gross_profit_margin=Decimal('60.00'),
        fiscal_reporting_date=date(2023, 3, 31),
        fiscal_reporting_quarter=1,
        reporting_year=2023,
        reporting_quarter=1,
        created_date=date.today(),
        created_by="test_user"
    )
    db_session.add(reporting_metrics)

    db_session.commit()
    
    # Test Company to MetricsInput relationship
    assert metrics_input in company.metrics_inputs
    assert metrics_input.company == company
    
    # Test Company to ReportingFinancials relationship
    assert reporting_financials in company.reporting_financials
    assert reporting_financials.company == company
    
    # Test Company to ReportingMetrics relationship
    assert reporting_metrics in company.reporting_metrics
    assert reporting_metrics.company == company

# Additional tests can be added here to cover more specific scenarios and edge cases