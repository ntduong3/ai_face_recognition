import re
from typing import Optional

ID_RE = re.compile(r"^[A-Za-z0-9_-]{2,64}$")
EMAIL_RE = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")


def validate_identity_id(value: Optional[str]) -> Optional[str]:
    if value is None or value.strip() == "":
        return "identity_id is required"
    if not ID_RE.match(value):
        return "identity_id must be 2-64 chars (letters, numbers, _ or -)"
    return None


def validate_email(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    cleaned = value.strip()
    if cleaned in ("", "-"):
        return None
    if not EMAIL_RE.match(cleaned):
        return "email is invalid"
    return None


def validate_text_length(label: str, value: Optional[str], max_len: int = 120) -> Optional[str]:
    if value is None:
        return None
    if len(value) > max_len:
        return f"{label} is too long (max {max_len})"
    return None
