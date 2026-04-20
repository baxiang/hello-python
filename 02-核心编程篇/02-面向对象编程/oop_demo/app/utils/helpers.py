"""辅助函数 — 图书馆常用工具"""

from __future__ import annotations

import hashlib


def generate_member_id(name: str) -> str:
    """根据姓名生成6位大写十六进制会员号，前缀 M"""
    return "M" + hashlib.md5(name.encode()).hexdigest()[:6].upper()


def format_book_list(books: list) -> str:
    """将图书列表格式化为带编号的可读字符串"""
    if not books:
        return "（暂无图书）"
    return "\n".join(f"  {i + 1}. {book}" for i, book in enumerate(books))
