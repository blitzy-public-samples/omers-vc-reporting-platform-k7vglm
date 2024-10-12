from datetime import datetime
from decimal import Decimal
from typing import List, Dict
from uuid import UUID

from sqlalchemy.orm import Session

from src.backend.models.metrics_input import MetricsInput
from src.backend.models.reporting_metrics import ReportingMetrics
from src.backend.db.session import db

class MetricsCalculationService:
    """
    Service class for calculating derived metrics based on input metrics.
    
    This class implements the requirements:
    - Data Transformation (1.2 Scope/Core Functionalities/3. Data Transformation)
    - Automated Calculations (1.1 System Objectives/3. Automate Calculations)
    """

    @staticmethod
    def calculate_derived_metrics(db: Session, company_id: UUID, reporting_year: int, reporting_quarter: int) -> ReportingMetrics:
        """
        Calculates derived metrics for a given company and reporting period.

        Args:
            db (Session): The database session.
            company_id (UUID): The ID of the company.
            reporting_year (int): The reporting year.
            reporting_quarter (int): The reporting quarter.

        Returns:
            ReportingMetrics: Calculated reporting metrics.

        Raises:
            ValueError: If no input metrics are found for the given company and reporting period.
        """
        # Retrieve input metrics for the given company and reporting period
        input_metrics = db.query(MetricsInput).filter(
            MetricsInput.company_id == company_id,
            MetricsInput.reporting_year == reporting_year,
            MetricsInput.reporting_quarter == reporting_quarter
        ).first()

        if not input_metrics:
            raise ValueError(f"No input metrics found for company {company_id} in {reporting_year} Q{reporting_quarter}")

        # Calculate derived metrics
        arr = MetricsCalculationService.calculate_arr(input_metrics.recurring_revenue)
        recurring_percentage_revenue = MetricsCalculationService.calculate_recurring_percentage_revenue(
            input_metrics.recurring_revenue, input_metrics.total_revenue
        )
        revenue_per_fte = MetricsCalculationService.calculate_revenue_per_fte(
            input_metrics.total_revenue, input_metrics.employees
        )
        gross_profit_per_fte = MetricsCalculationService.calculate_gross_profit_per_fte(
            input_metrics.gross_profit, input_metrics.employees
        )
        monthly_cash_burn = MetricsCalculationService.calculate_monthly_cash_burn(input_metrics.cash_burn)
        runway_months = MetricsCalculationService.calculate_runway_months(
            input_metrics.cash_balance, monthly_cash_burn
        )

        # Calculate additional metrics
        sales_marketing_percentage_revenue = MetricsCalculationService.calculate_percentage_of_revenue(
            input_metrics.sales_marketing_expense, input_metrics.total_revenue
        )
        total_operating_percentage_revenue = MetricsCalculationService.calculate_percentage_of_revenue(
            input_metrics.total_operating_expense, input_metrics.total_revenue
        )
        gross_profit_margin = MetricsCalculationService.calculate_percentage_of_revenue(
            input_metrics.gross_profit, input_metrics.total_revenue
        )

        # Create and return a new ReportingMetrics instance with calculated values
        return ReportingMetrics(
            company_id=company_id,
            currency=input_metrics.currency,
            arr=arr,
            recurring_percentage_revenue=recurring_percentage_revenue,
            revenue_per_fte=revenue_per_fte,
            gross_profit_per_fte=gross_profit_per_fte,
            monthly_cash_burn=monthly_cash_burn,
            runway_months=runway_months,
            sales_marketing_percentage_revenue=sales_marketing_percentage_revenue,
            total_operating_percentage_revenue=total_operating_percentage_revenue,
            gross_profit_margin=gross_profit_margin,
            fiscal_reporting_date=input_metrics.fiscal_reporting_date,
            fiscal_reporting_quarter=input_metrics.fiscal_reporting_quarter,
            reporting_year=reporting_year,
            reporting_quarter=reporting_quarter,
            created_date=datetime.utcnow().date(),
            created_by="MetricsCalculationService"
        )

    @staticmethod
    def calculate_arr(recurring_revenue: Decimal) -> Decimal:
        """
        Calculates Annual Recurring Revenue (ARR).

        Args:
            recurring_revenue (Decimal): The recurring revenue for the quarter.

        Returns:
            Decimal: Calculated ARR.
        """
        return recurring_revenue * 4

    @staticmethod
    def calculate_recurring_percentage_revenue(recurring_revenue: Decimal, total_revenue: Decimal) -> Decimal:
        """
        Calculates recurring percentage of revenue.

        Args:
            recurring_revenue (Decimal): The recurring revenue for the quarter.
            total_revenue (Decimal): The total revenue for the quarter.

        Returns:
            Decimal: Calculated recurring percentage of revenue.
        """
        return MetricsCalculationService.calculate_percentage_of_revenue(recurring_revenue, total_revenue)

    @staticmethod
    def calculate_revenue_per_fte(total_revenue: Decimal, employees: int) -> Decimal:
        """
        Calculates revenue per full-time equivalent employee.

        Args:
            total_revenue (Decimal): The total revenue for the quarter.
            employees (int): The number of employees.

        Returns:
            Decimal: Calculated revenue per FTE.
        """
        return MetricsCalculationService.calculate_per_fte(total_revenue, employees)

    @staticmethod
    def calculate_gross_profit_per_fte(gross_profit: Decimal, employees: int) -> Decimal:
        """
        Calculates gross profit per full-time equivalent employee.

        Args:
            gross_profit (Decimal): The gross profit for the quarter.
            employees (int): The number of employees.

        Returns:
            Decimal: Calculated gross profit per FTE.
        """
        return MetricsCalculationService.calculate_per_fte(gross_profit, employees)

    @staticmethod
    def calculate_employee_growth_rate(current_employees: int, previous_employees: int) -> Decimal:
        """
        Calculates employee growth rate compared to the previous quarter.

        Args:
            current_employees (int): The current number of employees.
            previous_employees (int): The number of employees in the previous quarter.

        Returns:
            Decimal: Calculated employee growth rate.
        """
        return MetricsCalculationService.calculate_growth_rate(Decimal(current_employees), Decimal(previous_employees))

    @staticmethod
    def calculate_revenue_growth(current_revenue: Decimal, previous_revenue: Decimal) -> Decimal:
        """
        Calculates revenue growth rate compared to the previous quarter.

        Args:
            current_revenue (Decimal): The current quarter's revenue.
            previous_revenue (Decimal): The previous quarter's revenue.

        Returns:
            Decimal: Calculated revenue growth rate.
        """
        return MetricsCalculationService.calculate_growth_rate(current_revenue, previous_revenue)

    @staticmethod
    def calculate_monthly_cash_burn(cash_burn: Decimal) -> Decimal:
        """
        Calculates monthly cash burn rate.

        Args:
            cash_burn (Decimal): The quarterly cash burn.

        Returns:
            Decimal: Calculated monthly cash burn rate.
        """
        return cash_burn / 3

    @staticmethod
    def calculate_runway_months(cash_balance: Decimal, monthly_cash_burn: Decimal) -> Decimal:
        """
        Calculates runway in months.

        Args:
            cash_balance (Decimal): The current cash balance.
            monthly_cash_burn (Decimal): The monthly cash burn rate.

        Returns:
            Decimal: Calculated runway in months.
        """
        if monthly_cash_burn == 0:
            return Decimal('0')
        return (cash_balance / monthly_cash_burn).quantize(Decimal('0.1'))

    @staticmethod
    def calculate_ltm_metrics(quarterly_metrics: List[MetricsInput]) -> Dict[str, Decimal]:
        """
        Calculates Last Twelve Months (LTM) metrics.

        Args:
            quarterly_metrics (List[MetricsInput]): List of quarterly metrics for the last four quarters.

        Returns:
            Dict[str, Decimal]: Calculated LTM metrics.

        Raises:
            ValueError: If the input list doesn't contain exactly 4 quarters of data.
        """
        if len(quarterly_metrics) != 4:
            raise ValueError("LTM calculations require exactly 4 quarters of data")

        ltm_total_revenue = sum(q.total_revenue for q in quarterly_metrics)
        ltm_gross_profit = sum(q.gross_profit for q in quarterly_metrics)
        ltm_sales_marketing_expense = sum(q.sales_marketing_expense for q in quarterly_metrics)
        ltm_operating_expense = sum(q.total_operating_expense for q in quarterly_metrics)
        ltm_ebitda = sum(q.ebitda for q in quarterly_metrics)
        ltm_net_income = sum(q.net_income for q in quarterly_metrics)

        return {
            "ltm_total_revenue": ltm_total_revenue,
            "ltm_gross_profit": ltm_gross_profit,
            "ltm_sales_marketing_expense": ltm_sales_marketing_expense,
            "ltm_gross_margin": MetricsCalculationService.calculate_percentage_of_revenue(ltm_gross_profit, ltm_total_revenue),
            "ltm_operating_expense": ltm_operating_expense,
            "ltm_ebitda": ltm_ebitda,
            "ltm_net_income": ltm_net_income,
            "ltm_ebitda_margin": MetricsCalculationService.calculate_percentage_of_revenue(ltm_ebitda, ltm_total_revenue),
            "ltm_net_income_margin": MetricsCalculationService.calculate_percentage_of_revenue(ltm_net_income, ltm_total_revenue)
        }

    @staticmethod
    def calculate_percentage_of_revenue(value: Decimal, total_revenue: Decimal) -> Decimal:
        """
        Calculates the percentage of a value relative to total revenue.

        Args:
            value (Decimal): The value to calculate the percentage for.
            total_revenue (Decimal): The total revenue.

        Returns:
            Decimal: Calculated percentage.
        """
        if total_revenue == 0:
            return Decimal('0')
        return (value / total_revenue * 100).quantize(Decimal('0.01'))

    @staticmethod
    def calculate_per_fte(value: Decimal, employees: int) -> Decimal:
        """
        Calculates a value per full-time equivalent employee.

        Args:
            value (Decimal): The value to calculate per FTE.
            employees (int): The number of employees.

        Returns:
            Decimal: Calculated value per FTE.
        """
        if employees == 0:
            return Decimal('0')
        return (value / Decimal(employees)).quantize(Decimal('0.01'))

    @staticmethod
    def calculate_growth_rate(current_value: Decimal, previous_value: Decimal) -> Decimal:
        """
        Calculates the growth rate between two values.

        Args:
            current_value (Decimal): The current value.
            previous_value (Decimal): The previous value.

        Returns:
            Decimal: Calculated growth rate.
        """
        if previous_value == 0:
            return Decimal('0')
        return ((current_value - previous_value) / previous_value * 100).quantize(Decimal('0.01'))