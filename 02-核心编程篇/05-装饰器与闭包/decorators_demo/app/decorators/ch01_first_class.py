"""第 1 章 — 函数是一等公民

演示函数的四大能力：赋值、参数传递、返回值、存储在数据结构。
这是理解装饰器的前置知识。
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

# ─────────────────────────────────────
# 能力 1: 赋值给变量
# ─────────────────────────────────────

def greet(name: str) -> str:
    """基础问候函数"""
    return f"Hello, {name}!"


# 函数可以赋值给变量
say_hello: Callable[[str], str] = greet


# ─────────────────────────────────────
# 能力 2: 作为参数传递
# ─────────────────────────────────────

def execute(func: Callable[[str], str], value: str) -> str:
    """接收一个函数作为参数并调用它"""
    return func(value)


# ─────────────────────────────────────
# 能力 3: 作为返回值
# ─────────────────────────────────────

def get_operation(op: str) -> Callable[[int, int], int]:
    """根据操作名返回对应的计算函数"""
    operations: dict[str, Callable[[int, int], int]] = {
        "add": lambda a, b: a + b,
        "sub": lambda a, b: a - b,
        "mul": lambda a, b: a * b,
    }
    return operations.get(op, lambda _a, _b: 0)


# ─────────────────────────────────────
# 能力 4: 存储在数据结构
# ─────────────────────────────────────

def handle_users(_req: dict[str, Any]) -> dict[str, list[str]]:
    """处理用户请求"""
    return {"users": ["Alice", "Bob", "Charlie"]}


def handle_products(_req: dict[str, Any]) -> dict[str, list[str]]:
    """处理商品请求"""
    return {"products": ["Apple", "Banana"]}


def handle_orders(_req: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    """处理订单请求"""
    return {"orders": [{"id": 1, "user": "Alice"}]}


# 路由表：路径 → 处理函数
routes: dict[str, Callable[[dict[str, Any]], dict[str, Any]]] = {
    "/users": handle_users,
    "/products": handle_products,
    "/orders": handle_orders,
}


def dispatch(path: str, req: dict[str, Any]) -> dict[str, Any] | None:
    """路由分发器 — 根据路径调用对应的处理函数"""
    handler = routes.get(path)
    if handler is None:
        return None
    return handler(req)
