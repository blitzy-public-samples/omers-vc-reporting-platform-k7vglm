"""
Initialization file for the API v1 tests package, organizing and exposing test modules for all v1 API endpoints.

This file imports all test functions from the individual test modules for company-related API endpoints,
metrics input API endpoints, reporting financials API endpoints, and reporting metrics API endpoints.

Requirements Addressed:
    - API Testing Organization (3. SYSTEM DESIGN/3.3 API DESIGN)
    - Organizes and exposes test modules for all v1 API endpoints

Dependencies:
    - src.backend.tests.api.v1.test_companies
    - src.backend.tests.api.v1.test_metrics_input
    - src.backend.tests.api.v1.test_reporting_financials
    - src.backend.tests.api.v1.test_reporting_metrics
"""

from .test_companies import (
    test_create_company,
    test_get_company,
    test_get_companies,
    test_update_company,
    test_create_company_validation_error,
    test_get_company_not_found,
    test_create_company_unauthorized,
    test_delete_company,
    test_partial_update_company
)

from .test_metrics_input import (
    test_create_metrics_input,
    test_get_metrics_input,
    test_update_metrics_input,
    test_delete_metrics_input,
    test_get_metrics_inputs,
    test_create_metrics_input_validation,
    test_update_metrics_input_validation
)

from .test_reporting_financials import (
    test_create_reporting_financials,
    test_get_reporting_financials,
    test_list_reporting_financials,
    test_update_reporting_financials,
    test_delete_reporting_financials,
    test_reporting_financials_validation,
    test_reporting_financials_permissions
)

from .test_reporting_metrics import (
    test_create_reporting_metrics,
    test_read_reporting_metrics,
    test_update_reporting_metrics,
    test_delete_reporting_metrics,
    test_read_reporting_metrics_with_filters,
    test_reporting_metrics_validation,
    test_reporting_metrics_authentication,
    test_reporting_metrics_authorization
)

# The imports above make all test functions from the respective modules available
# when importing from this package. This allows for easier organization and
# discovery of tests when running the test suite.

# Note: By using explicit imports, we're making only the necessary test functions
# available. This approach is more suitable for a production environment as it
# avoids potential naming conflicts and makes the imports more explicit.

# Example of how these tests might be discovered and run:
# pytest src/backend/tests/api/v1