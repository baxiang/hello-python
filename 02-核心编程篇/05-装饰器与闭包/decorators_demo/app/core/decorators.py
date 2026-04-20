"""装饰器与闭包示例 — 覆盖第01-04章

场景：API 请求处理中间件

章节对应：
  ch01  装饰器基础：@语法糖、functools.wraps 保留元信息
  ch02  闭包与 nonlocal：自由变量捕获、nonlocal 修改外层状态
  ch03  functools.lru_cache（缓存）、functools.partial（偏函数）
  ch04  带参数的装饰器；装饰器叠加（stacking）；类装饰器
"""

from __future__ import annotations

import functools
import time
from collections.abc import Callable
from typing import Any

# ---------------------------------------------------------------------------
# ch01: 装饰器基础
# ---------------------------------------------------------------------------

def log_call(func: Callable) -> Callable:
    """记录函数调用（ch01：最基础的装饰器 + @wraps）

    调用时打印函数名和参数，演示装饰器的副作用。
    """
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        print(f"[log_call] 调用 {func.__name__}({args!r}, {kwargs!r})")
        result = func(*args, **kwargs)
        print(f"[log_call] {func.__name__} 返回 {result!r}")
        return result
    wrapper._decorated = True          # type: ignore[attr-defined]
    return wrapper


def timer(func: Callable) -> Callable:
    """计时装饰器（ch01：@wraps 保留 __name__ / __doc__）"""
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        wrapper.last_elapsed = elapsed  # type: ignore[attr-defined]
        return result
    wrapper.last_elapsed = 0.0         # type: ignore[attr-defined]
    return wrapper


# ---------------------------------------------------------------------------
# ch02: 闭包与 nonlocal
# ---------------------------------------------------------------------------

def make_counter(start: int = 0) -> Callable[[], int]:
    """闭包工厂：用 nonlocal 修改外层变量（ch02：自由变量 + nonlocal）"""
    count = start

    def increment() -> int:
        nonlocal count
        count += 1
        return count

    return increment


def make_rate_limiter(max_calls: int) -> Callable[[Callable], Callable]:
    """基于闭包的限流装饰器（ch02：闭包状态 + nonlocal）"""
    def decorator(func: Callable) -> Callable:
        calls = 0

        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            nonlocal calls
            if calls >= max_calls:
                raise RuntimeError(f"调用次数超限（上限 {max_calls}）")
            calls += 1
            return func(*args, **kwargs)

        def reset() -> None:
            nonlocal calls
            calls = 0

        wrapper.reset = reset          # type: ignore[attr-defined]
        wrapper.call_count = lambda: calls  # type: ignore[attr-defined]
        return wrapper
    return decorator


# ---------------------------------------------------------------------------
# ch03: functools — lru_cache / partial
# ---------------------------------------------------------------------------

@functools.lru_cache(maxsize=128)
def expensive_parse(path: str) -> dict[str, str]:
    """模拟耗时解析（ch03：lru_cache 缓存结果，重复调用直接返回缓存）"""
    return {"path": path, "parsed": True}


def make_prefixed_logger(prefix: str) -> Callable[[str], str]:
    """用 partial 固定前缀（ch03：partial 偏函数）"""
    def _log(prefix: str, message: str) -> str:
        return f"[{prefix}] {message}"

    return functools.partial(_log, prefix)


# ---------------------------------------------------------------------------
# ch04: 带参数的装饰器；叠加装饰器；类装饰器
# ---------------------------------------------------------------------------

def retry(
    max_attempts: int = 3,
    exceptions: tuple[type[Exception], ...] = (Exception,),
) -> Callable:
    """带参数的装饰器（ch04：工厂函数返回装饰器）"""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            last_exc: Exception | None = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exc = e
                    wrapper.attempts = attempt      # type: ignore[attr-defined]
            raise last_exc  # type: ignore[misc]
        wrapper.attempts = 0            # type: ignore[attr-defined]
        return wrapper
    return decorator


def validate_positive(func: Callable) -> Callable:
    """验证首个位置参数为正数（ch04：与 @retry 叠加使用）"""
    @functools.wraps(func)
    def wrapper(value: float, *args: Any, **kwargs: Any) -> Any:
        if value <= 0:
            raise ValueError(f"参数必须为正数，收到 {value}")
        return func(value, *args, **kwargs)
    return wrapper


class singleton:
    """类装饰器：确保只有一个实例（ch04：__call__ 类装饰器）"""

    def __init__(self, cls: type) -> None:
        self._cls = cls
        self._instance: Any = None
        functools.update_wrapper(self, cls)

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        if self._instance is None:
            self._instance = self._cls(*args, **kwargs)
        return self._instance

    def reset(self) -> None:
        """测试辅助：重置单例"""
        self._instance = None
