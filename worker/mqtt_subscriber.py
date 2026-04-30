import paho.mqtt.client as mqtt
import os
from dotenv import load_dotenv

load_dotenv()

_mqtt_client = None

def get_client():
    return _mqtt_client

def start(on_image_callback=None, on_register_callback=None):
    global _mqtt_client

    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print(f"[MQTT] Conectado al broker")
            # Cámaras
            client.subscribe(os.getenv("MQTT_TOPIC"))
            print(f"[MQTT] Suscripto a {os.getenv('MQTT_TOPIC')}")
            # Registro
            client.subscribe("register/cam")
            client.subscribe("register/actor")
            print(f"[MQTT] Suscripto a register/cam y register/actor")
        else:
            print(f"[MQTT] Error de conexión, código {rc}")

    def on_message(client, userdata, msg):
        topic = msg.topic
        payload = msg.payload
        print(f"[MQTT] Mensaje recibido en {topic}")

        if topic == "register/cam":
            device_id = payload.decode("utf-8").strip()
            print(f"[MQTT] Registro de cámara: {device_id}")
            if on_register_callback:
                on_register_callback(device_id, "cam")

        elif topic == "register/actor":
            device_id = payload.decode("utf-8").strip()
            print(f"[MQTT] Registro de actuador: {device_id}")
            if on_register_callback:
                on_register_callback(device_id, "actor")

        elif on_image_callback:
            # Extraer device_id del topic ej: {id}/sensors/cam
            parts = topic.split("/")
            device_id = parts[0] if len(parts) > 1 else "unknown"
            on_image_callback(payload, device_id)

    def on_disconnect(client, userdata, rc):
        if rc != 0:
            print(f"[MQTT] Desconexión inesperada, código {rc}")

    _mqtt_client = mqtt.Client(client_id=os.getenv("MQTT_CLIENT_ID", "python-worker"))
    _mqtt_client.on_connect = on_connect
    _mqtt_client.on_message = on_message
    _mqtt_client.on_disconnect = on_disconnect

    _mqtt_client.connect(
        os.getenv("MQTT_HOST"),
        int(os.getenv("MQTT_PORT", 1883))
    )

    _mqtt_client.loop_forever()


def publish_relay(device_id: str, state: bool):
    """Publica en /{device_id}/actions/relay para actuar el relay."""
    if _mqtt_client is None:
        print("[MQTT] Cliente no inicializado")
        return False
    topic = f"{device_id}/actions/relay"
    payload = "1" if state else "0"
    result = _mqtt_client.publish(topic, payload)
    if result.rc == mqtt.MQTT_ERR_SUCCESS:
        print(f"[MQTT] Relay {device_id} -> {payload}")
        return True
    print(f"[MQTT] Error publicando relay: {result.rc}")
    return False
