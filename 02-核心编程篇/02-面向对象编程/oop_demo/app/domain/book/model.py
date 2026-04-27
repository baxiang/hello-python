"""图书领域模型 — BookItem 层次结构

覆盖：ch01 类定义、ch02 类属性/方法、ch03 继承/Mixin、
      ch04 封装/@property、ch05 接口实现、ch08 魔术方法
"""

from __future__ import annotations

from app.domain.book.mixins import DigitalMixin
from app.ports.catalog import Catalogable


class BookItem(Catalogable):
    """图书基类 — 所有图书类型的抽象基础

    核心职责：
      - 唯一标识（ISBN）
      - 借阅状态管理
      - 编目信息展示
    """

    total_books: int = 0

    def __init__(self, title: str, author: str, isbn: str, year: int) -> None:
        self.title: str = title
        self.author: str = author
        self._isbn: str = isbn
        self._year: int = year
        self._available: bool = True
        BookItem.total_books += 1

    # ---- 属性访问 ----

    @property
    def isbn(self) -> str:
        return self._isbn

    @property
    def year(self) -> int:
        return self._year

    @property
    def available(self) -> bool:
        return self._available

    # ---- 类方法 / 静态方法 ----

    @classmethod
    def get_total(cls) -> int:
        return cls.total_books

    @staticmethod
    def validate_isbn(isbn: str) -> bool:
        """校验 ISBN 格式（10位或13位纯数字，允许连字符）"""
        digits = isbn.replace("-", "")
        return len(digits) in (10, 13) and digits.isdigit()

    # ---- Catalogable 接口实现 ----

    def get_isbn(self) -> str:
        return self._isbn

    def get_info(self) -> str:
        return f"[{self._isbn}] {self.title} — {self.author} ({self._year})"

    # ---- 借阅操作 ----

    def checkout(self) -> bool:
        if self._available:
            self._available = False
            return True
        return False

    def return_item(self) -> None:
        self._available = True

    def is_available(self) -> bool:
        return self._available

    # ---- 魔术方法 ----

    def __str__(self) -> str:
        status = "可借" if self._available else "已借出"
        return f"《{self.title}》{self.author}（{status}）"

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"title={self.title!r}, isbn={self._isbn!r})"
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, BookItem):
            return NotImplemented
        return self._isbn == other._isbn

    def __hash__(self) -> int:
        return hash(self._isbn)

    def __lt__(self, other: BookItem) -> bool:
        return self.title < other.title


class PhysicalBook(BookItem):
    """实体书 — 通过页数区分"""

    def __init__(
        self, title: str, author: str, isbn: str, year: int, pages: int
    ) -> None:
        super().__init__(title, author, isbn, year)
        self._pages: int = pages

    @property
    def pages(self) -> int:
        return self._pages

    def get_info(self) -> str:
        return f"{super().get_info()} | {self._pages} 页"

    def __repr__(self) -> str:
        return f"PhysicalBook(title={self.title!r}, pages={self._pages})"


class EBook(BookItem):
    """电子书 — 含私有属性与 setter 验证"""

    def __init__(
        self,
        title: str,
        author: str,
        isbn: str,
        year: int,
        file_size_mb: float,
        fmt: str = "PDF",
    ) -> None:
        super().__init__(title, author, isbn, year)
        self.__file_size_mb: float = file_size_mb
        self._format: str = fmt

    @property
    def file_size_mb(self) -> float:
        return self.__file_size_mb

    @file_size_mb.setter
    def file_size_mb(self, value: float) -> None:
        if value <= 0:
            raise ValueError("文件大小必须大于 0 MB")
        self.__file_size_mb = value

    @property
    def format(self) -> str:
        return self._format

    def get_info(self) -> str:
        return f"{super().get_info()} | {self._format} {self.__file_size_mb:.1f} MB"

    def __repr__(self) -> str:
        return (
            f"EBook(title={self.title!r}, "
            f"format={self._format!r}, size={self.__file_size_mb})"
        )


class AudioBook(PhysicalBook, DigitalMixin):
    """有声书 — 多重继承 (PhysicalBook + DigitalMixin)

    MRO: AudioBook → PhysicalBook → BookItem → Catalogable → DigitalMixin → object
    """

    def __init__(
        self,
        title: str,
        author: str,
        isbn: str,
        year: int,
        pages: int,
        file_size_mb: float,
    ) -> None:
        super().__init__(title, author, isbn, year, pages)
        self._file_size_mb = file_size_mb
        self._format = "MP3"

    def get_info(self) -> str:
        return f"{super().get_info()} | 有声书 {self.download_info()}"

    def __repr__(self) -> str:
        return (
            f"AudioBook(title={self.title!r}, "
            f"pages={self._pages}, size={self._file_size_mb})"
        )
