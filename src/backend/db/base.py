"""
This file serves as the central point for database-related imports and configurations,
combining the SQLAlchemy base class with all models to ensure they are registered with the ORM.

Requirements addressed:
1. Data Storage (1.2 Scope/Core Functionalities/1. Data Storage):
   Centralizes database configuration and model imports for efficient data management
2. Database Design (3. SYSTEM DESIGN/3.2 DATABASE DESIGN):
   Implements the database schema by combining all models with the SQLAlchemy base

This file is crucial for maintaining a single import point for other parts of the application
that need access to both the Base class and all models, ensuring proper ORM registration.
"""

from typing import List, Type

# Import the Base class from the session module
from src.backend.db.session import Base

# Import all models to ensure they are registered with the ORM
from src.backend.models import Company, MetricsInput, ReportingFinancials, ReportingMetrics

# Define a list of all model classes for easier management and introspection
MODEL_CLASSES: List[Type[Base]] = [Company, MetricsInput, ReportingFinancials, ReportingMetrics]

# Re-export the Base class and all models
__all__ = ["Base", "Company", "MetricsInput", "ReportingFinancials", "ReportingMetrics"]

# The following comment is to explicitly show which models are imported and registered
# with the ORM. This is useful for developers to quickly see which models are available.
"""
Imported and registered models:
- Company
- MetricsInput
- ReportingFinancials
- ReportingMetrics
"""

# Note: By importing the models here and having them inherit from the same Base,
# we ensure that all models are properly registered with SQLAlchemy's ORM.
# This allows for easier querying and relationship management across the application.

def get_all_models() -> List[Type[Base]]:
    """
    Returns a list of all model classes defined in the application.
    
    This function can be useful for operations that need to work with all models,
    such as creating tables, performing database migrations, or generating schemas.
    
    Returns:
        List[Type[Base]]: A list containing all SQLAlchemy model classes.
    """
    return MODEL_CLASSES

# Verify that all imported models are subclasses of Base
for model in MODEL_CLASSES:
    assert issubclass(model, Base), f"{model.__name__} is not a subclass of SQLAlchemy Base"