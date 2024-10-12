"""
Initialization file for the core module of the backend application, importing and exposing key components and functions from the core submodules.

This file addresses the following requirement:
- Core module initialization (2. SYSTEM ARCHITECTURE/2.2 Component Description/2.2.1 Application Layer)

The core module provides essential components and functions for the backend application, including configuration management, security features, and common dependencies.
"""

# Import configuration-related components
from .config import get_settings, Settings

# Import security-related components
from .security import (
    create_access_token,
    get_password_hash,
    verify_password,
    get_current_user,
    get_current_active_user,
    RoleChecker,
    UserInDB
)

# Import dependency-related components
from .dependencies import (
    get_settings_dependency,
    get_db_dependency,
    get_current_user_dependency,
    get_current_active_user_dependency,
    RoleCheckerDependency
)

# Export all imported components
__all__ = [
    "get_settings",
    "Settings",
    "create_access_token",
    "get_password_hash",
    "verify_password",
    "get_current_user",
    "get_current_active_user",
    "RoleChecker",
    "UserInDB",
    "get_settings_dependency",
    "get_db_dependency",
    "get_current_user_dependency",
    "get_current_active_user_dependency",
    "RoleCheckerDependency"
]