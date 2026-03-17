import logging
from typing import List, Optional

from fastapi import APIRouter, File, Form, UploadFile
from fastapi.responses import JSONResponse

from app.models.schemas import AttendanceResponse, EnrollResponse, IdentifyResponse
from app.services.recognition_svc import DuplicateFaceError, RecognitionService
from app.utils.validation import validate_email, validate_identity_id, validate_text_length

logger = logging.getLogger("app")

router = APIRouter(prefix="/v1", tags=["recognition"])
service = RecognitionService()


def _reject(message: str, *, status_code: int = 400):
    logger.warning(message)
    return JSONResponse(status_code=status_code, content={"error": message})


@router.post("/enroll", response_model=EnrollResponse)
async def enroll(
    identity_id: str = Form(...),
    name: Optional[str] = Form(None),
    department: Optional[str] = Form(None),
    email: Optional[str] = Form(None),
    active: Optional[bool] = Form(True),
    image: Optional[UploadFile] = File(None),
    angle: Optional[str] = Form(None),
    images: Optional[List[UploadFile]] = File(None),
    angles: Optional[List[str]] = Form(None),
):
    err = validate_identity_id(identity_id)
    if err:
        return _reject(err)

    err = validate_text_length("name", name)
    if err:
        return _reject(err)
    err = validate_text_length("department", department)
    if err:
        return _reject(err)
    err = validate_text_length("email", email, max_len=160)
    if err:
        return _reject(err)
    err = validate_email(email)
    if err:
        return _reject(err)

    upload_items: List[tuple[UploadFile, Optional[str]]] = []
    if images:
        if angles and len(angles) != len(images):
            return _reject("angles count must match images count")
        for idx, img in enumerate(images):
            angle_value = angles[idx] if angles and idx < len(angles) else None
            upload_items.append((img, angle_value))
    elif image:
        upload_items.append((image, angle))
    else:
        return _reject("No image provided")

    try:
        return await service.enroll(
            identity_id=identity_id,
            name=name,
            department=department,
            email=email,
            active=active,
            upload_items=upload_items,
        )
    except DuplicateFaceError as exc:
        return JSONResponse(
            status_code=409,
            content={
                "error": "Duplicate face detected",
                "matched_identity": exc.matched_identity,
                "score": exc.score,
            },
        )
    except ValueError as exc:
        logger.exception("Enroll failed: %s", exc)
        return JSONResponse(status_code=400, content={"error": str(exc)})


@router.post("/identify", response_model=IdentifyResponse)
async def identify(image: UploadFile = File(...)):
    if image.content_type and not image.content_type.startswith("image/"):
        return _reject("Invalid file type. Please upload an image.")
    image_bytes = await image.read()
    if not image_bytes:
        return _reject("Empty image payload")
    try:
        return service.identify(image_bytes)
    except ValueError as exc:
        logger.exception("Identify failed: %s", exc)
        return JSONResponse(status_code=400, content={"error": str(exc)})


@router.post("/attendance", response_model=AttendanceResponse)
async def attendance(
    device_id: Optional[str] = Form(None),
    image: UploadFile = File(...),
):
    if image.content_type and not image.content_type.startswith("image/"):
        return _reject("Invalid file type. Please upload an image.")
    image_bytes = await image.read()
    if not image_bytes:
        return _reject("Empty image payload")
    try:
        return service.record_attendance(device_id=device_id, image_bytes=image_bytes)
    except ValueError as exc:
        logger.exception("Attendance failed: %s", exc)
        return JSONResponse(status_code=400, content={"error": str(exc)})
