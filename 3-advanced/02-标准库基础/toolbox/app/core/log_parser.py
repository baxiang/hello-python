"""日志解析模块 - 文件操作和正则表达式示例

演示文件操作和re模块的核心功能:
- 文件读取 (read_text)
- 正则匹配 (re.match/search/findall)
- IP/错误码提取
- 敏感信息屏蔽 (re.sub)
"""

import re
from pathlib import Path

from app.core.log_entry import LogEntry, parse_timestamp
from app.utils.patterns import (
    EMAIL_PATTERN,
    IP_PATTERN,
    LOG_LEVEL_PATTERN,
    PHONE_PATTERN,
    TIMESTAMP_PATTERN,
)


class LogParser:
    """日志文件解析器"""

    def parse_file(
        self, filepath: Path | str, level_filter: str | None = None
    ) -> list[LogEntry]:
        """解析日志文件

        Args:
            filepath: 文件路径
            level_filter: 级别过滤

        Returns:
            日志条目列表
        """
        path = Path(filepath)
        if not path.exists():
            return []

        content = path.read_text()
        lines = content.strip().split("\n")

        entries = []
        for line in lines:
            if not line.strip():
                continue
            entry = parse_log_line(line)
            if entry:
                if level_filter and entry.level != level_filter:
                    continue
                entries.append(entry)

        return entries

    def parse_lines(self, lines: list[str]) -> list[LogEntry]:
        """解析日志行列表

        Args:
            lines: 日志行列表

        Returns:
            日志条目列表
        """
        entries = []
        for line in lines:
            entry = parse_log_line(line)
            if entry:
                entries.append(entry)
        return entries


def parse_log_file(filepath: Path | str) -> list[LogEntry]:
    """解析日志文件

    Args:
        filepath: 文件路径

    Returns:
        日志条目列表
    """
    parser = LogParser()
    return parser.parse_file(filepath)


def parse_log_line(line: str) -> LogEntry | None:
    """解析单行日志

    Args:
        line: 日志行

    Returns:
        LogEntry或None
    """
    ts_match = re.search(TIMESTAMP_PATTERN, line)
    level_match = re.search(LOG_LEVEL_PATTERN, line)

    if not ts_match:
        return None

    timestamp_str = ts_match.group()
    level = level_match.group() if level_match else "INFO"

    message_start = ts_match.end()
    if level_match and level_match.end() > message_start:
        message_start = level_match.end()
    message = line[message_start:].strip()

    return LogEntry(
        timestamp=parse_timestamp(timestamp_str),
        level=level.upper(),
        message=message,
    )


def mask_sensitive_info(text: str) -> str:
    """屏蔽敏感信息

    Args:
        text: 原始文本

    Returns:
        屏蔽后的文本
    """
    masked = re.sub(EMAIL_PATTERN, "***@***.***", text)
    masked = re.sub(PHONE_PATTERN, "**********", masked)
    masked = re.sub(r"\b\d{16,19}\b", "************", masked)
    return masked


def extract_ip_addresses(text: str) -> list[str]:
    """提取IP地址

    Args:
        text: 文本内容

    Returns:
        IP地址列表
    """
    return re.findall(IP_PATTERN, text)


def extract_log_level(text: str) -> str | None:
    """提取日志级别

    Args:
        text: 文本内容

    Returns:
        日志级别或None
    """
    match = re.search(LOG_LEVEL_PATTERN, text)
    return match.group() if match else None
