from typing import Optional, List
from uuid import UUID
from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
import logging

from src.backend.crud.base import CRUDBase
from src.backend.models.metrics_input import MetricsInput
from src.backend.schemas.metrics_input import MetricsInputCreate, MetricsInputUpdate

# Set up logging
logger = logging.getLogger(__name__)

class CRUDMetricsInput(CRUDBase[MetricsInput, MetricsInputCreate, MetricsInputUpdate]):
    """
    CRUD operations for MetricsInput model
    
    This class extends the base CRUD functionality for specific operations related to metrics input data.
    It implements the requirements specified in:
    - Data Storage and Management (1. Data Storage and Management/F-001)
    - REST API Service (2. REST API Service/F-002)
    """

    def get_by_company_and_date(
        self, db: Session, company_id: UUID, fiscal_reporting_date: date
    ) -> Optional[MetricsInput]:
        """
        Get a metrics input record by company ID and fiscal reporting date

        Args:
            db (Session): The database session
            company_id (UUID): The ID of the company
            fiscal_reporting_date (date): The fiscal reporting date

        Returns:
            Optional[MetricsInput]: The found record or None if not found

        Raises:
            HTTPException: If there's a database error
        """
        try:
            return db.query(self.model).filter(
                self.model.company_id == company_id,
                self.model.fiscal_reporting_date == fiscal_reporting_date
            ).first()
        except SQLAlchemyError as e:
            logger.error(f"Error retrieving metrics input for company {company_id} and date {fiscal_reporting_date}: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")

    def get_latest_by_company(self, db: Session, company_id: UUID) -> Optional[MetricsInput]:
        """
        Get the latest metrics input record for a company

        Args:
            db (Session): The database session
            company_id (UUID): The ID of the company

        Returns:
            Optional[MetricsInput]: The latest record or None if not found

        Raises:
            HTTPException: If there's a database error
        """
        try:
            return db.query(self.model).filter(
                self.model.company_id == company_id
            ).order_by(self.model.fiscal_reporting_date.desc()).first()
        except SQLAlchemyError as e:
            logger.error(f"Error retrieving latest metrics input for company {company_id}: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")

    def create_with_company(
        self, db: Session, obj_in: MetricsInputCreate, company_id: UUID
    ) -> MetricsInput:
        """
        Create a new metrics input record with company association

        Args:
            db (Session): The database session
            obj_in (MetricsInputCreate): The input data for creating a new record
            company_id (UUID): The ID of the company to associate with the record

        Returns:
            MetricsInput: The created record

        Raises:
            HTTPException: If there's a database error
        """
        try:
            db_obj = MetricsInput(
                company_id=company_id,
                **obj_in.dict()
            )
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            return db_obj
        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"Error creating metrics input for company {company_id}: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")

    def get_by_company(
        self, db: Session, company_id: UUID, skip: int = 0, limit: int = 100
    ) -> List[MetricsInput]:
        """
        Get all metrics input records for a specific company

        Args:
            db (Session): The database session
            company_id (UUID): The ID of the company
            skip (int): Number of records to skip (for pagination)
            limit (int): Maximum number of records to return (for pagination)

        Returns:
            List[MetricsInput]: List of metrics input records for the company

        Raises:
            HTTPException: If there's a database error
        """
        try:
            return db.query(self.model).filter(
                self.model.company_id == company_id
            ).order_by(self.model.fiscal_reporting_date.desc()).offset(skip).limit(limit).all()
        except SQLAlchemyError as e:
            logger.error(f"Error retrieving metrics inputs for company {company_id}: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")

# Create a global instance of CRUDMetricsInput
metrics_input = CRUDMetricsInput(MetricsInput)