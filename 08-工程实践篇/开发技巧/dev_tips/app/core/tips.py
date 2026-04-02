"""开发技巧示例"""

import time
import functools
from typing import Callable, Any


def timer(func: Callable) -> Callable:
    """计时装饰器"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"{func.__name__} 耗时: {end - start:.6f}s")
        return result
    return wrapper


@functools.lru_cache(maxsize=128)
def fibonacci_cached(n: int) -> int:
    """带缓存的斐波那契"""
    if n <= 1:
        return n
    return fibonacci_cached(n - 1) + fibonacci_cached(n - 2)


class Timer:
    """计时上下文管理器"""
    
    def __init__(self, name: str = "操作"):
        self.name = name
        self.start = None
        self.end = None
    
    def __enter__(self) -> "Timer":
        self.start = time.perf_counter()
        return self
    
    def __exit__(self, *args):
        self.end = time.perf_counter()
        print(f"{self.name} 耗时: {self.end - self.start:.6f}s")


def profile_function(func: Callable, *args, **kwargs) -> dict:
    """分析函数性能"""
    start = time.perf_counter()
    result = func(*args, **kwargs)
    end = time.perf_counter()
    
    return {
        "function": func.__name__,
        "duration": end - start,
        "result": result
    }