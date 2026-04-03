# Python 3.11+ 迁移指南

本教程已全面升级到 Python 3.11+，本文档帮助你快速了解主要变化。

---

## 类型提示变化

### 旧语法（Python 3.9 之前）

```python
from typing import List, Dict, Optional, Union

def process(items: List[int]) -> Dict[str, int]:
    return {str(i): i for i in items}

def find(id: int) -> Optional[User]:
    return users.get(id)

def parse(value: Union[str, int]) -> str:
    return str(value)
```

### 新语法（Python 3.11+）

```python
# 无需导入 typing 模块的基础类型

def process(items: list[int]) -> dict[str, int]:
    return {str(i): i for i in items}

def find(id: int) -> User | None:
    return users.get(id)

def parse(value: str | int) -> str:
    return str(value)
```

**主要变化：**
- `List[X]` → `list[X]`
- `Dict[K, V]` → `dict[K, V]`
- `Optional[X]` → `X | None`
- `Union[X, Y]` → `X | Y`
- `Tuple[X, Y]` → `tuple[X, Y]`

---

## 包管理变化

### 旧方式（pip）

```bash
# 创建虚拟环境
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# 或
.\.venv\Scripts\activate  # Windows

# 安装依赖
pip install requests
pip freeze > requirements.txt

# 运行脚本
python main.py
```

### 新方式（uv）

```bash
# 创建项目（自动创建虚拟环境）
uv init my-project
cd my-project

# 添加依赖
uv add requests

# 运行脚本
uv run python main.py
```

**uv 的优势：**
- ⚡ 速度快 10-100 倍
- 🔒 自动锁定依赖（uv.lock）
- 🐍 内置 Python 版本管理
- 📦 统一工具链

---

## match 语句（Python 3.10+）

新的模式匹配语法：

```python
def http_status(status: int) -> str:
    match status:
        case 200:
            return "OK"
        case 404:
            return "Not Found"
        case 500:
            return "Internal Server Error"
        case _:
            return "Unknown"
```

**匹配模式：**

```python
# 匹配字面值
match value:
    case 0:
        print("零")
    case 1 | 2 | 3:  # 或模式
        print("小数字")

# 匹配结构
match point:
    case (0, 0):
        print("原点")
    case (x, 0):
        print(f"在x轴上，x={x}")
    case (x, y):
        print(f"点({x}, {y})")

# 匹配对象
match user:
    case User(name="张三", age=age):
        print(f"张三，{age}岁")
    case User(name=name, age=age) if age >= 18:
        print(f"{name}已成年")
```

---

## 异步改进

### 旧方式

```python
import asyncio

async def main():
    results = await asyncio.gather(
        task1(),
        task2(),
        task3()
    )
    return results

asyncio.run(main())
```

### 新方式（Python 3.11+ TaskGroup）

```python
import asyncio

async def main():
    async with asyncio.TaskGroup() as tg:
        tg.create_task(task1())
        tg.create_task(task2())
        tg.create_task(task3())
    # 所有任务完成后继续

asyncio.run(main())
```

**TaskGroup 的优势：**
- 更好的异常处理
- 自动等待所有任务
- 更清晰的代码结构

---

## 错误提示改进

Python 3.11+ 提供了更精确的错误提示：

```python
# 代码
x = {
    "name": "张三"
    "age": 25  # 缺少逗号
}

# Python 3.10 错误提示
SyntaxError: invalid syntax

# Python 3.11+ 错误提示
SyntaxError: '{' was never closed
  
Possible causes:
- Missing closing brace '}' 
- forgot to add comma after previous item
```

---

## 性能提升

Python 3.11 比 Python 3.10 快 10-60%（根据不同场景）：

| 场景 | 性能提升 |
|------|---------|
| 启动速度 | 10-15% |
| 运行速度 | 10-25% |
| 内存占用 | 降低 10-15% |

---

## 推荐升级步骤

### 1. 安装 Python 3.11+

```bash
# 使用 uv 安装
uv python install 3.11

# 或使用官方安装包
# https://www.python.org/downloads/
```

### 2. 更新代码中的类型提示

```python
# 批量替换（使用编辑器）
List[  →  list[
Dict[  →  dict[
Optional[  →  | None
Union[  →  （改用 |）
```

### 3. 使用 match 语句

- 替代复杂的 `if-elif-else` 链
- 用于结构化数据匹配

### 4. 使用 asyncio.TaskGroup

- 替代 `asyncio.gather()`
- 更好的异常处理

### 5. 使用 uv 管理项目

```bash
# 初始化新项目
uv init my-project

# 迁移老项目
cd existing-project
uv init
uv add $(cat requirements.txt | tr '\n' ' ')
```

---

## 兼容性检查

如果你的项目需要支持 Python 3.10 及以下版本：

```python
from __future__ import annotations

# 这样可以使用新语法，但仍兼容旧版本
def process(items: list[int]) -> dict[str, int]:
    ...
```

但本教程**不再支持旧版本**，直接使用 Python 3.11+ 语法。

---

## 常见问题

### Q: 必须升级到 Python 3.11 吗？
**A:** 是的。本教程使用 Python 3.11+ 特性，旧版本可能无法运行部分代码。

### Q: uv 完全替代 pip 吗？
**A:** uv 可以完全替代 pip、venv、pip-tools 等工具。但 pip 在老项目中仍然可用。

### Q: 如何处理类型提示兼容性？
**A:** 使用 `from __future__ import annotations` 可以在新旧版本间兼容。

### Q: TaskGroup 必须用吗？
**A:** 不必须，但推荐。`asyncio.gather()` 仍然可用。

---

## 参考资源

- [Python 3.11 官方文档](https://docs.python.org/3.11/whatsnew/3.11.html)
- [PEP 604 – Allow writing union types as X | Y](https://peps.python.org/pep-0604/)
- [PEP 634 – Structural Pattern Matching](https://peps.python.org/pep-0634/)
- [uv 官方文档](https://docs.astral.sh/uv/)

---

## 下一步

1. 安装 Python 3.11+
2. 安装 uv 包管理器
3. 开始学习教程：[00-Python学习大纲.md](./00-Python学习大纲.md)