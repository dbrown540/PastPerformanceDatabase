import requests
import os

def get_access_token():
    """Fetches SharePoint access token using client credentials."""
    url = f"https://login.microsoftonline.com/{os.getenv('TENANT_ID')}/oauth2/token"

    payload = {
        "grant_type": "client_credentials",
        "client_id": os.getenv("CLIENT_ID"),
        "client_secret": os.getenv("CLIENT_SECRET"),
        "resource": "https://graph.microsoft.com"
    }

    response = requests.post(url, data=payload)

    if response.status_code == 200:
        return response.json().get("access_token")

    return None  # Fail gracefully if authentication fails
