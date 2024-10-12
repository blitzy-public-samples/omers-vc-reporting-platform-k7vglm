"""
CRUD operations for ReportingMetrics

This module provides CRUD (Create, Read, Update, Delete) operations for the ReportingMetrics model.
It extends the base CRUD functionality with specific operations for reporting metrics.

Requirements addressed:
- Data Storage and Management (1. Data Storage and Management/F-001)
- REST API Service (2. REST API Service/F-002)
- Scalability and Performance (2.4 Scalability and Performance Considerations)

Dependencies:
- SQLAlchemy (^1.4.0): For ORM operations
- Pydantic (^1.8.0): For data validation and settings management
- FastAPI (^0.68.0): For HTTP exception handling
"""

from typing import List, Optional, Dict, Any
from uuid import UUID
from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
import logging

from src.backend.crud.base import CRUDBase
from src.backend.models.reporting_metrics import ReportingMetrics
from src.backend.schemas.reporting_metrics import ReportingMetricsCreate, ReportingMetricsUpdate

# Set up logging
logger = logging.getLogger(__name__)

class CRUDReportingMetrics(CRUDBase[ReportingMetrics, ReportingMetricsCreate, ReportingMetricsUpdate]):
    """
    CRUD operations for ReportingMetrics
    
    This class extends the base CRUD functionality with specific operations for reporting metrics.
    It addresses the following requirements:
    - Data Storage and Management (1. Data Storage and Management/F-001)
    - REST API Service (2. REST API Service/F-002)
    """

    def get_by_company_and_date(
        self, db: Session, company_id: UUID, fiscal_reporting_date: date
    ) -> Optional[ReportingMetrics]:
        """
        Get a ReportingMetrics entry by company ID and fiscal reporting date

        Args:
            db (Session): The database session
            company_id (UUID): The ID of the company
            fiscal_reporting_date (date): The fiscal reporting date

        Returns:
            Optional[ReportingMetrics]: The found ReportingMetrics entry or None

        Raises:
            HTTPException: If there's a database error
        """
        try:
            return db.query(self.model).filter(
                self.model.company_id == company_id,
                self.model.fiscal_reporting_date == fiscal_reporting_date
            ).first()
        except SQLAlchemyError as e:
            logger.error(f"Error retrieving ReportingMetrics for company {company_id} and date {fiscal_reporting_date}: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")

    def get_multi_by_company(
        self, db: Session, company_id: UUID, skip: int = 0, limit: int = 100
    ) -> List[ReportingMetrics]:
        """
        Get multiple ReportingMetrics entries for a specific company

        Args:
            db (Session): The database session
            company_id (UUID): The ID of the company
            skip (int, optional): Number of records to skip. Defaults to 0.
            limit (int, optional): Maximum number of records to return. Defaults to 100.

        Returns:
            List[ReportingMetrics]: A list of ReportingMetrics entries

        Raises:
            HTTPException: If there's a database error
        """
        try:
            return db.query(self.model).filter(
                self.model.company_id == company_id
            ).offset(skip).limit(limit).all()
        except SQLAlchemyError as e:
            logger.error(f"Error retrieving multiple ReportingMetrics for company {company_id}: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")

    def create_with_company(
        self, db: Session, company_id: UUID, obj_in: ReportingMetricsCreate
    ) -> ReportingMetrics:
        """
        Create a new ReportingMetrics entry with company association

        Args:
            db (Session): The database session
            company_id (UUID): The ID of the company
            obj_in (ReportingMetricsCreate): The ReportingMetrics data to create

        Returns:
            ReportingMetrics: The created ReportingMetrics entry

        Raises:
            HTTPException: If there's a database error
        """
        try:
            db_obj = ReportingMetrics(
                company_id=company_id,
                **obj_in.dict()
            )
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            return db_obj
        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"Error creating ReportingMetrics for company {company_id}: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")

    def update_with_company(
        self, db: Session, db_obj: ReportingMetrics, obj_in: ReportingMetricsUpdate
    ) -> ReportingMetrics:
        """
        Update an existing ReportingMetrics entry

        Args:
            db (Session): The database session
            db_obj (ReportingMetrics): The existing ReportingMetrics object to update
            obj_in (ReportingMetricsUpdate): The update data

        Returns:
            ReportingMetrics: The updated ReportingMetrics entry

        Raises:
            HTTPException: If there's a database error
        """
        try:
            update_data = obj_in.dict(exclude_unset=True)
            return super().update(db, db_obj=db_obj, obj_in=update_data)
        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"Error updating ReportingMetrics with id {db_obj.id}: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")

    def get_by_year_and_quarter(
        self, db: Session, company_id: UUID, year: int, quarter: int
    ) -> Optional[ReportingMetrics]:
        """
        Get a ReportingMetrics entry by company ID, year, and quarter

        Args:
            db (Session): The database session
            company_id (UUID): The ID of the company
            year (int): The reporting year
            quarter (int): The reporting quarter

        Returns:
            Optional[ReportingMetrics]: The found ReportingMetrics entry or None

        Raises:
            HTTPException: If there's a database error
        """
        try:
            return db.query(self.model).filter(
                self.model.company_id == company_id,
                self.model.reporting_year == year,
                self.model.reporting_quarter == quarter
            ).first()
        except SQLAlchemyError as e:
            logger.error(f"Error retrieving ReportingMetrics for company {company_id}, year {year}, quarter {quarter}: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")

reporting_metrics = CRUDReportingMetrics(ReportingMetrics)