from stats.base import BaseStat

EMOTIONS = ["HAPPY", "SAD", "ANGRY", "SURPRISED", "NEUTRAL", "DISGUSTED", "CONFUSED", "CALM"]

class EmotionStat(BaseStat):
    def parse(self, faces: list) -> list[dict]:
        counts = {e: 0 for e in EMOTIONS}

        for face in faces:
            if not face.get('Emotions'):
                continue
            dominant = max(face['Emotions'], key=lambda e: e['Confidence'])
            if dominant['Type'] in counts:
                counts[dominant['Type']] += 1

        return [
            self._build(f"{e.lower()}_count", "int", counts[e])
            for e in EMOTIONS
        ]