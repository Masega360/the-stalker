from stats.base import BaseStat

class AgeStat(BaseStat):
    def parse(self, faces: list) -> list[dict]:
        ages = [
            (f['AgeRange']['Low'] + f['AgeRange']['High']) / 2
            for f in faces if 'AgeRange' in f
        ]
        if not ages:
            return []

        mean = sum(ages) / len(ages)
        std = (sum((a - mean) ** 2 for a in ages) / len(ages)) ** 0.5

        return [
            self._build("age_mean", "float", round(mean, 2)),
            self._build("age_min", "int", int(min(ages))),
            self._build("age_max", "int", int(max(ages))),
            self._build("age_std", "float", round(std, 2))
        ]
