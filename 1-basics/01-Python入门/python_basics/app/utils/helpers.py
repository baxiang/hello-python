"""辅助函数"""

from typing import Any


def print_result(title: str, result: dict[str, Any]) -> None:
    """打印结果"""
    print(f"\n{title}:")
    for key, value in result.items():
        print(f"  {key}: {value}")