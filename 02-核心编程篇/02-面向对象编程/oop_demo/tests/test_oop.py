"""面向对象测试套件 — 图书馆管理系统，覆盖 OOP 第01-10章"""

import pytest

from app.core.catalog import Borrowable, Catalogable
from app.core.classes import AudioBook, BookItem, EBook, PhysicalBook
from app.core.library import Library, SilentNotification
from app.core.member import Member
from app.core.meta import BookPlugin, HardcoverPlugin, LibraryConfig, MagazinePlugin, PaperbackPlugin, SingletonMeta
from app.core.record import BorrowRecord, IsbnSnapshot
from app.utils.helpers import format_book_list, generate_member_id


# ===========================================================================
# ch01 / ch02: 基础类 + 属性与方法
# ===========================================================================
class TestBookItemBasics:
    """ch01: 类定义、实例化；ch02: 类属性、类方法、静态方法"""

    def setup_method(self):
        # 每个测试前重置类属性，避免测试间相互影响
        BookItem.total_books = 0

    def test_instance_attributes(self):
        book = BookItem("Python编程", "Guido", "9780134853987", 2019)
        assert book.title == "Python编程"
        assert book.author == "Guido"
        assert book.year == 2019

    def test_class_attribute_increments(self):
        assert BookItem.total_books == 0
        BookItem("A", "a", "9780000000001", 2020)
        BookItem("B", "b", "9780000000002", 2021)
        assert BookItem.total_books == 2

    def test_classmethod_get_total(self):
        BookItem("A", "a", "9780000000001", 2020)
        assert BookItem.get_total() == 1

    def test_staticmethod_validate_isbn(self):
        assert BookItem.validate_isbn("9780134853987") is True
        assert BookItem.validate_isbn("978-0-13-485398-7") is True
        assert BookItem.validate_isbn("123") is False
        assert BookItem.validate_isbn("abcdefghijklm") is False


# ===========================================================================
# ch03: 继承
# ===========================================================================
class TestInheritance:
    """ch03: 单继承 super()；多重继承 Mixin；MRO"""

    def setup_method(self):
        BookItem.total_books = 0

    def test_physical_book_inherits_book_item(self):
        pb = PhysicalBook("流畅的Python", "Ramalho", "9781491946008", 2015, 792)
        assert isinstance(pb, BookItem)
        assert pb.pages == 792
        assert "792 页" in pb.get_info()

    def test_ebook_inherits_book_item(self):
        eb = EBook("深入理解Python", "作者", "9780000000010", 2022, 5.2, "EPUB")
        assert isinstance(eb, BookItem)
        assert eb.file_size_mb == 5.2
        assert "EPUB" in eb.get_info()

    def test_audiobook_multiple_inheritance(self):
        ab = AudioBook("代码大全", "McConnell", "9780735619678", 2004, 960, 150.0)
        assert isinstance(ab, PhysicalBook)
        assert isinstance(ab, BookItem)
        assert ab.pages == 960
        assert "有声书" in ab.get_info()
        assert "MP3" in ab.download_info()

    def test_mro_order(self):
        mro_names = [cls.__name__ for cls in AudioBook.__mro__]
        # AudioBook → PhysicalBook → BookItem → ... → DigitalMixin
        assert mro_names.index("AudioBook") < mro_names.index("PhysicalBook")
        assert mro_names.index("PhysicalBook") < mro_names.index("BookItem")

    def test_super_get_info_chain(self):
        pb = PhysicalBook("流畅的Python", "Ramalho", "9781491946008", 2015, 792)
        info = pb.get_info()
        # get_info 调用链：PhysicalBook → BookItem
        assert "流畅的Python" in info
        assert "792 页" in info


# ===========================================================================
# ch04: 封装
# ===========================================================================
class TestEncapsulation:
    """ch04: 私有属性、@property、setter 验证"""

    def setup_method(self):
        BookItem.total_books = 0

    def test_property_readonly_isbn(self):
        book = BookItem("X", "Y", "9780000000001", 2020)
        assert book.isbn == "9780000000001"
        with pytest.raises(AttributeError):
            book.isbn = "new"  # type: ignore[misc]

    def test_ebook_private_attribute_name_mangling(self):
        eb = EBook("X", "Y", "9780000000001", 2020, 3.0)
        # 双下划线私有属性不可直接访问
        assert not hasattr(eb, "__file_size_mb")
        assert not hasattr(eb, "_file_size_mb")   # 名字改写后不存在此名
        assert eb.file_size_mb == 3.0             # 通过 @property 读取

    def test_ebook_setter_validates_positive(self):
        eb = EBook("X", "Y", "9780000000001", 2020, 3.0)
        eb.file_size_mb = 10.0
        assert eb.file_size_mb == 10.0

    def test_ebook_setter_rejects_non_positive(self):
        eb = EBook("X", "Y", "9780000000001", 2020, 3.0)
        with pytest.raises(ValueError):
            eb.file_size_mb = 0

    def test_member_email_private(self):
        m = Member("张三", "zhang@example.com", "M001")
        assert m.email == "zhang@example.com"
        with pytest.raises(ValueError):
            m.email = "not-an-email"

    def test_member_email_setter_valid(self):
        m = Member("张三", "zhang@example.com", "M001")
        m.email = "new@example.com"
        assert m.email == "new@example.com"


