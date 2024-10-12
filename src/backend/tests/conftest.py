"""
Pytest configuration file for backend tests.

This module contains fixtures and configurations used across multiple test files in the backend.
It sets up the test database, provides a test client, and overrides settings for testing purposes.

Requirements addressed:
1. Testing (5. TESTING AND QUALITY ASSURANCE):
   Implements fixtures for database testing, API client testing, and settings override.
2. Database Testing (5.2 Testing Strategies):
   Provides fixtures for creating and managing test databases.
3. API Testing (5.2 Testing Strategies):
   Offers a fixture for creating an async test client for API endpoint testing.
"""

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.backend.db.base import Base
from src.backend.db.session import get_db
from src.backend.core.config import get_settings, Settings
from src.backend.main import get_app

# Pytest fixture for overriding settings
@pytest.fixture
def test_settings() -> Settings:
    """
    Fixture to provide test-specific settings.
    
    Returns:
        Settings: A Settings instance with test-specific configurations.
    """
    settings = get_settings()
    settings.DATABASE_URL = "sqlite+aiosqlite:///./test.db"
    settings.DEBUG = True
    return settings

# Pytest fixture for creating a test database engine
@pytest.fixture(scope="session")
def db_engine(test_settings: Settings):
    """
    Fixture to create and yield a test database engine.
    
    Args:
        test_settings: The test settings fixture.
    
    Yields:
        AsyncEngine: The test database engine.
    """
    engine = create_async_engine(
        test_settings.DATABASE_URL,
        connect_args={"check_same_thread": False},
        echo=True,
    )
    yield engine
    engine.dispose()

# Pytest fixture for creating test database tables
@pytest.fixture(scope="session")
async def create_tables(db_engine):
    """
    Fixture to create test database tables.
    
    Args:
        db_engine: The test database engine fixture.
    """
    async with db_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Pytest fixture for creating a test database session
@pytest.fixture
async def db_session(db_engine, create_tables) -> AsyncSession:
    """
    Fixture to create and yield a test database session.
    
    Args:
        db_engine: The test database engine fixture.
        create_tables: The fixture to create test database tables.
    
    Yields:
        AsyncSession: The test database session.
    """
    async_session = sessionmaker(
        db_engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session
        await session.rollback()

# Pytest fixture for creating an async test client
@pytest.fixture
async def client(db_session: AsyncSession, test_settings: Settings) -> AsyncClient:
    """
    Fixture to create and yield an async test client.
    
    Args:
        db_session: The test database session fixture.
        test_settings: The test settings fixture.
    
    Yields:
        AsyncClient: The async test client.
    """
    app = get_app()
    
    async def override_get_db():
        yield db_session

    async def override_get_settings():
        return test_settings

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_settings] = override_get_settings
    
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

# Additional fixtures can be added here as needed for specific test cases