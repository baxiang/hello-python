# 类型提示

Python 类型提示示例项目，覆盖第 01-03 章（基础类型 → 泛型/Protocol/TypedDict → ParamSpec/TypeGuard/Final/ClassVar）。

## 场景

数据处理系统：通过用户查询、泛型容器、协议模式、类型守卫等，演示 Python 类型系统的完整用法。

## 项目结构

```
type_hints_demo/
├── pyproject.toml
├── app/
│   ├── __init__.py
│   ├── core/
│   │   ├── basics.py      # ch01: 容器类型、Optional/Union、Callable、类型别名
│   │   ├── generics.py    # ch02: TypeVar、泛型函数/类、Protocol、TypedDict
│   │   ├── protocols.py   # ch02: Protocol、TypedDict、runtime_checkable
│   │   └── advanced.py    # ch03: ParamSpec、Concatenate、Final、ClassVar、TypeGuard
│   └── utils/
│       └── helpers.py     # ch02: 泛型工具函数（first/reverse/safe_get）
└── tests/
    └── test_basics.py     # 29 个测试
```

## 安装

```bash
uv sync
```

## 使用示例

```python
from app.core.basics import parse_value, apply_operation, find_user
from app.core.generics import Stack, Repository, first, get_middle
from app.core.protocols import Drawable, render, Person, find_max
from app.core.advanced import log_call, is_string_list, Config, BaseService

# ch01: 基础类型
parse_value("42")       # → 42 (int)
parse_value("3.14")     # → 3.14 (float)
parse_value("true")     # → True (bool)
parse_value("hello")    # → "hello" (str)

# ch02: 泛型
stack = Stack[int]()
stack.push(1); stack.push(2)
stack.pop()  # → 2

repo = Repository([{"id": 1}, {"id": 2}])
repo.get(0)

# ch02: Protocol
from app.core.protocols import Circle
render(Circle())  # 鸭子类型：无需继承

# ch03: TypeGuard
items: list[object] = ["a", "b"]
if is_string_list(items):
    " ".join(items)  # mypy 知道 items 是 list[str]
```

## 运行测试

```bash
uv run pytest               # 全部测试
uv run mypy app/            # 类型检查（需安装 mypy）
```

## 章节映射

| 代码文件 | 对应章节 | 核心内容 |
|---------|---------|---------|
| `basics.py` | ch01 | 容器类型注解、Optional/Union、Callable、类型别名、回调模式 |
| `generics.py` | ch02 | TypeVar、泛型函数、泛型类(Generic)、约束泛型 |
| `protocols.py` | ch02 | Protocol、TypedDict、runtime_checkable、鸭子类型 |
| `advanced.py` | ch03 | ParamSpec、Concatenate、Final、ClassVar、TypeGuard |
| `helpers.py` | ch02 | 泛型工具函数（TypeVar 应用） |
