from core.result import Ok, Err

def log(tag: str, result: Ok | Err) -> None:
    if result.is_ok():
        print(f"[{tag}] OK — {result.value}")
    else:
        print(f"[{tag}] ERR — {result.reason}")
