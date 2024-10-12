"""
This file sets up the database session and connection management for the financial reporting metrics backend system.

Requirements addressed:
1. Database Connection Management (2. SYSTEM ARCHITECTURE/2.2 Component Description/2.2.2 Data Layer)
   - Implements database connection management using SQLAlchemy for Azure Database for PostgreSQL
2. Scalability and Performance (2. SYSTEM ARCHITECTURE/2.4 Scalability and Performance Considerations)
   - Configures database connection pooling and session management for optimal performance
"""

from contextlib import asynccontextmanager
from typing import AsyncGenerator, Generator

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from src.database.config import get_database_settings

# Get database settings based on the current environment
db_settings = get_database_settings()

# Create SQLAlchemy engine with connection pooling configuration
engine = create_engine(
    db_settings.DATABASE_URL,
    pool_size=db_settings.DATABASE_POOL_SIZE,
    max_overflow=db_settings.DATABASE_MAX_CONNECTIONS - db_settings.DATABASE_POOL_SIZE,
    pool_recycle=db_settings.DATABASE_POOL_RECYCLE,
    echo=db_settings.DATABASE_ECHO_SQL
)

# Create a sessionmaker factory for creating database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for declarative models
Base = declarative_base()

def get_db() -> Generator[SessionLocal, None, None]:
    """
    Dependency function to get a database session.

    Yields:
        Generator[SessionLocal, None, None]: Yields a database session

    Usage:
        This function should be used as a dependency in FastAPI route functions
        to ensure proper handling of database sessions.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db() -> None:
    """
    Initialize the database by creating all tables.

    This function should be called when setting up the application to ensure
    all database tables are created based on the defined models.
    """
    # Import all models here to ensure they are registered with the Base class
    from src.database.models import company, metrics_input, reporting_financials, reporting_metrics

    Base.metadata.create_all(bind=engine)

class AsyncDatabaseSession:
    """
    Asynchronous database session class for handling async database operations.
    """

    def __init__(self):
        self.engine = create_async_engine(
            db_settings.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://"),
            pool_size=db_settings.DATABASE_POOL_SIZE,
            max_overflow=db_settings.DATABASE_MAX_CONNECTIONS - db_settings.DATABASE_POOL_SIZE,
            pool_recycle=db_settings.DATABASE_POOL_RECYCLE,
            echo=db_settings.DATABASE_ECHO_SQL
        )
        self.SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.engine,
            class_=AsyncSession
        )

    @asynccontextmanager
    async def get_db(self) -> AsyncGenerator[AsyncSession, None]:
        """
        Asynchronous context manager for database sessions.

        Yields:
            AsyncGenerator[AsyncSession, None]: Yields an asynchronous database session

        Usage:
            This context manager should be used in async route functions to ensure
            proper handling of asynchronous database sessions.
        """
        async with self.SessionLocal() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()

# Create an instance of AsyncDatabaseSession for use in async operations
async_db_session = AsyncDatabaseSession()