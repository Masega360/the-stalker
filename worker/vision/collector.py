import threading
import boto3
import botocore.config
import cv2
import os
from datetime import datetime, timezone
from core.result import Ok, Err, Result

_local = threading.local()

def _get_client():
    if not hasattr(_local, 'client'):
        _local.client = boto3.client(
            's3',
            config=botocore.config.Config(retries={'max_attempts': 3, 'mode': 'adaptive'})
        )
    return _local.client

def collect(image, device_id: str) -> Result:
    bucket = os.getenv("S3_DATASET_BUCKET")
    if not bucket:
        return Err("S3_DATASET_BUCKET not configured")

    image_bytes = _to_bytes(image)
    if image_bytes is None:
        return Err("could not encode image")

    prefix = os.getenv("S3_DATASET_PREFIX", "frames").rstrip("/")
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%f")
    key = f"{prefix}/{device_id}/{ts}.jpg"

    try:
        _get_client().put_object(Bucket=bucket, Key=key, Body=image_bytes, ContentType="image/jpeg")
        return Ok(f"s3://{bucket}/{key}")
    except Exception as e:
        return Err(f"s3 upload error: {e}")

def _to_bytes(image) -> bytes | None:
    try:
        success, buffer = cv2.imencode('.jpg', image)
        return buffer.tobytes() if success else None
    except Exception:
        return None
