# auth/tableau_auth.py
import requests
import os
from dotenv import load_dotenv
from auth.jwt_builder import build_jwt

load_dotenv(override=True)

def login_tableau_cloud(jwt_token=None):
    """
    Logs in to the Tableau REST API using a UAT JWT.
    Can generate its own JWT or use one passed in for testing.
    """
    url = f"{os.getenv('TABLEAU_CLOUD_POD_URL')}/api/3.27/auth/signin"

    # Use the provided token for debugging, or generate a new one
    token_to_use = jwt_token if jwt_token else build_jwt()

    body = {
        "credentials": {
            "jwt": token_to_use,
            "isUat": True,
            "site": {
                "contentUrl": os.getenv("TABLEAU_CLOUD_SITE_ID")
            }
        }
    }

    r = requests.post(url, json=body, headers={"Content-Type": "application/json", "Accept": "application/json"})
    r.raise_for_status()
    return r.json()["credentials"]["token"]