from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime, date
from decimal import Decimal
from typing import Optional
from src.backend.db.base import Base  # Used for type hinting

class ReportingMetricsBase(BaseModel):
    """
    Base Pydantic model for ReportingMetrics with common attributes.
    
    Requirements addressed:
    - Data Validation (3. SYSTEM DESIGN/3.3 API DESIGN)
    - API Schema (3. SYSTEM DESIGN/3.3 API DESIGN)
    """
    company_id: UUID = Field(..., description="Unique identifier of the company")
    currency: str = Field(..., description="Currency used for financial metrics")
    enterprise_value: Decimal = Field(..., description="Enterprise value of the company")
    arr: Decimal = Field(..., description="Annual Recurring Revenue")
    recurring_percentage_revenue: Decimal = Field(..., ge=0, le=100, description="Percentage of recurring revenue")
    revenue_per_fte: Decimal = Field(..., ge=0, description="Revenue per Full-Time Equivalent")
    gross_profit_per_fte: Decimal = Field(..., description="Gross profit per Full-Time Equivalent")
    employee_growth_rate: Decimal = Field(..., description="Employee growth rate")
    change_in_cash: Decimal = Field(..., description="Change in cash")
    revenue_growth: Decimal = Field(..., description="Revenue growth rate")
    monthly_cash_burn: Decimal = Field(..., description="Monthly cash burn rate")
    runway_months: Decimal = Field(..., ge=0, description="Number of runway months")
    ev_by_equity_raised_plus_debt: Decimal = Field(..., description="Enterprise value divided by equity raised plus debt")
    sales_marketing_percentage_revenue: Decimal = Field(..., ge=0, le=100, description="Sales and marketing expense as a percentage of revenue")
    total_operating_percentage_revenue: Decimal = Field(..., ge=0, le=100, description="Total operating expense as a percentage of revenue")
    gross_profit_margin: Decimal = Field(..., ge=0, le=100, description="Gross profit margin")
    valuation_to_revenue: Decimal = Field(..., ge=0, description="Valuation to revenue ratio")
    yoy_growth_revenue: Decimal = Field(..., description="Year-over-year revenue growth")
    yoy_growth_profit: Decimal = Field(..., description="Year-over-year profit growth")
    yoy_growth_employees: Decimal = Field(..., description="Year-over-year employee growth")
    yoy_growth_ltm_revenue: Decimal = Field(..., description="Year-over-year growth in Last Twelve Months (LTM) revenue")
    ltm_total_revenue: Decimal = Field(..., ge=0, description="Last Twelve Months (LTM) total revenue")
    ltm_gross_profit: Decimal = Field(..., description="Last Twelve Months (LTM) gross profit")
    ltm_sales_marketing_expense: Decimal = Field(..., ge=0, description="Last Twelve Months (LTM) sales and marketing expense")
    ltm_gross_margin: Decimal = Field(..., ge=0, le=100, description="Last Twelve Months (LTM) gross margin")
    ltm_operating_expense: Decimal = Field(..., ge=0, description="Last Twelve Months (LTM) operating expense")
    ltm_ebitda: Decimal = Field(..., description="Last Twelve Months (LTM) EBITDA")
    ltm_net_income: Decimal = Field(..., description="Last Twelve Months (LTM) net income")
    ltm_ebitda_margin: Decimal = Field(..., description="Last Twelve Months (LTM) EBITDA margin")
    ltm_net_income_margin: Decimal = Field(..., description="Last Twelve Months (LTM) net income margin")
    fiscal_reporting_date: date = Field(..., description="Fiscal reporting date")
    fiscal_reporting_quarter: int = Field(..., ge=1, le=4, description="Fiscal reporting quarter")
    reporting_year: int = Field(..., ge=1900, le=2100, description="Reporting year")
    reporting_quarter: int = Field(..., ge=1, le=4, description="Reporting quarter")

    class Config:
        """Pydantic model configuration."""
        orm_mode = True
        schema_extra = {
            "example": {
                "company_id": "123e4567-e89b-12d3-a456-426614174000",
                "currency": "USD",
                "enterprise_value": 1000000000,
                "arr": 50000000,
                "recurring_percentage_revenue": 85,
                "revenue_per_fte": 200000,
                "gross_profit_per_fte": 150000,
                "employee_growth_rate": 0.15,
                "change_in_cash": 5000000,
                "revenue_growth": 0.25,
                "monthly_cash_burn": 1000000,
                "runway_months": 18,
                "ev_by_equity_raised_plus_debt": 5,
                "sales_marketing_percentage_revenue": 30,
                "total_operating_percentage_revenue": 70,
                "gross_profit_margin": 70,
                "valuation_to_revenue": 10,
                "yoy_growth_revenue": 0.3,
                "yoy_growth_profit": 0.35,
                "yoy_growth_employees": 0.2,
                "yoy_growth_ltm_revenue": 0.28,
                "ltm_total_revenue": 60000000,
                "ltm_gross_profit": 42000000,
                "ltm_sales_marketing_expense": 18000000,
                "ltm_gross_margin": 70,
                "ltm_operating_expense": 42000000,
                "ltm_ebitda": 18000000,
                "ltm_net_income": 15000000,
                "ltm_ebitda_margin": 30,
                "ltm_net_income_margin": 25,
                "fiscal_reporting_date": "2023-03-31",
                "fiscal_reporting_quarter": 1,
                "reporting_year": 2023,
                "reporting_quarter": 1
            }
        }

