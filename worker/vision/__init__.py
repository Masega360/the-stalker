import os
from core.result import Ok, Err
from vision.logger import log_vision

_BACKEND = os.getenv("VISION_BACKEND", "rekognition")

def get_handler():
    """Returns callable handle(image, device_id) -> dict | None"""

    if _BACKEND == "yolo":
        from vision.models import yolo as yolo_model
        from vision.parsers import yolo as yolo_parser
        def handle(image, device_id):
            result = yolo_model.call(image)
            log_vision("yolo", result)
            if result.is_err():
                return None
            parsed = yolo_parser.parse(result.value)
            return parsed.to_pipeline_dict()
        return handle

    if _BACKEND == "sagemaker":
        from vision.models import sagemaker as sm_model
        from vision.parsers import sagemaker as sm_parser
        endpoint = os.getenv("SAGEMAKER_ENDPOINT_NAME")
        def handle(image, device_id):
            result = sm_model.call(image, endpoint)
            log_vision("sagemaker", result)
            if result.is_err():
                return None
            parsed = sm_parser.parse(result.value)
            return parsed.to_pipeline_dict()
        return handle

    if _BACKEND == "collect":
        from vision.collector import collect
        def handle(image, device_id):
            result = collect(image, device_id)
            log_vision("collect", result)
            return None
        return handle

    # default: rekognition
    from vision.models import rekognition as rek_model
    from vision.parsers import rekognition as rek_parser
    def handle(image, device_id):
        result = rek_model.call(image)
        log_vision("rekognition", result)
        if result.is_err():
            return None
        parsed = rek_parser.parse(result.value)
        return parsed.to_pipeline_dict()
    return handle
