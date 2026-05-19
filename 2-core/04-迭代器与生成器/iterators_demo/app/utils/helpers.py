"""辅助函数 — 日志处理工具"""

from __future__ import annotations

from collections.abc import Generator

from app.core.iterators import LogEntry


def format_log(entry: LogEntry) -> str:
    """格式化单条日志"""
    return f"[{entry.level}] {entry.message}"


def format_log_list(entries: list[LogEntry]) -> str:
    """将日志列表格式化为多行字符串"""
    if not entries:
        return "（暂无日志）"
    return "\n".join(f"  {format_log(e)}" for e in entries)


def batch_generator(
    items: list[LogEntry], batch_size: int
) -> Generator[list[LogEntry], None, None]:
    """批量生成器（ch03：生成器 + 分批处理）

    用法：
        for batch in batch_generator(entries, batch_size=10):
            process_batch(batch)
    """
    for i in range(0, len(items), batch_size):
        yield items[i : i + batch_size]
