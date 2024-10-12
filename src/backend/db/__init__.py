"""
Database Package Initialization

This file serves as the initialization point for the database package, importing and exposing key
database-related components for use throughout the application.

Requirements addressed:
- Data Storage (1.2 Scope/Core Functionalities/1. Data Storage):
  Centralizes database-related imports and configurations for efficient data management.
- Database Design (3. SYSTEM DESIGN/3.2 DATABASE DESIGN):
  Exposes the Base class and all models to ensure proper ORM registration.

This module acts as a central point for importing and exposing key database-related components.
It simplifies imports in other parts of the application by providing a single import point for
essential database objects and functions.
"""

from typing import List, Type

from src.backend.db.base import Base, get_all_models
from src.backend.db.session import engine, SessionLocal, get_db, init_db, dispose_engine

# Expose key components at the package level
__all__ = [
    "Base",
    "engine",
    "SessionLocal",
    "get_db",
    "init_db",
    "dispose_engine",
    "get_all_models"
]

# SQLAlchemy declarative base instance with all models
Base = Base

# SQLAlchemy engine instance
engine = engine

# SQLAlchemy sessionmaker instance
SessionLocal = SessionLocal

# Database session dependency function
get_db = get_db

# Database initialization function
init_db = init_db

# Engine disposal function
dispose_engine = dispose_engine

# Function to get all model classes
get_all_models = get_all_models

def get_model_names() -> List[str]:
    """
    Returns a list of names of all model classes defined in the application.
    
    This function can be useful for introspection and logging purposes.
    
    Returns:
        List[str]: A list containing the names of all SQLAlchemy model classes.
    """
    return [model.__name__ for model in get_all_models()]

# Verify that all required database components are properly imported and exposed
assert all(component in globals() for component in __all__), "Missing required database components"

# Log the successful initialization of the database package
import logging
logger = logging.getLogger(__name__)
logger.info(f"Database package initialized with models: {', '.join(get_model_names())}")