# ===========================================================================
# ch05: 多态（ABC + Protocol）
# ===========================================================================
class TestPolymorphism:
    """ch05: ABC 强制接口；Borrowable Protocol 鸭子类型；isinstance 检查"""

    def setup_method(self):
        BookItem.total_books = 0

    def test_catalogable_abc_cannot_instantiate_without_methods(self):
        """ABC 不能直接实例化，必须实现所有抽象方法"""
        from app.core.catalog import Catalogable

        class Incomplete(Catalogable):
            pass  # 未实现 get_info / get_isbn

        with pytest.raises(TypeError):
            Incomplete()  # type: ignore[abstract]

    def test_book_item_satisfies_catalogable(self):
        book = BookItem("X", "Y", "9780000000001", 2020)
        assert isinstance(book, Catalogable)

    def test_book_item_satisfies_borrowable_protocol(self):
        """鸭子类型：BookItem 不显式继承 Borrowable，但满足协议"""
        book = BookItem("X", "Y", "9780000000001", 2020)
        assert isinstance(book, Borrowable)   # @runtime_checkable

    def test_borrowable_checkout_return_cycle(self):
        book = BookItem("X", "Y", "9780000000001", 2020)
        assert book.is_available() is True
        assert book.checkout() is True
        assert book.is_available() is False
        assert book.checkout() is False    # 已借出，无法再借
        book.return_item()
        assert book.is_available() is True

    def test_polymorphic_get_info(self):
        """里氏替换：用 Catalogable 类型变量调用 get_info，行为取决于实际类型"""
        books: list[Catalogable] = [
            PhysicalBook("A", "a", "9780000000001", 2020, 300),
            EBook("B", "b", "9780000000002", 2021, 2.0),
        ]
        infos = [b.get_info() for b in books]
        assert "300 页" in infos[0]
        assert "PDF" in infos[1]


# ===========================================================================
# ch06: 设计原则（组合 + SOLID）
# ===========================================================================
class TestDesignPrinciples:
    """ch06: 组合优于继承；SRP/OCP/LSP/DIP；NotificationService 依赖注入"""

    def setup_method(self):
        BookItem.total_books = 0
        self.notifier = SilentNotification()
        self.lib = Library("测试图书馆", notifier=self.notifier)
        self.book = PhysicalBook("Python", "Guido", "9780000000001", 2020, 500)
        self.member = Member("张三", "zhang@test.com", "M001")
        self.lib.add_book(self.book)
        self.lib.register_member(self.member)

    def test_composition_has_books_and_members(self):
        """Library 持有 BookItem 和 Member（has-a 组合）"""
        assert self.lib.find_book("9780000000001") is self.book
        assert self.lib.find_member("M001") is self.member

    def test_lsp_accepts_any_book_item_subclass(self):
        """里氏替换：add_book 接受 PhysicalBook / EBook / AudioBook"""
        eb = EBook("E", "e", "9780000000002", 2021, 3.0)
        ab = AudioBook("A", "a", "9780000000003", 2022, 100, 80.0)
        self.lib.add_book(eb)
        self.lib.add_book(ab)
        assert len(self.lib) == 3

    def test_borrow_flow(self):
        record = self.lib.borrow("M001", "9780000000001")
        assert record is not None
        assert not self.book.is_available()
        assert self.member.borrow_count == 1

    def test_return_flow(self):
        self.lib.borrow("M001", "9780000000001")
        ok = self.lib.return_book("M001", "9780000000001")
        assert ok is True
        assert self.book.is_available()
        assert self.member.borrow_count == 0

    def test_borrow_unavailable_book_returns_none(self):
        self.lib.borrow("M001", "9780000000001")   # 先借走
        record2 = self.lib.borrow("M001", "9780000000001")
        assert record2 is None

    def test_dip_notification_service_injected(self):
        """依赖倒置：通知走 SilentNotification，不是硬编码 ConsoleNotification"""
        self.lib.borrow("M001", "9780000000001")
        assert len(self.notifier.messages) == 1
        assert "张三" in self.notifier.messages[0][0]

    def test_ocp_swap_notifier(self):
        """开放封闭：换掉 notifier 不影响 borrow 逻辑"""
        from app.core.library import SilentNotification

        new_notifier = SilentNotification()
        lib2 = Library("另一个馆", notifier=new_notifier)
        lib2.add_book(PhysicalBook("B", "b", "9780000000009", 2020, 100))
        lib2.register_member(Member("李四", "li@test.com", "M099"))
        lib2.borrow("M099", "9780000000009")
        assert len(new_notifier.messages) == 1


