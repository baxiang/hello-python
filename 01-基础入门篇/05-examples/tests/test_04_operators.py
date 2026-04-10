"""测试 04 - 运算符"""

import pytest
from src import operators as operators


class TestExample01:
    def test_basic_operations(self) -> None:
        result = operators.example_01_basic()
        assert result["add"] == 15
        assert result["sub"] == 5
        assert result["mul"] == 50
        assert result["div"] == 2.0


class TestExample03:
    def test_advanced_arithmetic(self) -> None:
        result = operators.example_03_level2()
        assert result["floor"] == 3
        assert result["mod"] == 1
        assert result["power"] == 1000


class TestExample04:
    def test_comparison(self) -> None:
        result = operators.example_04_level3()
        assert result["is_odd"] is True


class TestExample05:
    def test_logical_combination(self) -> None:
        result = operators.example_05_level4()
        assert result["can_drive"] is True


class TestExample06:
    def test_composite_operation(self) -> None:
        final = operators.example_06_level5()
        assert final == pytest.approx(101.8, rel=0.01)


class TestPractical:
    def test_shopping_cart(self) -> None:
        result = operators.example_practical()
        assert "subtotal" in result
        assert "discount" in result
        assert "final" in result
