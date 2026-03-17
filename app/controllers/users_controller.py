from typing import Optional

import logging

from fastapi import APIRouter, Form, HTTPException
from pydantic import BaseModel

from app.core.deps import get_identities
from app.utils.validation import validate_email, validate_identity_id, validate_text_length

logger = logging.getLogger("app")

router = APIRouter(prefix="/ui/users", tags=["ui-users"])


class UserPayload(BaseModel):
    name: Optional[str] = None
    department: Optional[str] = None
    email: Optional[str] = None
    active: Optional[bool] = True


@router.get("/")
async def list_users():
    identities = get_identities()
    return identities.list_all()


@router.post("/")
async def create_user(
    identity_id: str = Form(...),
    name: Optional[str] = Form(None),
    department: Optional[str] = Form(None),
    email: Optional[str] = Form(None),
    active: Optional[bool] = Form(True),
):
    identities = get_identities()
    if identities.get(identity_id) is not None:
        raise HTTPException(status_code=400, detail="identity_id already exists")
    identities.upsert(
        identity_id,
        {
            "name": name or "-",
            "department": department or "-",
            "email": email or "-",
            "active": bool(active),
        },
    )
    return {"status": "ok"}


@router.put("/{identity_id}")
async def update_user(identity_id: str, payload: UserPayload):
    err = validate_identity_id(identity_id)
    if err:
        logger.warning(err)
        raise HTTPException(status_code=400, detail=err)
    err = validate_text_length("name", payload.name)
    if err:
        logger.warning(err)
        raise HTTPException(status_code=400, detail=err)
    err = validate_text_length("department", payload.department)
    if err:
        logger.warning(err)
        raise HTTPException(status_code=400, detail=err)
    err = validate_text_length("email", payload.email, max_len=160)
    if err:
        logger.warning(err)
        raise HTTPException(status_code=400, detail=err)
    err = validate_email(payload.email)
    if err:
        logger.warning(err)
        raise HTTPException(status_code=400, detail=err)

    identities = get_identities()
    existing = identities.get(identity_id)
    if existing is None:
        raise HTTPException(status_code=404, detail="identity_id not found")

    updated = {
        "name": payload.name if payload.name is not None else existing.get("name", "-"),
        "department": payload.department
        if payload.department is not None
        else existing.get("department", "-"),
        "email": payload.email if payload.email is not None else existing.get("email", "-"),
        "active": payload.active if payload.active is not None else existing.get("active", True),
        "image_url": existing.get("image_url"),
        "images": existing.get("images", {}),
    }
    identities.upsert(identity_id, updated)
    return {"status": "ok"}


@router.delete("/{identity_id}")
async def delete_user(identity_id: str):
    identities = get_identities()
    if identities.get(identity_id) is None:
        raise HTTPException(status_code=404, detail="identity_id not found")
    identities.delete(identity_id)
    return {"status": "ok"}
