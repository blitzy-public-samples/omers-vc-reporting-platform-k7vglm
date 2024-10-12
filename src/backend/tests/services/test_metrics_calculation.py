import pytest
from unittest.mock import Mock, patch
from decimal import Decimal
from uuid import UUID

from src.backend.services.metrics_calculation import MetricsCalculationService
from src.backend.models.reporting_metrics import ReportingMetrics
from src.backend.models.metrics_input import MetricsInput

# Pytest version: ^6.2.0

@pytest.fixture
def mock_db():
    return Mock()

@pytest.fixture
def test_input():
    return {
        "company_id": UUID("12345678-1234-5678-1234-567812345678"),
        "reporting_year": 2023,
        "reporting_quarter": 2,
        "currency": "USD",
        "total_revenue": Decimal("1000000"),
        "recurring_revenue": Decimal("800000"),
        "gross_profit": Decimal("600000"),
        "employees": 50,
        "cash_burn": Decimal("200000"),
        "cash_balance": Decimal("1000000"),
        "sales_marketing_expense": Decimal("150000"),
        "total_operating_expense": Decimal("800000"),
        "ebitda": Decimal("200000"),
        "net_income": Decimal("150000"),
        "fiscal_reporting_date": "2023-06-30",
        "fiscal_reporting_quarter": 2,
    }

@pytest.mark.asyncio
async def test_calculate_derived_metrics(mock_db, test_input):
    """
    Test the calculate_derived_metrics method of MetricsCalculationService.
    This test verifies the accuracy of automated calculations for derivative metrics.
    Requirement: Automated Calculations (1.1 System Objectives/3. Automate Calculations)
    """
    # Mock the retrieval of input metrics from the database
    mock_db.query.return_value.filter.return_value.first.return_value = MetricsInput(**test_input)

    # Initialize the MetricsCalculationService
    service = MetricsCalculationService()

    # Call the calculate_derived_metrics method
    result = service.calculate_derived_metrics(
        mock_db,
        test_input["company_id"],
        test_input["reporting_year"],
        test_input["reporting_quarter"]
    )

    # Assert that the returned object is an instance of ReportingMetrics
    assert isinstance(result, ReportingMetrics)

    # Assert that the calculated values match the expected results
    assert result.arr == Decimal("3200000")  # 800000 * 4
    assert result.recurring_percentage_revenue == Decimal("80.00")  # (800000 / 1000000) * 100
    assert result.revenue_per_fte == Decimal("20000.00")  # 1000000 / 50
    assert result.gross_profit_per_fte == Decimal("12000.00")  # 600000 / 50
    assert result.monthly_cash_burn == Decimal("66666.67")  # 200000 / 3
    assert result.runway_months == Decimal("15.0")  # 1000000 / 66666.67
    assert result.sales_marketing_percentage_revenue == Decimal("15.00")  # (150000 / 1000000) * 100
    assert result.total_operating_percentage_revenue == Decimal("80.00")  # (800000 / 1000000) * 100
    assert result.gross_profit_margin == Decimal("60.00")  # (600000 / 1000000) * 100

def test_calculate_arr():
    """
    Test the calculate_arr method of MetricsCalculationService.
    This test verifies the accuracy of the ARR calculation.
    Requirement: Automated Calculations (1.1 System Objectives/3. Automate Calculations)
    """
    service = MetricsCalculationService()
    result = service.calculate_arr(Decimal("100000"))
    assert result == Decimal("400000")

def test_calculate_recurring_percentage_revenue():
    """
    Test the calculate_recurring_percentage_revenue method of MetricsCalculationService.
    This test verifies the accuracy of the recurring percentage of revenue calculation.
    Requirement: Automated Calculations (1.1 System Objectives/3. Automate Calculations)
    """
    service = MetricsCalculationService()
    result = service.calculate_recurring_percentage_revenue(Decimal("80000"), Decimal("100000"))
    assert result == Decimal("80.00")

def test_calculate_revenue_per_fte():
    """
    Test the calculate_revenue_per_fte method of MetricsCalculationService.
    This test verifies the accuracy of the revenue per FTE calculation.
    Requirement: Automated Calculations (1.1 System Objectives/3. Automate Calculations)
    """
    service = MetricsCalculationService()
    result = service.calculate_revenue_per_fte(Decimal("1000000"), 50)
    assert result == Decimal("20000.00")

def test_calculate_gross_profit_per_fte():
    """
    Test the calculate_gross_profit_per_fte method of MetricsCalculationService.
    This test verifies the accuracy of the gross profit per FTE calculation.
    Requirement: Automated Calculations (1.1 System Objectives/3. Automate Calculations)
    """
    service = MetricsCalculationService()
    result = service.calculate_gross_profit_per_fte(Decimal("600000"), 50)
    assert result == Decimal("12000.00")

