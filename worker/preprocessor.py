import cv2
import numpy as np
import os

_last_frame = None

def preprocess(image) -> bool:
    if _is_blurry(image):
        print("[PREPROCESSOR] Imagen borrosa, descartando")
        return False

    if _is_too_dark(image):
        print("[PREPROCESSOR] Imagen muy oscura, descartando")
        return False

    if _is_duplicate(image):
        print("[PREPROCESSOR] Imagen sin cambios, descartando")
        return False

    _update_last_frame(image)
    return True

def _is_blurry(image) -> bool:
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    variance = cv2.Laplacian(gray, cv2.CV_64F).var()
    threshold = float(os.getenv("BLUR_THRESHOLD", 100))
    return variance < threshold

def _is_too_dark(image) -> bool:
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    brightness = np.mean(gray)
    threshold = float(os.getenv("MIN_BRIGHTNESS", 30))
    return brightness < threshold

def _is_duplicate(image) -> bool:
    global _last_frame
    if _last_frame is None:
        return False
    diff = cv2.absdiff(image, _last_frame)
    score = np.mean(diff)
    threshold = float(os.getenv("MIN_DIFF_THRESHOLD", 10))
    return score < threshold

def _update_last_frame(image):
    global _last_frame
    _last_frame = image.copy()