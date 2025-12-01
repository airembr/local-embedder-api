import os

from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi import status, HTTPException, Depends

API_TOKEN = os.getenv("API_TOKEN", None)
security = HTTPBearer()

# Dependency that checks the token
async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authorization header"
        )

    token = credentials.credentials
    if token != API_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid token"
        )

    return True