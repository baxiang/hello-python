"""日志解析器"""

import re
from datetime import datetime
from dataclasses import dataclass
from typing import Iterator


@dataclass
class LogEntry:
    """日志条目"""
    timestamp: datetime
    level: str
    message: str
    source: str = ""
    extra: dict = None
    
    def __post_init__(self):
        if self.extra is None:
            self.extra = {}


class LogParser:
    """日志解析器"""
    
    # 常见日志格式
    PATTERNS = {
        # Apache/Nginx 格式
        "apache": re.compile(
            r'(\d+\.\d+\.\d+\.\d+) - - \[([^\]]+)\] "([^"]*)" (\d+) (\d+)'
        ),
        # Python logging 格式
        "python": re.compile(
            r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) - (\w+) - ([^\n]+)'
        ),
        # 通用格式
        "generic": re.compile(
            r'\[?([^\]\[]+)]?\s*[\[(]?(INFO|DEBUG|WARN|ERROR|CRITICAL)[\])]?[:\s]*(.+)'
        ),
    }
    
    def __init__(self, format_type: str = "generic"):
        self.format_type = format_type
        self.pattern = self.PATTERNS.get(format_type, self.PATTERNS["generic"])
    
    def parse_line(self, line: str) -> LogEntry | None:
        """解析单行日志"""
        match = self.pattern.match(line.strip())
        if not match:
            return None
        
        groups = match.groups()
        
        if self.format_type == "python":
            timestamp = datetime.strptime(groups[0], "%Y-%m-%d %H:%M:%S")
            level = groups[1]
            message = groups[2]
        elif self.format_type == "apache":
            timestamp = datetime.strptime(groups[1], "%d/%b/%Y:%H:%M:%S")
            level = "INFO"
            message = groups[2]
        else:
            try:
                timestamp = datetime.strptime(groups[0].strip(), "%Y-%m-%d %H:%M:%S")
            except:
                timestamp = datetime.now()
            level = groups[1]
            message = groups[2]
        
        return LogEntry(timestamp=timestamp, level=level, message=message)
    
    def parse_file(self, filepath: str) -> Iterator[LogEntry]:
        """解析日志文件"""
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                entry = self.parse_line(line)
                if entry:
                    yield entry
    
    def parse_lines(self, lines: list[str]) -> list[LogEntry]:
        """解析多行"""
        entries = []
        for line in lines:
            entry = self.parse_line(line)
            if entry:
                entries.append(entry)
        return entries