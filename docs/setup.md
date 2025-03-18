# Past Performance Database - Setup Guide

This document provides comprehensive instructions for setting up and configuring the Past Performance Database system.

## Prerequisites

Before you begin, ensure you have:

- Python 3.11 or higher
- Azure CLI (latest version)
- Azure Functions Core Tools v4
- Access to the target SharePoint site with admin privileges
- Permissions to create Azure resources
- Visual Studio Code with the Azure Functions extension (recommended)

## Local Development Environment

### Clone the Repository

```bash
git clone https://your-repository-url/PastPerformanceDatabase.git
cd PastPerformanceDatabase
```

### Create a Virtual Environment

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Local Settings

1. Create a `local.settings.json` file in the root directory:

```json
{
  "IsEncrypted": false,
  "Values": {
    "AzureWebJobsStorage": "UseDevelopmentStorage=true",
    "FUNCTIONS_WORKER_RUNTIME": "python",
    "SHAREPOINT_SITE_URL": "https://your-company.sharepoint.com/sites/PastPerformance",
    "SHAREPOINT_CLIENT_ID": "your-client-id",
    "SHAREPOINT_CLIENT_SECRET": "your-client-secret",
    "SHAREPOINT_TENANT_ID": "your-tenant-id",
    "LOG_FILE_PATH": "/Shared Documents/Logs/pp_update_log.txt",
    "STATE_FILE_PATH": "/Shared Documents/Data/PP_Keywords.json",
    "MASTER_SPREADSHEET_PATH": "/Shared Documents/Master/Keywords_Master.xlsx",
    "MASTER_JSON_PATH": "/Shared Documents/Master/master.json"
  }
}
```

2. Replace the placeholder values with your actual SharePoint and Azure credentials.

## SharePoint Configuration

### Create Required Folder Structure

1. Log in to your SharePoint site
2. Create the following folder structure:
   - `/Shared Documents/Logs/`
   - `/Shared Documents/Data/`
   - `/Shared Documents/Master/`
   - Folders for your past performance documents (as referenced in master.json)

### Create Initial State File

1. Run the utility script to create an initial empty state file:

```bash
python scripts/create_empty_state.py --output PP_Keywords.json
```

2. Upload this file to `/Shared Documents/Data/PP_Keywords.json` in SharePoint

### Create Empty Log File

Create an empty text file and upload it to `/Shared Documents/Logs/pp_update_log.txt`

### Upload Master Spreadsheet

Ensure your master keyword spreadsheet is uploaded to `/Shared Documents/Master/Keywords_Master.xlsx`

### Create Master JSON File

Create a master.json file that maps document identifiers to their SharePoint paths and upload it to `/Shared Documents/Master/master.json`:

```json
{
  "documents": {
    "document1": {
      "path": "/Shared Documents/PastPerformance/document1.xlsx",
      "priority": 1
    },
    "document2": {
      "path": "/Shared Documents/PastPerformance/document2.xlsx",
      "priority": 2
    }
  }
}
```

## Azure AD App Registration

To allow the function to access SharePoint, you need to register an application in Azure AD:

