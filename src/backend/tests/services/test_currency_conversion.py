import pytest
from decimal import Decimal
from datetime import date, datetime
from unittest.mock import patch, MagicMock

from src.backend.services.currency_conversion import (
    get_exchange_rate,
    convert_currency,
    update_exchange_rates,
    _fetch_exchange_rate,
)
from src.backend.core.config import get_settings
from src.backend.models.company import Company
from src.backend.db.session import get_db

# Pytest fixture for mocking the settings
@pytest.fixture
def mock_settings():
    settings = get_settings()
    settings.FOREIGN_EXCHANGE_API_KEY = "test_api_key"
    settings.FOREIGN_EXCHANGE_API_URL = "https://api.example.com/forex"
    return settings

# Pytest fixture for mocking the Company model
@pytest.fixture
def mock_company_model():
    companies = [
        MagicMock(reporting_currency="USD"),
        MagicMock(reporting_currency="CAD"),
        MagicMock(reporting_currency="EUR"),
    ]
    with patch("src.backend.models.company.Company") as mock_company:
        mock_company.query.all.return_value = companies
        yield mock_company

# Pytest fixture for mocking the database session
@pytest.fixture
def mock_db_session():
    mock_session = MagicMock()
    with patch("src.backend.db.session.get_db", return_value=iter([mock_session])):
        yield mock_session

@pytest.mark.asyncio
async def test_get_exchange_rate(mock_settings):
    """
    Test the get_exchange_rate function
    
    Requirements addressed:
    - Multi-Currency Support Testing (1.2 Scope/Core Functionalities/4. Multi-Currency Support)
    - Data Transformation Testing (1.2 Scope/Core Functionalities/3. Data Transformation)
    """
    with patch("src.backend.services.currency_conversion._fetch_exchange_rate") as mock_fetch:
        mock_fetch.return_value = Decimal("1.25")
        
        # Test fetching a new exchange rate
        rate = await get_exchange_rate("USD", "CAD", date(2023, 1, 1))
        assert rate == Decimal("1.25")
        mock_fetch.assert_called_once_with("USD", "CAD", date(2023, 1, 1))
        
        # Test caching mechanism
        rate = await get_exchange_rate("USD", "CAD", date(2023, 1, 1))
        assert rate == Decimal("1.25")
        assert mock_fetch.call_count == 1  # Should not be called again due to caching

@pytest.mark.asyncio
async def test_convert_currency(mock_settings):
    """
    Test the convert_currency function
    
    Requirements addressed:
    - Multi-Currency Support Testing (1.2 Scope/Core Functionalities/4. Multi-Currency Support)
    - Data Transformation Testing (1.2 Scope/Core Functionalities/3. Data Transformation)
    """
    with patch("src.backend.services.currency_conversion.get_exchange_rate") as mock_get_rate:
        mock_get_rate.return_value = Decimal("1.25")
        
        amount = Decimal("100.00")
        converted = await convert_currency(amount, "USD", "CAD", date(2023, 1, 1))
        assert converted == Decimal("125.00")
        mock_get_rate.assert_called_once_with("USD", "CAD", date(2023, 1, 1))

@pytest.mark.asyncio
async def test_update_exchange_rates(mock_settings, mock_db_session):
    """
    Test the update_exchange_rates function
    
    Requirements addressed:
    - Multi-Currency Support Testing (1.2 Scope/Core Functionalities/4. Multi-Currency Support)
    """
    mock_db_session.query.return_value.distinct.return_value.all.return_value = [
        ("USD",), ("CAD",), ("EUR",)
    ]
    
    with patch("src.backend.services.currency_conversion.get_exchange_rate") as mock_get_rate:
        mock_get_rate.return_value = Decimal("1.25")
        
        await update_exchange_rates()
        
        # Check that get_exchange_rate was called for each unique currency pair
        expected_calls = [
            (("EUR", "USD", datetime.now().date()),),
            (("EUR", "CAD", datetime.now().date()),),
            (("USD", "CAD", datetime.now().date()),),
        ]
        assert mock_get_rate.call_count == len(expected_calls)
        mock_get_rate.assert_has_calls(expected_calls, any_order=True)

@pytest.mark.asyncio
async def test_fetch_exchange_rate(mock_settings):
    """
    Test the _fetch_exchange_rate function
    
    Requirements addressed:
    - Multi-Currency Support Testing (1.2 Scope/Core Functionalities/4. Multi-Currency Support)
    - Data Transformation Testing (1.2 Scope/Core Functionalities/3. Data Transformation)
    """
    with patch("requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = {"rates": {"CAD": 1.25}}
        mock_get.return_value = mock_response
        
        rate = await _fetch_exchange_rate("USD", "CAD", date(2023, 1, 1))
        assert rate == Decimal("1.25")
        
        mock_get.assert_called_once_with(
            f"{mock_settings.FOREIGN_EXCHANGE_API_URL}/historical",
            params={
                "api_key": mock_settings.FOREIGN_EXCHANGE_API_KEY,
                "base": "USD",
                "symbols": "CAD",
                "date": "2023-01-01",
            },
            timeout=10
        )

@pytest.mark.asyncio
async def test_exchange_rate_caching():
    """
    Test the caching mechanism of exchange rates
    
    Requirements addressed:
    - Multi-Currency Support Testing (1.2 Scope/Core Functionalities/4. Multi-Currency Support)
    """
    with patch("src.backend.services.currency_conversion._fetch_exchange_rate") as mock_fetch:
        mock_fetch.return_value = Decimal("1.25")
        
        # First call should fetch the rate
        rate1 = await get_exchange_rate("USD", "CAD", date(2023, 1, 1))
        assert rate1 == Decimal("1.25")
        mock_fetch.assert_called_once()
        
        # Second call with the same parameters should use the cached value
        rate2 = await get_exchange_rate("USD", "CAD", date(2023, 1, 1))
        assert rate2 == Decimal("1.25")
        assert mock_fetch.call_count == 1  # Should not be called again
        
        # Call with different parameters should fetch a new rate
        rate3 = await get_exchange_rate("USD", "EUR", date(2023, 1, 1))
        assert mock_fetch.call_count == 2  # Should be called again for the new currency pair

@pytest.mark.asyncio
async def test_convert_currency_same_currency():
    """
    Test converting currency when the source and target currencies are the same
    
    Requirements addressed:
    - Multi-Currency Support Testing (1.2 Scope/Core Functionalities/4. Multi-Currency Support)
    """
    amount = Decimal("100.00")
    converted = await convert_currency(amount, "USD", "USD", date(2023, 1, 1))
    assert converted == amount

@pytest.mark.asyncio
async def test_update_exchange_rates_error_handling(mock_db_session):
    """
    Test error handling in update_exchange_rates function
    
    Requirements addressed:
    - Error Handling and Logging (1.2 Scope/Core Functionalities/7. Error Handling and Logging)
    """
    mock_db_session.query.side_effect = Exception("Database error")
    
    with pytest.raises(ValueError, match="Failed to update exchange rates"):
        await update_exchange_rates()

@pytest.mark.asyncio
async def test_fetch_exchange_rate_error_handling(mock_settings):
    """
    Test error handling in _fetch_exchange_rate function
    
    Requirements addressed:
    - Error Handling and Logging (1.2 Scope/Core Functionalities/7. Error Handling and Logging)
    """
    with patch("requests.get") as mock_get:
        mock_get.side_effect = requests.RequestException("API error")
        
        with pytest.raises(ValueError, match="Failed to fetch exchange rate from API"):
            await _fetch_exchange_rate("USD", "CAD", date(2023, 1, 1))

if __name__ == "__main__":
    pytest.main()