from core.logger import log

def log_vision(backend: str, result) -> None:
    log(backend.upper(), result)
