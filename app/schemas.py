from typing import Optional

from pydantic import BaseModel


class EnrollResponse(BaseModel):
    identity_id: str
    score: float


class IdentifyResponse(BaseModel):
    identity_id: Optional[str]
    score: Optional[float]
    matched: bool


class AttendanceResponse(BaseModel):
    identity_id: Optional[str]
    score: Optional[float]
    matched: bool
    timestamp: str