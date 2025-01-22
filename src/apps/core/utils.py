# core/utils.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2AuthorizationCodeBearer
from starlette.requests import Request

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl="/login",
    tokenUrl="/token"
)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    # Placeholder function to retrieve current user
    if token != "valid_token":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )
    return {"username": "johndoe", "roles": ["admin"]}