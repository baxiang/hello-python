"""第 4 章 — 带参数装饰器与装饰器工厂

演示三层嵌套结构、装饰器工厂、可选参数兼容性写法。
"""

from __future__ import annotations

import functools
import time
from collections.abc import Callable
from typing import Any, TypeVar

T = TypeVar("T")


# ─────────────────────────────────────
# 三层嵌套：带参数的装饰器
# ─────────────────────────────────────


def repeat(times: int) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """重复执行装饰器 — 三层嵌套展示

    第 1 层：接收参数（times）
    第 2 层：接收函数（func）
    第 3 层：包装逻辑（wrapper）
    """

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            result: T | None = None
            for _ in range(times):
                result = func(*args, **kwargs)
            return result  # type: ignore[return-value]

        return wrapper

    return decorator


# ─────────────────────────────────────
# 权限验证装饰器
# ─────────────────────────────────────


def require_role(required_role: str) -> Callable:
    """权限验证装饰器 — 检查用户角色"""

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            req = kwargs.get("request") or (args[0] if args else None)
            user_role = getattr(req, "role", "guest") if req else "guest"

            if user_role != required_role:
                return {
                    "status": 403,
                    "error": "权限不足",
                    "required": required_role,
                    "actual": user_role,
                }

            return func(*args, **kwargs)

        return wrapper

    return decorator


# ─────────────────────────────────────
# 重试装饰器
# ─────────────────────────────────────


def retry(
    max_attempts: int = 3,
    delay: float = 0.0,
    exceptions: tuple[type[Exception], ...] = (Exception,),
) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """重试装饰器 — 失败时自动重试"""

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            last_exc: Exception | None = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exc = e
                    wrapper._attempts = attempt  # type: ignore[attr-defined]
                    if delay > 0 and attempt < max_attempts:
                        time.sleep(delay)
            raise last_exc  # type: ignore[misc]

        wrapper._attempts = 0  # type: ignore[attr-defined]
        return wrapper

    return decorator


# ─────────────────────────────────────
# 装饰器工厂模式
# ─────────────────────────────────────


def create_rate_limiter(max_calls: int) -> Callable:
    """装饰器工厂 — 根据配置生成不同的限流装饰器"""

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

        wrapper.reset = reset  # type: ignore[attr-defined]
        wrapper.call_count = lambda: calls  # type: ignore[attr-defined]
        return wrapper

    return decorator
