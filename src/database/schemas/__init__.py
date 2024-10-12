"""
This file serves as the entry point for the schemas package, importing and exposing the Pydantic models
defined in the individual schema files for easy access throughout the application.

Requirements addressed:
- Centralized Schema Access (3. SYSTEM DESIGN/3.3 API DESIGN)
  Provide a single import point for all Pydantic schemas used in the application
- Data Validation (2. SYSTEM ARCHITECTURE/2.2 Component Description/2.2.1 Application Layer)
  Ensure consistent data validation across the application
- API Schema Definition (3. SYSTEM DESIGN/3.3 API DESIGN)
  Define clear and consistent API schemas for all data models

Version: 1.0.0
"""

from src.database.schemas.company import (
    Company,
    CompanyCreate,
    CompanyUpdate,
    CompanyInDB,
    CompanyBase,
    CompanyInDBBase
)
from src.database.schemas.metrics_input import (
    MetricsInput,
    MetricsInputCreate,
    MetricsInputUpdate,
    MetricsInputInDB,
    MetricsInputBase
)
from src.database.schemas.reporting_financials import (
    ReportingFinancials,
    ReportingFinancialsCreate,
    ReportingFinancialsUpdate,
    ReportingFinancialsInDB,
    ReportingFinancialsBase
)
from src.database.schemas.reporting_metrics import (
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
    
    # ReportingFinancials schemas
    "ReportingFinancials",
    "ReportingFinancialsCreate",
    "ReportingFinancialsUpdate",
    "ReportingFinancialsInDB",
    "ReportingFinancialsBase",
    
    # ReportingMetrics schemas
    "ReportingMetrics",
    "ReportingMetricsCreate",
    "ReportingMetricsUpdate",
    "ReportingMetricsInDB",
    "ReportingMetricsBase"
]

# Version information
__version__ = "1.0.0"

"""
Usage:
This module provides a centralized import point for all Pydantic schemas used in the application.
By importing from this module, other parts of the application can easily access the required schemas
without needing to know the exact file structure.

Example:
from src.database.schemas import Company, MetricsInputCreate, ReportingFinancialsUpdate

def create_company(company_data: CompanyCreate) -> Company:
    # Implementation here

def update_metrics(metrics_data: MetricsInputUpdate) -> MetricsInput:
    # Implementation here

def get_financials(financials_id: UUID) -> ReportingFinancials:
    # Implementation here

Notes:
- Ensure that all new schemas are added to this file when created.
- Keep the imports organized by entity (Company, MetricsInput, etc.) for clarity.
- Update the __version__ when making changes to the schemas or this file.
- Consider adding type hints in other parts of the application that use these schemas.

Dependencies:
- pydantic==1.10.7 (or the version specified in your requirements.txt)
"""