"""
This file serves as the initialization point for the CRUD (Create, Read, Update, Delete) package,
importing and exposing CRUD objects for various models in the application.

Requirements addressed:
1. Data Storage and Management (1. Data Storage and Management/F-001):
   Centralizes access to CRUD operations for efficient data management across different models
2. REST API Service (2. REST API Service/F-002):
   Provides a single import point for API endpoints to access database operations
3. Scalability and Performance (2.4 Scalability and Performance Considerations):
   Ensures efficient data access and manipulation through centralized CRUD operations
"""

from .company import CRUDCompany, company
from .metrics_input import CRUDMetricsInput, metrics_input
from .reporting_financials import CRUDReportingFinancials, reporting_financials
from .reporting_metrics import CRUDReportingMetrics, reporting_metrics

# Expose CRUD instances for easy import in other modules
company = company
metrics_input = metrics_input
reporting_financials = reporting_financials
reporting_metrics = reporting_metrics

# Export classes and instances for type hinting and potential subclassing
__all__ = [
    "CRUDCompany",
    "CRUDMetricsInput",
    "CRUDReportingFinancials",
    "CRUDReportingMetrics",
    "company",
    "metrics_input",
    "reporting_financials",
    "reporting_metrics",
]