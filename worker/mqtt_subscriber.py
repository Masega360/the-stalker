import paho.mqtt.client as mqtt
import os
from dotenv import load_dotenv

load_dotenv()

def start(on_message_callback):
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print(f"[MQTT] Conectado al broker")
            client.subscribe(os.getenv("MQTT_TOPIC"))
            print(f"[MQTT] Suscripto a {os.getenv('MQTT_TOPIC')}")
        else:
            print(f"[MQTT] Error de conexión, código {rc}")

    def on_message(client, userdata, msg):
        print(f"[MQTT] Mensaje recibido en {msg.topic}")
        on_message_callback(msg.payload)

    def on_disconnect(client, userdata, rc):
        if rc != 0:
            print(f"[MQTT] Desconexión inesperada, código {rc}")

    client = mqtt.Client(client_id=os.getenv("MQTT_CLIENT_ID"))
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect

    client.connect(
        os.getenv("MQTT_HOST"),
        int(os.getenv("MQTT_PORT", 1883))
    )

    client.loop_forever()