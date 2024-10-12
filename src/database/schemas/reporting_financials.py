from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime, date
from typing import Optional
from src.database.base import Base

# Requirements addressed:
# 1. Data Validation (2. SYSTEM ARCHITECTURE/2.2 Component Description/2.2.1 Application Layer)
# 2. Multi-Currency Support (1.2 Scope/Core Functionalities/4. Multi-Currency Support)

class ReportingFinancialsBase(BaseModel):
    """
    Base Pydantic model for Reporting Financials with common fields.
    This model defines the structure for financial data reported by portfolio companies.
    """
    company_id: UUID = Field(..., description="Unique identifier of the company")
    currency: str = Field(..., description="Currency used for financial reporting")
    exchange_rate_used: float = Field(..., description="Exchange rate used for currency conversion")
    total_revenue: float = Field(..., description="Total revenue for the reporting period")
    recurring_revenue: float = Field(..., description="Recurring revenue for the reporting period")
    gross_profit: float = Field(..., description="Gross profit for the reporting period")
    debt_outstanding: Optional[float] = Field(None, description="Outstanding debt, if applicable")
    sales_marketing_expense: float = Field(..., description="Sales and marketing expenses")
    total_operating_expense: float = Field(..., description="Total operating expenses")
    ebitda: float = Field(..., description="Earnings Before Interest, Taxes, Depreciation, and Amortization")
    net_income: float = Field(..., description="Net income for the reporting period")
    cash_burn: float = Field(..., description="Cash burn rate for the reporting period")
    cash_balance: float = Field(..., description="Cash balance at the end of the reporting period")
    fiscal_reporting_date: date = Field(..., description="Date of the fiscal report")
    fiscal_reporting_quarter: int = Field(..., ge=1, le=4, description="Fiscal quarter of the report (1-4)")
    reporting_year: int = Field(..., description="Year of the report")
    reporting_quarter: int = Field(..., ge=1, le=4, description="Calendar quarter of the report (1-4)")

    class Config:
        orm_mode = True

class ReportingFinancialsCreate(ReportingFinancialsBase):
    """
    Pydantic model for creating new Reporting Financials entries.
    This model inherits all fields from ReportingFinancialsBase.
    """
    pass

class ReportingFinancialsUpdate(BaseModel):
    """
    Pydantic model for updating existing Reporting Financials entries.
    This model allows partial updates of financial data.
    """
    exchange_rate_used: Optional[float] = Field(None, description="Updated exchange rate")
    total_revenue: Optional[float] = Field(None, description="Updated total revenue")
    recurring_revenue: Optional[float] = Field(None, description="Updated recurring revenue")
    gross_profit: Optional[float] = Field(None, description="Updated gross profit")
    debt_outstanding: Optional[float] = Field(None, description="Updated outstanding debt")
    sales_marketing_expense: Optional[float] = Field(None, description="Updated sales and marketing expenses")
    total_operating_expense: Optional[float] = Field(None, description="Updated total operating expenses")
    ebitda: Optional[float] = Field(None, description="Updated EBITDA")
    net_income: Optional[float] = Field(None, description="Updated net income")
    cash_burn: Optional[float] = Field(None, description="Updated cash burn rate")
    cash_balance: Optional[float] = Field(None, description="Updated cash balance")

    class Config:
        orm_mode = True

class ReportingFinancialsInDB(ReportingFinancialsBase):
    """
    Pydantic model for Reporting Financials as stored in the database.
    This model extends ReportingFinancialsBase with additional database-specific fields.
    """
    id: UUID = Field(..., description="Unique identifier for the financial report")
    created_date: datetime = Field(..., description="Timestamp of when the report was created")
    created_by: str = Field(..., description="User who created the report")
    last_update_date: Optional[datetime] = Field(None, description="Timestamp of the last update")
    last_updated_by: Optional[str] = Field(None, description="User who last updated the report")

    class Config:
        orm_mode = True

class ReportingFinancials(ReportingFinancialsInDB):
    """
    Pydantic model for complete Reporting Financials data.
    This model represents the full set of financial data, including database-specific fields.
    """
    pass

# Note: The Base import from src.database.base is not used directly in this file,
# but it's included to maintain consistency with the project structure.
# It may be used in other parts of the application for ORM operations.