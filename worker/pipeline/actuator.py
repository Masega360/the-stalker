import os
import requests
from mqtt.subscriber import publish_relay
from core.logger import log

_OPERATORS = {
    "greater_than": lambda v, t: v > t,
    "less_than": lambda v, t: v < t,
    "equal": lambda v, t: v == t,
    "greater_equal": lambda v, t: v >= t,
    "less_equal": lambda v, t: v <= t,
}


def evaluate_rules(stats: list[dict]):
    rules = _fetch_rules()
    if not rules:
        return

    for rule in rules:
        for stat in stats:
            if _matches(rule, stat):
                publish_relay(rule["actuator_id"], True)
                log("ACTUATOR", f"triggered {rule['actuator_id']} by rule {rule.get('id', '?')}")
                break


def _fetch_rules() -> list[dict]:
    url = os.getenv("RULES_API_URL")
    if not url:
        return []
    try:
        r = requests.get(url, timeout=3)
        return r.json() if r.status_code == 200 else []
    except Exception:
        return []


def _matches(rule: dict, stat: dict) -> bool:
    if rule.get("stat_type") != stat.get("stat_type"):
        return False
    if rule.get("device_id") != stat.get("device_id"):
        return False
    op = _OPERATORS.get(rule.get("operator"))
    if not op:
        return False
    try:
        return op(float(stat.get("value", 0)), float(rule.get("threshold", 0)))
    except (TypeError, ValueError):
        return False
