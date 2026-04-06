"""测试 03 - 变量与数据类型"""

import pytest
from src import variables as variables


class TestExample01:
    def test_basic_returns_dict(self) -> None:
        result = variables.example_01_basic()
        assert isinstance(result, dict)
        assert "name" in result
        assert "age" in result


class TestExample03:
    def test_multiple_variables(self) -> None:
        result = variables.example_03_level2()
        assert result["name"] == "张三"
        assert result["age"] == 18
        assert result["score"] == 85.5


class TestExample04:
    def test_variable_swap(self) -> None:
        a, b = variables.example_04_level3()
        assert a == 20
        assert b == 10


class TestExample06:
    def test_calculation(self) -> None:
        total = variables.example_06_level5()
        assert total == pytest.approx(299.7, rel=0.01)


class TestPractical:
    def test_student_management(self) -> None:
        students = variables.example_practical()
        assert len(students) == 3
        assert all("name" in s for s in students)
