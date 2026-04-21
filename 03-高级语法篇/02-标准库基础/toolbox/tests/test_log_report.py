"""LogReport测试 - json模块"""

import json
from datetime import datetime
from pathlib import Path

from app.core.log_entry import LogEntry
from app.core.log_report import (
    LogReport,
    export_to_json,
    generate_report,
    load_report,
    save_report,
)


class TestLogReport:
    def test_create_report(self):
        report = LogReport()
        assert report is not None

    def test_generate_summary(self):
        entries = [
            LogEntry(datetime(2024, 4, 20, 10, 0), "INFO", "msg1"),
            LogEntry(datetime(2024, 4, 20, 11, 0), "ERROR", "msg2"),
            LogEntry(datetime(2024, 4, 20, 12, 0), "ERROR", "msg3"),
        ]
        report = LogReport()
        summary = report.generate_summary(entries)
        assert summary["total_count"] == 3
        assert summary["level_counts"]["ERROR"] == 2
        assert summary["level_counts"]["INFO"] == 1

    def test_to_json(self):
        entries = [
            LogEntry(datetime(2024, 4, 20, 10, 0), "INFO", "test"),
        ]
        report = LogReport()
        json_str = report.to_json(entries)
        data = json.loads(json_str)
        assert len(data) == 1
        assert data[0]["level"] == "INFO"

    def test_to_json_with_indent(self):
        entries = [
            LogEntry(datetime(2024, 4, 20, 10, 0), "INFO", "test"),
        ]
        report = LogReport()
        json_str = report.to_json(entries, indent=2)
        assert "\n" in json_str

    def test_to_json_chinese(self):
        entries = [
            LogEntry(datetime(2024, 4, 20, 10, 0), "INFO", "中文消息"),
        ]
        report = LogReport()
        json_str = report.to_json(entries)
        assert "中文消息" in json_str


class TestGenerateReport:
    def test_generate_report_func(self, tmp_path: Path):
        entries = [
            LogEntry(datetime(2024, 4, 20, 10, 0), "INFO", "msg1"),
            LogEntry(datetime(2024, 4, 20, 11, 0), "ERROR", "msg2"),
        ]
        report = generate_report(entries)
        assert report["total_count"] == 2
        assert report["level_counts"]["INFO"] == 1
        assert report["level_counts"]["ERROR"] == 1

    def test_generate_report_empty(self):
        report = generate_report([])
        assert report["total_count"] == 0


class TestSaveReport:
    def test_save_report(self, tmp_path: Path):
        report_data = {"total_count": 5, "errors": 2}
        output_file = tmp_path / "report.json"
        save_report(report_data, output_file)
        assert output_file.exists()

        with open(output_file) as f:
            loaded = json.load(f)
        assert loaded["total_count"] == 5

    def test_save_report_with_indent(self, tmp_path: Path):
        report_data = {"total_count": 5}
        output_file = tmp_path / "report.json"
        save_report(report_data, output_file, indent=4)
        content = output_file.read_text()
        assert "    " in content


class TestLoadReport:
    def test_load_report(self, tmp_path: Path):
        report_data = {"total_count": 5, "errors": 2}
        output_file = tmp_path / "report.json"
        output_file.write_text(json.dumps(report_data))
        loaded = load_report(output_file)
        assert loaded["total_count"] == 5

    def test_load_report_nonexistent(self, tmp_path: Path):
        nonexistent = tmp_path / "nonexistent.json"
        loaded = load_report(nonexistent)
        assert loaded is None


class TestExportToJson:
    def test_export_to_json(self, tmp_path: Path):
        entries = [
            LogEntry(datetime(2024, 4, 20, 10, 0), "INFO", "msg1"),
        ]
        output_file = tmp_path / "export.json"
        export_to_json(entries, output_file)
        assert output_file.exists()

    def test_export_to_json_chinese(self, tmp_path: Path):
        entries = [
            LogEntry(datetime(2024, 4, 20, 10, 0), "INFO", "中文测试"),
        ]
        output_file = tmp_path / "export.json"
        export_to_json(entries, output_file)
        content = output_file.read_text()
        assert "中文测试" in content


class TestReportStatistics:
    def test_time_range(self):
        entries = [
            LogEntry(datetime(2024, 4, 20, 10, 0), "INFO", "msg1"),
            LogEntry(datetime(2024, 4, 20, 12, 0), "ERROR", "msg2"),
            LogEntry(datetime(2024, 4, 21, 10, 0), "WARN", "msg3"),
        ]
        report = LogReport()
        summary = report.generate_summary(entries)
        assert summary["time_range"]["start"] is not None
        assert summary["time_range"]["end"] is not None

    def test_message_count(self):
        entries = [
            LogEntry(datetime(2024, 4, 20, 10, 0), "INFO", "User login"),
            LogEntry(datetime(2024, 4, 20, 11, 0), "INFO", "User logout"),
            LogEntry(datetime(2024, 4, 20, 12, 0), "ERROR", "Error"),
        ]
        report = LogReport()
        summary = report.generate_summary(entries)
        assert summary["message_count"] == 3
