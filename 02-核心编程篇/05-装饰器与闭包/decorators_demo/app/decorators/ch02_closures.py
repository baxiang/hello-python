"""第 2 章 — 闭包与作用域链

演示 LEGB 查找规则、nonlocal 语义、闭包的 __closure__ 属性。
"""

from __future__ import annotations

from collections.abc import Callable

# ─────────────────────────────────────
# LEGB 查找顺序演示
# ─────────────────────────────────────

x: str = "global"


def outer_enclosed() -> Callable[[], str]:
    """演示 E 层（Enclosed）变量查找"""
    x = "enclosed"

    def inner() -> str:
        return x  # 找到 E 层

    return inner


# ─────────────────────────────────────
# 闭包：捕获外层变量
# ─────────────────────────────────────

def make_multiplier(factor: int) -> Callable[[int], int]:
    """创建乘法器 — 最简闭包"""

    def multiply(number: int) -> int:
        return number * factor  # factor 来自闭包

    return multiply


# ─────────────────────────────────────
# nonlocal: 修改外层变量
# ─────────────────────────────────────

def make_counter(start: int = 0) -> Callable[[], int]:
    """计数器闭包 — 用 nonlocal 修改外层变量"""
    count = start

    def increment() -> int:
        nonlocal count
        count += 1
        return count

    return increment


def make_counter_with_ops(start: int = 0) -> dict[str, Callable]:
    """带多种操作的计数器 — 返回函数字典"""
    count = start

    def increment() -> int:
        nonlocal count
        count += 1
        return count

    def decrement() -> int:
        nonlocal count
        count -= 1
        return count

    def get_value() -> int:
        return count

    def reset() -> int:
        nonlocal count
        count = 0
        return count

    return {
        "increment": increment,
        "decrement": decrement,
        "get": get_value,
        "reset": reset,
    }


# ─────────────────────────────────────
# 循环变量陷阱（经典坑）
# ─────────────────────────────────────

def create_multipliers_wrong() -> list[Callable[[int], int]]:
    """❌ 循环变量陷阱 — 所有函数共享同一个 i"""
    return [lambda x: x * i for i in range(5)]  # noqa: B023


def create_multipliers_correct() -> list[Callable[[int], int]]:
    """✅ 用默认参数捕获当前值"""
    return [lambda x, i=i: x * i for i in range(5)]


# ─────────────────────────────────────
# 闭包检查工具
# ─────────────────────────────────────

def inspect_closure(func: Callable) -> dict[str, object]:
    """检查闭包的自由变量"""
    code = func.__code__
    closure = func.__closure__

    return {
        "freevars": code.co_freevars,
        "cell_contents": [cell.cell_contents for cell in closure] if closure else [],
    }
