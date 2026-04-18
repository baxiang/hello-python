# __init_subclass__ 钩子方法

> **难度**：⭐⭐ 进阶
> **预计时间**：30分钟
> **前置知识**：面向对象基础、继承
> **引入版本**：Python 3.6+

本章讲解 `__init_subclass__` 钩子方法，一种比元类更简单的类定制方式。

---

## 为什么需要 __init_subclass__？

### 问题场景

你需要在父类中自动为所有子类添加功能：
- 自动注册子类到注册表
- 自动验证子类是否实现了必需方法
- 自动给子类添加配置参数

**传统方式：使用元类**

```python
plugins: dict[str, type] = {}

class PluginMeta(type):
    def __new__(cls, name, bases, namespace):
        new_class = super().__new__(cls, name, bases, namespace)
        if name != "BasePlugin":
            plugins[name.lower()] = new_class
        return new_class

class BasePlugin(metaclass=PluginMeta):
    pass

class PDFPlugin(BasePlugin):
    def run(self) -> None:
        print("处理 PDF")

class ImagePlugin(BasePlugin):
    def run(self) -> None:
        print("处理图片")

print(plugins)
```

**问题：**
- 需要定义额外的元类
- 元类语法复杂（`__new__`、`__prepare__`）
- 学习曲线陡峭
- 对于简单需求，过度设计

**__init_subclass__ 方式：直接在父类定义**

```python
plugins: dict[str, type] = {}

class BasePlugin:
    def __init_subclass__(cls, **kwargs: object) -> None:
        super().__init_subclass__(**kwargs)
        plugins[cls.__name__.lower()] = cls

class PDFPlugin(BasePlugin):
    def run(self) -> None:
        print("处理 PDF")

class ImagePlugin(BasePlugin):
    def run(self) -> None:
        print("处理图片")

print(plugins)
```

这就是 `__init_subclass__` 的价值：**在父类中定义，子类创建时自动调用，无需元类**。

---

## __init_subclass__ 概念铺垫

```
┌─────────────────────────────────────────────────────────────┐
│          __init_subclass__ 关键概念                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. 什么是 __init_subclass__？                              │
│  ─────────────────────────────────────────────              │
│  • Python 3.6+ 引入的钩子方法                               │
│  • 在父类中定义                                             │
│  • 子类创建时自动调用                                       │
│  • 参数：cls（子类）、**kwargs（自定义参数）                 │
│                                                             │
│  2. 调用时机                                                │
│  ─────────────────────────────────────────────              │
│  • class SubClass(Base) 定义执行后                          │
│  • Python 自动调用 Base.__init_subclass__(SubClass)         │
│  • 在类创建完成后调用                                       │
│                                                             │
│  3. 与元类的区别                                            │
│  ─────────────────────────────────────────────              │
│  元类：                                                      │
│  • 在"类创建过程中"介入                                     │
│  • 可以修改 namespace（类属性字典）                         │
│  • 可以完全控制类创建                                       │
│  • 更强大，也更复杂                                         │
│                                                             │
│  __init_subclass__：                                        │
│  • 在"类创建完成后"介入                                     │
│  • 只能修改已创建的类                                       │
│  • 更简单，更直观                                           │
│  • 适合大多数场景                                           │
│                                                             │
│  4. 调用链                                                  │
│  ─────────────────────────────────────────────              │
│                                                             │
│  class SubClass(Parent):                                   │
│      pass                                                  │
│                                                             │
│  执行流程：                                                  │
│  1. Python 创建 SubClass 类对象                            │
│  2. 自动调用 Parent.__init_subclass__(SubClass)            │
│  3. 如果有多继承，按 MRO 顺序调用各父类的钩子               │
│                                                             │
│  5. 传递参数                                                │
│  ─────────────────────────────────────────────              │
│  class Parent:                                             │
│      def __init_subclass__(cls, config, **kwargs):         │
│          ...                                               │
│                                                             │
│  class Child(Parent, config="value"):                      │
│      pass                                                  │
│                                                             │
│  6. 生活类比                                                │
│  ─────────────────────────────────────────────              │
│  • 父类 = 学校                                              │
│  • 子类 = 新入学班级                                       │
│  • __init_subclass__ = 入学登记                            │
│  • 每个新班级入学时自动登记                                │
│                                                             │
│  学校(Parent) 定义了入学登记规则                           │
│  新班级(Child) 创建后自动登记                              │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## L1 理解层：基础语法

### 语法结构

```
┌─────────────────────────────────────────────────────────────┐
│  __init_subclass__ 语法                                     │
│                                                             │
│  class Parent:                                              │
│      def __init_subclass__(cls, **kwargs) -> None:         │
│          super().__init_subclass__(**kwargs)  # 必须        │
│          # 子类创建后的自定义逻辑                           │
│                                                             │
│  class Child(Parent, custom_param="value"):                │
│      pass                                                   │
│                                                             │
│  参数说明：                                                  │
│  cls        → 正在创建的子类（类对象）                       │
│  **kwargs   → class 定义中传入的额外参数                    │
│                                                             │
│  关键要点：                                                  │
│  1. 必须调用 super().__init_subclass__(**kwargs)           │
│  2. 参数通过 class 定义传递：class Child(Parent, param=val)│
│  3. 在子类定义完成后调用                                    │
└─────────────────────────────────────────────────────────────┘
```

### 最简示例

```python
class Base:
    def __init_subclass__(cls, **kwargs: object) -> None:
        super().__init_subclass__(**kwargs)
        print(f"[钩子] 子类 {cls.__name__} 已创建")

