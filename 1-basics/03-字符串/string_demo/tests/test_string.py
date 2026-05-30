"""字符串测试"""

from app.core.string_ops import (
    string_formatting,
    string_methods,
    string_operations,
    string_validation,
)


def test_string_operations():
    result = string_operations("Hello, Python!")
    assert result["length"] == 14
    assert result["upper"] == "HELLO, PYTHON!"
    assert result["reverse"] == "!nohtyP ,olleH"


def test_string_formatting():
    result = string_formatting("Python", 3.14159)
    assert "Python" in result["f_string"]
    assert "3.14" in result["f_string"]


def test_string_methods():
    result = string_methods("  hello,python,world  ")
    assert result["strip"] == "hello,python,world"
    assert result["split"] == ["  hello", "python", "world  "]
    assert result["join"] == "  hello-python-world  "
    assert result["find"] == 8
    assert result["replace"] == "  hello,Python,world  "


def test_string_validation():
    result = string_validation("abc123")
    assert result["isdigit"] is False
    assert result["isalpha"] is False
    assert result["isalnum"] is True
    assert result["isspace"] is False
