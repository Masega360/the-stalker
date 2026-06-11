from dataclasses import dataclass, field

@dataclass
class VisionResult:
    total_persons: int
    face_details: list = field(default_factory=list)

    def to_pipeline_dict(self) -> dict:
        return {"TotalPersons": self.total_persons, "FaceDetails": self.face_details}
