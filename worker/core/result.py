from dataclasses import dataclass
from typing import TypeVar, Generic

T = TypeVar("T")

@dataclass(frozen=True)
class Ok(Generic[T]):
    value: T
    def is_ok(self): return True
    def is_err(self): return False

@dataclass(frozen=True)
class Err:
    reason: str
    def is_ok(self): return False
    def is_err(self): return True

Result = Ok | Err
