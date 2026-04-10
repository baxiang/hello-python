"""辅助函数"""

from typing import Any


def flatten_list(nested_list: list[list[Any]]) -> list[Any]:
    """扁平化列表"""
    return [item for sublist in nested_list for item in sublist]


def unique_items(items: list) -> list:
    """获取唯一元素"""
    return list(set(items))