# 面向对象编程

Python OOP 示例项目，覆盖第 01-10 章（类基础 → 属性 → 继承 → 封装 → 多态 → SOLID → 数据类 → 魔术方法 → 元类 → `__init_subclass__`）。

## 快速开始

```bash
# 安装依赖
uv sync

# 交互式演示（推荐）— 按章节逐步探索 OOP 概念
uv run python -m app

# 运行测试（59 个测试，全覆盖）
uv run pytest -v
```

## 架构

领域驱动分层设计，贴近工程实践：

```
oop_demo/
├── pyproject.toml
├── app/
│   ├── __main__.py            # 模块入口（uv run python -m app）
│   ├── main.py                # 交互式 CLI 菜单 — 10 章独立演示
│   ├── domain/                # 领域模型（业务实体）
│   │   ├── book/
│   │   │   ├── model.py       # BookItem / PhysicalBook / EBook / AudioBook
│   │   │   └── mixins.py      # DigitalMixin
│   │   ├── member.py          # Member
│   │   └── record.py          # BorrowRecord (dataclass)
│   ├── ports/                 # 接口定义（依赖倒置）
│   │   ├── catalog.py         # Catalogable(ABC) + Borrowable(Protocol)
│   │   └── notification.py    # NotificationService(Protocol)
│   ├── services/              # 应用服务（流程编排）
│   │   ├── library.py         # Library — 借还/查询/会员管理
│   │   └── notification.py    # Console/Silent/Email 实现
│   ├── infra/                 # 基础设施（技术实现）
│   │   ├── singleton.py       # SingletonMeta 元类
│   │   └── plugin.py          # BookPlugin (__init_subclass__)
│   └── utils/
│       └── helpers.py
└── tests/
    └── test_oop.py            # 59 个测试，全覆盖
```

**分层职责：**

| 层 | 职责 | OOP 概念 |
|----|------|---------|
| `domain/` | 业务实体与规则 | 继承、封装、属性、魔术方法 |
| `ports/` | 接口定义（抽象） | ABC、Protocol、DIP |
| `services/` | 业务流程编排 | 组合、SOLID、依赖注入 |
| `infra/` | 技术实现细节 | 元类、`__init_subclass__` |

## 交互式演示

运行 `uv run python -m app` 后进入菜单：

```
  📚 图书馆管理系统 — OOP 学习演示

  1.  类与对象基础
  2.  属性与方法
  3.  继承
  4.  封装
  5.  多态
  6.  设计原则（SOLID）
  7.  数据类（@dataclass）
  8.  魔术方法
  9.  元类（metaclass）
  10. 子类钩子（__init_subclass__）

  0.  退出
```

- 输入章节号查看该章演示
- 每章演示后按 Enter 返回菜单
- 可反复运行感兴趣的章节

## 章节映射

| 代码文件 | 对应章节 | 核心内容 |
|---------|---------|---------|
| `domain/book/model.py` | ch01-05/08 | 类定义、super()、多重继承、Mixin、@property、ABC/Protocol、魔术方法 |
| `domain/book/mixins.py` | ch03 | DigitalMixin 多重继承 |
| `domain/member.py` | ch01-04/08 | 类属性/方法、私有属性、@property 验证、魔术方法 |
| `domain/record.py` | ch07 | @dataclass、field(default_factory)、__post_init__、frozen |
| `ports/catalog.py` | ch05 | Catalogable(ABC)、Borrowable(Protocol) |
| `ports/notification.py` | ch06 | NotificationService(Protocol) 依赖倒置 |
| `services/library.py` | ch06/08 | 组合、SOLID、依赖注入、容器魔术方法 |
| `services/notification.py` | ch06 | Console/Silent/Email 通知实现 |
| `infra/singleton.py` | ch09 | SingletonMeta 元类、全局唯一配置 |
| `infra/plugin.py` | ch10 | __init_subclass__ 自动插件注册 |
| `main.py` | 全章整合 | 交互式菜单 + 10 章独立演示 |
