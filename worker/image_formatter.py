import cv2
import numpy as np
import base64

def format_image(payload: bytes):
    image = _decode(payload)
    if image is None:
        print("[FORMATTER] No se pudo decodificar la imagen")
    return image

def _decode(payload: bytes):
    try:
        decoded = base64.b64decode(payload)
        return _bytes_to_cv2(decoded)
    except Exception:
        pass

    try:
        return _bytes_to_cv2(payload)
    except Exception:
        pass

    return None

def _bytes_to_cv2(data: bytes):
    arr = np.frombuffer(data, np.uint8)
    image = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError("imdecode devolvió None")
    return image