"""元类与子类钩子 — 覆盖第09章、第10章

章节对应：
  ch09  SingletonMeta：自定义 __call__ 拦截实例创建，实现单例模式
        LibraryConfig(metaclass=SingletonMeta)：全局唯一配置对象
  ch10  BookPlugin.__init_subclass__：子类注册时自动执行钩子
        子类通过关键字参数 book_type="..." 完成自动注册
"""

from __future__ import annotations


# ---------------------------------------------------------------------------
# ch09: 元类 — 通过重写 __call__ 控制实例创建
# ---------------------------------------------------------------------------
class SingletonMeta(type):
    """单例元类（ch09）

    工作原理：
      type.__call__(cls, *args, **kwargs)
        → cls.__new__(cls)   创建实例
        → cls.__init__(inst) 初始化
      SingletonMeta.__call__ 在此之前检查缓存，
      若已有实例则直接返回，跳过 __new__ 和 __init__。
    """

    _instances: dict[type, object] = {}

    def __call__(cls, *args: object, **kwargs: object) -> object:
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class LibraryConfig(metaclass=SingletonMeta):
    """全局图书馆配置（ch09：元类实际应用）

    无论在任何地方执行 LibraryConfig()，始终返回同一个对象。
    """

    def __init__(self) -> None:
        self.max_borrow_days: int = 14
        self.max_books_per_member: int = 5
        self.overdue_fine_per_day: float = 0.5   # 单位：元/天

    def __repr__(self) -> str:
        return (
            f"LibraryConfig("
            f"max_days={self.max_borrow_days}, "
            f"max_books={self.max_books_per_member}, "
            f"fine={self.overdue_fine_per_day})"
        )


# ---------------------------------------------------------------------------
# ch10: __init_subclass__ — 子类创建时自动触发钩子，完成插件注册
# ---------------------------------------------------------------------------
class BookPlugin:
    """图书插件基类（ch10：__init_subclass__）

    使用方式：
        class PaperbackPlugin(BookPlugin, book_type="paperback"):
            label = "平装"

    每次定义新子类，Python 自动调用 BookPlugin.__init_subclass__，
    将该子类注册到 _registry，无需手动 register()。
    """

    _registry: dict[str, type[BookPlugin]] = {}

    def __init_subclass__(cls, book_type: str = "", **kwargs: object) -> None:
        super().__init_subclass__(**kwargs)
        if book_type:
            BookPlugin._registry[book_type] = cls

    @classmethod
    def get_plugin(cls, book_type: str) -> type[BookPlugin] | None:
        return cls._registry.get(book_type)

    @classmethod
    def list_types(cls) -> list[str]:
        return sorted(cls._registry.keys())


# 注册三种插件 — 定义即注册，无需额外调用
class PaperbackPlugin(BookPlugin, book_type="paperback"):
    """平装书"""
    label = "平装"


class HardcoverPlugin(BookPlugin, book_type="hardcover"):
    """精装书"""
    label = "精装"


class MagazinePlugin(BookPlugin, book_type="magazine"):
    """期刊"""
    label = "期刊"
