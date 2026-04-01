# 错误与异常示例

"""
Python 错误与异常示例
包含：异常处理、自定义异常、上下文管理器
"""


# 1. 基本异常处理
def divide(a: int, b: int) -> float | None:
    """除法（带异常处理）"""
    try:
        return a / b
    except ZeroDivisionError:
        print("错误: 除数不能为零")
        return None
    except TypeError as e:
        print(f"类型错误: {e}")
        return None


# 2. 多异常处理
def convert_to_int(value: str) -> int | None:
    """转换为整数"""
    try:
        return int(value)
    except (ValueError, TypeError) as e:
        print(f"转换失败: {e}")
        return None


# 3. finally 和 else
def read_file(filename: str) -> str | None:
    """读取文件"""
    try:
        # 模拟读取
        if filename == "error.txt":
            raise FileNotFoundError(f"文件不存在: {filename}")
        return f"内容: {filename}"
    except FileNotFoundError as e:
        print(f"文件错误: {e}")
        return None
    else:
        print("读取成功")
    finally:
        print("清理资源")


# 4. 自定义异常
class ValidationError(Exception):
    """验证错误"""
    pass


class AgeError(ValidationError):
    """年龄错误"""
    pass


def validate_age(age: int) -> bool:
    """验证年龄"""
    if not isinstance(age, int):
        raise ValidationError("年龄必须是整数")
    if age < 0:
        raise AgeError("年龄不能为负数")
    if age > 150:
        raise AgeError("年龄不合理")
    return True


# 5. 异常链
def process_data(data: dict) -> str:
    """处理数据"""
    try:
        value = data["key"]
        return int(value)
    except KeyError:
        raise ValueError("缺少必要的键") from None
    except ValueError as e:
        raise ValueError("数据格式错误") from e


# 6. 上下文管理器
class Timer:
    """计时上下文管理器"""
    
    def __init__(self, name: str):
        self.name = name
        self.start = None
        self.end = None
    
    def __enter__(self) -> "Timer":
        import time
        self.start = time.time()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        import time
        self.end = time.time()
        print(f"{self.name} 耗时: {self.end - self.start:.4f}s")


# 7. contextlib
from contextlib import contextmanager


@contextmanager
def open_file(filename: str):
    """文件上下文管理器"""
    print(f"打开文件: {filename}")
    try:
        yield f"文件内容: {filename}"
    finally:
        print(f"关闭文件: {filename}")


# 8. 断言
def calculate_average(numbers: list) -> float:
    """计算平均值"""
    assert len(numbers) > 0, "列表不能为空"
    return sum(numbers) / len(numbers)


if __name__ == "__main__":
    print("=" * 40)
    print("错误与异常示例")
    print("=" * 40)
    
    # 基本异常
    print("\n【基本异常处理】")
    print(f"divide(10, 2) = {divide(10, 2)}")
    print(f"divide(10, 0) = {divide(10, 0)}")
    
    # 多异常
    print("\n【多异常处理】")
    print(f"convert_to_int('123') = {convert_to_int('123')}")
    print(f"convert_to_int('abc') = {convert_to_int('abc')}")
    
    # finally/else
    print("\n【finally/else】")
    read_file("test.txt")
    print()
    read_file("error.txt")
    
    # 自定义异常
    print("\n【自定义异常】")
    try:
        validate_age(-5)
    except AgeError as e:
        print(f"捕获异常: {e}")
    
    # 上下文管理器
    print("\n【上下文管理器】")
    with Timer("测试"):
        sum(range(1000000))
    
    # contextlib
    print("\n【contextlib】")
    with open_file("test.txt") as content:
        print(f"内容: {content}")
    
    # 断言
    print("\n【断言】")
    print(f"平均值: {calculate_average([1, 2, 3, 4, 5])}")