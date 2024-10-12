"""
Database Scripts Package Initialization

This file serves as the initialization script for the database scripts package.
It imports and exposes the main functions from the init_db and backup_db scripts,
making them easily accessible when the package is imported.

Requirements addressed:
- Database Management Scripts (2. SYSTEM ARCHITECTURE/2.2 Component Description/2.2.2 Data Layer):
  Provides easy access to database initialization and backup scripts.
- Data Backup and Recovery (6. SECURITY CONSIDERATIONS/6.2 DATA SECURITY/6.2.5 Data Backup and Recovery):
  Exposes functions for database backup and cleanup.
"""

from typing import List, Optional
import logging

# Import the database initialization function
from src.database.scripts.init_db import init_db, setup_initial_data

# Import the database backup and cleanup functions
from src.database.scripts.backup_db import create_backup, cleanup_old_backups, main as backup_main

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Export the imported functions
__all__: List[str] = ['init_db', 'setup_initial_data', 'create_backup', 'cleanup_old_backups', 'run_backup']

def run_backup() -> None:
    """
    Wrapper function to run the backup process.
    This function calls the main function from the backup_db module.
    """
    try:
        logger.info("Starting database backup process")
        backup_main()
        logger.info("Database backup process completed successfully")
    except Exception as e:
        logger.error(f"Error during database backup process: {str(e)}")

# Verify that all imported functions exist
if not all(callable(globals().get(func)) for func in __all__):
    missing_funcs = [func for func in __all__ if not callable(globals().get(func))]
    raise ImportError(f"The following functions are missing or not callable: {', '.join(missing_funcs)}")

logger.info("Database scripts package initialized successfully")