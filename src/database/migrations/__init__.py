"""
This file serves as the initialization point for the database migrations package,
providing a centralized location for migration-related imports and configurations.

Requirements addressed:
1. Database Migration Management
   Location: 2. SYSTEM ARCHITECTURE/2.2 Component Description/2.2.2 Data Layer
   Description: Initializes the migration environment for managing database schema changes in Azure Database for PostgreSQL

Usage:
- This file is automatically executed when the migrations package is imported
- It sets up the necessary components for Alembic to manage database migrations
- Developers should not need to modify this file directly

Notes:
- Ensure that all model files are imported in src.database.base to include them in migrations
- The alembic.ini file in the parent directory configures the migration environment
- Use 'alembic revision --autogenerate' to generate new migration scripts
- Run 'alembic upgrade head' to apply all pending migrations to the database
"""

from src.database.migrations.env import run_migrations_offline, run_migrations_online
from src.database.base import Base
from src.database.config import get_database_settings

# Alembic version: ^1.7.0
# SQLAlchemy version: ^1.4.0

# Importing Base ensures that all models are included in the migrations
# Importing get_database_settings allows access to database configuration in the migration environment

# The actual migration logic is implemented in the env.py file
# This __init__.py file serves as a convenient import point for migration-related components

__all__ = [
    "run_migrations_offline",
    "run_migrations_online",
    "Base",
    "get_database_settings",
]

# Version information
__version__ = "1.0.0"

# Additional comments for junior developers
"""
This file is crucial for setting up the database migration environment in your project.
It imports and re-exports key components needed for Alembic to manage database migrations.

Key components:
1. run_migrations_offline and run_migrations_online: These functions from env.py handle the actual migration process.
2. Base: The declarative base from SQLAlchemy, which includes all your model definitions.
3. get_database_settings: A function to retrieve the appropriate database settings based on the current environment.

When working with migrations:
1. Ensure all your models are imported in src.database.base to be included in migrations.
2. After making changes to your models, generate a new migration using:
   alembic revision --autogenerate -m "Description of changes"
3. Review the generated migration script in the 'versions' directory.
4. Apply the migration to your database using:
   alembic upgrade head

Remember to always backup your database before applying migrations in production environments.
"""