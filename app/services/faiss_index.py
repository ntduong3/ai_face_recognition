import json
import os
from typing import Dict, List, Tuple

import faiss
import numpy as np

from app.utils.images import normalize_l2


class FaissIndex:
    def __init__(self, vector_dim: int, index_path: str, ids_path: str) -> None:
        self.vector_dim = vector_dim
        self.index_path = index_path
        self.ids_path = ids_path
        self._index = self._load_or_create_index()
        self._ids = self._load_ids()

    def _load_or_create_index(self) -> faiss.Index:
        if os.path.exists(self.index_path):
            return faiss.read_index(self.index_path)
        index = faiss.IndexFlatIP(self.vector_dim)
        return faiss.IndexIDMap2(index)

    def _load_ids(self) -> Dict[int, str]:
        if not os.path.exists(self.ids_path):
            return {}
        with open(self.ids_path, "r", encoding="utf-8") as handle:
            data = json.load(handle)
        return {int(k): v for k, v in data.items()}

    def _persist(self) -> None:
        faiss.write_index(self._index, self.index_path)
        with open(self.ids_path, "w", encoding="utf-8") as handle:
            json.dump(self._ids, handle, ensure_ascii=False, indent=2)

    def add(self, vector: np.ndarray, identity_id: str, vector_id: int) -> None:
        vector = normalize_l2(vector).reshape(1, -1).astype("float32")
        self._index.add_with_ids(vector, np.array([vector_id], dtype="int64"))
        self._ids[vector_id] = identity_id
        self._persist()

    def search(self, vector: np.ndarray, top_k: int = 1) -> List[Tuple[str, float]]:
        vector = normalize_l2(vector).reshape(1, -1).astype("float32")
        scores, ids = self._index.search(vector, top_k)
        results: List[Tuple[str, float]] = []
        for idx, score in zip(ids[0], scores[0]):
            if idx == -1:
                continue
            identity_id = self._ids.get(int(idx))
            if identity_id is None:
                continue
            results.append((identity_id, float(score)))
        return results

    def next_vector_id(self) -> int:
        if not self._ids:
            return 1
        return max(self._ids.keys()) + 1