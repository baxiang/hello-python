"""图书馆应用服务 — 借还流程编排

覆盖：ch06 组合优于继承、SOLID 五原则、依赖注入
      ch08 __len__ / __iter__ / __contains__ / __repr__
"""

from __future__ import annotations

from app.domain.book.model import BookItem
from app.domain.member import Member
from app.domain.record import BorrowRecord
from app.ports.notification import NotificationService
from app.services.notification import ConsoleNotification


class Library:
    """图书馆服务

    组合关系（has-a）：
      self._books   : dict[isbn, BookItem]
      self._members : dict[member_id, Member]
      self._records : list[BorrowRecord]
      self._notifier: NotificationService（依赖注入）

    职责：
      - 图书编目管理（增删查搜）
      - 会员管理
      - 借还流程编排
      - 逾期追踪

    不使用继承，只通过组合持有领域实体。
    """

    def __init__(
        self,
        name: str,
        notifier: NotificationService | None = None,
    ) -> None:
        self.name: str = name
        self._books: dict[str, BookItem] = {}
        self._members: dict[str, Member] = {}
        self._records: list[BorrowRecord] = []
        self._notifier: NotificationService = notifier or ConsoleNotification()

    # ---- 图书管理 ----

    def add_book(self, book: BookItem) -> None:
        """接受任意 BookItem 子类（LSP 体现）"""
        self._books[book.isbn] = book

    def remove_book(self, isbn: str) -> bool:
        return self._books.pop(isbn, None) is not None

    def find_book(self, isbn: str) -> BookItem | None:
        return self._books.get(isbn)

    def search_by_author(self, author: str) -> list[BookItem]:
        return [
            b for b in self._books.values()
            if author.lower() in b.author.lower()
        ]

    def available_books(self) -> list[BookItem]:
        return [b for b in self._books.values() if b.is_available()]

    # ---- 会员管理 ----

    def register_member(self, member: Member) -> None:
        self._members[member.member_id] = member

    def find_member(self, member_id: str) -> Member | None:
        return self._members.get(member_id)

    # ---- 借还流程 ----

    def borrow(self, member_id: str, isbn: str) -> BorrowRecord | None:
        member = self._members.get(member_id)
        book = self._books.get(isbn)
        if not member or not book:
            return None
        if not book.checkout():
            return None
        member.borrow(isbn)
        record = BorrowRecord(member_id=member_id, isbn=isbn)
        self._records.append(record)
        self._notifier.notify(
            member,
            f"《{book.title}》借阅成功，请于 {record.due_date.date()} 前归还",
        )
        return record

    def return_book(self, member_id: str, isbn: str) -> bool:
        member = self._members.get(member_id)
        book = self._books.get(isbn)
        if not member or not book:
            return False
        record = self._find_active_record(member_id, isbn)
        if not record:
            return False
        book.return_item()
        member.return_book(isbn)
        record.complete_return()
        self._notifier.notify(member, f"《{book.title}》归还成功，感谢使用")
        return True

    def overdue_records(self) -> list[BorrowRecord]:
        return [r for r in self._records if r.is_overdue]

    def member_records(self, member_id: str) -> list[BorrowRecord]:
        return [r for r in self._records if r.member_id == member_id]

    def _find_active_record(
        self, member_id: str, isbn: str
    ) -> BorrowRecord | None:
        for r in reversed(self._records):
            if r.member_id == member_id and r.isbn == isbn and r.returned_at is None:
                return r
        return None

    # ---- 容器魔术方法 ----

    def __len__(self) -> int:
        return len(self._books)

    def __iter__(self):
        return iter(sorted(self._books.values()))

    def __contains__(self, isbn: str) -> bool:
        return isbn in self._books

    def __repr__(self) -> str:
        return (
            f"Library(name={self.name!r}, "
            f"books={len(self._books)}, members={len(self._members)})"
        )
