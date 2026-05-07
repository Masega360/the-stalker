from vision.result import VisionResult

def log_result(backend: str, result: VisionResult | None) -> None:
    if result is None:
        print(f"[{backend.upper()}] No result")
        return
    faces = len(result.face_details)
    print(f"[{backend.upper()}] {result.total_persons} persons detected" +
          (f", {faces} faces" if faces else ""))
