"""
Company Model Definition

This module defines the SQLAlchemy ORM model for the Company entity in the application.
It includes various attributes and enums that represent the structure and properties of a company.

Requirements addressed:
1. Data Storage (1.2 Scope/Core Functionalities/1. Data Storage)
2. Database Design (3. SYSTEM DESIGN/3.2 DATABASE DESIGN/3.2.1 Companies Table)

Version Information:
- SQLAlchemy: 1.4.0
- psycopg2-binary: 2.9.3 (for PostgreSQL dialect support)
"""

from sqlalchemy import Column, String, Enum, Date, DECIMAL
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from datetime import date
import uuid
import enum
from src.backend.db.base import Base

class ReportingStatus(enum.Enum):
    """
    Enumeration for company reporting status.
    
    Requirement: Data Storage
    Location: 1.2 Scope/Core Functionalities/1. Data Storage
    """
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    EXITED = "EXITED"

class CustomerType(enum.Enum):
    """
    Enumeration for company customer types.
    
    Requirement: Data Storage
    Location: 1.2 Scope/Core Functionalities/1. Data Storage
    """
    SMB = "SMB"
    ENTERPRISE = "ENTERPRISE"
    CONSUMER = "CONSUMER"

class RevenueType(enum.Enum):
    """
    Enumeration for company revenue types.
    
    Requirement: Data Storage
    Location: 1.2 Scope/Core Functionalities/1. Data Storage
    """
    SAAS = "SAAS"
    TRANSACTIONAL = "TRANSACTIONAL"
    MARKETPLACE = "MARKETPLACE"

class Company(Base):
    """
    SQLAlchemy model for the Company table.
    
    Requirement: Database Design
    Location: 3. SYSTEM DESIGN/3.2 DATABASE DESIGN/3.2.1 Companies Table
    """
    __tablename__ = "companies"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True, nullable=False)
    name = Column(String(255), nullable=False, index=True)
    reporting_status = Column(Enum(ReportingStatus), nullable=False)
    reporting_currency = Column(String(3), nullable=False)
    fund = Column(String(100), nullable=False)
    location_country = Column(String(100), nullable=False)
    customer_type = Column(Enum(CustomerType), nullable=False)
    revenue_type = Column(Enum(RevenueType), nullable=False)
    equity_raised = Column(DECIMAL(15, 2))
    post_money_valuation = Column(DECIMAL(15, 2))
    year_end_date = Column(Date, nullable=False)
    created_date = Column(Date, nullable=False, server_default=func.current_date())
    created_by = Column(String(100), nullable=False)
    last_update_date = Column(Date, onupdate=func.current_date())
    last_updated_by = Column(String(100))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.id is None:
            self.id = uuid.uuid4()
        if self.created_date is None:
            self.created_date = date.today()

    def __repr__(self):
        return (f"<Company(id={self.id}, name='{self.name}', "
                f"reporting_status={self.reporting_status.value})>")

    @classmethod
    def create_table(cls, engine):
        """
        Creates the companies table in the database.
        
        Args:
            engine: SQLAlchemy engine instance
        """
        Base.metadata.create_all(bind=engine, tables=[cls.__table__])

    @classmethod
    def drop_table(cls, engine):
        """
        Drops the companies table from the database.
        
        Args:
            engine: SQLAlchemy engine instance
        """
        cls.__table__.drop(engine)

# Index creation
from sqlalchemy import Index

Index('idx_company_name', Company.name)
Index('idx_company_reporting_status', Company.reporting_status)
Index('idx_company_fund', Company.fund)
Index('idx_company_customer_type', Company.customer_type)
Index('idx_company_revenue_type', Company.revenue_type)

# Ensure all enum values are unique
assert len(set(ReportingStatus)) == len(ReportingStatus), "Duplicate values in ReportingStatus enum"
assert len(set(CustomerType)) == len(CustomerType), "Duplicate values in CustomerType enum"
assert len(set(RevenueType)) == len(RevenueType), "Duplicate values in RevenueType enum"