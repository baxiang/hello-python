# 代码质量示例

"""
代码质量示例
包含：类型提示、文档字符串、代码风格、单元测试
"""

from typing import List, Dict, Optional, Callable, Any
from dataclasses import dataclass
from functools import wraps
import time


# 1. 类型提示
def calculate_average(numbers: List[float]) -> float:
    """
    计算平均值
    
    Args:
        numbers: 数字列表
        
    Returns:
        平均值
        
    Raises:
        ValueError: 如果列表为空
    """
    if not numbers:
        raise ValueError("列表不能为空")
    return sum(numbers) / len(numbers)


def find_user(
    users: Dict[str, Dict[str, Any]],
    user_id: str
) -> Optional[Dict[str, Any]]:
    """
    查找用户
    
    Args:
        users: 用户字典
        user_id: 用户ID
        
    Returns:
        用户信息，如果不存在返回 None
    """
    return users.get(user_id)


# 2. 数据类
@dataclass
class User:
    """用户数据类"""
    id: int
    name: str
    email: str
    is_active: bool = True
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "is_active": self.is_active
        }


# 3. 代码风格示例
class Calculator:
    """计算器类
    
    提供基本的数学运算功能。
    
    Attributes:
        history: 计算历史记录
    """
    
    def __init__(self) -> None:
        self._history: List[Dict[str, Any]] = []
    
    def add(self, a: float, b: float) -> float:
        """加法"""
        result = a + b
        self._record("add", a, b, result)
        return result
    
    def subtract(self, a: float, b: float) -> float:
        """减法"""
        result = a - b
        self._record("subtract", a, b, result)
        return result
    
    def multiply(self, a: float, b: float) -> float:
        """乘法"""
        result = a * b
        self._record("multiply", a, b, result)
        return result
    
    def divide(self, a: float, b: float) -> float:
        """除法"""
        if b == 0:
            raise ValueError("除数不能为零")
        result = a / b
        self._record("divide", a, b, result)
        return result
    
    def _record(
        self,
        operation: str,
        a: float,
        b: float,
        result: float
    ) -> None:
        """记录操作"""
        self._history.append({
            "operation": operation,
            "a": a,
            "b": b,
            "result": result,
            "timestamp": time.time()
        })
    
    def get_history(self) -> List[Dict[str, Any]]:
        """获取历史记录"""
        return self._history.copy()


# 4. 单元测试示例
def run_tests() -> None:
    """运行简单测试"""
    print("运行单元测试...")
    
    # 测试 calculate_average
    assert calculate_average([1, 2, 3]) == 2.0
    assert calculate_average([10, 20, 30, 40]) == 25.0
    
    try:
        calculate_average([])
        assert False, "应该抛出异常"
    except ValueError:
        pass
    
    # 测试 Calculator
    calc = Calculator()
    assert calc.add(2, 3) == 5
    assert calc.subtract(10, 4) == 6
    assert calc.multiply(3, 4) == 12
    assert calc.divide(10, 2) == 5
    
    try:
        calc.divide(1, 0)
        assert False, "应该抛出异常"
    except ValueError:
        pass
    
    print("所有测试通过！")


# 5. 代码质量检查装饰器
def validate_input(validator: Callable[[Any], bool]):
    """输入验证装饰器"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            for arg in args:
                if not validator(arg):
                    raise ValueError(f"无效输入: {arg}")
            return func(*args, **kwargs)
        return wrapper
    return decorator


@validate_input(lambda x: x >= 0)
def sqrt_approx(n: float) -> float:
    """近似平方根（仅接受非负数）"""
    return n ** 0.5


if __name__ == "__main__":
    print("=" * 40)
    print("代码质量示例")
    print("=" * 40)
    
    # 类型提示
    print("\n【类型提示】")
    print(f"平均值: {calculate_average([1, 2, 3, 4, 5])}")
    
    # 数据类
    print("\n【数据类】")
    user = User(1, "张三", "zhangsan@example.com")
    print(f"用户: {user}")
    print(f"字典: {user.to_dict()}")
    
    # 计算器
    print("\n【计算器】")
    calc = Calculator()
    print(f"2 + 3 = {calc.add(2, 3)}")
    print(f"10 - 4 = {calc.subtract(10, 4)}")
    print(f"历史记录: {calc.get_history()}")
    
    # 单元测试
    print("\n【单元测试】")
    run_tests()
    
    # 验证装饰器
    print("\n【验证装饰器】")
    print(f"sqrt(16) = {sqrt_approx(16)}")
    try:
        sqrt_approx(-1)
    except ValueError as e:
        print(f"捕获异常: {e}")