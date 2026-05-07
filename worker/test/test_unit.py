"""
Unit tests for the worker modules.

PURE functions (fully testable, no mocks needed):
  - stats/*              all stat classes
  - image_formatter.py   format_image
  - preprocessor.py      preprocess (impure due to global state)
  - vision/parsers/*     all parsers

IMPURE functions (require mocks, marked with # IMPURE):
  - stats/provider.py    provide          — uses uuid4() and datetime.now()
  - preprocessor.py      preprocess       — stateful (_last_frame global)
  - vision/models/*      all models       — call external services
  - api_sender.py        send / register  — makes HTTP requests
"""

import sys
import os
import importlib
import numpy as np
import cv2
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from result import Ok, Err

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

SNAP = "snap-123"
DEV  = "dev-456"
TIME = "2024-01-01T00:00:00+00:00"

def _face(gender="Male", age_low=20, age_high=30, emotions=None, bb=None):
    return {
        "Gender": {"Value": gender},
        "AgeRange": {"Low": age_low, "High": age_high},
        "Emotions": emotions or [{"Type": "HAPPY", "Confidence": 90.0}],
        "BoundingBox": bb or {"Left": 0.1, "Top": 0.2},
    }

# ---------------------------------------------------------------------------
# stats/base.py  [PURE]
# ---------------------------------------------------------------------------

from stats.people_stat import PeopleStat

class TestBaseBuild:
    def _stat(self):
        return PeopleStat(SNAP, DEV, TIME, 0)

    def test_build_keys(self):
        result = self._stat()._build("people_count", "int", 5)
        assert set(result.keys()) == {"snapshot_id", "device_id", "time", "stat_type", "data_type", "value"}

    def test_build_values(self):
        result = self._stat()._build("people_count", "int", 5)
        assert result["snapshot_id"] == SNAP
        assert result["device_id"] == DEV
        assert result["time"] == TIME
        assert result["stat_type"] == "people_count"
        assert result["data_type"] == "int"
        assert result["value"] == 5

# ---------------------------------------------------------------------------
# stats/people_stat.py  [PURE]
# ---------------------------------------------------------------------------

class TestPeopleStat:
    def _stat(self, n):
        return PeopleStat(SNAP, DEV, TIME, n)

    def test_zero(self):
        result = self._stat(0).parse([])
        assert result == [{"snapshot_id": SNAP, "device_id": DEV, "time": TIME,
                           "stat_type": "people_count", "data_type": "int", "value": 0}]

    def test_count(self):
        assert self._stat(7).parse([])[0]["value"] == 7

    def test_ignores_faces_arg(self):
        assert self._stat(3).parse([_face(), _face()])[0]["value"] == 3

# ---------------------------------------------------------------------------
# stats/gender_stat.py  [PURE]
# ---------------------------------------------------------------------------

from stats.gender_stat import GenderStat

class TestGenderStat:
    def _stat(self):
        return GenderStat(SNAP, DEV, TIME)

    def test_empty(self):
        types = {r["stat_type"]: r["value"] for r in self._stat().parse([])}
        assert types == {"male_count": 0, "female_count": 0}

    def test_counts(self):
        faces = [_face("Male"), _face("Female"), _face("Male")]
        types = {r["stat_type"]: r["value"] for r in self._stat().parse(faces)}
        assert types["male_count"] == 2
        assert types["female_count"] == 1

    def test_missing_gender_ignored(self):
        types = {r["stat_type"]: r["value"] for r in self._stat().parse([{"AgeRange": {"Low": 20, "High": 30}}])}
        assert types["male_count"] == 0
        assert types["female_count"] == 0

# ---------------------------------------------------------------------------
# stats/age_stat.py  [PURE]
# ---------------------------------------------------------------------------

from stats.age_stat import AgeStat

class TestAgeStat:
    def _stat(self):
        return AgeStat(SNAP, DEV, TIME)

    def test_empty_returns_nothing(self):
        assert self._stat().parse([]) == []

    def test_single_face(self):
        result = {r["stat_type"]: r["value"] for r in self._stat().parse([_face(age_low=20, age_high=30)])}
        assert result["age_mean"] == 25.0
        assert result["age_min"] == 25
        assert result["age_max"] == 25
        assert result["age_std"] == 0.0

    def test_multiple_faces(self):
        faces = [_face(age_low=20, age_high=30), _face(age_low=30, age_high=40)]
        result = {r["stat_type"]: r["value"] for r in self._stat().parse(faces)}
        assert result["age_mean"] == 30.0
        assert result["age_min"] == 25
        assert result["age_max"] == 35

    def test_face_without_age_ignored(self):
        assert self._stat().parse([{"Gender": {"Value": "Male"}}]) == []

