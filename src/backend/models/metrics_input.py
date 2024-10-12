"""
Metrics Input Model Definition

This module defines the SQLAlchemy ORM model for the MetricsInput entity in the application.
It includes various attributes that represent the structure and properties of metrics input data.

Requirements addressed:
1. Data Storage (1.2 Scope/Core Functionalities/1. Data Storage)
2. Database Design (3. SYSTEM DESIGN/3.2 DATABASE DESIGN/3.2.2 Metrics Input Table)

Version Information:
- SQLAlchemy: 1.4.0
- psycopg2-binary: 2.9.3 (for PostgreSQL dialect support)
"""

from sqlalchemy import Column, ForeignKey, String, Date, DECIMAL, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import date
import uuid
from src.backend.db.base import Base

class MetricsInput(Base):
    """
    SQLAlchemy model for the Metrics Input table.

    This model represents the input metrics for portfolio companies in the VC firm's database.
    It implements the Metrics Input table structure for storing financial metrics data from portfolio companies.

    Requirements addressed:
    - Data Storage (1.2 Scope/Core Functionalities/1. Data Storage)
    - Database Design (3. SYSTEM DESIGN/3.2 DATABASE DESIGN/3.2.2 Metrics Input Table)
    """

    __tablename__ = "metrics_input"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id"), nullable=False, index=True)
    currency = Column(String(3), nullable=False)
    total_revenue = Column(DECIMAL(15, 2), nullable=False)
    recurring_revenue = Column(DECIMAL(15, 2), nullable=False)
    gross_profit = Column(DECIMAL(15, 2), nullable=False)
    sales_marketing_expense = Column(DECIMAL(15, 2), nullable=False)
    total_operating_expense = Column(DECIMAL(15, 2), nullable=False)
    ebitda = Column(DECIMAL(15, 2), nullable=False)
    net_income = Column(DECIMAL(15, 2), nullable=False)
    cash_burn = Column(DECIMAL(15, 2), nullable=False)
    cash_balance = Column(DECIMAL(15, 2), nullable=False)
    debt_outstanding = Column(DECIMAL(15, 2))
    employees = Column(Integer, nullable=False)
    customers = Column(Integer)
    fiscal_reporting_date = Column(Date, nullable=False, index=True)
    fiscal_reporting_quarter = Column(Integer, nullable=False)
    reporting_year = Column(Integer, nullable=False)
    reporting_quarter = Column(Integer, nullable=False)
    created_date = Column(Date, nullable=False, server_default=func.current_date())
    created_by = Column(String(100), nullable=False)
    last_update_date = Column(Date, onupdate=func.current_date())
    last_updated_by = Column(String(100))

    # Relationship with the Company model
    company = relationship("Company", back_populates="metrics_inputs")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.id is None:
            self.id = uuid.uuid4()
        if self.created_date is None:
            self.created_date = date.today()

    def __repr__(self):
        return f"<MetricsInput(id={self.id}, company_id={self.company_id}, fiscal_reporting_date={self.fiscal_reporting_date})>"

    @classmethod
    def create_table(cls, engine):
        """
        Creates the metrics_input table in the database.
        
        Args:
            engine: SQLAlchemy engine instance
        """
        Base.metadata.create_all(bind=engine, tables=[cls.__table__])

    @classmethod
    def drop_table(cls, engine):
        """
        Drops the metrics_input table from the database.
        
        Args:
            engine: SQLAlchemy engine instance
        """
        cls.__table__.drop(engine)

# Index creation
from sqlalchemy import Index

Index('idx_metrics_input_company_id', MetricsInput.company_id)
Index('idx_metrics_input_fiscal_reporting_date', MetricsInput.fiscal_reporting_date)
Index('idx_metrics_input_reporting_year_quarter', MetricsInput.reporting_year, MetricsInput.reporting_quarter)

# Add this relationship to the Company model in src/backend/models/company.py
# Company.metrics_inputs = relationship("MetricsInput", back_populates="company")

"""
Note: The relationship between Company and MetricsInput should be defined in the Company model.
Please add the following line to the Company model in src/backend/models/company.py:

metrics_inputs = relationship("MetricsInput", back_populates="company")

This ensures that the relationship is properly established on both sides.
"""