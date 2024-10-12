"""
This file contains utility functions for creating, dropping, and checking database indexes
to optimize query performance in the financial reporting metrics system.

Requirements addressed:
1. Database Optimization (2. SYSTEM ARCHITECTURE/2.4 Scalability and Performance Considerations)
2. Data Storage and Management (1. Introduction/1.2 Scope/Core Functionalities)
"""

from sqlalchemy import Index, inspect
from src.database.base import Base
from src.database.session import get_db
from src.database.models import Company, MetricsInput, ReportingFinancials, ReportingMetrics

# SQLAlchemy version: ^1.4.0 (as per the project's requirements)


def create_indexes(db):
    """
    Creates indexes on the database tables to optimize query performance.

    Args:
        db: Database session dependency.

    Returns:
        None
    """
    with db() as session:
        # Create index on Companies table for the 'name' column
        Index('idx_companies_name', Company.name).create(session.bind)

        # Create index on Metrics_Input table for 'company_id' and 'fiscal_reporting_date' columns
        Index('idx_metrics_input_company_date', MetricsInput.company_id, MetricsInput.fiscal_reporting_date).create(session.bind)

        # Create index on Quarterly_Reporting_Financials table for 'company_id' and 'fiscal_reporting_date' columns
        Index('idx_quarterly_financials_company_date', ReportingFinancials.company_id, ReportingFinancials.fiscal_reporting_date).create(session.bind)

        # Create index on Quarterly_Reporting_Metrics table for 'company_id' and 'fiscal_reporting_date' columns
        Index('idx_quarterly_metrics_company_date', ReportingMetrics.company_id, ReportingMetrics.fiscal_reporting_date).create(session.bind)

        # Commit the changes to the database
        session.commit()


def drop_indexes(db):
    """
    Drops all custom indexes created for the financial reporting metrics tables.

    Args:
        db: Database session dependency.

    Returns:
        None
    """
    with db() as session:
        # Drop index on Companies table for the 'name' column
        Index('idx_companies_name', Company.name).drop(session.bind)

        # Drop index on Metrics_Input table for 'company_id' and 'fiscal_reporting_date' columns
        Index('idx_metrics_input_company_date', MetricsInput.company_id, MetricsInput.fiscal_reporting_date).drop(session.bind)

        # Drop index on Quarterly_Reporting_Financials table for 'company_id' and 'fiscal_reporting_date' columns
        Index('idx_quarterly_financials_company_date', ReportingFinancials.company_id, ReportingFinancials.fiscal_reporting_date).drop(session.bind)

        # Drop index on Quarterly_Reporting_Metrics table for 'company_id' and 'fiscal_reporting_date' columns
        Index('idx_quarterly_metrics_company_date', ReportingMetrics.company_id, ReportingMetrics.fiscal_reporting_date).drop(session.bind)

        # Commit the changes to the database
        session.commit()


def check_indexes(db):
    """
    Checks if the required indexes exist on the financial reporting metrics tables.

    Args:
        db: Database session dependency.

    Returns:
        dict: A dictionary containing the status of each required index.
    """
    with db() as session:
        # Get an inspector object for the database
        inspector = inspect(session.bind)

        # Check for the existence of each required index
        index_status = {
            'idx_companies_name': False,
            'idx_metrics_input_company_date': False,
            'idx_quarterly_financials_company_date': False,
            'idx_quarterly_metrics_company_date': False
        }

        for table_name in ['companies', 'metrics_input', 'quarterly_reporting_financials', 'quarterly_reporting_metrics']:
            indexes = inspector.get_indexes(table_name)
            for index in indexes:
                if index['name'] in index_status:
                    index_status[index['name']] = True

        return index_status


def create_index_if_not_exists(db, index_name, table, *columns):
    """
    Creates an index if it doesn't already exist.

    Args:
        db: Database session dependency.
        index_name (str): Name of the index to create.
        table (Table): SQLAlchemy Table object on which to create the index.
        *columns: Columns to include in the index.

    Returns:
        None
    """
    with db() as session:
        inspector = inspect(session.bind)
        existing_indexes = inspector.get_indexes(table.__tablename__)
        
        if not any(index['name'] == index_name for index in existing_indexes):
            Index(index_name, *columns).create(session.bind)
            session.commit()


def optimize_indexes(db):
    """
    Optimizes existing indexes in the database.

    Args:
        db: Database session dependency.

    Returns:
        None
    """
    with db() as session:
        # Perform REINDEX on all tables to optimize existing indexes
        session.execute("REINDEX DATABASE CONCURRENTLY")
        session.commit()


def monitor_index_usage(db):
    """
    Monitors the usage of indexes in the database.

    Args:
        db: Database session dependency.

    Returns:
        list: A list of dictionaries containing index usage statistics.
    """
    with db() as session:
        query = """
        SELECT
            schemaname || '.' || relname AS table,
            indexrelname AS index,
            pg_size_pretty(pg_relation_size(i.indexrelid)) AS index_size,
            idx_scan AS index_scans
        FROM pg_stat_user_indexes ui
        JOIN pg_index i ON ui.indexrelid = i.indexrelid
        WHERE schemaname NOT IN ('pg_catalog', 'information_schema')
        ORDER BY pg_relation_size(i.indexrelid) DESC;
        """
        result = session.execute(query)
        return [dict(row) for row in result]


# Additional comments for junior developers
"""
This module provides utility functions for managing database indexes in the financial reporting metrics system.
Proper indexing is crucial for optimizing query performance, especially as the database grows in size.

Key functions:
1. create_indexes: Creates all necessary indexes for the main tables.
2. drop_indexes: Drops all custom indexes (useful for maintenance or schema changes).
3. check_indexes: Verifies the existence of required indexes.
4. create_index_if_not_exists: Creates an index only if it doesn't already exist.
5. optimize_indexes: Rebuilds indexes to improve their efficiency.
6. monitor_index_usage: Provides statistics on index usage to help identify unused or inefficient indexes.

When working with large datasets, consider the following best practices:
1. Create indexes on columns frequently used in WHERE clauses, JOIN conditions, and ORDER BY clauses.
2. Avoid over-indexing, as it can slow down write operations and increase storage requirements.
3. Regularly monitor index usage and performance to identify opportunities for optimization.
4. Use composite indexes for queries that frequently filter or sort by multiple columns together.

Example usage:
from src.database.session import get_db
from src.database.utils.indexing import create_indexes, check_indexes, monitor_index_usage

def setup_database_indexes():
    create_indexes(get_db)
    index_status = check_indexes(get_db)
    print("Index status:", index_status)

def analyze_index_performance():
    usage_stats = monitor_index_usage(get_db)
    for stat in usage_stats:
        print(f"Index {stat['index']} on {stat['table']} - Size: {stat['index_size']}, Scans: {stat['index_scans']}")

Remember to run these functions during application setup or as part of regular maintenance tasks.
"""