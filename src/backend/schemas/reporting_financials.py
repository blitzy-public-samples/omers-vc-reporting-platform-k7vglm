from uuid import UUID
from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, Field, constr, validator
from src.backend.db.base import Base  # Import for type hinting

# Pydantic version comment
# pydantic==1.10.7

class ReportingFinancialsBase(BaseModel):
    """
    Base Pydantic model for ReportingFinancials with common fields.

    This model implements data validation for the ReportingFinancials entity as per the
    requirements specified in '3. SYSTEM DESIGN/3.3 API DESIGN'.

    It also supports multi-currency functionality as outlined in
    '1.2 Scope/Core Functionalities/4. Multi-Currency Support'.
    """
    company_id: UUID
    currency: constr(min_length=3, max_length=3)
    exchange_rate_used: float = Field(..., gt=0)
    total_revenue: float = Field(..., ge=0)
    recurring_revenue: float = Field(..., ge=0)
    gross_profit: float
    sales_marketing_expense: float = Field(..., ge=0)
    total_operating_expense: float = Field(..., ge=0)
    ebitda: float
    net_income: float
    cash_burn: float
    cash_balance: float = Field(..., ge=0)
    debt_outstanding: float = Field(..., ge=0)
    fiscal_reporting_date: date
    fiscal_reporting_quarter: int = Field(..., ge=1, le=4)
    reporting_year: int
    reporting_quarter: int = Field(..., ge=1, le=4)

    @validator('currency')
    def validate_currency(cls, v):
        if not v.isalpha() or not v.isupper():
            raise ValueError('Currency must be a 3-letter uppercase alphabetic code')
        return v

    @validator('reporting_year')
    def validate_reporting_year(cls, v):
        current_year = datetime.now().year
        if v < 1900 or v > current_year + 1:
            raise ValueError(f'Reporting year must be between 1900 and {current_year + 1}')
        return v

    class Config:
        extra = "forbid"

class ReportingFinancialsCreate(ReportingFinancialsBase):
    """
    Pydantic model for creating a new ReportingFinancials entry.
    This model inherits all fields from ReportingFinancialsBase.
    """
    pass

class ReportingFinancialsUpdate(BaseModel):
    """
    Pydantic model for updating an existing ReportingFinancials entry.
    This model makes all fields from ReportingFinancialsBase optional.
    """
    company_id: Optional[UUID] = None
    currency: Optional[constr(min_length=3, max_length=3)] = None
    exchange_rate_used: Optional[float] = Field(None, gt=0)
    total_revenue: Optional[float] = Field(None, ge=0)
    recurring_revenue: Optional[float] = Field(None, ge=0)
    gross_profit: Optional[float] = None
    sales_marketing_expense: Optional[float] = Field(None, ge=0)
    total_operating_expense: Optional[float] = Field(None, ge=0)
    ebitda: Optional[float] = None
    net_income: Optional[float] = None
    cash_burn: Optional[float] = None
    cash_balance: Optional[float] = Field(None, ge=0)
    debt_outstanding: Optional[float] = Field(None, ge=0)
    fiscal_reporting_date: Optional[date] = None
    fiscal_reporting_quarter: Optional[int] = Field(None, ge=1, le=4)
    reporting_year: Optional[int] = None
    reporting_quarter: Optional[int] = Field(None, ge=1, le=4)

    @validator('currency')
    def validate_currency(cls, v):
        if v is not None and (not v.isalpha() or not v.isupper()):
            raise ValueError('Currency must be a 3-letter uppercase alphabetic code')
        return v

    @validator('reporting_year')
    def validate_reporting_year(cls, v):
        if v is not None:
            current_year = datetime.now().year
            if v < 1900 or v > current_year + 1:
                raise ValueError(f'Reporting year must be between 1900 and {current_year + 1}')
        return v

    class Config:
        extra = "forbid"

class ReportingFinancialsInDBBase(ReportingFinancialsBase):
    """
    Base Pydantic model for ReportingFinancials with database-specific fields.
    This model extends ReportingFinancialsBase with fields that are present in the database.
    """
    id: UUID
    created_date: datetime
    created_by: str
    last_update_date: Optional[datetime] = None
    last_updated_by: Optional[str] = None

    class Config:
        orm_mode = True
        extra = "forbid"

class ReportingFinancials(ReportingFinancialsInDBBase):
    """
    Pydantic model for reading ReportingFinancials data.
    This model is used for returning ReportingFinancials data from the API.
    """
    pass

class ReportingFinancialsInDB(ReportingFinancialsInDBBase):
    """
    Pydantic model representing a ReportingFinancials entry in the database.
    This model is used for internal operations and includes all database fields.
    """
    pass

# Type hint for SQLAlchemy model
ReportingFinancialsModel = Base