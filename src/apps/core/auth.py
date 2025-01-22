# core/auth.py
from fastapi import APIRouter, Request
from authlib.integrations.starlette_client import OAuth
from starlette.config import Config
from starlette.responses import RedirectResponse
from core.utils import get_current_user

router = APIRouter()
config = Config('.env')
oauth = OAuth(config)

oauth.register(
    name='auth0',
    client_id='YOUR_CLIENT_ID',
    client_secret='YOUR_CLIENT_SECRET',
    server_metadata_url='https://YOUR_DOMAIN/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid profile email',
    },
)

@router.get('/login')
async def login(request: Request):
    redirect_uri = request.url_for('auth')
    return await oauth.auth0.authorize_redirect(request, redirect_uri)

@router.get('/auth')
async def auth(request: Request):
    token = await oauth.auth0.authorize_access_token(request)
    user = token.get('userinfo')
    # Here you would create the user in your db or retrieve it
    request.session['user'] = user
    return RedirectResponse(url='/')

@router.get('/logout')
async def logout(request: Request):
    request.session.pop('user', None)
    return RedirectResponse(url='/')

@router.get('/me')
async def read_users_me(current_user: dict = Depends(get_current_user)):
    return current_user