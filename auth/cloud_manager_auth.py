# auth/cloud_manager_auth.py
import requests
import os
from dotenv import load_dotenv
from auth.jwt_builder import build_jwt

load_dotenv(override=True)

def login_cloud_manager_pat():
    url = os.getenv("CLOUD_MANAGER_PAT_LOGIN_URL")
    body = {"token": os.getenv("CLOUD_MANAGER_PAT_SECRET")}

    r = requests.post(url, json=body)
    r.raise_for_status()
    return r.json()["sessionToken"]


def login_tcm_with_jwt(jwt_token):
    """
    Logs in to the Tableau Cloud Manager API using a PRE-GENERATED UAT JWT.
    This ensures we use the exact same token that was validated in the workflow.
    """
    url = os.getenv("CLOUD_MANAGER_JWT_LOGIN_URL")

    # The request body uses the token passed into the function
    body = {
        "token": jwt_token
    }
    
    # Explicitly setting headers to match the curl command as closely as possible
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    r = requests.post(url, json=body, headers=headers)
    r.raise_for_status()
    return r.json()["sessionToken"]