from fastapi import APIRouter, Depends, HTTPException, Query, Request
from fastapi.exceptions import RequestValidationError
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID
from datetime import date, datetime

from src.backend.api.v1 import api_router
from src.backend.schemas.reporting_financials import (
    ReportingFinancialsCreate,
    ReportingFinancialsUpdate,
    ReportingFinancials,
)
from src.backend.crud import reporting_financials
from src.backend.models.reporting_financials import ReportingFinancials as ReportingFinancialsModel
from src.backend.core.dependencies import (
    get_db,
    get_current_active_user,
    RoleChecker,
)
from src.backend.utils.error_handlers import http_error_handler, validation_error_handler
from src.backend.utils.rate_limiter import rate_limit

# Create a router for reporting financials endpoints
router = APIRouter()

# Apply rate limiting middleware to all routes in this router
@router.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    return await rate_limit(request, call_next)

@router.post("/", response_model=ReportingFinancials, status_code=201)
async def create_reporting_financials(
    financials_in: ReportingFinancialsCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_active_user),
    role_checker: RoleChecker = Depends(RoleChecker(["admin", "portfolio_manager"]))
):
    """
    Create a new reporting financials entry.
    
    Requirements addressed:
    - REST API Service (2. REST API Service/F-002)
    - Data Retrieval (1.2 Scope/Core Functionalities/2. Data Retrieval)
    - Multi-Currency Support (1.2 Scope/Core Functionalities/4. Multi-Currency Support)
    - Security and Compliance (1.2 Scope/Core Functionalities/5. Security and Compliance)
    """
    existing_financials = reporting_financials.get_by_company_and_date(
        db, company_id=financials_in.company_id, fiscal_reporting_date=financials_in.fiscal_reporting_date
    )
    if existing_financials:
        raise HTTPException(
            status_code=400,
            detail="Reporting financials entry already exists for this company and fiscal reporting date",
        )
    
    new_financials = reporting_financials.create_with_company(
        db=db, obj_in=financials_in, company_id=financials_in.company_id
    )
    return new_financials

@router.get("/{company_id}/{fiscal_reporting_date}", response_model=ReportingFinancials)
async def get_reporting_financials(
    company_id: UUID,
    fiscal_reporting_date: date,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_active_user),
    role_checker: RoleChecker = Depends(RoleChecker(["admin", "portfolio_manager", "analyst"]))
):
    """
    Retrieve a specific reporting financials entry.
    
    Requirements addressed:
    - REST API Service (2. REST API Service/F-002)
    - Data Retrieval (1.2 Scope/Core Functionalities/2. Data Retrieval)
    - Security and Compliance (1.2 Scope/Core Functionalities/5. Security and Compliance)
    """
    financials = reporting_financials.get_by_company_and_date(db, company_id=company_id, fiscal_reporting_date=fiscal_reporting_date)
    if not financials:
        raise HTTPException(status_code=404, detail="Reporting financials not found")
    return financials

@router.get("/", response_model=List[ReportingFinancials])
async def list_reporting_financials(
    company_id: Optional[UUID] = None,
    year: Optional[int] = None,
    quarter: Optional[int] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_active_user),
    role_checker: RoleChecker = Depends(RoleChecker(["admin", "portfolio_manager", "analyst"]))
):
    """
    Retrieve a list of reporting financials entries.
    
    Requirements addressed:
    - REST API Service (2. REST API Service/F-002)
    - Data Retrieval (1.2 Scope/Core Functionalities/2. Data Retrieval)
    - Security and Compliance (1.2 Scope/Core Functionalities/5. Security and Compliance)
    """
    filters = {}
    if company_id:
        filters["company_id"] = company_id
    if year:
        filters["reporting_year"] = year
    if quarter:
        filters["reporting_quarter"] = quarter
    
    financials_list = reporting_financials.get_multi(db, skip=skip, limit=limit, **filters)
    return financials_list

@router.put("/{company_id}/{fiscal_reporting_date}", response_model=ReportingFinancials)
async def update_reporting_financials(
    company_id: UUID,
    fiscal_reporting_date: date,
    financials_in: ReportingFinancialsUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_active_user),
    role_checker: RoleChecker = Depends(RoleChecker(["admin", "portfolio_manager"]))
):
    """
    Update an existing reporting financials entry.
    
    Requirements addressed:
    - REST API Service (2. REST API Service/F-002)
    - Data Retrieval (1.2 Scope/Core Functionalities/2. Data Retrieval)
    - Multi-Currency Support (1.2 Scope/Core Functionalities/4. Multi-Currency Support)
    - Security and Compliance (1.2 Scope/Core Functionalities/5. Security and Compliance)
    """
    existing_financials = reporting_financials.get_by_company_and_date(db, company_id=company_id, fiscal_reporting_date=fiscal_reporting_date)
    if not existing_financials:
        raise HTTPException(status_code=404, detail="Reporting financials not found")
    
    updated_financials = reporting_financials.update(db, db_obj=existing_financials, obj_in=financials_in)
    return updated_financials

@router.delete("/{company_id}/{fiscal_reporting_date}", status_code=204)
async def delete_reporting_financials(
    company_id: UUID,
    fiscal_reporting_date: date,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_active_user),
    role_checker: RoleChecker = Depends(RoleChecker(["admin"]))
):
    """
    Delete a reporting financials entry.
    
    Requirements addressed:
    - REST API Service (2. REST API Service/F-002)
    - Security and Compliance (1.2 Scope/Core Functionalities/5. Security and Compliance)
    """
    existing_financials = reporting_financials.get_by_company_and_date(db, company_id=company_id, fiscal_reporting_date=fiscal_reporting_date)
    if not existing_financials:
        raise HTTPException(status_code=404, detail="Reporting financials not found")
    
    reporting_financials.remove(db, id=existing_financials.id)

# Add error handlers
api_router.add_exception_handler(HTTPException, http_error_handler)
api_router.add_exception_handler(RequestValidationError, validation_error_handler)

# Include the reporting financials router in the main API router
api_router.include_router(router, prefix="/reporting-financials", tags=["reporting-financials"])