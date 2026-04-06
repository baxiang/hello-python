# 类型提示子目录重构实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 重构类型提示子目录，应用渐进式教学，扩展高级内容，完善示例项目

**Architecture:** 三份文档（基础/进阶/高级），示例项目拆分为四个模块（basics/generics/protocols/advanced），每个模块对应独立测试

**Tech Stack:** Python 3.11+, pytest, typing 模块

---

## File Structure

```
创建文件：
- docs/superpowers/specs/2026-04-06-type-hints-refactoring-design.md (已完成)
- docs/superpowers/plans/2026-04-06-type-hints-refactoring-plan.md (本文件)
- 02-核心编程篇/类型提示/02-类型进阶应用.md
- 02-核心编程篇/类型提示/03-高级类型特性.md
- 02-核心编程篇/类型提示/type_hints_demo/app/core/basics.py
- 02-核心编程篇/类型提示/type_hints_demo/app/core/generics.py
- 02-核心编程篇/类型提示/type_hints_demo/app/core/protocols.py
- 02-核心编程篇/类型提示/type_hints_demo/app/core/advanced.py
- 02-核心编程篇/类型提示/type_hints_demo/tests/test_basics.py
- 02-核心编程篇/类型提示/type_hints_demo/tests/test_generics.py
- 02-核心编程篇/类型提示/type_hints_demo/tests/test_protocols.py
- 02-核心编程篇/类型提示/type_hints_demo/tests/test_advanced.py

修改文件：
- 02-核心编程篇/类型提示/01-类型提示基础.md
- 02-核心编程篇/类型提示/README.md
- 02-核心编程篇/类型提示/type_hints_demo/README.md
- 02-核心编程篇/类型提示/type_hints_demo/pyproject.toml

删除文件：
- 02-核心编程篇/类型提示/type_hints_demo/app/core/type_hints.py
- 02-核心编程篇/类型提示/type_hints_demo/tests/test_type_hints.py
```

---

## Task 1: 重构 01-类型提示基础.md

**Files:**
- Modify: `02-核心编程篇/类型提示/01-类型提示基础.md`

- [ ] **Step 1: 精简现有内容，删除与入门篇重复的"为什么要用类型提示"部分**

保留 Python 版本要求说明，删除第 1 节"为什么要用类型提示"，将基础类型注解部分简化为快速回顾。

- [ ] **Step 2: 应用 6 步渐进式教学结构重写容器类型章节**

将现有第 3 节"容器类型详解"按 6 步法重写：
- 问题引入
- 概念解释
- 最简示例
- 详细说明
- 渐进复杂
- 实际应用

- [ ] **Step 3: 重写 Optional 和 Union 章节**

将第 4 节按 6 步法重写，重点展示 str | None 语法和实际使用场景。

- [ ] **Step 4: 重写 Callable 章节**

将第 5 节按 6 步法重写，添加策略模式示例。

- [ ] **Step 5: 重写类型别名章节**

将第 8 节按 6 步法重写，添加 NewType 对比说明。

- [ ] **Step 6: 更新章节导航链接**

确保文档末尾导航链接指向正确的文件名。

- [ ] **Step 7: 提交修改**

```bash
git add 02-核心编程篇/类型提示/01-类型提示基础.md
git commit -m "Refactor type hints basics with progressive teaching"
```

---

## Task 2: 创建 02-类型进阶应用.md

**Files:**
- Create: `02-核心编程篇/类型提示/02-类型进阶应用.md`

- [ ] **Step 1: 创建文档头部和 Python 版本要求**

```markdown
# 第 9 章：类型进阶应用

> **Python 版本要求：3.11+**
> 本章使用 Python 3.11+ 现代语法...

深入掌握 Python 类型系统的进阶特性。
```

- [ ] **Step 2: 编写泛型深入理解章节（6 步法）**

从现有 02-类型注解进阶.md 第 2 节提取泛型内容，按 6 步法组织。

- [ ] **Step 3: 编写协议 Protocol 章节（6 步法）**

从现有文档提取协议内容，添加协议继承和 runtime_checkable 示例。

- [ ] **Step 4: 编写 TypedDict 章节（6 步法）**

