"""测试 08 - 元组"""

import pytest
from src import tuples as tuples


class TestExample01:
    def test_basic_tuple(self) -> None:
        result = tuples.example_01_basic()
        assert result == (10, 20)


class TestExample02:
    def test_tuple_creation(self) -> None:
        result = tuples.example_02_level1()
        assert result == ("red", "green", "blue")


class TestExample03:
    def test_tuple_unpacking(self) -> None:
        result = tuples.example_03_level2()
        assert result == (255, 128, 0)


class TestExample04:
    def test_tuple_as_dict_key(self) -> None:
        result = tuples.example_04_level3()
        assert result == pytest.approx(1.414, rel=0.01)


class TestExample06:
    def test_function_returns_tuple(self) -> None:
        result = tuples.example_06_level5()
        minimum, maximum, average = result
        assert minimum == 1
        assert maximum == 5
        assert average == pytest.approx(3.0, rel=0.01)


class TestPractical:
    def test_config_management(self) -> None:
        result = tuples.example_practical()
        assert result.host == "localhost"
        assert result.port == 3306
        assert result.database == "myapp"
