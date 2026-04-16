import boto3
import cv2
import os

_client = None

def _get_client():
    global _client
    if _client is None:
        _client = boto3.client(
            'rekognition',
            region_name=os.getenv("AWS_REGION"),
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
        )
    return _client

def handle(image):
    image_bytes = _to_bytes(image)
    if image_bytes is None:
        print("[REKOGNITION] No se pudo convertir la imagen")
        return None

    try:
        response = _get_client().detect_faces(
            Image={'Bytes': image_bytes},
            Attributes=['ALL']
        )
        print(f"[REKOGNITION] {len(response['FaceDetails'])} caras detectadas")
        return response

    except Exception as e:
        print(f"[REKOGNITION] Error: {e}")
        return None

def _to_bytes(image) -> bytes | None:
    try:
        success, buffer = cv2.imencode('.jpg', image)
        if not success:
            return None
        return buffer.tobytes()
    except Exception:
        return None