从现有文档第 4 节提取内容，添加 ReadOnly 示例。

- [ ] **Step 5: 编写运行时类型检查章节（6 步法）**

从现有文档第 1 节提取内容，保留 get_type_hints 和验证装饰器示例。

- [ ] **Step 6: 编写类型守卫章节（6 步法）**

从现有文档第 5 节提取 TypeGuard 内容。

- [ ] **Step 7: 提交新文档**

```bash
git add 02-核心编程篇/类型提示/02-类型进阶应用.md
git commit -m "Create advanced type hints application document"
```

---

## Task 3: 创建 03-高级类型特性.md

**Files:**
- Create: `02-核心编程篇/类型提示/03-高级类型特性.md`

- [ ] **Step 1: 创建文档头部**

```markdown
# 第 10 章：高级类型特性

> **Python 版本要求：3.12+**
> 本章涉及部分 Python 3.12+ 新特性...

探索类型系统的高级特性。
```

- [ ] **Step 2: 编写参数规格类型章节**

```python
from typing import ParamSpec, Concatenate, Callable, TypeVar

P = ParamSpec('P')
R = TypeVar('R')

def decorator(
    func: Callable[P, R]
) -> Callable[P, R]:
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        print("Before call")
        return func(*args, **kwargs)
    return wrapper
```

- [ ] **Step 3: 编写类相关类型章节**

```python
from typing import Final, ClassVar

class Config:
    MAX_SIZE: ClassVar[Final[int]] = 100
    version: Final[str] = "1.0.0"
    
    @final
    def get_version(self) -> str:
        return self.version
```

- [ ] **Step 4: 编写类型守卫进阶章节**

```python
from typing import TypeGuard, TypeIs

def is_string_list(val: list[object]) -> TypeGuard[list[str]]:
    return all(isinstance(x, str) for x in val)

# TypeIs 示例（Python 3.13+）
def is_positive(val: int) -> TypeIs[int]:
    return val > 0
```

- [ ] **Step 5: 编写 Python 3.12+ 新特性章节**

```python
# type 语句定义类型别名
type Point = tuple[float, float]
type Vector[T] = list[T]

# TypeAlias 注解
from typing import TypeAlias
UserId: TypeAlias = int
```

- [ ] **Step 6: 提交新文档**

```bash
git add 02-核心编程篇/类型提示/03-高级类型特性.md
git commit -m "Create advanced type features document"
```

---

## Task 4: 更新 README.md 导航

**Files:**
- Modify: `02-核心编程篇/类型提示/README.md`

- [ ] **Step 1: 更新章节导航表格**

```markdown
| 章节 | 文件 | 主题 |
|------|------|------|
| 01 | [01-类型提示基础.md](./01-类型提示基础.md) | 容器类型、Optional、Union、Callable、类型别名 |
| 02 | [02-类型进阶应用.md](./02-类型进阶应用.md) | 泛型深入、协议、TypedDict、运行时检查、类型守卫 |
| 03 | [03-高级类型特性.md](./03-高级类型特性.md) | ParamSpec、Final、ClassVar、Python 3.12+ 特性 |
```

- [ ] **Step 2: 提交修改**

```bash
git add 02-核心编程篇/类型提示/README.md
git commit -m "Update type hints README navigation"
```

---

## Task 5: 创建 basics.py 示例模块

**Files:**
- Create: `02-核心编程篇/类型提示/type_hints_demo/app/core/basics.py`

- [ ] **Step 1: 编写容器类型示例**

```python
"""基础类型提示示例"""

from typing import Callable, Any


def count_words(text: str) -> dict[str, int]:
    """统计单词频率"""
    result: dict[str, int] = {}
    for word in text.split():
        result[word] = result.get(word, 0) + 1
    return result


def get_point() -> tuple[float, float]:
    """获取坐标点"""
    return (10.5, 20.3)


def unique_items(items: list[str]) -> set[str]:
    """获取唯一元素"""
    return set(items)
```

- [ ] **Step 2: 编写 Optional/Union 示例**

