from uuid import UUID
from datetime import date
from typing import Optional
from pydantic import BaseModel, Field, validator
from src.database.base import Base

# Version comment for third-party imports
# uuid: ^3.8
# datetime: ^3.8
# pydantic: ^1.8

class MetricsInputBase(BaseModel):
    """
    Base Pydantic model for MetricsInput with common attributes.

    This model defines the common structure for metrics input data, including
    financial metrics and reporting information for a specific company and period.

    Requirements addressed:
    - Data Validation (2. SYSTEM ARCHITECTURE/2.2 Component Description/2.2.1 Application Layer)
    - API Schema (3. SYSTEM DESIGN/3.3 API DESIGN)
    """
    company_id: UUID
    currency: str = Field(..., min_length=3, max_length=3)
    total_revenue: float = Field(..., gt=0)
    recurring_revenue: float = Field(..., ge=0)
    gross_profit: float
    sales_marketing_expense: float = Field(..., ge=0)
    total_operating_expense: float = Field(..., gt=0)
    ebitda: float
    net_income: float
    cash_burn: float
    cash_balance: float = Field(..., ge=0)
    debt_outstanding: float = Field(..., ge=0)
    employees: int = Field(..., gt=0)
    customers: int = Field(..., ge=0)
    fiscal_reporting_date: date
    fiscal_reporting_quarter: int = Field(..., ge=1, le=4)
    reporting_year: int = Field(..., ge=2000)
    reporting_quarter: int = Field(..., ge=1, le=4)

    @validator('currency')
    def validate_currency(cls, v):
        if not v.isalpha() or len(v) != 3:
            raise ValueError('Currency must be a 3-letter alphabetic code')
        return v.upper()

    @validator('recurring_revenue')
    def validate_recurring_revenue(cls, v, values):
        if 'total_revenue' in values and v > values['total_revenue']:
            raise ValueError('Recurring revenue cannot be greater than total revenue')
        return v

    @validator('total_operating_expense')
    def validate_total_operating_expense(cls, v, values):
        if 'sales_marketing_expense' in values and v < values['sales_marketing_expense']:
            raise ValueError('Total operating expense must be greater than or equal to sales and marketing expense')
        return v

    class Config:
        orm_mode = True
        extra = 'forbid'

class MetricsInputCreate(MetricsInputBase):
    """
    Pydantic model for creating a new MetricsInput entry.

    This model is used when submitting new metrics data to the system.
    It inherits all fields from MetricsInputBase.

    Requirements addressed:
    - Data Validation (2. SYSTEM ARCHITECTURE/2.2 Component Description/2.2.1 Application Layer)
    - API Schema (3. SYSTEM DESIGN/3.3 API DESIGN)
    """
    pass

class MetricsInputUpdate(BaseModel):
    """
    Pydantic model for updating an existing MetricsInput entry.

    This model is used when updating metrics data in the system.
    All fields are optional to allow partial updates.

    Requirements addressed:
    - Data Validation (2. SYSTEM ARCHITECTURE/2.2 Component Description/2.2.1 Application Layer)
    - API Schema (3. SYSTEM DESIGN/3.3 API DESIGN)
    """
    company_id: Optional[UUID] = None
    currency: Optional[str] = Field(None, min_length=3, max_length=3)
    total_revenue: Optional[float] = Field(None, gt=0)
    recurring_revenue: Optional[float] = Field(None, ge=0)
    gross_profit: Optional[float] = None
    sales_marketing_expense: Optional[float] = Field(None, ge=0)
    total_operating_expense: Optional[float] = Field(None, gt=0)
    ebitda: Optional[float] = None
    net_income: Optional[float] = None
    cash_burn: Optional[float] = None
    cash_balance: Optional[float] = Field(None, ge=0)
    debt_outstanding: Optional[float] = Field(None, ge=0)
    employees: Optional[int] = Field(None, gt=0)
    customers: Optional[int] = Field(None, ge=0)
    fiscal_reporting_date: Optional[date] = None
    fiscal_reporting_quarter: Optional[int] = Field(None, ge=1, le=4)
    reporting_year: Optional[int] = Field(None, ge=2000)
    reporting_quarter: Optional[int] = Field(None, ge=1, le=4)

    @validator('currency')
    def validate_currency(cls, v):
        if v is not None:
            if not v.isalpha() or len(v) != 3:
                raise ValueError('Currency must be a 3-letter alphabetic code')
            return v.upper()
        return v

    class Config:
        orm_mode = True
        extra = 'forbid'

class MetricsInputInDB(MetricsInputBase):
    """
    Pydantic model representing a MetricsInput entry as stored in the database.

    This model extends MetricsInputBase by adding an 'id' field, which is
    automatically generated when a new entry is created in the database.

    Requirements addressed:
    - Data Validation (2. SYSTEM ARCHITECTURE/2.2 Component Description/2.2.1 Application Layer)
    - API Schema (3. SYSTEM DESIGN/3.3 API DESIGN)
    """
    id: UUID

class MetricsInput(MetricsInputInDB):
    """
    Pydantic model for general use of MetricsInput data.

    This model is used for returning metrics input data from the API.
    It includes all fields from MetricsInputInDB.

    Requirements addressed:
    - Data Validation (2. SYSTEM ARCHITECTURE/2.2 Component Description/2.2.1 Application Layer)
    - API Schema (3. SYSTEM DESIGN/3.3 API DESIGN)
    """
    pass

# Ensure that the MetricsInput model is properly associated with the SQLAlchemy Base
MetricsInput.update_forward_refs()