"""基础语法示例"""

from typing import Any


def check_score(score: int) -> str:
    """根据分数判断等级"""
    if score >= 90:
        return "优秀"
    elif score >= 80:
        return "良好"
    elif score >= 60:
        return "及格"
    else:
        return "不及格"


def loop_examples(n: int) -> list[int]:
    """循环示例"""
    results = []
    for i in range(n):
        results.append(i + 1)
    return results


def comprehension_examples() -> dict[str, list[int]]:
    """推导式示例"""
    return {
        "squares": [x ** 2 for x in range(10)],
        "even_squares": [x ** 2 for x in range(10) if x % 2 == 0],
        "cube": [x ** 3 for x in range(5)]
    }


def match_example(status: int) -> str:
    """match 语句示例 (Python 3.10+)"""
    match status:
        case 200:
            return "OK"
        case 404:
            return "Not Found"
        case 500:
            return "Server Error"
        case _:
            return "Unknown"