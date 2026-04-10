# Python 代码规范完整指南

> **摘要**：本文档是 Python 代码编写规范的完整指南，涵盖命名、布局、类型提示、文档、函数设计、错误处理等核心规范，帮助团队写出高质量、可维护的代码。

---

## 1. PEP 8 核心规范

PEP 8 是 Python 官方代码风格指南。以下是最核心的规则。

### 1.1 代码布局

| 规则 | 规范 | 错误示例 | 正确示例 |
|------|------|---------|---------|
| **缩进** | 4 个空格（禁止 Tab） | `if x:` + Tab | `if x:` + 4空格 |
| **行长度** | 最大 88 字符 (Ruff 默认) 或 79 (PEP 8) | 超长一行 | 使用括号换行 |
| **空行** | 顶层函数/类之间空 2 行 | 连续写函数 | 函数间空 2 行 |
| **导入** | 分组导入，组间空 1 行 | 混在一起 | 标准库→第三方→本地 |

```python
# ✅ 正确：行过长时使用括号换行
result = some_long_function(
    arg1=value1,
    arg2=value2,
    arg3=value3,
)

# ❌ 错误：使用反斜杠换行（不推荐）
result = some_long_function(arg1=value1, \
    arg2=value2)

# ✅ 正确：导入分组
import os
import sys
from pathlib import Path

import requests
from fastapi import FastAPI

from app.core import config
from app.services import user_service
```

### 1.2 命名规范速查表

| 类型 | 规范 | 示例 | 说明 |
|------|------|------|------|
| **变量/函数** | `snake_case` | `user_name`, `get_data()` | 全小写，单词间用下划线 |
| **类名** | `PascalCase` | `UserProfile`, `HTTPClient` | 每个单词首字母大写 |
| **常量** | `UPPER_SNAKE_CASE` | `MAX_SIZE`, `DEFAULT_TIMEOUT` | 全大写 |
| **私有属性** | `_leading_underscore` | `_cache`, `_internal_data` | 单下划线开头，表示内部使用 |
| **强私有** | `__double_underscore` | `__private_method` | 双下划线（触发名称改写） |
| **魔法方法** | `__dunder__` | `__init__`, `__str__` | 双下划线前后包围 |
| **模块名** | `snake_case` | `user_service.py` | 全小写，可含下划线 |
| **包名** | `snake_case` | `my_package` | 全小写，尽量不含下划线 |

```python
# ✅ 正确命名
class UserAccount:          # 类名：PascalCase
    MAX_LOGIN_ATTEMPTS = 3  # 常量：UPPER_SNAKE_CASE
    
    def __init__(self):
        self.user_name = ""     # 公开属性：snake_case
        self._cache = {}        # 私有属性：_prefix
        self.__secret = None    # 强私有：__prefix
    
    def get_full_name(self):    # 方法：snake_case
        pass

# ❌ 错误命名
class userAccount:           # 类名应用 PascalCase
    maxLoginAttempts = 3     # 常量应全大写
    
    def GetFullName(self):   # 方法应全小写
        pass
```

### 1.3 空格使用规则

```python
# ✅ 运算符两侧各一个空格
x = 5
y = x + 10
is_valid = x > 0 and y < 100

# ✅ 逗号后一个空格
numbers = [1, 2, 3, 4]
config = {"name": "Alice", "age": 25}

# ✅ 函数参数冒号后无空格，默认值前有空格
def greet(name: str, age: int = 18) -> str:
    pass

# ❌ 错误：冒号后有空格
def greet(name: str, age: int= 18) -> str:  # 错误

# ✅ 列表索引、切片不加空格
items[0]
items[1:5]
items[::2]

# ❌ 错误：加了空格
items[ 0 ]
items[ 1 : 5 ]
```

---

## 2. 函数设计规范

### 2.1 函数长度原则

*   **理想长度**：不超过 20 行。
*   **最大长度**：不超过 50 行（超过则考虑拆分）。
*   **单一职责**：一个函数只做一件事。

