"""
Reporting Metrics API endpoints.

This module defines the API endpoints for managing reporting metrics data.
It includes operations for retrieving, creating, updating, and deleting reporting metrics.

Requirements addressed:
- REST API Service (2. REST API Service/F-002)
- Data Retrieval (1.2 Scope/Core Functionalities/2. Data Retrieval)
- Multi-Currency Support (1.2 Scope/Core Functionalities/4. Multi-Currency Support)
- Authentication and Authorization (6. SECURITY CONSIDERATIONS/6.1 AUTHENTICATION AND AUTHORIZATION)
- Role-Based Access Control (6. SECURITY CONSIDERATIONS/6.1 AUTHENTICATION AND AUTHORIZATION/6.1.2 Authorization)
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from uuid import UUID
from datetime import date
from sqlalchemy.orm import Session

from src.backend.schemas.reporting_metrics import ReportingMetrics, ReportingMetricsCreate, ReportingMetricsUpdate
from src.backend.core.dependencies import get_db_dependency, get_current_active_user_dependency, RoleCheckerDependency
from src.backend.crud import reporting_metrics
from src.backend.utils.error_handlers import http_error_handler
from src.backend.utils.rate_limiter import rate_limit_middleware
from src.backend.core.security import UserInDB

router = APIRouter()

# Apply rate limiting middleware to all endpoints
router = rate_limit_middleware(router)

@router.get("/{company_id}", response_model=List[ReportingMetrics])
async def get_reporting_metrics(
    company_id: UUID,
    db: Session = Depends(get_db_dependency),
    current_user: UserInDB = Depends(get_current_active_user_dependency),
    role_checker: RoleCheckerDependency = Depends(RoleCheckerDependency(["admin", "analyst"])),
    currency: Optional[str] = Query(None, description="Currency for the metrics (e.g., USD, CAD)"),
    start_date: Optional[date] = Query(None, description="Start date for filtering metrics"),
    end_date: Optional[date] = Query(None, description="End date for filtering metrics"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000)
):
    """
    Retrieve reporting metrics for a specific company.
    
    Args:
        company_id (UUID): The unique identifier of the company.
        db (Session): Database session.
        current_user (UserInDB): The current authenticated user.
        role_checker (RoleCheckerDependency): Role checker for authorization.
        currency (Optional[str]): Currency for the metrics.
        start_date (Optional[date]): Start date for filtering metrics.
        end_date (Optional[date]): End date for filtering metrics.
        skip (int): Number of records to skip.
        limit (int): Maximum number of records to return.

    Returns:
        List[ReportingMetrics]: List of reporting metrics.

    Raises:
        HTTPException: If there's an error retrieving the metrics.
    """
    try:
        filters = {}
        if currency:
            filters["currency"] = currency
        if start_date:
            filters["fiscal_reporting_date__gte"] = start_date
        if end_date:
            filters["fiscal_reporting_date__lte"] = end_date
        
        metrics = reporting_metrics.get_multi(
            db, company_id=company_id, skip=skip, limit=limit, **filters
        )
        
        return metrics
    except Exception as e:
        return http_error_handler(e)

@router.post("/", response_model=ReportingMetrics)
async def create_reporting_metrics(
    reporting_metrics_in: ReportingMetricsCreate,
    db: Session = Depends(get_db_dependency),
    current_user: UserInDB = Depends(get_current_active_user_dependency),
    role_checker: RoleCheckerDependency = Depends(RoleCheckerDependency(["admin"]))
):
    """
    Create a new reporting metrics entry.
    
    Args:
        reporting_metrics_in (ReportingMetricsCreate): The reporting metrics data to create.
        db (Session): Database session.
        current_user (UserInDB): The current authenticated user.
        role_checker (RoleCheckerDependency): Role checker for authorization.

    Returns:
        ReportingMetrics: The created reporting metrics.

    Raises:
        HTTPException: If there's an error creating the metrics.
    """
    try:
        new_metrics = reporting_metrics.create(db, obj_in=reporting_metrics_in, created_by=current_user.username)
        return new_metrics
    except Exception as e:
        return http_error_handler(e)

@router.put("/{company_id}/{fiscal_reporting_date}", response_model=ReportingMetrics)
async def update_reporting_metrics(
    company_id: UUID,
    fiscal_reporting_date: date,
    reporting_metrics_in: ReportingMetricsUpdate,
    db: Session = Depends(get_db_dependency),
    current_user: UserInDB = Depends(get_current_active_user_dependency),
    role_checker: RoleCheckerDependency = Depends(RoleCheckerDependency(["admin"]))
):
    """
    Update an existing reporting metrics entry.
    
    Args:
        company_id (UUID): The unique identifier of the company.
        fiscal_reporting_date (date): The fiscal reporting date of the metrics.
        reporting_metrics_in (ReportingMetricsUpdate): The updated reporting metrics data.
        db (Session): Database session.
        current_user (UserInDB): The current authenticated user.
        role_checker (RoleCheckerDependency): Role checker for authorization.

    Returns:
        ReportingMetrics: The updated reporting metrics.

    Raises:
        HTTPException: If the metrics are not found or there's an error updating them.
    """
    try:
        existing_metrics = reporting_metrics.get(db, company_id=company_id, fiscal_reporting_date=fiscal_reporting_date)
        if not existing_metrics:
            raise HTTPException(status_code=404, detail="Reporting metrics not found")
        
        updated_metrics = reporting_metrics.update(
            db, 
            db_obj=existing_metrics, 
            obj_in=reporting_metrics_in, 
            last_updated_by=current_user.username
        )
        
        return updated_metrics
    except Exception as e:
        return http_error_handler(e)

@router.delete("/{company_id}/{fiscal_reporting_date}")
async def delete_reporting_metrics(
    company_id: UUID,
    fiscal_reporting_date: date,
    db: Session = Depends(get_db_dependency),
    current_user: UserInDB = Depends(get_current_active_user_dependency),
    role_checker: RoleCheckerDependency = Depends(RoleCheckerDependency(["admin"]))
):
    """
    Delete a reporting metrics entry.
    
    Args:
        company_id (UUID): The unique identifier of the company.
        fiscal_reporting_date (date): The fiscal reporting date of the metrics.
        db (Session): Database session.
        current_user (UserInDB): The current authenticated user.
        role_checker (RoleCheckerDependency): Role checker for authorization.

    Returns:
        dict: A message confirming the deletion.

    Raises:
        HTTPException: If the metrics are not found or there's an error deleting them.
    """
    try:
        deleted = reporting_metrics.remove(db, company_id=company_id, fiscal_reporting_date=fiscal_reporting_date)
        
        if not deleted:
            raise HTTPException(status_code=404, detail="Reporting metrics not found")
        
        return {"message": "Reporting metrics successfully deleted"}
    except Exception as e:
        return http_error_handler(e)