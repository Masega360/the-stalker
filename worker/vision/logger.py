from result import Ok, Err
from logger import log

def log_vision(backend: str, result: Ok | Err) -> None:
    log(backend.upper(), result)
