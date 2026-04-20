"""LogEntry测试 - datetime模块"""

from datetime import datetime, timedelta

from app.core.log_entry import LogEntry, format_timestamp, is_weekday, parse_timestamp


class TestLogEntry:
    def test_create_log_entry(self):
        entry = LogEntry(
            timestamp=datetime(2024, 4, 20, 10, 30, 0),
            level="INFO",
            message="User logged in",
            source="app.py",
        )
        assert entry.level == "INFO"
        assert entry.message == "User logged in"
        assert entry.source == "app.py"

    def test_log_entry_to_dict(self):
        entry = LogEntry(
            timestamp=datetime(2024, 4, 20, 10, 30, 0),
            level="ERROR",
            message="Connection failed",
        )
        d = entry.to_dict()
        assert d["level"] == "ERROR"
        assert d["message"] == "Connection failed"

    def test_log_entry_from_dict(self):
        d = {
            "timestamp": "2024-04-20T10:30:00",
            "level": "WARN",
            "message": "Low memory",
        }
        entry = LogEntry.from_dict(d)
        assert entry.level == "WARN"
        assert entry.message == "Low memory"

    def test_log_entry_str(self):
        entry = LogEntry(
            timestamp=datetime(2024, 4, 20, 10, 30, 0),
            level="INFO",
            message="Test message",
        )
        s = str(entry)
        assert "INFO" in s
        assert "Test message" in s


class TestParseTimestamp:
    def test_parse_iso_format(self):
        ts = parse_timestamp("2024-04-20T10:30:00")
        assert ts.year == 2024
        assert ts.month == 4
        assert ts.day == 20

    def test_parse_standard_format(self):
        ts = parse_timestamp("2024-04-20 10:30:00")
        assert ts.year == 2024
        assert ts.hour == 10
        assert ts.minute == 30

    def test_parse_custom_format(self):
        ts = parse_timestamp("20/04/2024 10:30", format="%d/%m/%Y %H:%M")
        assert ts.year == 2024
        assert ts.day == 20

    def test_parse_with_milliseconds(self):
        ts = parse_timestamp("2024-04-20 10:30:00.123")
        assert ts.microsecond == 123000


class TestFormatTimestamp:
    def test_format_iso(self):
        ts = datetime(2024, 4, 20, 10, 30, 0)
        formatted = format_timestamp(ts)
        assert formatted == "2024-04-20T10:30:00"

    def test_format_custom(self):
        ts = datetime(2024, 4, 20, 10, 30, 0)
        formatted = format_timestamp(ts, fmt="%Y/%m/%d %H:%M")
        assert formatted == "2024/04/20 10:30"

    def test_format_readable(self):
        ts = datetime(2024, 4, 20, 10, 30, 0)
        formatted = format_timestamp(ts, fmt="%B %d, %Y at %I:%M %p")
        assert "April" in formatted
        assert "2024" in formatted


class TestIsWeekday:
    def test_weekday_true(self):
        ts = datetime(2024, 4, 22)
        assert is_weekday(ts) is True

    def test_weekday_false_saturday(self):
        ts = datetime(2024, 4, 20)
        assert is_weekday(ts) is False

    def test_weekday_false_sunday(self):
        ts = datetime(2024, 4, 21)
        assert is_weekday(ts) is False


class TestTimeDelta:
    def test_time_difference(self):
        entry1 = LogEntry(
            timestamp=datetime(2024, 4, 20, 10, 0, 0), level="INFO", message="Start"
        )
        entry2 = LogEntry(
            timestamp=datetime(2024, 4, 20, 11, 30, 0), level="INFO", message="End"
        )
        diff = entry2.time_since(entry1)
        assert diff == timedelta(hours=1, minutes=30)

    def test_seconds_between(self):
        entry1 = LogEntry(
            timestamp=datetime(2024, 4, 20, 10, 0, 0), level="INFO", message="Start"
        )
        entry2 = LogEntry(
            timestamp=datetime(2024, 4, 20, 10, 0, 45), level="INFO", message="End"
        )
        assert entry2.seconds_since(entry1) == 45
