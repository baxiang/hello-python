"""图书馆管理系统 — 交互式 CLI 演示

运行方式:
    cd oop_demo
    uv run python -m app

学习者可以按章节选择演示，逐步探索 OOP 概念。
每章演示结束后按 Enter 返回菜单，可反复运行感兴趣的章节。
"""

from __future__ import annotations

import sys
from datetime import datetime, timedelta


# ============================================================================
# 第 1 章：类与对象基础
# ============================================================================

def demo_ch01() -> None:
    """类与对象 — BookItem 的创建和使用"""
    from app.domain.book.model import BookItem

    print("\n" + "=" * 50)
    print("  第 1 章：类与对象基础")
    print("=" * 50)

    print("\n📖 类是对象的模板，对象是类的具体实例\n")

    # 创建图书对象
    BookItem.total_books = 0  # 重置计数器
    book = BookItem("流畅的Python", "Ramalho", "9781491946008", 2015)

    print(f"创建图书: {book}")
    print(f"  书名: {book.title}")
    print(f"  作者: {book.author}")
    print(f"  ISBN: {book.isbn}")
    print(f"  年份: {book.year}")
    print(f"  可借: {book.is_available()}")

    # 创建多个对象
    print("\n创建多本图书:")
    books = [
        BookItem("设计模式", "GoF", "9780201633610", 1994),
        BookItem("代码大全", "McConnell", "9780735619678", 2004),
    ]
    for b in books:
        print(f"  + {b.title}")

    print(f"\n📊 图书创建总数: {BookItem.get_total()}")


# ============================================================================
# 第 2 章：属性与方法
# ============================================================================

def demo_ch02() -> None:
    """属性与方法 — 实例属性、类属性、三种方法"""
    from app.domain.book.model import BookItem
    from app.domain.member import Member

    print("\n" + "=" * 50)
    print("  第 2 章：属性与方法")
    print("=" * 50)

    # 实例属性 vs 类属性
    BookItem.total_books = 0
    print("\n📌 实例属性（每个对象独立）vs 类属性（所有对象共享）\n")

    b1 = BookItem("Python", "Guido", "9780000000001", 2020)
    b2 = BookItem("Java", "Gosling", "9780000000002", 2021)

    print(f"b1.title = {b1.title!r}  ← 实例属性，独立")
    print(f"b2.title = {b2.title!r}  ← 实例属性，独立")
    print(f"b1.total_books = {b1.total_books}  ← 类属性，共享")
    print(f"b2.total_books = {b2.total_books}  ← 类属性，共享")

    # 类方法
    print(f"\n📌 类方法: BookItem.get_total() = {BookItem.get_total()}")

    # 静态方法
    print(f"\n📌 静态方法: BookItem.validate_isbn('9780000000001') = {BookItem.validate_isbn('9780000000001')}")
    print(f"  静态方法: BookItem.validate_isbn('123') = {BookItem.validate_isbn('123')}")

    # 会员的 classmethod
    print(f"\n📌 会员统计: Member.get_total_members() = {Member.get_total_members()}")


# ============================================================================
# 第 3 章：继承
# ============================================================================