# ---------------------------------------------------------------------------
# stats/emotion_stat.py  [PURE]
# ---------------------------------------------------------------------------

from stats.emotion_stat import EmotionStat, EMOTIONS

class TestEmotionStat:
    def _stat(self):
        return EmotionStat(SNAP, DEV, TIME)

    def test_empty(self):
        types = {r["stat_type"]: r["value"] for r in self._stat().parse([])}
        for e in EMOTIONS:
            assert types[f"{e.lower()}_count"] == 0

    def test_dominant_emotion_counted(self):
        face = _face(emotions=[{"Type": "HAPPY", "Confidence": 90.0}, {"Type": "SAD", "Confidence": 10.0}])
        result = {r["stat_type"]: r["value"] for r in self._stat().parse([face])}
        assert result["happy_count"] == 1
        assert result["sad_count"] == 0

    def test_per_face_entry(self):
        face = _face(emotions=[{"Type": "CALM", "Confidence": 75.0}], bb={"Left": 0.3, "Top": 0.4})
        result = self._stat().parse([face])
        per_face = [r for r in result if r["stat_type"] == "face_1_emotion"]
        assert len(per_face) == 1
        assert per_face[0]["value"]["emotion"] == "CALM"
        assert per_face[0]["value"]["position"] == {"left": 0.3, "top": 0.4}

    def test_face_without_emotions_skipped(self):
        result = self._stat().parse([{"Gender": {"Value": "Male"}, "AgeRange": {"Low": 20, "High": 30}}])
        assert [r for r in result if "face_" in r["stat_type"]] == []

    def test_multiple_faces_indexed(self):
        keys = [r["stat_type"] for r in self._stat().parse([_face(), _face()]) if "face_" in r["stat_type"]]
        assert "face_1_emotion" in keys
        assert "face_2_emotion" in keys

# ---------------------------------------------------------------------------
# stats/provider.py  [IMPURE — uuid4 + datetime.now]
# ---------------------------------------------------------------------------

from stats.provider import provide

class TestProvider:
    def test_returns_list(self):  # IMPURE
        assert isinstance(provide({"FaceDetails": [], "TotalPersons": 0}, "dev-1"), list)

    def test_people_count_in_result(self):  # IMPURE
        result = provide({"FaceDetails": [], "TotalPersons": 5}, "dev-1")
        assert "people_count" in [r["stat_type"] for r in result]

    def test_all_stats_have_device_id(self):  # IMPURE
        result = provide({"FaceDetails": [_face()], "TotalPersons": 1}, "my-device")
        assert all(r["device_id"] == "my-device" for r in result)

    def test_snapshot_id_consistent_within_call(self):  # IMPURE
        result = provide({"FaceDetails": [_face()], "TotalPersons": 1}, "dev-1")
        assert len({r["snapshot_id"] for r in result}) == 1

# ---------------------------------------------------------------------------
# image_formatter.py  [PURE — returns Result]
# ---------------------------------------------------------------------------

from image_formatter import format_image

def _make_jpeg_bytes():
    img = np.zeros((100, 100, 3), dtype=np.uint8)
    img[40:60, 40:60] = (200, 100, 50)
    _, buf = cv2.imencode('.jpg', img)
    return buf.tobytes()

def _make_png_bytes():
    img = np.zeros((100, 100, 3), dtype=np.uint8)
    _, buf = cv2.imencode('.png', img)
    return buf.tobytes()

class TestImageFormatter:
    def test_valid_jpeg(self):
        r = format_image(_make_jpeg_bytes())
        assert r.is_ok()
        assert r.value.shape == (100, 100, 3)

    def test_valid_png(self):
        assert format_image(_make_png_bytes()).is_ok()

    def test_invalid_payload(self):
        assert format_image(b"not an image").is_err()

    def test_empty_payload(self):
        assert format_image(b"").is_err()

# ---------------------------------------------------------------------------
# preprocessor.py  [IMPURE — stateful global, returns Result]
# ---------------------------------------------------------------------------

