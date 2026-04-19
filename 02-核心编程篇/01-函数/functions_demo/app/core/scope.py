"""变量作用域示例 — 覆盖第03章（变量作用域）

章节对应：
  ch03  LEGB 规则：Local → Enclosing → Global → Built-in
        global   修改全局变量（全局调用计数器）
        nonlocal 修改外层函数变量（闭包状态机）
        闭包常见陷阱：循环中捕获变量
"""

from __future__ import annotations


# ---------------------------------------------------------------------------
# ch03: global — 修改全局变量
# ---------------------------------------------------------------------------

_call_count: int = 0   # 全局调用计数器


def record_call() -> int:
    """记录一次调用，返回累计次数（ch03：global）"""
    global _call_count
    _call_count += 1
    return _call_count


def get_call_count() -> int:
    return _call_count


def reset_call_count() -> None:
    global _call_count
    _call_count = 0


# ---------------------------------------------------------------------------
# ch03: nonlocal — 闭包内修改外层变量
# ---------------------------------------------------------------------------

def make_score_accumulator(initial: float = 0.0):
    """工厂函数：返回三个共享同一 total/count 状态的闭包（ch03：nonlocal）

    返回 (add, average, reset) 三个函数，演示 nonlocal 对外层变量的修改。
    """
    total: float = initial
    count: int = 0

    def add(score: float) -> float:
        nonlocal total, count
        total += score
        count += 1
        return total

    def average() -> float:
        return total / count if count > 0 else 0.0

    def reset() -> None:
        nonlocal total, count
        total = initial
        count = 0

    return add, average, reset


# ---------------------------------------------------------------------------
# ch03: 闭包陷阱 — 循环中捕获变量
# ---------------------------------------------------------------------------

def make_grade_checkers_buggy(thresholds: list[float]) -> list:
    """错误写法：所有闭包共享同一个 t 变量（循环结束后 t = 最后的值）

    返回的所有函数都用的是同一个 t，即 thresholds[-1]。
    """
    checkers = []
    for t in thresholds:
        checkers.append(lambda score: score >= t)   # t 是自由变量，循环结束后绑定末尾值
    return checkers


def make_grade_checkers_fixed(thresholds: list[float]) -> list:
    """正确写法：用默认参数在定义时固定 t 的值（ch03：闭包陷阱修复）"""
    return [lambda score, t=t: score >= t for t in thresholds]


# ---------------------------------------------------------------------------
# ch03: LEGB 演示 — 四个作用域层级
# ---------------------------------------------------------------------------

_GRADE_SCALE = 100   # Global


def show_legb(score: float) -> dict[str, object]:
    """展示 LEGB 各层变量（ch03：LEGB 规则）"""
    enclosing_label = "及格线"           # Enclosing（外层函数）

    def inner() -> dict[str, object]:
        local_result = score >= 60       # Local
        return {
            "local_result": local_result,        # L
            "enclosing_label": enclosing_label,  # E
            "global_scale": _GRADE_SCALE,        # G
            "builtin_abs": abs(-score),          # B（内置函数）
        }

    return inner()
