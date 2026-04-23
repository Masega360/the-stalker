"""
Script de prueba local para Rekognition + stats pipeline.
Uso: py test_local.py <ruta_imagen>
     py test_local.py  (usa foto.jpeg por defecto)
"""
import sys
import os
import cv2
from dotenv import load_dotenv

# .env está en la misma carpeta que este script (worker/)
env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
load_dotenv(env_path, override=True)

# Debug: verificar que las variables se cargaron
key = os.getenv("AWS_ACCESS_KEY_ID", "NO CARGÓ")
token = os.getenv("AWS_SESSION_TOKEN", "NO CARGÓ")
print(f"[DEBUG] KEY: {key[:15]}...")
print(f"[DEBUG] TOKEN: {token[:20]}...")

from rekognition_handler import handle
from stats.provider import provide

def main():
    image_path = sys.argv[1] if len(sys.argv) > 1 else "foto.jpeg"

    if not os.path.exists(image_path):
        print(f"[ERROR] No se encontró la imagen: {image_path}")
        sys.exit(1)

    print(f"[TEST] Cargando imagen: {image_path}")
    image = cv2.imread(image_path)
    if image is None:
        print("[ERROR] No se pudo leer la imagen con OpenCV")
        sys.exit(1)

    print(f"[TEST] Imagen cargada: {image.shape[1]}x{image.shape[0]} px")
    print("[TEST] Enviando a Rekognition...")

    response = handle(image)
    if response is None:
        print("[ERROR] Rekognition no devolvió respuesta")
        sys.exit(1)

    print(f"\n[RESULTADO] Personas detectadas (incl. espaldas): {response['TotalPersons']}")
    print(f"[RESULTADO] Caras detectadas: {len(response['FaceDetails'])}")

    stats = provide(response, device_id="test-device-01")

    print("\n[STATS]")
    for s in stats:
        print(f"  {s['stat_type']:20s} = {s['value']}")

if __name__ == "__main__":
    main()
