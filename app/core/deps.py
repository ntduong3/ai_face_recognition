from typing import Optional

import redis

from app.core.config import settings
from app.repositories.identities import IdentityStore
from app.services.attendance_svc import AttendanceService
from app.services.cache_svc import Cache
from app.services.embedding_svc import ArcFaceEmbedder
from app.services.face_detection_svc import FaceDetector
from app.services.faiss_index_svc import FaissIndex


_face_detector: Optional[FaceDetector] = None
_embedder: Optional[ArcFaceEmbedder] = None
_faiss_index: Optional[FaissIndex] = None
_identities: Optional[IdentityStore] = None
_cache: Optional[Cache] = None
_attendance: Optional[AttendanceService] = None


def get_face_detector() -> FaceDetector:
    global _face_detector
    if _face_detector is None:
        _face_detector = FaceDetector()
    return _face_detector


def get_embedder() -> ArcFaceEmbedder:
    global _embedder
    if _embedder is None:
        _embedder = ArcFaceEmbedder(settings.vector_dim)
    return _embedder


def get_faiss_index() -> FaissIndex:
    global _faiss_index
    if _faiss_index is None:
        _faiss_index = FaissIndex(
            settings.vector_dim, settings.faiss_index_path, settings.faiss_ids_path
        )
    return _faiss_index


def get_identities() -> IdentityStore:
    global _identities
    if _identities is None:
        _identities = IdentityStore(settings.identities_path)
    return _identities


def get_cache() -> Cache:
    global _cache
    if _cache is None:
        client = None
        if settings.redis_url:
            client = redis.Redis.from_url(settings.redis_url, decode_responses=False)
        _cache = Cache(client, settings.redis_ttl_seconds)
    return _cache


def get_attendance_service() -> AttendanceService:
    global _attendance
    if _attendance is None:
        _attendance = AttendanceService(settings.attendance_path)
    return _attendance
