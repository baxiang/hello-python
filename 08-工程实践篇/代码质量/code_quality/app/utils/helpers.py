"""辅助函数"""

from typing import Any


def validate_input(value: Any, expected_type: type) -> bool:
    """验证输入类型"""
    return isinstance(value, expected_type)