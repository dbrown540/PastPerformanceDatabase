"""
settings.py
Application settings and environment variables.
"""

import os

# SharePoint Configuration
TENANT_ID = os.getenv("TENANT_ID")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
SHAREPOINT_URL = os.getenv("SHAREPOINT_URL")
SHAREPOINT_SITE = os.getenv("SHAREPOINT_SITE")

# Database Connection
DATABASE_CONNECTION_STRING = os.getenv("DATABASE_CONNECTION_STRING")

# Logging Configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
ENABLE_FILE_LOGGING = True

# Performance Configuration
BATCH_SIZE = int(os.getenv("BATCH_SIZE", "5"))
TIMEOUT_SECONDS = int(os.getenv("TIMEOUT_SECONDS", "300"))
MIN_DISK_SPACE_MB = int(os.getenv("MIN_DISK_SPACE_MB", "100"))

# Feature Flags
ENABLE_METRICS = os.getenv("ENABLE_METRICS", "True").lower() in ("true", "1", "yes")
ENABLE_DOCUMENT_LOCKING = os.getenv("ENABLE_DOCUMENT_LOCKING", "True").lower() in ("true", "1", "yes")