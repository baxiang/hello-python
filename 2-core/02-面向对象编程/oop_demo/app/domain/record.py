"""借阅记录 — dataclass 演示

覆盖：ch07 @dataclass、field(default_factory)、__post_init__、frozen
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta


@dataclass
class BorrowRecord:
    """借阅记录

    @dataclass 自动生成 __init__ / __repr__ / __eq__。
    """

    member_id: str
    isbn: str
    borrowed_at: datetime = field(default_factory=datetime.now)
    due_date: datetime = field(
        default_factory=lambda: datetime.now() + timedelta(days=14)
    )
    returned_at: datetime | None = field(default=None)

    def __post_init__(self) -> None:
        if self.due_date <= self.borrowed_at:
            raise ValueError("还书日期必须晚于借阅日期")

    @property
    def is_overdue(self) -> bool:
        if self.returned_at is not None:
            return False
        return datetime.now() > self.due_date

    @property
    def days_remaining(self) -> int:
        if self.returned_at is not None:
            return 0
        delta = self.due_date - datetime.now()
        return max(0, delta.days)

    def complete_return(self) -> None:
        self.returned_at = datetime.now()


@dataclass(frozen=True)
class IsbnSnapshot:
    """ISBN 快照 — frozen=True 使其可哈希，可用作字典键"""

    isbn: str
    title: str
    author: str
