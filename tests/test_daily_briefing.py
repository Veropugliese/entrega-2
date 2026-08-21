import importlib.util
import os
import tempfile
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

    def test_send_email_uses_gmail_smtp(self):
        briefing = {"fecha_briefing": "2026-08-21", "noticias": []}
        with tempfile.TemporaryDirectory() as directory:
            attachment = Path(directory) / "briefing.json"
            attachment.write_text("{}", encoding="utf-8")
            credentials = {
                "EMAIL_USERNAME": "emisor@gmail.com",
                "EMAIL_PASSWORD": "app-password",
                "EMAIL_TO": "destino@example.com",
            }
            with patch.dict(os.environ, credentials), patch.object(daily.smtplib, "SMTP") as smtp:
                daily.send_email(briefing, attachment)

        smtp.assert_called_once_with("smtp.gmail.com", 587, timeout=60)
        server = smtp.return_value.__enter__.return_value
        server.starttls.assert_called_once()
        server.login.assert_called_once_with("emisor@gmail.com", "app-password")
        server.send_message.assert_called_once()


if __name__ == "__main__":
    unittest.main()
