"""
This file serves as the initialization module for the services package, importing and exposing the main service classes
for data transformation, currency conversion, and metrics calculation.

Requirements addressed:
1. Centralize Data Management (1.1 System Objectives/1. Centralize Data Management)
   - Consolidate financial reporting metrics from multiple portfolio companies into a single, organized system.
2. Automate Calculations (1.1 System Objectives/3. Automate Calculations)
   - Reduce manual effort and potential errors by automating the calculation of derivative metrics and currency conversions.
3. Data Transformation (1.2 Scope/Core Functionalities/3. Data Transformation)
   - Transform input data by converting currencies and calculating metrics for financial reporting.
4. Multi-Currency Support (1.2 Scope/Core Functionalities)
   - Support multiple currencies and provide currency conversion functionality.
5. Metrics Calculation (1.2 Scope/Core Functionalities)
   - Calculate various financial metrics and ratios based on input data.
"""

from src.backend.services.data_transformation import DataTransformationService
from src.backend.services.currency_conversion import (
    get_exchange_rate,
    convert_currency,
    update_exchange_rates,
)
from src.backend.services.metrics_calculation import MetricsCalculationService

# Export the main service classes and functions
__all__ = [
    'DataTransformationService',
    'get_exchange_rate',
    'convert_currency',
    'update_exchange_rates',
    'MetricsCalculationService',
]