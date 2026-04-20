"""辅助函数 — 学生成绩格式化工具"""

from __future__ import annotations


def format_student(record: dict) -> str:
    """将学生记录格式化为单行字符串"""
    name = record.get("name", "?")
    score = record.get("score", 0)
    subject = record.get("subject", "")
    return f"{name} | {subject} | {score:.1f}"


def format_rank_list(ranked: list[tuple[int, dict]]) -> str:
    """将 rank_students() 返回的榜单格式化为多行字符串"""
    if not ranked:
        return "（暂无数据）"
    lines = [f"  第{rank}名  {format_student(s)}" for rank, s in ranked]
    return "\n".join(lines)