class ChildA(Base):
    pass

class ChildB(Base):
    pass
```

**运行结果：**

```
[钩子] 子类 ChildA 已创建
[钩子] 子类 ChildB 已创建
```

**说明：**
- ChildA 定义后，自动调用 Base.__init_subclass__(ChildA)
- ChildB 定义后，自动调用 Base.__init_subclass__(ChildB)
- 无需手动调用，Python 自动触发

### 详细示例：传递参数

```python
class Base:
    def __init_subclass__(
        cls,
        version: str = "1.0",
        enabled: bool = True,
        **kwargs: object,
    ) -> None:
        super().__init_subclass__(**kwargs)
        cls._version = version
        cls._enabled = enabled
        print(f"[钩子] {cls.__name__}: version={version}, enabled={enabled}")

class PluginA(Base, version="2.0"):
    pass

class PluginB(Base, enabled=False):
    pass

class PluginC(Base, version="3.0", enabled=True):
    pass

print(PluginA._version)
print(PluginA._enabled)
print(PluginB._version)
print(PluginB._enabled)
print(PluginC._version)
print(PluginC._enabled)
```

**运行结果：**

```
[钩子] PluginA: version=2.0, enabled=True
[钩子] PluginB: version=1.0, enabled=False
[钩子] PluginC: version=3.0, enabled=True
2.0
True
1.0
False
3.0
True
```

**关键代码说明：**

| 代码 | 含义 |
|------|------|
| `def __init_subclass__(cls, version="1.0", ...)` | 定义钩子，接受自定义参数 |
| `super().__init_subclass__(**kwargs)` | 必须调用，支持多继承 |
| `class PluginA(Base, version="2.0")` | 在类定义中传递参数 |
| `cls._version = version` | 给子类添加属性 |
| `PluginA._version` | 访问子类属性 |

---

## L2 实践层：实际应用

### 实际应用场景

#### 场景1：自动注册子类

```python
handlers: dict[str, type] = {}

class HandlerBase:
    def __init_subclass__(cls, **kwargs: object) -> None:
        super().__init_subclass__(**kwargs)
        handler_name = cls.__name__.lower().replace("handler", "")
        handlers[handler_name] = cls
    
    def handle(self, data: str) -> str:
        raise NotImplementedError

class PDFHandler(HandlerBase):
    def handle(self, data: str) -> str:
        return f"处理PDF: {data}"

class ImageHandler(HandlerBase):
    def handle(self, data: str) -> str:
        return f"处理图片: {data}"

class VideoHandler(HandlerBase):
    def handle(self, data: str) -> str:
        return f"处理视频: {data}"

print(handlers)

for name, handler_class in handlers.items():
    handler = handler_class()
    print(handler.handle("test_file"))
```

**运行结果：**

```
{'pdf': <class 'PDFHandler'>, 'image': <class 'ImageHandler'>, 'video': <class 'VideoHandler'>}
处理PDF: test_file
处理图片: test_file
处理视频: test_file
```

**说明：**
- 所有 Handler 子类自动注册到 handlers 字典
- HandlerBase 被排除（名字处理逻辑）
- 无需手动注册，减少遗漏风险

#### 场景2：验证子类实现必需方法

```python
class ValidatorBase:
    required_methods: list[str] = ["validate", "get_errors"]
    
    def __init_subclass__(cls, **kwargs: object) -> None:
        super().__init_subclass__(**kwargs)
        for method_name in cls.required_methods:
            if not hasattr(cls, method_name):
                raise TypeError(
                    f"{cls.__name__} 必须实现方法: {method_name}"
                )

