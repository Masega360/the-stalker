import requests
import os
from core.result import Ok, Err, Result

_BASE_URL = None
_API_KEY = None

def _setup():
    global _BASE_URL, _API_KEY
    if _BASE_URL is None:
        _BASE_URL = os.getenv("NUXT_API_URL")
        _API_KEY = os.getenv("INTERNAL_API_KEY")

def _headers() -> dict:
    _setup()
    return {"Content-Type": "application/json", "x-api-key": _API_KEY}

def send(stats: list[dict]) -> list[Result]:
    return [_post(stat) for stat in stats]

def register_device(device_id: str, device_type: str) -> Result:
    _setup()
    try:
        response = requests.post(
            f"{_BASE_URL}/api/internal/devices/register",
            json={"device_id": device_id, "type": device_type},
            headers=_headers(),
            timeout=5
        )
        if response.status_code in (200, 201):
            return Ok(f"device {device_id} ({device_type}) registered")
        return Err(f"device {device_id} registration failed: {response.status_code}")
    except Exception as e:
        return Err(f"device {device_id} registration error: {e}")

def _post(stat: dict, retries: int = 3) -> Result:
    last_err = Err(f"{stat['stat_type']} failed after {retries} retries")
    for attempt in range(retries):
        try:
            response = requests.post(
                f"{_BASE_URL}/api/internal/stats",
                json=stat,
                headers=_headers(),
                timeout=5
            )
            if response.status_code == 201:
                return Ok(f"{stat['stat_type']} sent")
            last_err = Err(f"{stat['stat_type']} failed with {response.status_code} (attempt {attempt + 1})")
        except requests.exceptions.Timeout:
            last_err = Err(f"{stat['stat_type']} timeout (attempt {attempt + 1})")
        except requests.exceptions.ConnectionError:
            last_err = Err(f"{stat['stat_type']} no connection (attempt {attempt + 1})")
    return last_err