```python
def find_user(user_id: int) -> dict[str, str] | None:
    """查找用户"""
    users: dict[int, dict[str, str]] = {
        1: {"name": "张三", "email": "zhangsan@example.com"},
        2: {"name": "李四", "email": "lisi@example.com"},
    }
    return users.get(user_id)


def parse_value(value: str) -> int | float | bool:
    """解析字符串值"""
    if value.isdigit():
        return int(value)
    try:
        return float(value)
    except ValueError:
        return value.lower() == "true"
```

- [ ] **Step 3: 编写 Callable 示例**

```python
def apply_operation(
    func: Callable[[int, int], int],
    a: int,
    b: int
) -> int:
    """应用运算函数"""
    return func(a, b)


def callback_pattern(callback: Callable[[str], None]) -> None:
    """回调模式示例"""
    message = "处理完成"
    callback(message)
```

- [ ] **Step 4: 编写类型别名示例**

```python
UserId = int
UserName = str
UserDict = dict[UserName, int]


def get_user_score(user_id: UserId) -> UserDict | None:
    """获取用户分数"""
    scores: UserDict = {"张三": 85, "李四": 92}
    if user_id in [1, 2]:
        return scores
    return None
```

- [ ] **Step 5: 提交新模块**

```bash
git add 02-核心编程篇/类型提示/type_hints_demo/app/core/basics.py
git commit -m "Add basics type hints examples module"
```

---

## Task 6: 创建 generics.py 示例模块

**Files:**
- Create: `02-核心编程篇/类型提示/type_hints_demo/app/core/generics.py`

- [ ] **Step 1: 编写泛型函数示例**

```python
"""泛型示例"""

from typing import TypeVar, Generic

T = TypeVar('T')


def first(items: list[T]) -> T:
    """返回列表第一个元素"""
    return items[0]


def reverse(items: list[T]) -> list[T]:
    """反转列表"""
    return items[::-1]


def get_middle(items: list[T]) -> T:
    """获取中间元素"""
    return items[len(items) // 2]
```

- [ ] **Step 2: 编写泛型约束示例**

```python
Number = TypeVar('Number', int, float)


def double(value: Number) -> Number:
    """翻倍数值"""
    return value * 2


def add_numbers(a: Number, b: Number) -> Number:
    """数字相加"""
    return a + b
```

- [ ] **Step 3: 编写 Stack 泛型类**

```python
class Stack(Generic[T]):
    """泛型栈"""
    
    def __init__(self) -> None:
        self._items: list[T] = []
    
    def push(self, item: T) -> None:
        self._items.append(item)
    
    def pop(self) -> T:
        if not self._items:
            raise IndexError("栈为空")
        return self._items.pop()
    
    def peek(self) -> T:
        if not self._items:
            raise IndexError("栈为空")
        return self._items[-1]
    
    def is_empty(self) -> bool:
        return len(self._items) == 0
```

- [ ] **Step 4: 编写 Repository 泛型类**

```python
from dataclasses import dataclass


@dataclass
class Entity:
    id: int


class Repository(Generic[T]):
    """泛型仓储"""
    
    def __init__(self) -> None:
        self._storage: list[T] = []
    
    def add(self, item: T) -> int:
        self._storage.append(item)
        return len(self._storage) - 1
    
    def get(self, index: int) -> T | None:
        if 0 <= index < len(self._storage):
            return self._storage[index]
        return None
    
    def get_all(self) -> list[T]:
        return self._storage.copy()
```

- [ ] **Step 5: 提交新模块**

```bash
git add 02-核心编程篇/类型提示/type_hints_demo/app/core/generics.py
git commit -m "Add generics examples module"
```

---

## Task 7: 创建 protocols.py 示例模块

**Files:**
- Create: `02-核心编程篇/类型提示/type_hints_demo/app/core/protocols.py`

- [ ] **Step 1: 编写基础协议示例**

```python
"""协议示例"""

from typing import Protocol, runtime_checkable


class Drawable(Protocol):
    """绘制协议"""
    
    def draw(self) -> None: ...


class Circle:
    """圆形"""
    
    def draw(self) -> None:
        print("画圆")


class Square:
    """正方形"""
    
    def draw(self) -> None:
        print("画正方形")


def render(shape: Drawable) -> None:
    """渲染图形"""
    shape.draw()
```

