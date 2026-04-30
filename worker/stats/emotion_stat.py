from stats.base import BaseStat

EMOTIONS = ["HAPPY", "SAD", "ANGRY", "SURPRISED", "NEUTRAL", "DISGUSTED", "CONFUSED", "CALM"]

class EmotionStat(BaseStat):
    def parse(self, faces: list) -> list[dict]:
        counts = {e: 0 for e in EMOTIONS}
        per_face = []

        for i, face in enumerate(faces):
            if not face.get('Emotions'):
                continue

            dominant = max(face['Emotions'], key=lambda e: e['Confidence'])
            emotion_type = dominant['Type']

            if emotion_type in counts:
                counts[emotion_type] += 1

            # Posición de la cara (BoundingBox normalizado 0-1)
            bb = face.get('BoundingBox', {})
            left = round(bb.get('Left', 0), 2)
            top = round(bb.get('Top', 0), 2)

            per_face.append(
                self._build(
                    f"face_{i+1}_emotion",
                    "json",
                    {
                        "emotion": emotion_type,
                        "confidence": round(dominant['Confidence'], 1),
                        "position": {"left": left, "top": top}
                    }
                )
            )

        # Conteos agregados por emoción
        aggregated = [
            self._build(f"{e.lower()}_count", "int", counts[e])
            for e in EMOTIONS
        ]

        return aggregated + per_face
