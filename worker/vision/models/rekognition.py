import threading
import boto3
import botocore.config
import cv2
from result import Ok, Err, Result

MAX_IMAGE_BYTES = 5 * 1024 * 1024
_local = threading.local()

def _get_client():
    if not hasattr(_local, 'client'):
        _local.client = boto3.client(
            'rekognition',
            config=botocore.config.Config(retries={'max_attempts': 3, 'mode': 'adaptive'})
        )
    return _local.client

def call(image) -> Result:
    image_bytes = _to_bytes(image)
    if image_bytes is None:
        return Err("could not encode image")
    if len(image_bytes) > MAX_IMAGE_BYTES:
        return Err(f"image too large: {len(image_bytes)} bytes")
    try:
        client = _get_client()
        labels = client.detect_labels(Image={'Bytes': image_bytes}, MaxLabels=20, MinConfidence=60)
        faces = client.detect_faces(Image={'Bytes': image_bytes}, Attributes=['ALL'])
        return Ok({"labels": labels, "faces": faces})
    except Exception as e:
        return Err(f"rekognition error: {e}")

def _to_bytes(image) -> bytes | None:
    try:
        success, buffer = cv2.imencode('.jpg', image)
        return buffer.tobytes() if success else None
    except Exception:
        return None
