"""函数示例"""

from typing import Callable, Any


def greet(name: str) -> str:
    """问候函数"""
    return f"Hello, {name}!"


def parameter_types(required: str, default: str = "默认值", *args: str, **kwargs: int) -> dict:
    """演示各种参数类型"""
    return {
        "required": required,
        "default": default,
        "args": args,
        "kwargs": kwargs
    }


def apply_operation(x: int, y: int, operation: Callable[[int, int], int]) -> int:
    """高阶函数"""
    return operation(x, y)


def create_multiplier(n: int) -> Callable[[int], int]:
    """闭包"""
    return lambda x: x * n


def factorial(n: int) -> int:
    """递归函数"""
    if n <= 1:
        return 1
    return n * factorial(n - 1)


def fibonacci(n: int) -> int:
    """斐波那契数列"""
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)