- [ ] **Step 2: 编写 Comparable 协议**

```python
class Comparable(Protocol):
    """可比较协议"""
    
    def compare_to(self, other: "Comparable") -> int: ...


class Person:
    """人员类"""
    
    def __init__(self, name: str, age: int) -> None:
        self.name = name
        self.age = age
    
    def compare_to(self, other: "Person") -> int:
        return self.age - other.age
```

- [ ] **Step 3: 编写 runtime_checkable 协议**

```python
@runtime_checkable
class Serializable(Protocol):
    """可序列化协议"""
    
    def to_json(self) -> str: ...


class User:
    """用户类"""
    
    def __init__(self, name: str, age: int) -> None:
        self.name = name
        self.age = age
    
    def to_json(self) -> str:
        return f'{"name": "{self.name}", "age": {self.age}}'
```

- [ ] **Step 4: 编写 TypedDict 示例**

```python
from typing import TypedDict


class UserDict(TypedDict):
    """用户字典类型"""
    
    id: int
    name: str
    email: str
    age: int | None


class ConfigDict(TypedDict, total=False):
    """配置字典类型（所有字段可选）"""
    
    host: str
    port: int
    debug: bool


def create_user(data: UserDict) -> UserDict:
    """创建用户"""
    return data
```

- [ ] **Step 5: 提交新模块**

```bash
git add 02-核心编程篇/类型提示/type_hints_demo/app/core/protocols.py
git commit -m "Add protocols and TypedDict examples module"
```

---

## Task 8: 创建 advanced.py 示例模块

**Files:**
- Create: `02-核心编程篇/类型提示/type_hints_demo/app/core/advanced.py`

- [ ] **Step 1: 编写 ParamSpec 示例**

```python
"""高级类型特性示例"""

from typing import ParamSpec, Concatenate, Callable, TypeVar

P = ParamSpec('P')
R = TypeVar('R')


def log_call(func: Callable[P, R]) -> Callable[P, R]:
    """日志装饰器"""
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        print(f"Calling {func.__name__}")
        return func(*args, **kwargs)
    return wrapper
```

- [ ] **Step 2: 编写 Final/ClassVar 示例**

```python
from typing import Final, ClassVar


class Config:
    """配置类"""
    
    MAX_SIZE: ClassVar[Final[int]] = 100
    MIN_SIZE: ClassVar[Final[int]] = 1
    DEFAULT_PORT: Final[int] = 8080
    
    def __init__(self, port: int) -> None:
        self.port: Final[int] = port


class BaseService:
    """基础服务"""
    
    VERSION: ClassVar[str] = "1.0.0"
    
    @final
    def get_version(self) -> str:
        return self.VERSION
```

- [ ] **Step 3: 编写 TypeGuard 示例**

```python
from typing import TypeGuard, Any


def is_string_list(val: list[Any]) -> TypeGuard[list[str]]:
    """类型守卫：检查是否为字符串列表"""
    return all(isinstance(x, str) for x in val)


def is_positive_dict(val: dict[str, Any]) -> TypeGuard[dict[str, int]]:
    """类型守卫：检查是否为正整数值字典"""
    return all(isinstance(v, int) and v > 0 for v in val.values())


def process_data(items: list[Any]) -> str:
    """处理数据"""
    if is_string_list(items):
        return " ".join(items)
    return "非字符串列表"
```

- [ ] **Step 4: 编写类型别名新语法示例**

```python
# Python 3.12+ type 语句
# type Point = tuple[float, float]
# type Vector[T] = list[T]

from typing import TypeAlias

UserId: TypeAlias = int
UserName: TypeAlias = str
```

- [ ] **Step 5: 提交新模块**

```bash
git add 02-核心编程篇/类型提示/type_hints_demo/app/core/advanced.py
git commit -m "Add advanced type features examples module"
```

---

## Task 9: 创建 test_basics.py 测试

**Files:**
- Create: `02-核心编程篇/类型提示/type_hints_demo/tests/test_basics.py`

