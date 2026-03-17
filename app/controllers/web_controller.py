from datetime import datetime

from fastapi import APIRouter
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.requests import Request

from app.core.deps import get_identities
from app.i18n import TRANSLATIONS

router = APIRouter()

REQUIRED_ANGLES = ["front", "left", "right", "up", "down"]

templates = Jinja2Templates(directory="app/web")


@router.get("/")
async def root():
    return RedirectResponse(url="/dashboard")


@router.get("/dashboard")
async def dashboard(request: Request):
    identities = get_identities()
    users = []
    for identity_id, payload in identities.list_all().items():
        images = payload.get("images") or {}
        front_image = None
        if isinstance(images, dict):
            front = images.get("front") or {}
            front_image = front.get("image_url")

        missing = []
        for angle in REQUIRED_ANGLES:
            entry = (images or {}).get(angle) or {}
            if not entry.get("image_url"):
                missing.append(angle)

        users.append(
            {
                "identity_id": identity_id,
                "name": payload.get("name", "-"),
                "department": payload.get("department", "-"),
                "email": payload.get("email", "-"),
                "active": payload.get("active", True),
                "image_url": front_image or payload.get("image_url"),
                "images": images,
                "missing_angles": missing,
                "images_complete": len(missing) == 0,
            }
        )

    users.sort(key=lambda item: item["identity_id"])

    return templates.TemplateResponse(
        "pages/dashboard.html",
        {
            "request": request,
            "users": users,
            "total_users": len(users),
            "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "translations": TRANSLATIONS,
        },
    )


@router.get("/login")
async def login(request: Request):
    return templates.TemplateResponse(
        "pages/login.html", {"request": request, "translations": TRANSLATIONS}
    )


@router.get("/register")
async def register(request: Request):
    return templates.TemplateResponse(
        "pages/register.html", {"request": request, "translations": TRANSLATIONS}
    )


@router.get("/users/{identity_id}")
async def user_detail(request: Request, identity_id: str):
    identities = get_identities()
    payload = identities.get(identity_id)
    if payload is None:
        return RedirectResponse(url="/dashboard")

    images = payload.get("images") or {}
    angle_cards = []
    for angle in REQUIRED_ANGLES:
        entry = (images or {}).get(angle) or {}
        angle_cards.append(
            {
                "angle": angle,
                "image_url": entry.get("image_url"),
                "updated_at": entry.get("updated_at"),
            }
        )

    missing = [card["angle"] for card in angle_cards if not card.get("image_url")]

    return templates.TemplateResponse(
        "pages/user_detail.html",
        {
            "request": request,
            "user": {
                "identity_id": identity_id,
                "name": payload.get("name", "-"),
                "department": payload.get("department", "-"),
                "email": payload.get("email", "-"),
                "active": payload.get("active", True),
                "image_url": payload.get("image_url"),
            },
            "angle_cards": angle_cards,
            "missing_angles": missing,
            "images_complete": len(missing) == 0,
            "translations": TRANSLATIONS,
        },
    )


@router.get("/i18n.json")
async def i18n_json():
    return TRANSLATIONS
