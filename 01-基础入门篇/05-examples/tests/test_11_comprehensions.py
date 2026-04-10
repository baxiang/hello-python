"""测试 11 - 推导式"""

import pytest
from src import comprehensions as comprehensions


class TestExample01:
    def test_basic_comprehension(self) -> None:
        result = comprehensions.example_01_basic()
        assert result == [0, 1, 4, 9, 16]


class TestExample02:
    def test_basic_transformation(self) -> None:
        result = comprehensions.example_02_level1()
        assert result == [0, 1, 4, 9, 16]


class TestExample03:
    def test_filtering(self) -> None:
        result = comprehensions.example_03_level2()
        assert result == [0, 2, 4, 6, 8]


class TestExample04:
    def test_nested_loop(self) -> None:
        result = comprehensions.example_04_level3()
        assert len(result) == 9  # 3x3 = 9 points


class TestExample05:
    def test_dict_comprehension(self) -> None:
        result = comprehensions.example_05_level4()
        assert result["apple"] == 5
        assert result["banana"] == 6


class TestExample06:
    def test_generator_expression(self) -> None:
        result = comprehensions.example_06_level5()
        assert result == sum(x**2 for x in range(100) if x % 2 == 0)


class TestPractical:
    def test_data_pipeline(self) -> None:
        result = comprehensions.example_practical()
        assert result["passed_count"] == 2
        assert "average_score" in result
        assert "courses" in result
        assert "id_name_map" in result
