from vision.result import VisionResult

def parse(raw: dict) -> VisionResult:
    """PURE: converts raw Rekognition response to VisionResult."""
    faces = raw["faces"]["FaceDetails"]
    total_persons = 0
    for label in raw["labels"]["Labels"]:
        if label["Name"] == "Person":
            instances = label.get("Instances", [])
            total_persons = len(instances) if instances else 0
    total_persons = max(total_persons, len(faces))
    return VisionResult(total_persons=total_persons, face_details=faces)