def demo_ch03() -> None:
    """继承 — BookItem → PhysicalBook → AudioBook"""
    from app.domain.book.model import AudioBook, BookItem, EBook, PhysicalBook

    print("\n" + "=" * 50)
    print("  第 3 章：继承")
    print("=" * 50)

    BookItem.total_books = 0

    print("\n📌 继承层次:\n")
    print("  BookItem（基类）")
    print("    ├── PhysicalBook（继承: title, author, isbn, year + pages）")
    print("    │     └── AudioBook（多重继承: PhysicalBook + DigitalMixin）")
    print("    └── EBook（继承: title, author, isbn, year + file_size_mb）")

    # 基类
    book = BookItem("基础书籍", "作者", "9780000000001", 2020)
    print(f"\nBookItem: {book.title}")

    # 子类 — 继承 + 扩展
    pb = PhysicalBook("流畅的Python", "Ramalho", "9781491946008", 2015, 792)
    print(f"\nPhysicalBook: {pb.title}")
    print(f"  继承自 BookItem: title={pb.title!r}, author={pb.author!r}")
    print(f"  自有属性: pages={pb.pages}")
    print(f"  重写方法: {pb.get_info()}")

    # 另一个子类
    eb = EBook("深入理解Python", "作者", "9780000000002", 2022, 5.2, "EPUB")
    print(f"\nEBook: {eb.title}")
    print(f"  继承自 BookItem: title={eb.title!r}")
    print(f"  自有属性: file_size_mb={eb.file_size_mb}, format={eb._format}")

    # 多重继承
    ab = AudioBook("代码大全", "McConnell", "9780735619678", 2004, 960, 150.0)
    print(f"\nAudioBook: {ab.title}（多重继承 PhysicalBook + DigitalMixin）")
    print(f"  来自 PhysicalBook: pages={ab.pages}")
    print(f"  来自 DigitalMixin: {ab.download_info()}")

    # MRO
    print(f"\n📌 MRO（方法解析顺序）:")
    print(f"  AudioBook.__mro__ = {[c.__name__ for c in AudioBook.__mro__]}")


# ============================================================================
# 第 4 章：封装
# ============================================================================

def demo_ch04() -> None:
    """封装 — @property、私有属性、验证"""
    from app.domain.book.model import EBook
    from app.domain.member import Member

    print("\n" + "=" * 50)
    print("  第 4 章：封装")
    print("=" * 50)

    print("\n📌 @property — 将方法伪装成属性，添加验证逻辑\n")

    # 只读属性
    book = EBook("Python", "作者", "9780000000001", 2020, 3.0)
    print(f"只读属性: book.isbn = {book.isbn!r}")
    print("尝试修改: book.isbn = 'new' → AttributeError ❌（不允许）")

    # 带验证的 setter
    print(f"\n带验证的 setter: book.file_size_mb = {book.file_size_mb}")
    book.file_size_mb = 10.0
    print(f"修改后: book.file_size_mb = {book.file_size_mb}")
    print("尝试设置负数: book.file_size_mb = -1 → ValueError ❌")

    # 私有属性（名称改写）
    print(f"\n📌 私有属性 — 名称改写（name mangling）")
    print(f"  hasattr(eb, '__file_size_mb') = {hasattr(book, '__file_size_mb')}  ← 访问不到")
    print(f"  hasattr(eb, '_EBook__file_size_mb') = {hasattr(book, '_EBook__file_size_mb')}  ← 实际存储位置")

    # 会员邮箱验证
    print(f"\n📌 邮箱验证:")
    m = Member("张三", "zhang@example.com", "M001")
    print(f"  有效邮箱: m.email = {m.email!r}")
    m.email = "new@example.com"
    print(f"  修改成功: m.email = {m.email!r}")
    print("  无效邮箱: m.email = 'not-email' → ValueError ❌")

    # 只读 member_id
    print(f"\n📌 只读属性: m.member_id = {m.member_id!r}（不可修改）")


# ============================================================================
# 第 5 章：多态
# ============================================================================

def demo_ch05() -> None:
    """多态 — ABC + Protocol"""
    from app.domain.book.model import AudioBook, BookItem, EBook, PhysicalBook
    from app.ports.catalog import Borrowable, Catalogable

    print("\n" + "=" * 50)
    print("  第 5 章：多态")
    print("=" * 50)

    BookItem.total_books = 0

    print("\n📌 同一接口，不同实现 — 多态的核心\n")

    # ABC: Catalogable
    print("📌 抽象基类（ABC）: Catalogable")
    print("  要求子类实现 get_info() 和 get_isbn()")
    print("  无法实例化没有实现抽象方法的子类")

    try:
        class Incomplete(Catalogable):
            pass
        Incomplete()
    except TypeError as e:
        print(f"  实例化未实现抽象方法的类 → TypeError: {e}")

    # Protocol: Borrowable
    print(f"\n📌 结构类型（Protocol）: Borrowable")
    print("  鸭子类型 — 只要实现了 checkout/return_item/is_available 就是 Borrowable")

    book = BookItem("测试", "作者", "9780000000001", 2020)
    print(f"  BookItem 是 Borrowable? {isinstance(book, Borrowable)}")

    # 多态调用
    print(f"\n📌 多态调用 — 同一方法，不同实现:")
    books: list[Catalogable] = [
        PhysicalBook("流畅的Python", "Ramalho", "9781491946008", 2015, 792),
        EBook("深入理解Python", "作者", "9780000000002", 2022, 5.2, "EPUB"),
        AudioBook("代码大全", "McConnell", "9780735619678", 2004, 960, 150.0),
    ]
    for b in books:
        print(f"  {b.__class__.__name__}: {b.get_info()}")


