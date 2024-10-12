"""
Alembic environment configuration script for managing database migrations in the VC firm's financial reporting system.

This script is the entry point for Alembic migrations. It integrates with the project's database configuration and models,
supports both online and offline migration modes, and ensures that all model changes are reflected in the database schema.

Requirements addressed:
1. Database Migration Management (2. SYSTEM ARCHITECTURE/2.2 Component Description/2.2.2 Data Layer)
   - Implements database schema migration management using Alembic for Azure Database for PostgreSQL
2. Data Model Integration (3. SYSTEM COMPONENTS ARCHITECTURE/3.1 COMPONENT DIAGRAMS)
   - Integrates database models for consistent schema management across environments

"""

import logging
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# Import the database configuration and models
from src.database.config import get_database_settings
from src.database.base import Base
from src.database.models.company import Company
from src.database.models.metrics_input import MetricsInput
from src.database.models.reporting_financials import ReportingFinancials
from src.database.models.reporting_metrics import ReportingMetrics

# Alembic Config object, which provides access to the values within the .ini file
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Set up target metadata
target_metadata = Base.metadata

# Load database settings
db_settings = get_database_settings()

def run_migrations_offline() -> None:
    """
    Run migrations in 'offline' mode.

    This configures the context with just a URL and not an Engine,
    though an Engine is acceptable here as well. By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the script output.
    """
    url = db_settings.DATABASE_URL
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """
    Run migrations in 'online' mode.

    In this scenario we need to create an Engine and associate a connection with the context.
    """
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = db_settings.DATABASE_URL
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("alembic.env")

if context.is_offline_mode():
    logger.info("Running migrations offline")
    run_migrations_offline()
else:
    logger.info("Running migrations online")
    run_migrations_online()

# Additional comments for junior developers
"""
This script is crucial for managing database migrations using Alembic. It ensures that your database schema
stays in sync with your SQLAlchemy models as they evolve over time.

Key components:
1. Configuration: The script loads the Alembic configuration and sets up logging.
2. Metadata: It uses the Base.metadata from your SQLAlchemy models to generate migrations.
3. Database Settings: It loads the appropriate database settings based on the current environment.
4. Migration Modes: It supports both online and offline migration modes.

When working with migrations:
1. After making changes to your SQLAlchemy models, generate a new migration using:
   alembic revision --autogenerate -m "Description of changes"

2. Review the generated migration script in the 'versions' directory to ensure it captures your intended changes.

3. Apply the migration to your database using:
   alembic upgrade head

4. To revert a migration, use:
   alembic downgrade -1

Remember to always backup your database before applying migrations in production environments.
"""