"""字符串测试"""

from app.core.string_ops import string_operations, string_formatting


def test_string_operations():
    result = string_operations("Hello, Python!")
    assert result["length"] == 14
    assert result["upper"] == "HELLO, PYTHON!"
    assert result["reverse"] == "!nohtyP ,olleH"


def test_string_formatting():
    result = string_formatting("Python", 3.14159)
    assert "Python" in result["f_string"]
    assert "3.14" in result["f_string"]