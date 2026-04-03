# 类型提示

本章讲解 Python 类型提示的完整知识体系，从基础类型注解到高级类型特性。

---

## 章节导航

| 章节 | 文件 | 主题 |
|------|------|------|
| 01 | [01-类型提示基础.md](./01-类型提示基础.md) | 基础类型、容器类型、Optional、Union、Callable、泛型 |
| 02 | [02-类型注解进阶.md](./02-类型注解进阶.md) | 运行时检查、泛型类、协议进阶、TypedDict、类型守卫 |

---

## 核心知识点

### 基础类型注解

```python
# 变量类型
name: str = "张三"
age: int = 25
scores: list[float] = [85.5, 90.0]

# 函数类型
def greet(name: str) -> str:
    return f"Hello, {name}"
```

### 常用类型

| 类型 | 说明 | 示例 |
|------|------|------|
| `int`, `str`, `float`, `bool` | 基础类型 | `x: int = 10` |
| `list[T]` | 列表 | `nums: list[int]` |
| `dict[K, V]` | 字典 | `info: dict[str, int]` |
| `Optional[T]` | 可选（T或None） | `name: Optional[str]` |
| `Union[A, B]` | 联合类型 | `value: int | str` |
| `Callable[[A], B]` | 函数类型 | `func: Callable[[int], str]` |

### 泛型

```python
from typing import TypeVar, Generic

T = TypeVar('T')

class Box(Generic[T]):
    def __init__(self, item: T):
        self._item = item
    
    def get(self) -> T:
        return self._item
```

### 协议

```python
from typing import Protocol

class Drawable(Protocol):
    def draw(self) -> None: ...

# 任何有 draw 方法的类都符合
class Circle:
    def draw(self) -> None:
        print("画圆")
```

---

## 示例项目

本项目包含类型提示的实用示例，位于 `type_hints_demo/` 目录。

运行测试：

```bash
cd type_hints_demo
uv run pytest
```