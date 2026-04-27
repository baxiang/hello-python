"""第 5 章 — functools 标准装饰器

演示 Python 标准库中最重要的装饰器：
lru_cache, cached_property, singledispatch, partial, wraps
"""

from __future__ import annotations

import functools
import time
from typing import Any

# ─────────────────────────────────────
# @lru_cache：缓存装饰器
# ─────────────────────────────────────


@functools.lru_cache(maxsize=128)
def fibonacci(n: int) -> int:
    """斐波那契数列 — 用 lru_cache 缓存避免重复计算"""
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


def fibonacci_without_cache(n: int) -> int:
    """对比：没有缓存的版本（指数级慢）"""
    if n < 2:
        return n
    return fibonacci_without_cache(n - 1) + fibonacci_without_cache(n - 2)


@functools.cache
def parse_config(key: str) -> dict[str, Any]:
    """模拟配置解析 — 用 @cache（无限缓存）"""
    time.sleep(0.1)  # 模拟 I/O
    return {"key": key, "value": f"value_for_{key}"}


# ─────────────────────────────────────
# @cached_property：惰性属性
# ─────────────────────────────────────


class DataReport:
    """报表类 — 用 cached_property 惰性计算"""

    def __init__(self, data: list[int]) -> None:
        self.data = data
        self._calc_count = 0

    @functools.cached_property
    def total(self) -> int:
        """总和 — 只计算一次"""
        self._calc_count += 1
        return sum(self.data)

    @functools.cached_property
    def average(self) -> float:
        """平均值 — 只计算一次"""
        self._calc_count += 1
        return sum(self.data) / len(self.data) if self.data else 0.0

    @property
    def calc_count(self) -> int:
        """计算次数 — 验证 cached_property 只执行一次"""
        return self._calc_count


# ─────────────────────────────────────
# @singledispatch：函数重载
# ─────────────────────────────────────


@functools.singledispatch
def process_data(data: Any) -> str:
    """默认处理函数"""
    return f"Unknown type: {type(data).__name__}"


@process_data.register
def _(data: str) -> str:
    return f"String: {data.upper()}"


@process_data.register
def _(data: int) -> str:
    return f"Integer: {data * 2}"


@process_data.register
def _(data: list) -> str:
    return f"List: {len(data)} items"


@process_data.register(dict)
def _(data: dict) -> str:
    return f"Dict: {len(data)} keys"


# ─────────────────────────────────────
# @partial：偏函数
# ─────────────────────────────────────


def format_response(
    status: int, message: str, content_type: str = "application/json"
) -> dict:
    """通用响应格式化函数"""
    return {
        "status": status,
        "content_type": content_type,
        "message": message,
    }


ok_response = functools.partial(format_response, 200, content_type="application/json")
created_response = functools.partial(format_response, 201)
not_found = functools.partial(format_response, 404)