class GoodValidator(ValidatorBase):
    def validate(self, data: dict[str, object]) -> bool:
        return True
    
    def get_errors(self) -> list[str]:
        return []

try:
    class BadValidator(ValidatorBase):
        def validate(self, data: dict[str, object]) -> bool:
            return True
except TypeError as e:
    print(f"错误: {e}")
```

**运行结果：**

```
错误: BadValidator 必须实现方法: get_errors
```

**说明：**
- 子类创建时自动验证是否实现必需方法
- 未实现则抛出 TypeError，阻止类创建
- 强制子类遵守接口规范

#### 场景3：配置参数注入

```python
class ConfigurableBase:
    def __init_subclass__(
        cls,
        api_version: str = "v1",
        timeout: int = 30,
        **kwargs: object,
    ) -> None:
        super().__init_subclass__(**kwargs)
        cls._api_version = api_version
        cls._timeout = timeout

class UserService(ConfigurableBase, api_version="v2", timeout=60):
    def get_user(self, user_id: int) -> dict[str, object]:
        return {
            "id": user_id,
            "api_version": self._api_version,
            "timeout": self._timeout,
        }

class ProductService(ConfigurableBase, timeout=120):
    def get_product(self, sku: str) -> dict[str, object]:
        return {
            "sku": sku,
            "api_version": self._api_version,
            "timeout": self._timeout,
        }

user_service = UserService()
print(user_service.get_user(1))

product_service = ProductService()
print(product_service.get_product("ABC123"))
```

**运行结果：**

```
{'id': 1, 'api_version': 'v2', 'timeout': 60}
{'sku': 'ABC123', 'api_version': 'v1', 'timeout': 120}
```

**说明：**
- 子类通过 class 定义传递配置参数
- 默认值可被覆盖
- 配置自动注入到子类属性

#### 场景4：多继承中的调用顺序

```python
class BaseA:
    def __init_subclass__(cls, **kwargs: object) -> None:
        super().__init_subclass__(**kwargs)
        print(f"[BaseA] {cls.__name__} 创建")
        cls._from_a = True

class BaseB:
    def __init_subclass__(cls, **kwargs: object) -> None:
        super().__init_subclass__(**kwargs)
        print(f"[BaseB] {cls.__name__} 创建")
        cls._from_b = True

class Child(BaseA, BaseB):
    pass

print(Child._from_a)
print(Child._from_b)
```

**运行结果：**

```
[BaseA] Child 创建
[BaseB] Child 创建
True
True
```

**说明：**
- 多继承时，按 MRO 顺序调用各父类的 __init_subclass__
- 必须调用 super().__init_subclass__(**kwargs) 才能触发链式调用
- 每个父类的钩子都会执行

### 推荐做法

| 做法 | 原因 | 示例 |
|------|------|------|
| **替代简单元类场景** | 更简单，无需定义额外元类 | 自动注册、参数注入 |
| **必须调用 super()** | 支持多继承，避免断链 | `super().__init_subclass__(**kwargs)` |
| **使用 **kwargs** | 避免参数传递问题 | 接收并传递未处理的参数 |
| **在父类定义钩子** | 所有子类自动受益 | 集中控制逻辑 |

### 反模式：不要这样做

#### 错误1：忘记调用 super()

```python
class BaseA:
    def __init_subclass__(cls, **kwargs: object) -> None:
        print(f"[BaseA] {cls.__name__}")
        cls._from_a = True

class BaseB:
    def __init_subclass__(cls, **kwargs: object) -> None:
        print(f"[BaseB] {cls.__name__}")
        cls._from_b = True

class Child(BaseA, BaseB):
    pass
```

**问题：**
- BaseA.__init_subclass__ 没有调用 super()
- BaseB.__init_subclass__ 不会被调用
- 多继承链断裂

```python
class BaseA:
    def __init_subclass__(cls, **kwargs: object) -> None:
        super().__init_subclass__(**kwargs)
        print(f"[BaseA] {cls.__name__}")
        cls._from_a = True