# ============================================================================
# 第 6 章：设计原则
# ============================================================================

def demo_ch06() -> None:
    """设计原则 — 组合 + SOLID"""
    from app.domain.book.model import PhysicalBook
    from app.domain.member import Member
    from app.services.library import Library
    from app.services.notification import SilentNotification

    print("\n" + "=" * 50)
    print("  第 6 章：设计原则（SOLID）")
    print("=" * 50)

    print("\n📌 组合优于继承 — Library 'has-a' books/members\n")

    notifier = SilentNotification()
    lib = Library("测试图书馆", notifier=notifier)

    book = PhysicalBook("Python", "Guido", "9780000000001", 2020, 500)
    member = Member("张三", "zhang@test.com", "M001")

    lib.add_book(book)
    lib.register_member(member)

    print(f"组合: Library 包含 Books({len(lib)}) 和 Members({len(lib._members)})")

    # DIP: 依赖倒置
    print(f"\n📌 依赖倒置（DIP）— 依赖接口而非具体实现")
    print(f"  Library 依赖 NotificationService（Protocol），不依赖 ConsoleNotification")
    print(f"  可轻松替换为 EmailNotification、SlackNotification 等")

    # 借还流程
    print(f"\n📌 借书流程:")
    record = lib.borrow("M001", "9780000000001")
    if record:
        print(f"  ✅ {record.member_id} 借出 {record.isbn}")
        print(f"  应还日期: {record.due_date.date()}")
        print(f"  通知消息: {notifier.messages[-1][0]}")

    print(f"\n📌 还书流程:")
    ok = lib.return_book("M001", "9780000000001")
    print(f"  {'✅ 归还成功' if ok else '❌ 归还失败'}")
    print(f"  通知消息: {notifier.messages[-1][0]}")

    # LSP: 里氏替换
    print(f"\n📌 里氏替换原则（LSP）— 子类可替换父类")
    print(f"  任何接受 BookItem 的地方，都可以传入 PhysicalBook、EBook、AudioBook")


# ============================================================================
# 第 7 章：数据类
# ============================================================================

def demo_ch07() -> None:
    """数据类 — @dataclass"""
    from app.domain.record import BorrowRecord, IsbnSnapshot

    print("\n" + "=" * 50)
    print("  第 7 章：数据类（@dataclass）")
    print("=" * 50)

    print("\n📌 @dataclass 自动生成 __init__、__repr__、__eq__\n")

    # 普通 dataclass
    r = BorrowRecord(member_id="M001", isbn="9780000000001")
    print(f"自动生成的 __repr__: {r!r}")
    print(f"  member_id = {r.member_id!r}")
    print(f"  isbn = {r.isbn!r}")
    print(f"  borrowed_at = {r.borrowed_at}")
    print(f"  due_date = {r.due_date}")
    print(f"  returned_at = {r.returned_at}")

    # 默认工厂
    print(f"\n📌 default_factory — 每个实例独立的默认值:")
    r1 = BorrowRecord(member_id="M001", isbn="9780000000001")
    r2 = BorrowRecord(member_id="M002", isbn="9780000000002")
    print(f"  r1.borrowed_at is r2.borrowed_at = {r1.borrowed_at is r2.borrowed_at}  ← 不同实例")

    # __post_init__ 验证
    print(f"\n📌 __post_init__ — 初始化后验证:")
    try:
        BorrowRecord(
            member_id="M001",
            isbn="9780000000001",
            borrowed_at=datetime.now(),
            due_date=datetime.now() - timedelta(days=1),  # 过去的日期
        )
    except ValueError as e:
        print(f"  due_date 早于 borrowed_at → ValueError: {e}")

    # frozen dataclass
    print(f"\n📌 frozen=True — 不可变数据类:")
    snap = IsbnSnapshot("9780000000001", "Python", "Guido")
    print(f"  创建: {snap!r}")
    print(f"  可哈希: hash(snap) = {hash(snap)}")
    print(f"  可作为 dict key: {{snap: 'cached'}}")
    print("  尝试修改: snap.title = 'other' → FrozenInstanceError ❌")


