"""第 7 章 — 装饰器边界情况

演示装饰器叠加顺序、属性冲突、闭包变量绑定、async 与方法兼容性等边界问题。
"""

from __future__ import annotations

import asyncio
import functools
import time
from collections.abc import Callable, Coroutine
from typing import Any, ParamSpec, TypeVar

P = ParamSpec("P")
T = TypeVar("T")


# ─────────────────────────────────────
# 7.1 装饰器叠加顺序问题
# ─────────────────────────────────────

def timer_a(func: Callable[P, T]) -> Callable[P, T]:
    """计时装饰器 A — 设置 _last_elapsed 和 _source 属性"""
    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        start = time.perf_counter()
        result = func(*args, **kwargs)
        wrapper._last_elapsed = time.perf_counter() - start
        wrapper._source = "timer_a"
        return result
    wrapper._last_elapsed = 0.0
    wrapper._source = "timer_a"
    return wrapper


def timer_b(func: Callable[P, T]) -> Callable[P, T]:
    """计时装饰器 B — 也设置 _last_elapsed 和 _source 属性（冲突）"""
    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        start = time.perf_counter()
        result = func(*args, **kwargs)
        wrapper._last_elapsed = time.perf_counter() - start
        wrapper._source = "timer_b"
        return result
    wrapper._last_elapsed = 0.0
    wrapper._source = "timer_b"
    return wrapper


def timer_outer(func: Callable[P, T]) -> Callable[P, T]:
    """外层计时装饰器 — 使用不同属性名避免冲突"""
    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        start = time.perf_counter()
        result = func(*args, **kwargs)
        wrapper._outer_elapsed = time.perf_counter() - start
        return result
    wrapper._outer_elapsed = 0.0
    return wrapper


def timer_inner(func: Callable[P, T]) -> Callable[P, T]:
    """内层计时装饰器 — 使用不同属性名避免冲突"""
    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        start = time.perf_counter()
        result = func(*args, **kwargs)
        wrapper._inner_elapsed = time.perf_counter() - start
        return result
    wrapper._inner_elapsed = 0.0
    return wrapper


def get_inner_elapsed(func: Callable) -> float | None:
    """通过 __wrapped__ 链获取内层装饰器的计时"""
    inner = getattr(func, "__wrapped__", None)
    if inner and hasattr(inner, "_last_elapsed"):
        return inner._last_elapsed
    return None


# 异常处理顺序示例
def catch_errors(func: Callable[P, T]) -> Callable[P, T]:
    """捕获异常装饰器（外层）"""
    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T | dict[str, Any]:
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return {"error": str(e), "func": func.__name__}
    return wrapper


def retry_simple(func: Callable[P, T]) -> Callable[P, T]:
    """简单重试装饰器（内层）"""
    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        for attempt in range(3):
            try:
                return func(*args, **kwargs)
            except Exception:
                if attempt == 2:
                    raise
                time.sleep(0.01)
        raise RuntimeError("重试失败")
    return wrapper


# ─────────────────────────────────────
# 7.2 装饰器嵌套与元装饰器
# ─────────────────────────────────────

def log_decorator_usage(decorator_func: Callable) -> Callable:
    """元装饰器：记录装饰器的使用"""
    @functools.wraps(decorator_func)
    def meta_wrapper(func: Callable) -> Callable:
        decorator_name = decorator_func.__name__
        func_name = func.__name__
        setattr(meta_wrapper, "_last_decorator", decorator_name)
        setattr(meta_wrapper, "_last_decorated", func_name)
        return decorator_func(func)
    return meta_wrapper


def create_rate_limiter_factory(default_max_calls: int) -> Callable:
    """工厂的工厂：生成不同默认配置的限流装饰器"""
    def create_rate_limiter(max_calls: int = default_max_calls) -> Callable:
        def decorator(func: Callable[P, T]) -> Callable[P, T]:
            calls = 0
            @functools.wraps(func)
            def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
                nonlocal calls
                if calls >= max_calls:
                    raise RuntimeError(f"调用超限（上限 {max_calls}）")
                calls += 1
                return func(*args, **kwargs)
            wrapper._max_calls = max_calls
            wrapper._call_count = lambda: calls
            return wrapper
        return decorator
    return create_rate_limiter


# ─────────────────────────────────────
# 7.3 闭包变量绑定陷阱（进阶）
# ─────────────────────────────────────

def create_callbacks_wrong() -> list[Callable[[], int]]:
    """❌ late-binding：变量在调用时才绑定"""
    callbacks = []
    for i in range(3):
        def callback() -> int:
            return i * 2
        callbacks.append(callback)
    return callbacks


