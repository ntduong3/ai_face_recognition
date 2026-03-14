import json
import os
from typing import Dict, Optional


class IdentityStore:
    def __init__(self, identities_path: str) -> None:
        self._path = identities_path
        os.makedirs(os.path.dirname(identities_path), exist_ok=True)
        self._data = self._load()

    def _load(self) -> Dict[str, Dict]:
        if not os.path.exists(self._path):
            return {}
        with open(self._path, "r", encoding="utf-8-sig") as handle:
            return json.load(handle)

    def _persist(self) -> None:
        with open(self._path, "w", encoding="utf-8") as handle:
            json.dump(self._data, handle, ensure_ascii=False, indent=2)

    def upsert(self, identity_id: str, payload: Dict) -> None:
        self._data[identity_id] = payload
        self._persist()

    def get(self, identity_id: str) -> Optional[Dict]:
        return self._data.get(identity_id)

    def delete(self, identity_id: str) -> None:
        if identity_id in self._data:
            del self._data[identity_id]
            self._persist()

    def list_all(self) -> Dict[str, Dict]:
        return dict(self._data)