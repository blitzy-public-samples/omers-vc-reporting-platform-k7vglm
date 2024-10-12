"""
This module implements database sharding functionality for the financial reporting metrics backend system.

Requirements addressed:
1. Database Sharding (2. SYSTEM ARCHITECTURE/2.4 Scalability and Performance Considerations)
   Implements database sharding for the Metrics Input and Quarterly Reporting tables to improve query performance and system scalability.
2. Scalability (3. SYSTEM DESIGN/3.2 DATABASE DESIGN)
   Supports horizontal scaling of the database through sharding.

"""

from typing import List, Type, Any
from sqlalchemy import Column, String, inspect
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base
from src.database.config import get_database_settings
from src.database.session import engine, Base
from src.database.models import MetricsInput, ReportingFinancials, ReportingMetrics

# SQLAlchemy version: ^1.4.0
# Pydantic version: ^1.8.0

# Global variable for the shard key column
SHARD_KEY_COLUMN = "company_id"

# Get database settings
db_settings = get_database_settings()

def create_sharded_tables(Base: Type[Base], engine: Any) -> None:
    """
    Creates sharded tables for MetricsInput, ReportingFinancials, and ReportingMetrics.

    Args:
        Base (Type[Base]): SQLAlchemy declarative base
        engine (Any): SQLAlchemy engine

    Returns:
        None
    """
    num_shards = db_settings.DATABASE_SHARDS

    for model in [MetricsInput, ReportingFinancials, ReportingMetrics]:
        for shard in range(num_shards):
            table_name = f"{model.__tablename__}_shard_{shard}"
            shard_table = type(
                f"{model.__name__}Shard{shard}",
                (Base,),
                {
                    "__tablename__": table_name,
                    **{col.name: col.copy() for col in inspect(model).columns},
                },
            )
            shard_table.__table__.create(bind=engine, checkfirst=True)

def get_shard_for_company(company_id: str) -> int:
    """
    Determines the appropriate shard for a given company ID.

    Args:
        company_id (str): The company ID

    Returns:
        int: The shard number for the given company ID
    """
    num_shards = db_settings.DATABASE_SHARDS
    return hash(company_id) % num_shards

def insert_into_shard(instance: Base, session: Session) -> None:
    """
    Inserts data into the appropriate shard based on the company ID.

    Args:
        instance (Base): SQLAlchemy model instance to be inserted
        session (Session): SQLAlchemy session

    Returns:
        None

    Raises:
        AttributeError: If the instance does not have the shard key column
    """
    if not hasattr(instance, SHARD_KEY_COLUMN):
        raise AttributeError(f"Instance does not have the shard key column: {SHARD_KEY_COLUMN}")

    company_id = getattr(instance, SHARD_KEY_COLUMN)
    shard_number = get_shard_for_company(company_id)
    table_name = f"{instance.__class__.__tablename__}_shard_{shard_number}"
    shard_table = type(
        f"{instance.__class__.__name__}Shard{shard_number}",
        (Base,),
        {
            "__tablename__": table_name,
            **{col.name: col.copy() for col in inspect(instance.__class__).columns},
        },
    )
    shard_instance = shard_table(**{col.name: getattr(instance, col.name) for col in inspect(instance.__class__).columns})
    session.add(shard_instance)
    session.commit()

def query_sharded_table(model: Type[Base], company_id: str, session: Session) -> List[Base]:
    """
    Queries data from the appropriate shard based on the company ID.

    Args:
        model (Type[Base]): SQLAlchemy model class to query
        company_id (str): The company ID to query
        session (Session): SQLAlchemy session

    Returns:
        List[Base]: A list of model instances from the queried shard
    """
    shard_number = get_shard_for_company(company_id)
    table_name = f"{model.__tablename__}_shard_{shard_number}"
    shard_table = type(
        f"{model.__name__}Shard{shard_number}",
        (Base,),
        {
            "__tablename__": table_name,
            **{col.name: col.copy() for col in inspect(model).columns},
        },
    )
    return session.query(shard_table).filter(getattr(shard_table, SHARD_KEY_COLUMN) == company_id).all()

def get_all_shards(model: Type[Base], session: Session) -> List[Type[Base]]:
    """
    Returns a list of all shard tables for a given model.

    Args:
        model (Type[Base]): SQLAlchemy model class
        session (Session): SQLAlchemy session

    Returns:
        List[Type[Base]]: A list of all shard table classes for the given model
    """
    num_shards = db_settings.DATABASE_SHARDS
    return [
        type(
            f"{model.__name__}Shard{shard}",
            (Base,),
            {
                "__tablename__": f"{model.__tablename__}_shard_{shard}",
                **{col.name: col.copy() for col in inspect(model).columns},
            },
        )
        for shard in range(num_shards)
    ]

def query_all_shards(model: Type[Base], session: Session, **filters) -> List[Base]:
    """
    Queries data from all shards for a given model with optional filters.

    Args:
        model (Type[Base]): SQLAlchemy model class to query
        session (Session): SQLAlchemy session
        **filters: Optional keyword arguments for filtering the query

    Returns:
        List[Base]: A list of model instances from all shards that match the filters
    """
    results = []
    for shard_table in get_all_shards(model, session):
        query = session.query(shard_table)
        for key, value in filters.items():
            query = query.filter(getattr(shard_table, key) == value)
        results.extend(query.all())
    return results