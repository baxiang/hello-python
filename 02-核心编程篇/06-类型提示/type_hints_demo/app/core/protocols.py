"""协议示例"""

from typing import Protocol, runtime_checkable, TypedDict


class Drawable(Protocol):
    """绘制协议"""
    
    def draw(self) -> None: ...


class Circle:
    """圆形"""
    
    def draw(self) -> None:
        print("画圆")


class Square:
    """正方形"""
    
    def draw(self) -> None:
        print("画正方形")


def render(shape: Drawable) -> None:
    """渲染图形"""
    shape.draw()


class Comparable(Protocol):
    """可比较协议"""
    
    def compare_to(self, other: "Comparable") -> int: ...


class Person:
    """人员类"""
    
    def __init__(self, name: str, age: int) -> None:
        self.name = name
        self.age = age
    
    def compare_to(self, other: "Person") -> int:
        return self.age - other.age


@runtime_checkable
class Serializable(Protocol):
    """可序列化协议"""
    
    def to_json(self) -> str: ...


class User:
    """用户类"""
    
    def __init__(self, name: str, age: int) -> None:
        self.name = name
        self.age = age
    
    def to_json(self) -> str:
        return f'{{"name": "{self.name}", "age": {self.age}}}'


class UserDict(TypedDict):
    """用户字典类型"""
    
    id: int
    name: str
    email: str
    age: int | None


class ConfigDict(TypedDict, total=False):
    """配置字典类型（所有字段可选）"""
    
    host: str
    port: int
    debug: bool


def create_user(data: UserDict) -> UserDict:
    """创建用户"""
    return data


def find_max(items: list[Comparable]) -> Comparable:
    """找到最大的元素"""
    if not items:
        raise ValueError("列表为空")
    max_item = items[0]
    for item in items[1:]:
        if item.compare_to(max_item) > 0:
            max_item = item
    return max_item