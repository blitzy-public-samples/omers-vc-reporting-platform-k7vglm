import asyncio
from decimal import Decimal
from typing import Dict, List, Tuple
from uuid import UUID

from src.backend.services.currency_conversion import convert_currency, get_exchange_rate
from src.backend.services.metrics_calculation import MetricsCalculationService
from src.backend.models.metrics_input import MetricsInput
from src.backend.models.reporting_financials import ReportingFinancials
from src.backend.models.reporting_metrics import ReportingMetrics
from src.backend.db.session import AsyncSession
from src.backend.utils.logging import get_logger

logger = get_logger(__name__)

class DataTransformationService:
    """
    Service class for orchestrating data transformation processes.
    
    This class is responsible for transforming input data by converting currencies
    and calculating metrics for financial reporting.
    
    Requirements addressed:
    - Data Transformation Process (1.2 Scope/Core Functionalities)
    - Multi-Currency Support (1.2 Scope/Core Functionalities)
    """

    def __init__(self, db_session: AsyncSession):
        """
        Initialize the DataTransformationService.

        Args:
            db_session (AsyncSession): The asynchronous database session for database operations.
        """
        self.db_session = db_session
        self.metrics_calculation_service = MetricsCalculationService()

    async def transform_data(self, company_id: UUID, reporting_year: int, reporting_quarter: int) -> Tuple[ReportingFinancials, ReportingMetrics]:
        """
        Transform input data by converting currencies and calculating metrics.

        Args:
            company_id (UUID): The ID of the company.
            reporting_year (int): The reporting year.
            reporting_quarter (int): The reporting quarter.

        Returns:
            Tuple[ReportingFinancials, ReportingMetrics]: Transformed financial data and calculated metrics.

        Raises:
            ValueError: If no input metrics are found for the specified company and reporting period.
        """
        logger.info(f"Starting data transformation for company {company_id}, year {reporting_year}, quarter {reporting_quarter}")

        # Retrieve the latest MetricsInput for the given company and reporting period
        input_metrics = await self.db_session.execute(
            self.db_session.query(MetricsInput).filter(
                MetricsInput.company_id == company_id,
                MetricsInput.reporting_year == reporting_year,
                MetricsInput.reporting_quarter == reporting_quarter
            )
        )
        input_metrics = input_metrics.scalar_one_or_none()

        if not input_metrics:
            logger.error(f"No input metrics found for company {company_id}, year {reporting_year}, quarter {reporting_quarter}")
            raise ValueError("No input metrics found for the specified company and reporting period")

        # Convert financial data to USD and CAD
        target_currencies = ['USD', 'CAD']
        converted_financials = await self.convert_financials(input_metrics, target_currencies)

        # Create or update ReportingFinancials instances for local currency, USD, and CAD
        reporting_financials = await self.update_reporting_financials(company_id, reporting_year, reporting_quarter, converted_financials)

        # Calculate derived metrics using MetricsCalculationService
        reporting_metrics = await self.metrics_calculation_service.calculate_derived_metrics(company_id, reporting_year, reporting_quarter)

        # Save ReportingFinancials and ReportingMetrics instances to the database
        for financials in reporting_financials.values():
            self.db_session.add(financials)
        self.db_session.add(reporting_metrics)
        await self.db_session.commit()

        logger.info(f"Data transformation completed for company {company_id}, year {reporting_year}, quarter {reporting_quarter}")

        return reporting_financials[input_metrics.currency], reporting_metrics

    async def convert_financials(self, input_metrics: MetricsInput, target_currencies: List[str]) -> Dict[str, Dict[str, Decimal]]:
        """
        Convert financial data to specified currencies.

        Args:
            input_metrics (MetricsInput): The input metrics to convert.
            target_currencies (List[str]): The list of target currencies for conversion.

        Returns:
            Dict[str, Dict[str, Decimal]]: Converted financial data for each target currency.
        """
        converted_financials = {input_metrics.currency: {}}
        source_currency = input_metrics.currency
        conversion_date = input_metrics.fiscal_reporting_date

        for target_currency in target_currencies:
            if target_currency != source_currency:
                converted_financials[target_currency] = {}

                for field in ['total_revenue', 'recurring_revenue', 'gross_profit', 'sales_marketing_expense',
                              'total_operating_expense', 'ebitda', 'net_income', 'cash_burn', 'cash_balance', 'debt_outstanding']:
                    source_value = getattr(input_metrics, field)
                    if source_value is not None:
                        converted_value = await convert_currency(source_value, source_currency, target_currency, conversion_date)
                        converted_financials[target_currency][field] = converted_value
                    else:
                        converted_financials[target_currency][field] = None

                # Add exchange rate used for the conversion
                exchange_rate = await get_exchange_rate(source_currency, target_currency, conversion_date)
                converted_financials[target_currency]['exchange_rate_used'] = exchange_rate
            else:
                # For the source currency, use the original values
                for field in ['total_revenue', 'recurring_revenue', 'gross_profit', 'sales_marketing_expense',
                              'total_operating_expense', 'ebitda', 'net_income', 'cash_burn', 'cash_balance', 'debt_outstanding']:
                    converted_financials[source_currency][field] = getattr(input_metrics, field)
                converted_financials[source_currency]['exchange_rate_used'] = Decimal('1.0')

        return converted_financials

    async def update_reporting_financials(self, company_id: UUID, reporting_year: int, reporting_quarter: int,
                                          converted_financials: Dict[str, Dict[str, Decimal]]) -> Dict[str, ReportingFinancials]:
        """
        Update or create ReportingFinancials instances for each currency.

        Args:
            company_id (UUID): The ID of the company.
            reporting_year (int): The reporting year.
            reporting_quarter (int): The reporting quarter.
            converted_financials (Dict[str, Dict[str, Decimal]]): Converted financial data for each currency.

        Returns:
            Dict[str, ReportingFinancials]: Updated ReportingFinancials instances for each currency.
        """
        reporting_financials = {}

        for currency, financials in converted_financials.items():
            existing_financials = await self.db_session.execute(
                self.db_session.query(ReportingFinancials).filter(
                    ReportingFinancials.company_id == company_id,
                    ReportingFinancials.currency == currency,
                    ReportingFinancials.reporting_year == reporting_year,
                    ReportingFinancials.reporting_quarter == reporting_quarter
                )
            )
            existing_financials = existing_financials.scalar_one_or_none()

            if existing_financials:
                # Update existing instance
                for field, value in financials.items():
                    setattr(existing_financials, field, value)
                reporting_financials[currency] = existing_financials
            else:
                # Create new instance
                new_financials = ReportingFinancials(
                    company_id=company_id,
                    currency=currency,
                    reporting_year=reporting_year,
                    reporting_quarter=reporting_quarter,
                    **financials
                )
                reporting_financials[currency] = new_financials

        return reporting_financials