"""测试 06 - 字符串"""

import pytest
from src import strings as strings


class TestExample01:
    def test_basic_string(self) -> None:
        result = strings.example_01_basic()
        assert "Python" in result
        assert "3.11" in result


class TestExample06:
    def test_text_processing(self) -> None:
        error_count = strings.example_06_level5()
        assert error_count == 1


class TestPractical:
    def test_log_analysis(self) -> None:
        result = strings.example_practical()
        assert "total_lines" in result
        assert "level_counts" in result
        assert result["total_lines"] == 3
