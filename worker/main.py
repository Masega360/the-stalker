import os
import threading
from flask import Flask, request, jsonify
from mqtt_subscriber import start, publish_relay
from image_formatter import format_image
from preprocessor import preprocess
from stats.provider import provide
from api_sender import send, register_device
from vision import get_handler

app = Flask(__name__)
_vision = get_handler()

# --- MQTT callbacks ---

def on_image(payload, device_id):
    image = format_image(payload)
    if image is None:
        return

    if not preprocess(image):
        return

    response = _vision(image, device_id)
    if response is None:
        return

    stats = provide(response, device_id)
    if stats:
        send(stats)

def on_register(device_id, device_type):
    register_device(device_id, device_type)

# --- HTTP endpoint for Nuxt ---

@app.route("/relay/<device_id>", methods=["POST"])
def relay(device_id):
    api_key = request.headers.get("x-api-key")
    if api_key != os.getenv("INTERNAL_API_KEY"):
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    state = data.get("state", False)

    success = publish_relay(device_id, state)
    if success:
        return jsonify({"ok": True, "device_id": device_id, "state": state}), 200
    return jsonify({"error": "No se pudo publicar en MQTT"}), 500

# --- Entry point ---

if __name__ == "__main__":
    mqtt_thread = threading.Thread(
        target=start,
        kwargs={"on_image_callback": on_image, "on_register_callback": on_register},
        daemon=True
    )
    mqtt_thread.start()

    port = int(os.getenv("WORKER_PORT", 5000))
    print(f"[WORKER] HTTP escuchando en puerto {port}")
    app.run(host="0.0.0.0", port=port)
