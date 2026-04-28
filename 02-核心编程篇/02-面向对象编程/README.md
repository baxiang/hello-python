# 面向对象编程

本章讲解 Python 面向对象编程的完整知识体系，从类与对象基础到元类和 `__init_subclass__`。

---

## 快速开始

```bash
# 进入示例项目
cd oop_demo

# 安装依赖
uv sync

# 交互式演示（推荐）— 按章节逐步探索 OOP 概念
uv run python -m app

# 运行测试（59 个测试，全覆盖）
uv run pytest -v
```

---

## 知识地图

```
类与对象基础 ──→ 属性与方法 ──→ 继承 ──→ 封装
      ↓              ↓            ↓         ↓
  class/实例     实例/类属性   super()    @property
  __init__       三种方法     MRO        私有属性
                      ↓
                ┌───────┴───────┐
                ↓               ↓
            多态            设计原则
                ↓               ↓
        ABC / Protocol    SOLID / 组合
                ↓
          ┌─────┴─────┐
          ↓           ↓
       数据类       魔术方法
          ↓           ↓
    @dataclass    __str__/__eq__/__hash__
          │           │
          └─────┬─────┘
                ↓
          元类 ──→ 子类钩子
            ↓           ↓
       metaclass   __init_subclass__
```

---

## 章节导航

| 章节 | 文件 | 主题 | 代码位置 | 验证方式 |
|------|------|------|---------|---------|
| 01 | [类与对象基础](./01-面向对象基础.md) | 类定义、实例化 | `domain/book/model.py` | CLI 菜单 1 / `pytest -k basics` |
| 02 | [属性与方法](./02-属性与方法.md) | 实例/类属性、三种方法 | `domain/book/model.py`, `domain/member.py` | CLI 菜单 2 / `pytest -k basics` |
| 03 | [继承](./03-继承.md) | super()、多重继承 | `domain/book/model.py` | CLI 菜单 3 / `pytest -k inherit` |
| 04 | [封装](./04-封装.md) | @property、私有属性 | `domain/book/model.py`, `domain/member.py` | CLI 菜单 4 / `pytest -k encapsul` |
| 05 | [多态](./05-多态.md) | ABC、Protocol、鸭子类型 | `ports/catalog.py` | CLI 菜单 5 / `pytest -k polymorph` |
| 06 | [设计原则](./06-设计原则.md) | 组合、SOLID | `services/library.py` | CLI 菜单 6 / `pytest -k design` |
| 07 | [数据类](./07-数据类.md) | @dataclass | `domain/record.py` | CLI 菜单 7 / `pytest -k dataclass` |
| 08 | [魔术方法](./08-魔术方法.md) | __str__、__eq__、容器协议 | `domain/member.py`, `services/library.py` | CLI 菜单 8 / `pytest -k magic` |
| 09 | [元类](./09-元类.md) ⭐选读 | metaclass、单例 | `infra/singleton.py` | CLI 菜单 9 / `pytest -k metaclass` |
| 10 | [子类钩子](./10-子类钩子.md) ⭐选读 | __init_subclass__ | `infra/plugin.py` | CLI 菜单 10 / `pytest -k subclass` |

---

## 项目架构

`oop_demo/` 采用 DDD 分层设计，所有文档中的代码示例均来自该项目：

```
oop_demo/
├── domain/      # 领域模型（Book, Member, Record）
├── ports/       # 接口定义（ABC, Protocol）
├── services/    # 应用服务（Library, Notification）
├── infra/       # 基础设施（元类, __init_subclass__）
└── utils/       # 工具函数
```

| 层 | OOP 概念 | 对应章节 |
|----|---------|---------|
| `domain/` | 类定义、继承、封装、属性、魔术方法 | ch01-ch04, ch08 |
| `ports/` | ABC、Protocol、DIP | ch05, ch06 |
| `services/` | 组合、SOLID、依赖注入 | ch06 |
| `infra/` | 元类、`__init_subclass__` | ch09, ch10 |

---

## 交互式演示

运行 `uv run python -m app` 后进入章节菜单：

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
```

每章独立演示，可反复运行感兴趣的章节。
