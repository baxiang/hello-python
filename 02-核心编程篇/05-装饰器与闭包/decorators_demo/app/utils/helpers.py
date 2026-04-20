"""辅助函数 — 装饰器常用工具"""

from __future__ import annotations

from collections.abc import Callable


def counter() -> Callable[[], int]:
    """计数器闭包（ch02：nonlocal 维护状态）

    用法：
        cnt = counter()
        cnt()  → 1
        cnt()  → 2
    """
    count = 0

    def increment() -> int:
        nonlocal count
        count += 1
        return count

    return increment


def compose_decorators(*decorators: Callable) -> Callable:
    """组合多个装饰器为一个（ch04：装饰器高阶用法）

    用法：
        @compose_decorators(@retry(3), @timer)
        def my_func(): ...
    """

    def composed(func: Callable) -> Callable:
        result = func
        for deco in reversed(decorators):
            result = deco(result)
        return result

    return composed
