"""
Models Package Initialization

This module serves as the initialization point for the models package, importing and exposing
the main model classes for easy access throughout the application. It centralizes the import
of all database models, facilitating easy access to the data structures.

Requirements addressed:
- Data Storage (1.2 Scope/Core Functionalities/1. Data Storage)

Version: 1.0.0
"""

from src.backend.models.company import Company, ReportingStatus, CustomerType, RevenueType
from src.backend.models.metrics_input import MetricsInput
from src.backend.models.reporting_financials import ReportingFinancials
from src.backend.models.reporting_metrics import ReportingMetrics

__all__ = [
    "Company",
    "ReportingStatus",
    "CustomerType",
    "RevenueType",
    "MetricsInput",
    "ReportingFinancials",
    "ReportingMetrics"
]

# Verify that all imported classes exist
assert all(cls for cls in __all__), "One or more imported classes do not exist"

# Ensure circular imports are avoided
from src.backend.db.base import Base

# Register models with Base
Base.metadata.tables.update({
    Company.__tablename__: Company.__table__,
    MetricsInput.__tablename__: MetricsInput.__table__,
    ReportingFinancials.__tablename__: ReportingFinancials.__table__,
    ReportingMetrics.__tablename__: ReportingMetrics.__table__
})

# Set up relationships
Company.metrics_inputs = relationship("MetricsInput", back_populates="company")
Company.reporting_financials = relationship("ReportingFinancials", back_populates="company")
Company.reporting_metrics = relationship("ReportingMetrics", back_populates="company")

# Perform any necessary model validations
def validate_models():
    """
    Perform validation checks on the models to ensure consistency and correctness.
    """
    # Example validation: Check if all required columns are present in each model
    required_columns = {
        Company: ['id', 'name', 'reporting_status', 'reporting_currency'],
        MetricsInput: ['id', 'company_id', 'currency', 'total_revenue'],
        ReportingFinancials: ['id', 'company_id', 'currency', 'exchange_rate_used'],
        ReportingMetrics: ['id', 'company_id', 'currency', 'fiscal_reporting_date']
    }

    for model, columns in required_columns.items():
        for column in columns:
            assert hasattr(model, column), f"{model.__name__} is missing required column: {column}"

    print("All model validations passed successfully.")

# Run model validations
validate_models()