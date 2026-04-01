# 装饰器与闭包示例

"""
Python 装饰器与闭包示例
包含：闭包、装饰器、带参数装饰器
"""

from functools import wraps
from time import time
from typing import Callable, Any


# 1. 闭包
def outer(x: int):
    """外层函数"""
    def inner(y: int) -> int:
        """内层函数（闭包）"""
        return x + y
    return inner


def counter():
    """计数器闭包"""
    count = 0
    
    def increment() -> int:
        nonlocal count
        count += 1
        return count
    
    return increment


# 2. 基本装饰器
def log_call(func: Callable) -> Callable:
    """日志装饰器"""
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        print(f"调用函数: {func.__name__}")
        result = func(*args, **kwargs)
        print(f"函数返回: {result}")
        return result
    return wrapper


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


# 3. 带参数装饰器
def repeat(times: int):
    """重复执行装饰器"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            results = []
            for _ in range(times):
                results.append(func(*args, **kwargs))
            return results
        return wrapper
    return decorator


# 4. 类装饰器
class CountCalls:
    """计数类装饰器"""
    
    def __init__(self, func: Callable):
        self.func = func
        self.count = 0
    
    def __call__(self, *args, **kwargs) -> Any:
        self.count += 1
        print(f"第 {self.count} 次调用 {self.func.__name__}")
        return self.func(*args, **kwargs)


# 5. 使用装饰器
@log_call
def add(a: int, b: int) -> int:
    """加法函数"""
    return a + b


@timer
def slow_function():
    """慢函数"""
    import time
    time.sleep(0.1)
    return "完成"


@repeat(3)
def say_hello(name: str) -> str:
    """问候函数"""
    return f"Hello, {name}!"


@CountCalls
def greet(name: str) -> str:
    """问候函数"""
    return f"Hi, {name}!"


# 6. 缓存装饰器
def memoize(func: Callable) -> Callable:
    """缓存装饰器"""
    cache = {}
    
    @wraps(func)
    def wrapper(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    
    return wrapper


@memoize
def fibonacci(n: int) -> int:
    """斐波那契数列（带缓存）"""
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


if __name__ == "__main__":
    print("=" * 40)
    print("装饰器与闭包示例")
    print("=" * 40)
    
    # 闭包
    print("\n【闭包】")
    add_five = outer(5)
    print(f"add_five(3) = {add_five(3)}")
    
    cnt = counter()
    print(f"计数器: {cnt()}, {cnt()}, {cnt()}")
    
    # 基本装饰器
    print("\n【基本装饰器】")
    add(3, 5)
    
    print()
    slow_function()
    
    # 带参数装饰器
    print("\n【带参数装饰器】")
    print(f"repeat(3): {say_hello('Python')}")
    
    # 类装饰器
    print("\n【类装饰器】")
    greet("张三")
    greet("李四")
    
    # 缓存装饰器
    print("\n【缓存装饰器】")
    print(f"fibonacci(10) = {fibonacci(10)}")