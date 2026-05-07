import cv2
import numpy as np
import base64
from core.result import Ok, Err, Result

def format_image(payload: bytes) -> Result:
    image = _decode(payload)
    if image is None:
        return Err("could not decode image")
    return Ok(image)

def _decode(payload: bytes):
    for attempt in (lambda: _bytes_to_cv2(base64.b64decode(payload)),
                    lambda: _bytes_to_cv2(payload)):
        try:
            return attempt()
        except Exception:
            pass
    return None

def _bytes_to_cv2(data: bytes):
    arr = np.frombuffer(data, np.uint8)
    image = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError("imdecode returned None")
    return image
