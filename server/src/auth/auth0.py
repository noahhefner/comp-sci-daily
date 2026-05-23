from functools import lru_cache
from typing import Optional

import httpx
import jwt
from fastapi import HTTPException, status
from jwt import PyJWTError
from jose import jwt as jose_jwt
from jose.exceptions import JWTError as JoseJWTError

from src.config import get_settings


class Auth0Service:
    """Service for Auth0 authentication and token verification."""

    def __init__(self):
        self.settings = get_settings()
        self.domain = self.settings.auth0_domain
        self.client_id = self.settings.auth0_client_id
        self._jwks_cache = None

    async def get_jwks(self) -> dict:
        """Fetch JWKS from Auth0."""
        if self._jwks_cache is None:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"https://{self.domain}/.well-known/jwks.json")
                response.raise_for_status()
                self._jwks_cache = response.json()
        return self._jwks_cache

    def _get_public_key(self, token: str) -> Optional[str]:
        """Extract the public key from JWKS."""
        try:
            header = jwt.get_unverified_header(token)
            kid = header.get("kid")
            
            # Try to get from cache
            if self._jwks_cache:
                jwks = self._jwks_cache
            else:
                # This should be called after get_jwks() is awaited
                return None
            
            for key in jwks.get("keys", []):
                if key.get("kid") == kid:
                    return jwt.algorithms.RSAAlgorithm.from_jwk(key)
        except Exception as e:
            print(f"Error extracting public key: {e}")
        
        return None

    async def verify_token(self, token: str) -> dict:
        """Verify and decode Auth0 token.
        
        Handles both signed JWTs (RS256) and encrypted JWTs (dir + A256GCM).
        """
        try:
            # Get unverified header to check token type
            header = jwt.get_unverified_header(token)
            algorithm = header.get("alg")
            
            # For encrypted tokens (dir), we need to use python-jose
            if algorithm == "dir":
                # For direct encryption, Auth0 uses the client secret
                decoded = jose_jwt.get_unverified_claims(token)
                
                # Verify the token using the client secret
                decoded = jose_jwt.decode(
                    token,
                    key=self.settings.auth0_client_secret,
                    algorithms=["dir"],
                )
                
                return decoded
            
            # For signed tokens (RS256)
            else:
                # Get JWKS
                await self.get_jwks()
                
                # Get the public key
                public_key = self._get_public_key(token)
                if not public_key:
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Invalid token",
                    )
                
                # Verify with JWKS
                decoded = jwt.decode(
                    token,
                    public_key,
                    algorithms=["RS256"],
                    audience=self.client_id,
                    issuer=f"https://{self.domain}/",
                )
                
                return decoded
        
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired",
            )
        except JoseJWTError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )
        except jwt.InvalidTokenError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )
        except Exception as e:
            print(f"Token verification error: {e}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token verification failed",
            )


@lru_cache
def get_auth0_service() -> Auth0Service:
    """Get cached Auth0Service instance."""
    return Auth0Service()
