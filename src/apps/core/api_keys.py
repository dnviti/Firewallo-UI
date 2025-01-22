# core/api_keys.py
from fastapi import APIRouter, Depends, HTTPException, status
from src.apps.core.rbac import has_role

router = APIRouter()

# In-memory API keys storage
api_keys_db = {
    "valid_api_key": {"roles": ["admin"]}
}

@router.post('/api-keys', dependencies=[Depends(has_role('admin'))])
async def create_api_key(key: str, roles: list):
    api_keys_db[key] = {"roles": roles}
    return {"msg": "API key created"}

def api_key_auth(api_key: str):
    if api_key not in api_keys_db:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key",
        )
    return api_keys_db[api_key]