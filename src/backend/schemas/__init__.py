"""
This file serves as the entry point for the schemas package, importing and exposing the main Pydantic models for easy access throughout the application.

Requirements addressed:
1. Data Validation (2. SYSTEM ARCHITECTURE/2.2 Component Description/2.2.1 Application Layer):
   Centralizes access to Pydantic models used for request/response validation in the FastAPI application
2. API Design (3. SYSTEM DESIGN/3.3 API DESIGN):
   Provides a single import point for all schema models used in API endpoints
3. Modularity and Maintainability:
   Organizes schema models in a structured manner, making it easier to manage and update as the application grows

Version information:
- pydantic==1.10.7 (inferred from imported files)
"""

from src.backend.schemas.company import (
    Company,
    CompanyCreate,
    CompanyUpdate,
    CompanyInDB,
    CompanyBase,
    CompanyInDBBase
)
from src.backend.schemas.metrics_input import (
    MetricsInput,
    MetricsInputCreate,
    MetricsInputUpdate,
    MetricsInputInDB,
    MetricsInputBase,
    MetricsInputInDBBase
)
from src.backend.schemas.reporting_financials import (
    ReportingFinancials,
    ReportingFinancialsCreate,
    ReportingFinancialsUpdate,
    ReportingFinancialsInDB,
    ReportingFinancialsBase,
    ReportingFinancialsInDBBase
)
from src.backend.schemas.reporting_metrics import (
    ReportingMetrics,
    ReportingMetricsCreate,
    ReportingMetricsUpdate,
    ReportingMetricsInDB,
    ReportingMetricsBase
)

__all__ = [
    # Company schemas
    "Company",
    "CompanyCreate",
    "CompanyUpdate",
    "CompanyInDB",
    "CompanyBase",
    "CompanyInDBBase",
    
    # MetricsInput schemas
    "MetricsInput",
    "MetricsInputCreate",
    "MetricsInputUpdate",
    "MetricsInputInDB",
    "MetricsInputBase",
    "MetricsInputInDBBase",
    
    # ReportingFinancials schemas
    "ReportingFinancials",
    "ReportingFinancialsCreate",
    "ReportingFinancialsUpdate",
    "ReportingFinancialsInDB",
    "ReportingFinancialsBase",
    "ReportingFinancialsInDBBase",
    
    # ReportingMetrics schemas
    "ReportingMetrics",
    "ReportingMetricsCreate",
    "ReportingMetricsUpdate",
    "ReportingMetricsInDB",
    "ReportingMetricsBase"
]

# Additional notes for developers:
# 1. This file acts as a central hub for all schema models, simplifying imports in other parts of the application.
# 2. When adding new schema models or modifying existing ones, make sure to update this file accordingly.
# 3. The __all__ list explicitly defines which names are exported when using "from src.backend.schemas import *".
# 4. Keeping this file organized and up-to-date is crucial for maintaining a clean and efficient codebase.
# 5. If you add new schema files, remember to import and include them in this file.