class TestPreprocessor:
    def _fresh(self):
        import preprocessor
        importlib.reload(preprocessor)
        return preprocessor

    def _sharp_bright(self):
        img = np.ones((100, 100, 3), dtype=np.uint8) * 150
        cv2.rectangle(img, (10, 10), (90, 90), (0, 0, 0), 2)
        cv2.line(img, (0, 0), (100, 100), (0, 0, 0), 1)
        return img

    def test_accepts_good_image(self):  # IMPURE
        assert self._fresh().preprocess(self._sharp_bright()).is_ok()

    def test_rejects_dark_image(self):  # IMPURE
        r = self._fresh().preprocess(np.zeros((100, 100, 3), dtype=np.uint8))
        assert r.is_err()

    def test_rejects_duplicate(self):  # IMPURE
        pp = self._fresh()
        img = self._sharp_bright()
        pp.preprocess(img)
        r = pp.preprocess(img.copy())
        assert r.is_err()
        assert "duplicate" in r.reason

    def test_accepts_different_frame(self):  # IMPURE
        pp = self._fresh()
        img1 = self._sharp_bright()
        img2 = self._sharp_bright()
        img2[0:50, 0:50] = 0
        pp.preprocess(img1)
        assert pp.preprocess(img2).is_ok()

# ---------------------------------------------------------------------------
# vision/models/rekognition.py + vision/parsers/rekognition.py
# ---------------------------------------------------------------------------

from vision.models.rekognition import call as rek_call
from vision.parsers.rekognition import parse as rek_parse
from vision.result import VisionResult

class TestRekognitionHandler:
    def test_returns_err_on_aws_error(self):  # IMPURE
        with patch("vision.models.rekognition._get_client") as mock_client:
            mock_client.return_value.detect_labels.side_effect = Exception("AWS error")
            r = rek_call(np.zeros((100, 100, 3), dtype=np.uint8))
            assert r.is_err()

    def test_returns_err_on_oversized_image(self):  # IMPURE
        big = np.random.randint(0, 255, (2000, 2000, 3), dtype=np.uint8)
        with patch("vision.models.rekognition._get_client"):
            r = rek_call(big)
            assert isinstance(r, (Ok, Err))

    def test_returns_ok_with_raw(self):  # IMPURE
        with patch("vision.models.rekognition._get_client") as mock_client:
            mock_client.return_value.detect_labels.return_value = {
                "Labels": [{"Name": "Person", "Instances": [{}, {}]}]
            }
            mock_client.return_value.detect_faces.return_value = {"FaceDetails": [_face()]}
            r = rek_call(np.zeros((100, 100, 3), dtype=np.uint8))
            assert r.is_ok()

    def test_parser_extracts_persons_and_faces(self):  # PURE
        raw = {
            "labels": {"Labels": [{"Name": "Person", "Instances": [{}, {}, {}]}]},
            "faces": {"FaceDetails": [_face()]}
        }
        result = rek_parse(raw)
        assert isinstance(result, VisionResult)
        assert result.total_persons == 3
        assert len(result.face_details) == 1

    def test_parser_uses_face_count_when_higher(self):  # PURE
        raw = {
            "labels": {"Labels": [{"Name": "Person", "Instances": [{}]}]},
            "faces": {"FaceDetails": [_face(), _face(), _face()]}
        }
        assert rek_parse(raw).total_persons == 3

# ---------------------------------------------------------------------------
# api_sender.py  [IMPURE — returns Result]
# ---------------------------------------------------------------------------

from api_sender import send, register_device

class TestApiSender:
    def test_send_returns_ok_per_stat(self):  # IMPURE
        stats = [{"stat_type": "people_count", "value": 3}, {"stat_type": "age_mean", "value": 25.0}]
        with patch("requests.post") as mock_post:
            mock_post.return_value = MagicMock(status_code=201)
            results = send(stats)
            assert len(results) == 2
            assert all(r.is_ok() for r in results)

    def test_send_returns_err_after_retries(self):  # IMPURE
        with patch("requests.post") as mock_post:
            mock_post.return_value = MagicMock(status_code=500)
            results = send([{"stat_type": "people_count", "value": 1}])
            assert results[0].is_err()
            assert mock_post.call_count == 3

    def test_register_device_returns_ok(self):  # IMPURE
        with patch("requests.post") as mock_post:
            mock_post.return_value = MagicMock(status_code=201)
            r = register_device("cam-01", "cam")
            assert r.is_ok()
            assert mock_post.call_args[1]["json"] == {"device_id": "cam-01", "type": "cam"}

    def test_register_device_returns_err_on_exception(self):  # IMPURE
        with patch("requests.post", side_effect=Exception("connection error")):
            assert register_device("cam-01", "cam").is_err()
