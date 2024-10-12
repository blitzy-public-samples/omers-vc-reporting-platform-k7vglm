"""
This module defines the SQLAlchemy ORM model for the Quarterly Reporting Financials table.

Requirements addressed:
1. Data Storage (1.2 Scope/Core Functionalities/1. Data Storage)
2. Multi-Currency Support (1.2 Scope/Core Functionalities/4. Multi-Currency Support)
3. Data Integrity (3. SYSTEM DESIGN/3.2 DATABASE DESIGN)
4. Audit Trail (1.2 Scope/Core Functionalities/5. Audit Trail)
"""

from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Numeric, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
from src.database.base import Base
from datetime import date

class ReportingFinancials(Base):
    """
    SQLAlchemy ORM model representing the Quarterly Reporting Financials table.
    
    This model stores financial data for portfolio companies on a quarterly basis.
    It includes various financial metrics, currency information, and audit trail fields.
    """

    __tablename__ = "quarterly_reporting_financials"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id", ondelete="CASCADE"), nullable=False, index=True)
    currency = Column(String(3), nullable=False)
    exchange_rate_used = Column(Numeric(10, 6), nullable=False)
    total_revenue = Column(Numeric(18, 2), nullable=False)
    recurring_revenue = Column(Numeric(18, 2), nullable=False)
    gross_profit = Column(Numeric(18, 2), nullable=False)
    debt_outstanding = Column(Numeric(18, 2))
    sales_marketing_expense = Column(Numeric(18, 2), nullable=False)
    total_operating_expense = Column(Numeric(18, 2), nullable=False)
    ebitda = Column(Numeric(18, 2), nullable=False)
    net_income = Column(Numeric(18, 2), nullable=False)
    cash_burn = Column(Numeric(18, 2), nullable=False)
    cash_balance = Column(Numeric(18, 2), nullable=False)
    fiscal_reporting_date = Column(Date, nullable=False)
    fiscal_reporting_quarter = Column(Integer, nullable=False)
    reporting_year = Column(Integer, nullable=False)
    reporting_quarter = Column(Integer, nullable=False)
    created_date = Column(Date, nullable=False, default=date.today)
    created_by = Column(String(100), nullable=False)
    last_update_date = Column(Date)
    last_updated_by = Column(String(100))

    # Relationships
    company = relationship("Company", back_populates="reporting_financials")

    # Constraints
    __table_args__ = (
        CheckConstraint('currency ~ \'^[A-Z]{3}$\'', name='check_currency_format'),
        CheckConstraint('exchange_rate_used > 0', name='check_positive_exchange_rate'),
        CheckConstraint('fiscal_reporting_quarter BETWEEN 1 AND 4', name='check_fiscal_quarter_range'),
        CheckConstraint('reporting_quarter BETWEEN 1 AND 4', name='check_reporting_quarter_range'),
        CheckConstraint('reporting_year > 1900', name='check_reporting_year_range'),
    )

    def __init__(self, **kwargs):
        """
        Initializes a new ReportingFinancials instance.
        All parameters are optional and can be set after initialization.
        """
        super().__init__(**kwargs)

    def __repr__(self):
        """
        Returns a string representation of the ReportingFinancials instance.
        """
        return (f"<ReportingFinancials(id={self.id}, company_id={self.company_id}, "
                f"fiscal_reporting_date={self.fiscal_reporting_date}, "
                f"reporting_year={self.reporting_year}, reporting_quarter={self.reporting_quarter})>")

    @classmethod
    def from_dict(cls, data):
        """
        Creates a new ReportingFinancials instance from a dictionary.
        
        :param data: Dictionary containing the ReportingFinancials data
        :return: New ReportingFinancials instance
        """
        return cls(**data)

    def to_dict(self):
        """
        Converts the ReportingFinancials instance to a dictionary.
        
        :return: Dictionary representation of the ReportingFinancials instance
        """
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def update(self, **kwargs):
        """
        Updates the ReportingFinancials instance with the provided keyword arguments.
        
        :param kwargs: Key-value pairs to update
        """
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.last_update_date = date.today()