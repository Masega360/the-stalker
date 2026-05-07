from ultralytics import YOLO
import os

_model = None

def _get_model():
    global _model
    if _model is None:
        model_path = os.getenv("YOLO_MODEL_PATH", "yolov8n.pt")
        _model = YOLO(model_path)
    return _model

def handle(image, confidence_threshold: float = None):
    threshold = confidence_threshold or float(os.getenv("YOLO_CONFIDENCE", 0.4))
    try:
        results = _get_model()(image, verbose=False)
        persons = [b for b in results[0].boxes if int(b.cls) == 0 and float(b.conf) >= threshold]
        print(f"[YOLO] {len(persons)} personas detectadas (umbral {threshold})")
        return {
            "FaceDetails": [],
            "TotalPersons": len(persons)
        }
    except Exception as e:
        print(f"[YOLO] Error: {e}")
        return None
