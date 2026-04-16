from stats.base import BaseStat

class GenderStat(BaseStat):
    def parse(self, faces: list) -> list[dict]:
        male = sum(1 for f in faces if f.get('Gender', {}).get('Value') == 'Male')
        female = sum(1 for f in faces if f.get('Gender', {}).get('Value') == 'Female')
        return [
            self._build("male_count", "int", male),
            self._build("female_count", "int", female)
        ]