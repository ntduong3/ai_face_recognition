import hashlib
import logging
import os
from datetime import datetime
from typing import List, Optional

import numpy as np
from fastapi import UploadFile

from app.core.config import settings
from app.core.deps import (
    get_attendance_service,
    get_cache,
    get_embedder,
    get_face_detector,
    get_faiss_index,
    get_identities,
)
from app.models.schemas import AttendanceResponse, EnrollResponse, IdentifyResponse
from app.utils.images import crop_face, decode_image
from app.utils.pose import ANGLES, estimate_pose, normalize_angle

logger = logging.getLogger("app")


class DuplicateFaceError(Exception):
    def __init__(self, matched_identity: str, score: float) -> None:
        super().__init__("Duplicate face detected")
        self.matched_identity = matched_identity
        self.score = score


class RecognitionService:
    def __init__(self) -> None:
        self._cache = get_cache()
        self._embedder = get_embedder()
        self._detector = get_face_detector()
        self._faiss_index = get_faiss_index()
        self._identities = get_identities()
        self._attendance = get_attendance_service()

    def _select_largest_face(self, boxes):
        if not boxes:
            return None

        def area(box):
            x1, y1, x2, y2 = box
            return (x2 - x1) * (y2 - y1)

        return max(boxes, key=area)

    def _hash_bytes(self, payload: bytes) -> str:
        return hashlib.sha256(payload).hexdigest()

    def _pose_penalty(self, angle: str, confidence: float) -> float:
        penalty = 0.0
        if angle in ("left", "right"):
            penalty += settings.pose_penalty_side
        elif angle in ("up", "down"):
            penalty += settings.pose_penalty_vertical
        if confidence < settings.pose_confidence_threshold:
            penalty += settings.pose_penalty_low_confidence
        return penalty

    def _get_embedding_from_image(self, image_bytes: bytes, *, include_meta: bool = False):
        if not image_bytes:
            raise ValueError("Empty image payload")

        image = decode_image(image_bytes)
        boxes = self._detector.detect(image)
        box = self._select_largest_face(boxes)
        if box is None:
            raise ValueError("No face detected")

        cache_key = f"embed:{self._hash_bytes(image_bytes)}"
        cached = self._cache.get(cache_key)
        if cached is not None:
            vector = np.array(cached, dtype="float32")
        else:
            face = crop_face(image, box)
            face = self._embedder.preprocess(face)
            vector = self._embedder.embed(face)
            self._cache.set(cache_key, vector.tolist())

        if include_meta:
            return vector, image, box
        return vector

    def _find_duplicate_identity(self, vector: np.ndarray):
        results = self._faiss_index.search(vector, top_k=1)
        if not results:
            return None
        identity_id, score = results[0]
        if score >= settings.similarity_threshold:
            return identity_id, score
        return None

    def _save_upload(self, identity_id: str, image: UploadFile, angle: str = "front") -> str:
        ext = os.path.splitext(image.filename or "")[1] or ".jpg"
        safe_id = identity_id.replace("/", "_").replace("\\", "_")
        safe_angle = angle.replace("/", "_").replace("\\", "_")
        ts = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"{safe_id}_{safe_angle}_{ts}{ext}"
        os.makedirs(settings.uploads_dir, exist_ok=True)
        filepath = os.path.join(settings.uploads_dir, filename)
        with open(filepath, "wb") as handle:
            handle.write(image.file.read())
        return f"/uploads/{filename}"

    def identify(self, image_bytes: bytes) -> IdentifyResponse:
        cache_key = f"match:{self._hash_bytes(image_bytes)}"
        cached = self._cache.get(cache_key)
        if cached is not None:
            return IdentifyResponse(**cached)

        vector, image, box = self._get_embedding_from_image(image_bytes, include_meta=True)

        pose = estimate_pose(image, box)
        penalty = self._pose_penalty(pose["angle"], pose["confidence"])
        threshold = settings.similarity_threshold + penalty

        def pick_best(candidates, allowed_angles):
            best = None
            for identity_id, score, meta in candidates:
                angle = (meta or {}).get("angle", "front")
                if angle not in allowed_angles:
                    continue
                if best is None or score > best["score"]:
                    best = {"identity_id": identity_id, "score": score, "angle": angle}
            return best

        front_candidates = self._faiss_index.search_with_meta(vector, top_k=settings.front_search_k)
        front_best = pick_best(front_candidates, {"front"})
        if front_best and front_best["score"] >= threshold:
            logger.info(
                "Pose %s conf=%.2f matched=front score=%.3f threshold=%.3f",
                pose["angle"],
                pose["confidence"],
                front_best["score"],
                threshold,
            )
            response = IdentifyResponse(
                identity_id=front_best["identity_id"],
                score=front_best["score"],
                matched=True,
            )
            self._cache.set(cache_key, response.model_dump())
            return response

        side_candidates = self._faiss_index.search_with_meta(vector, top_k=settings.side_search_k)
        side_best = pick_best(side_candidates, {"left", "right", "up", "down"})
        if side_best and side_best["score"] >= threshold:
            logger.info(
                "Pose %s conf=%.2f matched=%s score=%.3f threshold=%.3f",
                pose["angle"],
                pose["confidence"],
                side_best["angle"],
                side_best["score"],
                threshold,
            )
            response = IdentifyResponse(
                identity_id=side_best["identity_id"],
                score=side_best["score"],
                matched=True,
            )
            self._cache.set(cache_key, response.model_dump())
            return response

        response = IdentifyResponse(identity_id=None, score=None, matched=False)
        self._cache.set(cache_key, response.model_dump())
        return response

    async def enroll(
        self,
        *,
        identity_id: str,
        name: Optional[str],
        department: Optional[str],
        email: Optional[str],
        active: Optional[bool],
        upload_items: List[tuple[UploadFile, Optional[str]]],
    ) -> EnrollResponse:
        prepared = []
        for img, angle_value in upload_items:
            if img.content_type and not img.content_type.startswith("image/"):
                raise ValueError("Invalid file type. Please upload an image.")
            image_bytes = await img.read()
            if not image_bytes:
                raise ValueError("Empty image payload")

            vector, image_np, box = self._get_embedding_from_image(image_bytes, include_meta=True)

            pose = estimate_pose(image_np, box)
            normalized_angle = normalize_angle(angle_value) or pose["angle"]
            if normalized_angle not in ANGLES:
                normalized_angle = "front"

            duplicate = self._find_duplicate_identity(vector)
            if duplicate is not None:
                matched_id, score = duplicate
                if matched_id != identity_id:
                    raise DuplicateFaceError(matched_id, score)

            prepared.append(
                {
                    "image": img,
                    "vector": vector,
                    "angle": normalized_angle,
                }
            )

        existing = self._identities.get(identity_id) or {}
        images_map = dict(existing.get("images") or {})

        for item in prepared:
            angle_key = item["angle"]
            existing_entry = images_map.get(angle_key) or {}
            existing_vector_id = existing_entry.get("vector_id")
            if existing_vector_id:
                self._faiss_index.remove(existing_vector_id)

            vector_id = self._faiss_index.next_vector_id()
            self._faiss_index.add(item["vector"], identity_id, vector_id, angle=angle_key)

            item["image"].file.seek(0)
            image_url = self._save_upload(identity_id, item["image"], angle=angle_key)
            images_map[angle_key] = {
                "image_url": image_url,
                "vector_id": vector_id,
                "updated_at": datetime.now().isoformat(),
            }
            if angle_key == "front":
                existing["image_url"] = image_url

        self._identities.upsert(
            identity_id,
            {
                "name": name or existing.get("name", "-"),
                "department": department or existing.get("department", "-"),
                "email": email or existing.get("email", "-"),
                "active": bool(active) if active is not None else existing.get("active", True),
                "image_url": existing.get("image_url"),
                "images": images_map,
            },
        )

        return EnrollResponse(identity_id=identity_id, score=1.0)

    def record_attendance(self, *, device_id: Optional[str], image_bytes: bytes) -> AttendanceResponse:
        match = self.identify(image_bytes)

        record = self._attendance.record(
            {
                "device_id": device_id,
                "identity_id": match.identity_id,
                "score": match.score,
                "matched": match.matched,
            }
        )

        return AttendanceResponse(
            identity_id=match.identity_id,
            score=match.score,
            matched=match.matched,
            timestamp=record["timestamp"],
        )
