"""辅助函数"""

from importlib import import_module
from typing import Any


def safe_import(module_name: str) -> Any | None:
    """安全导入模块"""
    try:
        return import_module(module_name)
    except ImportError:
        return None