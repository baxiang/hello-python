"""第 3 章 — 装饰器核心原理

演示 @ 语法的本质、functools.wraps 的作用、装饰器的执行时序。
"""

from __future__ import annotations

import functools
import time
from collections.abc import Callable
from typing import Any, TypeVar

T = TypeVar("T")


# ─────────────────────────────────────
# 最简装饰器：展示 @ 语法本质
# ─────────────────────────────────────


def simple_decorator(func: Callable[..., T]) -> Callable[..., T]:
    """最简单的装饰器 — 什么都不做，只演示原理"""

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> T:
        return func(*args, **kwargs)

    return wrapper


# ─────────────────────────────────────
# 日志装饰器：演示前置/后置逻辑
# ─────────────────────────────────────

# 全局日志列表，用于测试验证
_call_log: list[dict[str, Any]] = []


def log_call(func: Callable[..., T]) -> Callable[..., T]:
    """日志装饰器 — 记录函数调用信息"""

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> T:
        _call_log.append(
            {
                "func": func.__name__,
                "args": args,
                "kwargs": kwargs,
                "status": "calling",
            }
        )
        result = func(*args, **kwargs)
        _call_log.append(
            {
                "func": func.__name__,
                "result": result,
                "status": "returned",
            }
        )
        return result

    return wrapper


def get_call_log() -> list[dict[str, Any]]:
    """获取调用日志（测试用）"""
    return _call_log


def clear_call_log() -> None:
    """清空调用日志（测试用）"""
    _call_log.clear()


# ─────────────────────────────────────
# 计时装饰器：演示性能监控
# ─────────────────────────────────────


def timer(func: Callable[..., T]) -> Callable[..., T]:
    """计时装饰器 — 记录函数执行耗时"""

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> T:
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        wrapper._last_elapsed = elapsed  # type: ignore[attr-defined]
        return result

    wrapper._last_elapsed = 0.0  # type: ignore[attr-defined]
    return wrapper


# ─────────────────────────────────────
# 不用 wraps 的反面教材
# ─────────────────────────────────────


def bad_decorator(func: Callable[..., T]) -> Callable[..., T]:
    """❌ 不用 @wraps — 丢失元信息"""

    def wrapper(*args: Any, **kwargs: Any) -> T:
        return func(*args, **kwargs)

    return wrapper
