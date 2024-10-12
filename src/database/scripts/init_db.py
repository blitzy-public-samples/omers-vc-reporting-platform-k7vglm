import logging
import click
from sqlalchemy.exc import SQLAlchemyError
from src.database.base import Base, engine, get_db, Company, MetricsInput, ReportingFinancials, ReportingMetrics
from src.database.config import get_database_settings

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@click.command()
@click.option('--drop-existing', is_flag=True, help='Drop existing tables before creating new ones')
def init_db(drop_existing):
    """
    Initializes the database by creating all tables.

    This function addresses the following requirements:
    - Database Initialization (2. SYSTEM ARCHITECTURE/2.2 Component Description/2.2.2 Data Layer)
    - Data Model Implementation (3. SYSTEM COMPONENTS ARCHITECTURE/3.1 COMPONENT DIAGRAMS)

    Args:
        drop_existing (bool): If True, drop existing tables before creating new ones.
    """
    logger.info("Starting database initialization")

    try:
        if drop_existing:
            logger.info("Dropping existing tables")
            Base.metadata.drop_all(bind=engine)

        logger.info("Creating database tables")
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")

        # Call setup_initial_data function to populate initial data if required
        setup_initial_data()

        logger.info("Database initialization completed successfully")
    except SQLAlchemyError as e:
        logger.error(f"An error occurred during database initialization: {str(e)}")
        raise

def setup_initial_data():
    """
    Sets up initial data in the database if required.

    This function can be used to populate the database with any necessary initial data
    for the Company, MetricsInput, ReportingFinancials, and ReportingMetrics tables.
    """
    logger.info("Setting up initial data")

    try:
        db = next(get_db())

        # Check if any initial data needs to be inserted
        if db.query(Company).count() == 0:
            # Insert initial data for Company table
            # Example:
            # initial_company = Company(name="Example Company", ...)
            # db.add(initial_company)
            pass

        # Similar checks and insertions can be done for other tables if needed

        db.commit()
        logger.info("Initial data setup completed")
    except SQLAlchemyError as e:
        logger.error(f"An error occurred during initial data setup: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    # Load database settings
    db_settings = get_database_settings()
    
    # Log database configuration (excluding sensitive information)
    logger.info(f"Database configuration: MAX_CONNECTIONS={db_settings.DATABASE_MAX_CONNECTIONS}, "
                f"POOL_SIZE={db_settings.DATABASE_POOL_SIZE}, "
                f"POOL_RECYCLE={db_settings.DATABASE_POOL_RECYCLE}, "
                f"ECHO_SQL={db_settings.DATABASE_ECHO_SQL}")

    init_db()