- [ ] **Step 1: 编写容器类型测试**

```python
"""基础类型提示测试"""

from app.core.basics import count_words, get_point, unique_items


def test_count_words():
    result = count_words("hello world hello")
    assert result["hello"] == 2
    assert result["world"] == 1


def test_get_point():
    x, y = get_point()
    assert x == 10.5
    assert y == 20.3


def test_unique_items():
    result = unique_items(["a", "b", "a", "c"])
    assert result == {"a", "b", "c"}
```

- [ ] **Step 2: 编写 Optional/Union 测试**

```python
from app.core.basics import find_user, parse_value


def test_find_user():
    user = find_user(1)
    assert user is not None
    assert user["name"] == "张三"
    
    user = find_user(999)
    assert user is None


def test_parse_value():
    assert parse_value("123") == 123
    assert parse_value("3.14") == 3.14
    assert parse_value("true") == True
```

- [ ] **Step 3: 编写 Callable 测试**

```python
from app.core.basics import apply_operation


def test_apply_operation():
    assert apply_operation(lambda x, y: x + y, 5, 3) == 8
    assert apply_operation(lambda x, y: x * y, 5, 3) == 15
```

- [ ] **Step 4: 运行测试验证**

```bash
cd 02-核心编程篇/类型提示/type_hints_demo && uv run pytest tests/test_basics.py -v
```

- [ ] **Step 5: 提交测试**

```bash
git add 02-核心编程篇/类型提示/type_hints_demo/tests/test_basics.py
git commit -m "Add basics module tests"
```

---

## Task 10: 创建 test_generics.py 测试

**Files:**
- Create: `02-核心编程篇/类型提示/type_hints_demo/tests/test_generics.py`

- [ ] **Step 1: 编写泛型函数测试**

```python
"""泛型测试"""

from app.core.generics import first, reverse, get_middle


def test_first():
    assert first([1, 2, 3]) == 1
    assert first(["a", "b", "c"]) == "a"


def test_reverse():
    assert reverse([1, 2, 3]) == [3, 2, 1]
    assert reverse(["a", "b"]) == ["b", "a"]


def test_get_middle():
    assert get_middle([1, 2, 3]) == 2
    assert get_middle(["a", "b", "c"]) == "b"
```

- [ ] **Step 2: 编写泛型约束测试**

```python
from app.core.generics import double, add_numbers


def test_double():
    assert double(5) == 10
    assert double(5.0) == 10.0


def test_add_numbers():
    assert add_numbers(1, 2) == 3
    assert add_numbers(1.5, 2.5) == 4.0
```

- [ ] **Step 3: 编写 Stack 测试**

```python
from app.core.generics import Stack


def test_stack():
    stack: Stack[int] = Stack()
    stack.push(1)
    stack.push(2)
    stack.push(3)
    
    assert stack.pop() == 3
    assert stack.peek() == 2
    assert not stack.is_empty()
```

- [ ] **Step 4: 编写 Repository 测试**

```python
from app.core.generics import Repository, Entity


def test_repository():
    repo: Repository[Entity] = Repository()
    
    entity = Entity(id=1)
    index = repo.add(entity)
    
    assert index == 0
    assert repo.get(0) == entity
    assert len(repo.get_all()) == 1
```

- [ ] **Step 5: 运行测试验证**

```bash
cd 02-核心编程篇/类型提示/type_hints_demo && uv run pytest tests/test_generics.py -v
```

- [ ] **Step 6: 提交测试**

```bash
git add 02-核心编程篇/类型提示/type_hints_demo/tests/test_generics.py
git commit -m "Add generics module tests"
```

---

## Task 11: 创建 test_protocols.py 测试

**Files:**
- Create: `02-核心编程篇/类型提示/type_hints_demo/tests/test_protocols.py`

- [ ] **Step 1: 编写协议测试**

```python
"""协议测试"""

from app.core.protocols import Drawable, Circle, Square, render


def test_render():
    circle = Circle()
    square = Square()
    
    render(circle)
    render(square)
```

- [ ] **Step 2: 编写 Comparable 测试**

