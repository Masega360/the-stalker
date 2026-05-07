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
            config=botocore.config.Config(retries={'max_attempts': 3, 'mode': 'adaptive'})
        )
    return _local.client

def call(image, endpoint_name: str) -> dict | None:
    """Returns raw endpoint JSON response or None on error."""
    image_bytes = _to_bytes(image)
    if image_bytes is None:
        return None
    try:
        response = _get_client().invoke_endpoint(
            EndpointName=endpoint_name,
            ContentType="image/jpeg",
            Body=image_bytes
        )
        return json.loads(response['Body'].read())
    except Exception as e:
        print(f"[SAGEMAKER] Error: {e}")
        return None

def _to_bytes(image) -> bytes | None:
    try:
        success, buffer = cv2.imencode('.jpg', image)
        return buffer.tobytes() if success else None
    except Exception:
        return None
