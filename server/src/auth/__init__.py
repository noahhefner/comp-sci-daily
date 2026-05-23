from fastapi_plugin.fast_api_client import Auth0FastAPI
import os
import sys

AUTH0_DOMAIN: str | None = os.getenv("AUTH0_DOMAIN")
if not AUTH0_DOMAIN:
    print("AUTH0_DOMAIN not set.")
    sys.exit(1)

AUTH0_AUDIENCE: str | None = os.getenv("AUTH0_AUDIENCE")
if not AUTH0_AUDIENCE:
    print("AUTH0_AUDIENCE not set.")
    sys.exit(1)

auth0 = Auth0FastAPI(
    domain=AUTH0_DOMAIN,
    audience=AUTH0_AUDIENCE,
)