"""辅助函数模块"""

import json
from collections.abc import Sequence


def pretty_print(data) -> str:
    """美化打印JSON

    Args:
        data: 要打印的数据

    Returns:
        格式化的JSON字符串
    """
    return json.dumps(data, ensure_ascii=False, indent=2, default=str)


def format_size(size: int) -> str:
    """格式化文件大小

    Args:
        size: 文件大小(字节)

    Returns:
        格式化的字符串
    """
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024
    return f"{size:.2f} PB"


def truncate_string(s: str, max_length: int = 50, suffix: str = "...") -> str:
    """截断字符串

    Args:
        s: 原始字符串
        max_length: 最大长度
        suffix: 后缀

    Returns:
        截断后的字符串
    """
    if len(s) <= max_length:
        return s
    return s[: max_length - len(suffix)] + suffix


def count_occurrences(items: Sequence, item) -> int:
    """统计出现次数

    Args:
        items: 序列
        item: 要统计的元素

    Returns:
        出现次数
    """
    return sum(1 for i in items if i == item)


def unique_items(items: Sequence) -> list:
    """获取唯一元素列表

    Args:
        items: 序列

    Returns:
        唯一元素列表
    """
    return list(dict.fromkeys(items))


def chunk_list(items: Sequence, chunk_size: int) -> list[list]:
    """分块列表

    Args:
        items: 序列
        chunk_size: 每块大小

    Returns:
        分块后的列表
    """
    return [list(items[i : i + chunk_size]) for i in range(0, len(items), chunk_size)]
