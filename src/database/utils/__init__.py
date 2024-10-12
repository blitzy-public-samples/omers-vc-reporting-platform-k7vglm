"""
This module serves as the initialization module for the database utilities package,
providing easy access to indexing and sharding functions.

Requirements addressed:
- Database Optimization (2. SYSTEM ARCHITECTURE/2.4 Scalability and Performance Considerations):
  Implement database indexing and sharding to optimize query performance and ensure system scalability.

Dependencies:
- src.database.utils.indexing: Import indexing utility functions
- src.database.utils.sharding: Import sharding utility functions
"""

from .indexing import (
    create_indexes,
    drop_indexes,
    check_indexes,
    create_index_if_not_exists,
    optimize_indexes,
    monitor_index_usage
)
from .sharding import (
    create_sharded_tables,
    get_shard_for_company,
    insert_into_shard,
    query_sharded_table,
    get_all_shards,
    query_all_shards
)

__all__ = [
    # Indexing functions
    'create_indexes',
    'drop_indexes',
    'check_indexes',
    'create_index_if_not_exists',
    'optimize_indexes',
    'monitor_index_usage',
    
    # Sharding functions
    'create_sharded_tables',
    'get_shard_for_company',
    'insert_into_shard',
    'query_sharded_table',
    'get_all_shards',
    'query_all_shards'
]

# Additional comments for junior developers
"""
This __init__.py file serves as the entry point for the database utilities package.
It imports and exposes key functions from the indexing and sharding modules, making
them easily accessible when importing from src.database.utils.

Key components:
1. Indexing functions: These functions help manage database indexes for optimizing query performance.
2. Sharding functions: These functions implement database sharding for improved scalability and performance.

Usage example:
from src.database.utils import create_indexes, create_sharded_tables, query_all_shards

def setup_database():
    # Create necessary indexes
    create_indexes(db_session)
    
    # Set up sharded tables
    create_sharded_tables(Base, engine)

def query_data(model, **filters):
    # Query data across all shards
    return query_all_shards(model, db_session, **filters)

Remember to import only the functions you need in your modules to keep the code clean and maintainable.
"""