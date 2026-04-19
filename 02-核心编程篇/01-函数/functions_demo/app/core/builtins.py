"""Lambda 与内置函数示例 — 覆盖第04章（Lambda）和第05章（内置函数）

章节对应：
  ch04  lambda 语法；lambda 作为 sorted/filter/map 的 key/函数参数
        functools.reduce 与 lambda 组合
  ch05  map / filter / sorted / reversed / enumerate / zip
        any / all / min / max / sum / len
        isinstance / type
"""

from __future__ import annotations

from functools import reduce
from typing import Any


# ---------------------------------------------------------------------------
# ch04: lambda 匿名函数
# ---------------------------------------------------------------------------

# lambda 作为模块级常量（命名的 lambda 用于复用）
SCORE_KEY = lambda s: s["score"]          # 按分数取值
NAME_KEY  = lambda s: s["name"]           # 按姓名取值


def sort_students(
    students: list[dict], *, reverse: bool = False
) -> list[dict]:
    """按分数排序（ch04：lambda 作为 sorted key）"""
    return sorted(students, key=SCORE_KEY, reverse=reverse)


def sort_by_name(students: list[dict]) -> list[dict]:
    """按姓名排序（ch04：lambda key）"""
    return sorted(students, key=NAME_KEY)


def filter_passing(
    students: list[dict], threshold: float = 60.0
) -> list[dict]:
    """筛选及格学生（ch04：lambda + filter）"""
    return list(filter(lambda s: s["score"] >= threshold, students))


def scale_scores(students: list[dict], factor: float) -> list[float]:
    """等比缩放分数（ch04：lambda + map）"""
    return list(map(lambda s: round(s["score"] * factor, 2), students))


def total_score(scores: list[float]) -> float:
    """用 reduce 累加（ch04：lambda + functools.reduce）"""
    if not scores:
        return 0.0
    return reduce(lambda acc, x: acc + x, scores, 0.0)


# ---------------------------------------------------------------------------
# ch05: Python 内置函数
# ---------------------------------------------------------------------------

def score_stats(scores: list[float]) -> dict[str, float]:
    """分数统计：min / max / sum / len（ch05：内置函数）"""
    if not scores:
        return {}
    return {
        "min": min(scores),
        "max": max(scores),
        "total": sum(scores),
        "count": float(len(scores)),
        "average": sum(scores) / len(scores),
    }


def all_passed(students: list[dict], threshold: float = 60.0) -> bool:
    """全部及格（ch05：all）"""
    return all(s["score"] >= threshold for s in students)


def any_excellent(students: list[dict], threshold: float = 90.0) -> bool:
    """存在优秀（ch05：any）"""
    return any(s["score"] >= threshold for s in students)


def rank_students(students: list[dict]) -> list[tuple[int, dict]]:
    """生成带名次的榜单（ch05：enumerate）

    按分数降序排列后，从 1 开始编号。
    """
    sorted_list = sort_students(students, reverse=True)
    return list(enumerate(sorted_list, start=1))


def pair_name_score(
    names: list[str], scores: list[float]
) -> list[dict[str, Any]]:
    """将姓名列表与分数列表合并（ch05：zip）"""
    return [{"name": n, "score": s} for n, s in zip(names, scores)]


def clamp_score(score: float) -> float:
    """将分数限制在 [0, 100]（ch05：max/min 组合）"""
    return max(0.0, min(100.0, score))


def classify_items(items: list[Any]) -> dict[str, list[Any]]:
    """按类型分类（ch05：isinstance / type）"""
    result: dict[str, list[Any]] = {"int": [], "float": [], "str": [], "other": []}
    for item in items:
        if isinstance(item, bool):          # bool 是 int 子类，需先判断
            result["other"].append(item)
        elif isinstance(item, int):
            result["int"].append(item)
        elif isinstance(item, float):
            result["float"].append(item)
        elif isinstance(item, str):
            result["str"].append(item)
        else:
            result["other"].append(item)
    return result


def top_n(students: list[dict], n: int) -> list[dict]:
    """取分数前 n 名（ch05：sorted + 切片）"""
    return sorted(students, key=SCORE_KEY, reverse=True)[:n]