```python
from app.core.protocols import Person


def test_person_compare():
    p1 = Person("张三", 25)
    p2 = Person("李四", 18)
    
    assert p1.compare_to(p2) > 0
    assert p2.compare_to(p1) < 0
```

- [ ] **Step 3: 编写 Serializable 测试**

```python
from app.core.protocols import Serializable, User


def test_serializable():
    user = User("张三", 25)
    
    assert isinstance(user, Serializable)
    json_str = user.to_json()
    assert "张三" in json_str
```

- [ ] **Step 4: 编写 TypedDict 测试**

```python
from app.core.protocols import UserDict, create_user


def test_user_dict():
    user_data: UserDict = {
        "id": 1,
        "name": "张三",
        "email": "test@example.com",
        "age": None
    }
    
    result = create_user(user_data)
    assert result["id"] == 1
```

- [ ] **Step 5: 运行测试验证**

```bash
cd 02-核心编程篇/类型提示/type_hints_demo && uv run pytest tests/test_protocols.py -v
```

- [ ] **Step 6: 提交测试**

```bash
git add 02-核心编程篇/类型提示/type_hints_demo/tests/test_protocols.py
git commit -m "Add protocols module tests"
```

---

## Task 12: 创建 test_advanced.py 测试

**Files:**
- Create: `02-核心编程篇/类型提示/type_hints_demo/tests/test_advanced.py`

- [ ] **Step 1: 编写 ParamSpec 测试**

```python
"""高级特性测试"""

from app.core.advanced import log_call


def test_log_call():
    @log_call
    def add(a: int, b: int) -> int:
        return a + b
    
    result = add(1, 2)
    assert result == 3
```

- [ ] **Step 2: 编写 Final/ClassVar 测试**

```python
from app.core.advanced import Config, BaseService


def test_config():
    config = Config(9000)
    assert config.port == 9000
    assert Config.MAX_SIZE == 100


def test_base_service():
    service = BaseService()
    assert service.get_version() == "1.0.0"
```

- [ ] **Step 3: 编写 TypeGuard 测试**

```python
from app.core.advanced import is_string_list, process_data


def test_is_string_list():
    assert is_string_list(["a", "b", "c"]) == True
    assert is_string_list([1, "b", 3]) == False


def test_process_data():
    assert process_data(["a", "b", "c"]) == "a b c"
    assert process_data([1, 2, 3]) == "非字符串列表"
```

- [ ] **Step 4: 运行测试验证**

```bash
cd 02-核心编程篇/类型提示/type_hints_demo && uv run pytest tests/test_advanced.py -v
```

- [ ] **Step 5: 提交测试**

```bash
git add 02-核心编程篇/类型提示/type_hints_demo/tests/test_advanced.py
git commit -m "Add advanced features module tests"
```

---

## Task 13: 更新 app/core/__init__.py

**Files:**
- Modify: `02-核心编程篇/类型提示/type_hints_demo/app/core/__init__.py`

- [ ] **Step 1: 更新导入**

```python
"""核心模块"""

from app.core.basics import (
    count_words,
    find_user,
    parse_value,
    apply_operation,
)
from app.core.generics import (
    first,
    reverse,
    Stack,
    Repository,
)
from app.core.protocols import (
    Drawable,
    Circle,
    Square,
    UserDict,
)
from app.core.advanced import (
    log_call,
    Config,
    is_string_list,
)

__all__ = [
    "count_words",
    "find_user",
    "parse_value",
    "apply_operation",
    "first",
    "reverse",
    "Stack",
    "Repository",
    "Drawable",
    "Circle",
    "Square",
    "UserDict",
    "log_call",
    "Config",
    "is_string_list",
]
```

- [ ] **Step 2: 提交修改**

```bash
git add 02-核心编程篇/类型提示/type_hints_demo/app/core/__init__.py
git commit -m "Update core module imports"
```

---

## Task 14: 删除旧文件

**Files:**
- Delete: `02-核心编程篇/类型提示/type_hints_demo/app/core/type_hints.py`
- Delete: `02-核心编程篇/类型提示/type_hints_demo/tests/test_type_hints.py`

- [ ] **Step 1: 删除旧文件**

