from mqtt_subscriber import start
from image_formatter import format_image
from preprocessor import preprocess
from rekognition_handler import handle
from stats.provider import provide
from api_sender import send

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

if __name__ == "__main__":
    start(on_image)