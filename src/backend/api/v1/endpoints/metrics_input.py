from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from datetime import date

from src.backend.core.dependencies import (
    get_db_dependency,
    get_current_active_user_dependency,
    RoleCheckerDependency
)
from src.backend.schemas.metrics_input import (
    MetricsInputCreate,
    MetricsInputUpdate,
    MetricsInput
)
from src.backend.crud.metrics_input import metrics_input
from src.backend.utils.error_handlers import http_error_handler
from src.backend.utils.rate_limiter import rate_limit_middleware
from src.backend.core.security import UserInDB

router = APIRouter()

# Apply rate limiting middleware to all routes in this router
router = rate_limit_middleware(router)

@router.post("/", response_model=MetricsInput, status_code=status.HTTP_201_CREATED)
async def create_metrics_input(
    metrics_input_in: MetricsInputCreate,
    db: Session = Depends(get_db_dependency),
    current_user: UserInDB = Depends(get_current_active_user_dependency),
    role_checker: RoleCheckerDependency = Depends(RoleCheckerDependency(["admin", "portfolio_manager"]))
):
    """
    Create a new metrics input record.
    
    This endpoint allows creating a new metrics input record for a company.
    Only users with 'admin' or 'portfolio_manager' roles can access this endpoint.
    
    Requirements addressed:
    - REST API Service (2. REST API Service/F-002): Implements POST endpoints for adding data in Input Metrics tables
    - Data Validation (2. SYSTEM ARCHITECTURE/2.2 Component Description/2.2.1 Application Layer): Implements request validation using Pydantic schemas for metrics input data
    """
    try:
        # Check if a record already exists for the given company and date
        existing_record = metrics_input.get_by_company_and_date(
            db, company_id=metrics_input_in.company_id, fiscal_reporting_date=metrics_input_in.fiscal_reporting_date
        )
        if existing_record:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A metrics input record already exists for this company and date."
            )
        
        # Create the new metrics input record
        new_metrics_input = metrics_input.create_with_company(
            db=db, obj_in=metrics_input_in, company_id=metrics_input_in.company_id
        )
        return new_metrics_input
    except Exception as e:
        return http_error_handler(e)

@router.get("/{metrics_input_id}", response_model=MetricsInput)
async def get_metrics_input(
    metrics_input_id: UUID,
    db: Session = Depends(get_db_dependency),
    current_user: UserInDB = Depends(get_current_active_user_dependency),
    role_checker: RoleCheckerDependency = Depends(RoleCheckerDependency(["admin", "portfolio_manager", "analyst"]))
):
    """
    Retrieve a metrics input record by ID.
    
    This endpoint allows retrieving a specific metrics input record by its ID.
    Users with 'admin', 'portfolio_manager', or 'analyst' roles can access this endpoint.
    
    Requirements addressed:
    - Data Retrieval (1.2 Scope/Core Functionalities/2. Data Retrieval): Implements GET endpoints for retrieving metrics input data
    """
    try:
        metrics_input_record = metrics_input.get(db, id=metrics_input_id)
        if not metrics_input_record:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Metrics input record not found")
        return metrics_input_record
    except Exception as e:
        return http_error_handler(e)

@router.put("/{metrics_input_id}", response_model=MetricsInput)
async def update_metrics_input(
    metrics_input_id: UUID,
    metrics_input_in: MetricsInputUpdate,
    db: Session = Depends(get_db_dependency),
    current_user: UserInDB = Depends(get_current_active_user_dependency),
    role_checker: RoleCheckerDependency = Depends(RoleCheckerDependency(["admin", "portfolio_manager"]))
):
    """
    Update an existing metrics input record.
    
    This endpoint allows updating an existing metrics input record.
    Only users with 'admin' or 'portfolio_manager' roles can access this endpoint.
    
    Requirements addressed:
    - REST API Service (2. REST API Service/F-002): Implements PUT endpoints for updating data in Input Metrics tables
    - Data Validation (2. SYSTEM ARCHITECTURE/2.2 Component Description/2.2.1 Application Layer): Implements request validation using Pydantic schemas for metrics input data
    """
    try:
        existing_record = metrics_input.get(db, id=metrics_input_id)
        if not existing_record:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Metrics input record not found")
        
        updated_record = metrics_input.update(db, db_obj=existing_record, obj_in=metrics_input_in)
        return updated_record
    except Exception as e:
        return http_error_handler(e)

@router.delete("/{metrics_input_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_metrics_input(
    metrics_input_id: UUID,
    db: Session = Depends(get_db_dependency),
    current_user: UserInDB = Depends(get_current_active_user_dependency),
    role_checker: RoleCheckerDependency = Depends(RoleCheckerDependency(["admin"]))
):
    """
    Delete a metrics input record.
    
    This endpoint allows deleting a specific metrics input record.
    Only users with the 'admin' role can access this endpoint.
    
    Requirements addressed:
    - Data Management (1. Data Storage and Management/F-001): Implements deletion of metrics input records
    """
    try:
        existing_record = metrics_input.get(db, id=metrics_input_id)
        if not existing_record:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Metrics input record not found")
        
        metrics_input.remove(db, id=metrics_input_id)
        return {"message": "Metrics input record successfully deleted"}
    except Exception as e:
        return http_error_handler(e)

@router.get("/", response_model=List[MetricsInput])
async def get_metrics_inputs(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db_dependency),
    current_user: UserInDB = Depends(get_current_active_user_dependency),
    role_checker: RoleCheckerDependency = Depends(RoleCheckerDependency(["admin", "portfolio_manager", "analyst"]))
):
    """
    Retrieve a list of metrics input records with pagination.
    
    This endpoint allows retrieving a list of metrics input records with pagination support.
    Users with 'admin', 'portfolio_manager', or 'analyst' roles can access this endpoint.
    
    Requirements addressed:
    - Data Retrieval (1.2 Scope/Core Functionalities/2. Data Retrieval): Implements GET endpoints for retrieving metrics input data
    """
    try:
        metrics_input_records = metrics_input.get_multi(db, skip=skip, limit=limit)
        return metrics_input_records
    except Exception as e:
        return http_error_handler(e)

# Note: The router is included in the main FastAPI app in the main.py file