1. Sign in to the [Azure Portal](https://portal.azure.com)
2. Navigate to Azure Active Directory → App registrations → New registration
3. Name the application "PastPerformanceDatabaseApp"
4. Set the redirect URI to "https://login.microsoftonline.com/common/oauth2/nativeclient"
5. Register the application
6. Note the Application (client) ID and Directory (tenant) ID
7. Create a client secret:
   - Navigate to Certificates & secrets → New client secret
   - Add a description and set an expiration period
   - Copy the Value (not the Secret ID) immediately as it won't be shown again
8. Grant API permissions:
   - Navigate to API permissions → Add a permission
   - Select Microsoft Graph → Application permissions
   - Add the following permissions:
     - Files.Read.All
     - Files.ReadWrite.All
     - Sites.Read.All
     - Sites.ReadWrite.All
   - Click "Grant admin consent"

## Local Function Testing

1. Start the Azure Storage Emulator (if using Windows) or Azurite

2. Run the function locally:

```bash
func start
```

3. Verify the function executes correctly

4. Check logs to ensure proper operation

## Azure Deployment

### Create Azure Resources

1. Create a resource group:

```bash
az group create --name PastPerformanceRG --location eastus
```

2. Create a storage account:

```bash
az storage account create --name pastperfstorage --location eastus --resource-group PastPerformanceRG --sku Standard_LRS
```

3. Create a Function App:

```bash
az functionapp create --resource-group PastPerformanceRG --consumption-plan-location eastus --runtime python --runtime-version 3.9 --functions-version 4 --name PP-DocumentSyncUpdater --storage-account pastperfstorage --os-type linux
```

### Configure Function App Settings

```bash
az functionapp config appsettings set --name PP-DocumentSyncUpdater --resource-group PastPerformanceRG --settings "SHAREPOINT_SITE_URL=https://your-company.sharepoint.com/sites/PastPerformance" "SHAREPOINT_CLIENT_ID=your-client-id" "SHAREPOINT_CLIENT_SECRET=your-client-secret" "SHAREPOINT_TENANT_ID=your-tenant-id" "LOG_FILE_PATH=/Shared Documents/Logs/pp_update_log.txt" "STATE_FILE_PATH=/Shared Documents/Data/PP_Keywords.json" "MASTER_SPREADSHEET_PATH=/Shared Documents/Master/Keywords_Master.xlsx" "MASTER_JSON_PATH=/Shared Documents/Master/master.json"
```

### Deploy the Function

Use the provided PowerShell script:

```powershell
./scripts/deploy_function.ps1 -resourceGroup PastPerformanceRG -functionAppName PP-DocumentSyncUpdater
```

Alternatively, deploy directly from Visual Studio Code using the Azure Functions extension.

## Verify Deployment

1. Check the Azure Portal to ensure the function is deployed successfully
2. Monitor the function logs:

```bash
az functionapp log tail --name PP-DocumentSyncUpdater --resource-group PastPerformanceRG
```

3. Wait for the first execution (based on your timer schedule) and check the logs for success
4. Verify updates in SharePoint documents after the function executes

## Troubleshooting

### Authentication Issues

- Verify the client ID, client secret, and tenant ID are correct
- Ensure the Azure AD application has the required permissions
- Check that admin consent has been granted for the permissions

### SharePoint Access Problems

- Verify the SharePoint site URL is correct
- Ensure the paths to documents and folders are correct
- Check that the service principal has sufficient permissions

### Function Execution Issues

- Review the function logs for detailed error messages
- Verify all required files exist in SharePoint
- Check that the master.json file has the correct format
- Ensure the state file is properly formatted

### Common Error Codes

- **503 Service Unavailable**: Issues with SharePoint connectivity or authentication
- **500 Internal Server Error**: Issues with document processing or unexpected errors
- **207 Multi-Status**: Some documents updated successfully, others failed

## Maintenance

### Monitoring

Set up Azure Monitor alerts to notify you of function failures:

```bash
az monitor alert create --name "PP Function Failed" --resource-group PastPerformanceRG --condition "count FunctionExecutionCount >= 1 where Status == 'Failed' and FunctionName == 'PP_DocumentSyncUpdater'" --description "Alerts when the Past Performance function fails" --action-group "/subscriptions/your-subscription-id/resourceGroups/PastPerformanceRG/providers/Microsoft.Insights/actionGroups/YourActionGroup"
```

### Updating the Function

1. Make changes to the code locally
2. Test changes thoroughly
3. Deploy using the same deployment script

## Security Considerations

- Regularly rotate the client secret in Azure AD
- Store secrets in Azure Key Vault for production environments
- Consider using managed identities instead of client secrets
- Review SharePoint permissions to ensure principle of least privilege