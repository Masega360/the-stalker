import threading
import boto3
import botocore.config
import cv2
import os
from datetime import datetime, timezone

_local = threading.local()

def _get_client():
    if not hasattr(_local, 'client'):
        _local.client = boto3.client(
            's3',
            config=botocore.config.Config(
                retries={'max_attempts': 3, 'mode': 'adaptive'}
            )
        )
    return _local.client

def collect(image, device_id: str) -> bool:
    """Uploads a JPEG frame to S3 for dataset collection."""
    bucket = os.getenv("S3_DATASET_BUCKET")
    prefix = os.getenv("S3_DATASET_PREFIX", "frames/").rstrip("/")

    if not bucket:
        print("[COLLECTOR] S3_DATASET_BUCKET no configurado")
        return False

    image_bytes = _to_bytes(image)
    if image_bytes is None:
        print("[COLLECTOR] No se pudo convertir la imagen")
        return False

    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%f")
    key = f"{prefix}/{device_id}/{ts}.jpg"

    try:
        _get_client().put_object(
            Bucket=bucket,
            Key=key,
            Body=image_bytes,
            ContentType="image/jpeg"
        )
        print(f"[COLLECTOR] Frame guardado: s3://{bucket}/{key}")
        return True
    except Exception as e:
        print(f"[COLLECTOR] Error subiendo a S3: {e}")
        return False

def _to_bytes(image) -> bytes | None:
    try:
        success, buffer = cv2.imencode('.jpg', image)
        if not success:
            return None
        return buffer.tobytes()
    except Exception:
        return None
