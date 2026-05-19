"""LogFilter测试 - 时间过滤和级别过滤"""

from datetime import datetime

from app.core.log_entry import LogEntry
from app.core.log_filter import (
    LogFilter,
    filter_by_level,
    filter_by_pattern,
    filter_by_time_range,
    filter_by_weekday,
)


class TestLogFilter:
    def test_create_filter(self):
        filter_obj = LogFilter()
        assert filter_obj is not None

    def test_filter_by_time_range(self):
        entries = [
            LogEntry(datetime(2024, 4, 20, 10, 0), "INFO", "msg1"),
            LogEntry(datetime(2024, 4, 20, 12, 0), "INFO", "msg2"),
            LogEntry(datetime(2024, 4, 20, 14, 0), "INFO", "msg3"),
        ]
        filter_obj = LogFilter()
        filtered = filter_obj.filter_by_time_range(
            entries,
            start=datetime(2024, 4, 20, 11, 0),
            end=datetime(2024, 4, 20, 13, 0),
        )
        assert len(filtered) == 1
        assert filtered[0].message == "msg2"

    def test_filter_by_level(self):
        entries = [
            LogEntry(datetime(2024, 4, 20, 10, 0), "INFO", "msg1"),
            LogEntry(datetime(2024, 4, 20, 11, 0), "ERROR", "msg2"),
            LogEntry(datetime(2024, 4, 20, 12, 0), "WARN", "msg3"),
        ]
        filter_obj = LogFilter()
        filtered = filter_obj.filter_by_level(entries, levels=["ERROR", "WARN"])
        assert len(filtered) == 2

    def test_filter_by_weekday(self):
        entries = [
            LogEntry(datetime(2024, 4, 22, 10, 0), "INFO", "Monday"),
            LogEntry(datetime(2024, 4, 20, 10, 0), "INFO", "Saturday"),
            LogEntry(datetime(2024, 4, 21, 10, 0), "INFO", "Sunday"),
        ]
        filter_obj = LogFilter()
        filtered = filter_obj.filter_by_weekday(entries, weekdays_only=True)
        assert len(filtered) == 1
        assert filtered[0].message == "Monday"

    def test_filter_by_weekday_weekend(self):
        entries = [
            LogEntry(datetime(2024, 4, 22, 10, 0), "INFO", "Monday"),
            LogEntry(datetime(2024, 4, 20, 10, 0), "INFO", "Saturday"),
            LogEntry(datetime(2024, 4, 21, 10, 0), "INFO", "Sunday"),
        ]
        filter_obj = LogFilter()
        filtered = filter_obj.filter_by_weekday(entries, weekdays_only=False)
        assert len(filtered) == 2

    def test_filter_by_pattern(self):
        entries = [
            LogEntry(datetime(2024, 4, 20, 10, 0), "INFO", "User logged in"),
            LogEntry(datetime(2024, 4, 20, 11, 0), "ERROR", "Connection failed"),
            LogEntry(datetime(2024, 4, 20, 12, 0), "INFO", "User logged out"),
        ]
        filter_obj = LogFilter()
        filtered = filter_obj.filter_by_pattern(entries, pattern="User")
        assert len(filtered) == 2


class TestFilterByTimeRange:
    def test_filter_by_time_range_func(self):
        entries = [
            LogEntry(datetime(2024, 4, 20, 9, 0), "INFO", "msg1"),
            LogEntry(datetime(2024, 4, 20, 10, 0), "INFO", "msg2"),
            LogEntry(datetime(2024, 4, 20, 11, 0), "INFO", "msg3"),
        ]
        filtered = filter_by_time_range(
            entries,
            start=datetime(2024, 4, 20, 9, 30),
            end=datetime(2024, 4, 20, 10, 30),
        )
        assert len(filtered) == 1

    def test_filter_by_time_range_no_start(self):
        entries = [
            LogEntry(datetime(2024, 4, 20, 9, 0), "INFO", "msg1"),
            LogEntry(datetime(2024, 4, 20, 10, 0), "INFO", "msg2"),
        ]
        filtered = filter_by_time_range(entries, end=datetime(2024, 4, 20, 10, 0))
        assert len(filtered) == 2

    def test_filter_by_time_range_no_end(self):
        entries = [
            LogEntry(datetime(2024, 4, 20, 9, 0), "INFO", "msg1"),
            LogEntry(datetime(2024, 4, 20, 10, 0), "INFO", "msg2"),
        ]
        filtered = filter_by_time_range(entries, start=datetime(2024, 4, 20, 10, 0))
        assert len(filtered) == 1


class TestFilterByLevel:
    def test_filter_by_level_single(self):
        entries = [
            LogEntry(datetime(2024, 4, 20, 10, 0), "INFO", "msg1"),
            LogEntry(datetime(2024, 4, 20, 11, 0), "ERROR", "msg2"),
        ]
        filtered = filter_by_level(entries, levels=["ERROR"])
        assert len(filtered) == 1

    def test_filter_by_level_multiple(self):
        entries = [
            LogEntry(datetime(2024, 4, 20, 10, 0), "INFO", "msg1"),
            LogEntry(datetime(2024, 4, 20, 11, 0), "ERROR", "msg2"),
            LogEntry(datetime(2024, 4, 20, 12, 0), "WARN", "msg3"),
        ]
        filtered = filter_by_level(entries, levels=["ERROR", "WARN"])
        assert len(filtered) == 2

    def test_filter_by_level_empty(self):
        entries = [
            LogEntry(datetime(2024, 4, 20, 10, 0), "INFO", "msg1"),
        ]
        filtered = filter_by_level(entries, levels=["ERROR"])
        assert len(filtered) == 0


class TestFilterByWeekday:
    def test_filter_weekday_only(self):
        entries = [
            LogEntry(datetime(2024, 4, 22, 10, 0), "INFO", "Monday"),
            LogEntry(datetime(2024, 4, 20, 10, 0), "INFO", "Saturday"),
        ]
        filtered = filter_by_weekday(entries, weekdays_only=True)
        assert len(filtered) == 1

    def test_filter_weekend_only(self):
        entries = [
            LogEntry(datetime(2024, 4, 22, 10, 0), "INFO", "Monday"),
            LogEntry(datetime(2024, 4, 20, 10, 0), "INFO", "Saturday"),
        ]
        filtered = filter_by_weekday(entries, weekdays_only=False)
        assert len(filtered) == 1


class TestFilterByPattern:
    def test_filter_by_pattern_match(self):
        entries = [
            LogEntry(datetime(2024, 4, 20, 10, 0), "INFO", "User logged in"),
            LogEntry(datetime(2024, 4, 20, 11, 0), "ERROR", "Connection failed"),
        ]
        filtered = filter_by_pattern(entries, pattern="User")
        assert len(filtered) == 1

    def test_filter_by_pattern_regex(self):
        entries = [
            LogEntry(datetime(2024, 4, 20, 10, 0), "INFO", "Error 500 occurred"),
            LogEntry(datetime(2024, 4, 20, 11, 0), "INFO", "Error 404 found"),
            LogEntry(datetime(2024, 4, 20, 12, 0), "INFO", "Success"),
        ]
        filtered = filter_by_pattern(entries, pattern=r"Error \d+")
        assert len(filtered) == 2

    def test_filter_by_pattern_no_match(self):
        entries = [
            LogEntry(datetime(2024, 4, 20, 10, 0), "INFO", "Success"),
        ]
        filtered = filter_by_pattern(entries, pattern="Error")
        assert len(filtered) == 0
