# 开发技巧示例

"""
开发技巧示例
包含：调试技巧、性能优化、代码重构
"""

import time
import functools
import cProfile
import pstats
from io import StringIO
from typing import Callable, Any
from contextlib import contextmanager


# 1. 调试技巧
def debug_print(*args, **kwargs):
    """调试打印"""
    import inspect
    caller = inspect.currentframe().f_back
    print(f"[{caller.f_code.co_filename}:{caller.f_lineno}] ", end="")
    print(*args, **kwargs)


def debug_variables(**variables):
    """打印变量"""
    for name, value in variables.items():
        print(f"  {name} = {value!r}")


# 2. 计时装饰器
def timer(func: Callable) -> Callable:
    """计时装饰器"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"{func.__name__} 耗时: {end - start:.6f}s")
        return result
    return wrapper


# 3. 性能分析
@contextmanager
def profile_context(sort_by: str = "cumulative"):
    """性能分析上下文"""
    profiler = cProfile.Profile()
    profiler.enable()
    yield
    profiler.disable()
    
    stream = StringIO()
    stats = pstats.Stats(profiler, stream=stream)
    stats.sort_stats(sort_by)
    stats.print_stats(10)
    print(stream.getvalue())


# 4. 缓存优化
@functools.lru_cache(maxsize=128)
def fibonacci_cached(n: int) -> int:
    """带缓存的斐波那契"""
    if n <= 1:
        return n
    return fibonacci_cached(n - 1) + fibonacci_cached(n - 2)


def fibonacci_no_cache(n: int) -> int:
    """不带缓存的斐波那契"""
    if n <= 1:
        return n
    return fibonacci_no_cache(n - 1) + fibonacci_no_cache(n - 2)


# 5. 列表推导式优化
def slow_way(n: int) -> list:
    """慢速方式"""
    result = []
    for i in range(n):
        result.append(i ** 2)
    return result


def fast_way(n: int) -> list:
    """快速方式（列表推导式）"""
    return [i ** 2 for i in range(n)]


# 6. 字符串拼接优化
def slow_concat(parts: list) -> str:
    """慢速字符串拼接"""
    result = ""
    for part in parts:
        result += part
    return result


def fast_concat(parts: list) -> str:
    """快速字符串拼接"""
    return "".join(parts)


# 7. 代码重构示例
# 重构前
def process_data_before(data):
    result = []
    for item in data:
        if item > 0:
            result.append(item * 2)
    return result


# 重构后
def process_data_after(data: list) -> list:
    """处理数据（重构后）"""
    return [item * 2 for item in data if item > 0]


# 8. 异常处理最佳实践
def safe_divide(a: float, b: float) -> float | None:
    """安全除法"""
    try:
        return a / b
    except ZeroDivisionError:
        print("警告: 除数为零")
        return None
    except TypeError as e:
        print(f"类型错误: {e}")
        return None


# 9. 上下文管理器
class Timer:
    """计时上下文管理器"""
    
    def __init__(self, name: str = "操作"):
        self.name = name
        self.start = None
        self.end = None
    
    def __enter__(self):
        self.start = time.perf_counter()
        return self
    
    def __exit__(self, *args):
        self.end = time.perf_counter()
        print(f"{self.name} 耗时: {self.end - self.start:.6f}s")


if __name__ == "__main__":
    print("=" * 40)
    print("开发技巧示例")
    print("=" * 40)
    
    # 计时装饰器
    print("\n【计时装饰器】")
    
    @timer
    def slow_function():
        time.sleep(0.1)
        return "完成"
    
    slow_function()
    
    # 缓存优化
    print("\n【缓存优化】")
    
    with Timer("带缓存"):
        result = fibonacci_cached(35)
        print(f"fibonacci(35) = {result}")
    
    # 列表推导式
    print("\n【列表推导式优化】")
    
    with Timer("列表推导式"):
        fast_way(100000)
    
    # 字符串拼接
    print("\n【字符串拼接优化】")
    parts = ["hello"] * 10000
    
    with Timer("join 拼接"):
        fast_concat(parts)
    
    # 性能分析
    print("\n【性能分析】")
    
    def test_function():
        return sum(i ** 2 for i in range(10000))
    
    with profile_context():
        test_function()
    
    # 代码重构
    print("\n【代码重构】")
    data = [-2, -1, 0, 1, 2, 3, 4, 5]
    print(f"重构前: {process_data_before(data)}")
    print(f"重构后: {process_data_after(data)}")