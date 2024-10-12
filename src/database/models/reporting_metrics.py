"""
This module defines the SQLAlchemy ORM model for the reporting_metrics table.

Requirements addressed:
1. Data Model (3. SYSTEM DESIGN/3.1 DATA MODEL):
   Implements the ReportingMetrics model to store quarterly reporting metrics from portfolio companies
2. Database Schema (3. SYSTEM DESIGN/3.2 DATABASE DESIGN):
   Defines the schema for the reporting_metrics table with appropriate columns and relationships
"""

from sqlalchemy import Column, ForeignKey, Integer, String, Date, Numeric, UUID
from sqlalchemy.orm import relationship
from uuid import uuid4
from src.database.base import Base
from src.database.config import get_database_settings

class ReportingMetrics(Base):
    """
    SQLAlchemy model representing the reporting_metrics table
    """
    __tablename__ = "reporting_metrics"

    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    
    # Foreign key to link with the company
    company_id = Column(UUID(as_uuid=True), ForeignKey('companies.id'), nullable=False, index=True)
    
    # Currency of the reported metrics
    currency = Column(String(3), nullable=False)
    
    # Financial metrics
    enterprise_value = Column(Numeric(20, 2))
    arr = Column(Numeric(20, 2))
    recurring_percentage_revenue = Column(Numeric(5, 2))
    revenue_per_fte = Column(Numeric(20, 2))
    gross_profit_per_fte = Column(Numeric(20, 2))
    employee_growth_rate = Column(Numeric(5, 2))
    change_in_cash = Column(Numeric(20, 2))
    revenue_growth = Column(Numeric(5, 2))
    monthly_cash_burn = Column(Numeric(20, 2))
    runway_months = Column(Numeric(7, 1))
    ev_by_equity_raised_plus_debt = Column(Numeric(7, 2))
    sales_marketing_percentage_revenue = Column(Numeric(5, 2))
    total_operating_percentage_revenue = Column(Numeric(5, 2))
    gross_profit_margin = Column(Numeric(5, 2))
    valuation_to_revenue = Column(Numeric(7, 2))
    yoy_growth_revenue = Column(Numeric(5, 2))
    yoy_growth_profit = Column(Numeric(5, 2))
    yoy_growth_employees = Column(Numeric(5, 2))
    yoy_growth_ltm_revenue = Column(Numeric(5, 2))
    ltm_total_revenue = Column(Numeric(20, 2))
    ltm_gross_profit = Column(Numeric(20, 2))
    ltm_sales_marketing_expense = Column(Numeric(20, 2))
    ltm_gross_margin = Column(Numeric(5, 2))
    ltm_operating_expense = Column(Numeric(20, 2))
    ltm_ebitda = Column(Numeric(20, 2))
    ltm_net_income = Column(Numeric(20, 2))
    ltm_ebitda_margin = Column(Numeric(5, 2))
    ltm_net_income_margin = Column(Numeric(5, 2))
    
    # Reporting period information
    fiscal_reporting_date = Column(Date, nullable=False, index=True)
    fiscal_reporting_quarter = Column(Integer, nullable=False)
    reporting_year = Column(Integer, nullable=False, index=True)
    reporting_quarter = Column(Integer, nullable=False)
    
    # Audit fields
    created_date = Column(Date, nullable=False)
    created_by = Column(String(100), nullable=False)
    last_update_date = Column(Date)
    last_updated_by = Column(String(100))

    # Relationship with the Company model
    company = relationship("Company", back_populates="reporting_metrics")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id = uuid4()

    def __repr__(self):
        return f"<ReportingMetrics(id={self.id}, company_id={self.company_id}, fiscal_reporting_date={self.fiscal_reporting_date})>"

# Get database settings
db_settings = get_database_settings()

# Use database settings if needed
# For example, to set table-specific options based on the environment:
if db_settings.DATABASE_ECHO_SQL:
    __table_args__ = {'mysql_engine': 'InnoDB'}

"""
Additional notes for developers:

1. The ReportingMetrics model represents the structure of the reporting_metrics table in the database.
2. Each instance of this model corresponds to a row in the reporting_metrics table.
3. The UUID type is used for the id and company_id fields to ensure global uniqueness.
4. Indexes have been added to frequently queried columns (id, company_id, fiscal_reporting_date, reporting_year) to improve query performance.
5. The Numeric type is used for financial values, with appropriate precision and scale:
   - (20, 2) for large monetary values (e.g., enterprise_value, arr)
   - (5, 2) for percentage values
   - (7, 2) for ratios that might exceed 100
   - (7, 1) for runway_months to allow for longer runway periods
6. The relationship with the Company model is defined using SQLAlchemy's relationship function.
7. The __init__ method ensures that a new UUID is generated for each new instance.
8. The __repr__ method provides a string representation of the object for debugging purposes.
9. Database-specific settings (e.g., mysql_engine) are applied conditionally based on the environment.

When working with this model:
- Ensure that all required fields are provided when creating new instances.
- Use appropriate data types when assigning values to fields (e.g., use Decimal for Numeric fields).
- Be aware of the relationships between models when querying or manipulating data.
- Consider using SQLAlchemy's session management for database operations to ensure proper transaction handling.
"""