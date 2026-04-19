"""会员类 — 覆盖第01-04章、第08章

章节对应：
  ch01  Member 基础类定义
  ch02  _member_count 类属性；get_total_members 类方法；validate_email 静态方法
  ch04  __email 私有属性；@property + setter 验证
  ch08  __str__ / __repr__ / __eq__ / __hash__
"""

from __future__ import annotations


class Member:
    """图书馆会员

    ch01: 类的定义
    ch02: _member_count 类属性；类方法；静态方法
    ch04: __email 双下划线私有属性；@property setter 验证邮箱格式
    ch08: __str__ / __repr__ / __eq__ / __hash__
    """

    # ch02: 类属性 — 跟踪已注册会员总数
    _member_count: int = 0

    def __init__(self, name: str, email: str, member_id: str) -> None:
        self.name: str = name
        self.__email: str = self._check_email(email)   # ch04: 私有属性
        self._member_id: str = member_id
        self._borrowed_isbns: list[str] = []
        Member._member_count += 1

    # ch04: @property — 读取私有邮箱
    @property
    def email(self) -> str:
        return self.__email

    # ch04: setter — 修改前重新校验
    @email.setter
    def email(self, value: str) -> None:
        self.__email = self._check_email(value)

    @property
    def member_id(self) -> str:
        return self._member_id

    @property
    def borrow_count(self) -> int:
        """当前借阅数量"""
        return len(self._borrowed_isbns)

    # ch02: 类方法
    @classmethod
    def get_total_members(cls) -> int:
        """返回已注册的会员总数"""
        return cls._member_count

    # ch02: 静态方法 — 纯工具函数，不依赖实例/类状态
    @staticmethod
    def validate_email(email: str) -> bool:
        """粗校验邮箱格式"""
        parts = email.split("@")
        return len(parts) == 2 and "." in parts[1]

    # 内部：供 __init__ 和 setter 共用
    @staticmethod
    def _check_email(email: str) -> str:
        if not Member.validate_email(email):
            raise ValueError(f"邮箱格式不正确: {email!r}")
        return email

    def borrow(self, isbn: str) -> None:
        self._borrowed_isbns.append(isbn)

    def return_book(self, isbn: str) -> None:
        self._borrowed_isbns.remove(isbn)

    # ch08: 魔术方法
    def __str__(self) -> str:
        return f"会员 {self.name}（{self._member_id}）借阅 {self.borrow_count} 本"

    def __repr__(self) -> str:
        return f"Member(name={self.name!r}, member_id={self._member_id!r})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Member):
            return NotImplemented
        return self._member_id == other._member_id

    def __hash__(self) -> int:
        return hash(self._member_id)
