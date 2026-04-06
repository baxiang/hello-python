"""面向对象示例"""

from dataclasses import dataclass
from typing import Any


class Person:
    """人员类"""
    
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age
    
    def __str__(self) -> str:
        return f"Person(name={self.name}, age={self.age})"
    
    def __repr__(self) -> str:
        return f"Person('{self.name}', {self.age})"
    
    def introduce(self) -> str:
        return f"我是 {self.name}，今年 {self.age} 岁"


class Student(Person):
    """学生类"""
    
    def __init__(self, name: str, age: int, grade: str):
        super().__init__(name, age)
        self.grade = grade
    
    def introduce(self) -> str:
        return f"我是 {self.name}，{self.grade} 年级"


class Circle:
    """圆形类"""
    
    def __init__(self, radius: float):
        self._radius = radius
    
    @property
    def radius(self) -> float:
        return self._radius
    
    @radius.setter
    def radius(self, value: float):
        if value < 0:
            raise ValueError("半径不能为负数")
        self._radius = value
    
    @property
    def area(self) -> float:
        return 3.14159 * self._radius ** 2


@dataclass
class Point:
    """点坐标"""
    x: float
    y: float
    
    def distance_to(self, other: "Point") -> float:
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5