"""图书类层次结构 — 覆盖第01-05章、第08章

章节对应：
  ch01  BookItem 基础类定义
  ch02  类属性 total_books、@classmethod、@staticmethod
  ch03  PhysicalBook / EBook 继承、super()；AudioBook 多重继承 + Mixin
  ch04  EBook.__file_size_mb 私有属性；@property 带验证的 setter
  ch05  Catalogable(ABC) 强制接口；Borrowable(Protocol) 鸭子类型
  ch08  __str__ / __repr__ / __eq__ / __hash__ / __lt__
"""

from __future__ import annotations

from app.core.catalog import Catalogable, Borrowable


# ---------------------------------------------------------------------------
# ch03: Mixin — 为多重继承提供数字内容能力，自身不继承 Catalogable
# ---------------------------------------------------------------------------
class DigitalMixin:
    """数字内容 Mixin：提供文件信息，用于多重继承演示（ch03）"""

    _file_size_mb: float
    _format: str

    def download_info(self) -> str:
        return f"{self._format} | {self._file_size_mb:.1f} MB"


# ---------------------------------------------------------------------------
# ch01 / ch02 / ch04 / ch05 / ch08: 图书基类
# ---------------------------------------------------------------------------
class BookItem(Catalogable):
    """图书基类 — 实现 Catalogable 接口，同时满足 Borrowable 协议

    ch01: 类的定义与实例化
    ch02: total_books 类属性；get_total 类方法；validate_isbn 静态方法
    ch04: _isbn / _available 受保护属性；isbn / available @property
    ch05: 实现 Catalogable(ABC)；checkout/return_item 满足 Borrowable(Protocol)
    ch08: __str__ / __repr__ / __eq__ / __hash__ / __lt__
    """

    # ch02: 类属性 — 所有实例共享，记录创建总数
    total_books: int = 0

    def __init__(self, title: str, author: str, isbn: str, year: int) -> None:
        # ch02: 实例属性
        self.title: str = title
        self.author: str = author
        self._isbn: str = isbn          # ch04: 受保护，外部通过 @property 访问
        self._year: int = year
        self._available: bool = True
        BookItem.total_books += 1

    # ch04: @property — 只读
    @property
    def isbn(self) -> str:
        return self._isbn

    @property
    def year(self) -> int:
        return self._year

    @property
    def available(self) -> bool:
        return self._available

    # ch02: 类方法 — 访问类属性
    @classmethod
    def get_total(cls) -> int:
        """返回已创建的图书总数"""
        return cls.total_books

    # ch02: 静态方法 — 与实例无关的工具函数
    @staticmethod
    def validate_isbn(isbn: str) -> bool:
        """校验 ISBN 格式（10位或13位纯数字，允许连字符）"""
        digits = isbn.replace("-", "")
        return len(digits) in (10, 13) and digits.isdigit()

    # ch05: 实现 Catalogable ABC 的抽象方法
    def get_isbn(self) -> str:
        return self._isbn

    def get_info(self) -> str:
        return f"[{self._isbn}] {self.title} — {self.author} ({self._year})"

    # ch05: 满足 Borrowable Protocol（鸭子类型，无需显式继承）
    def checkout(self) -> bool:
        if self._available:
            self._available = False
            return True
        return False

    def return_item(self) -> None:
        self._available = True

    def is_available(self) -> bool:
        return self._available

    # ch08: 魔术方法
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
        """按书名排序，支持 sorted() 和比较运算符"""
        return self.title < other.title


# ---------------------------------------------------------------------------
# ch03: 单继承 — PhysicalBook
# ---------------------------------------------------------------------------
class PhysicalBook(BookItem):
    """实体书（ch03：继承与 super()）"""

    def __init__(
        self, title: str, author: str, isbn: str, year: int, pages: int
    ) -> None:
        super().__init__(title, author, isbn, year)   # ch03: super()
        self._pages: int = pages

    @property
    def pages(self) -> int:
        return self._pages

    def get_info(self) -> str:
        return f"{super().get_info()} | {self._pages} 页"

    def __repr__(self) -> str:
        return f"PhysicalBook(title={self.title!r}, pages={self._pages})"


# ---------------------------------------------------------------------------
# ch03 / ch04: 单继承 — EBook，含私有属性与带验证的 setter
# ---------------------------------------------------------------------------
class EBook(BookItem):
    """电子书（ch03：继承；ch04：__file_size_mb 私有属性 + setter 验证）"""

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
        self.__file_size_mb: float = file_size_mb   # ch04: 双下划线私有
        self._format: str = fmt

    # ch04: @property + setter 带值域验证
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


# ---------------------------------------------------------------------------
# ch03: 多重继承 — AudioBook 继承 PhysicalBook + DigitalMixin
# MRO: AudioBook → PhysicalBook → BookItem → Catalogable → DigitalMixin → object
# ---------------------------------------------------------------------------
class AudioBook(PhysicalBook, DigitalMixin):
    """有声书（ch03：多重继承 / Mixin 模式）

    PhysicalBook 提供页数（脚本页数），DigitalMixin 提供音频文件信息。
    print(AudioBook.__mro__) 可观察 MRO 顺序。
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
        self._file_size_mb = file_size_mb   # DigitalMixin 声明的属性
        self._format = "MP3"

    def get_info(self) -> str:
        return f"{super().get_info()} | 有声书 {self.download_info()}"

    def __repr__(self) -> str:
        return (
            f"AudioBook(title={self.title!r}, "
            f"pages={self._pages}, size={self._file_size_mb})"
        )