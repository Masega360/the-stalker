import requests
import os

_BASE_URL = None
_API_KEY = None

def _setup():
    global _BASE_URL, _API_KEY
    if _BASE_URL is None:
        _BASE_URL = os.getenv("NUXT_API_URL")
        _API_KEY = os.getenv("INTERNAL_API_KEY")

def send(stats: list[dict]):
    _setup()
    headers = {
        "Content-Type": "application/json",
        "x-api-key": _API_KEY
    }

    for stat in stats:
        _post(stat, headers)

def register_device(device_id: str, device_type: str):
    """Notifica al back el registro de un nuevo dispositivo."""
    _setup()
    headers = {
        "Content-Type": "application/json",
        "x-api-key": _API_KEY
    }
    payload = {"device_id": device_id, "type": device_type}
    try:
        response = requests.post(
            f"{_BASE_URL}/api/internal/devices/register",
            json=payload,
            headers=headers,
            timeout=5
        )
        if response.status_code in (200, 201):
            print(f"[SENDER] Dispositivo {device_id} ({device_type}) registrado OK")
        else:
            print(f"[SENDER] Error registrando {device_id}: {response.status_code}")
    except Exception as e:
        print(f"[SENDER] Error registrando dispositivo: {e}")

def _post(stat: dict, headers: dict, retries: int = 3):
    for attempt in range(retries):
        try:
            response = requests.post(
                f"{_BASE_URL}/api/internal/stats",
                json=stat,
                headers=headers,
                timeout=5
            )
            if response.status_code == 201:
                print(f"[SENDER] {stat['stat_type']} enviado OK")
                return
            else:
                print(f"[SENDER] Error {response.status_code} en {stat['stat_type']}, intento {attempt + 1}")
        except requests.exceptions.Timeout:
            print(f"[SENDER] Timeout en {stat['stat_type']}, intento {attempt + 1}")
        except requests.exceptions.ConnectionError:
            print(f"[SENDER] Sin conexión, intento {attempt + 1}")

    print(f"[SENDER] Falló {stat['stat_type']} después de {retries} intentos, descartando")