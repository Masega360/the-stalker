import threading
import boto3
import botocore.config
import cv2

MAX_IMAGE_BYTES = 5 * 1024 * 1024

_local = threading.local()

def _get_client():
    if not hasattr(_local, 'client'):
        _local.client = boto3.client(
            'rekognition',
            config=botocore.config.Config(retries={'max_attempts': 3, 'mode': 'adaptive'})
        )
    return _local.client

def call(image) -> dict | None:
    """Returns raw Rekognition response or None on error."""
    image_bytes = _to_bytes(image)
    if image_bytes is None or len(image_bytes) > MAX_IMAGE_BYTES:
        print(f"[REKOGNITION] Image too large or unreadable ({len(image_bytes) if image_bytes else 0} bytes)")
        return None
    try:
        client = _get_client()
        labels = client.detect_labels(Image={'Bytes': image_bytes}, MaxLabels=20, MinConfidence=60)
        faces = client.detect_faces(Image={'Bytes': image_bytes}, Attributes=['ALL'])
        return {"labels": labels, "faces": faces}
    except Exception as e:
        print(f"[REKOGNITION] Error: {e}")
        return None

def _to_bytes(image) -> bytes | None:
    try:
        success, buffer = cv2.imencode('.jpg', image)
        return buffer.tobytes() if success else None
    except Exception:
        return None
