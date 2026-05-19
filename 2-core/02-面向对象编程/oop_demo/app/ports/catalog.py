"""编目与借阅接口定义 — ABC + Protocol

覆盖：ch05 多态、鸭子类型、抽象基类
"""

from abc import ABC, abstractmethod
from typing import Protocol, runtime_checkable


class Catalogable(ABC):
    """可被编目的抽象基类

    所有图书类型都必须实现 get_info() 和 get_isbn()，
    否则无法实例化 → 演示 ABC 的强制接口约束。
    """

    @abstractmethod
    def get_info(self) -> str:
        ...

    @abstractmethod
    def get_isbn(self) -> str:
        ...


@runtime_checkable
class Borrowable(Protocol):
    """可借阅协议 — 鸭子类型

    只要对象拥有这三个方法，就被视为"可借阅"，无需显式继承。
    @runtime_checkable 允许 isinstance() 检查。
    """

    def checkout(self) -> bool:
        ...

    def return_item(self) -> None:
        ...

    def is_available(self) -> bool:
        ...
