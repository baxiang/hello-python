"""类型提示工具函数"""

from typing import List, Dict, Optional, TypeVar


T = TypeVar("T")


def first(items: List[T]) -> T:
    """返回列表第一个元素"""
    if not items:
        raise ValueError("列表为空")
    return items[0]


def reverse(items: List[T]) -> List[T]:
    """反转列表"""
    return items[::-1]


def count_words(text: str) -> Dict[str, int]:
    """统计单词出现次数"""
    result: Dict[str, int] = {}
    for word in text.split():
        result[word] = result.get(word, 0) + 1
    return result


def safe_get(data: Dict, key: str) -> Optional[str]:
    """安全获取字典值"""
    return data.get(key)
