import pytest
from unittest.mock import Mock, patch
from freezegun import freeze_time
from decimal import Decimal
from uuid import UUID

from src.backend.services.data_transformation import DataTransformationService
from src.backend.models.metrics_input import MetricsInput
from src.backend.models.reporting_financials import ReportingFinancials
from src.backend.models.reporting_metrics import ReportingMetrics
from src.backend.db.session import AsyncSession

pytestmark = pytest.mark.asyncio

@pytest.fixture
async def mock_db_session():
    return Mock(spec=AsyncSession)

@pytest.fixture
async def mock_metrics_calculation_service():
    return Mock()

@pytest.fixture
async def data_transformation_service(mock_db_session, mock_metrics_calculation_service):
    service = DataTransformationService(db_session=mock_db_session)
    service.metrics_calculation_service = mock_metrics_calculation_service
    return service

@pytest.fixture
def mock_input_metrics():
    return MetricsInput(
        id=UUID('87654321-4321-8765-4321-876543210987'),
        company_id=UUID('12345678-1234-5678-1234-567812345678'),
        currency='USD',
        total_revenue=Decimal('1000000'),
        recurring_revenue=Decimal('800000'),
        gross_profit=Decimal('600000'),
        sales_marketing_expense=Decimal('200000'),
        total_operating_expense=Decimal('500000'),
        ebitda=Decimal('300000'),
        net_income=Decimal('250000'),
        cash_burn=Decimal('50000'),
        cash_balance=Decimal('1000000'),
        debt_outstanding=Decimal('500000'),
        employees=100,
        customers=1000,
        fiscal_reporting_date='2023-03-31',
        fiscal_reporting_quarter=1,
        reporting_year=2023,
        reporting_quarter=1
    )

async def test_transform_data(data_transformation_service, mock_db_session, mock_metrics_calculation_service, mock_input_metrics):
    company_id = UUID('12345678-1234-5678-1234-567812345678')
    reporting_year = 2023
    reporting_quarter = 1

    # Mock database query
    mock_db_session.execute.return_value.scalar_one_or_none.return_value = mock_input_metrics

    # Mock currency conversion
    with patch('src.backend.services.data_transformation.convert_currency') as mock_convert_currency, \
         patch('src.backend.services.data_transformation.get_exchange_rate') as mock_get_exchange_rate:
        mock_convert_currency.side_effect = lambda amount, from_currency, to_currency, date: amount * Decimal('1.25') if to_currency == 'CAD' else amount
        mock_get_exchange_rate.return_value = Decimal('1.25')

        # Mock metrics calculation
        mock_metrics = ReportingMetrics(
            company_id=company_id,
            currency='USD',
            enterprise_value=Decimal('10000000'),
            arr=Decimal('3200000'),
            recurring_percentage_revenue=Decimal('80'),
            revenue_per_fte=Decimal('10000'),
            gross_profit_per_fte=Decimal('6000'),
            employee_growth_rate=Decimal('10'),
            change_in_cash=Decimal('-50000'),
            revenue_growth=Decimal('20'),
            monthly_cash_burn=Decimal('16667'),
            runway_months=Decimal('60'),
            ev_by_equity_raised_plus_debt=Decimal('2'),
            sales_marketing_percentage_revenue=Decimal('20'),
            total_operating_percentage_revenue=Decimal('50'),
            gross_profit_margin=Decimal('60'),
            valuation_to_revenue=Decimal('10'),
            yoy_growth_revenue=Decimal('25'),
            yoy_growth_profit=Decimal('30'),
            yoy_growth_employees=Decimal('15'),
            yoy_growth_ltm_revenue=Decimal('22'),
            ltm_total_revenue=Decimal('3800000'),
            ltm_gross_profit=Decimal('2280000'),
            ltm_sales_marketing_expense=Decimal('760000'),
            ltm_gross_margin=Decimal('60'),
            ltm_operating_expense=Decimal('1900000'),
            ltm_ebitda=Decimal('1140000'),
            ltm_net_income=Decimal('950000'),
            ltm_ebitda_margin=Decimal('30'),
            ltm_net_income_margin=Decimal('25'),
            fiscal_reporting_date='2023-03-31',
            fiscal_reporting_quarter=1,
            reporting_year=2023,
            reporting_quarter=1
        )
        mock_metrics_calculation_service.calculate_derived_metrics.return_value = mock_metrics

        # Call the method under test
        with freeze_time("2023-04-15"):
            result_financials, result_metrics = await data_transformation_service.transform_data(company_id, reporting_year, reporting_quarter)

    # Assertions
    assert isinstance(result_financials, ReportingFinancials)
    assert isinstance(result_metrics, ReportingMetrics)

    # Check USD financials
    assert result_financials.company_id == company_id
    assert result_financials.currency == 'USD'
    assert result_financials.exchange_rate_used == Decimal('1')
    assert result_financials.total_revenue == Decimal('1000000')
    assert result_financials.recurring_revenue == Decimal('800000')
    assert result_financials.gross_profit == Decimal('600000')
    assert result_financials.sales_marketing_expense == Decimal('200000')
    assert result_financials.total_operating_expense == Decimal('500000')
    assert result_financials.ebitda == Decimal('300000')
    assert result_financials.net_income == Decimal('250000')
    assert result_financials.cash_burn == Decimal('50000')
    assert result_financials.cash_balance == Decimal('1000000')
    assert result_financials.debt_outstanding == Decimal('500000')

    # Check metrics
    assert result_metrics == mock_metrics

    # Verify method calls
    mock_db_session.execute.assert_called_once()
    mock_convert_currency.assert_called()
    mock_get_exchange_rate.assert_called()
    mock_metrics_calculation_service.calculate_derived_metrics.assert_called_once_with(company_id, reporting_year, reporting_quarter)
    mock_db_session.add.assert_called()
    mock_db_session.commit.assert_called()

