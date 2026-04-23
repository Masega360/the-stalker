import uuid
from datetime import datetime, timezone
from stats.people_stat import PeopleStat
from stats.gender_stat import GenderStat
from stats.age_stat import AgeStat
from stats.emotion_stat import EmotionStat

_STATS = [PeopleStat, GenderStat, AgeStat, EmotionStat]

def provide(response: dict, device_id: str) -> list[dict]:
    snapshot_id = str(uuid.uuid4())
    time = datetime.now(timezone.utc).isoformat()
    faces = response.get('FaceDetails', [])
    total_persons = response.get('TotalPersons', len(faces))

    results = []
    for StatClass in _STATS:
        if StatClass is PeopleStat:
            stat = PeopleStat(snapshot_id, device_id, time, total_persons)
        else:
            stat = StatClass(snapshot_id, device_id, time)
        results += stat.parse(faces)
    return results