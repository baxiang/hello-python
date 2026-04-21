"""日志报告模块 - json模块示例

演示json模块的核心功能:
- JSON序列化 (json.dump/dumps)
- JSON反序列化 (json.load/loads)
- 格式化输出 (indent)
- 中文支持 (ensure_ascii=False)
"""

import json
from collections.abc import Sequence
from pathlib import Path

from app.core.log_entry import LogEntry


class LogReport:
    """日志报告生成器"""

    def generate_summary(self, entries: Sequence[LogEntry]) -> dict:
        """生成摘要报告

        Args:
            entries: 日志条目列表

        Returns:
            摘要字典
        """
        return generate_report(entries)

    def to_json(self, entries: Sequence[LogEntry], indent: int | None = None) -> str:
        """转换为JSON字符串

        Args:
            entries: 日志条目列表
            indent: 缩进级别

        Returns:
            JSON字符串
        """
        return json.dumps(
            [e.to_dict() for e in entries],
            indent=indent,
            ensure_ascii=False,
            default=str,
        )

    def save(self, data: dict, filepath: Path | str, indent: int | None = None) -> None:
        """保存报告到文件

        Args:
            data: 数据字典
            filepath: 文件路径
            indent: 缩进级别
        """
        save_report(data, filepath, indent)

    def load(self, filepath: Path | str) -> dict | None:
        """加载报告文件

        Args:
            filepath: 文件路径

        Returns:
            数据字典或None
        """
        return load_report(filepath)


def generate_report(entries: Sequence[LogEntry]) -> dict:
    """生成报告

    Args:
        entries: 日志条目列表

    Returns:
        报告字典
    """
    if not entries:
        return {
            "total_count": 0,
            "level_counts": {},
            "time_range": {"start": None, "end": None},
            "message_count": 0,
        }

    level_counts = {}
    timestamps = []

    for entry in entries:
        level_counts[entry.level] = level_counts.get(entry.level, 0) + 1
        timestamps.append(entry.timestamp)

    sorted_ts = sorted(timestamps)

    return {
        "total_count": len(entries),
        "level_counts": level_counts,
        "time_range": {
            "start": sorted_ts[0].isoformat() if sorted_ts else None,
            "end": sorted_ts[-1].isoformat() if sorted_ts else None,
        },
        "message_count": len(entries),
    }


def save_report(data: dict, filepath: Path | str, indent: int | None = None) -> None:
    """保存报告到文件

    Args:
        data: 数据字典
        filepath: 文件路径
        indent: 缩进级别
    """
    path = Path(filepath)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=indent, ensure_ascii=False, default=str)


def load_report(filepath: Path | str) -> dict | None:
    """加载报告文件

    Args:
        filepath: 文件路径

    Returns:
        数据字典或None
    """
    path = Path(filepath)
    if not path.exists():
        return None
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def export_to_json(
    entries: Sequence[LogEntry], filepath: Path | str, indent: int = 2
) -> None:
    """导出日志到JSON文件

    Args:
        entries: 日志条目列表
        filepath: 文件路径
        indent: 缩进级别
    """
    path = Path(filepath)
    data = [e.to_dict() for e in entries]
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=indent, ensure_ascii=False, default=str)
