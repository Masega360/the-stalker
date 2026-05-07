import os
from ultralytics import YOLO
from result import Ok, Err, Result

_model = None

def _get_model():
    global _model
    if _model is None:
        _model = YOLO(os.getenv("YOLO_MODEL_PATH", "yolov8n.pt"))
    return _model

def call(image) -> Result:
    try:
        results = _get_model()(image, verbose=False)
        return Ok(results[0].boxes)
    except Exception as e:
        return Err(f"yolo error: {e}")