class ReportingMetricsCreate(ReportingMetricsBase):
    """Pydantic model for creating a new ReportingMetrics entry."""
    pass

class ReportingMetricsUpdate(BaseModel):
    """Pydantic model for updating an existing ReportingMetrics entry."""
    currency: Optional[str] = None
    enterprise_value: Optional[Decimal] = None
    arr: Optional[Decimal] = None
    recurring_percentage_revenue: Optional[Decimal] = Field(None, ge=0, le=100)
    revenue_per_fte: Optional[Decimal] = Field(None, ge=0)
    gross_profit_per_fte: Optional[Decimal] = None
    employee_growth_rate: Optional[Decimal] = None
    change_in_cash: Optional[Decimal] = None
    revenue_growth: Optional[Decimal] = None
    monthly_cash_burn: Optional[Decimal] = None
    runway_months: Optional[Decimal] = Field(None, ge=0)
    ev_by_equity_raised_plus_debt: Optional[Decimal] = None
    sales_marketing_percentage_revenue: Optional[Decimal] = Field(None, ge=0, le=100)
    total_operating_percentage_revenue: Optional[Decimal] = Field(None, ge=0, le=100)
    gross_profit_margin: Optional[Decimal] = Field(None, ge=0, le=100)
    valuation_to_revenue: Optional[Decimal] = Field(None, ge=0)
    yoy_growth_revenue: Optional[Decimal] = None
    yoy_growth_profit: Optional[Decimal] = None
    yoy_growth_employees: Optional[Decimal] = None
    yoy_growth_ltm_revenue: Optional[Decimal] = None
    ltm_total_revenue: Optional[Decimal] = Field(None, ge=0)
    ltm_gross_profit: Optional[Decimal] = None
    ltm_sales_marketing_expense: Optional[Decimal] = Field(None, ge=0)
    ltm_gross_margin: Optional[Decimal] = Field(None, ge=0, le=100)
    ltm_operating_expense: Optional[Decimal] = Field(None, ge=0)
    ltm_ebitda: Optional[Decimal] = None
    ltm_net_income: Optional[Decimal] = None
    ltm_ebitda_margin: Optional[Decimal] = None
    ltm_net_income_margin: Optional[Decimal] = None
    fiscal_reporting_date: Optional[date] = None
    fiscal_reporting_quarter: Optional[int] = Field(None, ge=1, le=4)
    reporting_year: Optional[int] = Field(None, ge=1900, le=2100)
    reporting_quarter: Optional[int] = Field(None, ge=1, le=4)

    class Config:
        """Pydantic model configuration."""
        orm_mode = True

class ReportingMetricsInDB(ReportingMetricsBase):
    """Pydantic model for ReportingMetrics as stored in the database."""
    id: UUID = Field(..., description="Unique identifier for the reporting metrics entry")
    created_date: datetime = Field(..., description="Date and time when the entry was created")
    created_by: str = Field(..., description="User who created the entry")
    last_update_date: Optional[datetime] = Field(None, description="Date and time of the last update")
    last_updated_by: Optional[str] = Field(None, description="User who last updated the entry")

class ReportingMetrics(ReportingMetricsInDB):
    """Pydantic model for ReportingMetrics responses in the API."""
    pass

# Version comment for third-party imports
# pydantic==1.10.7