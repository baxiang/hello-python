"""Python 基础语法示例"""

from typing import Any


def demonstrate_variables() -> dict[str, Any]:
    """演示变量和数据类型"""
    name = "Python"          # 字符串
    version = 3.11           # 浮点数
    year = 2024              # 整数
    is_popular = True        # 布尔值
    
    return {
        "name": name,
        "version": version,
        "year": year,
        "is_popular": is_popular
    }


def demonstrate_operators(a: int, b: int) -> dict[str, int | float]:
    """演示运算符"""
    return {
        "add": a + b,
        "subtract": a - b,
        "multiply": a * b,
        "divide": a / b,
        "floor_divide": a // b,
        "modulo": a % b,
        "power": a ** b
    }


def type_conversion(value: str) -> dict[str, Any]:
    """类型转换示例"""
    return {
        "original": value,
        "int": int(value) if value.isdigit() else None,
        "float": float(value) if value.replace(".", "").isdigit() else None,
        "type": type(value).__name__
    }