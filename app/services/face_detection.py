from typing import List, Tuple

import cv2
import numpy as np


class FaceDetector:
    def __init__(self) -> None:
        self._detector = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )
        if self._detector.empty():
            raise RuntimeError("Failed to load Haar cascade for face detection")

    def detect(self, image: np.ndarray) -> List[Tuple[int, int, int, int]]:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = self._detector.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
        boxes: List[Tuple[int, int, int, int]] = []
        for x, y, w, h in faces:
            boxes.append((x, y, x + w, y + h))
        return boxes