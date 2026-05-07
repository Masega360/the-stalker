from dataclasses import dataclass, field

@dataclass
class VisionResult:
    total_persons: int
    face_details: list = field(default_factory=list)  # raw Rekognition FaceDetails or []

    def to_pipeline_dict(self) -> dict:
        """Format expected by stats/provider.py"""
        return {
            "TotalPersons": self.total_persons,
            "FaceDetails": self.face_details,
        }
