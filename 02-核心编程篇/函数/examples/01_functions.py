# 函数示例

"""
Python 函数示例
包含：函数定义、参数、返回值、高阶函数
"""

from typing import Callable


# 1. 基本函数
def greet(name: str) -> str:
    """问候函数"""
    return f"Hello, {name}!"


# 2. 参数类型
def parameter_types(
    required: str,           # 必需参数
    default: str = "默认值",  # 默认参数
    *args: str,              # 可变位置参数
    **kwargs: int            # 可变关键字参数
) -> dict:
    """演示各种参数类型"""
    return {
        "required": required,
        "default": default,
        "args": args,
        "kwargs": kwargs
    }


# 3. 仅位置参数和仅关键字参数
def special_params(a, b, /, c, d, *, e, f):
    """
    / 之前: 仅位置参数
    * 之后: 仅关键字参数
    """
    return f"a={a}, b={b}, c={c}, d={d}, e={e}, f={f}"


# 4. Lambda 函数
square: Callable[[int], int] = lambda x: x ** 2
add: Callable[[int, int], int] = lambda a, b: a + b


# 5. 高阶函数
def apply_operation(x: int, y: int, operation: Callable[[int, int], int]) -> int:
    """高阶函数：接收函数作为参数"""
    return operation(x, y)


def create_multiplier(n: int) -> Callable[[int], int]:
    """高阶函数：返回函数"""
    return lambda x: x * n


# 6. 递归函数
def factorial(n: int) -> int:
    """阶乘（递归）"""
    if n <= 1:
        return 1
    return n * factorial(n - 1)


def fibonacci(n: int) -> int:
    """斐波那契数列（递归）"""
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


# 7. 生成器函数
def countdown(n: int):
    """倒计时生成器"""
    while n > 0:
        yield n
        n -= 1


if __name__ == "__main__":
    print("=" * 40)
    print("函数示例")
    print("=" * 40)
    
    # 基本函数
    print(f"\n基本函数: {greet('Python')}")
    
    # 参数类型
    result = parameter_types("必需", "自定义", "extra1", "extra2", key1=1, key2=2)
    print(f"\n参数类型: {result}")
    
    # Lambda
    print(f"\nLambda: square(5) = {square(5)}")
    print(f"Lambda: add(3, 4) = {add(3, 4)}")
    
    # 高阶函数
    print(f"\n高阶函数: apply_operation(5, 3, lambda x, y: x * y) = {apply_operation(5, 3, lambda x, y: x * y)}")
    
    double = create_multiplier(2)
    print(f"闭包: double(5) = {double(5)}")
    
    # 递归
    print(f"\n递归: factorial(5) = {factorial(5)}")
    print(f"递归: fibonacci(10) = {fibonacci(10)}")
    
    # 生成器
    print(f"\n生成器: list(countdown(5)) = {list(countdown(5))}")