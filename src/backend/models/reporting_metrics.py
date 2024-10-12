"""
ReportingMetrics Model Definition

This module defines the SQLAlchemy ORM model for the Quarterly Reporting Metrics entity in the application.
It includes various attributes that represent the structure and properties of quarterly reporting metrics.

Requirements addressed:
1. Data Storage (1.2 Scope/Core Functionalities/1. Data Storage)
2. Database Design (3. SYSTEM DESIGN/3.2 DATABASE DESIGN/3.2.4 Quarterly Reporting Metrics Table)

Version Information:
- SQLAlchemy: 1.4.0
- psycopg2-binary: 2.9.3 (for PostgreSQL dialect support)
"""

from sqlalchemy import Column, ForeignKey, String, Date, DECIMAL, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.backend.db.base import Base
from datetime import datetime
import uuid

class ReportingMetrics(Base):
    """
    SQLAlchemy model for the Quarterly Reporting Metrics table.
    
    This model represents the quarterly reporting metrics for portfolio companies
    in the VC firm's database. It implements the Quarterly Reporting Metrics table
    structure for storing derived financial metrics as specified in the requirements:
    1.2 Scope/Core Functionalities/1. Data Storage
    3. SYSTEM DESIGN/3.2 DATABASE DESIGN/3.2.4 Quarterly Reporting Metrics Table
    """
    __tablename__ = "quarterly_reporting_metrics"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    company_id = Column(UUID(as_uuid=True), ForeignKey('companies.id'), nullable=False, index=True)
    currency = Column(String(3), nullable=False)
    enterprise_value = Column(DECIMAL(20, 2))
    arr = Column(DECIMAL(20, 2))
    recurring_percentage_revenue = Column(DECIMAL(5, 2))
    revenue_per_fte = Column(DECIMAL(20, 2))
    gross_profit_per_fte = Column(DECIMAL(20, 2))
    employee_growth_rate = Column(DECIMAL(5, 2))
    change_in_cash = Column(DECIMAL(20, 2))
    revenue_growth = Column(DECIMAL(5, 2))
    monthly_cash_burn = Column(DECIMAL(20, 2))
    runway_months = Column(DECIMAL(5, 1))
    ev_by_equity_raised_plus_debt = Column(DECIMAL(10, 2))
    sales_marketing_percentage_revenue = Column(DECIMAL(5, 2))
    total_operating_percentage_revenue = Column(DECIMAL(5, 2))
    gross_profit_margin = Column(DECIMAL(5, 2))
    valuation_to_revenue = Column(DECIMAL(10, 2))
    yoy_growth_revenue = Column(DECIMAL(5, 2))
    yoy_growth_profit = Column(DECIMAL(5, 2))
    yoy_growth_employees = Column(DECIMAL(5, 2))
    yoy_growth_ltm_revenue = Column(DECIMAL(5, 2))
    ltm_total_revenue = Column(DECIMAL(20, 2))
    ltm_gross_profit = Column(DECIMAL(20, 2))
    ltm_sales_marketing_expense = Column(DECIMAL(20, 2))
    ltm_gross_margin = Column(DECIMAL(5, 2))
    ltm_operating_expense = Column(DECIMAL(20, 2))
    ltm_ebitda = Column(DECIMAL(20, 2))
    ltm_net_income = Column(DECIMAL(20, 2))
    ltm_ebitda_margin = Column(DECIMAL(5, 2))
    ltm_net_income_margin = Column(DECIMAL(5, 2))
    fiscal_reporting_date = Column(Date, nullable=False, index=True)
    fiscal_reporting_quarter = Column(Integer, nullable=False)
    reporting_year = Column(Integer, nullable=False, index=True)
    reporting_quarter = Column(Integer, nullable=False, index=True)
    created_date = Column(Date, nullable=False, server_default=func.current_date())
    created_by = Column(String(100), nullable=False)
    last_update_date = Column(Date, onupdate=func.current_date())
    last_updated_by = Column(String(100))

    # Relationship with the Company model
    company = relationship("Company", back_populates="reporting_metrics")

    def __init__(self, **kwargs):
        """
        Initializes a new ReportingMetrics instance.
        Sets default values for id and dates if not provided.
        """
        if 'id' not in kwargs:
            kwargs['id'] = uuid.uuid4()
        if 'created_date' not in kwargs:
            kwargs['created_date'] = datetime.utcnow().date()
        super().__init__(**kwargs)

    def __repr__(self):
        """
        Returns a string representation of the ReportingMetrics instance.
        """
        return f"<ReportingMetrics(id={self.id}, company_id={self.company_id}, fiscal_reporting_date={self.fiscal_reporting_date})>"

    @classmethod
    def create_table(cls, engine):
        """
        Creates the quarterly_reporting_metrics table in the database.
        
        Args:
            engine: SQLAlchemy engine instance
        """
        Base.metadata.create_all(bind=engine, tables=[cls.__table__])

    @classmethod
    def drop_table(cls, engine):
        """
        Drops the quarterly_reporting_metrics table from the database.
        
        Args:
            engine: SQLAlchemy engine instance
        """
        cls.__table__.drop(engine)

# Index creation
from sqlalchemy import Index

Index('idx_reporting_metrics_company_id', ReportingMetrics.company_id)
Index('idx_reporting_metrics_fiscal_reporting_date', ReportingMetrics.fiscal_reporting_date)
Index('idx_reporting_metrics_reporting_year_quarter', ReportingMetrics.reporting_year, ReportingMetrics.reporting_quarter)

# Ensure all decimal columns have appropriate precision and scale
for column in ReportingMetrics.__table__.columns:
    if isinstance(column.type, DECIMAL):
        assert column.type.precision is not None, f"Precision not set for {column.name}"
        assert column.type.scale is not None, f"Scale not set for {column.name}"