# ============================================================================
# 第 8 章：魔术方法
# ============================================================================

def demo_ch08() -> None:
    """魔术方法 — __str__, __repr__, __eq__, __hash__, __lt__, 容器协议"""
    from app.domain.book.model import BookItem
    from app.services.library import Library

    print("\n" + "=" * 50)
    print("  第 8 章：魔术方法")
    print("=" * 50)

    BookItem.total_books = 0

    print("\n📌 __str__ vs __repr__\n")
    book = BookItem("Python", "Guido", "9780000000001", 2020)
    print(f"  str(book)  = {str(book)}")
    print(f"  repr(book) = {book!r}")

    print(f"\n📌 __eq__ 和 __hash__ — 基于 ISBN 比较:")
    b1 = BookItem("Python", "Guido", "9780000000001", 2020)
    b2 = BookItem("Python 入门", "不同作者", "9780000000001", 2021)
    print(f"  b1 == b2 (同 ISBN) = {b1 == b2}")
    print(f"  hash(b1) == hash(b2) = {hash(b1) == hash(b2)}")
    print(f"  set([b1, b2]) 长度 = {len({b1, b2})}  ← 去重")

    print(f"\n📌 __lt__ — 排序:")
    books = [
        BookItem("C语言", "x", "9780000000003", 2020),
        BookItem("A语言", "x", "9780000000001", 2020),
        BookItem("B语言", "x", "9780000000002", 2020),
    ]
    sorted_titles = [b.title for b in sorted(books)]
    print(f"  排序后: {sorted_titles}")

    print(f"\n📌 容器协议 — __len__, __iter__, __contains__:")
    lib = Library("测试馆")
    lib.add_book(BookItem("A", "a", "9780000000001", 2020))
    lib.add_book(BookItem("B", "b", "9780000000002", 2020))
    lib.add_book(BookItem("C", "c", "9780000000003", 2020))
    print(f"  len(lib) = {len(lib)}")
    print(f"  '9780000000001' in lib = {'9780000000001' in lib}")
    print(f"  迭代（按书名排序）: {[b.title for b in lib]}")


# ============================================================================
# 第 9 章：元类
# ============================================================================

def demo_ch09() -> None:
    """元类 — SingletonMeta"""
    from app.infra.singleton import LibraryConfig, SingletonMeta

    print("\n" + "=" * 50)
    print("  第 9 章：元类（metaclass）")
    print("=" * 50)

    print("\n📌 元类是'类的类' — 控制类的创建行为\n")

    print(f"  type(int) = {type(int)}")
    print(f"  type(str) = {type(str)}")
    print(f"  type(LibraryConfig) = {type(LibraryConfig)}")

    print(f"\n📌 单例模式 — 通过元类控制 __call__:")
    c1 = LibraryConfig()
    c2 = LibraryConfig()
    print(f"  c1 is c2 = {c1 is c2}  ← 同一个实例")
    print(f"  id(c1) = {id(c1)}")
    print(f"  id(c2) = {id(c2)}")

    print(f"\n📌 单例配置:")
    print(f"  max_borrow_days = {c1.max_borrow_days}")
    print(f"  max_books_per_member = {c1.max_books_per_member}")
    print(f"  overdue_fine_per_day = {c1.overdue_fine_per_day}")

    # 自定义元类
    print(f"\n📌 自定义元类示例:")

    class MyService(metaclass=SingletonMeta):
        def __init__(self) -> None:
            self.value = 0

    s1 = MyService()
    s2 = MyService()
    print(f"  MyService: s1 is s2 = {s1 is s2}")

    # 清理
    SingletonMeta._instances.pop(MyService, None)