```python
# ❌ 错误：函数过长、职责过多
def process_user(user_id):
    # 验证用户
    user = get_user(user_id)
    if not user:
        return None
    
    # 计算分数
    score = 0
    for activity in user.activities:
        score += activity.points
    
    # 发送通知
    send_email(user.email, "您的分数更新了")
    
    # 更新数据库
    update_user_score(user_id, score)
    
    # 记录日志
    log_activity(user_id, "score_updated")
    
    return score

# ✅ 正确：拆分为多个小函数
def process_user(user_id: int) -> int | None:
    user = validate_and_get_user(user_id)
    if not user:
        return None
    
    score = calculate_score(user.activities)
    notify_user(user, score)
    update_score(user_id, score)
    
    return score

def validate_and_get_user(user_id: int) -> User | None:
    """获取并验证用户"""
    return get_user(user_id)

def calculate_score(activities: list[Activity]) -> int:
    """计算用户分数"""
    return sum(a.points for a in activities)

def notify_user(user: User, score: int) -> None:
    """发送分数更新通知"""
    send_email(user.email, f"您的分数: {score}")
```

### 2.2 参数设计原则

| 原则 | 说明 |
|------|------|
| **参数数量** | 建议 ≤ 5 个，超过则用对象封装 |
| **避免布尔参数** | `func(True)` 不可读，用枚举或拆分函数 |
| **必填在前，可选在后** | 位置参数在前，默认参数在后 |
| **避免可变默认值** | `def f(x=[])` 是陷阱 |

```python
# ❌ 错误：布尔参数不可读
def send_email(recipient, urgent):
    pass

send_email("user@example.com", True)  # True 是什么意思？

# ✅ 正确：使用枚举
from enum import Enum

class Priority(Enum):
    NORMAL = "normal"
    URGENT = "urgent"

def send_email(recipient: str, priority: Priority = Priority.NORMAL):
    pass

send_email("user@example.com", Priority.URGENT)  # 可读！

# ❌ 错误：可变默认值陷阱
def add_item(item, items=[]):  # 列表是可变的！
    items.append(item)
    return items

# 调用两次会累积数据
add_item("a")  # ["a"]
add_item("b")  # ["a", "b"]  ← 意料之外的累积！

# ✅ 正确：使用 None 作为默认值
def add_item(item: str, items: list[str] | None = None) -> list[str]:
    if items is None:
        items = []
    items.append(item)
    return items
```

---

## 3. 类设计规范

### 3.1 类的组织结构

```python
class UserService:
    """用户服务类"""
    
    # 1. 类常量（在最前面）
    MAX_RETRIES = 3
    DEFAULT_TIMEOUT = 30
    
    # 2. 实例属性（__init__）
    def __init__(self, config: Config) -> None:
        self._config = config
        self._cache: dict[int, User] = {}
    
    # 3. 公共方法
    def get_user(self, user_id: int) -> User | None:
        return self._cache.get(user_id)
    
    def create_user(self, name: str) -> User:
        user = User(name=name)
        self._cache[user.id] = user
        return user
    
    # 4. 私有方法（最后）
    def _validate_user(self, user: User) -> bool:
        return bool(user.name)
    
    # 5. 魔法方法（如果需要）
    def __repr__(self) -> str:
        return f"UserService(config={self._config})"
```

### 3.2 使用 dataclass 简化

Python 3.7+ 推荐 `dataclasses`，自动生成 `__init__`, `__repr__`, `__eq__`。

```python
from dataclasses import dataclass, field

# ✅ 推荐：简单数据类用 dataclass
@dataclass
class User:
    id: int
    name: str
    email: str
    is_active: bool = True
    tags: list[str] = field(default_factory=list)

# 使用
user = User(id=1, name="Alice", email="alice@example.com")
print(user)  # User(id=1, name='Alice', email='alice@example.com', is_active=True, tags=[])
```

