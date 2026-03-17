import cv2
import numpy as np
from typing import Dict, Tuple


ANGLES = ("front", "left", "right", "up", "down")

ANGLE_ALIASES = {
    "front": "front",
    "forward": "front",
    "straight": "front",
    "left": "left",
    "right": "right",
    "up": "up",
    "down": "down",
    "nhin thang": "front",
    "nhin th?ng": "front",
    "quay trai": "left",
    "quay tr?i": "left",
    "quay phai": "right",
    "quay ph?i": "right",
    "nhin len": "up",
    "nhin l?n": "up",
    "nhin xuong": "down",
    "nhin xu?ng": "down",
}


def normalize_angle(value: str | None) -> str | None:
    if not value:
        return None
    key = value.strip().lower()
    return ANGLE_ALIASES.get(key)


_EYE_CASCADE = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye.xml")


def estimate_pose(image: np.ndarray, box: Tuple[int, int, int, int]) -> Dict[str, float]:
    x1, y1, x2, y2 = box
    face = image[y1:y2, x1:x2]
    if face.size == 0:
        return {"angle": "front", "yaw": 0.0, "pitch": 0.0, "confidence": 0.0}

    gray = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
    if _EYE_CASCADE.empty():
        return {"angle": "front", "yaw": 0.0, "pitch": 0.0, "confidence": 0.1}

    face_h, face_w = gray.shape[:2]
    min_eye = max(12, int(face_w * 0.12))
    eyes = _EYE_CASCADE.detectMultiScale(
        gray, scaleFactor=1.1, minNeighbors=4, minSize=(min_eye, min_eye)
    )
    if len(eyes) == 0:
        return {"angle": "front", "yaw": 0.0, "pitch": 0.0, "confidence": 0.2}

    # Pick two largest eye boxes
    eyes = sorted(eyes, key=lambda e: e[2] * e[3], reverse=True)[:2]
    centers = [(ex + ew / 2, ey + eh / 2, ew, eh) for ex, ey, ew, eh in eyes]

    avg_eye_x = sum(c[0] for c in centers) / len(centers)
    avg_eye_y = sum(c[1] for c in centers) / len(centers)

    x_ratio = (avg_eye_x / face_w) - 0.5
    y_ratio = avg_eye_y / face_h

    # Heuristic thresholds for 5-way bucket (front/left/right/up/down)
    if x_ratio > 0.08:
        angle = "left"
    elif x_ratio < -0.08:
        angle = "right"
    elif y_ratio < 0.32:
        angle = "down"
    elif y_ratio > 0.45:
        angle = "up"
    else:
        angle = "front"

    # Confidence: more eyes detected + clear contrast
    blur_score = cv2.Laplacian(gray, cv2.CV_64F).var()
    blur_conf = min(1.0, blur_score / 150.0)
    base_conf = 0.75 if len(centers) >= 2 else 0.5
    confidence = min(1.0, base_conf * 0.7 + blur_conf * 0.3)

    return {"angle": angle, "yaw": float(x_ratio), "pitch": float(y_ratio), "confidence": float(confidence)}
