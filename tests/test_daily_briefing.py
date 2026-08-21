import importlib.util
import os
import unittest
from datetime import datetime
from pathlib import Path
from unittest.mock import patch
from zoneinfo import ZoneInfo


MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "daily_briefing.py"
SPEC = importlib.util.spec_from_file_location("daily_briefing", MODULE_PATH)
daily = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(daily)


class DailyBriefingTests(unittest.TestCase):
    def test_strip_json_fence(self):
        self.assertEqual(daily.strip_json_fence("```json\n{\"ok\": true}\n```"), '{"ok": true}')

    def test_schedule_uses_local_hour(self):
        now = datetime(2026, 8, 21, 8, 7, tzinfo=ZoneInfo("America/Argentina/Buenos_Aires"))
        with patch.dict(os.environ, {"DAILY_SEND_HOUR": "8"}):
            self.assertTrue(daily.scheduled_for_this_hour(now))

    def test_validate_rejects_missing_schema(self):
        with self.assertRaises(RuntimeError):
            daily.validate_briefing({"noticias": []})


if __name__ == "__main__":
    unittest.main()
