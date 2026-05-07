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

        # 1. Contar personas (funciona de espaldas también)
        resp_labels = client.detect_labels(
            Image={'Bytes': image_bytes},
            MaxLabels=20,
            MinConfidence=60
        )
        total_personas = 0
        for label in resp_labels['Labels']:
            if label['Name'] == 'Person':
                instances = label.get('Instances', [])
                if instances:
                    total_personas = len(instances)

        # 2. Detectar caras con todos los atributos
        resp_faces = client.detect_faces(
            Image={'Bytes': image_bytes},
            Attributes=['ALL']
        )

        # Usar el mayor entre personas por labels y caras detectadas
        total_personas = max(total_personas, len(resp_faces['FaceDetails']))

        print(f"[REKOGNITION] {total_personas} personas detectadas, {len(resp_faces['FaceDetails'])} caras")

        return {
            'FaceDetails': resp_faces['FaceDetails'],
            'TotalPersons': total_personas
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
