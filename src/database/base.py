"""
This module serves as the central point for importing and re-exporting database models, schemas,
and core database components for the financial reporting metrics backend system.

Requirements addressed:
1. Centralized Database Access (3. SYSTEM DESIGN/3.2 DATABASE DESIGN):
   Provides a single import point for all database-related components
2. Data Storage and Management (1. Introduction/1.2 Scope/Core Functionalities):
   Implements a PostgreSQL database to store quarterly reporting metrics from portfolio companies

Version: 1.1.0
"""

# Import ORM models
from src.database.models import Company, MetricsInput, ReportingFinancials, ReportingMetrics

# Import Pydantic schemas
from src.database.schemas import (
    Company as CompanySchema,
    CompanyCreate,
    CompanyUpdate,
    CompanyInDB,
    CompanyBase,
    CompanyInDBBase,
    MetricsInput as MetricsInputSchema,
    MetricsInputCreate,
    MetricsInputUpdate,
    MetricsInputInDB,
    MetricsInputBase,
    ReportingFinancials as ReportingFinancialsSchema,
    ReportingFinancialsCreate,
    ReportingFinancialsUpdate,
    ReportingFinancialsInDB,
    ReportingFinancialsBase,
    ReportingMetrics as ReportingMetricsSchema,
    ReportingMetricsCreate,
    ReportingMetricsUpdate,
    ReportingMetricsInDB,
    ReportingMetricsBase,
)

# Import database configuration function
from src.database.config import get_database_settings, database_settings

# Import database session and engine components
from src.database.session import (
    engine,
    SessionLocal,
    Base,
    get_db,
    init_db,
    AsyncDatabaseSession,
    async_db_session,
)

# Re-export all imported components
__all__ = [
    # ORM models
    "Company",
    "MetricsInput",
    "ReportingFinancials",
    "ReportingMetrics",
    # Pydantic schemas
    "CompanySchema",
    "CompanyCreate",
    "CompanyUpdate",
    "CompanyInDB",
    "CompanyBase",
    "CompanyInDBBase",
    "MetricsInputSchema",
    "MetricsInputCreate",
    "MetricsInputUpdate",
    "MetricsInputInDB",
    "MetricsInputBase",
    "ReportingFinancialsSchema",
    "ReportingFinancialsCreate",
    "ReportingFinancialsUpdate",
    "ReportingFinancialsInDB",
    "ReportingFinancialsBase",
    "ReportingMetricsSchema",
    "ReportingMetricsCreate",
    "ReportingMetricsUpdate",
    "ReportingMetricsInDB",
    "ReportingMetricsBase",
    # Database configuration
    "get_database_settings",
    "database_settings",
    # Database session and engine components
    "engine",
    "SessionLocal",
    "Base",
    "get_db",
    "init_db",
    "AsyncDatabaseSession",
    "async_db_session",
]

# Version information
__version__ = "1.1.0"

# Additional comments for developers
"""
This file serves as the main entry point for all database-related imports in the application.
By centralizing these imports, we achieve better organization and make it easier to manage
database dependencies throughout the project.

Key components:
1. ORM models: These represent the database tables and are used for interacting with the database.
2. Pydantic schemas: These are used for data validation and serialization/deserialization.
3. Database configuration: The get_database_settings function provides environment-specific database settings.
4. Database session and engine: These components manage database connections and sessions.

When working with database operations in other parts of the application, you should import
the necessary components from this file rather than from their individual modules. This
approach helps maintain consistency and makes it easier to manage changes to the database structure.

Example usage:
from src.database.base import Company, CompanySchema, get_db, async_db_session

def create_company(db: Session, company: CompanySchema):
    db_company = Company(**company.dict())
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    return db_company

async def get_company(company_id: int):
    async with async_db_session.get_db() as db:
        return await db.get(Company, company_id)

Changes in version 1.1.0:
- Added import and export of CompanyBase and CompanyInDBBase schemas
- Added import and export of MetricsInputBase, ReportingFinancialsBase, and ReportingMetricsBase schemas
- Included database_settings in imports and exports
- Added init_db, AsyncDatabaseSession, and async_db_session to imports and exports
- Updated example usage to include an async function using async_db_session

Note: When adding new models, schemas, or database-related components, make sure to update
this file to include the new imports and add them to the __all__ list for easy access.
"""