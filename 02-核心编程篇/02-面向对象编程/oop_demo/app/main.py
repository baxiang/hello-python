"""图书馆管理系统 — CLI 入口

运行方式：
    uv run python -m app              # 模块方式
    uv run oop-demo                   # 脚本入口（配置后）

演示场景：完整展示图书馆借还流程，涵盖 OOP 第 01-10 章核心概念。
"""

from __future__ import annotations

from app.domain.book.model import AudioBook, BookItem, EBook, PhysicalBook
from app.domain.member import Member
from app.infra.plugin import BookPlugin
from app.infra.singleton import LibraryConfig
from app.services.library import Library
from app.services.notification import ConsoleNotification
from app.utils.helpers import format_book_list, generate_member_id


def main() -> None:
    """运行图书馆管理系统演示"""

    print("=" * 60)
    print("  图书馆管理系统 — OOP 全栈演示")
    print("=" * 60)

    # ---- ch09: 元类单例 ----
    cfg = LibraryConfig()
    print(f"\n📋 系统配置: {cfg}")
    print(f"   借阅天数: {cfg.max_borrow_days} 天")
    print(f"   每人限借: {cfg.max_books_per_member} 本")

    # ---- ch10: 插件注册 ----
    print(f"\n📚 图书类型插件: {BookPlugin.list_types()}")

    # ---- ch01-03: 创建图书馆与图书 ----
    lib = Library("市图书馆", notifier=ConsoleNotification())

    books = [
        PhysicalBook("流畅的Python", "Ramalho", "9781491946008", 2015, 792),
        EBook("深入理解计算机系统", "Bryant", "9787111544937", 2016, 15.5, "PDF"),
        AudioBook("代码大全", "McConnell", "9780735619678", 2004, 960, 150.0),
        PhysicalBook("设计模式", "GoF", "9780201633610", 1994, 395),
    ]

    print("\n📖 新书入库：")
    for book in books:
        lib.add_book(book)
        print(f"   + {book}")

    print(f"\n📊 馆藏统计: {len(lib)} 册")
    print(f"   可借阅: {len(lib.available_books())} 册")

    # ---- ch05: 多态 — ABC + Protocol ----
    print("\n🔍 类型检查：")
    for book in books:
        from app.ports.catalog import Catalogable

        from app.ports.catalog import Borrowable

        catalog = isinstance(book, Catalogable)
        borrow = isinstance(book, Borrowable)
        print(f"   {book.title}: Catalogable={catalog}, Borrowable={borrow}")

    # ---- ch01-04: 注册会员 ----
    print("\n👤 会员注册：")
    members = [
        Member("张三", "zhang@example.com", "M001"),
        Member("李四", "li@example.com", "M002"),
    ]
    for m in members:
        lib.register_member(m)
        print(f"   + {m}")

    # ---- ch06: 借书流程（依赖注入通知） ----
    print("\n📤 借书：")
    record = lib.borrow("M001", "9781491946008")
    if record:
        print(f"   借阅记录: {record.member_id} → {record.isbn}")
        print(f"   应还日期: {record.due_date.date()}")

    # ---- ch06: 还书流程 ----
    print("\n📥 还书：")
    ok = lib.return_book("M001", "9781491946008")
    print(f"   归还结果: {'成功' if ok else '失败'}")

    # ---- ch08: 容器操作 ----
    print(f"\n📊 最终馆藏: {lib}")
    print(f"   ISBN 9781491946008 在馆藏: {'9781491946008' in lib}")

    # ---- ch02: 类属性统计 ----
    print(f"\n📈 系统统计:")
    print(f"   图书创建总数: {BookItem.get_total()}")
    print(f"   注册会员总数: {Member.get_total_members()}")

    # ---- 工具函数 ----
    print(f"\n🔧 工具函数:")
    mid = generate_member_id("王五")
    print(f"   生成会员号: {mid}")
    print(f"   可借图书: \n{format_book_list(lib.available_books())}")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
