import os
import sys
import paho.mqtt.client as mqtt
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

image_path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "foto.jpg")

with open(image_path, "rb") as f:
    payload = f.read()

client = mqtt.Client(client_id="publisher-test")
client.connect(os.getenv("MQTT_HOST"), int(os.getenv("MQTT_PORT", 1883)))
client.publish(os.getenv("MQTT_TOPIC"), payload)
client.disconnect()

print(f"[PUB] Enviado {len(payload)} bytes a {os.getenv('MQTT_TOPIC')} en {os.getenv('MQTT_HOST')}")
