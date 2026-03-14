from datetime import datetime

from fastapi import APIRouter
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.requests import Request

from app.core.deps import get_identities

router = APIRouter()

templates = Jinja2Templates(directory="app/web/templates")


@router.get("/")
async def root():
    return RedirectResponse(url="/dashboard")


@router.get("/dashboard")
async def dashboard(request: Request):
    identities = get_identities()
    users = []
    for identity_id, payload in identities.list_all().items():
        users.append(
            {
                "identity_id": identity_id,
                "name": payload.get("name", "-"),
                "department": payload.get("department", "-"),
                "email": payload.get("email", "-"),
                "active": payload.get("active", True),
                "image_url": payload.get("image_url"),
            }
        )

    users.sort(key=lambda item: item["identity_id"])

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "users": users,
            "total_users": len(users),
            "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        },
    )


@router.get("/login")
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.get("/register")
async def register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})
