"""LogParser测试 - 文件操作和正则表达式"""

from pathlib import Path

from app.core.log_parser import (
    LogParser,
    extract_ip_addresses,
    extract_log_level,
    mask_sensitive_info,
    parse_log_file,
    parse_log_line,
)


class TestLogParser:
    def test_parse_file(self, tmp_path: Path):
        log_file = tmp_path / "test.log"
        log_file.write_text(
            "2024-04-20T10:30:00 INFO User logged in\n"
            "2024-04-20T10:31:00 ERROR Connection failed\n"
        )
        parser = LogParser()
        entries = parser.parse_file(log_file)
        assert len(entries) == 2

    def test_parse_empty_file(self, tmp_path: Path):
        log_file = tmp_path / "empty.log"
        log_file.write_text("")
        parser = LogParser()
        entries = parser.parse_file(log_file)
        assert len(entries) == 0

    def test_parse_with_filter(self, tmp_path: Path):
        log_file = tmp_path / "test.log"
        log_file.write_text(
            "2024-04-20T10:30:00 INFO User logged in\n"
            "2024-04-20T10:31:00 ERROR Connection failed\n"
        )
        parser = LogParser()
        entries = parser.parse_file(log_file, level_filter="ERROR")
        assert len(entries) == 1
        assert entries[0].level == "ERROR"


class TestParseLogFile:
    def test_parse_log_file(self, tmp_path: Path):
        log_file = tmp_path / "test.log"
        log_file.write_text(
            "2024-04-20T10:30:00 INFO User logged in\n"
            "2024-04-20T10:31:00 WARN Low memory\n"
        )
        entries = parse_log_file(log_file)
        assert len(entries) == 2


class TestParseLogLine:
    def test_parse_standard_line(self):
        line = "2024-04-20T10:30:00 INFO User logged in"
        entry = parse_log_line(line)
        assert entry is not None
        assert entry.level == "INFO"
        assert "User logged in" in entry.message

    def test_parse_with_ip(self):
        line = "2024-04-20T10:30:00 INFO Connection from 192.168.1.1"
        entry = parse_log_line(line)
        assert entry is not None

    def test_parse_invalid_line(self):
        line = "invalid log line"
        entry = parse_log_line(line)
        assert entry is None


class TestMaskSensitiveInfo:
    def test_mask_email(self):
        text = "Contact: admin@example.com for support"
        masked = mask_sensitive_info(text)
        assert "admin@example.com" not in masked
        assert "***@***.***" in masked

    def test_mask_phone(self):
        text = "Call: 13812345678 for help"
        masked = mask_sensitive_info(text)
        assert "13812345678" not in masked

    def test_mask_multiple(self):
        text = "Email: test@example.com Phone: 13812345678"
        masked = mask_sensitive_info(text)
        assert "test@example.com" not in masked
        assert "13812345678" not in masked


class TestExtractIpAddresses:
    def test_extract_ips(self):
        text = "Connection from 192.168.1.1 and 10.0.0.1"
        ips = extract_ip_addresses(text)
        assert len(ips) == 2
        assert "192.168.1.1" in ips

    def test_extract_no_ips(self):
        text = "No IP addresses here"
        ips = extract_ip_addresses(text)
        assert len(ips) == 0


class TestExtractLogLevel:
    def test_extract_level(self):
        text = "2024-04-20T10:30:00 ERROR Connection failed"
        level = extract_log_level(text)
        assert level == "ERROR"

    def test_extract_no_level(self):
        text = "Just a plain message"
        level = extract_log_level(text)
        assert level is None
