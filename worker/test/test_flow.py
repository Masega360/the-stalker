# test_flow.py
import os
import cv2
import numpy as np
from unittest.mock import patch, MagicMock
from image_formatter import format_image
from preprocessor import preprocess
from rekognition_handler import handle
from stats.provider import provide
from api_sender import send

def make_test_image():
    img_path = os.path.join(os.path.dirname(__file__), 'test_image.jpg')
    with open(img_path, 'rb') as f:
        return f.read()

def test():
    print("\n=== TEST FLOW ===\n")

    # 1. image_formatter
    payload = make_test_image()
    image = format_image(payload)
    assert image is not None, "format_image falló"
    print("[OK] image_formatter")

    # 2. preprocessor
    result = preprocess(image)
    assert result is True, "preprocessor descartó la imagen"
    print("[OK] preprocessor")

    # 3. rekognition — real, sin mock
    response = handle(image)
    assert response is not None, "rekognition_handler falló"
    print("[OK] rekognition_handler")

    # 4. stats provider
    stats = provide(response, "device-uuid-test")
    assert len(stats) > 0, "provider no generó stats"
    print(f"[OK] stats provider — {len(stats)} stats generadas")
    for s in stats:
        print(f"     {s['stat_type']}: {s['value']} ({s['data_type']})")

    # 5. api_sender — mockeado
    with patch('requests.post') as mock_post:
        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_post.return_value = mock_response
        send(stats)
    print(f"[OK] api_sender — {len(stats)} POSTs enviados")

    print("\n=== TODO OK ===\n")

if __name__ == "__main__":
    test()