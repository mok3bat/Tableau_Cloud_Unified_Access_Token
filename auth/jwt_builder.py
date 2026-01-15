# auth/jwt_builder.py
import jwt
from datetime import datetime, timedelta
import uuid

# In jwt_builder.py, modify the build_jwt function:

def build_jwt(jwt_issuer, jwt_expiration, cm_tenant_id, tc_username, final_scopes):
    with open("keys/private_key.pem", "r") as f:
        private_key = f.read()

    payload = {
                    "iss": jwt_issuer, 
                    "iat": datetime.utcnow(), 
                    "exp": datetime.utcnow() + timedelta(minutes=int(jwt_expiration)),
                    # ❗ REQUIRED by Tableau
                    "https://tableau.com/tenantId": cm_tenant_id,
                    # Must match usernameClaim in UAT config
                    "email": tc_username,
                    # Must be <= scopes in UAT config
                    "scp": final_scopes, 
                    "jti": str(uuid.uuid4())
                }
    headers = {
        "typ": "JWT",
        # required ONLY if using JWKS
        "kid": "kid"
    }

    return jwt.encode(payload, private_key, algorithm="RS256", headers=headers)