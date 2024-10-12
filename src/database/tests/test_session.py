import pytest
from unittest.mock import Mock, patch
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.session import get_db, SessionLocal, AsyncDatabaseSession
from src.database.config import get_database_settings

# Requirement: Database Connection Testing
# Location: 3. SYSTEM COMPONENTS ARCHITECTURE/3.2 SEQUENCE DIAGRAMS
@pytest.mark.asyncio
async def test_get_db_yields_session():
    """
    Test that get_db yields a valid database session.
    This test verifies the correct establishment of database connections.
    """
    db_generator = get_db()
    session = next(db_generator)
    try:
        assert isinstance(session, Session)
        assert session.bind is not None
    finally:
        session.close()
        db_generator.close()

# Requirement: Session Management Testing
# Location: 3. SYSTEM DESIGN/3.2 DATABASE DESIGN
def test_get_db_closes_session():
    """
    Test that get_db closes the session after use.
    This test ensures proper creation, usage, and closure of database sessions.
    """
    mock_session = Mock(spec=Session)
    with patch('src.database.session.SessionLocal', return_value=mock_session):
        db_generator = get_db()
        next(db_generator)
        db_generator.close()
    mock_session.close.assert_called_once()

# Requirement: Error Handling Testing
# Location: 6. SECURITY CONSIDERATIONS/6.2 DATA SECURITY
def test_get_db_handles_exceptions():
    """
    Test that get_db properly handles exceptions during session use.
    This test validates correct handling of database connection and session errors.
    """
    mock_session = Mock(spec=Session)
    mock_session.query.side_effect = SQLAlchemyError("Test exception")
    
    with patch('src.database.session.SessionLocal', return_value=mock_session):
        db_generator = get_db()
        session = next(db_generator)
        with pytest.raises(SQLAlchemyError):
            session.query()  # This will raise the mocked exception
        db_generator.close()
    
    mock_session.close.assert_called_once()

def test_database_url_configuration():
    """
    Test that the database URL is correctly configured.
    This test verifies that the database connection string is properly set.
    """
    db_settings = get_database_settings()
    assert db_settings.DATABASE_URL is not None
    assert db_settings.DATABASE_URL.startswith('postgresql://')

def test_session_factory_configuration():
    """
    Test that the SessionLocal is correctly configured.
    This test ensures that the session factory is properly set up.
    """
    session = SessionLocal()
    try:
        assert isinstance(session, Session)
        assert session.bind is not None
    finally:
        session.close()

def test_database_pool_size_configuration():
    """
    Test that the database pool size is correctly configured.
    """
    db_settings = get_database_settings()
    assert db_settings.DATABASE_POOL_SIZE > 0
    assert db_settings.DATABASE_POOL_SIZE <= db_settings.DATABASE_MAX_CONNECTIONS

def test_database_max_connections_configuration():
    """
    Test that the maximum number of database connections is correctly configured.
    """
    db_settings = get_database_settings()
    assert db_settings.DATABASE_MAX_CONNECTIONS > 0
    assert db_settings.DATABASE_MAX_CONNECTIONS >= db_settings.DATABASE_POOL_SIZE

def test_database_pool_recycle_configuration():
    """
    Test that the database connection recycle time is correctly configured.
    """
    db_settings = get_database_settings()
    assert db_settings.DATABASE_POOL_RECYCLE > 0

@pytest.mark.asyncio
async def test_async_database_session():
    """
    Test that AsyncDatabaseSession can be used to create an async session.
    """
    async_db = AsyncDatabaseSession()
    async with async_db.get_db() as session:
        assert isinstance(session, AsyncSession)
        assert session.bind is not None

@pytest.mark.asyncio
async def test_async_database_session_exception_handling():
    """
    Test that AsyncDatabaseSession properly handles exceptions and performs rollback.
    """
    async_db = AsyncDatabaseSession()
    with patch.object(AsyncSession, 'commit', side_effect=SQLAlchemyError("Test exception")):
        with pytest.raises(SQLAlchemyError):
            async with async_db.get_db() as session:
                # Simulate some database operation
                await session.execute("SELECT 1")
        # The session should be closed after the exception
        assert session.is_active is False

def test_environment_specific_settings():
    """
    Test that environment-specific database settings are correctly applied.
    """
    db_settings = get_database_settings()
    
    if db_settings.__class__.__name__ == "DevDatabaseSettings":
        assert db_settings.DATABASE_ECHO_SQL is True
    elif db_settings.__class__.__name__ in ["StagingDatabaseSettings", "ProdDatabaseSettings"]:
        assert db_settings.DATABASE_ECHO_SQL is False
        assert db_settings.DATABASE_MAX_CONNECTIONS >= 50
        assert db_settings.DATABASE_POOL_SIZE >= 20

# Note: The following imports are included as comments to show the versions of the external libraries used
# pytest==6.2.5
# SQLAlchemy==1.4.0