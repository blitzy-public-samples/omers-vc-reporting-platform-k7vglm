"""
This file serves as the main entry point for the API module. It imports and configures the versioned API routers,
currently including v1.

Requirements addressed:
1. API Versioning (3.3.5 API Versioning): Implements API versioning to ensure backward compatibility and secure updates.
2. API Organization (2. SYSTEM ARCHITECTURE/2.2 Component Description/2.2.1 Application Layer): Organizes API endpoints
   into a structured module system for better maintainability and scalability.
3. Extensibility: Provides a structure that allows easy addition of future API versions (e.g., v2, v3) when needed.

Note: The FastAPI version used is ^0.68.0 or later. Make sure to install the correct version.
"""

from fastapi import APIRouter
from src.backend.api.v1 import api_router as v1_router

# Create the main API router
# This router will include all versioned API routers
api_router = APIRouter()

# Include the v1 API router
# All v1 endpoints will be accessible under the "/v1" prefix
api_router.include_router(v1_router, prefix="/v1")

# To add a new API version in the future, follow this pattern:
# from src.backend.api.v2 import api_router as v2_router
# api_router.include_router(v2_router, prefix="/v2")

# The configuration in the v1 router ensures that all endpoints under /v1 are properly organized,
# versioned, and include the necessary security measures (authentication, authorization, and rate limiting)
# as implemented in their respective router files.

# When adding new versions, make sure to implement similar security measures and follow the same
# organizational structure to maintain consistency across API versions.