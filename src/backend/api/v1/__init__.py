"""
This file serves as the main entry point for version 1 of the API.
It imports and configures all the endpoint routers for the different modules in the v1 API.

Requirements addressed:
1. API Versioning (3.3.5 API Versioning):
   - Implements API versioning to ensure backward compatibility and secure updates.
   - All v1 endpoints are grouped under the "/v1" prefix.

2. API Organization (2. SYSTEM ARCHITECTURE/2.2 Component Description/2.2.1 Application Layer):
   - Organizes API endpoints into a structured module system for better maintainability and scalability.
   - Each module (companies, metrics-input, reporting-financials, reporting-metrics) has its own router.

3. Authentication and Authorization (6. SECURITY CONSIDERATIONS/6.1 AUTHENTICATION AND AUTHORIZATION):
   - Ensures that all endpoints are protected by authentication and authorization mechanisms.
   - These are implemented at the individual router level in their respective files.

4. Rate Limiting (6. SECURITY CONSIDERATIONS/6.2 RATE LIMITING):
   - Applies rate limiting to all endpoints to prevent abuse and ensure fair usage.
   - Rate limiting is implemented at the individual router level in their respective files.

Note: The FastAPI version used is ^0.68.0 or later. Make sure to install the correct version.
"""

from fastapi import APIRouter
from src.backend.api.v1.endpoints import (
    companies,
    metrics_input,
    reporting_financials,
    reporting_metrics,
)

# Create the main v1 API router
api_router = APIRouter(prefix="/v1", tags=["v1"])

# Include all the endpoint routers
api_router.include_router(companies.router, prefix="/companies", tags=["companies"])
api_router.include_router(metrics_input.router, prefix="/metrics-input", tags=["metrics-input"])
api_router.include_router(reporting_financials.router, prefix="/reporting-financials", tags=["reporting-financials"])
api_router.include_router(reporting_metrics.router, prefix="/reporting-metrics", tags=["reporting-metrics"])

# This configuration ensures that all endpoints under /v1 are properly organized,
# versioned, and include the necessary security measures (authentication, authorization, and rate limiting)
# as implemented in their respective router files.