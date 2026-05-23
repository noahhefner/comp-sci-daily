from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel

from src.auth.auth0 import get_auth0_service, Auth0Service


class User(BaseModel):
    """User information extracted from Auth0 token."""

    id: str
    email: str
    sub: str


security = HTTPBearer()


async def get_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    auth_service: Annotated[Auth0Service, Depends(get_auth0_service)],
) -> User:
    """Extract and verify user information from Auth0 token.
    
    Requires a Bearer token in the `Authorization` header.
    The token is verified against Auth0's JWKS.
    """
    
    token = credentials.credentials
    
    # Verify token with Auth0
    decoded = await auth_service.verify_token(token)
    
    # Extract user information from token claims
    user_id = decoded.get("sub")
    email = decoded.get("email")
    
    if not user_id or not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token claims",
        )
    
    return User(
        id=user_id,
        email=email,
        sub=user_id,
    )
