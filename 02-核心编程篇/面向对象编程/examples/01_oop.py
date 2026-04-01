# 面向对象编程示例

"""
Python 面向对象编程示例
包含：类定义、继承、多态、魔术方法
"""


# 1. 基本类
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


# 2. 继承
class Student(Person):
    """学生类（继承自 Person）"""
    
    def __init__(self, name: str, age: int, grade: str):
        super().__init__(name, age)
        self.grade = grade
    
    def introduce(self) -> str:
        return f"我是 {self.name}，今年 {self.age} 岁，{self.grade} 年级"


# 3. 多态
class Animal:
    """动物基类"""
    
    def speak(self) -> str:
        raise NotImplementedError


class Dog(Animal):
    def speak(self) -> str:
        return "汪汪汪"


class Cat(Animal):
    def speak(self) -> str:
        return "喵喵喵"


def animal_sound(animal: Animal) -> str:
    """多态示例"""
    return animal.speak()


# 4. 属性装饰器
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
    
    @property
    def circumference(self) -> float:
        return 2 * 3.14159 * self._radius


# 5. 类方法和静态方法
class MathUtils:
    """数学工具类"""
    
    PI = 3.14159
    
    @classmethod
    def circle_area(cls, radius: float) -> float:
        return cls.PI * radius ** 2
    
    @staticmethod
    def add(a: float, b: float) -> float:
        return a + b


# 6. 数据类
from dataclasses import dataclass


@dataclass
class Point:
    """点坐标"""
    x: float
    y: float
    
    def distance_to(self, other: "Point") -> float:
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5


if __name__ == "__main__":
    print("=" * 40)
    print("面向对象编程示例")
    print("=" * 40)
    
    # 基本类
    person = Person("张三", 25)
    print(f"\n基本类: {person}")
    print(f"介绍: {person.introduce()}")
    
    # 继承
    student = Student("李四", 18, "高三")
    print(f"\n继承: {student}")
    print(f"介绍: {student.introduce()}")
    
    # 多态
    print(f"\n多态:")
    print(f"  Dog: {animal_sound(Dog())}")
    print(f"  Cat: {animal_sound(Cat())}")
    
    # 属性装饰器
    circle = Circle(5)
    print(f"\n属性装饰器:")
    print(f"  半径: {circle.radius}")
    print(f"  面积: {circle.area:.2f}")
    print(f"  周长: {circle.circumference:.2f}")
    
    # 类方法和静态方法
    print(f"\n类方法: circle_area(3) = {MathUtils.circle_area(3):.2f}")
    print(f"静态方法: add(3, 4) = {MathUtils.add(3, 4)}")
    
    # 数据类
    p1 = Point(0, 0)
    p2 = Point(3, 4)
    print(f"\n数据类: {p1}, {p2}")
    print(f"距离: {p1.distance_to(p2)}")