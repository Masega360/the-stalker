import os

_BACKEND = os.getenv("VISION_BACKEND", "rekognition")

def get_handler():
    """Returns a callable handle(image, device_id) based on VISION_BACKEND."""
    if _BACKEND == "sagemaker":
        from vision.sagemaker import handle as _handle
        endpoint = os.getenv("SAGEMAKER_ENDPOINT_NAME")
        return lambda image, device_id: _handle(image, endpoint)

    if _BACKEND == "collect":
        from vision.collector import collect
        return lambda image, device_id: (collect(image, device_id), None)[1]

    from vision.rekognition import handle
    return lambda image, device_id: handle(image)
