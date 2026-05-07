from stats.base import BaseStat

class PeopleStat(BaseStat):
    def __init__(self, snapshot_id, device_id, time, total_persons: int = 0):
        super().__init__(snapshot_id, device_id, time)
        self.total_persons = total_persons

    def parse(self, faces: list) -> list[dict]:
        return [
            self._build("people_count", "int", self.total_persons)
        ]
