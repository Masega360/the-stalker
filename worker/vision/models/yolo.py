import os
from ultralytics import YOLO

_model = None

def _get_model():
    global _model
    if _model is None:
        _model = YOLO(os.getenv("YOLO_MODEL_PATH", "yolov8n.pt"))
    return _model

def call(image) -> list | None:
    """Returns list of ultralytics Boxes or None on error."""
    try:
        results = _get_model()(image, verbose=False)
        return results[0].boxes
    except Exception as e:
        print(f"[YOLO] Error: {e}")
        return None
