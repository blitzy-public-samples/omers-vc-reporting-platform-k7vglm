from typing import List, Optional
from uuid import UUID
from datetime import date, datetime
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
import logging

from src.backend.crud.base import CRUDBase
from src.backend.models.reporting_financials import ReportingFinancials
from src.backend.schemas.reporting_financials import ReportingFinancialsCreate, ReportingFinancialsUpdate

# Set up logging
logger = logging.getLogger(__name__)

class CRUDReportingFinancials(CRUDBase[ReportingFinancials, ReportingFinancialsCreate, ReportingFinancialsUpdate]):
    def get_by_company_and_date(
        self, db: Session, company_id: UUID, fiscal_reporting_date: date
    ) -> Optional[ReportingFinancials]:
        """
        Get a single reporting financials record by company ID and fiscal reporting date.

        Args:
            db (Session): The database session.
            company_id (UUID): The ID of the company.
            fiscal_reporting_date (date): The fiscal reporting date.

        Returns:
            Optional[ReportingFinancials]: The found record or None if not found.

        Requirements addressed:
            - Data Storage and Management (1. Data Storage and Management/F-001)
            - REST API Service (2. REST API Service/F-002)
        """
        try:
            return db.query(self.model).filter(
                self.model.company_id == company_id,
                self.model.fiscal_reporting_date == fiscal_reporting_date
            ).first()
        except SQLAlchemyError as e:
            logger.error(f"Error retrieving ReportingFinancials for company {company_id} and date {fiscal_reporting_date}: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")

    def get_multi_by_company(
        self, db: Session, company_id: UUID, skip: int = 0, limit: int = 100
    ) -> List[ReportingFinancials]:
        """
        Get multiple reporting financials records for a specific company.

        Args:
            db (Session): The database session.
            company_id (UUID): The ID of the company.
            skip (int, optional): Number of records to skip. Defaults to 0.
            limit (int, optional): Maximum number of records to return. Defaults to 100.

        Returns:
            List[ReportingFinancials]: A list of found records.

        Requirements addressed:
            - Data Storage and Management (1. Data Storage and Management/F-001)
            - REST API Service (2. REST API Service/F-002)
        """
        try:
            return db.query(self.model).filter(self.model.company_id == company_id).offset(skip).limit(limit).all()
        except SQLAlchemyError as e:
            logger.error(f"Error retrieving multiple ReportingFinancials for company {company_id}: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")

    def create_with_company(
        self, db: Session, obj_in: ReportingFinancialsCreate, company_id: UUID
    ) -> ReportingFinancials:
        """
        Create a new reporting financials record with company association.

        Args:
            db (Session): The database session.
            obj_in (ReportingFinancialsCreate): The input data for creating the record.
            company_id (UUID): The ID of the company to associate with the record.

        Returns:
            ReportingFinancials: The created record.

        Requirements addressed:
            - Data Storage and Management (1. Data Storage and Management/F-001)
            - REST API Service (2. REST API Service/F-002)
            - Multi-Currency Support (4. Multi-Currency Support/F-004)
        """
        try:
            db_obj = ReportingFinancials(
                company_id=company_id,
                currency=obj_in.currency,
                exchange_rate_used=obj_in.exchange_rate_used,
                total_revenue=obj_in.total_revenue,
                recurring_revenue=obj_in.recurring_revenue,
                gross_profit=obj_in.gross_profit,
                sales_marketing_expense=obj_in.sales_marketing_expense,
                total_operating_expense=obj_in.total_operating_expense,
                ebitda=obj_in.ebitda,
                net_income=obj_in.net_income,
                cash_burn=obj_in.cash_burn,
                cash_balance=obj_in.cash_balance,
                debt_outstanding=obj_in.debt_outstanding,
                fiscal_reporting_date=obj_in.fiscal_reporting_date,
                fiscal_reporting_quarter=obj_in.fiscal_reporting_quarter,
                reporting_year=obj_in.reporting_year,
                reporting_quarter=obj_in.reporting_quarter,
                created_by=obj_in.created_by
            )
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            return db_obj
        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"Error creating ReportingFinancials for company {company_id}: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")

    def update_financials(
        self, db: Session, db_obj: ReportingFinancials, obj_in: ReportingFinancialsUpdate
    ) -> ReportingFinancials:
        """
        Update an existing reporting financials record.

        Args:
            db (Session): The database session.
            db_obj (ReportingFinancials): The existing database object to update.
            obj_in (ReportingFinancialsUpdate): The input data for updating the record.

        Returns:
            ReportingFinancials: The updated record.

        Requirements addressed:
            - Data Storage and Management (1. Data Storage and Management/F-001)
            - REST API Service (2. REST API Service/F-002)
            - Multi-Currency Support (4. Multi-Currency Support/F-004)
        """
        try:
            update_data = obj_in.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_obj, field, value)
            db_obj.last_update_date = datetime.utcnow()
            db_obj.last_updated_by = obj_in.last_updated_by
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            return db_obj
        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"Error updating ReportingFinancials with id {db_obj.id}: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")

reporting_financials = CRUDReportingFinancials(ReportingFinancials)