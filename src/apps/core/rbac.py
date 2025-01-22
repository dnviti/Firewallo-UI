# core/rbac.py
from fastapi import Depends, HTTPException, status
from apps.core.utils import get_current_user

def has_role(required_role: str):
    async def role_checker(current_user: dict = Depends(get_current_user)):
        if required_role not in current_user.get('roles', []):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Operation not permitted",
            )
    return role_checker