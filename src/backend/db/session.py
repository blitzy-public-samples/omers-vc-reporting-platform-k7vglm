"""
Database Session Management Module

This module sets up the database session and engine for the backend application,
providing a centralized point for database connections and session management.

Requirements addressed:
1. Data Storage (1.2 Scope/Core Functionalities/1. Data Storage):
   Implements the database connection and session management for efficient data storage and retrieval.
2. Scalability and Performance (2.4 Scalability and Performance Considerations):
   Configures the database engine with performance optimizations and connection pooling.
3. Security (6. SECURITY CONSIDERATIONS):
   Implements secure database connection handling using environment variables.

Dependencies:
- SQLAlchemy (^1.4.0): For database ORM and connection management.
- psycopg2 (^2.9.0): PostgreSQL database adapter for Python.
"""

import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.engine import URL
from sqlalchemy.exc import SQLAlchemyError
from typing import Generator

from src.backend.config import get_config

# Set up logging
logger = logging.getLogger(__name__)

# Retrieve the configuration settings
config = get_config()

# Create the SQLAlchemy engine
try:
    engine = create_engine(
        URL.create(
            drivername="postgresql+psycopg2",
            username=config.DB_USERNAME,
            password=config.DB_PASSWORD,
            host=config.DB_HOST,
            port=config.DB_PORT,
            database=config.DB_NAME,
        ),
        pool_pre_ping=True,  # Enables connection health checks
        pool_recycle=300,  # Recycle connections every 5 minutes
        pool_size=10,  # Set the connection pool size
        max_overflow=20,  # Allow up to 20 connections beyond the pool size
        echo=config.SQL_ECHO,  # SQL query logging based on configuration
    )
    logger.info("Database engine created successfully.")
except SQLAlchemyError as e:
    logger.error(f"Error creating database engine: {str(e)}")
    raise

# Create a sessionmaker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for declarative models
Base = declarative_base()

def get_db() -> Generator:
    """
    Dependency function to get a database session.
    
    Yields:
        Generator[Session, None, None]: Yields a SQLAlchemy Session object.
    
    Usage:
        This function should be used as a dependency in FastAPI route functions
        to ensure proper session management and connection handling.
    
    Example:
        @app.get("/items")
        async def read_items(db: Session = Depends(get_db)):
            items = db.query(Item).all()
            return items
    """
    db = SessionLocal()
    try:
        yield db
    except SQLAlchemyError as e:
        logger.error(f"Database session error: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()

def init_db() -> None:
    """
    Initialize the database by creating all tables defined in the models.

    This function should be called once when setting up the application.
    """
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully.")
    except SQLAlchemyError as e:
        logger.error(f"Error initializing database: {str(e)}")
        raise

# Optionally, you can add a function to dispose of the engine
def dispose_engine() -> None:
    """
    Dispose of the database engine.

    This function should be called when shutting down the application to properly
    close all database connections.
    """
    try:
        engine.dispose()
        logger.info("Database engine disposed successfully.")
    except SQLAlchemyError as e:
        logger.error(f"Error disposing database engine: {str(e)}")
        raise