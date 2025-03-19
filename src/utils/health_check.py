"""
health_check.py
Provides pre-execution health check functionality to verify system readiness
"""

import logging
import requests
from typing import Dict, List, Tuple, Optional

from src.functions.authentication import get_access_token
from src.config.settings import SHAREPOINT_URL
from src.utils.logging_helper import log_health_status

def check_sharepoint_availability() -> Tuple[bool, Optional[str]]:
    """
    Verifies SharePoint connectivity by attempting to get an access token.

    Returns:
        Tuple[bool, Optional[str]] (is_available, error_message)
    """
    try:
        token = get_access_token()
        if token:
            return True, None
        else:
            return False, "Failed to acquire SharePoint access token"
        
    except Exception as e:
        return False, f"SharePoint authentication error: {str(e)}"
    
def run_health_check() -> Tuple[bool, Dict[str, Dict]]:
    """
    Performs a comprehensive health check of all required services.

    Returns:
        Tuple[bool, Dict]: (all_systems_go, health_status_details)
    """
    
    health_results = {}
    all_healthy = True

    sharepoint_healthy, sharepoint_error = check_sharepoint_availability()
    health_results["sharepoint"] = {
        "status": "healthy" if sharepoint_healthy else "unhealthy",
        "error": sharepoint_error
    }

    all_healthy = all_healthy and sharepoint_healthy

    return all_healthy, health_results

def is_system_ready():
    """
    Simplified interface for health check that returns a boolean.
    
    Returns:
        bool: True if all systems are healthy, False otherwise
    """
    all_healthy, status_details = run_health_check()

    return all_healthy