from sqlalchemy import Column, ForeignKey, Integer, String, Date, Numeric, DateTime, UUID, Index, UniqueConstraint
from sqlalchemy.orm import relationship
from src.backend.db.base import Base
import uuid
from datetime import datetime
from typing import Optional

class ReportingFinancials(Base):
    """
    SQLAlchemy model representing the quarterly reporting financials for a portfolio company.
    
    This model implements the database schema for storing quarterly financial data,
    addressing the following requirements:
    1. Data Storage (1.2 Scope/Core Functionalities/1. Data Storage)
    2. Multi-Currency Support (1.2 Scope/Core Functionalities/4. Multi-Currency Support)
    3. Audit Trail (1.2 Scope/Core Functionalities/5. Audit Trail)
    """

    __tablename__ = "reporting_financials"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id"), nullable=False, index=True)
    currency = Column(String(3), nullable=False)
    exchange_rate_used = Column(Numeric(10, 6), nullable=False)
    total_revenue = Column(Numeric(15, 2), nullable=False)
    recurring_revenue = Column(Numeric(15, 2), nullable=False)
    gross_profit = Column(Numeric(15, 2), nullable=False)
    sales_marketing_expense = Column(Numeric(15, 2), nullable=False)
    total_operating_expense = Column(Numeric(15, 2), nullable=False)
    ebitda = Column(Numeric(15, 2), nullable=False)
    net_income = Column(Numeric(15, 2), nullable=False)
    cash_burn = Column(Numeric(15, 2), nullable=False)
    cash_balance = Column(Numeric(15, 2), nullable=False)
    debt_outstanding = Column(Numeric(15, 2))
    fiscal_reporting_date = Column(Date, nullable=False, index=True)
    fiscal_reporting_quarter = Column(Integer, nullable=False)
    reporting_year = Column(Integer, nullable=False, index=True)
    reporting_quarter = Column(Integer, nullable=False)
    created_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    created_by = Column(String(100), nullable=False)
    last_update_date = Column(DateTime, onupdate=datetime.utcnow)
    last_updated_by = Column(String(100))

    # Relationship with the Company model
    company = relationship("Company", back_populates="reporting_financials")

    __table_args__ = (
        Index('idx_reporting_financials_company_date', 'company_id', 'fiscal_reporting_date'),
        UniqueConstraint('company_id', 'fiscal_reporting_date', name='uq_company_date'),
    )

    def __init__(self, company_id: uuid.UUID, currency: str, exchange_rate_used: float,
                 total_revenue: float, recurring_revenue: float, gross_profit: float,
                 sales_marketing_expense: float, total_operating_expense: float,
                 ebitda: float, net_income: float, cash_burn: float, cash_balance: float,
                 debt_outstanding: Optional[float], fiscal_reporting_date: datetime.date,
                 fiscal_reporting_quarter: int, reporting_year: int, reporting_quarter: int,
                 created_by: str):
        """
        Initialize a new ReportingFinancials instance.

        :param company_id: UUID of the associated company
        :param currency: 3-letter currency code
        :param exchange_rate_used: Exchange rate used for currency conversion
        :param total_revenue: Total revenue for the reporting period
        :param recurring_revenue: Recurring revenue for the reporting period
        :param gross_profit: Gross profit for the reporting period
        :param sales_marketing_expense: Sales and marketing expenses
        :param total_operating_expense: Total operating expenses
        :param ebitda: Earnings Before Interest, Taxes, Depreciation, and Amortization
        :param net_income: Net income for the reporting period
        :param cash_burn: Cash burn rate
        :param cash_balance: Cash balance at the end of the reporting period
        :param debt_outstanding: Outstanding debt at the end of the reporting period (optional)
        :param fiscal_reporting_date: Date of the fiscal report
        :param fiscal_reporting_quarter: Fiscal quarter of the report (1-4)
        :param reporting_year: Year of the report
        :param reporting_quarter: Calendar quarter of the report (1-4)
        :param created_by: User who created the record
        """
        self.id = uuid.uuid4()
        self.company_id = company_id
        self.currency = currency
        self.exchange_rate_used = exchange_rate_used
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
        self.fiscal_reporting_date = fiscal_reporting_date
        self.fiscal_reporting_quarter = fiscal_reporting_quarter
        self.reporting_year = reporting_year
        self.reporting_quarter = reporting_quarter
        self.created_by = created_by
        self.created_date = datetime.utcnow()
        self.last_update_date = None
        self.last_updated_by = None

    def __repr__(self):
        return (f"<ReportingFinancials(id={self.id}, company_id={self.company_id}, "
                f"fiscal_reporting_date={self.fiscal_reporting_date})>")

    @classmethod
    def from_dict(cls, data: dict) -> 'ReportingFinancials':
        """
        Create a ReportingFinancials instance from a dictionary.

        :param data: Dictionary containing the ReportingFinancials data
        :return: ReportingFinancials instance
        """
        return cls(**data)

    def to_dict(self) -> dict:
        """
        Convert the ReportingFinancials instance to a dictionary.

        :return: Dictionary representation of the ReportingFinancials instance
        """
        return {
            'id': str(self.id),
            'company_id': str(self.company_id),
            'currency': self.currency,
            'exchange_rate_used': float(self.exchange_rate_used),
            'total_revenue': float(self.total_revenue),
            'recurring_revenue': float(self.recurring_revenue),
            'gross_profit': float(self.gross_profit),
            'sales_marketing_expense': float(self.sales_marketing_expense),
            'total_operating_expense': float(self.total_operating_expense),
            'ebitda': float(self.ebitda),
            'net_income': float(self.net_income),
            'cash_burn': float(self.cash_burn),
            'cash_balance': float(self.cash_balance),
            'debt_outstanding': float(self.debt_outstanding) if self.debt_outstanding else None,
            'fiscal_reporting_date': self.fiscal_reporting_date.isoformat(),
            'fiscal_reporting_quarter': self.fiscal_reporting_quarter,
            'reporting_year': self.reporting_year,
            'reporting_quarter': self.reporting_quarter,
            'created_date': self.created_date.isoformat() if self.created_date else None,
            'created_by': self.created_by,
            'last_update_date': self.last_update_date.isoformat() if self.last_update_date else None,
            'last_updated_by': self.last_updated_by
        }