import os
import requests
from mqtt.subscriber import publish_relay
from core.logger import log

_CONDITION_OPS = {
    "GT": lambda v, c: v > c,
    "LT": lambda v, c: v < c,
    "EQ": lambda v, c: v == c,
}


def evaluate_rules(stats: list[dict]):
    rules = _fetch_rules()
    if not rules:
        return

    for rule in rules:
        for stat in stats:
            if _matches(rule, stat):
                actuator_id = rule["actuator_device"]["ip"]
                publish_relay(actuator_id, True)
                log("ACTUATOR", f"triggered {actuator_id} by rule {rule['id']}")
                break


def _fetch_rules() -> list[dict]:
    url = os.getenv("NUXT_API_URL")
    key = os.getenv("INTERNAL_API_KEY")
    if not url or not key:
        return []
    try:
        r = requests.get(f"{url}/api/internal/rules", headers={"x-api-key": key}, timeout=3)
        return r.json().get("rules", []) if r.status_code == 200 else []
    except Exception:
        return []


def _matches(rule: dict, stat: dict) -> bool:
    if rule.get("stat_type", {}).get("name") != stat.get("stat_type"):
        return False
    if rule.get("sensor_device_id") != stat.get("device_id"):
        return False
    op = _CONDITION_OPS.get(rule.get("condition"))
    if not op:
        return False
    try:
        return op(float(stat.get("value", 0)), float(rule.get("comparator", 0)))
    except (TypeError, ValueError):
        return False
