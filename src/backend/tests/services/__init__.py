"""
This file serves as an initialization file for the services test package, importing and exposing test modules for various services in the backend application.

Requirements addressed:
- Testing (2. SYSTEM ARCHITECTURE/2.2 Component Description/2.2.1 Application Layer):
  Organizes and exposes test modules for backend services, facilitating comprehensive testing of the application's service layer.
- Automated Calculations (1.1 System Objectives/3. Automate Calculations):
  Imports test modules that verify the accuracy of automated calculations for derivative metrics.
- Multi-Currency Support Testing (1.2 Scope/Core Functionalities/4. Multi-Currency Support):
  Imports test modules that verify the functionality of currency conversion and exchange rate handling.
- Data Transformation Testing (1.2 Scope/Core Functionalities/3. Data Transformation):
  Imports test modules that verify the accuracy of data transformation processes.
- Error Handling and Logging (1.2 Scope/Core Functionalities/7. Error Handling and Logging):
  Imports test modules that verify proper error handling in various service functions.
"""

from src.backend.tests.services.test_data_transformation import *
from src.backend.tests.services.test_currency_conversion import *
from src.backend.tests.services.test_metrics_calculation import *

# The following imports are used by the test modules and are included here for convenience
import pytest
from unittest.mock import Mock, patch
from freezegun import freeze_time
from decimal import Decimal
from datetime import datetime, date
from uuid import UUID
import requests

# Version information for external dependencies
__test_dependencies__ = {
    "pytest": "^6.2.0",
    "freezegun": "^1.1.0"
}

# Ensure that pytest.mark.asyncio is available for asynchronous tests
pytest_plugins = ["pytest_asyncio"]

# Define common fixtures that can be used across multiple test modules
@pytest.fixture
def mock_db_session():
    return Mock()

@pytest.fixture
def mock_settings():
    from src.backend.core.config import get_settings
    settings = get_settings()
    settings.FOREIGN_EXCHANGE_API_KEY = "test_api_key"
    settings.FOREIGN_EXCHANGE_API_URL = "https://api.example.com/forex"
    return settings

# Define common test data that can be used across multiple test modules
@pytest.fixture
def sample_metrics_input():
    return {
        "company_id": UUID("12345678-1234-5678-1234-567812345678"),
        "reporting_year": 2023,
        "reporting_quarter": 2,
        "currency": "USD",
        "total_revenue": Decimal("1000000"),
        "recurring_revenue": Decimal("800000"),
        "gross_profit": Decimal("600000"),
        "employees": 50,
        "cash_burn": Decimal("200000"),
        "cash_balance": Decimal("1000000"),
        "sales_marketing_expense": Decimal("150000"),
        "total_operating_expense": Decimal("800000"),
        "ebitda": Decimal("200000"),
        "net_income": Decimal("150000"),
        "fiscal_reporting_date": "2023-06-30",
        "fiscal_reporting_quarter": 2,
    }

# Add any additional common fixtures or setup code here

if __name__ == "__main__":
    pytest.main()