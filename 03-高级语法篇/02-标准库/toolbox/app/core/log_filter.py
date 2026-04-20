"""日志过滤模块 - datetime和pathlib组合示例

演示datetime和pathlib模块的核心功能:
- 时间范围过滤 (datetime比较)
- 级别过滤
- 路径模式过滤 (glob)
- 工作日过滤 (weekday)
"""

import re
from collections.abc import Sequence
from datetime import datetime

from app.core.log_entry import LogEntry, is_weekday


class LogFilter:
    """日志过滤器"""

    def filter_by_time_range(
        self,
        entries: Sequence[LogEntry],
        start: datetime | None = None,
        end: datetime | None = None,
    ) -> list[LogEntry]:
        """按时间范围过滤

        Args:
            entries: 日志条目列表
            start: 开始时间
            end: 结束时间

        Returns:
            过滤后的日志条目
        """
        return filter_by_time_range(entries, start, end)

    def filter_by_level(
        self, entries: Sequence[LogEntry], levels: Sequence[str]
    ) -> list[LogEntry]:
        """按级别过滤

        Args:
            entries: 日志条目列表
            levels: 级别列表

        Returns:
            过滤后的日志条目
        """
        return filter_by_level(entries, levels)

    def filter_by_weekday(
        self, entries: Sequence[LogEntry], weekdays_only: bool = True
    ) -> list[LogEntry]:
        """按工作日/周末过滤

        Args:
            entries: 日志条目列表
            weekdays_only: True表示只保留工作日

        Returns:
            过滤后的日志条目
        """
        return filter_by_weekday(entries, weekdays_only)

    def filter_by_pattern(
        self, entries: Sequence[LogEntry], pattern: str
    ) -> list[LogEntry]:
        """按消息模式过滤

        Args:
            entries: 日志条目列表
            pattern: 正则模式

        Returns:
            过滤后的日志条目
        """
        return filter_by_pattern(entries, pattern)

    def filter_by_source(
        self, entries: Sequence[LogEntry], sources: Sequence[str]
    ) -> list[LogEntry]:
        """按来源过滤

        Args:
            entries: 日志条目列表
            sources: 来源列表

        Returns:
            过滤后的日志条目
        """
        return [e for e in entries if e.source and e.source in sources]


def filter_by_time_range(
    entries: Sequence[LogEntry],
    start: datetime | None = None,
    end: datetime | None = None,
) -> list[LogEntry]:
    """按时间范围过滤

    Args:
        entries: 日志条目列表
        start: 开始时间
        end: 结束时间

    Returns:
        过滤后的日志条目
    """
    result = []
    for entry in entries:
        if start and entry.timestamp < start:
            continue
        if end and entry.timestamp > end:
            continue
        result.append(entry)
    return result


def filter_by_level(
    entries: Sequence[LogEntry], levels: Sequence[str]
) -> list[LogEntry]:
    """按级别过滤

    Args:
        entries: 日志条目列表
        levels: 级别列表

    Returns:
        过滤后的日志条目
    """
    level_set = set(levels)
    return [e for e in entries if e.level in level_set]


def filter_by_weekday(
    entries: Sequence[LogEntry], weekdays_only: bool = True
) -> list[LogEntry]:
    """按工作日/周末过滤

    Args:
        entries: 日志条目列表
        weekdays_only: True表示只保留工作日

    Returns:
        过滤后的日志条目
    """
    return [e for e in entries if is_weekday(e.timestamp) == weekdays_only]


def filter_by_pattern(entries: Sequence[LogEntry], pattern: str) -> list[LogEntry]:
    """按消息模式过滤

    Args:
        entries: 日志条目列表
        pattern: 正则模式

    Returns:
        过滤后的日志条目
    """
    regex = re.compile(pattern)
    return [e for e in entries if regex.search(e.message)]
