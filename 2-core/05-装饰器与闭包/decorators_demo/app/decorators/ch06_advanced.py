"""第 6 章 — 装饰器高级用法与最佳实践

演示 ParamSpec/Concatenate 精确类型签名、async 装饰器、
类装饰器、__wrapped__ 调试技巧。
"""

from __future__ import annotations

import functools
import time
from collections.abc import Callable, Coroutine
from typing import Any, ParamSpec, TypeVar

P = ParamSpec("P")
T = TypeVar("T")


# ─────────────────────────────────────
# ParamSpec：精确类型签名保留
# ─────────────────────────────────────

def timer_precise(func: Callable[P, T]) -> Callable[P, T]:
    """用 ParamSpec 保留精确类型签名的计时装饰器"""

    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        wrapper._last_elapsed = elapsed  # type: ignore[attr-defined]
        return result

    wrapper._last_elapsed = 0.0  # type: ignore[attr-defined]
    return wrapper


# ─────────────────────────────────────
# async 装饰器
# ─────────────────────────────────────

def async_timer(
    func: Callable[P, Coroutine[Any, Any, T]],
) -> Callable[P, Coroutine[Any, Any, T]]:
    """异步计时装饰器 — 正确处理 await"""

    @functools.wraps(func)
    async def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        start = time.perf_counter()
        result = await func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        wrapper._last_elapsed = elapsed  # type: ignore[attr-defined]
        return result

    wrapper._last_elapsed = 0.0  # type: ignore[attr-defined]
    return wrapper


# ─────────────────────────────────────
# 类装饰器
# ─────────────────────────────────────

class CountCalls:
    """类装饰器 — 记录函数调用次数"""

    def __init__(self, func: Callable[..., Any]) -> None:
        functools.update_wrapper(self, func)
        self._func = func
        self._count = 0

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        self._count += 1
        return self._func(*args, **kwargs)

    @property
    def count(self) -> int:
        return self._count


class Singleton:
    """类装饰器 — 单例模式"""

    def __init__(self, cls: type) -> None:
        self._cls = cls
        self._instance: Any = None
        functools.update_wrapper(self, cls)

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        if self._instance is None:
            self._instance = self._cls(*args, **kwargs)
        return self._instance

    def reset(self) -> None:
        self._instance = None


# ─────────────────────────────────────
# __wrapped__ 调试技巧
# ─────────────────────────────────────

def get_original_func(decorated_func: Callable) -> Callable:
    """通过 __wrapped__ 获取被装饰的原始函数"""
    return getattr(decorated_func, "__wrapped__", decorated_func)


def is_decorated(func: Callable) -> bool:
    """判断函数是否被装饰过"""
    return hasattr(func, "__wrapped__")
