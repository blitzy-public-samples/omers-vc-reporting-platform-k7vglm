from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from src.database.base import Base
import uuid
from typing import Optional

class MetricsInput(Base):
    """
    SQLAlchemy ORM model for the MetricsInput table, representing the input metrics data
    for portfolio companies in the VC firm's financial reporting system.

    Requirements addressed:
    - Data Storage (1.2 Scope/Core Functionalities): Implements a PostgreSQL database to store quarterly reporting metrics from portfolio companies.
    - Data Model (3. SYSTEM COMPONENTS ARCHITECTURE/3.1 COMPONENT DIAGRAMS): Defines the database model for input metrics data.
    - Data Integrity (3.2 DATABASE DESIGN): Ensures data integrity through proper column definitions and constraints.
    """

    __tablename__ = "metrics_input"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id", ondelete="CASCADE"), nullable=False, index=True)
    currency = Column(String(3), nullable=False)
    total_revenue = Column(Float, nullable=False)
    recurring_revenue = Column(Float, nullable=False)
    gross_profit = Column(Float, nullable=False)
    sales_marketing_expense = Column(Float, nullable=False)
    total_operating_expense = Column(Float, nullable=False)
    ebitda = Column(Float, nullable=False)
    net_income = Column(Float, nullable=False)
    cash_burn = Column(Float, nullable=False)
    cash_balance = Column(Float, nullable=False)
    debt_outstanding = Column(Float)
    employees = Column(Integer, nullable=False)
    customers = Column(Integer)
    fiscal_reporting_date = Column(Date, nullable=False, index=True)
    fiscal_reporting_quarter = Column(Integer, nullable=False)
    reporting_year = Column(Integer, nullable=False, index=True)
    reporting_quarter = Column(Integer, nullable=False, index=True)

    # Relationship with the Company model
    company = relationship("Company", back_populates="metrics_inputs")

    def __init__(self, company_id: uuid.UUID, currency: str, total_revenue: float,
                 recurring_revenue: float, gross_profit: float, sales_marketing_expense: float,
                 total_operating_expense: float, ebitda: float, net_income: float, cash_burn: float,
                 cash_balance: float, employees: int, fiscal_reporting_date: Date,
                 fiscal_reporting_quarter: int, reporting_year: int, reporting_quarter: int,
                 id: Optional[uuid.UUID] = None, debt_outstanding: Optional[float] = None,
                 customers: Optional[int] = None):
        """
        Initializes a new MetricsInput instance.

        Args:
            company_id (uuid.UUID): Foreign key referencing the associated company.
            currency (str): The currency used for financial values.
            total_revenue (float): Total revenue for the reporting period.
            recurring_revenue (float): Recurring revenue for the reporting period.
            gross_profit (float): Gross profit for the reporting period.
            sales_marketing_expense (float): Sales and marketing expenses for the reporting period.
            total_operating_expense (float): Total operating expenses for the reporting period.
            ebitda (float): Earnings Before Interest, Taxes, Depreciation, and Amortization.
            net_income (float): Net income for the reporting period.
            cash_burn (float): Cash burn rate for the reporting period.
            cash_balance (float): Cash balance at the end of the reporting period.
            employees (int): Number of employees at the end of the reporting period.
            fiscal_reporting_date (Date): The date of the fiscal report.
            fiscal_reporting_quarter (int): The fiscal quarter of the report.
            reporting_year (int): The year of the report.
            reporting_quarter (int): The quarter of the report.
            id (Optional[uuid.UUID]): Unique identifier for the metrics input record. If not provided, a new UUID will be generated.
            debt_outstanding (Optional[float]): Outstanding debt at the end of the reporting period.
            customers (Optional[int]): Number of customers at the end of the reporting period.
        """
        self.id = id or uuid.uuid4()
        self.company_id = company_id
        self.currency = currency
        self.total_revenue = total_revenue
        self.recurring_revenue = recurring_revenue
        self.gross_profit = gross_profit
        self.sales_marketing_expense = sales_marketing_expense
        self.total_operating_expense = total_operating_expense
        self.ebitda = ebitda
        self.net_income = net_income
        self.cash_burn = cash_burn
        self.cash_balance = cash_balance
        self.debt_outstanding = debt_outstanding
        self.employees = employees
        self.customers = customers
        self.fiscal_reporting_date = fiscal_reporting_date
        self.fiscal_reporting_quarter = fiscal_reporting_quarter
        self.reporting_year = reporting_year
        self.reporting_quarter = reporting_quarter

    def __repr__(self):
        return f"<MetricsInput(id={self.id}, company_id={self.company_id}, fiscal_reporting_date={self.fiscal_reporting_date}, reporting_year={self.reporting_year}, reporting_quarter={self.reporting_quarter})>"

    @property
    def gross_margin(self) -> float:
        """
        Calculates the gross margin as a percentage.

        Returns:
            float: The gross margin as a percentage.
        """
        return (self.gross_profit / self.total_revenue) * 100 if self.total_revenue != 0 else 0

    @property
    def recurring_revenue_percentage(self) -> float:
        """
        Calculates the recurring revenue as a percentage of total revenue.

        Returns:
            float: The recurring revenue percentage.
        """
        return (self.recurring_revenue / self.total_revenue) * 100 if self.total_revenue != 0 else 0

    @property
    def ebitda_margin(self) -> float:
        """
        Calculates the EBITDA margin as a percentage.

        Returns:
            float: The EBITDA margin as a percentage.
        """
        return (self.ebitda / self.total_revenue) * 100 if self.total_revenue != 0 else 0