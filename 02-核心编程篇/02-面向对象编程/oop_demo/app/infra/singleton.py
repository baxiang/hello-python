"""元类与单例模式

覆盖：ch09 元类 — 通过 __call__ 拦截实例创建
"""

from __future__ import annotations


class SingletonMeta(type):
    """单例元类

    工作原理：
      type.__call__(cls, *args, **kwargs)
        → cls.__new__(cls)   创建实例
        → cls.__init__(inst) 初始化
      SingletonMeta.__call__ 在此之前检查缓存，
      若已有实例则直接返回。
    """

    _instances: dict[type, object] = {}

    def __call__(cls, *args: object, **kwargs: object) -> object:
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class LibraryConfig(metaclass=SingletonMeta):
    """全局图书馆配置

    无论在任何地方执行 LibraryConfig()，始终返回同一个对象。
    """

    def __init__(self) -> None:
        self.max_borrow_days: int = 14
        self.max_books_per_member: int = 5
        self.overdue_fine_per_day: float = 0.5

    def __repr__(self) -> str:
        return (
            f"LibraryConfig("
            f"max_days={self.max_borrow_days}, "
            f"max_books={self.max_books_per_member}, "
            f"fine={self.overdue_fine_per_day})"
        )
