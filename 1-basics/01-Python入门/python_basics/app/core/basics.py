"""Python 基础语法示例"""

from typing import Any


def demonstrate_variables() -> dict[str, Any]:
    """演示变量和数据类型"""
    name = "Python"  # 字符串
    version = 3.11  # 浮点数
    year = 2024  # 整数
    is_popular = True  # 布尔值

    return {"name": name, "version": version, "year": year, "is_popular": is_popular}


def demonstrate_operators(a: int, b: int) -> dict[str, int | float]:
    """演示运算符"""
    return {
        "add": a + b,
        "subtract": a - b,
        "multiply": a * b,
        "divide": a / b,
        "floor_divide": a // b,
        "modulo": a % b,
        "power": a**b,
    }


def type_conversion(value: str) -> dict[str, Any]:
    """类型转换示例"""

    def try_int(s: str) -> int | None:
        try:
            return int(s)
        except ValueError:
            return None

    def try_float(s: str) -> float | None:
        try:
            return float(s)
        except ValueError:
            return None

    return {
        "original": value,
        "int": try_int(value),
        "float": try_float(value),
        "type": type(value).__name__,
    }
