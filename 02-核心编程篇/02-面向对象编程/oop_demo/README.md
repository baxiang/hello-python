# 面向对象编程

Python OOP 示例项目，覆盖第 01-10 章（类基础 → 属性 → 继承 → 封装 → 多态 → SOLID → 数据类 → 魔术方法 → 元类 → `__init_subclass__`）。

## 场景

图书馆管理系统：通过 BookItem、Library、Member 等类，完整演示 Python 面向对象编程的所有核心概念。

## 项目结构

```
oop_demo/
├── pyproject.toml
├── app/
│   ├── __init__.py
│   ├── core/
│   │   ├── classes.py    # ch01-05/08: BookItem 层次、Mixin、魔术方法
│   │   ├── catalog.py    # ch05: ABC + Protocol 抽象接口
│   │   ├── library.py    # ch06/08: 组合、SOLID、容器魔术方法
│   │   ├── member.py     # ch01-04/08: Member 类、封装
│   │   ├── meta.py       # ch09-10: 元类单例、__init_subclass__ 插件注册
│   │   └── record.py     # ch07: @dataclass 借阅记录
│   └── utils/
│       └── helpers.py    # 工具函数
└── tests/
    └── test_oop.py       # 30+ 测试，全覆盖
```

## 安装

```bash
uv sync
```

## 使用示例

```python
from app.core.classes import PhysicalBook, EBook, AudioBook
from app.core.library import Library, SilentNotification
from app.core.member import Member
from app.core.record import BorrowRecord
from app.core.meta import LibraryConfig, BookPlugin

# ch01-03: 类的继承层次
book = PhysicalBook("流畅的Python", "Ramalho", "9781491946008", 2015, 792)

# ch05: 多态 — ABC + Protocol
from app.core.catalog import Catalogable, Borrowable
isinstance(book, Catalogable)   # → True
isinstance(book, Borrowable)    # → True（鸭子类型）

# ch06: 组合 + SOLID
lib = Library("测试馆", notifier=SilentNotification())
lib.add_book(book)
lib.register_member(Member("张三", "z@test.com", "M001"))
lib.borrow("M001", "9781491946008")

# ch09: 元类单例
cfg1, cfg2 = LibraryConfig(), LibraryConfig()
cfg1 is cfg2   # → True
```

## 运行测试

```bash
uv run pytest               # 全部测试
uv run pytest -k "inherit"  # 只运行继承相关测试
uv run pytest -k "magic"    # 只运行魔术方法测试
```

## 章节映射

| 代码文件 | 对应章节 | 核心内容 |
|---------|---------|---------|
| `classes.py` | ch01-05/08 | 类定义、super()、多重继承、Mixin、@property、ABC/Protocol、__str__/__eq__/__hash__/__lt__ |
| `catalog.py` | ch05 | Catalogable(ABC)、Borrowable(Protocol) |
| `library.py` | ch06/08 | 组合、SOLID、NotificationService 依赖注入、__len__/__iter__/__contains__ |
| `member.py` | ch01-04/08 | 类属性/方法、私有属性、@property、魔术方法 |
| `meta.py` | ch09-10 | SingletonMeta 元类、__init_subclass__ 自动注册 |
| `record.py` | ch07 | @dataclass、field(default_factory)、__post_init__、frozen=True |
