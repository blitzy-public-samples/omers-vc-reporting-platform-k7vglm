"""
Core dependencies module for the backend application.

This module defines dependency functions and classes used throughout the application
for managing settings, database sessions, and user authentication.

Requirements addressed:
- Configuration Management (2. SYSTEM ARCHITECTURE/2.2 Component Description/2.2.1 Application Layer)
- Database Connection Management (2. SYSTEM ARCHITECTURE/2.2 Component Description/2.2.2 Data Layer)
- Authentication and Authorization (6. SECURITY CONSIDERATIONS/6.1 AUTHENTICATION AND AUTHORIZATION)
- Role-Based Access Control (6. SECURITY CONSIDERATIONS/6.1 AUTHENTICATION AND AUTHORIZATION/6.1.2 Authorization)
"""

from typing import Generator, List
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from src.backend.core.config import get_settings, Settings
from src.backend.db.session import get_db
from src.backend.core.security import (
    get_current_user,
    get_current_active_user,
    RoleChecker,
    UserInDB
)

def get_settings_dependency() -> Settings:
    """
    Dependency function to get application settings.
    
    Returns:
        Settings: Application settings instance
    """
    return get_settings()

def get_db_dependency() -> Generator[Session, None, None]:
    """
    Dependency function to get a database session.
    
    Yields:
        Generator[Session, None, None]: A database session
    """
    yield from get_db()

def get_current_user_dependency(db: Session = Depends(get_db_dependency)) -> UserInDB:
    """
    Dependency function to get the current authenticated user.
    
    Args:
        db (Session): Database session dependency
    
    Returns:
        UserInDB: Current authenticated user
    """
    return get_current_user(db=db)

def get_current_active_user_dependency(
    current_user: UserInDB = Depends(get_current_user_dependency)
) -> UserInDB:
    """
    Dependency function to get the current active user.
    
    Args:
        current_user (UserInDB): Current authenticated user
    
    Returns:
        UserInDB: Current active user
    """
    return get_current_active_user(current_user)

class RoleCheckerDependency:
    """
    Dependency class for checking user roles.
    """

    def __init__(self, allowed_roles: List[str]):
        """
        Initialize the RoleCheckerDependency with allowed roles.
        
        Args:
            allowed_roles (List[str]): List of allowed roles
        """
        self._role_checker = RoleChecker(allowed_roles)

    def __call__(
        self, current_user: UserInDB = Depends(get_current_active_user_dependency)
    ) -> UserInDB:
        """
        Check if the user has an allowed role.
        
        Args:
            current_user (UserInDB): Current active user
        
        Returns:
            UserInDB: The user if they have an allowed role
        
        Raises:
            HTTPException: If the user doesn't have an allowed role
        """
        return self._role_checker(current_user)