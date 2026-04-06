"""泛型示例"""

from typing import TypeVar, Generic
from dataclasses import dataclass

T = TypeVar('T')
Number = TypeVar('Number', int, float)


def first(items: list[T]) -> T:
    """返回列表第一个元素"""
    return items[0]


def reverse(items: list[T]) -> list[T]:
    """反转列表"""
    return items[::-1]


def get_middle(items: list[T]) -> T:
    """获取中间元素"""
    return items[len(items) // 2]


def double(value: Number) -> Number:
    """翻倍数值"""
    return value * 2


def add_numbers(a: Number, b: Number) -> Number:
    """数字相加"""
    return a + b


class Stack(Generic[T]):
    """泛型栈"""
    
    def __init__(self) -> None:
        self._items: list[T] = []
    
    def push(self, item: T) -> None:
        self._items.append(item)
    
    def pop(self) -> T:
        if not self._items:
            raise IndexError("栈为空")
        return self._items.pop()
    
    def peek(self) -> T:
        if not self._items:
            raise IndexError("栈为空")
        return self._items[-1]
    
    def is_empty(self) -> bool:
        return len(self._items) == 0


@dataclass
class Entity:
    id: int


class Repository(Generic[T]):
    """泛型仓储"""
    
    def __init__(self) -> None:
        self._storage: list[T] = []
    
    def add(self, item: T) -> int:
        self._storage.append(item)
        return len(self._storage) - 1
    
    def get(self, index: int) -> T | None:
        if 0 <= index < len(self._storage):
            return self._storage[index]
        return None
    
    def get_all(self) -> list[T]:
        return self._storage.copy()
    
    def update(self, index: int, item: T) -> bool:
        if 0 <= index < len(self._storage):
            self._storage[index] = item
            return True
        return False
    
    def delete(self, index: int) -> bool:
        if 0 <= index < len(self._storage):
            self._storage.pop(index)
            return True
        return False