"""辅助函数"""

from functools import wraps
from typing import Callable, Any


def memoize(func: Callable) -> Callable:
    """缓存装饰器"""
    cache = {}
    
    @wraps(func)
    def wrapper(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    
    return wrapper