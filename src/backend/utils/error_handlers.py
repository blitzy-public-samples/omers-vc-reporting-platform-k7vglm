"""
Error handling module for the backend application.

This module provides custom error handlers for HTTP exceptions and validation errors,
ensuring consistent error responses across the application.

Requirements addressed:
- Error Handling (3. SYSTEM DESIGN/3.3 API DESIGN/3.3.7 Error Handling)
- API Security (6. SECURITY CONSIDERATIONS/6.3 SECURITY PROTOCOLS/6.3.6 API Security)
"""

from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
import logging
from typing import List, Dict, Any

from src.backend.core.config import settings

# Initialize logger
logger = logging.getLogger(__name__)

async def http_error_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """
    Handles HTTP exceptions and returns a formatted JSON response.
    
    Args:
        request (Request): The incoming request object.
        exc (HTTPException): The HTTP exception that was raised.
    
    Returns:
        JSONResponse: Formatted error response.
    """
    # Log the error details
    logger.error(f"HTTP error occurred: {exc.status_code} - {exc.detail}")
    logger.error(f"Request path: {request.url.path}")

    # Create the error response
    error_response = format_error_response(
        error_code=f"HTTP_{exc.status_code}",
        error_message=str(exc.detail),
        error_details=[]
    )

    return JSONResponse(content=error_response, status_code=exc.status_code)

async def validation_error_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """
    Handles validation errors for request data and returns a formatted JSON response.
    
    Args:
        request (Request): The incoming request object.
        exc (RequestValidationError): The validation error that was raised.
    
    Returns:
        JSONResponse: Formatted validation error response.
    """
    # Log the validation error details
    logger.error(f"Validation error occurred: {exc.errors()}")
    logger.error(f"Request path: {request.url.path}")

    # Extract error details
    error_details = [
        {"field": ".".join(map(str, error["loc"])), "issue": error["msg"]}
        for error in exc.errors()
    ]

    # Create the error response
    error_response = format_error_response(
        error_code="VALIDATION_ERROR",
        error_message="The provided input is invalid.",
        error_details=error_details
    )

    return JSONResponse(content=error_response, status_code=422)

def format_error_response(error_code: str, error_message: str, error_details: List[Dict[str, str]]) -> Dict[str, Any]:
    """
    Formats an error response according to the specified structure.
    
    Args:
        error_code (str): A unique code identifying the error.
        error_message (str): A human-readable error message.
        error_details (List[Dict[str, str]]): A list of detailed error information.
    
    Returns:
        Dict[str, Any]: Formatted error response dictionary.
    """
    return {
        "error": {
            "code": error_code,
            "message": error_message,
            "details": error_details,
            "request_id": settings.REQUEST_ID_HEADER  # Add request ID for tracing
        }
    }

def setup_error_handlers(app):
    """
    Sets up error handlers for the FastAPI application.
    
    Args:
        app: The FastAPI application instance.
    """
    app.add_exception_handler(HTTPException, http_error_handler)
    app.add_exception_handler(RequestValidationError, validation_error_handler)

# Note: The following imports are used in this file
# fastapi version: ^0.68.0
# logging: Python standard library