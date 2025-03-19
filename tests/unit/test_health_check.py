"""
test_health_check.py
Testing the handling of the health checks.
"""

import pytest
from unittest.mock import patch, MagicMock
from src.utils.health_check import (
    check_sharepoint_availability,
    run_health_check,
    is_system_ready
)

# Test the SharePoint availability check
@patch("src.utils.health_check.get_access_token")
def test_check_sharepoint_availability(mock_get_token):
    """Test SharePoint availability check with different token scenarios"""
    # Test successful scenario
    mock_get_token.return_value = "mock_token"
    is_available, error_message = check_sharepoint_availability()
    assert is_available == True
    assert error_message is None

    # Test failure scenario
    mock_get_token.return_value = None
    is_available, error_message = check_sharepoint_availability()
    assert is_available == False
    assert "Failed to acquire SharePoint access token" in error_message

    # Test exception scenario
    mock_get_token.side_effect = Exception("Connection error")
    is_available, error_message = check_sharepoint_availability()
    assert is_available == False
    assert "SharePoint authentication error" in error_message

# Test the comprehensive health check
@patch("src.utils.health_check.check_sharepoint_availability")
def test_run_health_check(mock_check_sharepoint):
    """Test health check aggregation"""
    # Test when all systems are healthy
    mock_check_sharepoint.return_value = (True, None)
    all_healthy, health_results = run_health_check()
    assert all_healthy == True
    assert health_results["sharepoint"]["status"] == "healthy"
    
    # Test when a system is unhealthy
    mock_check_sharepoint.return_value = (False, "SharePoint error")
    all_healthy, health_results = run_health_check()
    assert all_healthy == False
    assert health_results["sharepoint"]["status"] == "unhealthy"

# Test the simplified interface
@patch("src.utils.health_check.run_health_check")
def test_is_system_ready(mock_run_health_check):
    """Test is_system_ready interface"""
    # Test ready scenario
    mock_run_health_check.return_value = (True, {})
    assert is_system_ready() == True
    
    # Test not ready scenario
    mock_run_health_check.return_value = (False, {})
    assert is_system_ready() == False