import threading
import json
import boto3
import botocore.config
import cv2

_local = threading.local()

def _get_client():
    if not hasattr(_local, 'client'):
        _local.client = boto3.client(
            'sagemaker-runtime',
            config=botocore.config.Config(
                retries={'max_attempts': 3, 'mode': 'adaptive'}
            )
        )
    return _local.client

def handle(image, endpoint_name: str, confidence_threshold: float = 0.5):
    """
    Calls a SageMaker endpoint with a JPEG image and returns a response
    compatible with the existing stats pipeline.

    Expected endpoint response (JSON):
    {
        "predictions": [
            {"label": "person", "confidence": 0.92, "bbox": [x1, y1, x2, y2]},
            ...
        ]
    }

    Returns:
    {
        "FaceDetails": [],        # SageMaker person detection has no face attributes
        "TotalPersons": <int>
    }
    """
    image_bytes = _to_bytes(image)
    if image_bytes is None:
        print("[SAGEMAKER] No se pudo convertir la imagen")
        return None

    try:
        client = _get_client()
        response = client.invoke_endpoint(
            EndpointName=endpoint_name,
            ContentType="image/jpeg",
            Body=image_bytes
        )
        result = json.loads(response['Body'].read())
        persons = [
            p for p in result.get('predictions', [])
            if p.get('label') == 'person' and p.get('confidence', 0) >= confidence_threshold
        ]
        total = len(persons)
        print(f"[SAGEMAKER] {total} personas detectadas (umbral {confidence_threshold})")
        return {
            'FaceDetails': [],
            'TotalPersons': total
        }

    except Exception as e:
        print(f"[SAGEMAKER] Error: {e}")
        return None

def _to_bytes(image) -> bytes | None:
    try:
        success, buffer = cv2.imencode('.jpg', image)
        if not success:
            return None
        return buffer.tobytes()
    except Exception:
        return None