# ===========================================================================
# ch07: 数据类
# ===========================================================================
class TestDataclass:
    """ch07: @dataclass 自动生成 __init__/__repr__/__eq__；__post_init__；frozen"""

    def test_borrow_record_auto_init(self):
        r = BorrowRecord(member_id="M001", isbn="9780000000001")
        assert r.member_id == "M001"
        assert r.isbn == "9780000000001"
        assert r.returned_at is None

    def test_borrow_record_default_factory_fields(self):
        r1 = BorrowRecord(member_id="M001", isbn="9780000000001")
        r2 = BorrowRecord(member_id="M002", isbn="9780000000002")
        # default_factory 保证每次是新对象，不共享
        assert r1.borrowed_at is not r2.borrowed_at

    def test_borrow_record_post_init_validation(self):
        from datetime import datetime, timedelta

        past = datetime.now() - timedelta(days=1)
        with pytest.raises(ValueError):
            BorrowRecord(
                member_id="M001",
                isbn="9780000000001",
                borrowed_at=datetime.now(),
                due_date=past,
            )

    def test_borrow_record_complete_return(self):
        r = BorrowRecord(member_id="M001", isbn="9780000000001")
        assert r.returned_at is None
        r.complete_return()
        assert r.returned_at is not None

    def test_borrow_record_dataclass_eq(self):
        from datetime import datetime

        dt = datetime(2024, 1, 1)
        due = datetime(2024, 1, 15)
        r1 = BorrowRecord("M001", "ISBN1", dt, due)
        r2 = BorrowRecord("M001", "ISBN1", dt, due)
        assert r1 == r2

    def test_isbn_snapshot_frozen_hashable(self):
        snap = IsbnSnapshot("9780000000001", "Python", "Guido")
        # frozen=True → 可哈希
        d = {snap: "cached"}
        assert d[snap] == "cached"

    def test_isbn_snapshot_frozen_immutable(self):
        snap = IsbnSnapshot("9780000000001", "Python", "Guido")
        with pytest.raises(Exception):  # FrozenInstanceError
            snap.title = "other"  # type: ignore[misc]


# ===========================================================================
# ch08: 魔术方法
# ===========================================================================
class TestMagicMethods:
    """ch08: __str__ / __repr__ / __eq__ / __hash__ / __lt__ / __len__ / __iter__ / __contains__"""

    def setup_method(self):
        BookItem.total_books = 0

    def test_str_shows_availability(self):
        book = BookItem("Python", "Guido", "9780000000001", 2020)
        assert "可借" in str(book)
        book.checkout()
        assert "已借出" in str(book)

    def test_repr_contains_class_name(self):
        pb = PhysicalBook("A", "a", "9780000000001", 2020, 100)
        assert repr(pb).startswith("PhysicalBook(")

    def test_eq_by_isbn(self):
        b1 = BookItem("A", "x", "9780000000001", 2020)
        b2 = BookItem("B", "y", "9780000000001", 2021)   # 同 ISBN 不同其他属性
        assert b1 == b2

    def test_ne_different_isbn(self):
        b1 = BookItem("A", "x", "9780000000001", 2020)
        b2 = BookItem("A", "x", "9780000000002", 2020)
        assert b1 != b2

    def test_hash_same_isbn(self):
        b1 = BookItem("A", "x", "9780000000001", 2020)
        b2 = BookItem("B", "y", "9780000000001", 2020)
        assert hash(b1) == hash(b2)
        # 可放入 set
        s = {b1, b2}
        assert len(s) == 1

    def test_lt_sorts_by_title(self):
        b1 = BookItem("B标题", "x", "9780000000001", 2020)
        b2 = BookItem("A标题", "y", "9780000000002", 2020)
        assert b2 < b1
        assert sorted([b1, b2])[0].title == "A标题"

    def test_library_len(self):
        lib = Library("馆")
        assert len(lib) == 0
        lib.add_book(BookItem("A", "a", "9780000000001", 2020))
        assert len(lib) == 1

    def test_library_iter_sorted(self):
        lib = Library("馆")
        lib.add_book(BookItem("C", "c", "9780000000003", 2020))
        lib.add_book(BookItem("A", "a", "9780000000001", 2020))
        lib.add_book(BookItem("B", "b", "9780000000002", 2020))
        titles = [b.title for b in lib]
        assert titles == ["A", "B", "C"]

    def test_library_contains(self):
        lib = Library("馆")
        lib.add_book(BookItem("A", "a", "9780000000001", 2020))
        assert "9780000000001" in lib
        assert "9780000000099" not in lib

    def test_member_str_and_repr(self):
        m = Member("张三", "z@example.com", "M001")
        assert "张三" in str(m)
        assert repr(m).startswith("Member(")

    def test_member_eq_by_member_id(self):
        m1 = Member("张三", "a@x.com", "M001")
        m2 = Member("李四", "b@x.com", "M001")   # 同 member_id
        assert m1 == m2

    def test_member_hash(self):
        m1 = Member("张三", "a@x.com", "M001")
        m2 = Member("李四", "b@x.com", "M001")
        assert hash(m1) == hash(m2)


