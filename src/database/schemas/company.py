from pydantic import BaseModel, UUID4, Field, validator
from datetime import date
from typing import Optional
from src.database.base import Base

# Pydantic version comment
# pydantic==2.0.2

class CompanyBase(BaseModel):
    """
    Base Pydantic model for Company data.
    
    This model defines the common attributes shared by all company-related schemas.
    
    Requirements addressed:
    - Data Validation (2. SYSTEM ARCHITECTURE/2.2 Component Description/2.2.1 Application Layer)
    - API Schema Definition (3. SYSTEM DESIGN/3.3 API DESIGN)
    """
    name: str = Field(..., description="Name of the company", max_length=255)
    reporting_status: str = Field(..., description="Current reporting status of the company", max_length=50)
    reporting_currency: str = Field(..., description="Currency used for financial reporting", max_length=3)
    fund: str = Field(..., description="Fund associated with the company", max_length=100)
    location_country: str = Field(..., description="Country where the company is located", max_length=100)
    customer_type: str = Field(..., description="Type of customers the company serves", max_length=50)
    revenue_type: str = Field(..., description="Type of revenue model", max_length=50)
    equity_raised: float = Field(..., description="Total equity raised by the company", ge=0)
    post_money_valuation: float = Field(..., description="Post-money valuation of the company", ge=0)
    year_end_date: date = Field(..., description="Financial year end date")

    @validator('reporting_currency')
    def validate_currency(cls, v):
        if len(v) != 3 or not v.isalpha():
            raise ValueError('Currency must be a 3-letter alphabetic code')
        return v.upper()

    class Config:
        orm_mode = True
        extra = "forbid"

class CompanyCreate(CompanyBase):
    """
    Pydantic model for creating a new Company.
    
    This model is used when creating a new company entry in the system.
    It inherits all fields from CompanyBase.
    
    Requirements addressed:
    - API Schema Definition (3. SYSTEM DESIGN/3.3 API DESIGN)
    """
    pass

class CompanyUpdate(BaseModel):
    """
    Pydantic model for updating an existing Company.
    
    This model is used when updating an existing company entry in the system.
    All fields are optional to allow partial updates.
    
    Requirements addressed:
    - API Schema Definition (3. SYSTEM DESIGN/3.3 API DESIGN)
    """
    name: Optional[str] = Field(None, description="Name of the company", max_length=255)
    reporting_status: Optional[str] = Field(None, description="Current reporting status of the company", max_length=50)
    reporting_currency: Optional[str] = Field(None, description="Currency used for financial reporting", max_length=3)
    fund: Optional[str] = Field(None, description="Fund associated with the company", max_length=100)
    location_country: Optional[str] = Field(None, description="Country where the company is located", max_length=100)
    customer_type: Optional[str] = Field(None, description="Type of customers the company serves", max_length=50)
    revenue_type: Optional[str] = Field(None, description="Type of revenue model", max_length=50)
    equity_raised: Optional[float] = Field(None, description="Total equity raised by the company", ge=0)
    post_money_valuation: Optional[float] = Field(None, description="Post-money valuation of the company", ge=0)
    year_end_date: Optional[date] = Field(None, description="Financial year end date")

    @validator('reporting_currency')
    def validate_currency(cls, v):
        if v is not None:
            if len(v) != 3 or not v.isalpha():
                raise ValueError('Currency must be a 3-letter alphabetic code')
            return v.upper()
        return v

    class Config:
        extra = "forbid"

class CompanyInDBBase(CompanyBase):
    """
    Base Pydantic model for Company data stored in the database.
    
    This model extends CompanyBase with additional fields that are present
    in the database but not required for creation.
    
    Requirements addressed:
    - Data Validation (2. SYSTEM ARCHITECTURE/2.2 Component Description/2.2.1 Application Layer)
    - API Schema Definition (3. SYSTEM DESIGN/3.3 API DESIGN)
    """
    id: UUID4 = Field(..., description="Unique identifier for the company")
    created_date: date = Field(..., description="Date when the company entry was created")
    created_by: str = Field(..., description="User who created the company entry", max_length=100)
    last_update_date: Optional[date] = Field(None, description="Date of the last update to the company entry")
    last_updated_by: Optional[str] = Field(None, description="User who last updated the company entry", max_length=100)

class Company(CompanyInDBBase):
    """
    Pydantic model for full Company data, used for responses.
    
    This model represents the complete company data as it would be returned in API responses.
    It inherits all fields from CompanyInDBBase.
    
    Requirements addressed:
    - API Schema Definition (3. SYSTEM DESIGN/3.3 API DESIGN)
    """
    pass

class CompanyInDB(CompanyInDBBase):
    """
    Pydantic model for Company data as stored in the database.
    
    This model represents the company data exactly as it is stored in the database.
    It inherits all fields from CompanyInDBBase and is used for ORM operations.
    
    Requirements addressed:
    - Data Validation (2. SYSTEM ARCHITECTURE/2.2 Component Description/2.2.1 Application Layer)
    - API Schema Definition (3. SYSTEM DESIGN/3.3 API DESIGN)
    """
    pass

# Type aliases for improved readability
CompanyCreate = CompanyCreate
CompanyUpdate = CompanyUpdate
CompanyInDB = CompanyInDB

# Version information
__version__ = "1.1.0"

# Additional comments for developers
"""
This module defines the Pydantic models for the Company entity in our financial reporting metrics system.
These models are used for data validation, serialization, and deserialization throughout the application.

Key components:
1. CompanyBase: The base model with common fields for all company-related operations.
2. CompanyCreate: Used when creating a new company entry.
3. CompanyUpdate: Used for updating existing company entries, with all fields optional.
4. CompanyInDBBase: Extends CompanyBase with additional database-specific fields.
5. Company: Represents the full company data as returned in API responses.
6. CompanyInDB: Represents the company data as stored in the database, used for ORM operations.

When working with company data in other parts of the application, use these models for
data validation and serialization/deserialization. This ensures consistency and type safety
across the entire system.

Example usage:
from src.database.schemas.company import CompanyCreate, Company

def create_new_company(company_data: CompanyCreate) -> Company:
    # Validate input data
    validated_data = CompanyCreate(**company_data.dict())
    
    # Create company in database
    db_company = create_company_in_db(validated_data)
    
    # Return full company data
    return Company.from_orm(db_company)
"""