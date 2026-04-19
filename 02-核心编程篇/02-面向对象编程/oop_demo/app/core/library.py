"""图书馆核心逻辑 — 覆盖第06章、第08章（容器魔术方法）

章节对应：
  ch06  组合优于继承：Library 持有 books/members/records（has-a 关系）
        开放封闭原则：NotificationService Protocol，新增通知方式无需改 Library
        依赖倒置原则：Library 依赖 NotificationService 抽象，而非具体实现
        单一职责原则：Library 只负责协调，不自己处理通知/记录细节
        里氏替换原则：borrow() 接受任意 BookItem 子类
  ch08  __len__ / __iter__ / __contains__ / __repr__
"""

from __future__ import annotations

from typing import Protocol

from app.core.classes import BookItem
from app.core.member import Member
from app.core.record import BorrowRecord


# ---------------------------------------------------------------------------
# ch06: 依赖倒置原则 — 定义通知抽象，Library 不依赖具体实现
# ---------------------------------------------------------------------------
class NotificationService(Protocol):
    """通知服务协议（ch06：DIP + Protocol）

    任何实现了 notify(member, message) 的对象都满足此接口。
    """

    def notify(self, member: Member, message: str) -> None:
        ...


class ConsoleNotification:
    """控制台通知（默认实现，可被替换）"""

    def notify(self, member: Member, message: str) -> None:
        print(f"[通知] {member.name}: {message}")


class SilentNotification:
    """静默通知（测试用，不输出任何内容）"""

    def __init__(self) -> None:
        self.messages: list[tuple[str, str]] = []

    def notify(self, member: Member, message: str) -> None:
        self.messages.append((member.name, message))


# ---------------------------------------------------------------------------
# ch06: 组合 — Library has BookItem(s), Member(s), BorrowRecord(s)
# ch08: __len__ / __iter__ / __contains__ / __repr__
# ---------------------------------------------------------------------------
class Library:
    """图书馆（ch06：组合 + SOLID；ch08：容器魔术方法）

    组合关系（has-a）：
      self._books   : dict[isbn, BookItem]
      self._members : dict[member_id, Member]
      self._records : list[BorrowRecord]
      self._notifier: NotificationService（依赖注入）

    不使用继承，不从 BookItem/Member 派生，只持有它们。
    """

    def __init__(
        self,
        name: str,
        notifier: NotificationService | None = None,
    ) -> None:
        self.name: str = name
        self._books: dict[str, BookItem] = {}       # isbn → BookItem
        self._members: dict[str, Member] = {}        # member_id → Member
        self._records: list[BorrowRecord] = []
        self._notifier: NotificationService = notifier or ConsoleNotification()

    # ------------------------------------------------------------------
    # 图书管理（ch06: SRP — Library 只协调，不关心 BookItem 内部实现）
    # ------------------------------------------------------------------
    def add_book(self, book: BookItem) -> None:
        """添加图书；接受任意 BookItem 子类（ch06: LSP 体现）"""
        self._books[book.isbn] = book

    def remove_book(self, isbn: str) -> bool:
        return self._books.pop(isbn, None) is not None

    def find_book(self, isbn: str) -> BookItem | None:
        return self._books.get(isbn)

    def search_by_author(self, author: str) -> list[BookItem]:
        return [b for b in self._books.values()
                if author.lower() in b.author.lower()]

    def available_books(self) -> list[BookItem]:
        return [b for b in self._books.values() if b.is_available()]

    # ------------------------------------------------------------------
    # 会员管理
    # ------------------------------------------------------------------
    def register_member(self, member: Member) -> None:
        self._members[member.member_id] = member

    def find_member(self, member_id: str) -> Member | None:
        return self._members.get(member_id)

    # ------------------------------------------------------------------
    # 借阅 / 归还（ch06: OCP — 通知方式可扩展，借阅流程不变）
    # ------------------------------------------------------------------
    def borrow(self, member_id: str, isbn: str) -> BorrowRecord | None:
        """借书：成功返回 BorrowRecord，失败返回 None"""
        member = self._members.get(member_id)
        book = self._books.get(isbn)
        if not member or not book:
            return None
        if not book.checkout():        # book 可以是任意 BookItem 子类
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
        """还书：成功返回 True"""
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

    def _find_active_record(
        self, member_id: str, isbn: str
    ) -> BorrowRecord | None:
        for r in reversed(self._records):
            if r.member_id == member_id and r.isbn == isbn and r.returned_at is None:
                return r
        return None

    # ------------------------------------------------------------------
    # ch08: 容器魔术方法
    # ------------------------------------------------------------------
    def __len__(self) -> int:
        """len(library) → 馆藏总数"""
        return len(self._books)

    def __iter__(self):
        """for book in library → 按书名字母序迭代"""
        return iter(sorted(self._books.values()))

    def __contains__(self, isbn: str) -> bool:
        """isbn in library → 快速查询是否馆藏"""
        return isbn in self._books

    def __repr__(self) -> str:
        return (
            f"Library(name={self.name!r}, "
            f"books={len(self._books)}, members={len(self._members)})"
        )
