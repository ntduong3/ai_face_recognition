import hashlib
import logging
import os
from datetime import datetime
from typing import Optional

import numpy as np
from fastapi import FastAPI, File, Form, UploadFile
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from app.api.users import router as users_router
from app.core.config import settings
from app.core.deps import (
    get_attendance_service,
    get_cache,
    get_embedder,
    get_face_detector,
    get_faiss_index,
    get_identities,
)
from app.core.logging import setup_logging
from app.schemas import AttendanceResponse, EnrollResponse, IdentifyResponse
from app.utils.images import crop_face, decode_image
from app.web.routes import router as dashboard_router

setup_logging()
logger = logging.getLogger("app")

app = FastAPI(title=settings.app_name)
app.mount("/static", StaticFiles(directory="app/web/static"), name="static")
app.mount("/uploads", StaticFiles(directory=settings.uploads_dir), name="uploads")

app.include_router(dashboard_router)
app.include_router(users_router)


@app.middleware("http")
async def log_requests(request, call_next):
    logger.info("%s %s", request.method, request.url.path)
    response = await call_next(request)
    logger.info("%s %s -> %s", request.method, request.url.path, response.status_code)
    return response


def _select_largest_face(boxes):
    if not boxes:
        return None

    def area(box):
        x1, y1, x2, y2 = box
        return (x2 - x1) * (y2 - y1)

    return max(boxes, key=area)


def _hash_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def _find_duplicate_identity(vector: np.ndarray):
    faiss_index = get_faiss_index()
    results = faiss_index.search(vector, top_k=1)
    if not results:
        return None
    identity_id, score = results[0]
    if score >= settings.similarity_threshold:
        return identity_id, score
    return None


def _get_embedding_from_image(image_bytes: bytes) -> np.ndarray:
    cache = get_cache()
    embedder = get_embedder()
    detector = get_face_detector()

    cache_key = f"embed:{_hash_bytes(image_bytes)}"
    cached = cache.get(cache_key)
    if cached is not None:
        return np.array(cached, dtype="float32")

    if not image_bytes:
        raise ValueError("Empty image payload")

    image = decode_image(image_bytes)
    boxes = detector.detect(image)
    box = _select_largest_face(boxes)
    if box is None:
        raise ValueError("No face detected")

    face = crop_face(image, box)
    face = embedder.preprocess(face)
    vector = embedder.embed(face)
    cache.set(cache_key, vector.tolist())
    return vector


def _save_upload(identity_id: str, image: UploadFile) -> str:
    ext = os.path.splitext(image.filename or "")[1] or ".jpg"
    safe_id = identity_id.replace("/", "_").replace("\\", "_")
    ts = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"{safe_id}_{ts}{ext}"
    os.makedirs(settings.uploads_dir, exist_ok=True)
    filepath = os.path.join(settings.uploads_dir, filename)
    with open(filepath, "wb") as handle:
        handle.write(image.file.read())
    return f"/uploads/{filename}"


def _identify_from_bytes(image_bytes: bytes):
    cache = get_cache()
    cache_key = f"match:{_hash_bytes(image_bytes)}"
    cached = cache.get(cache_key)
    if cached is not None:
        return IdentifyResponse(**cached)

    try:
        vector = _get_embedding_from_image(image_bytes)
    except ValueError as exc:
        logger.exception("Identify failed: %s", exc)
        return JSONResponse(status_code=400, content={"error": str(exc)})

    faiss_index = get_faiss_index()
    results = faiss_index.search(vector, top_k=1)

    if not results:
        response = IdentifyResponse(identity_id=None, score=None, matched=False)
        cache.set(cache_key, response.model_dump())
        return response

    identity_id, score = results[0]
    matched = score >= settings.similarity_threshold
    response = IdentifyResponse(
        identity_id=identity_id if matched else None,
        score=score if matched else None,
        matched=matched,
    )
    cache.set(cache_key, response.model_dump())
    return response


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/v1/enroll", response_model=EnrollResponse)
async def enroll(
    identity_id: str = Form(...),
    name: Optional[str] = Form(None),
    department: Optional[str] = Form(None),
    email: Optional[str] = Form(None),
    active: Optional[bool] = Form(True),
    image: UploadFile = File(...),
):
    image_bytes = await image.read()
    try:
        vector = _get_embedding_from_image(image_bytes)
    except ValueError as exc:
        logger.exception("Enroll failed: %s", exc)
        return JSONResponse(status_code=400, content={"error": str(exc)})

    duplicate = _find_duplicate_identity(vector)
    if duplicate is not None:
        matched_id, score = duplicate
        if matched_id != identity_id:
            return JSONResponse(
                status_code=409,
                content={
                    "error": "Duplicate face detected",
                    "matched_identity": matched_id,
                    "score": score,
                },
            )

    faiss_index = get_faiss_index()
    identities = get_identities()

    vector_id = faiss_index.next_vector_id()
    faiss_index.add(vector, identity_id, vector_id)

    image.file.seek(0)
    image_url = _save_upload(identity_id, image)

    existing = identities.get(identity_id) or {}
    identities.upsert(
        identity_id,
        {
            "name": name or existing.get("name", "-"),
            "department": department or existing.get("department", "-"),
            "email": email or existing.get("email", "-"),
            "active": bool(active) if active is not None else existing.get("active", True),
            "image_url": image_url,
        },
    )

    return EnrollResponse(identity_id=identity_id, score=1.0)


@app.post("/v1/identify", response_model=IdentifyResponse)
async def identify(image: UploadFile = File(...)):
    image_bytes = await image.read()
    return _identify_from_bytes(image_bytes)


@app.post("/v1/attendance", response_model=AttendanceResponse)
async def attendance(
    device_id: Optional[str] = Form(None),
    image: UploadFile = File(...),
):
    image_bytes = await image.read()
    match = _identify_from_bytes(image_bytes)

    if isinstance(match, JSONResponse):
        return match

    attendance_service = get_attendance_service()
    payload = {
        "device_id": device_id,
        "identity_id": match.identity_id,
        "score": match.score,
        "matched": match.matched,
    }
    record = attendance_service.record(payload)

    return AttendanceResponse(
        identity_id=match.identity_id,
        score=match.score,
        matched=match.matched,
        timestamp=record["timestamp"],
    )