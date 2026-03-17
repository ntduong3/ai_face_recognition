import hashlib
from typing import Optional

import numpy as np

from app.utils.images import normalize_l2, resize_to_square


class ArcFaceEmbedder:
    def __init__(self, vector_dim: int) -> None:
        self.vector_dim = vector_dim

    def embed(self, face_image: np.ndarray, *, seed_bytes: Optional[bytes] = None) -> np.ndarray:
        # Placeholder implementation: deterministic vector derived from image bytes.
        # Replace with real ArcFace inference (e.g., insightface) in production.
        if seed_bytes is None:
            seed_bytes = face_image.tobytes()
        digest = hashlib.sha256(seed_bytes).digest()
        seed = int.from_bytes(digest[:8], "little", signed=False)
        rng = np.random.default_rng(seed)
        vector = rng.standard_normal(self.vector_dim).astype("float32")
        return normalize_l2(vector)

    def preprocess(self, face_image: np.ndarray) -> np.ndarray:
        # ArcFace commonly uses 112x112 input
        return resize_to_square(face_image, 112)