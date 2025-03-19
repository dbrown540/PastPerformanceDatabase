"""
logging_helper.py
Provides centralized logging functionality for the application.
"""

import os
import logging
import traceback
from datetime import datetime
from typing import Dict, Any, Optional

# Import app settings
from src.config.settings import LOG_LEVEL, LOG_FORMAT, ENABLE_FILE_LOGGING
from src.config.constants import PATHS

def setup_logging() -> None:
    """
    Sets up the logging configuration for Azure Functions environment.
    """
    # Determine log level from settings
    numeric_level = getattr(logging, LOG_LEVEL.upper(), logging.INFO)
    
    # Configure the root logger
    logging.getLogger().setLevel(numeric_level)
    
    # Suppress verbose logging from libraries
    logging.getLogger("azure").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("msrest").setLevel(logging.WARNING)
    
    logging.info(f"Logging initialized at level {LOG_LEVEL}")
    
def log_health_status(is_healthy: bool, status_details: Dict[str, Dict]) -> None:
    """
    Logs the results of a system health check.
    
    Args:
        is_healthy: Overall health status
        status_details: Detailed status for each service
    """
    if is_healthy:
        logging.info("Health check passed: All services available")
    else:
        logging.error("Health check failed: One or more services unavailable")
    
    for service, details in status_details.items():
        if details['status'] == 'healthy':
            logging.info(f"Service {service}: Healthy")
        else:
            logging.error(f"Service {service}: Unhealthy - {details['error']}")