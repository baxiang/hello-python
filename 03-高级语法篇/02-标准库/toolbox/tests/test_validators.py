"""验证器测试 - 正则表达式模块"""

from app.utils.validators import (
    validate_email,
    validate_ip,
    validate_phone,
    validate_url,
)


class TestValidateEmail:
    def test_valid_email(self):
        assert validate_email("test@example.com") is True

    def test_valid_email_complex(self):
        assert validate_email("user.name+tag@subdomain.example.co.uk") is True

    def test_invalid_email_no_domain(self):
        assert validate_email("test@") is False

    def test_invalid_email_no_at(self):
        assert validate_email("testexample.com") is False


class TestValidatePhone:
    def test_valid_phone(self):
        assert validate_phone("13812345678") is True

    def test_valid_phone_199(self):
        assert validate_phone("19912345678") is True

    def test_invalid_phone_wrong_start(self):
        assert validate_phone("12345678901") is False

    def test_invalid_phone_short(self):
        assert validate_phone("1381234567") is False


class TestValidateIp:
    def test_valid_ip(self):
        assert validate_ip("192.168.1.1") is True

    def test_valid_ip_zero(self):
        assert validate_ip("0.0.0.0") is True

    def test_invalid_ip_high_number(self):
        assert validate_ip("999.999.999.999") is False

    def test_invalid_ip_format(self):
        assert validate_ip("192.168.1") is False


class TestValidateUrl:
    def test_valid_url_http(self):
        assert validate_url("http://example.com") is True

    def test_valid_url_https(self):
        assert validate_url("https://example.com/path") is True

    def test_invalid_url_no_protocol(self):
        assert validate_url("example.com") is False
