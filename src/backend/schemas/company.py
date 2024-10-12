from pydantic import BaseModel, Field, validator
from uuid import UUID
from datetime import date, datetime
from decimal import Decimal
from typing import Optional
from src.backend.models.company import ReportingStatus, CustomerType, RevenueType

class CompanyBase(BaseModel):
    """
    Base Pydantic model for Company data.
    
    Requirements addressed:
    - Data Validation (2. SYSTEM ARCHITECTURE/2.2 Component Description/2.2.1 Application Layer)
    - API Design (3. SYSTEM DESIGN/3.3 API DESIGN)
    """
    name: str = Field(..., max_length=255)
    reporting_status: ReportingStatus
    reporting_currency: str = Field(..., min_length=3, max_length=3)
    fund: str = Field(..., max_length=100)
    location_country: str = Field(..., max_length=100)
    customer_type: CustomerType
    revenue_type: RevenueType
    equity_raised: Decimal = Field(..., ge=0, max_digits=15, decimal_places=2)
    post_money_valuation: Decimal = Field(..., ge=0, max_digits=15, decimal_places=2)
    year_end_date: date

    @validator('reporting_currency')
    def validate_reporting_currency(cls, v):
        if not v.isalpha() or len(v) != 3:
            raise ValueError('reporting_currency must be a 3-letter alphabetic code')
        return v.upper()

class CompanyCreate(CompanyBase):
    """
    Pydantic model for creating a new Company.
    Inherits all fields from CompanyBase.
    """
    pass

class CompanyUpdate(BaseModel):
    """
    Pydantic model for updating an existing Company.
    All fields are optional to allow partial updates.
    """
    name: Optional[str] = Field(None, max_length=255)
    reporting_status: Optional[ReportingStatus] = None
    reporting_currency: Optional[str] = Field(None, min_length=3, max_length=3)
    fund: Optional[str] = Field(None, max_length=100)
    location_country: Optional[str] = Field(None, max_length=100)
    customer_type: Optional[CustomerType] = None
    revenue_type: Optional[RevenueType] = None
    equity_raised: Optional[Decimal] = Field(None, ge=0, max_digits=15, decimal_places=2)
    post_money_valuation: Optional[Decimal] = Field(None, ge=0, max_digits=15, decimal_places=2)
    year_end_date: Optional[date] = None

    @validator('reporting_currency')
    def validate_reporting_currency(cls, v):
        if v is not None:
            if not v.isalpha() or len(v) != 3:
                raise ValueError('reporting_currency must be a 3-letter alphabetic code')
            return v.upper()
        return v

class CompanyInDBBase(CompanyBase):
    """
    Base Pydantic model for Company data stored in the database.
    Includes all fields from CompanyBase plus additional database-specific fields.
    """
    id: UUID
    created_date: datetime
    created_by: str = Field(..., max_length=100)
    last_update_date: Optional[datetime] = None
    last_updated_by: Optional[str] = Field(None, max_length=100)

    class Config:
        orm_mode = True

class Company(CompanyInDBBase):
    """
    Pydantic model for Company data returned in API responses.
    Inherits all fields from CompanyInDBBase.
    """
    pass

class CompanyInDB(CompanyInDBBase):
    """
    Pydantic model for Company data as stored in the database.
    Inherits all fields from CompanyInDBBase.
    This model can be used for operations that require the full database representation.
    """
    pass