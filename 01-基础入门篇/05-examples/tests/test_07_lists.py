"""测试 07 - 列表"""

import pytest
from src import lists as lists


class TestExample01:
    def test_basic_list(self) -> None:
        result = lists.example_01_basic()
        assert isinstance(result, list)
        assert "西瓜" in result


class TestExample02:
    def test_list_operations(self) -> None:
        result = lists.example_02_level1()
        assert "苹果" in result


class TestExample05:
    def test_list_comprehension(self) -> None:
        result = lists.example_05_level4()
        assert all(p > 10 for p in result)


class TestPractical:
    def test_student_management(self) -> None:
        result = lists.example_practical()
        assert len(result) == 3
        assert all("name" in s for s in result)
        assert all("scores" in s for s in result)
