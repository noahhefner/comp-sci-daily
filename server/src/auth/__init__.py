from fastapi_plugin.fast_api_client import Auth0FastAPI
import os
import sys

AUTH0_DOMAIN: str | None = os.getenv("AUTH0_DOMAIN")
if not AUTH0_DOMAIN:
    print("AUTH0_DOMAIN not set.")
    AUTH0_DOMAIN = "AUTH0_DOMAIN"

AUTH0_AUDIENCE: str | None = os.getenv("AUTH0_AUDIENCE")
if not AUTH0_AUDIENCE:
    print("AUTH0_AUDIENCE not set.")
    AUTH0_AUDIENCE = "AUTH0_AUDIENCE"

auth0 = Auth0FastAPI(
    domain=AUTH0_DOMAIN,
    audience=AUTH0_AUDIENCE,
)