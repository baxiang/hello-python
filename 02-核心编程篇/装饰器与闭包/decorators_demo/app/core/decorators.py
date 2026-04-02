"""装饰器示例"""

from functools import wraps
from time import time
from typing import Callable, Any


def timer(func: Callable) -> Callable:
    """计时装饰器"""
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        start = time()
        result = func(*args, **kwargs)
        end = time()
        print(f"{func.__name__} 执行时间: {end - start:.4f}s")
        return result
    return wrapper


def log_call(func: Callable) -> Callable:
    """日志装饰器"""
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        print(f"调用函数: {func.__name__}")
        result = func(*args, **kwargs)
        print(f"函数返回: {result}")
        return result
    return wrapper


def repeat(times: int):
    """重复执行装饰器"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> list:
            results = []
            for _ in range(times):
                results.append(func(*args, **kwargs))
            return results
        return wrapper
    return decorator


def memoize(func: Callable) -> Callable:
    """缓存装饰器"""
    cache = {}
    
    @wraps(func)
    def wrapper(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    
    return wrapper


class CountCalls:
    """计数类装饰器"""
    
    def __init__(self, func: Callable):
        self.func = func
        self.count = 0
    
    def __call__(self, *args, **kwargs) -> Any:
        self.count += 1
        print(f"第 {self.count} 次调用 {self.func.__name__}")
        return self.func(*args, **kwargs)