"""基础语法测试"""

from app.core.basics import demonstrate_variables, demonstrate_operators


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