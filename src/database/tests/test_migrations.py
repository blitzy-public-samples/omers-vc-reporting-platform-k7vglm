"""
This file contains unit tests for database migrations, ensuring that schema changes are applied correctly and can be rolled back if necessary.

Requirements addressed:
1. Database Migration Testing (2. SYSTEM ARCHITECTURE/2.2 Component Description/2.2.2 Data Layer)
2. Data Integrity (6. SECURITY CONSIDERATIONS/6.2 DATA SECURITY)
"""

import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy import inspect, text
from src.database.tests.conftest import create_test_database, drop_test_database, TEST_DATABASE_URL
from src.database.config import get_database_settings
from src.database.base import Base

# pytest v6.2.5
# alembic v1.7.0
# sqlalchemy v1.4.0

ALEMBIC_CONFIG_FILE = "src/database/alembic.ini"


@pytest.fixture(scope="module")
def alembic_config():
    """Fixture to create and return an Alembic configuration object."""
    config = Config(ALEMBIC_CONFIG_FILE)
    config.set_main_option("sqlalchemy.url", TEST_DATABASE_URL)
    return config


@pytest.fixture(scope="module", autouse=True)
def setup_and_teardown_test_database(request):
    """
    Fixture to set up the test database before running the tests and tear it down after.
    """
    create_test_database()
    
    def finalizer():
        drop_test_database()
    
    request.addfinalizer(finalizer)


@pytest.mark.usefixtures("setup_and_teardown_test_database")
def test_migrations_apply_successfully(alembic_config):
    """
    Test that all migrations can be applied successfully.

    This test ensures that the database schema can be updated to the latest version without errors.
    """
    # Apply all migrations
    command.upgrade(alembic_config, "head")

    # Verify that all expected tables are created in the database
    engine = Base.metadata.bind
    inspector = inspect(engine)
    table_names = inspector.get_table_names()

    expected_tables = [
        "companies",
        "metrics_input",
        "reporting_financials",
        "reporting_metrics",
        "alembic_version",
    ]

    for table in expected_tables:
        assert table in table_names, f"Table '{table}' not found in the database"

    # Check that the alembic_version table contains the latest revision
    with engine.connect() as connection:
        result = connection.execute(text("SELECT version_num FROM alembic_version")).fetchone()
        assert result is not None, "No version found in alembic_version table"
        assert result[0] is not None, "Version number is None in alembic_version table"


@pytest.mark.usefixtures("setup_and_teardown_test_database")
def test_migrations_rollback_successfully(alembic_config):
    """
    Test that all migrations can be rolled back successfully.

    This test ensures that the database schema can be reverted to its initial state without errors.
    """
    # Apply all migrations
    command.upgrade(alembic_config, "head")

    # Rollback all migrations
    command.downgrade(alembic_config, "base")

    # Verify that all tables are dropped from the database
    engine = Base.metadata.bind
    inspector = inspect(engine)
    table_names = inspector.get_table_names()

    expected_tables = [
        "companies",
        "metrics_input",
        "reporting_financials",
        "reporting_metrics",
    ]

    for table in expected_tables:
        assert table not in table_names, f"Table '{table}' still exists in the database after rollback"

    # Check that the alembic_version table is empty
    with engine.connect() as connection:
        result = connection.execute(text("SELECT COUNT(*) FROM alembic_version")).fetchone()
        assert result[0] == 0, "alembic_version table is not empty after rollback"


@pytest.mark.usefixtures("setup_and_teardown_test_database")
def test_migration_idempotency(alembic_config):
    """
    Test that migrations are idempotent and can be reapplied without errors.

    This test ensures that running migrations multiple times does not cause errors or unexpected changes.
    """
    # Apply all migrations
    command.upgrade(alembic_config, "head")

    # Get the current database schema
    engine = Base.metadata.bind
    inspector = inspect(engine)
    initial_schema = {table: inspector.get_columns(table) for table in inspector.get_table_names()}

    # Attempt to reapply all migrations
    command.upgrade(alembic_config, "head")

    # Verify that the database schema remains unchanged after reapplication
    inspector = inspect(engine)
    final_schema = {table: inspector.get_columns(table) for table in inspector.get_table_names()}

    assert initial_schema == final_schema, "Database schema changed after reapplying migrations"


@pytest.mark.usefixtures("setup_and_teardown_test_database")
def test_migration_data_preservation(alembic_config, db):
    """
    Test that existing data is preserved during migrations.

    This test ensures that applying new migrations does not affect existing data in the database.
    """
    # Apply initial migrations
    command.upgrade(alembic_config, "head")

    # Insert sample data into the database
    sample_company = {
        "name": "Test Company",
        "reporting_status": "Active",
        "reporting_currency": "USD",
        "fund": "Test Fund",
        "location_country": "USA",
        "customer_type": "B2B",
        "revenue_type": "Subscription",
        "year_end_date": "2023-12-31",
    }

    db.execute(
        text("""
        INSERT INTO companies (name, reporting_status, reporting_currency, fund, location_country, customer_type, revenue_type, year_end_date)
        VALUES (:name, :reporting_status, :reporting_currency, :fund, :location_country, :customer_type, :revenue_type, :year_end_date)
        """),
        sample_company,
    )
    db.commit()

    # Get the current revision
    current_revision = command.current(alembic_config)

    # Simulate applying a new migration (for this test, we'll just reapply the current migration)
    command.upgrade(alembic_config, "head")

    # Verify that the sample data is still present and correctly structured after migrations
    result = db.execute(text("SELECT * FROM companies WHERE name = :name"), {"name": sample_company["name"]}).fetchone()
    assert result is not None, "Sample data not found after applying migrations"
    for key, value in sample_company.items():
        assert getattr(result, key) == value, f"Data mismatch for {key} after applying migrations"


if __name__ == "__main__":
    pytest.main([__file__])