"""类型提示工具函数 — ch02：泛型函数"""

from __future__ import annotations

from typing import TypeVar

T = TypeVar("T")


def first(items: list[T]) -> T:
    """返回列表第一个元素（ch02：泛型函数）

    Raises:
        ValueError: 列表为空时抛出
    """
    if not items:
        raise ValueError("列表为空")
    return items[0]


def reverse(items: list[T]) -> list[T]:
    """反转列表（ch02：泛型函数）"""
    return items[::-1]


def safe_get(data: dict[str, T], key: str) -> T | None:
    """安全获取字典值（ch02：泛型 + Optional）"""
    return data.get(key)
