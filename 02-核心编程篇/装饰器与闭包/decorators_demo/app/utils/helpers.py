"""辅助函数"""

from functools import wraps
from typing import Callable


def counter() -> Callable:
    """计数器闭包"""
    count = 0
    
    def increment() -> int:
        nonlocal count
        count += 1
        return count
    
    return increment