import os
import threading
from flask import Flask, request, jsonify
from mqtt.subscriber import start, publish_relay
from pipeline.formatter import format_image
from pipeline.preprocessor import preprocess
from pipeline.sender import send, register_device
from stats.provider import provide
from vision import get_handler
from core.logger import log

app = Flask(__name__)
_vision = get_handler()

# --- MQTT callbacks ---

def on_image(payload, device_id):
    fmt = format_image(payload)
    log("FORMATTER", fmt)
    if fmt.is_err():
        return

    pre = preprocess(fmt.value)
    log("PREPROCESSOR", pre)
    if pre.is_err():
        return

    response = _vision(fmt.value, device_id)
    if response is None:
        return

    stats = provide(response, device_id)
    if not stats:
        return

    for r in send(stats):
        log("SENDER", r)

def on_register(device_id, device_type):
    log("SENDER", register_device(device_id, device_type))

# --- HTTP endpoint for Nuxt ---

@app.route("/relay/<device_id>", methods=["POST"])
def relay(device_id):
    if request.headers.get("x-api-key") != os.getenv("INTERNAL_API_KEY"):
        return jsonify({"error": "Unauthorized"}), 401
    state = request.get_json().get("state", False)
    if publish_relay(device_id, state):
        return jsonify({"ok": True, "device_id": device_id, "state": state}), 200
    return jsonify({"error": "could not publish to MQTT"}), 500

# --- Entry point ---

if __name__ == "__main__":
    threading.Thread(
        target=start,
        kwargs={"on_image_callback": on_image, "on_register_callback": on_register},
        daemon=True
    ).start()

    port = int(os.getenv("WORKER_PORT", 5000))
    print(f"[WORKER] HTTP listening on port {port}")
    app.run(host="0.0.0.0", port=port)
