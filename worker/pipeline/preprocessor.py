import cv2
import numpy as np
import os
from core.result import Ok, Err, Result

_last_frame = None

def preprocess(image) -> Result:
    if _is_blurry(image):
        return Err("blurry image")
    if _is_too_dark(image):
        return Err("image too dark")
    if _is_duplicate(image):
        return Err("duplicate frame")
    _update_last_frame(image)
    return Ok("frame accepted")

def _is_blurry(image) -> bool:
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return cv2.Laplacian(gray, cv2.CV_64F).var() < float(os.getenv("BLUR_THRESHOLD", 100))

def _is_too_dark(image) -> bool:
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return np.mean(gray) < float(os.getenv("MIN_BRIGHTNESS", 30))

def _is_duplicate(image) -> bool:
    global _last_frame
    if _last_frame is None:
        return False
    return np.mean(cv2.absdiff(image, _last_frame)) < float(os.getenv("MIN_DIFF_THRESHOLD", 10))

def _update_last_frame(image):
    global _last_frame
    _last_frame = image.copy()
