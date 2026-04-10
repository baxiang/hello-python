"""测试 05 - 流程控制"""

import pytest
from src import flow_control as flow_control


class TestExample01:
    def test_basic_flow_control(self) -> None:
        result = flow_control.example_01_basic()
        assert result == "成年人"


class TestExample03:
    def test_multi_condition(self) -> None:
        result = flow_control.example_03_level2()
        assert result == "通过"


class TestExample05:
    def test_loop_with_condition(self) -> None:
        count = flow_control.example_05_level4()
        assert count == 3


class TestExample06:
    def test_match_statement(self) -> None:
        result = flow_control.example_06_level5()
        assert result == "攻击"
