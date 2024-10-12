from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.backend.schemas.company import Company, CompanyCreate, CompanyUpdate
from src.backend.core.dependencies import get_db_dependency, get_current_active_user_dependency, RoleCheckerDependency
from src.backend.crud.company import company
from src.backend.core.security import UserInDB

router = APIRouter()

@router.get("/", response_model=List[Company])
def get_companies(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db_dependency),
    current_user: UserInDB = Depends(get_current_active_user_dependency),
    role_checker: RoleCheckerDependency = Depends(RoleCheckerDependency(["admin", "portfolio_manager"]))
):
    """
    Retrieve a list of all companies.
    
    Args:
        skip (int): Number of records to skip (for pagination).
        limit (int): Maximum number of records to return.
        db (Session): Database session.
        current_user (UserInDB): Current authenticated user.
        role_checker (RoleCheckerDependency): Role checker for authorization.
    
    Returns:
        List[Company]: List of companies.
    
    Requirements addressed:
    - REST API Service (2. REST API Service/F-002): Implements GET endpoint for retrieving company data
    - Authentication and Authorization (6. SECURITY CONSIDERATIONS/6.1 AUTHENTICATION AND AUTHORIZATION): Implements role-based access control
    - Pagination (2.4 Scalability and Performance Considerations): Implements pagination for large datasets
    """
    return company.get_multi(db, skip=skip, limit=limit)

@router.get("/{company_id}", response_model=Company)
def get_company(
    company_id: UUID,
    db: Session = Depends(get_db_dependency),
    current_user: UserInDB = Depends(get_current_active_user_dependency),
    role_checker: RoleCheckerDependency = Depends(RoleCheckerDependency(["admin", "portfolio_manager", "analyst"]))
):
    """
    Retrieve a specific company by ID.
    
    Args:
        company_id (UUID): ID of the company to retrieve.
        db (Session): Database session.
        current_user (UserInDB): Current authenticated user.
        role_checker (RoleCheckerDependency): Role checker for authorization.
    
    Returns:
        Company: The requested company.
    
    Raises:
        HTTPException: If the company is not found.
    
    Requirements addressed:
    - REST API Service (2. REST API Service/F-002): Implements GET endpoint for retrieving specific company data
    - Authentication and Authorization (6. SECURITY CONSIDERATIONS/6.1 AUTHENTICATION AND AUTHORIZATION): Implements role-based access control
    """
    db_company = company.get(db, id=company_id)
    if db_company is None:
        raise HTTPException(status_code=404, detail="Company not found")
    return db_company

@router.post("/", response_model=Company, status_code=status.HTTP_201_CREATED)
def create_company(
    company_in: CompanyCreate,
    db: Session = Depends(get_db_dependency),
    current_user: UserInDB = Depends(get_current_active_user_dependency),
    role_checker: RoleCheckerDependency = Depends(RoleCheckerDependency(["admin", "portfolio_manager"]))
):
    """
    Create a new company.
    
    Args:
        company_in (CompanyCreate): Company data to create.
        db (Session): Database session.
        current_user (UserInDB): Current authenticated user.
        role_checker (RoleCheckerDependency): Role checker for authorization.
    
    Returns:
        Company: The created company.
    
    Raises:
        HTTPException: If a company with the same name already exists.
    
    Requirements addressed:
    - REST API Service (2. REST API Service/F-002): Implements POST endpoint for creating company data
    - Data Storage and Management (1. Data Storage and Management/F-001): Interacts with the database to store company information
    - Authentication and Authorization (6. SECURITY CONSIDERATIONS/6.1 AUTHENTICATION AND AUTHORIZATION): Implements role-based access control
    """
    db_company = company.get_by_name(db, name=company_in.name)
    if db_company:
        raise HTTPException(
            status_code=400,
            detail="A company with this name already exists in the system."
        )
    company_in.created_by = current_user.username
    return company.create(db=db, obj_in=company_in)

@router.put("/{company_id}", response_model=Company)
def update_company(
    company_id: UUID,
    company_in: CompanyUpdate,
    db: Session = Depends(get_db_dependency),
    current_user: UserInDB = Depends(get_current_active_user_dependency),
    role_checker: RoleCheckerDependency = Depends(RoleCheckerDependency(["admin", "portfolio_manager"]))
):
    """
    Update an existing company.
    
    Args:
        company_id (UUID): ID of the company to update.
        company_in (CompanyUpdate): Company data to update.
        db (Session): Database session.
        current_user (UserInDB): Current authenticated user.
        role_checker (RoleCheckerDependency): Role checker for authorization.
    
    Returns:
        Company: The updated company.
    
    Raises:
        HTTPException: If the company is not found.
    
    Requirements addressed:
    - REST API Service (2. REST API Service/F-002): Implements PUT endpoint for updating company data
    - Data Storage and Management (1. Data Storage and Management/F-001): Interacts with the database to update company information
    - Authentication and Authorization (6. SECURITY CONSIDERATIONS/6.1 AUTHENTICATION AND AUTHORIZATION): Implements role-based access control
    """
    db_company = company.get(db, id=company_id)
    if db_company is None:
        raise HTTPException(status_code=404, detail="Company not found")
    company_in.last_updated_by = current_user.username
    return company.update(db=db, db_obj=db_company, obj_in=company_in)

@router.delete("/{company_id}", response_model=Company)
def delete_company(
    company_id: UUID,
    db: Session = Depends(get_db_dependency),
    current_user: UserInDB = Depends(get_current_active_user_dependency),
    role_checker: RoleCheckerDependency = Depends(RoleCheckerDependency(["admin"]))
):
    """
    Delete a company.
    
    Args:
        company_id (UUID): ID of the company to delete.
        db (Session): Database session.
        current_user (UserInDB): Current authenticated user.
        role_checker (RoleCheckerDependency): Role checker for authorization.
    
    Returns:
        Company: The deleted company.
    
    Raises:
        HTTPException: If the company is not found.
    
    Requirements addressed:
    - REST API Service (2. REST API Service/F-002): Implements DELETE endpoint for removing company data
    - Data Storage and Management (1. Data Storage and Management/F-001): Interacts with the database to remove company information
    - Authentication and Authorization (6. SECURITY CONSIDERATIONS/6.1 AUTHENTICATION AND AUTHORIZATION): Implements role-based access control
    """
    db_company = company.get(db, id=company_id)
    if db_company is None:
        raise HTTPException(status_code=404, detail="Company not found")
    return company.remove(db=db, id=company_id)