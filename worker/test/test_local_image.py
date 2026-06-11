"""
Usage: python test/test_local_image.py [image_path]
Defaults to test/foto.jpg
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from pipeline.formatter import format_image
from vision.models.rekognition import call as rek_call
from vision.parsers.rekognition import parse as rek_parse
from stats.provider import provide
import cv2

image_path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "foto.jpg")

img = cv2.imread(image_path)
if img is None:
    print(f"[ERROR] No se pudo leer {image_path}")
    sys.exit(1)

print(f"[OK] Imagen cargada: {image_path} ({img.shape})")

_, buf = cv2.imencode('.jpg', img)
fmt = format_image(buf.tobytes())
if fmt.is_err():
    print(f"[ERROR] Formatter: {fmt.reason}")
    sys.exit(1)

print("[OK] Formato válido, llamando a Rekognition...")
result = rek_call(fmt.value)
if result.is_err():
    print(f"[ERROR] Rekognition: {result.reason}")
    sys.exit(1)

parsed = rek_parse(result.value)
print(f"[OK] Personas detectadas: {parsed.total_persons}")
print(f"[OK] Caras detectadas: {len(parsed.face_details)}")

stats = provide(parsed.to_pipeline_dict(), "test-device")
print(f"\n{'='*40}")
print(f"STATS ({len(stats)}):")
print(f"{'='*40}")
for s in stats:
    print(f"  {s['stat_type']}: {s['value']}")
