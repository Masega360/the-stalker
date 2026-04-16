from stats.base import BaseStat

class PeopleStat(BaseStat):
    def parse(self, faces: list) -> list[dict]:
        return [
            self._build("people_count", "int", len(faces))
        ]