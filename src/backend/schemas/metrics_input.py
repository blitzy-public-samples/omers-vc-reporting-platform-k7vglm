from pydantic import BaseModel, Field, validator
from uuid import UUID
from datetime import date, datetime
from decimal import Decimal
from typing import Optional
from src.backend.schemas.company import Company
from src.backend.models.company import ReportingStatus, CustomerType, RevenueType

class MetricsInputBase(BaseModel):
    """
    Base Pydantic model for MetricsInput data
    
    Requirements addressed:
    - Data Validation (2. SYSTEM ARCHITECTURE/2.2 Component Description/2.2.1 Application Layer)
    - API Design (3. SYSTEM DESIGN/3.3 API DESIGN)
    """
    company_id: UUID
    currency: str = Field(..., min_length=3, max_length=3)
    total_revenue: Decimal = Field(..., gt=0, max_digits=15, decimal_places=2)
    recurring_revenue: Decimal = Field(..., ge=0, max_digits=15, decimal_places=2)
    gross_profit: Decimal = Field(..., max_digits=15, decimal_places=2)
    sales_marketing_expense: Decimal = Field(..., ge=0, max_digits=15, decimal_places=2)
    total_operating_expense: Decimal = Field(..., gt=0, max_digits=15, decimal_places=2)
    ebitda: Decimal = Field(..., max_digits=15, decimal_places=2)
    net_income: Decimal = Field(..., max_digits=15, decimal_places=2)
    cash_burn: Decimal = Field(..., max_digits=15, decimal_places=2)
    cash_balance: Decimal = Field(..., ge=0, max_digits=15, decimal_places=2)
    debt_outstanding: Decimal = Field(..., ge=0, max_digits=15, decimal_places=2)
    employees: int = Field(..., gt=0)
    customers: int = Field(..., ge=0)
    fiscal_reporting_date: date
    fiscal_reporting_quarter: int = Field(..., ge=1, le=4)
    reporting_year: int = Field(..., gt=2000)
    reporting_quarter: int = Field(..., ge=1, le=4)

    @validator('currency')
    def validate_currency(cls, v):
        if not v.isalpha():
            raise ValueError('currency must be a 3-letter alphabetic code')
        return v.upper()

    class Config:
        """Pydantic configuration class"""
        orm_mode = True

class MetricsInputCreate(MetricsInputBase):
    """Pydantic model for creating a new MetricsInput"""
    pass

class MetricsInputUpdate(BaseModel):
    """Pydantic model for updating an existing MetricsInput"""
    currency: Optional[str] = Field(None, min_length=3, max_length=3)
    total_revenue: Optional[Decimal] = Field(None, gt=0, max_digits=15, decimal_places=2)
    recurring_revenue: Optional[Decimal] = Field(None, ge=0, max_digits=15, decimal_places=2)
    gross_profit: Optional[Decimal] = Field(None, max_digits=15, decimal_places=2)
    sales_marketing_expense: Optional[Decimal] = Field(None, ge=0, max_digits=15, decimal_places=2)
    total_operating_expense: Optional[Decimal] = Field(None, gt=0, max_digits=15, decimal_places=2)
    ebitda: Optional[Decimal] = Field(None, max_digits=15, decimal_places=2)
    net_income: Optional[Decimal] = Field(None, max_digits=15, decimal_places=2)
    cash_burn: Optional[Decimal] = Field(None, max_digits=15, decimal_places=2)
    cash_balance: Optional[Decimal] = Field(None, ge=0, max_digits=15, decimal_places=2)
    debt_outstanding: Optional[Decimal] = Field(None, ge=0, max_digits=15, decimal_places=2)
    employees: Optional[int] = Field(None, gt=0)
    customers: Optional[int] = Field(None, ge=0)
    fiscal_reporting_date: Optional[date] = None
    fiscal_reporting_quarter: Optional[int] = Field(None, ge=1, le=4)
    reporting_year: Optional[int] = Field(None, gt=2000)
    reporting_quarter: Optional[int] = Field(None, ge=1, le=4)

    @validator('currency')
    def validate_currency(cls, v):
        if v is not None:
            if not v.isalpha() or len(v) != 3:
                raise ValueError('currency must be a 3-letter alphabetic code')
            return v.upper()
        return v

class MetricsInputInDBBase(MetricsInputBase):
    """Base Pydantic model for MetricsInput data stored in the database"""
    id: UUID
    created_date: datetime
    created_by: str = Field(..., max_length=100)
    last_update_date: Optional[datetime] = None
    last_updated_by: Optional[str] = Field(None, max_length=100)

class MetricsInput(MetricsInputInDBBase):
    """Pydantic model for full MetricsInput data, used for responses"""
    company: Company

class MetricsInputInDB(MetricsInputInDBBase):
    """Pydantic model for MetricsInput data as stored in the database"""
    pass

# Additional comments for junior developers:
# - The MetricsInputBase class defines the core structure of the metrics input data.
# - Field(...) is used to specify required fields with additional validation.
# - The Config class with orm_mode=True allows the model to work with ORMs.
# - MetricsInputCreate inherits from MetricsInputBase without changes.
# - MetricsInputUpdate allows for partial updates with all fields being optional.
# - MetricsInputInDBBase adds database-specific fields like id and timestamps.
# - MetricsInput includes the full Company object, which is useful for API responses.
# - MetricsInputInDB represents the data as stored in the database.
# - Validators are used to ensure data integrity, such as the currency validator.
# - Decimal fields use max_digits and decimal_places for precise financial calculations.
# - The file structure follows best practices for separation of concerns and modularity.