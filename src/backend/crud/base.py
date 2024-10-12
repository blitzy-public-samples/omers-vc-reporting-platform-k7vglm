"""
Base CRUD Operations Module

This module provides a generic CRUD (Create, Read, Update, Delete) class that can be used
as a base for specific model CRUD operations throughout the application.

Requirements addressed:
- Data Storage and Management (1. Data Storage and Management/F-001)
- REST API Service (2. REST API Service/F-002)
- Scalability and Performance (2.4 Scalability and Performance Considerations)

Dependencies:
- SQLAlchemy (^1.4.0): For ORM operations
- Pydantic (^1.8.0): For data validation and settings management
"""

from typing import Generic, Type, TypeVar, Any, Optional, List, Union, Dict
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from pydantic import BaseModel
from fastapi import HTTPException
import logging

from src.backend.db.base import Base

# Set up logging
logger = logging.getLogger(__name__)

# Define generic type variables
ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
    Generic CRUD object with default methods to Create, Read, Update, Delete (CRUD).
    """

    def __init__(self, model: Type[ModelType]):
        """
        Initialize the CRUD object with the given model.
        
        Args:
            model (Type[ModelType]): The SQLAlchemy model class
        """
        self.model = model

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        """
        Get a single record by ID.
        
        Args:
            db (Session): The database session
            id (Any): The ID of the record to retrieve
        
        Returns:
            Optional[ModelType]: The found record or None if not found
        """
        try:
            return db.query(self.model).filter(self.model.id == id).first()
        except SQLAlchemyError as e:
            logger.error(f"Error retrieving {self.model.__name__} with id {id}: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")

    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[ModelType]:
        """
        Get multiple records with optional skip and limit.
        
        Args:
            db (Session): The database session
            skip (int): Number of records to skip (default: 0)
            limit (int): Maximum number of records to return (default: 100)
        
        Returns:
            List[ModelType]: A list of found records
        """
        try:
            return db.query(self.model).offset(skip).limit(limit).all()
        except SQLAlchemyError as e:
            logger.error(f"Error retrieving multiple {self.model.__name__} records: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        """
        Create a new record.
        
        Args:
            db (Session): The database session
            obj_in (CreateSchemaType): The input data for creating the record
        
        Returns:
            ModelType: The created record
        """
        try:
            obj_in_data = obj_in.dict()
            db_obj = self.model(**obj_in_data)
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            return db_obj
        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"Error creating {self.model.__name__}: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")

    def update(self, db: Session, *, db_obj: ModelType, obj_in: Union[UpdateSchemaType, Dict[str, Any]]) -> ModelType:
        """
        Update an existing record.
        
        Args:
            db (Session): The database session
            db_obj (ModelType): The existing database object
            obj_in (Union[UpdateSchemaType, Dict[str, Any]]): The input data for updating the record
        
        Returns:
            ModelType: The updated record
        """
        try:
            obj_data = db_obj.__dict__
            if isinstance(obj_in, dict):
                update_data = obj_in
            else:
                update_data = obj_in.dict(exclude_unset=True)
            for field in obj_data:
                if field in update_data:
                    setattr(db_obj, field, update_data[field])
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            return db_obj
        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"Error updating {self.model.__name__} with id {db_obj.id}: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")

    def remove(self, db: Session, *, id: Any) -> Optional[ModelType]:
        """
        Remove a record.
        
        Args:
            db (Session): The database session
            id (Any): The ID of the record to remove
        
        Returns:
            Optional[ModelType]: The removed record or None if not found
        """
        try:
            obj = db.query(self.model).get(id)
            if obj:
                db.delete(obj)
                db.commit()
            return obj
        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"Error removing {self.model.__name__} with id {id}: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")

# Import this at the end to avoid circular imports
from src.backend.db.session import SessionLocal