---

## 4. 注释规范

### 4.1 注释原则

*   **代码应自解释**：好的命名比注释更重要。
*   **解释为什么，不是做什么**：代码本身展示了做什么。
*   **保持同步**：修改代码时同步更新注释。

```python
# ❌ 错误：解释做什么（代码已经展示了）
# 遍历列表中的每个元素
for item in items:
    process(item)

# ✅ 正确：解释为什么
# 使用二分查找而非线性搜索，因为列表已排序且数据量大
index = bisect.bisect_left(sorted_items, target)

# ✅ 正确：TODO/FIXME 标记
# TODO: 优化算法，当前 O(n²) 复杂度过高
# FIXME: 在 Windows 上存在路径问题
```

### 4.2 文档字符串 (Docstrings)

使用 **Google 风格**（清晰易读）：

```python
def calculate_average(
    numbers: list[float],
    exclude_zeros: bool = False
) -> float | None:
    """计算数值列表的平均值。

    使用加权平均算法，支持排除零值选项。
    注意：空列表返回 None 而非抛出异常。

    Args:
        numbers: 数值列表，不能为空列表时返回 None。
        exclude_zeros: 是否排除零值，默认 False。

    Returns:
        平均值，空列表时返回 None。

    Raises:
        TypeError: 如果 numbers 不是列表类型。

    Example:
        >>> calculate_average([1, 2, 3])
        2.0
        >>> calculate_average([1, 0, 3], exclude_zeros=True)
        2.0
    """
    if not numbers:
        return None
    
    filtered = [n for n in numbers if not exclude_zeros or n != 0]
    return sum(filtered) / len(filtered) if filtered else None
```

---

## 5. 错误处理规范

### 5.1 异常处理原则

| 原则 | 说明 |
|------|------|
| **具体异常** | 捕获具体异常，而非裸 `except:` |
| **不要吞掉异常** | 必须处理或重新抛出 |
| **早失败** | 参数验证放在函数开头 |
| **提供上下文** | 异常消息包含调试信息 |

```python
# ❌ 错误：裸 except 会吞掉所有异常（包括 KeyboardInterrupt）
try:
    do_something()
except:  # 捕获所有异常，包括系统异常
    pass

# ❌ 错误：吞掉异常不处理
try:
    result = risky_operation()
except ValueError:
    pass  # 静默忽略，问题被隐藏

# ✅ 正确：捕获具体异常并处理
try:
    result = risky_operation()
except ValueError as e:
    logger.error(f"操作失败: {e}")
    raise  #重新抛出，让上层处理

# ✅ 正确：早失败（参数验证在前）
def divide(a: float, b: float) -> float:
    if b == 0:
        raise ValueError("除数不能为零")  # 早失败
    return a / b
```

### 5.2 HTTP API 错误处理

```python
from fastapi import HTTPException

@router.get("/users/{user_id}")
def get_user(user_id: int) -> UserResponse:
    user = user_service.get(user_id)
    
    # ✅ 正确：使用适当的 HTTP 状态码
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    if not user.is_active:
        raise HTTPException(status_code=403, detail="用户已被禁用")
    
    return user
```

---

## 6. 类型提示规范

### 6.1 基本类型

```python
# Python 3.9+：使用内置类型
def process(items: list[str]) -> dict[str, int]:
    return {item: len(item) for item in items}

# Python 3.10+：使用 | 语法
def find(id: int) -> User | None:
    return database.get(id)

# Python 3.11+：Self 类型
from typing import Self

class Builder:
    def set_name(self, name: str) -> Self:
        self.name = name
        return self
```

### 6.2 复杂类型

```python
from typing import Callable, TypeVar, Generic, Protocol

# Callable：函数类型
def apply(func: Callable[[int], str], value: int) -> str:
    return func(value)

# TypeVar：泛型
T = TypeVar("T")

class Stack(Generic[T]):
    def __init__(self) -> None:
        self._items: list[T] = []
    
    def push(self, item: T) -> None:
        self._items.append(item)

# Protocol：结构化类型（鸭子类型）
class SupportsRead(Protocol):
    def read(self) -> str: ...

def read_data(source: SupportsRead) -> str:
    return source.read()
```

