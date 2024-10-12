"""
This file serves as the entry point for the API endpoints in version 1 of the backend.
It imports and combines all the endpoint routers from different modules.

Requirements addressed:
1. API Organization (2. SYSTEM ARCHITECTURE/2.2 Component Description/2.2.1 Application Layer):
   Organizes API endpoints into a structured module system for better maintainability and scalability.
2. API Versioning (3.3.5 API Versioning):
   Facilitates API versioning by grouping v1 endpoints together.
3. Authentication and Authorization (6. SECURITY CONSIDERATIONS/6.1 AUTHENTICATION AND AUTHORIZATION):
   Ensures that all endpoints are protected by authentication and authorization mechanisms.
4. Rate Limiting (6. SECURITY CONSIDERATIONS/6.2 RATE LIMITING):
   Applies rate limiting to all endpoints to prevent abuse and ensure fair usage.
"""

from fastapi import APIRouter

# Import routers from individual endpoint modules
from src.backend.api.v1.endpoints.companies import router as companies_router
from src.backend.api.v1.endpoints.metrics_input import router as metrics_input_router
from src.backend.api.v1.endpoints.reporting_financials import router as reporting_financials_router
from src.backend.api.v1.endpoints.reporting_metrics import router as reporting_metrics_router

# Create the main API router for version 1
api_router = APIRouter()

# Include individual routers with their respective prefixes and tags
api_router.include_router(companies_router, prefix="/companies", tags=["companies"])
api_router.include_router(metrics_input_router, prefix="/metrics-input", tags=["metrics-input"])
api_router.include_router(reporting_financials_router, prefix="/reporting-financials", tags=["reporting-financials"])
api_router.include_router(reporting_metrics_router, prefix="/reporting-metrics", tags=["reporting-metrics"])

# Note: Authentication, authorization, and rate limiting are applied at the individual router level
# in their respective files. This ensures that all endpoints are properly secured and rate-limited.