# ============================================================================
# 第 10 章：__init_subclass__
# ============================================================================

def demo_ch10() -> None:
    """__init_subclass__ — 自动注册插件"""
    from app.infra.plugin import BookPlugin, HardcoverPlugin, MagazinePlugin, PaperbackPlugin

    print("\n" + "=" * 50)
    print("  第 10 章：__init_subclass__（子类钩子）")
    print("=" * 50)

    print("\n📌 __init_subclass__ — 类被创建时自动调用，无需元类\n")

    print(f"📚 已注册的图书类型:")
    for book_type, plugin_class in BookPlugin._registry.items():
        label = getattr(plugin_class, "label", book_type)
        print(f"  {book_type!r} → {plugin_class.__name__}（{label}）")

    print(f"\n📌 自动注册 — 定义子类时自动加入注册表:")
    print(f"  PaperbackPlugin 在定义时自动注册: {BookPlugin.get_plugin('paperback') is PaperbackPlugin}")
    print(f"  HardcoverPlugin 在定义时自动注册: {BookPlugin.get_plugin('hardcover') is HardcoverPlugin}")

    # 动态注册
    print(f"\n📌 动态注册 — 运行时创建新插件:")

    class AudioPlugin(BookPlugin, book_type="audio"):
        label = "有声书"

    print(f"  定义 AudioPlugin 后自动注册")
    print(f"  BookPlugin.get_plugin('audio') = {BookPlugin.get_plugin('audio')}")
    print(f"  BookPlugin.list_types() = {BookPlugin.list_types()}")

    # 清理
    BookPlugin._registry.pop("audio", None)

    print(f"\n📌 __init_subclass__ vs 元类:")
    print(f"  __init_subclass__: 简单场景（注册、验证），无需理解 metaclass")
    print(f"  metaclass: 复杂场景（控制类创建全过程），如单例")


# ============================================================================
# 主菜单
# ============================================================================

def _clear_screen() -> None:
    """清屏"""
    print("\033[H\033[J", end="")


def _print_menu() -> None:
    """打印菜单"""
    print("=" * 50)
    print("  📚 图书馆管理系统 — OOP 学习演示")
    print("=" * 50)
    print()
    print("  1.  类与对象基础")
    print("  2.  属性与方法")
    print("  3.  继承")
    print("  4.  封装")
    print("  5.  多态")
    print("  6.  设计原则（SOLID）")
    print("  7.  数据类（@dataclass）")
    print("  8.  魔术方法")
    print("  9.  元类（metaclass）")
    print("  10. 子类钩子（__init_subclass__）")
    print()
    print("  0.  退出")
    print()


def main() -> None:
    """交互式 CLI 菜单"""
    demos = {
        "1": ("类与对象基础", demo_ch01),
        "2": ("属性与方法", demo_ch02),
        "3": ("继承", demo_ch03),
        "4": ("封装", demo_ch04),
        "5": ("多态", demo_ch05),
        "6": ("设计原则", demo_ch06),
        "7": ("数据类", demo_ch07),
        "8": ("魔术方法", demo_ch08),
        "9": ("元类", demo_ch09),
        "10": ("子类钩子", demo_ch10),
    }

    while True:
        _print_menu()
        choice = input("请选择章节 (0-10): ").strip()

        if choice == "0":
            print("\n👋 再见！")
            break

        if choice in demos:
            name, demo_fn = demos[choice]
            print(f"\n▶ 演示: 第 {choice} 章 — {name}")
            try:
                demo_fn()
            except Exception as e:
                print(f"\n❌ 演示出错: {e}")
            print("\n" + "-" * 50)
            input("按 Enter 返回菜单...")
            _clear_screen()
        else:
            print(f"\n❌ 无效选择: {choice!r}，请输入 0-10")
            input("按 Enter 重试...")
            _clear_screen()


if __name__ == "__main__":
    main()
