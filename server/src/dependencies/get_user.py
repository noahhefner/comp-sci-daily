from fastapi import Depends
from pydantic import BaseModel

from src.auth import auth0


class User(BaseModel):
    """User information extracted from Auth0 token."""

    id: str
    email: str
    sub: str


async def get_user(
    claims=Depends(auth0.require_auth()),
) -> User:
    """Get user from Auth0 token."""

    user = User(
        id=claims["sub"],
        email="john.doe@email.com",  # FIX
        sub=claims["sub"],
    )
    return user
