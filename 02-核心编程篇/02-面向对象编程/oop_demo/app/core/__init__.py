"""核心模块 — 图书馆管理系统，覆盖 OOP 第01-10章"""

from app.core.catalog import Borrowable, Catalogable
from app.core.classes import AudioBook, BookItem, DigitalMixin, EBook, PhysicalBook
from app.core.library import ConsoleNotification, Library, NotificationService, SilentNotification
from app.core.member import Member
from app.core.meta import BookPlugin, HardcoverPlugin, LibraryConfig, MagazinePlugin, PaperbackPlugin, SingletonMeta
from app.core.record import BorrowRecord, IsbnSnapshot

__all__ = [
    # ch01-05, ch08: 图书类层次
    "BookItem",
    "DigitalMixin",
    "PhysicalBook",
    "EBook",
    "AudioBook",
    # ch05: 接口抽象
    "Catalogable",
    "Borrowable",
    # ch01-04, ch08: 会员
    "Member",
    # ch07: 数据类
    "BorrowRecord",
    "IsbnSnapshot",
    # ch06, ch08: 图书馆（组合 + SOLID）
    "Library",
    "NotificationService",
    "ConsoleNotification",
    "SilentNotification",
    # ch09: 元类
    "SingletonMeta",
    "LibraryConfig",
    # ch10: __init_subclass__
    "BookPlugin",
    "PaperbackPlugin",
    "HardcoverPlugin",
    "MagazinePlugin",
]