def test_calculate_employee_growth_rate():
    """
    Test the calculate_employee_growth_rate method of MetricsCalculationService.
    This test verifies the accuracy of the employee growth rate calculation.
    Requirement: Automated Calculations (1.1 System Objectives/3. Automate Calculations)
    """
    service = MetricsCalculationService()
    result = service.calculate_employee_growth_rate(55, 50)
    assert result == Decimal("10.00")

def test_calculate_revenue_growth():
    """
    Test the calculate_revenue_growth method of MetricsCalculationService.
    This test verifies the accuracy of the revenue growth calculation.
    Requirement: Automated Calculations (1.1 System Objectives/3. Automate Calculations)
    """
    service = MetricsCalculationService()
    result = service.calculate_revenue_growth(Decimal("1100000"), Decimal("1000000"))
    assert result == Decimal("10.00")

def test_calculate_monthly_cash_burn():
    """
    Test the calculate_monthly_cash_burn method of MetricsCalculationService.
    This test verifies the accuracy of the monthly cash burn calculation.
    Requirement: Automated Calculations (1.1 System Objectives/3. Automate Calculations)
    """
    service = MetricsCalculationService()
    result = service.calculate_monthly_cash_burn(Decimal("300000"))
    assert result == Decimal("100000")

def test_calculate_runway_months():
    """
    Test the calculate_runway_months method of MetricsCalculationService.
    This test verifies the accuracy of the runway months calculation.
    Requirement: Automated Calculations (1.1 System Objectives/3. Automate Calculations)
    """
    service = MetricsCalculationService()
    result = service.calculate_runway_months(Decimal("1000000"), Decimal("100000"))
    assert result == Decimal("10.0")

def test_calculate_ltm_metrics():
    """
    Test the calculate_ltm_metrics method of MetricsCalculationService.
    This test verifies the accuracy of the LTM metrics calculations.
    Requirement: Automated Calculations (1.1 System Objectives/3. Automate Calculations)
    """
    service = MetricsCalculationService()
    quarterly_metrics = [
        MetricsInput(total_revenue=Decimal("1000000"), gross_profit=Decimal("600000"), sales_marketing_expense=Decimal("200000"), total_operating_expense=Decimal("800000"), ebitda=Decimal("200000"), net_income=Decimal("150000")),
        MetricsInput(total_revenue=Decimal("1100000"), gross_profit=Decimal("660000"), sales_marketing_expense=Decimal("220000"), total_operating_expense=Decimal("880000"), ebitda=Decimal("220000"), net_income=Decimal("165000")),
        MetricsInput(total_revenue=Decimal("1200000"), gross_profit=Decimal("720000"), sales_marketing_expense=Decimal("240000"), total_operating_expense=Decimal("960000"), ebitda=Decimal("240000"), net_income=Decimal("180000")),
        MetricsInput(total_revenue=Decimal("1300000"), gross_profit=Decimal("780000"), sales_marketing_expense=Decimal("260000"), total_operating_expense=Decimal("1040000"), ebitda=Decimal("260000"), net_income=Decimal("195000"))
    ]
    result = service.calculate_ltm_metrics(quarterly_metrics)
    
    assert result["ltm_total_revenue"] == Decimal("4600000")
    assert result["ltm_gross_profit"] == Decimal("2760000")
    assert result["ltm_sales_marketing_expense"] == Decimal("920000")
    assert result["ltm_gross_margin"] == Decimal("60.00")
    assert result["ltm_operating_expense"] == Decimal("3680000")
    assert result["ltm_ebitda"] == Decimal("920000")
    assert result["ltm_net_income"] == Decimal("690000")
    assert result["ltm_ebitda_margin"] == Decimal("20.00")
    assert result["ltm_net_income_margin"] == Decimal("15.00")

def test_calculate_percentage_of_revenue():
    """
    Test the calculate_percentage_of_revenue method of MetricsCalculationService.
    This test verifies the accuracy of the percentage of revenue calculation.
    Requirement: Automated Calculations (1.1 System Objectives/3. Automate Calculations)
    """
    service = MetricsCalculationService()
    result = service.calculate_percentage_of_revenue(Decimal("200000"), Decimal("1000000"))
    assert result == Decimal("20.00")

def test_calculate_per_fte():
    """
    Test the calculate_per_fte method of MetricsCalculationService.
    This test verifies the accuracy of the per FTE calculation.
    Requirement: Automated Calculations (1.1 System Objectives/3. Automate Calculations)
    """
    service = MetricsCalculationService()
    result = service.calculate_per_fte(Decimal("1000000"), 50)
    assert result == Decimal("20000.00")

def test_calculate_growth_rate():
    """
    Test the calculate_growth_rate method of MetricsCalculationService.
    This test verifies the accuracy of the growth rate calculation.
    Requirement: Automated Calculations (1.1 System Objectives/3. Automate Calculations)
    """
    service = MetricsCalculationService()
    result = service.calculate_growth_rate(Decimal("1100000"), Decimal("1000000"))
    assert result == Decimal("10.00")