"""验证器模块 - 正则表达式示例

演示re模块的核心功能:
- 验证邮箱 (re.match)
- 验证手机号
- 验证IP地址
- 验证URL
"""

import re


def validate_email(email: str) -> bool:
    """验证邮箱地址

    Args:
        email: 邗箱地址

    Returns:
        是否有效
    """
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))


def validate_phone(phone: str) -> bool:
    """验证手机号

    Args:
        phone: 手机号

    Returns:
        是否有效
    """
    pattern = r"^1[3-9]\d{9}$"
    return bool(re.match(pattern, phone))


def validate_ip(ip: str) -> bool:
    """验证IP地址

    Args:
        ip: IP地址

    Returns:
        是否有效
    """
    pattern = r"^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$"
    match = re.match(pattern, ip)
    if not match:
        return False
    return all(int(group) <= 255 for group in match.groups())


def validate_url(url: str) -> bool:
    """验证URL

    Args:
        url: URL

    Returns:
        是否有效
    """
    pattern = r"^https?://[^\s]+$"
    return bool(re.match(pattern, url))
