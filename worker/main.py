import threading
from flask import Flask, request, jsonify
from mqtt_subscriber import start, publish_relay
from image_formatter import format_image
from preprocessor import preprocess
from stats.provider import provide
from api_sender import send, register_device
import os

app = Flask(__name__)

_VISION_BACKEND = os.getenv("VISION_BACKEND", "rekognition")  # "rekognition" | "sagemaker"

if _VISION_BACKEND == "sagemaker":
    from sagemaker_handler import handle as _handle
    _SAGEMAKER_ENDPOINT = os.getenv("SAGEMAKER_ENDPOINT_NAME")
    def handle(image):
        return _handle(image, _SAGEMAKER_ENDPOINT)
else:
    from rekognition_handler import handle

# --- Callbacks MQTT ---

def on_image(payload, device_id):
    image = format_image(payload)
    if image is None:
        return

    if not preprocess(image):
        return

    response = handle(image)
    if response is None:
        return

    stats = provide(response, device_id)
    if not stats:
        return

    send(stats)

def on_register(device_id, device_type):
    register_device(device_id, device_type)

# --- Endpoint HTTP para Nuxt ---

@app.route("/relay/<device_id>", methods=["POST"])
def relay(device_id):
    api_key = request.headers.get("x-api-key")
    if api_key != os.getenv("INTERNAL_API_KEY"):
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    state = data.get("state", False)  # true = encender, false = apagar

    success = publish_relay(device_id, state)
    if success:
        return jsonify({"ok": True, "device_id": device_id, "state": state}), 200
    return jsonify({"error": "No se pudo publicar en MQTT"}), 500

# --- Entry point ---

if __name__ == "__main__":
    # MQTT en hilo separado
    mqtt_thread = threading.Thread(
        target=start,
        kwargs={"on_image_callback": on_image, "on_register_callback": on_register},
        daemon=True
    )
    mqtt_thread.start()

    # HTTP server para recibir pedidos de Nuxt
    port = int(os.getenv("WORKER_PORT", 5000))
    print(f"[WORKER] HTTP escuchando en puerto {port}")
    app.run(host="0.0.0.0", port=port)
