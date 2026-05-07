import paho.mqtt.client as mqtt
import os
from dotenv import load_dotenv

load_dotenv()

_mqtt_client = None

def start(on_image_callback=None, on_register_callback=None):
    global _mqtt_client

    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print(f"[MQTT] Connected to broker")
            client.subscribe("+/camera/frame")
            client.subscribe("+/camera/meta")
            client.subscribe("register/cam")
            client.subscribe("register/actor")
        else:
            print(f"[MQTT] Connection error, code {rc}")

    def on_message(client, userdata, msg):
        topic = msg.topic
        payload = msg.payload

        if topic == "register/cam":
            if on_register_callback:
                on_register_callback(payload.decode("utf-8").strip(), "cam")

        elif topic == "register/actor":
            if on_register_callback:
                on_register_callback(payload.decode("utf-8").strip(), "actor")

        elif topic.endswith("/camera/meta"):
            pass  # metadata logged externally if needed

        elif topic.endswith("/camera/frame") and on_image_callback:
            device_id = topic.split("/")[0]
            on_image_callback(payload, device_id)

    def on_disconnect(client, userdata, rc):
        if rc != 0:
            print(f"[MQTT] Unexpected disconnect, code {rc}")

    _mqtt_client = mqtt.Client(client_id=os.getenv("MQTT_CLIENT_ID", "python-worker"))
    _mqtt_client.on_connect = on_connect
    _mqtt_client.on_message = on_message
    _mqtt_client.on_disconnect = on_disconnect
    _mqtt_client.connect(os.getenv("MQTT_HOST"), int(os.getenv("MQTT_PORT", 1883)))
    _mqtt_client.loop_forever()

def publish_relay(device_id: str, state: bool) -> bool:
    if _mqtt_client is None:
        return False
    result = _mqtt_client.publish(f"{device_id}/actions/relay", "1" if state else "0")
    return result.rc == mqtt.MQTT_ERR_SUCCESS
