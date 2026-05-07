import os
from vision.result import VisionResult

def parse(raw: dict, confidence_threshold: float = None) -> VisionResult:
    """PURE: converts SageMaker endpoint response to VisionResult.

    Expected raw format:
    {"predictions": [{"label": "person", "confidence": 0.92, "bbox": [x1,y1,x2,y2]}, ...]}
    """
    threshold = confidence_threshold or float(os.getenv("SAGEMAKER_CONFIDENCE", 0.5))
    persons = [
        p for p in raw.get("predictions", [])
        if p.get("label") == "person" and p.get("confidence", 0) >= threshold
    ]
    return VisionResult(total_persons=len(persons), face_details=[])
