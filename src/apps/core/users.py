# core/users.py
from fastapi import APIRouter, Depends
from apps.core.rbac import has_role

router = APIRouter()

# In-memory user storage for demonstration
fake_users_db = {}

@router.post('/users', dependencies=[Depends(has_role('admin'))])
async def create_user(user: dict):
    fake_users_db[user['username']] = user
    return {"msg": "User created"}

@router.get('/users', dependencies=[Depends(has_role('admin'))])
async def get_users():
    return fake_users_db