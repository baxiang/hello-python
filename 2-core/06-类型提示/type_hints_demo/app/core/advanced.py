"""高级类型特性示例 — ch03：ParamSpec, Concatenate, Final, ClassVar, TypeGuard"""

import functools
from collections.abc import Callable
from typing import (
    Any,
    ClassVar,
    Concatenate,
    Final,
    ParamSpec,
    TypeGuard,
    TypeVar,
)

P = ParamSpec("P")
R = TypeVar("R")


def log_call(func: Callable[P, R]) -> Callable[P, R]:
    """日志装饰器（ch03：ParamSpec 保留签名）"""

    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        print(f"调用 {func.__name__}")
        return func(*args, **kwargs)

    return wrapper


def with_context(func: Callable[Concatenate[str, P], R]) -> Callable[P, R]:
    """注入上下文参数（ch03：Concatenate 扩展签名）"""

    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        context = "默认上下文"
        return func(context, *args, **kwargs)

    return wrapper


class Config:
    """配置类"""

    MAX_SIZE: Final[int] = 100
    MIN_SIZE: Final[int] = 1
    DEFAULT_PORT: Final[int] = 8080

    def __init__(self, port: int) -> None:
        self.port: Final[int] = port


class BaseService:
    """基础服务"""

    VERSION: ClassVar[str] = "1.0.0"

    def get_version(self) -> str:
        return self.VERSION


def is_string_list(val: list[Any]) -> TypeGuard[list[str]]:
    """类型守卫：检查是否为字符串列表"""
    return all(isinstance(x, str) for x in val)


def is_positive_dict(val: dict[str, Any]) -> TypeGuard[dict[str, int]]:
    """类型守卫：检查是否为正整数值字典"""
    return all(isinstance(v, int) and v > 0 for v in val.values())


def process_data(items: list[Any]) -> str:
    """处理数据"""
    if is_string_list(items):
        return " ".join(items)
    return "非字符串列表"


def sum_values(data: dict[str, Any]) -> int:
    """求和"""
    if is_positive_dict(data):
        return sum(data.values())
    return 0
