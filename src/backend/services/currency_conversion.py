"""
Currency conversion service for the backend application.

This module provides functionality for currency conversion, including fetching
exchange rates, converting amounts between currencies, and updating exchange rates.

Requirements addressed:
- Currency conversion (3. FUNCTIONAL REQUIREMENTS/3.2 Data Processing and Analysis/3.2.3 Currency Conversion)
- Caching for performance optimization (2. SYSTEM ARCHITECTURE/2.2 Component Description/2.2.3 Data Layer)
"""

import requests
from datetime import date, datetime
from decimal import Decimal
from typing import Dict, Optional
from functools import lru_cache

from src.backend.core.config import get_settings
from src.backend.utils.logging import get_logger
from src.backend.models.company import Company
from src.backend.db.session import get_db

# Initialize logger and settings
logger = get_logger(__name__)
settings = get_settings()

# Global cache for exchange rates
exchange_rates: Dict[str, Dict[str, Dict[date, Decimal]]] = {}

@lru_cache(maxsize=100)
def get_exchange_rate(from_currency: str, to_currency: str, date: date) -> Decimal:
    """
    Retrieves the exchange rate for a given currency pair.

    Args:
        from_currency (str): The currency to convert from.
        to_currency (str): The currency to convert to.
        date (date): The date for which to retrieve the exchange rate.

    Returns:
        Decimal: The exchange rate as a Decimal.

    Raises:
        ValueError: If the exchange rate cannot be retrieved.
    """
    logger.info(f"Getting exchange rate for {from_currency} to {to_currency} on {date}")

    # Check if the exchange rate is already in the cache
    if from_currency in exchange_rates and to_currency in exchange_rates[from_currency]:
        cached_rate = exchange_rates[from_currency][to_currency].get(date)
        if cached_rate:
            logger.debug(f"Using cached exchange rate: {cached_rate}")
            return cached_rate

    # If not in cache, fetch the rate from the foreign exchange API
    rate = _fetch_exchange_rate(from_currency, to_currency, date)

    # Store the fetched rate in the cache
    if from_currency not in exchange_rates:
        exchange_rates[from_currency] = {}
    if to_currency not in exchange_rates[from_currency]:
        exchange_rates[from_currency][to_currency] = {}
    exchange_rates[from_currency][to_currency][date] = rate

    return rate

def convert_currency(amount: Decimal, from_currency: str, to_currency: str, date: date) -> Decimal:
    """
    Converts an amount from one currency to another.

    Args:
        amount (Decimal): The amount to convert.
        from_currency (str): The currency to convert from.
        to_currency (str): The currency to convert to.
        date (date): The date for which to perform the conversion.

    Returns:
        Decimal: The converted amount as a Decimal.

    Raises:
        ValueError: If the conversion cannot be performed.
    """
    logger.info(f"Converting {amount} {from_currency} to {to_currency} on {date}")

    if from_currency == to_currency:
        return amount

    rate = get_exchange_rate(from_currency, to_currency, date)
    converted_amount = amount * rate
    return Decimal(round(converted_amount, 2))

def update_exchange_rates() -> None:
    """
    Updates the exchange rates for all required currency pairs.

    This function fetches the list of unique reporting currencies from the Company model
    and updates exchange rates to USD and CAD for each currency.

    Raises:
        ValueError: If there's an error updating the exchange rates.
    """
    logger.info("Updating exchange rates")

    try:
        db = next(get_db())
        reporting_currencies = db.query(Company.reporting_currency).distinct().all()
        reporting_currencies = [currency[0] for currency in reporting_currencies]

        today = date.today()

        for currency in reporting_currencies:
            if currency != "USD":
                get_exchange_rate(currency, "USD", today)
            if currency != "CAD":
                get_exchange_rate(currency, "CAD", today)

        # Update exchange rate between USD and CAD
        get_exchange_rate("USD", "CAD", today)

        logger.info("Exchange rates updated successfully")
    except Exception as e:
        logger.error(f"Error updating exchange rates: {str(e)}")
        raise ValueError("Failed to update exchange rates") from e

def _fetch_exchange_rate(from_currency: str, to_currency: str, date: date) -> Decimal:
    """
    Private function to fetch exchange rate from the foreign exchange API.

    Args:
        from_currency (str): The currency to convert from.
        to_currency (str): The currency to convert to.
        date (date): The date for which to retrieve the exchange rate.

    Returns:
        Decimal: The fetched exchange rate as a Decimal.

    Raises:
        ValueError: If the API request fails or returns an invalid response.
    """
    logger.debug(f"Fetching exchange rate from API: {from_currency} to {to_currency} on {date}")

    url = f"{settings.FOREIGN_EXCHANGE_API_URL}/historical"
    params = {
        "api_key": settings.FOREIGN_EXCHANGE_API_KEY,
        "base": from_currency,
        "symbols": to_currency,
        "date": date.isoformat()
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if "rates" not in data or to_currency not in data["rates"]:
            raise ValueError("Invalid API response")

        rate = Decimal(str(data["rates"][to_currency]))
        logger.debug(f"Fetched exchange rate: {rate}")
        return rate
    except requests.RequestException as e:
        logger.error(f"Error fetching exchange rate: {str(e)}")
        raise ValueError("Failed to fetch exchange rate from API") from e