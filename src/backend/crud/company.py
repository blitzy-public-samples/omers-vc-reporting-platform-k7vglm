"""
CRUD operations for Company model.

This module provides CRUD (Create, Read, Update, Delete) operations for the Company model.
It extends the base CRUD operations provided by CRUDBase and adds company-specific operations.

Requirements addressed:
- Data Storage and Management (1. Data Storage and Management/F-001)
- REST API Service (2. REST API Service/F-002)
- Scalability and Performance (2.4 Scalability and Performance Considerations)

Dependencies:
- SQLAlchemy (^1.4.0): For ORM operations
- Pydantic (^1.8.0): For data validation and settings management
- FastAPI (^0.68.0): For HTTP exception handling
"""

from typing import Optional, List
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
import logging

from src.backend.crud.base import CRUDBase
from src.backend.models.company import Company
from src.backend.schemas.company import CompanyCreate, CompanyUpdate

# Set up logging
logger = logging.getLogger(__name__)

class CRUDCompany(CRUDBase[Company, CompanyCreate, CompanyUpdate]):
    def get_by_name(self, db: Session, name: str) -> Optional[Company]:
        """
        Get a company by its name.
        
        Args:
            db (Session): The database session.
            name (str): The name of the company to retrieve.
        
        Returns:
            Optional[Company]: The found company or None if not found.
        
        Raises:
            HTTPException: If there's a database error.
        """
        try:
            return db.query(self.model).filter(self.model.name == name).first()
        except SQLAlchemyError as e:
            logger.error(f"Error retrieving company by name '{name}': {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")

    def create(self, db: Session, obj_in: CompanyCreate) -> Company:
        """
        Create a new company.
        
        Args:
            db (Session): The database session.
            obj_in (CompanyCreate): The company data to create.
        
        Returns:
            Company: The created company.
        
        Raises:
            HTTPException: If there's a database error.
        """
        try:
            db_obj = Company(
                name=obj_in.name,
                reporting_status=obj_in.reporting_status,
                reporting_currency=obj_in.reporting_currency,
                fund=obj_in.fund,
                location_country=obj_in.location_country,
                customer_type=obj_in.customer_type,
                revenue_type=obj_in.revenue_type,
                equity_raised=obj_in.equity_raised,
                post_money_valuation=obj_in.post_money_valuation,
                year_end_date=obj_in.year_end_date,
                created_by=obj_in.created_by,  # Assuming this is provided in the CompanyCreate schema
            )
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            return db_obj
        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"Error creating company: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")

    def update(self, db: Session, db_obj: Company, obj_in: CompanyUpdate) -> Company:
        """
        Update an existing company.
        
        Args:
            db (Session): The database session.
            db_obj (Company): The existing company object to update.
            obj_in (CompanyUpdate): The company data to update.
        
        Returns:
            Company: The updated company.
        
        Raises:
            HTTPException: If there's a database error.
        """
        try:
            update_data = obj_in.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_obj, field, value)
            db_obj.last_updated_by = obj_in.last_updated_by  # Assuming this is provided in the CompanyUpdate schema
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            return db_obj
        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"Error updating company with id {db_obj.id}: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")

    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[Company]:
        """
        Get multiple companies with pagination.
        
        Args:
            db (Session): The database session.
            skip (int): Number of records to skip (for pagination).
            limit (int): Maximum number of records to return.
        
        Returns:
            List[Company]: A list of companies.
        
        Raises:
            HTTPException: If there's a database error.
        """
        try:
            return super().get_multi(db, skip=skip, limit=limit)
        except SQLAlchemyError as e:
            logger.error(f"Error retrieving multiple companies: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")

    def remove(self, db: Session, *, id: UUID) -> Company:
        """
        Remove a company by ID.
        
        Args:
            db (Session): The database session.
            id (UUID): The ID of the company to remove.
        
        Returns:
            Company: The removed company.
        
        Raises:
            HTTPException: If the company is not found or if there's a database error.
        """
        try:
            company = super().remove(db, id=id)
            if not company:
                raise HTTPException(status_code=404, detail="Company not found")
            return company
        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"Error removing company with id {id}: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")

# Instantiate the CRUDCompany class
company = CRUDCompany(Company)