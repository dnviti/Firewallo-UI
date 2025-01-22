# plugins/example_plugin/pages/page1.py
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="plugins/example_plugin/templates")

@router.get("/example_plugin/example")
async def example_page(request: Request):
    return templates.TemplateResponse("page1.html", {"request": request, "title": "Example Page"})