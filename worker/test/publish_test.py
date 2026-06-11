import os
import sys
import cv2
import numpy as np
import paho.mqtt.client as mqtt
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

device_id = sys.argv[1] if len(sys.argv) > 1 else "test-device-01"
image_path = sys.argv[2] if len(sys.argv) > 2 else os.path.join(os.path.dirname(__file__), "foto.jpg")

# Leer y comprimir a JPEG <4MB
image = cv2.imread(image_path)
if image is None:
    print(f"[ERROR] No se pudo leer {image_path}")
    sys.exit(1)

quality = 85
while True:
    success, buffer = cv2.imencode('.jpg', image, [cv2.IMWRITE_JPEG_QUALITY, quality])
    payload = buffer.tobytes()
    if len(payload) < 4 * 1024 * 1024 or quality <= 30:
        break
    quality -= 10

topic = f"{device_id}/camera/frame"
print(f"[PUB] Imagen comprimida a {len(payload)/1024:.0f} KB (calidad {quality})")

client = mqtt.Client(client_id="publisher-test")
client.connect(os.getenv("MQTT_HOST"), int(os.getenv("MQTT_PORT", 1883)))
client.loop_start()
result = client.publish(topic, payload, qos=1)
result.wait_for_publish(timeout=10)
client.loop_stop()
client.disconnect()

print(f"[PUB] Enviado a {topic} en {os.getenv('MQTT_HOST')}")
