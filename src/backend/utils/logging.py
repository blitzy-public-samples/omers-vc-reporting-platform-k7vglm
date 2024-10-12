"""
Logging configuration and utility functions for the backend application.

This module provides a centralized logging setup, including JSON formatting,
Azure Monitor integration, and handlers for console and file logging.
It also includes utility functions for logging API calls, database queries, and errors.

Requirements addressed:
- Comprehensive monitoring and logging (2. SYSTEM ARCHITECTURE/2.2 Component Description/2.2.4 Monitoring & Logging)
- Audit logging (6. SECURITY CONSIDERATIONS/6.3 SECURITY PROTOCOLS/6.3.2 Monitoring and Logging)
"""

import logging
from logging.handlers import RotatingFileHandler
import json
from typing import Any, Dict, Optional
from pythonjsonlogger import jsonlogger  # type: ignore
from azure.monitor.opentelemetry import configure_azure_monitor  # type: ignore
from src.backend.config import get_config, ENVIRONMENT

# Import versions:
# pythonjsonlogger==2.0.1
# azure-monitor-opentelemetry==1.0.0b3

logger = logging.getLogger(__name__)

def setup_logging(log_level: str) -> None:
    """
    Configures the logging system for the application.

    This function sets up the logging configuration, including JSON formatting,
    Azure Monitor integration (if in production), and handlers for console and file logging.

    Args:
        log_level (str): The desired log level for the application.

    Returns:
        None
    """
    config = get_config()
    
    # Set up basic logging configuration
    logging.basicConfig(level=log_level)
    
    # Configure JSON formatting for logs
    json_handler = logging.StreamHandler()
    json_formatter = jsonlogger.JsonFormatter(
        fmt='%(asctime)s %(levelname)s %(name)s %(message)s'
    )
    json_handler.setFormatter(json_formatter)
    
    # Set up Azure Monitor integration if in production environment
    if ENVIRONMENT == "production":
        configure_azure_monitor(
            connection_string=config.AZURE_MONITOR_CONNECTION_STRING,
            log_level=log_level
        )
    
    # Add handlers for console and file logging
    console_handler = logging.StreamHandler()
    file_handler = RotatingFileHandler(
        'app.log', maxBytes=10485760, backupCount=5
    )
    
    # Set formatters
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    
    # Add handlers to the root logger
    root_logger = logging.getLogger()
    root_logger.addHandler(json_handler)
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)

def get_logger(module_name: str) -> logging.Logger:
    """
    Returns a logger instance for the specified module.

    Args:
        module_name (str): The name of the module requesting the logger.

    Returns:
        logging.Logger: A configured logger instance.
    """
    return logging.getLogger(module_name)

def log_api_call(request: Any, response: Any) -> None:
    """
    Logs details of an API call.

    Args:
        request: The request object from the API call.
        response: The response object from the API call.

    Returns:
        None
    """
    log_entry = {
        "method": request.method,
        "url": str(request.url),
        "headers": dict(request.headers),
        "client_ip": request.client.host,
        "response_status": response.status_code,
    }
    
    if response.status_code >= 400:
        logger.error(f"API call error: {json.dumps(log_entry)}")
    else:
        logger.info(f"API call: {json.dumps(log_entry)}")

def log_database_query(query: str, params: Dict[str, Any], duration: float) -> None:
    """
    Logs details of a database query.

    Args:
        query (str): The SQL query string.
        params (Dict[str, Any]): The parameters used in the query.
        duration (float): The execution time of the query in seconds.

    Returns:
        None
    """
    log_entry = {
        "query": query,
        "params": params,
        "duration": duration
    }
    logger.info(f"Database query: {json.dumps(log_entry)}")

def log_error(message: str, exc_info: Exception, extra: Optional[Dict[str, Any]] = None) -> None:
    """
    Logs an error with additional context.

    Args:
        message (str): The error message.
        exc_info (Exception): The exception information.
        extra (Optional[Dict[str, Any]]): Additional context to include in the log entry.

    Returns:
        None
    """
    log_entry = {
        "message": message,
        "exception": str(exc_info),
        "extra": extra or {}
    }
    logger.error(f"Error occurred: {json.dumps(log_entry)}", exc_info=True)