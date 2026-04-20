"""日志条目模块 - datetime模块示例

演示datetime模块的核心功能:
- datetime解析 (strptime)
- datetime格式化 (strftime)
- 时间差计算 (timedelta)
- 工作日判断 (weekday)
"""

from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass
class LogEntry:
    """日志条目类"""

    timestamp: datetime
    level: str
    message: str
    source: str | None = None

    def to_dict(self) -> dict:
        return {
            "timestamp": self.timestamp.isoformat(),
            "level": self.level,
            "message": self.message,
            "source": self.source,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "LogEntry":
        ts = data["timestamp"]
        if isinstance(ts, str):
            ts = parse_timestamp(ts)
        return cls(
            timestamp=ts,
            level=data["level"],
            message=data["message"],
            source=data.get("source"),
        )

    def time_since(self, other: "LogEntry") -> timedelta:
        return self.timestamp - other.timestamp

    def seconds_since(self, other: "LogEntry") -> float:
        return (self.timestamp - other.timestamp).total_seconds()

    def __str__(self) -> str:
        return f"[{format_timestamp(self.timestamp)}] {self.level}: {self.message}"


def parse_timestamp(ts_str: str, format: str | None = None) -> datetime:
    """解析时间戳字符串

    Args:
        ts_str: 时间戳字符串
        format: 可选的自定义格式

    Returns:
        datetime对象
    """
    if format:
        return datetime.strptime(ts_str, format)

    iso_formats = [
        "%Y-%m-%dT%H:%M:%S.%f",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%d %H:%M:%S.%f",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d",
    ]

    for fmt in iso_formats:
        try:
            return datetime.strptime(ts_str, fmt)
        except ValueError:
            continue

    raise ValueError(f"无法解析时间戳: {ts_str}")


def format_timestamp(ts: datetime, fmt: str | None = None) -> str:
    """格式化时间戳

    Args:
        ts: datetime对象
        fmt: 可选的自定义格式

    Returns:
        格式化后的字符串
    """
    if fmt:
        return ts.strftime(fmt)
    return ts.strftime("%Y-%m-%dT%H:%M:%S")


def is_weekday(ts: datetime) -> bool:
    """判断是否为工作日

    Args:
        ts: datetime对象

    Returns:
        True表示工作日(周一到周五)
    """
    return ts.weekday() < 5
