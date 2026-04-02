"""工具测试"""

from app.core.tools import validate_email, validate_phone, format_size, truncate_string


def test_validate_email():
    assert validate_email("test@example.com") is True
    assert validate_email("invalid-email") is False


def test_validate_phone():
    assert validate_phone("13812345678") is True
    assert validate_phone("12345678901") is False


def test_format_size():
    assert "B" in format_size(100)
    assert "KB" in format_size(1024)
    assert "MB" in format_size(1024 * 1024)


def test_truncate_string():
    assert truncate_string("hello", 10) == "hello"
    assert len(truncate_string("hello world", 5)) == 5