class BaseB:
    def __init_subclass__(cls, **kwargs: object) -> None:
        super().__init_subclass__(**kwargs)
        print(f"[BaseB] {cls.__name__}")
        cls._from_b = True

class Child(BaseA, BaseB):
    pass

print(Child._from_a)
print(Child._from_b)
```

#### 错误2：在子类中重写 __init_subclass__

```python
class Parent:
    def __init_subclass__(cls, **kwargs: object) -> None:
        super().__init_subclass__(**kwargs)
        print(f"[Parent] {cls.__name__}")

class Child(Parent):
    def __init_subclass__(cls, **kwargs: object) -> None:
        print(f"[Child] 子类不应该重写这个方法")

class GrandChild(Child):
    pass
```

**问题：**
- __init_subclass__ 应在父类定义，子类不应重写
- 重写会导致 Parent 的钩子不再被调用

```python
class Parent:
    def __init_subclass__(cls, **kwargs: object) -> None:
        super().__init_subclass__(**kwargs)
        print(f"[Parent] {cls.__name__}")

class Child(Parent):
    pass

class GrandChild(Child):
    pass
```

#### 错误3：尝试修改 namespace

```python
class Parent:
    def __init_subclass__(cls, **kwargs: object) -> None:
        super().__init_subclass__(**kwargs)
        cls.new_attr = "added"

class Child(Parent):
    existing_attr = "original"

print(Child.existing_attr)
print(Child.new_attr)
```

**说明：**
- __init_subclass__ 在类创建后调用，无法修改 namespace
- 可以添加新属性，但无法改变原有属性的定义方式
- 如需修改 namespace，必须用元类

### 与元类对比

```
┌─────────────────────────────────────────────────────────────┐
│          __init_subclass__ vs 元类                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  能力对比：                                                  │
│                                                             │
│  ┌─────────────────────┬───────────────────────┐           │
│  │ __init_subclass__   │        元类           │           │
│  ├─────────────────────┼───────────────────────┤           │
│  │ 修改已创建的类      │ 修改 namespace        │           │
│  │ 添加类属性          │ 完全控制类创建        │           │
│  │ 注册子类            │ 自定义 __prepare__    │           │
│  │ 验证子类            │ 控制 __new__          │           │
│  │ 简单直观            │ 更强大更复杂          │           │
│  └─────────────────────┴───────────────────────┘           │
│                                                             │
│  选择建议：                                                  │
│                                                             │
│  ✅ 用 __init_subclass__：                                  │
│     • 自动注册子类                                          │
│     • 参数注入                                              │
│     • 验证子类                                              │
│     • 简单定制                                              │
│                                                             │
│  ✅ 用元类：                                                 │
│     • 需要修改 namespace                                    │
│     • 框架开发（ORM）                                       │
│     • 需要 __prepare__                                      │
│     • 完全控制类创建                                        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 适用场景

| 场景 | 推荐 | 原因 |
|------|------|------|
| 自动注册子类 | ✅ __init_subclass__ | 简单，无需元类 |
| 参数配置注入 | ✅ __init_subclass__ | 参数传递直观 |
| 验证子类接口 | ✅ __init_subclass__ | 类创建时自动验证 |
| 简单类定制 | ✅ __init_subclass__ | 比元类更简单 |
| 修改 namespace | ❌ 用元类 | __init_subclass__ 无法做到 |
| 需要 __prepare__ | ❌ 用元类 | 只有元类有此方法 |
| 框架开发（ORM） | ❓ 视需求 | 简单 ORM 可用 __init_subclass__ |

---

## L3 专家层：底层原理

### 调用时机详解

```
┌─────────────────────────────────────────────────────────────┐
│          __init_subclass__ 调用时机                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  class SubClass(Parent, param="value"):                    │
│      attr = 100                                             │
│                                                             │
│  Python 执行流程：                                          │
│                                                             │
│  1. 准备 namespace                                         │
│     namespace = {"attr": 100, "__module__": ...}           │
│                                                             │
│  2. 确定元类（默认 type）                                  │
│     metaclass = type                                       │
│                                                             │
│  3. 调用 type.__new__                                       │
│     cls = type.__new__(type, "SubClass", (Parent,), ns)    │
│     ← 类对象创建完成                                        │
│                                                             │
│  4. 调用 type.__init__                                      │
│     type.__init__(cls, "SubClass", (Parent,), ns)          │
│                                                             │
│  5. 调用 Parent.__init_subclass__ ← 这里！                 │
│     Parent.__init_subclass__(SubClass, param="value")      │
│                                                             │
│  6. 返回类对象                                              │
│     SubClass = cls                                          │
│                                                             │
│  关键点：                                                    │
│  • __init_subclass__ 在类对象创建完成后调用                │
│  • 无法修改 namespace（已创建完成）                         │
│  • 可以修改已创建的类对象                                   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 参数传递机制

```python
class Parent:
    def __init_subclass__(
        cls,
        custom: str = "default",
        **kwargs: object,
    ) -> None:
        super().__init_subclass__(**kwargs)
        print(f"custom={custom}, kwargs={kwargs}")

