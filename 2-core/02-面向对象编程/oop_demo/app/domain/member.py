"""会员领域模型

覆盖：ch01 类定义、ch02 类属性/方法、ch04 封装/@property、ch08 魔术方法
"""

from __future__ import annotations


class Member:
    """图书馆会员

    职责：
      - 身份标识（member_id）
      - 联系信息（email 带验证）
      - 借阅记录追踪
    """

    _member_count: int = 0

    def __init__(self, name: str, email: str, member_id: str) -> None:
        self.name: str = name
        self.__email: str = self._check_email(email)
        self._member_id: str = member_id
        self._borrowed_isbns: list[str] = []
        Member._member_count += 1

    @property
    def email(self) -> str:
        return self.__email

    @email.setter
    def email(self, value: str) -> None:
        self.__email = self._check_email(value)

    @property
    def member_id(self) -> str:
        return self._member_id

    @property
    def borrow_count(self) -> int:
        return len(self._borrowed_isbns)

    @classmethod
    def get_total_members(cls) -> int:
        return cls._member_count

    @staticmethod
    def validate_email(email: str) -> bool:
        parts = email.split("@")
        return len(parts) == 2 and "." in parts[1]

    @staticmethod
    def _check_email(email: str) -> str:
        if not Member.validate_email(email):
            raise ValueError(f"邮箱格式不正确: {email!r}")
        return email

    def borrow(self, isbn: str) -> None:
        self._borrowed_isbns.append(isbn)

    def return_book(self, isbn: str) -> None:
        self._borrowed_isbns.remove(isbn)

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
