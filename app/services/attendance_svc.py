import json
import os
from datetime import datetime, timezone
from typing import Dict


class AttendanceService:
    def __init__(self, attendance_path: str) -> None:
        self._path = attendance_path
        os.makedirs(os.path.dirname(attendance_path), exist_ok=True)

    def record(self, payload: Dict) -> Dict:
        payload = dict(payload)
        payload["timestamp"] = datetime.now(timezone.utc).isoformat()
        with open(self._path, "a", encoding="utf-8") as handle:
            handle.write(json.dumps(payload, ensure_ascii=False) + "\n")
        return payload