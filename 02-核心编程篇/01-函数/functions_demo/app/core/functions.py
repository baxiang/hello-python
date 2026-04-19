"""函数核心示例 — 覆盖第01章（函数基础）和第02章（函数参数详解）

场景：学生成绩统计系统

章节对应：
  ch01  letter_grade / calculate_average  基础函数定义与调用
        apply_to_all / make_threshold_checker  高阶函数 + 函数作为返回值
        merge_sort  递归
  ch02  create_student  全部参数类型：位置/默认/*args/**kwargs/keyword-only/positional-only
        summarize  **kwargs 场景化应用
"""

from __future__ import annotations

from typing import Any, Callable


# ---------------------------------------------------------------------------
# ch01: 函数基础 — 定义、调用、返回值、高阶函数、递归
# ---------------------------------------------------------------------------

def letter_grade(score: float) -> str:
    """按百分制返回等级（ch01：基础函数）"""
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    elif score >= 60:
        return "D"
    return "F"


def calculate_average(scores: list[float]) -> float:
    """计算平均分（ch01：基础函数）"""
    if not scores:
        return 0.0
    return sum(scores) / len(scores)


def apply_to_all(
    scores: list[float], transform: Callable[[float], float]
) -> list[float]:
    """对所有分数应用变换（ch01：高阶函数——函数作为参数）"""
    return [transform(s) for s in scores]


def make_threshold_checker(threshold: float) -> Callable[[float], bool]:
    """返回一个"是否达线"检查函数（ch01：函数作为返回值）"""
    def checker(score: float) -> bool:
        return score >= threshold
    return checker


def merge_sort(items: list[float]) -> list[float]:
    """归并排序（ch01：递归）

    拆分 → 递归排序左右子列 → 合并
    """
    if len(items) <= 1:
        return list(items)
    mid = len(items) // 2
    left = merge_sort(items[:mid])
    right = merge_sort(items[mid:])
    return _merge(left, right)


def _merge(left: list[float], right: list[float]) -> list[float]:
    result: list[float] = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


# ---------------------------------------------------------------------------
# ch02: 函数参数详解
# ---------------------------------------------------------------------------

def create_student(
    name: str,              # 位置参数
    score: float,           # 位置参数
    subject: str = "数学",  # 默认参数
    /,                      # positional-only 分隔符（以上三个只能按位置传入）
    *tags: str,             # *args — 收集额外标签
    comment: str = "",      # keyword-only（* 之后必须用关键字传入）
    rank: int | None = None,
) -> dict[str, Any]:
    """创建学生成绩记录（ch02：演示所有参数类型）

    调用示例：
        create_student("张三", 85)
        create_student("李四", 92, "英语", "努力", "进步大", comment="表现优秀")
    """
    return {
        "name": name,
        "score": score,
        "subject": subject,
        "tags": tags,
        "comment": comment,
        "rank": rank,
    }


def summarize(**scores: float) -> dict[str, float]:
    """按科目汇总任意数量的分数（ch02：**kwargs）

    调用示例：
        summarize(数学=90, 英语=85, 物理=78)
    """
    return dict(scores)