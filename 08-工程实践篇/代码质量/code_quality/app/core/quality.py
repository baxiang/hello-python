"""代码质量示例"""

from typing import List, Dict, Any
from dataclasses import dataclass


@dataclass
class User:
    """用户数据类"""
    id: int
    name: str
    email: str
    is_active: bool = True
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "is_active": self.is_active
        }


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


class Calculator:
    """计算器类"""
    
    def add(self, a: float, b: float) -> float:
        """加法"""
        return a + b
    
    def subtract(self, a: float, b: float) -> float:
        """减法"""
        return a - b
    
    def multiply(self, a: float, b: float) -> float:
        """乘法"""
        return a * b
    
    def divide(self, a: float, b: float) -> float:
        """除法"""
        if b == 0:
            raise ValueError("除数不能为零")
        return a / b