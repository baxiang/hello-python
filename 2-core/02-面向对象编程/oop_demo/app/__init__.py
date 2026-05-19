"""图书馆管理系统 — 领域驱动设计示例

项目结构：
    domain/      领域模型 — BookItem, Member, BorrowRecord
    ports/       接口定义 — ABC, Protocol, 依赖倒置
    services/    应用服务 — Library 编排、通知实现
    infra/       基础设施 — 元类、插件注册
    main.py      CLI 入口

教学映射：
    ch01  类的定义与实例化        → domain/book/model.py, domain/member.py
    ch02  类属性/类方法/静态方法  → domain/book/model.py (BookItem.total_books)
    ch03  继承/super()/Mixin     → domain/book/model.py (PhysicalBook/EBook/AudioBook)
    ch04  封装/@property         → domain/book/model.py, domain/member.py
    ch05  ABC/Protocol 多态      → ports/catalog.py
    ch06  组合/SOLID/DI          → services/library.py, ports/notification.py
    ch07  @dataclass             → domain/record.py
    ch08  魔术方法               → 遍布各领域模型
    ch09  元类                   → infra/singleton.py
    ch10  __init_subclass__     → infra/plugin.py
"""
