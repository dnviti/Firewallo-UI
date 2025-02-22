# main.py
import os
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from apps.core import auth, users, api_keys, plugin_loader
from starlette.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key=os.getenv("SECRET_KEY"))

app.mount("/static", StaticFiles(directory="apps/core/static"), name="static")

templates = Jinja2Templates(directory="apps/core/templates")

# Include core routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(api_keys.router)

# Load plugins
plugin_loader.load_plugins(app)

@app.get("/")
async def root():
    return RedirectResponse(url="/dashboard")

@app.get("/dashboard")
async def dashboard(request: Request):
    # Dynamically generate navigation based on loaded plugins
    navigation = [{"name": "Home", "url": "/dashboard"}]
    # You can enhance this to read from plugin manifests
    return templates.TemplateResponse("base.html", {"request": request, "navigation": navigation, "title": "Dashboard"})