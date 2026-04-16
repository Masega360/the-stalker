from abc import ABC, abstractmethod

class BaseStat(ABC):
    def __init__(self, snapshot_id: str, device_id: str, time: str):
        self.snapshot_id = snapshot_id
        self.device_id = device_id
        self.time = time

    @abstractmethod
    def parse(self, faces: list) -> list[dict]:
        pass

    def _build(self, stat_type: str, data_type: str, value) -> dict:
        return {
            "snapshot_id": self.snapshot_id,
            "device_id": self.device_id,
            "time": self.time,
            "stat_type": stat_type,
            "data_type": data_type,
            "value": value
        }