async def test_convert_financials(data_transformation_service, mock_input_metrics):
    target_currencies = ['USD', 'CAD']

    with patch('src.backend.services.data_transformation.convert_currency') as mock_convert_currency, \
         patch('src.backend.services.data_transformation.get_exchange_rate') as mock_get_exchange_rate:
        mock_convert_currency.side_effect = lambda amount, from_currency, to_currency, date: amount * Decimal('1.25') if to_currency == 'CAD' else amount
        mock_get_exchange_rate.return_value = Decimal('1.25')

        # Call the method under test
        result = await data_transformation_service.convert_financials(mock_input_metrics, target_currencies)

    # Assertions
    assert isinstance(result, dict)
    assert len(result) == 2  # USD and CAD

    # Check USD financials
    usd_financials = result['USD']
    assert usd_financials['total_revenue'] == Decimal('1000000')
    assert usd_financials['recurring_revenue'] == Decimal('800000')
    assert usd_financials['gross_profit'] == Decimal('600000')
    assert usd_financials['sales_marketing_expense'] == Decimal('200000')
    assert usd_financials['total_operating_expense'] == Decimal('500000')
    assert usd_financials['ebitda'] == Decimal('300000')
    assert usd_financials['net_income'] == Decimal('250000')
    assert usd_financials['cash_burn'] == Decimal('50000')
    assert usd_financials['cash_balance'] == Decimal('1000000')
    assert usd_financials['debt_outstanding'] == Decimal('500000')
    assert usd_financials['exchange_rate_used'] == Decimal('1.0')

    # Check CAD financials
    cad_financials = result['CAD']
    assert cad_financials['total_revenue'] == Decimal('1250000')
    assert cad_financials['recurring_revenue'] == Decimal('1000000')
    assert cad_financials['gross_profit'] == Decimal('750000')
    assert cad_financials['sales_marketing_expense'] == Decimal('250000')
    assert cad_financials['total_operating_expense'] == Decimal('625000')
    assert cad_financials['ebitda'] == Decimal('375000')
    assert cad_financials['net_income'] == Decimal('312500')
    assert cad_financials['cash_burn'] == Decimal('62500')
    assert cad_financials['cash_balance'] == Decimal('1250000')
    assert cad_financials['debt_outstanding'] == Decimal('625000')
    assert cad_financials['exchange_rate_used'] == Decimal('1.25')

    # Verify method calls
    assert mock_convert_currency.call_count == 10  # Once for each financial field
    assert mock_get_exchange_rate.call_count == 1  # Once for CAD

async def test_update_reporting_financials(data_transformation_service, mock_db_session):
    company_id = UUID('12345678-1234-5678-1234-567812345678')
    reporting_year = 2023
    reporting_quarter = 1
    converted_financials = {
        'USD': {
            'total_revenue': Decimal('1000000'),
            'recurring_revenue': Decimal('800000'),
            'gross_profit': Decimal('600000'),
            'sales_marketing_expense': Decimal('200000'),
            'total_operating_expense': Decimal('500000'),
            'ebitda': Decimal('300000'),
            'net_income': Decimal('250000'),
            'cash_burn': Decimal('50000'),
            'cash_balance': Decimal('1000000'),
            'debt_outstanding': Decimal('500000'),
            'exchange_rate_used': Decimal('1.0')
        },
        'CAD': {
            'total_revenue': Decimal('1250000'),
            'recurring_revenue': Decimal('1000000'),
            'gross_profit': Decimal('750000'),
            'sales_marketing_expense': Decimal('250000'),
            'total_operating_expense': Decimal('625000'),
            'ebitda': Decimal('375000'),
            'net_income': Decimal('312500'),
            'cash_burn': Decimal('62500'),
            'cash_balance': Decimal('1250000'),
            'debt_outstanding': Decimal('625000'),
            'exchange_rate_used': Decimal('1.25')
        }
    }

    # Mock the database query to return None (simulating no existing record)
    mock_db_session.execute.return_value.scalar_one_or_none.return_value = None

    # Call the method under test
    with freeze_time("2023-04-15"):
        result = await data_transformation_service.update_reporting_financials(
            company_id, reporting_year, reporting_quarter, converted_financials
        )

    # Assertions
    assert isinstance(result, dict)
    assert len(result) == 2  # USD and CAD

    for currency in ['USD', 'CAD']:
        financials = result[currency]
        assert isinstance(financials, ReportingFinancials)
        assert financials.company_id == company_id
        assert financials.currency == currency
        assert financials.exchange_rate_used == converted_financials[currency]['exchange_rate_used']
        assert financials.total_revenue == converted_financials[currency]['total_revenue']
        assert financials.recurring_revenue == converted_financials[currency]['recurring_revenue']
        assert financials.gross_profit == converted_financials[currency]['gross_profit']
        assert financials.sales_marketing_expense == converted_financials[currency]['sales_marketing_expense']
        assert financials.total_operating_expense == converted_financials[currency]['total_operating_expense']
        assert financials.ebitda == converted_financials[currency]['ebitda']
        assert financials.net_income == converted_financials[currency]['net_income']
        assert financials.cash_burn == converted_financials[currency]['cash_burn']
        assert financials.cash_balance == converted_financials[currency]['cash_balance']
        assert financials.debt_outstanding == converted_financials[currency]['debt_outstanding']
        assert financials.reporting_year == reporting_year
        assert financials.reporting_quarter == reporting_quarter

    # Verify method calls
    assert mock_db_session.execute.call_count == 2  # Once for each currency
    assert mock_db_session.add.call_count == 2  # Once for each new ReportingFinancials instance

if __name__ == "__main__":
    pytest.main()