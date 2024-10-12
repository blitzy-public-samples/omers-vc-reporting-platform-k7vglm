"""
Core configuration module for the backend application.

This module defines the configuration settings for different environments
and provides a factory function to get the appropriate settings based on
the current environment.

Requirements addressed:
- Environment-specific configuration (2. SYSTEM ARCHITECTURE/2.2 Component Description/2.2.1 Application Layer)
- Security settings (6. SECURITY CONSIDERATIONS/6.1 AUTHENTICATION AND AUTHORIZATION)
"""

import os
from typing import Dict, Any
from pydantic import BaseSettings, Field
from dotenv import load_dotenv

# Import the function to load environment variables from .env file
from src.backend.config import load_config

# Load environment variables from .env file
load_config()

# Global constant for the current environment
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

class Settings(BaseSettings):
    """
    Base settings class with common configuration for all environments.
    """
    API_V1_STR: str = Field("/api/v1", env="API_V1_STR")
    PROJECT_NAME: str = Field("VC Financial Reporting Backend", env="PROJECT_NAME")
    DATABASE_URL: str = Field(..., env="DATABASE_URL")
    JWT_SECRET_KEY: str = Field(..., env="JWT_SECRET_KEY")
    JWT_ALGORITHM: str = Field("HS256", env="JWT_ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(30, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    AZURE_AD_CLIENT_ID: str = Field(..., env="AZURE_AD_CLIENT_ID")
    AZURE_AD_TENANT_ID: str = Field(..., env="AZURE_AD_TENANT_ID")
    AZURE_AD_CLIENT_SECRET: str = Field(..., env="AZURE_AD_CLIENT_SECRET")
    FOREIGN_EXCHANGE_API_KEY: str = Field(..., env="FOREIGN_EXCHANGE_API_KEY")
    FOREIGN_EXCHANGE_API_URL: str = Field(..., env="FOREIGN_EXCHANGE_API_URL")
    DEBUG: bool = Field(False, env="DEBUG")

    class Config:
        case_sensitive = True
        env_file = ".env"

class DevSettings(Settings):
    """Settings class for the development environment."""
    DEBUG: bool = Field(True, env="DEBUG")

class StagingSettings(Settings):
    """Settings class for the staging environment."""
    pass

class ProdSettings(Settings):
    """Settings class for the production environment."""
    pass

def get_settings() -> Settings:
    """
    Factory function to return the appropriate Settings instance based on the current environment.
    
    Returns:
        Settings: An instance of the appropriate Settings class for the current environment.
    """
    env_settings: Dict[str, Any] = {
        "development": DevSettings,
        "staging": StagingSettings,
        "production": ProdSettings
    }
    
    settings_class = env_settings.get(ENVIRONMENT)
    if settings_class is None:
        raise ValueError(f"Unknown environment: {ENVIRONMENT}")
    
    return settings_class()

# Export the settings instance
settings = get_settings()