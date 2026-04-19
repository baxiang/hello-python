"""抽象接口定义 — 对应第05章：多态、鸭子类型、抽象基类"""

from abc import ABC, abstractmethod
from typing import Protocol, runtime_checkable


class Catalogable(ABC):
    """可被编目的抽象基类（ABC）

    所有图书类型都必须实现 get_info() 和 get_isbn()，
    否则无法实例化 → 演示 ABC 的强制接口约束。
    """

    @abstractmethod
    def get_info(self) -> str:
        """返回图书详细信息"""
        ...

    @abstractmethod
    def get_isbn(self) -> str:
        """返回 ISBN 编号"""
        ...


@runtime_checkable
class Borrowable(Protocol):
    """可借阅协议（Protocol）

    鸭子类型：只要对象拥有这三个方法，
    就被视为"可借阅"，无需显式继承。
    @runtime_checkable 允许 isinstance() 检查。
    """

    def checkout(self) -> bool:
        """借出，成功返回 True；已借出返回 False"""
        ...

    def return_item(self) -> None:
        """归还"""
        ...

    def is_available(self) -> bool:
        """是否可借"""
        ...
