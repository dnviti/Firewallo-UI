# plugins/example_plugin/pages/page1.py
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="apps/firewall/templates")

@router.get("/firewall/rules")
async def rules_list(request: Request):
    pars = {
        "request": request,
        "title": "Firewall Rules"
    }
    return templates.TemplateResponse("rules_list.html", pars)

@router.get("/firewall/rules/{rule_id}")
async def rules_edit(request: Request, rule_id: int):
    pars = {
        "request": request,
        "title": "Firewall Rule " + str(rule_id),
        "id": rule_id
    }
    return templates.TemplateResponse("rules_edit.html", pars)