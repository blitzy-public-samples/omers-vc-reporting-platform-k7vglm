"""
Security module for the backend application.

This module provides security-related functionality, including password hashing,
JWT token generation and validation, and user authentication.

Requirements addressed:
- Authentication and Authorization (6. SECURITY CONSIDERATIONS/6.1 AUTHENTICATION AND AUTHORIZATION)
- Password Security (6. SECURITY CONSIDERATIONS/6.2 DATA SECURITY)
"""

from datetime import datetime, timedelta
from typing import Optional, List, Union

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from pydantic import BaseModel

from src.backend.core.config import get_settings
from src.backend.db.session import get_db

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Get settings
settings = get_settings()

class UserInDB(BaseModel):
    """
    Pydantic model for user data stored in the database.
    This is a temporary solution until a proper User model is implemented.
    """
    id: int
    username: str
    email: str
    hashed_password: str
    is_active: bool = True
    role: str

    class Config:
        orm_mode = True

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password.
    
    Args:
        plain_password (str): The plain text password to verify.
        hashed_password (str): The hashed password to compare against.
    
    Returns:
        bool: True if the password is correct, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """
    Generate a hash for a password.
    
    Args:
        password (str): The plain text password to hash.
    
    Returns:
        str: The hashed password.
    """
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token.
    
    Args:
        data (dict): The data to encode in the token.
        expires_delta (Optional[timedelta]): The expiration time for the token.
    
    Returns:
        str: The encoded JWT access token.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> UserInDB:
    """
    Get the current user from the JWT token.
    
    Args:
        token (str): The JWT token.
        db (Session): The database session.
    
    Returns:
        UserInDB: The current authenticated user.
    
    Raises:
        HTTPException: If the token is invalid or the user is not found.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    # TODO: Implement proper user retrieval from the database
    # This is a placeholder implementation
    user = UserInDB(
        id=int(user_id),
        username="placeholder",
        email="placeholder@example.com",
        hashed_password="placeholder",
        role="user"
    )
    if user is None:
        raise credentials_exception
    return user

def get_current_active_user(current_user: UserInDB = Depends(get_current_user)) -> UserInDB:
    """
    Get the current active user.
    
    Args:
        current_user (UserInDB): The current authenticated user.
    
    Returns:
        UserInDB: The current active user.
    
    Raises:
        HTTPException: If the user is inactive.
    """
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

class RoleChecker:
    """
    Class for checking user roles.
    """
    def __init__(self, allowed_roles: List[str]):
        self.allowed_roles = allowed_roles

    def __call__(self, user: UserInDB = Depends(get_current_active_user)) -> UserInDB:
        """
        Check if the user has an allowed role.
        
        Args:
            user (UserInDB): The current active user.
        
        Returns:
            UserInDB: The user if they have an allowed role.
        
        Raises:
            HTTPException: If the user doesn't have an allowed role.
        """
        if user.role not in self.allowed_roles:
            raise HTTPException(status_code=403, detail="Operation not permitted")
        return user

# TODO: Implement proper user management system
# The current implementation is a placeholder and needs to be replaced with a proper user model and database integration