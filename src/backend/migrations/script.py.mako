"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}

"""
from alembic import op
import sqlalchemy as sa
${imports if imports else ""}
${other_imports if other_imports else ""}

# revision identifiers, used by Alembic.
revision = ${repr(up_revision)}
down_revision = ${repr(down_revision)}
branch_labels = ${repr(branch_labels)}
depends_on = ${repr(depends_on)}


def upgrade() -> None:
    """
    Upgrade database schema and data to the next version.
    
    This function should contain the SQL commands or Alembic operations
    necessary to upgrade the database to the current revision.
    """
    ${upgrades if upgrades else "pass"}


def downgrade() -> None:
    """
    Downgrade database schema and data to the previous version.
    
    This function should contain the SQL commands or Alembic operations
    necessary to downgrade the database to the previous revision.
    """
    ${downgrades if downgrades else "pass"}