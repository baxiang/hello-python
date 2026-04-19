"""借阅记录 — 覆盖第07章：@dataclass

章节对应：
  ch07  @dataclass 自动生成 __init__ / __repr__ / __eq__
        field(default_factory=...) 处理可变默认值
        __post_init__ 跨字段校验
        frozen=False（可变）vs frozen=True（不可变）演示
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta


@dataclass
class BorrowRecord:
    """借阅记录（ch07：@dataclass）

    @dataclass 自动生成：
      __init__(member_id, isbn, borrowed_at, due_date, returned_at)
      __repr__
      __eq__（按所有字段比较）
    """

    member_id: str
    isbn: str
    # field(default_factory=...) — 避免可变默认值陷阱
    borrowed_at: datetime = field(default_factory=datetime.now)
    due_date: datetime = field(
        default_factory=lambda: datetime.now() + timedelta(days=14)
    )
    returned_at: datetime | None = field(default=None)

    def __post_init__(self) -> None:
        """ch07: __post_init__ — 字段赋值后的跨字段校验"""
        if self.due_date <= self.borrowed_at:
            raise ValueError("还书日期必须晚于借阅日期")

    @property
    def is_overdue(self) -> bool:
        """是否逾期：已归还则不计入"""
        if self.returned_at is not None:
            return False
        return datetime.now() > self.due_date

    @property
    def days_remaining(self) -> int:
        """距还书截止日的剩余天数，已归还或逾期均返回 0"""
        if self.returned_at is not None:
            return 0
        delta = self.due_date - datetime.now()
        return max(0, delta.days)

    def complete_return(self) -> None:
        """标记归还时间"""
        self.returned_at = datetime.now()


# ---------------------------------------------------------------------------
# ch07: frozen=True 演示 — 不可变记录，自动获得 __hash__
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class IsbnSnapshot:
    """ISBN 快照，frozen=True 使其可哈希，可用作字典键（ch07）"""

    isbn: str
    title: str
    author: str
