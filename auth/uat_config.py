# auth/uat_config.py
import requests
import os
from dotenv import load_dotenv

load_dotenv(override=True)

def create_uat_config(session_token, scopes, config_name, resource_ids=None):
    """
    Creates a UAT configuration. Now accepts scopes, config name, and optional resource_ids.
    Returns a tuple: (success, response_data)
    """
    try:
        with open("keys/public_key.pem") as f:
            public_key = f.read()
    except FileNotFoundError:
        error_msg = "Public key file not found. Did the key generation step fail?"
        return False, {"error": error_msg}

    # Use provided resource_ids or fall back to environment variables
    if resource_ids is None:
        resource_ids = [
            os.getenv("CLOUD_MANAGER_TENANT_ID")
        ]
    
    # Filter out None values
    resource_ids = [rid for rid in resource_ids if rid is not None]

    body = {
        "name": config_name, # Use the name from the UI
        "issuer": os.getenv("JWT_ISSUER"),
        "publicKey": public_key,
        "usernameClaim": "email",
        "resourceIds": resource_ids,  # Use the provided resource_ids
        "scopes": scopes,
        "enabled": True
    }

    headers = {
        "x-tableau-session-token": session_token,
        "Content-Type": "application/json"
    }

    url = os.getenv("CLOUD_MANAGER_UAT_CONFIGS_URL")
    
    try:
        r = requests.post(url, json=body, headers=headers)
        
        response_data = {
            "status_code": r.status_code,
            "request_body_sent": body,
            "response_text": r.text
        }

        if r.status_code == 409: # Conflict - already exists
            response_data["message"] = f"UAT configuration '{config_name}' likely already exists. This is not a fatal error."
            return False, response_data

        r.raise_for_status()
        
        response_data["message"] = f"UAT configuration '{config_name}' created successfully."
        return True, response_data

    except requests.exceptions.HTTPError as e:
        response_data["message"] = f"HTTP Error: {e}"
        return False, response_data
    except requests.exceptions.RequestException as e:
        response_data["message"] = f"Request Exception: {e}"
        return False, response_data