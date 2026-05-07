import os
from vision.logger import log_result

_BACKEND = os.getenv("VISION_BACKEND", "rekognition")

def get_handler():
    """Returns a callable handle(image, device_id) -> dict | None based on VISION_BACKEND."""

    if _BACKEND == "yolo":
        from vision.models import yolo as yolo_model
        from vision.parsers import yolo as yolo_parser
        def handle(image, device_id):
            raw = yolo_model.call(image)
            if raw is None:
                return None
            result = yolo_parser.parse(raw)
            log_result("yolo", result)
            return result.to_pipeline_dict()
        return handle

    if _BACKEND == "sagemaker":
        from vision.models import sagemaker as sm_model
        from vision.parsers import sagemaker as sm_parser
        endpoint = os.getenv("SAGEMAKER_ENDPOINT_NAME")
        def handle(image, device_id):
            raw = sm_model.call(image, endpoint)
            if raw is None:
                return None
            result = sm_parser.parse(raw)
            log_result("sagemaker", result)
            return result.to_pipeline_dict()
        return handle

    if _BACKEND == "collect":
        from vision.collector import collect
        def handle(image, device_id):
            collect(image, device_id)
            return None
        return handle

    # default: rekognition
    from vision.models import rekognition as rek_model
    from vision.parsers import rekognition as rek_parser
    def handle(image, device_id):
        raw = rek_model.call(image)
        if raw is None:
            return None
        result = rek_parser.parse(raw)
        log_result("rekognition", result)
        return result.to_pipeline_dict()
    return handle
