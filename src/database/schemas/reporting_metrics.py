from uuid import UUID
from datetime import datetime, date
from pydantic import BaseModel, Field, validator
from typing import Optional
from decimal import Decimal

class ReportingMetricsBase(BaseModel):
    company_id: UUID = Field(..., description="UUID of the associated company")
    currency: str = Field(..., min_length=3, max_length=3, description="ISO 4217 currency code")
    enterprise_value: Decimal = Field(..., ge=0, description="Enterprise value in the specified currency")
    arr: Decimal = Field(..., ge=0, description="Annual Recurring Revenue in the specified currency")
    recurring_percentage_revenue: Decimal = Field(..., ge=0, le=100, description="Percentage of recurring revenue")
    revenue_per_fte: Decimal = Field(..., ge=0, description="Revenue per full-time equivalent employee")
    gross_profit_per_fte: Decimal = Field(..., description="Gross profit per full-time equivalent employee")
    employee_growth_rate: Decimal = Field(..., description="Employee growth rate as a percentage")
    change_in_cash: Decimal = Field(..., description="Change in cash position")
    revenue_growth: Decimal = Field(..., description="Revenue growth rate as a percentage")
    monthly_cash_burn: Decimal = Field(..., description="Monthly cash burn rate")
    runway_months: Decimal = Field(..., ge=0, description="Number of months of runway")
    ev_by_equity_raised_plus_debt: Decimal = Field(..., ge=0, description="Enterprise value divided by equity raised plus debt")
    sales_marketing_percentage_revenue: Decimal = Field(..., ge=0, le=100, description="Sales and marketing expense as a percentage of revenue")
    total_operating_percentage_revenue: Decimal = Field(..., ge=0, le=100, description="Total operating expense as a percentage of revenue")
    gross_profit_margin: Decimal = Field(..., le=100, description="Gross profit margin as a percentage")
    valuation_to_revenue: Decimal = Field(..., ge=0, description="Valuation to revenue ratio")
    yoy_growth_revenue: Decimal = Field(..., description="Year-over-year revenue growth as a percentage")
    yoy_growth_profit: Decimal = Field(..., description="Year-over-year profit growth as a percentage")
    yoy_growth_employees: Decimal = Field(..., description="Year-over-year employee growth as a percentage")
    yoy_growth_ltm_revenue: Decimal = Field(..., description="Year-over-year growth in last twelve months revenue as a percentage")
    ltm_total_revenue: Decimal = Field(..., ge=0, description="Last twelve months total revenue")
    ltm_gross_profit: Decimal = Field(..., description="Last twelve months gross profit")
    ltm_sales_marketing_expense: Decimal = Field(..., ge=0, description="Last twelve months sales and marketing expense")
    ltm_gross_margin: Decimal = Field(..., le=100, description="Last twelve months gross margin as a percentage")
    ltm_operating_expense: Decimal = Field(..., ge=0, description="Last twelve months operating expense")
    ltm_ebitda: Decimal = Field(..., description="Last twelve months EBITDA")
    ltm_net_income: Decimal = Field(..., description="Last twelve months net income")
    ltm_ebitda_margin: Decimal = Field(..., description="Last twelve months EBITDA margin as a percentage")
    ltm_net_income_margin: Decimal = Field(..., description="Last twelve months net income margin as a percentage")
    fiscal_reporting_date: date = Field(..., description="Fiscal reporting date")
    fiscal_reporting_quarter: int = Field(..., ge=1, le=4, description="Fiscal reporting quarter (1-4)")
    reporting_year: int = Field(..., ge=1900, le=2100, description="Reporting year")
    reporting_quarter: int = Field(..., ge=1, le=4, description="Reporting quarter (1-4)")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        json_encoders = {
            UUID: str,
            datetime: lambda v: v.isoformat(),
            date: lambda v: v.isoformat(),
            Decimal: lambda v: float(v)
        }

    @validator('currency')
    def validate_currency(cls, v):
        if len(v) != 3 or not v.isalpha():
            raise ValueError('Currency must be a 3-letter ISO 4217 code')
        return v.upper()

class ReportingMetricsCreate(ReportingMetricsBase):
    pass

class ReportingMetricsUpdate(ReportingMetricsBase):
    pass

class ReportingMetrics(ReportingMetricsBase):
    id: UUID = Field(..., description="Unique identifier for the reporting metrics entry")

class ReportingMetricsInDB(ReportingMetrics):
    created_date: datetime = Field(..., description="Date and time when the entry was created")
    created_by: str = Field(..., min_length=1, max_length=100, description="User who created the entry")
    last_update_date: Optional[datetime] = Field(None, description="Date and time of the last update")
    last_updated_by: Optional[str] = Field(None, min_length=1, max_length=100, description="User who last updated the entry")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        json_encoders = {
            UUID: str,
            datetime: lambda v: v.isoformat(),
            date: lambda v: v.isoformat(),
            Decimal: lambda v: float(v)
        }

# Additional validators can be added here for complex business logic or data integrity checks

"""
This module defines Pydantic models for the ReportingMetrics table, providing data validation
and serialization for the reporting metrics of portfolio companies.

Requirements addressed:
1. Data Validation (2. SYSTEM ARCHITECTURE/2.2 Component Description/2.2.1 Application Layer)
   - Implements request validation and error handling for financial data
2. Multi-Currency Support (1.2 Scope/Core Functionalities)
   - Supports financial data in local currency, USD, and CAD
3. Data Integrity (3. SYSTEM DESIGN/3.2 DATABASE DESIGN)
   - Ensures data consistency and validity through Pydantic's validation system

Notes:
- All financial values use the Decimal type for precise calculations
- UUID fields are used for unique identifiers
- Date and datetime fields use Python's built-in types
- Custom validators can be added for complex business logic
- The Config class in each model enables ORM mode and customizes JSON encoding

When using these models:
- Ensure all required fields are provided when creating or updating records
- Use appropriate data types, especially for financial calculations (Decimal)
- Be aware of the automatic conversion of Decimal to float in JSON responses
- Consider adding additional validators for complex business rules or data integrity checks

Dependencies:
- pydantic==1.10.7
- python-dateutil==2.8.2
"""