# ===========================================================================
# ch09: 元类
# ===========================================================================
class TestMetaclass:
    """ch09: SingletonMeta 拦截 __call__；LibraryConfig 全局唯一"""

    def test_singleton_meta_same_instance(self):
        c1 = LibraryConfig()
        c2 = LibraryConfig()
        assert c1 is c2

    def test_singleton_meta_custom_class(self):
        class MyService(metaclass=SingletonMeta):
            pass

        s1 = MyService()
        s2 = MyService()
        assert s1 is s2
        # 清理，不影响其他测试
        SingletonMeta._instances.pop(MyService, None)

    def test_library_config_default_values(self):
        cfg = LibraryConfig()
        assert cfg.max_borrow_days == 14
        assert cfg.max_books_per_member == 5
        assert cfg.overdue_fine_per_day == 0.5

    def test_library_config_mutation_persists(self):
        """单例：一处修改，全局可见"""
        cfg1 = LibraryConfig()
        original = cfg1.max_borrow_days
        cfg1.max_borrow_days = 30
        cfg2 = LibraryConfig()
        assert cfg2.max_borrow_days == 30
        cfg1.max_borrow_days = original  # 还原


# ===========================================================================
# ch10: __init_subclass__
# ===========================================================================
class TestInitSubclass:
    """ch10: __init_subclass__ 自动注册插件"""

    def test_predefined_plugins_registered(self):
        types = BookPlugin.list_types()
        assert "paperback" in types
        assert "hardcover" in types
        assert "magazine" in types

    def test_get_plugin_returns_correct_class(self):
        assert BookPlugin.get_plugin("paperback") is PaperbackPlugin
        assert BookPlugin.get_plugin("hardcover") is HardcoverPlugin
        assert BookPlugin.get_plugin("magazine") is MagazinePlugin

    def test_get_plugin_unknown_returns_none(self):
        assert BookPlugin.get_plugin("unknown_type") is None

    def test_dynamic_plugin_registration(self):
        """定义新子类即自动注册，无需手动调用 register()"""
        class AudioPlugin(BookPlugin, book_type="audio_test"):
            label = "有声书"

        assert BookPlugin.get_plugin("audio_test") is AudioPlugin
        # 清理
        BookPlugin._registry.pop("audio_test", None)

    def test_plugin_label_attribute(self):
        assert PaperbackPlugin.label == "平装"
        assert HardcoverPlugin.label == "精装"
        assert MagazinePlugin.label == "期刊"


# ===========================================================================
# helpers
# ===========================================================================
class TestHelpers:
    def setup_method(self):
        BookItem.total_books = 0

    def test_generate_member_id_prefix(self):
        mid = generate_member_id("张三")
        assert mid.startswith("M")
        assert len(mid) == 7   # M + 6位hex

    def test_generate_member_id_deterministic(self):
        assert generate_member_id("张三") == generate_member_id("张三")

    def test_format_book_list_empty(self):
        assert format_book_list([]) == "（暂无图书）"

    def test_format_book_list_numbered(self):
        books = [
            BookItem("A", "a", "9780000000001", 2020),
            BookItem("B", "b", "9780000000002", 2021),
        ]
        result = format_book_list(books)
        assert "1." in result
        assert "2." in result