---

## 7. 安全编码规范

### 7.1 输入验证

```python
# ❌ 危险：直接使用用户输入
user_input = request.form["path"]
file_path = f"/data/{user_input}"  # 路径注入风险！

# ✅ 安全：验证和清理输入
from pathlib import Path

def safe_path(base_dir: Path, user_input: str) -> Path:
    """安全拼接路径，防止路径遍历攻击"""
    base_dir = base_dir.resolve()
    target = (base_dir / user_input).resolve()
    
    if not str(target).startswith(str(base_dir)):
        raise ValueError("非法路径")
    
    return target
```

### 7.2 密码和敏感信息

```python
# ❌ 危险：硬编码密码
DATABASE_URL = "postgresql://admin:password123@localhost/db"

# ✅ 安全：使用环境变量
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# ✅ 安全：不在日志中打印敏感信息
logger.info(f"用户登录: {user.email}")  # OK
logger.debug(f"密码: {password}")       # ❌ 绝对禁止
```

---

## 8. 工具配置

### 8.1 Ruff 配置 (pyproject.toml)

```toml
[tool.ruff]
line-length = 88
target-version = "py311"

[tool.ruff.lint]
select = [
    "E",   # pycodestyle errors
    "W",   # pycodestyle warnings
    "F",   # pyflakes
    "I",   # isort
    "B",   # flake8-bugbear
    "C4",  # flake8-comprehensions
    "UP",  # pyupgrade
    "ARG", # flake8-unused-arguments
]
ignore = [
    "E501",  # line too long（交给 formatter 处理）
]

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
```

### 8.2 pre-commit 配置

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.3.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
  
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
        args: ['--maxkb=500']
```

---

## 9. 反模式清单

| 反模式 | 问题 | 正确做法 |
|--------|------|---------|
| 裸 `except:` | 吞掉所有异常 | 捕获具体异常 |
| `import *` | 污染命名空间 | 显式导入 |
| 可变默认参数 | 数据累积 | 用 `None` |
| 全局变量 | 隐式依赖 | 用类/函数封装 |
| 过深嵌套 | 可读性差 | 提前返回 |
| 神类 | 职责不清 | 拆分职责 |

```python
# ❌ 反模式：过深嵌套
def process(data):
    if data:
        if data.valid:
            if data.ready:
                if data.has_permission:
                    return do_work(data)
    return None

# ✅ 正确：提前返回（guard clauses）
def process(data):
    if not data:
        return None
    if not data.valid:
        return None
    if not data.ready:
        return None
    if not data.has_permission:
        return None
    
    return do_work(data)
```

---

## 本章小结

```
┌─────────────────────────────────────────────────────────────┐
│                 Python 代码规范核心要点                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  命名规范：                                                   │
│  ✓ 变量/函数：snake_case                                     │
│  ✓ 类名：PascalCase                                         │
│  ✓ 常量：UPPER_SNAKE_CASE                                   │
│                                                             │
│  函数设计：                                                   │
│  ✓ 单一职责，长度 ≤ 50 行                                    │
│  ✓ 参数 ≤ 5 个，避免布尔参数                                 │
│  ✓ 默认值用 None，不用可变对象                               │
│                                                             │
│  类型提示：                                                   │
│  ✓ 所有函数签名添加类型                                      │
│  ✓ Python 3.10+ 使用 | 语法                                  │
│                                                             │
│  错误处理：                                                   │
│  ✓ 捕获具体异常，不吞异常                                    │
│  ✓ 早失败：参数验证在前                                      │
│                                                             │
│  工具链：                                                     │
│  ✓ Ruff 检查 + 格式化                                       │
│  ✓ pre-commit 自动化                                        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```