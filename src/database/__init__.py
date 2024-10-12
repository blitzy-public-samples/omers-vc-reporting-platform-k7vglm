"""
This file serves as the main entry point for the database package, providing easy access to all database-related components,
including models, schemas, utilities, and core database functionality.

Requirements addressed:
1. Centralized Database Access (3. SYSTEM DESIGN/3.2 DATABASE DESIGN):
   Provides a single import point for all database-related components, simplifying usage across the application.
2. Data Storage and Management (1. Introduction/1.2 Scope/Core Functionalities):
   Facilitates the implementation of a PostgreSQL database to store quarterly reporting metrics from portfolio companies.
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

# Import database utility functions
from src.database.utils import (
    create_indexes,
    drop_indexes,
    check_indexes,
    create_index_if_not_exists,
    optimize_indexes,
    monitor_index_usage,
    create_sharded_tables,
    get_shard_for_company,
    insert_into_shard,
    query_sharded_table,
    get_all_shards,
    query_all_shards,
)

# Import database configuration
from src.database.config import get_database_settings, database_settings

# Import database session components
from src.database.session import (
    engine,
    SessionLocal,
    Base,
    get_db,
    init_db,
    AsyncDatabaseSession,
    async_db_session,
)

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
    # Database utility functions
    "create_indexes",
    "drop_indexes",
    "check_indexes",
    "create_index_if_not_exists",
    "optimize_indexes",
    "monitor_index_usage",
    "create_sharded_tables",
    "get_shard_for_company",
    "insert_into_shard",
    "query_sharded_table",
    "get_all_shards",
    "query_all_shards",
    # Database configuration
    "get_database_settings",
    "database_settings",
    # Database session components
    "engine",
    "SessionLocal",
    "Base",
    "get_db",
    "init_db",
    "AsyncDatabaseSession",
    "async_db_session",
]

# Version information
__version__ = "1.0.0"

"""
Usage:
This module provides a centralized import point for all database-related components.
By importing from this module, other parts of the application can easily access the required
database models, schemas, utilities, and session management functions without needing to know
the exact file structure.

Example:
from src.database import Company, CompanyCreate, create_indexes, get_db, init_db

def setup_database():
    init_db()
    create_indexes(get_db())

def create_company(company_data: CompanyCreate) -> Company:
    # Implementation here

Notes:
- Ensure that all new database-related components are added to this file when created.
- Keep the imports organized by component type (models, schemas, utils, etc.) for clarity.
- Update the __version__ when making changes to the database components or this file.
- Consider adding type hints in other parts of the application that use these components.

Dependencies:
- SQLAlchemy
- Pydantic
- asyncpg (for asynchronous database operations)
"""