"""基础语法测试"""

from app.core.basics import (
    demonstrate_operators,
    demonstrate_variables,
    type_conversion,
)


def test_demonstrate_variables():
    result = demonstrate_variables()
    assert result["name"] == "Python"
    assert result["year"] == 2024
    assert result["is_popular"] is True


def test_demonstrate_operators():
    result = demonstrate_operators(10, 3)
    assert result["add"] == 13
    assert result["subtract"] == 7
    assert result["multiply"] == 30


def test_type_conversion_int():
    result = type_conversion("42")
    assert result["int"] == 42


def test_type_conversion_negative_int():
    result = type_conversion("-5")
    assert result["int"] == -5


def test_type_conversion_float():
    result = type_conversion("3.14")
    assert result["float"] == 3.14


def test_type_conversion_not_a_number():
    result = type_conversion("hello")
    assert result["int"] is None
    assert result["float"] is None


def test_type_conversion_original_preserved():
    result = type_conversion("abc")
    assert result["original"] == "abc"
    assert result["type"] == "str"
