# Past Performance Database

An Azure Function application that automatically synchronizes Past Performance documents with a master keyword spreadsheet in SharePoint.

## Project Overview

This application runs on a timer trigger and performs the following tasks:
1. Checks if the master keyword spreadsheet has been updated
2. Identifies which documents need updates
3. Downloads, updates, and uploads each document while preserving formatting
4. Tracks document states and implements intelligent retry mechanisms

## Directory Structure

```
PastPerformanceDatabase/
│
├── function_app.py                  # Azure Function entry point 
├── host.json                        # Azure Function host configuration
├── local.settings.json              # Local development settings
│
├── src/                             # Core source code
│   ├── functions/                   # Main function components
│   ├── models/                      # Data models
│   ├── utils/                       # Utility functions
│   └── config/                      # Configuration settings
│
├── tests/                           # Test code
├── scripts/                         # Utility scripts
└── docs/                            # Documentation
```

## Key Components

### Root Directory

- **function_app.py**: Azure Functions entry point that defines the timer trigger and calls into the main processing function
- **host.json**: Configuration for the Azure Functions host
- **local.settings.json**: Local development settings (not committed to source control)
- **requirements.txt**: Python package dependencies

### src/functions/

Contains the main processing logic organized by functional area:

- **main_function.py**: Orchestrates the entire workflow
- **authentication.py**: Handles SharePoint authentication and token management
- **document_processor.py**: Processes individual documents
- **state_manager.py**: Manages the state tracking system
- **metadata_checker.py**: Performs quick metadata checks to avoid unnecessary processing

### src/models/

Contains data structure definitions:

- **document_state.py**: Tracks the state of individual documents
- **processing_result.py**: Captures the results of the processing operation
- **metrics.py**: Tracks performance metrics

### src/utils/

Contains reusable helper functions:

- **sharepoint.py**: SharePoint API interactions
- **excel_handler.py**: Excel file operations with formatting preservation
- **dataframe_tools.py**: Pandas DataFrame utilities
- **hash_calculator.py**: File and data hashing utilities
- **logging_helper.py**: Centralized logging
- **retry_mechanism.py**: Retry logic with exponential backoff
- **file_operations.py**: Temporary file handling

### src/config/

Contains configuration settings:

- **settings.py**: Application settings (connection strings, paths)
- **constants.py**: System constants and enumerations
- **error_codes.py**: Error code definitions

### tests/

Contains test code:

- **unit/**: Unit tests for individual components
- **integration/**: Integration tests that verify cross-component functionality
- **fixtures/**: Test data and mock objects

### scripts/

Contains utility scripts:

- **create_empty_state.py**: Creates initial state file
- **test_sharepoint_access.py**: Validates SharePoint connectivity
- **deploy_function.ps1**: PowerShell deployment script

### docs/

Contains documentation:

- **flowchart.md**: Process flowchart diagram
- **pp_keywords_schema.md**: State file schema documentation
- **sharepoint_api.md**: SharePoint API usage documentation
- **setup.md**: Setup instructions

## State Tracking System

The application uses a JSON state file (`PP_Keywords.json`) to track:

- Hash of the master spreadsheet
- Last successful update timestamp
- Status of each document (success, locked, error)
- Retry attempt counts with exponential backoff

## Getting Started

1. Clone this repository
2. Install dependencies with `pip install -r requirements.txt`
3. Configure SharePoint connection in `local.settings.json`
4. Run locally with `func start`

## Deployment

Deploy to Azure using:

```powershell
./scripts/deploy_function.ps1
```

## Contributing

Follow these steps to contribute:
1. Create a feature branch
2. Make your changes
3. Add tests for new functionality
4. Run the test suite
5. Submit a pull request
