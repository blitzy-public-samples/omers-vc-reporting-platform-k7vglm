"""
This file contains the database-specific configuration settings and utility functions
for the financial reporting metrics backend system.

Requirements addressed:
1. Database Configuration (2. SYSTEM ARCHITECTURE/2.2 Component Description/2.2.2 Data Layer)
   Provides database-specific configuration settings for Azure Database for PostgreSQL
2. Environment-specific Database Settings (3. SYSTEM DESIGN/3.2 DATABASE DESIGN)
   Implements environment-specific database settings for development, staging, and production environments
"""

import os
from pydantic import BaseSettings, Field
from typing import Dict, Any

# Import the load_config function from src.backend.config
from src.backend.config import load_config, ENVIRONMENT

# Load environment variables from .env file
load_config()

class BaseDatabaseSettings(BaseSettings):
    """
    Base settings class with common database configuration for all environments
    """
    DATABASE_URL: str = Field(..., env="DATABASE_URL")
    DATABASE_MAX_CONNECTIONS: int = Field(20, env="DATABASE_MAX_CONNECTIONS")
    DATABASE_POOL_SIZE: int = Field(5, env="DATABASE_POOL_SIZE")
    DATABASE_POOL_RECYCLE: int = Field(300, env="DATABASE_POOL_RECYCLE")
    DATABASE_ECHO_SQL: bool = Field(False, env="DATABASE_ECHO_SQL")

    class Config:
        case_sensitive = True
        env_file = '.env'

class DevDatabaseSettings(BaseDatabaseSettings):
    """
    Database settings class for the development environment
    """
    DATABASE_ECHO_SQL: bool = Field(True, env="DATABASE_ECHO_SQL")

class StagingDatabaseSettings(BaseDatabaseSettings):
    """
    Database settings class for the staging environment
    """
    DATABASE_MAX_CONNECTIONS: int = Field(50, env="DATABASE_MAX_CONNECTIONS")
    DATABASE_POOL_SIZE: int = Field(20, env="DATABASE_POOL_SIZE")

class ProdDatabaseSettings(BaseDatabaseSettings):
    """
    Database settings class for the production environment
    """
    DATABASE_MAX_CONNECTIONS: int = Field(100, env="DATABASE_MAX_CONNECTIONS")
    DATABASE_POOL_SIZE: int = Field(30, env="DATABASE_POOL_SIZE")

def get_database_settings() -> BaseDatabaseSettings:
    """
    Factory function to return the appropriate DatabaseSettings instance based on the current environment

    Returns:
        BaseDatabaseSettings: An instance of the appropriate DatabaseSettings class for the current environment
    """
    env_settings: Dict[str, Any] = {
        "development": DevDatabaseSettings,
        "staging": StagingDatabaseSettings,
        "production": ProdDatabaseSettings
    }
    
    settings_class = env_settings.get(ENVIRONMENT)
    if settings_class is None:
        raise ValueError(f"Invalid environment: {ENVIRONMENT}")
    
    return settings_class()

# Export the database settings instance
database_settings = get_database_settings()