import threading
import boto3
import botocore.config
import cv2
import os

MAX_IMAGE_BYTES = 5 * 1024 * 1024  # 5MB límite de Rekognition

_local = threading.local()

def _get_client():
    if not hasattr(_local, 'client'):
        _local.client = boto3.client(
            'rekognition',
            region_name=os.getenv("AWS_REGION"),
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            aws_session_token=os.getenv("AWS_SESSION_TOKEN"),
            config=botocore.config.Config(
                retries={'max_attempts': 3, 'mode': 'adaptive'}
            )
        )
    return _local.client

def handle(image):
    image_bytes = _to_bytes(image)
    if image_bytes is None:
        print("[REKOGNITION] No se pudo convertir la imagen")
        return None

    if len(image_bytes) > MAX_IMAGE_BYTES:
        print(f"[REKOGNITION] Imagen demasiado grande: {len(image_bytes)} bytes (máx 5MB)")
        return None

    try:
        client = _get_client()

        faces_response = client.detect_faces(
            Image={'Bytes': image_bytes},
            Attributes=['ALL']
        )

        labels_response = client.detect_labels(
            Image={'Bytes': image_bytes},
            MaxLabels=10,
            MinConfidence=80
        )

        total_persons = 0
        for label in labels_response.get('Labels', []):
            if label['Name'] == 'Person':
                total_persons = len(label.get('Instances', []))
                break

        print(f"[REKOGNITION] {total_persons} personas detectadas, {len(faces_response['FaceDetails'])} caras")

        return {
            'FaceDetails': faces_response['FaceDetails'],
            'TotalPersons': total_persons
        }

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
