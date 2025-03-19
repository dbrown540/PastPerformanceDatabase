import sys
import os
# Add the project root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import pytest
from unittest.mock import patch
from src.functions.authentication import get_access_token

# Mocking the requests.post method so we don't actually call SharePoint
@patch("src.functions.authentication.requests.post")
def test_get_access_token(mock_post):
    """Test successful token retrieval"""
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {"access_token": "mock_token"}

    token = get_access_token()
    assert token == "mock_token"

@patch("src.functions.authentication.requests.post")
def test_get_access_token_failure(mock_post):
    """Test failed token retrieval (403 Forbidden)"""
    mock_post.return_value.status_code = 403
    mock_post.return_value.json.return_value = {}

    token = get_access_token()
    assert token is None  # Function should return None if authentication fails