def create_callbacks_fixed() -> list[Callable[[], int]]:
    """✅ early-binding：变量在定义时就绑定"""
    callbacks = []
    for i in range(3):
        def callback(i: int = i) -> int:
            return i * 2
        callbacks.append(callback)
    return callbacks


def create_api_handlers_wrong() -> dict[str, Callable[[], str]]:
    """❌ 循环变量陷阱：所有 handler 共享同一个 endpoint"""
    handlers: dict[str, Callable[[], str]] = {}
    for endpoint in ["users", "products", "orders"]:
        def handler() -> str:
            return f"处理 {endpoint}"
        handlers[endpoint] = handler
    return handlers


def create_api_handlers_fixed() -> dict[str, Callable[[], str]]:
    """✅ 使用默认参数捕获当前值"""
    handlers: dict[str, Callable[[], str]] = {}
    for endpoint in ["users", "products", "orders"]:
        def handler(endpoint: str = endpoint) -> str:
            return f"处理 {endpoint}"
        handlers[endpoint] = handler
    return handlers


# ─────────────────────────────────────
# 7.4 async 与方法装饰器兼容性
# ─────────────────────────────────────

def sync_timer_wrong(func: Callable[P, Coroutine[Any, Any, T]]) -> Callable[P, Coroutine[Any, Any, T]]:
    """❌ sync 装饰器错误处理 async 函数（没有 await）"""
    @functools.wraps(func)
    async def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        start = time.perf_counter()
        result = func(*args, **kwargs)
        wrapper._elapsed = time.perf_counter() - start
        return result
    wrapper._elapsed = 0.0
    return wrapper


def async_timer_fixed(func: Callable[P, Coroutine[Any, Any, T]]) -> Callable[P, Coroutine[Any, Any, T]]:
    """✅ async 装饰器正确处理 await"""
    @functools.wraps(func)
    async def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        start = time.perf_counter()
        result = await func(*args, **kwargs)
        wrapper._elapsed = time.perf_counter() - start
        return result
    wrapper._elapsed = 0.0
    return wrapper


def log_method(func: Callable[P, T]) -> Callable[P, T]:
    """普通方法装饰器（包含 self 在日志中）"""
    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        print(f"调用 {func.__name__}, args={args}")
        return func(*args, **kwargs)
    return wrapper


def log_method_pretty(func: Callable[P, T]) -> Callable[P, T]:
    """优雅的方法装饰器（显式处理 self）"""
    @functools.wraps(func)
    def wrapper(self: Any, *args: P.args, **kwargs: P.kwargs) -> T:
        print(f"[{self.__class__.__name__}] {func.__name__}({args})")
        return func(self, *args, **kwargs)
    return wrapper


# classmethod 顺序示例
def timer_for_method(func: Callable[P, T]) -> Callable[P, T]:
    """用于 @classmethod 的计时装饰器"""
    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        start = time.perf_counter()
        result = func(*args, **kwargs)
        wrapper._elapsed = time.perf_counter() - start
        return result
    wrapper._elapsed = 0.0
    return wrapper


# ─────────────────────────────────────
# 7.5-7.6 调试相关示例
# ─────────────────────────────────────

def bad_decorator(func: Callable[P, T]) -> Callable[..., Any]:
    """❌ 没有 @wraps 的装饰器"""
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper


def good_decorator(func: Callable[P, T]) -> Callable[P, T]:
    """✅ 有 @wraps 的装饰器"""
    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        return func(*args, **kwargs)
    return wrapper


def catch_errors_swallow(func: Callable[P, T]) -> Callable[..., Any]:
    """❌ 吞掉异常栈的装饰器"""
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return {"error": str(e)}
    return wrapper


def catch_errors_preserve(func: Callable[P, T]) -> Callable[P, T]:
    """✅ 保留异常栈的装饰器"""
    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T | dict[str, Any]:
        try:
            return func(*args, **kwargs)
        except Exception as e:
            wrapper._last_error = e
            wrapper._last_traceback = str(e)
            raise RuntimeError(f"{func.__name__} 失败") from e
    return wrapper


# ─────────────────────────────────────
# 辅助函数
# ─────────────────────────────────────

def demo_process_with_sleep(duration: float = 0.01) -> str:
    """演示函数：睡眠指定时间"""
    time.sleep(duration)
    return "done"


async def demo_async_fetch(delay: float = 0.1) -> dict[str, str]:
    """演示异步函数：睡眠指定时间"""
    await asyncio.sleep(delay)
    return {"status": "ok"}