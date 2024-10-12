"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}

"""
from alembic import op
import sqlalchemy as sa
${imports if imports else ""}

from src.database.base import Base
from src.database.config import get_database_settings

# revision identifiers, used by Alembic.
revision = ${repr(up_revision)}
down_revision = ${repr(down_revision)}
branch_labels = ${repr(branch_labels)}
depends_on = ${repr(depends_on)}


def upgrade():
    """
    Upgrade database schema.
    
    This function defines the changes to be made to the database schema
    when upgrading to this revision.
    
    Requirements addressed:
    - Database Migration Management (2. SYSTEM ARCHITECTURE/2.2 Component Description/2.2.2 Data Layer)
    """
    ${upgrades if upgrades else "pass"}


def downgrade():
    """
    Downgrade database schema.
    
    This function defines the changes to be made to the database schema
    when downgrading from this revision.
    
    Requirements addressed:
    - Database Migration Management (2. SYSTEM ARCHITECTURE/2.2 Component Description/2.2.2 Data Layer)
    """
    ${downgrades if downgrades else "pass"}


# Additional helper functions for complex migrations

def _create_index(table_name, column_name, index_name=None):
    """
    Helper function to create an index on a table column.

    Args:
        table_name (str): Name of the table
        column_name (str): Name of the column to index
        index_name (str, optional): Custom name for the index. If not provided, a default name will be generated.

    Returns:
        None
    """
    if index_name is None:
        index_name = f"ix_{table_name}_{column_name}"
    op.create_index(index_name, table_name, [column_name])


def _drop_index(table_name, column_name, index_name=None):
    """
    Helper function to drop an index from a table column.

    Args:
        table_name (str): Name of the table
        column_name (str): Name of the column with the index
        index_name (str, optional): Name of the index to drop. If not provided, a default name will be used.

    Returns:
        None
    """
    if index_name is None:
        index_name = f"ix_{table_name}_{column_name}"
    op.drop_index(index_name, table_name)


def _add_audit_columns(table_name):
    """
    Helper function to add audit columns (created_at, updated_at) to a table.

    Args:
        table_name (str): Name of the table to add audit columns to

    Returns:
        None
    """
    op.add_column(table_name, sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()))
    op.add_column(table_name, sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.func.now(), onupdate=sa.func.now()))


def _remove_audit_columns(table_name):
    """
    Helper function to remove audit columns (created_at, updated_at) from a table.

    Args:
        table_name (str): Name of the table to remove audit columns from

    Returns:
        None
    """
    op.drop_column(table_name, 'updated_at')
    op.drop_column(table_name, 'created_at')


def _create_enum_type(type_name, enum_values):
    """
    Helper function to create an ENUM type.

    Args:
        type_name (str): Name of the ENUM type
        enum_values (list): List of values for the ENUM type

    Returns:
        None
    """
    op.execute(f"CREATE TYPE {type_name} AS ENUM {tuple(enum_values)}")


def _drop_enum_type(type_name):
    """
    Helper function to drop an ENUM type.

    Args:
        type_name (str): Name of the ENUM type to drop

    Returns:
        None
    """
    op.execute(f"DROP TYPE {type_name}")


# Environment-specific configuration
database_settings = get_database_settings()

# Use database_settings to configure environment-specific migration behavior
# For example:
# if database_settings.DATABASE_ECHO_SQL:
#     op.execute("SET log_statement = 'all'")