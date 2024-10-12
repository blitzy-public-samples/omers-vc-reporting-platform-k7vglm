"""
Alembic migration environment configuration file.

This module sets up the environment for database migrations using Alembic.
It configures logging, sets up the database connection, and defines functions
for running migrations in both online and offline modes.

Requirements addressed:
1. Data Storage (1.2 Scope/Core Functionalities/1. Data Storage):
   Configures database migrations for efficient schema management.
2. Database Design (3. SYSTEM DESIGN/3.2 DATABASE DESIGN):
   Utilizes SQLAlchemy metadata for automatic migration generation.
"""

import logging
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# Import the Base and get_config function
from src.backend.db.base import Base
from src.backend.config import get_config

# Alembic Config object, which provides access to values within the .ini file
config = context.config

# Interpret the config file for logging
fileConfig(config.config_file_name)
logger = logging.getLogger('alembic.env')

# Add your model's MetaData object here for 'autogenerate' support
target_metadata = Base.metadata

# Get the database URL from the application configuration
app_config = get_config()
config.set_main_option('sqlalchemy.url', app_config.DATABASE_URL)

def run_migrations_offline() -> None:
    """
    Run migrations in 'offline' mode.

    This configures the context with just a URL and not an Engine,
    though an Engine is acceptable here as well. By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the script output.
    """
    url = config.get_main_option("sqlalchemy.url")
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
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
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

if context.is_offline_mode():
    logger.info('Running migrations offline')
    run_migrations_offline()
else:
    logger.info('Running migrations online')
    run_migrations_online()

# Ensure all models are imported and registered with the ORM
from src.backend.db.base import get_all_models
get_all_models()