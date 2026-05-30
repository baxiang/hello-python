"""辅助函数测试"""

from app.utils.helpers import truncate_string


def test_truncate_string_short():
    result = truncate_string("hello", max_length=10)
    assert result == "hello"


def test_truncate_string_exact():
    result = truncate_string("hello", max_length=5)
    assert result == "hello"


def test_truncate_string_long():
    result = truncate_string("hello world", max_length=8)
    assert result == "hello wo..."


def test_truncate_string_default():
    long_str = "a" * 100
    result = truncate_string(long_str)
    assert len(result) == 53
    assert result.endswith("...")
