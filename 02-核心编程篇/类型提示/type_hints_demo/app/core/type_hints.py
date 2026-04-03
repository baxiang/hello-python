"""类型提示核心示例"""

from typing import Optional, Union, List, Dict, TypeVar, Generic, Protocol, Callable
from dataclasses import dataclass


UserId = int
UserDict = Dict[str, Union[str, int, bool]]


def greet(name: str, age: int) -> str:
    """
    问候函数

    Args:
        name: 用户名
        age: 年龄

    Returns:
        问候语
    """
    return f"Hello {name}, you are {age} years old"


def find_user(user_id: UserId) -> Optional[Dict]:
    """
    查找用户

    Args:
        user_id: 用户ID

    Returns:
        用户信息字典，不存在返回 None
    """
    users: Dict[int, Dict] = {
        1: {"name": "张三", "email": "zhangsan@example.com"},
        2: {"name": "李四", "email": "lisi@example.com"},
    }
    return users.get(user_id)


def process(value: Union[int, str]) -> str:
    """
    处理整数或字符串

    Args:
        value: 整数或字符串

    Returns:
        处理后的字符串
    """
    if isinstance(value, int):
        return f"整数: {value * 2}"
    return f"字符串: {value.upper()}"


@dataclass
class User:
    """用户数据类"""

    id: int
    name: str
    email: str
    age: Optional[int] = None

    def to_dict(self) -> Dict[str, Union[int, str]]:
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "age": self.age or 0,
        }


T = TypeVar("T")


class Stack(Generic[T]):
    """泛型栈"""

    def __init__(self) -> None:
        self._items: List[T] = []

    def push(self, item: T) -> None:
        self._items.append(item)

    def pop(self) -> T:
        if not self._items:
            raise IndexError("栈为空")
        return self._items.pop()

    def peek(self) -> T:
        if not self._items:
            raise IndexError("栈为空")
        return self._items[-1]

    def is_empty(self) -> bool:
        return len(self._items) == 0


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


def apply(func: Callable[[int, int], int], a: int, b: int) -> int:
    """应用函数"""
    return func(a, b)


def add(x: int, y: int) -> int:
    return x + y


def multiply(x: int, y: int) -> int:
    return x * y