class Child(Parent, custom="value", extra="data"):
    pass
```

**运行结果：**

```
custom=value, kwargs={'extra': 'data'}
```

**说明：**
- `custom="value"` 被显式参数接收
- `extra="data"` 被打包到 **kwargs
- 未被处理的参数通过 super().__init_subclass__(**kwargs) 传递

### MRO 与调用顺序

```python
class A:
    def __init_subclass__(cls, **kwargs: object) -> None:
        super().__init_subclass__(**kwargs)
        print(f"[A] {cls.__name__}")

class B:
    def __init_subclass__(cls, **kwargs: object) -> None:
        super().__init_subclass__(**kwargs)
        print(f"[B] {cls.__name__}")

class C:
    def __init_subclass__(cls, **kwargs: object) -> None:
        super().__init_subclass__(**kwargs)
        print(f"[C] {cls.__name__}")

class Child(A, B, C):
    pass

print(f"MRO: {Child.__mro__}")
```

**运行结果：**

```
[A] Child
[B] Child
[C] Child
MRO: (<class 'Child'>, <class 'A'>, <class 'B'>, <class 'C'>, <class 'object'>)
```

**说明：**
- 按照子类 → A → B → C → object 的 MRO 顺序
- 每个类的 __init_subclass__ 都被调用
- super().__init_subclass__(**kwargs) 负责链式传递

### 设计动机

| 设计选择 | 原因 |
|----------|------|
| 引入 __init_subclass__ | 元类太复杂，大多数场景只需简单定制 |
| 在类创建后调用 | 比 __new__ 更简单，不涉及 namespace |
| 通过 class 定义传递参数 | 参数传递直观，无需额外机制 |
| 必须调用 super() | 支持多继承，保证链式调用 |

**PEP 487 设计动机：**

> "许多定制类的需求实际上只需要在类创建后做一些操作，而不是在创建过程中修改类结构。__init_subclass__ 提供了一种比元类更简单的解决方案。"

### 知识关联

```
知识关联图：
┌─────────────────┐     ┌─────────────────┐
│   面向对象基础   │────→│ __init_subclass │
│   继承          │     │   (钩子方法)     │
└─────────────────┘     └─────────────────┘
        │                       │
        ↓                       ↓
┌─────────────────┐     ┌─────────────────┐
│   super()       │     │     元类        │
│   MRO           │     │   metaclass     │
└─────────────────┘     └─────────────────┘
        │                       │
        ↓                       ↓
┌─────────────────┐     ┌─────────────────┐
│   类装饰器      │     │   __prepare__   │
│   (替代方案)    │     │   (元类专属)    │
└─────────────────┘     └─────────────────┘
```

---

## 自检清单

回答以下问题，检查你是否掌握了核心概念：

1. __init_subclass__ 的第一个参数是什么？
2. 为什么必须调用 `super().__init_subclass__(**kwargs)`？
3. __init_subclass__ 和元类的调用时机有什么区别？
4. 如何在子类定义中传递参数给 __init_subclass__？
5. __init_subclass__ 能修改 namespace 吗？为什么？

---

## 本章术语表

| 术语 | 定义 | 本章位置 |
|------|------|---------|
| __init_subclass__ | Python 3.6+ 钩子方法，子类创建时自动调用 | 概念铺垫 |
| cls 参数 | 正在创建的子类（类对象） | L1理解层 |
| **kwargs | class 定义中传递的额外参数 | L1理解层 |
| MRO | 方法解析顺序，决定多继承时的调用顺序 | L3专家层 |
| 钩子方法 | 在特定时机自动调用的方法 | 概念铺垫 |

---

## 扩展阅读

- PEP 487：Simpler customization of class creation
- 《流畅的Python》第19章：元类（__init_subclass__ 作为替代方案）
- Python 官方文档：__init_subclass__