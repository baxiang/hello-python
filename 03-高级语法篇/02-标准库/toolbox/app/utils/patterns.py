"""正则表达式模式模块 - re模块示例

演示re模块的核心功能:
- 预定义正则模式
- 模式匹配 (match/search)
- 全局匹配 (findall)
"""

import re

TIMESTAMP_PATTERN = r"\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}(?:\.\d+)?"
IP_PATTERN = r"(?:\d{1,3}\.){3}\d{1,3}"
EMAIL_PATTERN = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
ERROR_CODE_PATTERN = r"(?:E\d{3}|\d{3})"
LOG_LEVEL_PATTERN = r"(?:DEBUG|INFO|WARN|WARNING|ERROR|CRITICAL)"
URL_PATTERN = r"https?://[^\s]+"
PHONE_PATTERN = r"1[3-9]\d{9}"


def extract_timestamps(text: str) -> list[str]:
    """提取时间戳

    Args:
        text: 文本内容

    Returns:
        时间戳列表
    """
    return re.findall(TIMESTAMP_PATTERN, text)


def extract_ips(text: str) -> list[str]:
    """提取IP地址

    Args:
        text: 文本内容

    Returns:
        IP地址列表
    """
    return re.findall(IP_PATTERN, text)


def extract_emails(text: str) -> list[str]:
    """提取邮箱地址

    Args:
        text: 文本内容

    Returns:
        邗箱列表
    """
    return re.findall(EMAIL_PATTERN, text)


def extract_error_codes(text: str) -> list[str]:
    """提取错误代码

    Args:
        text: 文本内容

    Returns:
        错误代码列表
    """
    return re.findall(ERROR_CODE_PATTERN, text)
