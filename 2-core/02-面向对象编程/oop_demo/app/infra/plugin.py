"""插件注册 — __init_subclass__ 自动钩子

覆盖：ch10 子类创建时自动触发钩子
"""

from __future__ import annotations


class BookPlugin:
    """图书插件基类

    使用方式：
        class PaperbackPlugin(BookPlugin, book_type="paperback"):
            label = "平装"

    每次定义新子类，Python 自动调用 __init_subclass__，
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


# 预注册插件 — 定义即注册
class PaperbackPlugin(BookPlugin, book_type="paperback"):
    label = "平装"


class HardcoverPlugin(BookPlugin, book_type="hardcover"):
    label = "精装"


class MagazinePlugin(BookPlugin, book_type="magazine"):
    label = "期刊"
