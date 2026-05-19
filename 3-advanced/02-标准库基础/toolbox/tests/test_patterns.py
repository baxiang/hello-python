"""patterns测试 - 正则表达式模块"""

from app.utils.patterns import (
    EMAIL_PATTERN,
    ERROR_CODE_PATTERN,
    IP_PATTERN,
    LOG_LEVEL_PATTERN,
    PHONE_PATTERN,
    TIMESTAMP_PATTERN,
    URL_PATTERN,
    extract_emails,
    extract_error_codes,
    extract_ips,
    extract_timestamps,
)


class TestPatterns:
    def test_timestamp_pattern(self):
        import re

        match = re.match(TIMESTAMP_PATTERN, "2024-04-20T10:30:00")
        assert match is not None

    def test_timestamp_pattern_standard(self):
        import re

        match = re.match(TIMESTAMP_PATTERN, "2024-04-20 10:30:00")
        assert match is not None

    def test_ip_pattern(self):
        import re

        match = re.match(IP_PATTERN, "192.168.1.1")
        assert match is not None

    def test_ip_pattern_invalid(self):
        import re

        match = re.match(IP_PATTERN, "999.999.999.999")
        assert match is not None

    def test_validate_ip(self):
        from app.utils.validators import validate_ip

        assert validate_ip("192.168.1.1") is True
        assert validate_ip("999.999.999.999") is False

    def test_email_pattern(self):
        import re

        match = re.match(EMAIL_PATTERN, "test@example.com")
        assert match is not None

    def test_email_pattern_complex(self):
        import re

        match = re.match(EMAIL_PATTERN, "user.name+tag@subdomain.example.co.uk")
        assert match is not None

    def test_error_code_pattern(self):
        import re

        match = re.match(ERROR_CODE_PATTERN, "E001")
        assert match is not None

    def test_error_code_pattern_digits(self):
        import re

        match = re.match(ERROR_CODE_PATTERN, "500")
        assert match is not None

    def test_log_level_pattern(self):
        import re

        match = re.match(LOG_LEVEL_PATTERN, "ERROR")
        assert match is not None

    def test_log_level_pattern_lowercase(self):
        import re

        match = re.match(LOG_LEVEL_PATTERN, "info", re.IGNORECASE)
        assert match is not None

    def test_url_pattern(self):
        import re

        match = re.match(URL_PATTERN, "https://example.com")
        assert match is not None

    def test_phone_pattern(self):
        import re

        match = re.match(PHONE_PATTERN, "13812345678")
        assert match is not None


class TestExtractFunctions:
    def test_extract_timestamps(self):
        text = "2024-04-20T10:30:00 and 2024-04-21T11:00:00"
        timestamps = extract_timestamps(text)
        assert len(timestamps) == 2

    def test_extract_ips(self):
        text = "Connection from 192.168.1.1 and 10.0.0.1"
        ips = extract_ips(text)
        assert len(ips) == 2
        assert "192.168.1.1" in ips

    def test_extract_emails(self):
        text = "Contact: admin@example.com and support@test.org"
        emails = extract_emails(text)
        assert len(emails) == 2

    def test_extract_error_codes(self):
        text = "Error E001 occurred, also E500 and 404"
        codes = extract_error_codes(text)
        assert len(codes) == 3
