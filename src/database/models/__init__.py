"""
This file serves as the entry point for the database models package, importing and exposing the ORM models for easy access throughout the application.

Requirements addressed:
- Data Storage and Management (1. Introduction/1.2 Scope/Core Functionalities):
  Implement a PostgreSQL database to store quarterly reporting metrics from portfolio companies
"""

from src.database.models.company import Company
from src.database.models.metrics_input import MetricsInput
from src.database.models.reporting_financials import ReportingFinancials
from src.database.models.reporting_metrics import ReportingMetrics

__all__ = ["Company", "MetricsInput", "ReportingFinancials", "ReportingMetrics"]

# Ensure all models are imported and accessible
assert Company
assert MetricsInput
assert ReportingFinancials
assert ReportingMetrics

# Additional information for developers:
# 1. This file imports all the database models from their respective modules.
# 2. The __all__ list specifies which models should be exposed when importing from this package.
# 3. The assert statements ensure that all models are properly imported and accessible.
# 4. When adding new models, make sure to:
#    a. Import the model at the top of this file
#    b. Add the model name to the __all__ list
#    c. Add an assert statement for the new model
# 5. This structure allows for easy access to all models throughout the application by simply importing from src.database.models