"""
Main entry point for the VC Financial Reporting Backend application.

This module initializes and configures the FastAPI application, sets up middleware,
includes API routers, and configures error handlers.

Requirements addressed:
1. Application Configuration (2. SYSTEM ARCHITECTURE/2.2 Component Description/2.2.1 Application Layer)
2. API Versioning (3. SYSTEM DESIGN/3.3 API DESIGN/3.3.5 API Versioning)
3. CORS Configuration (6. SECURITY CONSIDERATIONS/6.3 SECURITY PROTOCOLS/6.3.4 Cross-Origin Resource Sharing (CORS))
4. Logging (5. LOGGING AND MONITORING/5.1 Logging)
5. Error Handling (3. SYSTEM DESIGN/3.3 API DESIGN/3.3.7 Error Handling)
"""

import uvicorn
from fastapi import FastAPI, HTTPException, Request, RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.backend.config import get_config, API_V1_STR, PROJECT_NAME, DEBUG, ENVIRONMENT
from src.backend.api.v1 import api_router
from src.backend.db.session import get_db
from src.backend.utils.logging import setup_logging, get_logger
from src.backend.utils.error_handlers import http_error_handler, validation_error_handler, setup_error_handlers

# Setup logging
setup_logging(log_level="DEBUG" if DEBUG else "INFO")
logger = get_logger(__name__)

def create_app() -> FastAPI:
    """
    Creates and configures the FastAPI application
    
    Returns:
        FastAPI: Configured FastAPI application instance
    """
    config = get_config()
    
    app = FastAPI(
        title=PROJECT_NAME,
        description="Backend API for storing and retrieving financial reporting metrics",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
        debug=DEBUG
    )

    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include API router
    app.include_router(api_router, prefix=API_V1_STR)

    # Add custom exception handlers
    setup_error_handlers(app)

    @app.on_event("startup")
    async def startup_event():
        logger.info(f"Starting up the application in {ENVIRONMENT} environment")
        # Perform any additional startup tasks here
        # For example, initialize database connection pool
        await get_db()

    @app.on_event("shutdown")
    async def shutdown_event():
        logger.info("Shutting down the application")
        # Perform any cleanup tasks here
        # For example, close database connections
        # await close_db_connections()

    return app

def get_app() -> FastAPI:
    """
    Returns the configured FastAPI application instance
    
    Returns:
        FastAPI: Configured FastAPI application instance
    """
    return create_app()

app = get_app()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=DEBUG)