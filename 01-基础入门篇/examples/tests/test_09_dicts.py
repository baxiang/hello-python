"""测试 09 - 字典"""

import pytest
from src import dicts as dicts


class TestExample01:
    def test_basic_dict(self) -> None:
        result = dicts.example_01_basic()
        assert isinstance(result, dict)
        assert result["name"] == "张三"
        assert result["city"] == "北京"


class TestExample02:
    def test_dict_operations(self) -> None:
        result = dicts.example_02_level1()
        assert "science" in result
        assert result["science"] == 92


class TestExample04:
    def test_dict_get_method(self) -> None:
        result = dicts.example_04_level3()
        assert result == "未设置"


class TestExample06:
    def test_dict_comprehension(self) -> None:
        result = dicts.example_06_level5()
        assert result["apple"] == 5
        assert result["banana"] == 6


class TestPractical:
    def test_student_query_system(self) -> None:
        result = dicts.example_practical()
        assert "students" in result
        assert "avg_score" in result
        assert len(result["students"]) == 3
