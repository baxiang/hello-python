"""类型提示工具函数"""

from typing import TypeVar, Any


T = TypeVar("T")


def first(items: list[T]) -> T:
    """返回列表第一个元素"""
    if not items:
        raise ValueError("列表为空")
    return items[0]


def reverse(items: list[T]) -> list[T]:
    """反转列表"""
    return items[::-1]


def count_words(text: str) -> dict[str, int]:
    """统计单词出现次数"""
    result: dict[str, int] = {}
    for word in text.split():
        result[word] = result.get(word, 0) + 1
    return result


def safe_get(data: dict[str, Any], key: str) -> str | None:
    """安全获取字典值"""
    return data.get(key)
