"""
constants.py
Contains system constants, enumerations, and static mappings.
"""

# HTTP Status Codes with descriptive names
HTTP_STATUS_CODES = {
    "OK": 200,                     # Success
    "CREATED": 201,                # Resource created
    "NO_CONTENT": 204,             # Success with no content to return
    "MULTI_STATUS": 207,           # Multiple status responses
    "BAD_REQUEST": 400,            # Invalid request syntax
    "UNAUTHORIZED": 401,           # Authentication required
    "FORBIDDEN": 403,              # Authentication provided but not authorized
    "NOT_FOUND": 404,              # Resource not found
    "CONFLICT": 409,               # Request conflicts with current state
    "GONE": 410,                   # Resource permanently removed
    "PRECONDITION_FAILED": 412,    # Precondition in request failed
    "TOO_MANY_REQUESTS": 429,      # Too many requests (rate limiting)
    "INTERNAL_SERVER_ERROR": 500,  # Unexpected server error
    "SERVICE_UNAVAILABLE": 503,    # Server temporarily unavailable
}

# Required services for health checks
REQUIRED_SERVICES = [
    "sharepoint",
    "database",
    "disk_space"
]

# Retry configuration
RETRY_CONFIG = {
    "MAX_RETRIES": 3,
    "BASE_DELAY": 2,  # Base delay in seconds
    "MAX_DELAY": 30   # Maximum delay in seconds
}

# File paths and locations
PATHS = {
    "TEMP_DIR": "tmp",
    "LOG_DIR": "logs",
    "STATE_FILE": "PP_Keywords.json"
}

# SharePoint document library names
DOCUMENT_LIBRARIES = {
    "MASTER_SPREADSHEET": "Documents/Keywords",
    "PAST_PERFORMANCE": "Documents/PastPerformance"
}