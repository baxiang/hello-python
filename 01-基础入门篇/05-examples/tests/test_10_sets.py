"""测试 10 - 集合"""

import pytest
from src import sets as sets


class TestExample01:
    def test_basic_set(self) -> None:
        result = sets.example_01_basic()
        assert isinstance(result, set)
        assert "apple" in result


class TestExample02:
    def test_deduplication(self) -> None:
        result = sets.example_02_level1()
        assert result == {1, 2, 3, 4}


class TestExample03:
    def test_membership_test(self) -> None:
        result = sets.example_03_level2()
        assert result is True


class TestExample04:
    def test_set_operations(self) -> None:
        result = sets.example_04_level3()
        assert result == {3, 4}


class TestExample05:
    def test_difference_application(self) -> None:
        result = sets.example_05_level4()
        assert result["added"] == {"user4"}
        assert result["removed"] == {"user1"}


class TestExample06:
    def test_data_cleaning(self) -> None:
        result = sets.example_06_level5()
        assert result == [1, 2, 3, 4, 5]


class TestPractical:
    def test_permission_management(self) -> None:
        result = sets.example_practical()
        assert "user" in result
        assert "permissions" in result
        assert "manage_users" in result["permissions"]
