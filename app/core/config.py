import os


def _get_env(name: str, default: str) -> str:
    value = os.getenv(name)
    if value is None or value == "":
        return default
    return value


class Settings:
    app_name = _get_env("APP_NAME", "ai_face_recognition")
    host = _get_env("APP_HOST", "0.0.0.0")
    port = int(_get_env("APP_PORT", "8000"))

    # Vector/embedding settings
    vector_dim = int(_get_env("VECTOR_DIM", "512"))
    similarity_threshold = float(_get_env("SIMILARITY_THRESHOLD", "0.35"))

    # Storage paths
    data_dir = _get_env("DATA_DIR", "data")
    identities_path = _get_env("IDENTITIES_PATH", os.path.join(data_dir, "identities.json"))
    attendance_path = _get_env("ATTENDANCE_PATH", os.path.join(data_dir, "attendance.jsonl"))
    faiss_index_path = _get_env("FAISS_INDEX_PATH", os.path.join(data_dir, "faiss.index"))
    faiss_ids_path = _get_env("FAISS_IDS_PATH", os.path.join(data_dir, "faiss_ids.json"))
    uploads_dir = _get_env("UPLOADS_DIR", os.path.join(data_dir, "uploads"))

    # Redis (optional)
    redis_url = _get_env("REDIS_URL", "")
    redis_ttl_seconds = int(_get_env("REDIS_TTL_SECONDS", "300"))


settings = Settings()