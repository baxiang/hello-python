"""工具函数"""

import os
import re
import hashlib
from typing import Any
from pathlib import Path


def file_hash(filepath: str, algorithm: str = "md5") -> str:
    """计算文件哈希"""
    h = hashlib.new(algorithm)
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            h.update(chunk)
    return h.hexdigest()


def find_files(directory: str, pattern: str = "*") -> list[str]:
    """查找文件"""
    path = Path(directory)
    return [str(f) for f in path.glob(pattern) if f.is_file()]


def validate_email(email: str) -> bool:
    """验证邮箱"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_phone(phone: str) -> bool:
    """验证手机号"""
    pattern = r'^1[3-9]\d{9}$'
    return bool(re.match(pattern, phone))


def format_size(size: int) -> str:
    """格式化文件大小"""
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024
    return f"{size:.2f} PB"


def truncate_string(s: str, max_length: int = 50, suffix: str = "...") -> str:
    """截断字符串"""
    if len(s) <= max_length:
        return s
    return s[:max_length - len(suffix)] + suffix