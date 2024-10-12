"""
Initialization file for the API tests package, organizing and exposing test modules for all API versions.

This file imports all test functions from the v1 API test modules, making them available when importing
from this package. This structure allows for easy organization and access to all API test functions
across different versions.

Requirements addressed:
- API Testing Organization (3. SYSTEM DESIGN/3.3 API DESIGN):
  Organizes and exposes test modules for all API versions, facilitating comprehensive API testing.
- Scalability for Future API Versions:
  Provides a structure that can easily accommodate additional API versions as they are developed.

Imports:
- All test functions from src.backend.tests.api.v1 module
"""

# Import all test functions from v1 API test modules
from .v1 import (
    # Company-related tests
    test_create_company,
    test_get_company,
    test_get_companies,
    test_update_company,
    test_create_company_validation_error,
    test_get_company_not_found,
    test_create_company_unauthorized,
    test_delete_company,
    test_partial_update_company,

    # Metrics input tests
    test_create_metrics_input,
    test_get_metrics_input,
    test_update_metrics_input,
    test_delete_metrics_input,
    test_get_metrics_inputs,
    test_create_metrics_input_validation,
    test_update_metrics_input_validation,

    # Reporting financials tests
    test_create_reporting_financials,
    test_get_reporting_financials,
    test_list_reporting_financials,
    test_update_reporting_financials,
    test_delete_reporting_financials,
    test_reporting_financials_validation,
    test_reporting_financials_permissions,

    # Reporting metrics tests
    test_create_reporting_metrics,
    test_read_reporting_metrics,
    test_update_reporting_metrics,
    test_delete_reporting_metrics,
    test_read_reporting_metrics_with_filters,
    test_reporting_metrics_validation,
    test_reporting_metrics_authentication,
    test_reporting_metrics_authorization
)

# Note: As new API versions are added, their respective test modules should be imported here
# For example:
# from .v2 import *

# This structure allows for easy discovery and organization of tests when running the test suite.
# It also provides a clear separation between different API versions, enhancing maintainability
# and scalability of the test suite.