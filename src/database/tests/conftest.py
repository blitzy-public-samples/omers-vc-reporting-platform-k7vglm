"""
This module contains pytest fixtures and configuration for database testing in the financial reporting metrics backend system.

Requirements addressed:
- Database Testing (3. SYSTEM COMPONENTS ARCHITECTURE/3.2 SEQUENCE DIAGRAMS)
- Test Isolation (6. SECURITY CONSIDERATIONS/6.2 DATA SECURITY)
"""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator, Dict, Any

from src.database.config import get_database_settings
from src.database.base import Base
from src.database.models import Company, MetricsInput, ReportingFinancials, ReportingMetrics
from src.database.schemas import (
    CompanyCreate,
    MetricsInputCreate,
    ReportingFinancialsCreate,
    ReportingMetricsCreate
)

# Global variable for test database URL
TEST_DATABASE_URL = get_database_settings().DATABASE_URL + '_test'

def pytest_configure(config):
    """
    Pytest hook to configure the test environment
    
    This function sets up any global test configurations and configures pytest markers for database tests.
    
    Args:
        config (pytest.Config): The pytest configuration object
    """
    config.addinivalue_line("markers", "db: mark test as requiring database access")

def create_test_database():
    """
    Create a test database and tables
    
    This function creates a new database engine using TEST_DATABASE_URL,
    creates all tables defined in Base.metadata, and closes the engine connection.
    """
    engine = create_engine(TEST_DATABASE_URL)
    Base.metadata.create_all(bind=engine)
    engine.dispose()

def drop_test_database():
    """
    Drop the test database and all its tables
    
    This function creates a new database engine using TEST_DATABASE_URL,
    drops all tables defined in Base.metadata, and closes the engine connection.
    """
    engine = create_engine(TEST_DATABASE_URL)
    Base.metadata.drop_all(bind=engine)
    engine.dispose()

@pytest.fixture(scope="function")
def db() -> Generator[Session, None, None]:
    """
    Pytest fixture to provide a database session for tests
    
    This fixture creates a new database engine using TEST_DATABASE_URL,
    creates a new SessionLocal bound to the test engine, creates a new database session,
    yields the session for use in tests, rolls back any changes after the test, and closes the session.
    
    Yields:
        Generator[Session, None, None]: A database session
    """
    engine = create_engine(TEST_DATABASE_URL)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.rollback()
        session.close()

@pytest.fixture(scope="function")
def test_data(db: Session) -> Dict[str, Any]:
    """
    Pytest fixture to provide test data for database tests
    
    This fixture creates test Company, MetricsInput, ReportingFinancials, and ReportingMetrics objects,
    adds them to the database session, commits the changes, and returns a dictionary with all created test objects.
    
    Args:
        db (Session): The database session
    
    Returns:
        Dict[str, Any]: A dictionary containing test data objects
    """
    # Create test Company objects
    company1 = Company(**CompanyCreate(
        name="Test Company 1",
        reporting_status="Active",
        reporting_currency="USD",
        fund="Fund A",
        location_country="USA",
        customer_type="B2B",
        revenue_type="SaaS",
        equity_raised=1000000.00,
        post_money_valuation=5000000.00,
        year_end_date="2023-12-31"
    ).dict())
    company2 = Company(**CompanyCreate(
        name="Test Company 2",
        reporting_status="Inactive",
        reporting_currency="EUR",
        fund="Fund B",
        location_country="Germany",
        customer_type="B2C",
        revenue_type="E-commerce",
        equity_raised=2000000.00,
        post_money_valuation=10000000.00,
        year_end_date="2023-12-31"
    ).dict())
    db.add_all([company1, company2])
    db.flush()

    # Create test MetricsInput objects
    metrics_input1 = MetricsInput(**MetricsInputCreate(
        company_id=company1.id,
        currency="USD",
        total_revenue=1000000.00,
        recurring_revenue=800000.00,
        gross_profit=600000.00,
        sales_marketing_expense=200000.00,
        total_operating_expense=800000.00,
        ebitda=200000.00,
        net_income=150000.00,
        cash_burn=50000.00,
        cash_balance=500000.00,
        debt_outstanding=100000.00,
        employees=50,
        customers=100,
        fiscal_reporting_date="2023-03-31",
        fiscal_reporting_quarter=1,
        reporting_year=2023,
        reporting_quarter=1
    ).dict())
    db.add(metrics_input1)
    db.flush()

    # Create test ReportingFinancials objects
    reporting_financials1 = ReportingFinancials(**ReportingFinancialsCreate(
        company_id=company1.id,
        currency="USD",
        exchange_rate_used=1.0,
        total_revenue=1000000.00,
        recurring_revenue=800000.00,
        gross_profit=600000.00,
        debt_outstanding=100000.00,
        sales_marketing_expense=200000.00,
        total_operating_expense=800000.00,
        ebitda=200000.00,
        net_income=150000.00,
        cash_burn=50000.00,
        cash_balance=500000.00,
        fiscal_reporting_date="2023-03-31",
        fiscal_reporting_quarter=1,
        reporting_year=2023,
        reporting_quarter=1
    ).dict())
    db.add(reporting_financials1)
    db.flush()

    # Create test ReportingMetrics objects
    reporting_metrics1 = ReportingMetrics(**ReportingMetricsCreate(
        company_id=company1.id,
        currency="USD",
        enterprise_value=5100000.00,
        arr=3200000.00,
        recurring_percentage_revenue=80.00,
        revenue_per_fte=20000.00,
        gross_profit_per_fte=12000.00,
        employee_growth_rate=10.00,
        change_in_cash=-50000.00,
        revenue_growth=20.00,
        monthly_cash_burn=16666.67,
        runway_months=30.0,
        ev_by_equity_raised_plus_debt=4.64,
        sales_marketing_percentage_revenue=20.00,
        total_operating_percentage_revenue=80.00,
        gross_profit_margin=60.00,
        valuation_to_revenue=5.10,
        yoy_growth_revenue=20.00,
        yoy_growth_profit=15.00,
        yoy_growth_employees=10.00,
        yoy_growth_ltm_revenue=18.00,
        ltm_total_revenue=3800000.00,
        ltm_gross_profit=2280000.00,
        ltm_sales_marketing_expense=760000.00,
        ltm_gross_margin=60.00,
        ltm_operating_expense=3040000.00,
        ltm_ebitda=760000.00,
        ltm_net_income=570000.00,
        ltm_ebitda_margin=20.00,
        ltm_net_income_margin=15.00,
        fiscal_reporting_date="2023-03-31",
        fiscal_reporting_quarter=1,
        reporting_year=2023,
        reporting_quarter=1
    ).dict())
    db.add(reporting_metrics1)

    db.commit()

    return {
        "companies": [company1, company2],
        "metrics_inputs": [metrics_input1],
        "reporting_financials": [reporting_financials1],
        "reporting_metrics": [reporting_metrics1]
    }

def pytest_sessionstart(session):
    """
    Pytest hook to set up the test environment before running tests
    
    This function creates the test database before running any tests.
    """
    create_test_database()

def pytest_sessionfinish(session, exitstatus):
    """
    Pytest hook to clean up the test environment after running tests
    
    This function drops the test database after all tests have run.
    """
    drop_test_database()