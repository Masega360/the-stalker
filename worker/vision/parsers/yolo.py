import os
from vision.result import VisionResult

def parse(boxes, confidence_threshold: float = None) -> VisionResult:
    """PURE: converts YOLO boxes to VisionResult."""
    threshold = confidence_threshold or float(os.getenv("YOLO_CONFIDENCE", 0.3))
    persons = [b for b in boxes if int(b.cls) == 0 and float(b.conf) >= threshold]
    return VisionResult(total_persons=len(persons), face_details=[])