```bash
rm 02-核心编程篇/类型提示/type_hints_demo/app/core/type_hints.py
rm 02-核心编程篇/类型提示/type_hints_demo/tests/test_type_hints.py
```

- [ ] **Step 2: 提交删除**

```bash
git add -A 02-核心编程篇/类型提示/type_hints_demo/
git commit -m "Remove old type_hints files after refactoring"
```

---

## Task 15: 更新项目 README.md

**Files:**
- Modify: `02-核心编程篇/类型提示/type_hints_demo/README.md`

- [ ] **Step 1: 编写详细使用文档**

```markdown
# 类型提示示例项目

本项目包含 Python 类型提示的实用示例，覆盖基础到高级特性。

## 项目结构

```
app/
├── core/
│   ├── basics.py      # 容器类型、Optional/Union、Callable 示例
│   ├── generics.py    # 泛型函数、Stack、Repository 示例
│   ├── protocols.py   # Protocol、TypedDict 示例
│   └── advanced.py    # ParamSpec、Final、TypeGuard 示例
│   └── utils/
│       └── helpers.py # 辅助函数
tests/
├── test_basics.py     # basics 模块测试
├── test_generics.py   # generics 模块测试
├── test_protocols.py  # protocols 模块测试
├── test_advanced.py   # advanced 模块测试
```

## 运行测试

```bash
# 运行所有测试
uv run pytest -v

# 运行特定模块测试
uv run pytest tests/test_basics.py -v
uv run pytest tests/test_generics.py -v
```

## 类型检查（可选）

```bash
uv run mypy app/
```

## 学习建议

1. 先阅读对应章节文档（01-基础、02-进阶、03-高级）
2. 查看示例代码理解语法
3. 运行测试验证行为
4. 修改代码尝试变体

## 示例对照

| 文档章节 | 示例模块 | 测试文件 |
|---------|---------|---------|
| 容器类型、Optional、Callable | basics.py | test_basics.py |
| 泛型深入 | generics.py | test_generics.py |
| 协议、TypedDict | protocols.py | test_protocols.py |
| ParamSpec、Final、TypeGuard | advanced.py | test_advanced.py |
```

- [ ] **Step 2: 提交修改**

```bash
git add 02-核心编程篇/类型提示/type_hints_demo/README.md
git commit -m "Update demo project README with detailed guide"
```

---

## Task 16: 更新 pyproject.toml

**Files:**
- Modify: `02-核心编程篇/类型提示/type_hints_demo/pyproject.toml`

- [ ] **Step 1: 更新 Python 版本要求**

```toml
[project]
name = "type-hints-demo"
version = "0.2.0"
description = "Python 类型提示示例项目"
requires-python = ">=3.11"
```

- [ ] **Step 2: 添加 mypy 依赖**

```toml
[dependency-groups]
dev = [
    "pytest>=9.0.2",
    "mypy>=1.0.0",
]
```

- [ ] **Step 3: 提交修改**

```bash
git add 02-核心编程篇/类型提示/type_hints_demo/pyproject.toml
git commit -m "Update pyproject.toml with Python 3.11+ and mypy"
```

---

## Task 17: 运行完整测试验证

**Files:**
- N/A

- [ ] **Step 1: 运行所有测试**

```bash
cd 02-核心编程篇/类型提示/type_hints_demo && uv run pytest -v
```

Expected: All tests pass

- [ ] **Step 2: 验证类型检查（可选）**

```bash
cd 02-核心编程篇/类型提示/type_hints_demo && uv run mypy app/
```

Expected: No type errors

---

## Task 18: 最终提交和清理

**Files:**
- N/A

- [ ] **Step 1: 删除旧的 02-类型注解进阶.md**

```bash
rm 02-核心编程篇/类型提示/02-类型注解进阶.md
git add -A 02-核心编程篇/类型提示/
git commit -m "Remove old advanced types document after refactoring"
```

- [ ] **Step 2: 最终提交所有更改**

```bash
git status
git add docs/superpowers/plans/2026-04-06-type-hints-refactoring-plan.md
git commit -m "Complete type hints refactoring implementation plan"
```