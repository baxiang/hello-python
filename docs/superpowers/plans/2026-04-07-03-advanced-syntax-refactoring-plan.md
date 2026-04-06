# 03-高级语法篇 重构实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 重构 03-高级语法篇为扁平化目录结构，应用 6 步渐进式教学法，使用 Python 3.11+ 现代语法。

**Architecture:** 三阶段重构：目录重组 → 文档内容重构 → README 更新。每个子目录独立重构，完成后提交。

**Tech Stack:** Python 3.11+, type hints, uv, pytest

---

## Task 1: 重命名目录结构

**Files:**
- Modify: `03-高级语法篇/` directory structure

- [ ] **Step 1: 重命名 模块与包 为 01-模块与包**

```bash
mv "03-高级语法篇/模块与包" "03-高级语法篇/01-模块与包"
```

- [ ] **Step 2: 重命名 标准库 为 02-标准库**

```bash
mv "03-高级语法篇/标准库" "03-高级语法篇/02-标准库"
```

- [ ] **Step 3: 重命名 并发与异步编程 为 03-并发与异步编程**

```bash
mv "03-高级语法篇/并发与异步编程" "03-高级语法篇/03-并发与异步编程"
```

- [ ] **Step 4: 移动 Python工具箱 文件到 02-标准库**

```bash
mv "03-高级语法篇/Python工具箱/12-文件操作.md" "03-高级语法篇/02-标准库/06-文件操作.md"
mv "03-高级语法篇/Python工具箱/17-正则表达式.md" "03-高级语法篇/02-标准库/07-正则表达式.md"
```

- [ ] **Step 5: 删除 Python工具箱 空目录**

```bash
rm -rf "03-高级语法篇/Python工具箱"
```

- [ ] **Step 6: 提交目录重构**

```bash
git add "03-高级语法篇/"
git commit -m "refactor: restructure 03-高级语法篇 directory with numbered prefixes"
```

---

## Task 2: 重构 01-模块与包 文档（01-模块基础）

**Files:**
- Modify: `03-高级语法篇/01-模块与包/01-模块基础.md`

- [ ] **Step 1: 添加版本说明和实际场景引入**

在文档开头添加：

```markdown
# 模块基础（详细版）

> Python 3.11+

## 第一部分：模块概念

### 1.1 什么是模块

#### 实际场景

你写了一个计算工具 `calculator.py`，里面有加法、减法等函数。现在你想在另一个项目 `invoice.py` 里使用这些函数，不想重复写代码。

**问题：如何让多个项目共享同一份代码？**
```

- [ ] **Step 2: 添加类型注解示例**

修改代码示例添加类型注解：

```python
from typing import Any

def add(a: float, b: float) -> float:
    """加法运算"""
    return a + b

def test() -> None:
    """测试函数"""
    assert add(1, 2) == 3
    assert add(-1, 1) == 0
    print("所有测试通过！")

if __name__ == '__main__':
    test()
```

- [ ] **Step 3: 删除文档末尾的导航链接**

删除类似以下内容：
```
---
[上一章](./00-目录.md) | [下一章](./02-自定义模块.md)
```

- [ ] **Step 4: 提交修改**

```bash
git add "03-高级语法篇/01-模块与包/01-模块基础.md"
git commit -m "refactor: improve 01-模块基础 with progressive teaching and type hints"
```

---

## Task 3: 重构 01-模块与包 文档（02-自定义模块）

**Files:**
- Modify: `03-高级语法篇/01-模块与包/02-自定义模块.md`

- [ ] **Step 1: 添加实际场景和版本说明**

```markdown
# 自定义模块（详细版）

> Python 3.11+

## 第一部分：创建模块

### 2.1 创建自己的模块

#### 实际场景

你在多个项目中都要处理用户数据：验证邮箱、格式化手机号、计算年龄。每次都复制粘贴代码很麻烦，而且容易出错。

**问题：如何把常用功能打包成模块，方便复用？**
```

- [ ] **Step 2: 添加带类型注解的示例代码**

```python
# user_utils.py
"""用户数据处理工具模块"""
from __future__ import annotations
from typing import Optional
import re
from datetime import datetime

def validate_email(email: str) -> bool:
    """验证邮箱格式
    
    Args:
        email: 邮箱地址
        
    Returns:
        True 如果格式正确，否则 False
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def format_phone(phone: str) -> str:
    """格式化手机号为标准格式
    
    Args:
        phone: 手机号码字符串
        
    Returns:
        格式化后的手机号，如 "138-1234-5678"
    """
    digits = ''.join(filter(str.isdigit, phone))
    if len(digits) == 11:
        return f"{digits[:3]}-{digits[3:7]}-{digits[7:]}"
    return phone

def calculate_age(birth_year: int) -> int:
    """根据出生年份计算年龄
    
    Args:
        birth_year: 出生年份
        
    Returns:
        当前年龄
    """
    current_year = datetime.now().year
    return current_year - birth_year

if __name__ == '__main__':
    # 测试代码
    print(validate_email("test@example.com"))  # True
    print(format_phone("13812345678"))         # 138-1234-5678
    print(calculate_age(1990))                 # 36 (2026年)
```

- [ ] **Step 3: 删除导航链接并提交**

```bash
git add "03-高级语法篇/01-模块与包/02-自定义模块.md"
git commit -m "refactor: improve 02-自定义模块 with progressive teaching and type hints"
```

---

## Task 4: 重构 01-模块与包 文档（03-包的结构）

**Files:**
- Modify: `03-高级语法篇/01-模块与包/03-包的结构.md`

- [ ] **Step 1: 添加实际场景引入**

```markdown
# 包的结构（详细版）

> Python 3.11+

## 第一部分：包的概念

### 3.1 什么是包

#### 实际场景

你的项目越来越大：
- `user_utils.py` - 用户相关（验证邮箱、格式化手机号）
- `order_utils.py` - 订单相关（计算价格、生成订单号）
- `payment_utils.py` - 支付相关（处理支付、退款）
- `file_utils.py` - 文件相关（读写文件、压缩解压）

20 多个模块文件堆在一起，乱成一团。你想把它们按功能分类整理。

**问题：如何用"文件夹"的方式组织多个模块？**
```

- [ ] **Step 2: 添加包结构示例**

```python
# myproject/__init__.py
"""MyProject 工具包"""
from __future__ import annotations

__version__ = "1.0.0"
__all__ = ["user", "order", "payment"]

# 导入子模块供外部使用
from myproject import user
from myproject import order
from myproject import payment
```

- [ ] **Step 3: 删除导航链接并提交**

```bash
git add "03-高级语法篇/01-模块与包/03-包的结构.md"
git commit -m "refactor: improve 03-包的结构 with progressive teaching"
```

---

## Task 5: 重构 01-模块与包 文档（04-导入机制）

**Files:**
- Modify: `03-高级语法篇/01-模块与包/04-导入机制.md`

- [ ] **Step 1: 添加实际场景**

```markdown
# 导入机制（详细版）

> Python 3.11+

## 第一部分：导入路径

### 4.1 绝对导入与相对导入

#### 实际场景

你的项目结构如下：
```
myproject/
├── __init__.py
├── core/
│   ├── __init__.py
│   ├── config.py
│   └── database.py
├── services/
│   ├── __init__.py
│   └── user_service.py
└── utils/
    ├── __init__.py
    └── helpers.py
```

在 `services/user_service.py` 里，你想导入 `core/config.py` 里的配置。应该怎么写导入语句？
```

- [ ] **Step 2: 添加类型注解示例**

```python
# myproject/core/config.py
from __future__ import annotations
from typing import Final
from pathlib import Path

class Config:
    """应用配置"""
    DEBUG: Final[bool] = True
    DATABASE_URL: Final[str] = "postgresql://localhost/mydb"
    BASE_DIR: Final[Path] = Path(__file__).parent.parent
    
    @classmethod
    def get_database_path(cls) -> Path:
        """获取数据库文件路径"""
        return cls.BASE_DIR / "data" / "app.db"
```

- [ ] **Step 3: 删除导航链接并提交**

```bash
git add "03-高级语法篇/01-模块与包/04-导入机制.md"
git commit -m "refactor: improve 04-导入机制 with progressive teaching and type hints"
```

---

## Task 6: 重构 01-模块与包 文档（05-pip包管理）

**Files:**
- Modify: `03-高级语法篇/01-模块与包/05-pip包管理.md`

- [ ] **Step 1: 添加实际场景**

```markdown
# pip 包管理（详细版）

> Python 3.11+

## 第一部分：pip 基础

### 5.1 什么是 pip

#### 实际场景

你想用 Python 做数据分析，听说有个叫 `pandas` 的库很好用。但你的 Python 里没有这个库，直接 `import pandas` 会报错 `ModuleNotFoundError`。

**问题：如何安装别人开发的 Python 库？**
```

- [ ] **Step 2: 添加 uv 安装命令（推荐）**

```bash
# 推荐使用 uv（更快）
uv add pandas numpy matplotlib

# 传统 pip 方式
pip install pandas numpy matplotlib

# 查看已安装的包
pip list

# 导出依赖列表
pip freeze > requirements.txt
```

- [ ] **Step 3: 删除导航链接并提交**

```bash
git add "03-高级语法篇/01-模块与包/05-pip包管理.md"
git commit -m "refactor: improve 05-pip包管理 with progressive teaching and uv"
```

---

## Task 7: 重构 01-模块与包 文档（06-发布自己的包）

**Files:**
- Modify: `03-高级语法篇/01-模块与包/06-发布自己的包.md`

- [ ] **Step 1: 添加实际场景**

```markdown
# 发布自己的包（详细版）

> Python 3.11+

## 第一部分：打包基础

### 6.1 为什么发布包

#### 实际场景

你写了一个很棒的工具库 `myutils`，里面有各种常用函数。你的同事也想用，但他们不想每次都复制你的代码文件。

**问题：如何让你的库像 pandas 一样，别人可以用 pip install 安装？**
```

- [ ] **Step 2: 添加 pyproject.toml 示例**

```toml
# pyproject.toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "myutils"
version = "0.1.0"
description = "A collection of useful Python utilities"
readme = "README.md"
requires-python = ">=3.11"
license = "MIT"
authors = [
    { name = "Your Name", email = "your@email.com" }
]

[project.optional-dependencies]
dev = ["pytest", "ruff"]
```

- [ ] **Step 3: 删除导航链接并提交**

```bash
git add "03-高级语法篇/01-模块与包/06-发布自己的包.md"
git commit -m "refactor: improve 06-发布自己的包 with progressive teaching"
```

---

## Task 8: 更新 01-模块与包 README

**Files:**
- Modify: `03-高级语法篇/01-模块与包/README.md`

- [ ] **Step 1: 创建新的 README**

```markdown
# 模块与包

学习 Python 模块和包的管理，掌握代码组织和复用的核心技能。

---

## 章节导航

| 章节 | 文件 | 主题 |
|------|------|------|
| 01 | [01-模块基础.md](./01-模块基础.md) | 模块概念、import 语法 |
| 02 | [02-自定义模块.md](./02-自定义模块.md) | 创建模块、搜索路径 |
| 03 | [03-包的结构.md](./03-包的结构.md) | 包结构、__init__.py |
| 04 | [04-导入机制.md](./04-导入机制.md) | 绝对/相对导入 |
| 05 | [05-pip包管理.md](./05-pip包管理.md) | pip、uv 命令 |
| 06 | [06-发布自己的包.md](./06-发布自己的包.md) | 打包、发布 PyPI |

---

## 示例项目

[modules_demo/](./modules_demo/) - 模块和包的实践示例
```

- [ ] **Step 2: 提交 README**

```bash
git add "03-高级语法篇/01-模块与包/README.md"
git commit -m "refactor: update 01-模块与包 README with new structure"
```

---

## Task 9: 重命名 02-标准库 文档文件

**Files:**
- Modify: `03-高级语法篇/02-标准库/` file names

- [ ] **Step 1: 重命名标准库文档文件**

```bash
mv "03-高级语法篇/02-标准库/math.md" "03-高级语法篇/02-标准库/01-math数学库.md"
mv "03-高级语法篇/02-标准库/random.md" "03-高级语法篇/02-标准库/02-random随机数.md"
mv "03-高级语法篇/02-标准库/datetime.md" "03-高级语法篇/02-标准库/03-datetime日期时间.md"
mv "03-高级语法篇/02-标准库/os-pathlib.md" "03-高级语法篇/02-标准库/04-os-pathlib路径操作.md"
mv "03-高级语法篇/02-标准库/json.md" "03-高级语法篇/02-标准库/05-json数据处理.md"
```

- [ ] **Step 2: 提交重命名**

```bash
git add "03-高级语法篇/02-标准库/"
git commit -m "refactor: rename 02-标准库 files with numbered prefixes"
```

---

## Task 10: 重构 02-标准库 文档（01-math数学库）

**Files:**
- Modify: `03-高级语法篇/02-标准库/01-math数学库.md`

- [ ] **Step 1: 添加实际场景引入**

```markdown
# math 数学库（详细版）

> Python 3.11+

## 第一部分：数学计算

### 1.1 常用数学函数

#### 实际场景

你要计算一个圆的面积和周长，半径是 5 米。公式是：
- 面积 = π × r²
- 周长 = 2 × π × r

如果不导入 math 库，你得自己定义 π = 3.14159...，而且精度不够。math 库提供了精确的数学常量和函数。

**问题：如何使用 Python 的数学计算功能？**
```

- [ ] **Step 2: 添加带类型注解的函数示例**

```python
from __future__ import annotations
import math
from typing import Final

PI: Final[float] = math.pi

def circle_area(radius: float) -> float:
    """计算圆的面积
    
    Args:
        radius: 圆的半径
        
    Returns:
        圆的面积
    """
    return PI * radius ** 2

def circle_circumference(radius: float) -> float:
    """计算圆的周长
    
    Args:
        radius: 圆的半径
        
    Returns:
        圆的周长
    """
    return 2 * PI * radius

def distance(x1: float, y1: float, x2: float, y2: float) -> float:
    """计算两点之间的距离
    
    Args:
        x1, y1: 第一个点的坐标
        x2, y2: 第二个点的坐标
        
    Returns:
        两点之间的欧几里得距离
    """
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

if __name__ == '__main__':
    area = circle_area(5.0)
    circ = circle_circumference(5.0)
    print(f"半径 5 米的圆：面积 {area:.2f} 平方米，周长 {circ:.2f} 米")
    
    dist = distance(0, 0, 3, 4)
    print(f"(0,0) 到 (3,4) 的距离: {dist}")
```

- [ ] **Step 3: 删除导航链接并提交**

```bash
git add "03-高级语法篇/02-标准库/01-math数学库.md"
git commit -m "refactor: improve 01-math数学库 with progressive teaching and type hints"
```

---

## Task 11: 重构 02-标准库 文档（02-random随机数）

**Files:**
- Modify: `03-高级语法篇/02-标准库/02-random随机数.md`

- [ ] **Step 1: 添加实际场景**

```markdown
# random 随机数（详细版）

> Python 3.11+

## 第一部分：随机数基础

### 2.1 生成随机数

#### 实际场景

你正在开发一个抽奖程序，需要随机选择 3 名幸运用户。或者你在做数据模拟，需要生成随机测试数据。

**问题：如何用 Python 生成随机数字、随机选择元素？**
```

- [ ] **Step 2: 添加带类型注解的示例**

```python
from __future__ import annotations
import random
from typing import Sequence, TypeVar

T = TypeVar('T')

def random_choice(items: Sequence[T]) -> T:
    """随机选择一个元素
    
    Args:
        items: 元素序列
        
    Returns:
        随机选择的元素
    """
    return random.choice(items)

def random_sample(items: Sequence[T], k: int) -> list[T]:
    """随机选择多个不重复元素
    
    Args:
        items: 元素序列
        k: 选择数量
        
    Returns:
        随机选择的元素列表
    """
    return random.sample(items, k)

def generate_random_int(min_val: int, max_val: int) -> int:
    """生成指定范围的随机整数
    
    Args:
        min_val: 最小值
        max_val: 最大值
        
    Returns:
        随机整数 [min_val, max_val]
    """
    return random.randint(min_val, max_val)

if __name__ == '__main__':
    users = ["Alice", "Bob", "Charlie", "David", "Eve"]
    
    # 抽奖：随机选 3 名
    lucky_users = random_sample(users, 3)
    print(f"幸运用户: {lucky_users}")
    
    # 生成随机测试数据
    ages = [generate_random_int(18, 60) for _ in range(10)]
    print(f"随机年龄: {ages}")
```

- [ ] **Step 3: 删除导航链接并提交**

```bash
git add "03-高级语法篇/02-标准库/02-random随机数.md"
git commit -m "refactor: improve 02-random随机数 with progressive teaching and type hints"
```

---

## Task 12: 重构 02-标准库 文档（03-datetime日期时间）

**Files:**
- Modify: `03-高级语法篇/02-标准库/03-datetime日期时间.md`

- [ ] **Step 1: 添加实际场景**

```markdown
# datetime 日期时间（详细版）

> Python 3.11+

## 第一部分：日期时间基础

### 3.1 处理日期和时间

#### 实际场景

你的系统需要记录用户的注册时间、计算订单过期时间、显示"3 天前"这样的相对时间。日期和时间处理是几乎所有应用的必备功能。

**问题：如何用 Python 处理日期和时间的计算、格式化、比较？**
```

- [ ] **Step 2: 添加带类型注解的示例**

```python
from __future__ import annotations
from datetime import datetime, timedelta, date
from typing import Optional

def days_until(target_date: date) -> int:
    """计算距离目标日期还有多少天
    
    Args:
        target_date: 目标日期
        
    Returns:
        距离天数（正数表示未来，负数表示过去）
    """
    today = date.today()
    delta = target_date - today
    return delta.days

def format_datetime(dt: datetime, pattern: str = "%Y-%m-%d %H:%M:%S") -> str:
    """格式化日期时间
    
    Args:
        dt: datetime 对象
        pattern: 格式字符串
        
    Returns:
        格式化后的日期时间字符串
    """
    return dt.strftime(pattern)

def parse_datetime(date_str: str, pattern: str = "%Y-%m-%d") -> Optional[date]:
    """解析日期字符串
    
    Args:
        date_str: 日期字符串
        pattern: 格式字符串
        
    Returns:
        解析后的 date 对象，失败返回 None
    """
    try:
        return datetime.strptime(date_str, pattern).date()
    except ValueError:
        return None

if __name__ == '__main__':
    # 计算 2026 年春节还有多少天
    spring_festival = date(2026, 2, 17)
    days = days_until(spring_festival)
    print(f"距离春节还有 {days} 天")
    
    # 格式化当前时间
    now = datetime.now()
    print(format_datetime(now))
```

- [ ] **Step 3: 删除导航链接并提交**

```bash
git add "03-高级语法篇/02-标准库/03-datetime日期时间.md"
git commit -m "refactor: improve 03-datetime日期时间 with progressive teaching and type hints"
```

---

## Task 13: 重构 02-标准库 文档（04-os-pathlib路径操作）

**Files:**
- Modify: `03-高级语法篇/02-标准库/04-os-pathlib路径操作.md`

- [ ] **Step 1: 添加实际场景**

```markdown
# os 与 pathlib 路径操作（详细版）

> Python 3.11+

## 第一部分：路径操作基础

### 4.1 pathlib 现代路径操作

#### 实际场景

你的程序需要：
- 读取配置文件 `config/settings.json`
- 创建日志目录 `logs/2026/04/`
- 批量处理 `data/*.csv` 文件
- 获取用户上传文件的扩展名判断类型

手动拼接路径 `"logs/" + year + "/" + month + "/"` 容易出错，而且不同操作系统路径分隔符不同。

**问题：如何用 Python 安全、跨平台地处理文件路径？**
```

- [ ] **Step 2: 添加 pathlib 示例（推荐）**

```python
from __future__ import annotations
from pathlib import Path
from typing import Iterator, list

def get_project_root() -> Path:
    """获取项目根目录"""
    return Path(__file__).parent.parent.parent

def ensure_dir(path: Path) -> Path:
    """确保目录存在，不存在则创建
    
    Args:
        path: 目录路径
        
    Returns:
        目录路径
    """
    path.mkdir(parents=True, exist_ok=True)
    return path

def find_files(directory: Path, pattern: str = "*.txt") -> Iterator[Path]:
    """查找目录下匹配模式的文件
    
    Args:
        directory: 目录路径
        pattern: glob 匹配模式
        
    Returns:
        匹配的文件路径迭代器
    """
    return directory.glob(pattern)

def get_file_info(file_path: Path) -> dict[str, str | int]:
    """获取文件信息
    
    Args:
        file_path: 文件路径
        
    Returns:
        文件信息字典
    """
    return {
        "name": file_path.name,
        "extension": file_path.suffix,
        "size": file_path.stat().st_size,
        "parent": str(file_path.parent),
    }

if __name__ == '__main__':
    # 创建日志目录
    logs_dir = Path("logs") / "2026" / "04"
    ensure_dir(logs_dir)
    print(f"日志目录: {logs_dir}")
    
    # 查找所有 CSV 文件
    data_dir = Path("data")
    for csv_file in find_files(data_dir, "*.csv"):
        print(csv_file)
```

- [ ] **Step 3: 删除导航链接并提交**

```bash
git add "03-高级语法篇/02-标准库/04-os-pathlib路径操作.md"
git commit -m "refactor: improve 04-os-pathlib路径操作 with progressive teaching and type hints"
```

---

## Task 14: 重构 02-标准库 文档（05-json数据处理）

**Files:**
- Modify: `03-高级语法篇/02-标准库/05-json数据处理.md`

- [ ] **Step 1: 添加实际场景**

```markdown
# json 数据处理（详细版）

> Python 3.11+

## 第一部分：JSON 基础

### 5.1 JSON 格式简介

#### 实际场景

你的程序需要：
- 保存用户配置到文件
- 从 API 接口获取 JSON 数据
- 与前端 JavaScript 应用交换数据

JSON 是最常用的数据交换格式，几乎所有 Web API 都用 JSON 返回数据。

**问题：如何用 Python 读写 JSON 数据？**
```

- [ ] **Step 2: 添加带类型注解的示例**

```python
from __future__ import annotations
import json
from pathlib import Path
from typing import Any

def save_json(data: dict[str, Any], file_path: Path) -> None:
    """保存 JSON 数据到文件
    
    Args:
        data: 要保存的数据
        file_path: 文件路径
    """
    with file_path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_json(file_path: Path) -> dict[str, Any]:
    """从文件加载 JSON 数据
    
    Args:
        file_path: 文件路径
        
    Returns:
        解析后的数据字典
    """
    with file_path.open("r", encoding="utf-8") as f:
        return json.load(f)

def json_to_string(data: dict[str, Any]) -> str:
    """将数据转换为 JSON 字符串
    
    Args:
        data: 数据字典
        
    Returns:
        JSON 字符串
    """
    return json.dumps(data, ensure_ascii=False)

def string_to_json(json_str: str) -> dict[str, Any]:
    """将 JSON 字符串解析为数据
    
    Args:
        json_str: JSON 字符串
        
    Returns:
        解析后的数据字典
    """
    return json.loads(json_str)

if __name__ == '__main__':
    # 保存用户配置
    config = {
        "user": "Alice",
        "theme": "dark",
        "language": "zh-CN",
        "notifications": True,
    }
    config_file = Path("config/user_config.json")
    save_json(config, config_file)
    
    # 加载并打印
    loaded_config = load_json(config_file)
    print(f"用户主题: {loaded_config['theme']}")
```

- [ ] **Step 3: 删除导航链接并提交**

```bash
git add "03-高级语法篇/02-标准库/05-json数据处理.md"
git commit -m "refactor: improve 05-json数据处理 with progressive teaching and type hints"
```

---

## Task 15: 重构 02-标准库 文档（06-文件操作）

**Files:**
- Modify: `03-高级语法篇/02-标准库/06-文件操作.md`

- [ ] **Step 1: 添加实际场景**

```markdown
# 文件操作（详细版）

> Python 3.11+

## 第一部分：文件读写基础

### 6.1 读写文本文件

#### 实际场景

你的程序需要：
- 保存用户日志到文件
- 读取配置文件内容
- 处理 CSV 数据文件
- 复制和移动文件

文件操作是几乎所有程序的基础功能。

**问题：如何用 Python 安全、高效地读写文件？**
```

- [ ] **Step 2: 添加带类型注解的示例**

```python
from __future__ import annotations
from pathlib import Path
from typing import Iterator

def read_file(file_path: Path) -> str:
    """读取文件全部内容
    
    Args:
        file_path: 文件路径
        
    Returns:
        文件内容字符串
    """
    return file_path.read_text(encoding="utf-8")

def write_file(file_path: Path, content: str) -> None:
    """写入内容到文件
    
    Args:
        file_path: 文件路径
        content: 要写入的内容
    """
    file_path.write_text(content, encoding="utf-8")

def read_lines(file_path: Path) -> list[str]:
    """逐行读取文件
    
    Args:
        file_path: 文件路径
        
    Returns:
        行内容列表
    """
    return file_path.read_text(encoding="utf-8").splitlines()

def append_line(file_path: Path, line: str) -> None:
    """追加一行到文件
    
    Args:
        file_path: 文件路径
        line: 要追加的行内容
    """
    with file_path.open("a", encoding="utf-8") as f:
        f.write(line + "\n")

def copy_file(source: Path, destination: Path) -> None:
    """复制文件
    
    Args:
        source: 源文件路径
        destination: 目标文件路径
    """
    destination.write_bytes(source.read_bytes())

if __name__ == '__main__':
    # 写入日志
    log_file = Path("logs/app.log")
    append_line(log_file, f"[{Path(__file__).name}] 程序启动")
    
    # 读取配置
    config_file = Path("config/settings.txt")
    if config_file.exists():
        lines = read_lines(config_file)
        print(f"配置行数: {len(lines)}")
```

- [ ] **Step 3: 删除导航链接并提交**

```bash
git add "03-高级语法篇/02-标准库/06-文件操作.md"
git commit -m "refactor: improve 06-文件操作 with progressive teaching and type hints"
```

---

## Task 16: 重构 02-标准库 文档（07-正则表达式）

**Files:**
- Modify: `03-高级语法篇/02-标准库/07-正则表达式.md`

- [ ] **Step 1: 添加实际场景**

```markdown
# 正则表达式（详细版）

> Python 3.11+

## 第一部分：正则表达式基础

### 7.1 什么是正则表达式

#### 实际场景

你需要：
- 验证邮箱地址格式是否正确
- 从 HTML 中提取所有链接
- 批量替换文本中的日期格式
- 判断字符串是否是有效的手机号

这些"模式匹配"的任务，用普通字符串方法很难做，但正则表达式可以轻松解决。

**问题：如何用 Python 的正则表达式处理复杂的文本匹配？**
```

- [ ] **Step 2: 添加带类型注解的示例**

```python
from __future__ import annotations
import re
from typing import Optional

def validate_email(email: str) -> bool:
    """验证邮箱格式
    
    Args:
        email: 邮箱地址
        
    Returns:
        True 如果格式正确
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_phone(phone: str) -> bool:
    """验证中国手机号格式
    
    Args:
        phone: 手机号码
        
    Returns:
        True 如果格式正确
    """
    pattern = r'^1[3-9]\d{9}$'
    return bool(re.match(pattern, phone))

def extract_numbers(text: str) -> list[str]:
    """从文本中提取所有数字
    
    Args:
        text: 文本内容
        
    Returns:
        数字字符串列表
    """
    return re.findall(r'\d+', text)

def replace_date_format(text: str) -> str:
    """将 2026/04/07 格式转换为 2026-04-07
    
    Args:
        text: 文本内容
        
    Returns:
        替换后的文本
    """
    return re.sub(r'(\d{4})/(\d{2})/(\d{2})', r'\1-\2-\3', text)

if __name__ == '__main__':
    # 验证邮箱
    emails = ["test@example.com", "invalid-email", "user.name@domain.co.uk"]
    for email in emails:
        print(f"{email}: {validate_email(email)}")
    
    # 提取数字
    text = "订单号 12345，金额 678 元，日期 20260407"
    numbers = extract_numbers(text)
    print(f"提取的数字: {numbers}")
```

- [ ] **Step 3: 删除导航链接并提交**

```bash
git add "03-高级语法篇/02-标准库/07-正则表达式.md"
git commit -m "refactor: improve 07-正则表达式 with progressive teaching and type hints"
```

---

## Task 17: 更新 02-标准库 README

**Files:**
- Modify: `03-高级语法篇/02-标准库/README.md`

- [ ] **Step 1: 创建新的 README**

```markdown
# 标准库

学习 Python 标准库的常用模块，掌握文件、日期、数学、JSON 等核心功能。

---

## 章节导航

| 章节 | 文件 | 主题 |
|------|------|------|
| 01 | [01-math数学库.md](./01-math数学库.md) | 数学函数、常量 |
| 02 | [02-random随机数.md](./02-random随机数.md) | 随机数生成、随机选择 |
| 03 | [03-datetime日期时间.md](./03-datetime日期时间.md) | 日期时间处理 |
| 04 | [04-os-pathlib路径操作.md](./04-os-pathlib路径操作.md) | 路径操作、文件系统 |
| 05 | [05-json数据处理.md](./05-json数据处理.md) | JSON 编解码 |
| 06 | [06-文件操作.md](./06-文件操作.md) | 文件读写、复制 |
| 07 | [07-正则表达式.md](./07-正则表达式.md) | 模式匹配、文本处理 |

---

## 示例项目

[stdlib_demo/](./stdlib_demo/) - 标准库实践示例
```

- [ ] **Step 2: 提交 README**

```bash
git add "03-高级语法篇/02-标准库/README.md"
git commit -m "refactor: update 02-标准库 README with new structure"
```

---

## Task 18: 重构 03-并发与异步编程 文档（01-并发基础概念）

**Files:**
- Modify: `03-高级语法篇/03-并发与异步编程/01-并发基础概念.md`

- [ ] **Step 1: 添加实际场景**

```markdown
# 并发基础概念（详细版）

> Python 3.11+

## 第一部分：并发与并行

### 1.1 什么是并发

#### 实际场景

你开发一个 Web 应用，需要同时处理 100 个用户的请求：
- 用户 A 请求查看订单
- 用户 B 上传文件
- 用户 C 下载报告
- ...

如果一次只处理一个请求，其他 99 个用户都要等待，体验极差。

**问题：如何让程序"同时"处理多个任务？**
```

- [ ] **Step 2: 添加带类型注解的示例**

```python
from __future__ import annotations
import threading
import time
from typing import Callable

def cpu_bound_task(n: int) -> int:
    """CPU 密集型任务
    
    Args:
        n: 计算范围
        
    Returns:
        计算结果
    """
    count = 0
    for i in range(n):
        count += i
    return count

def io_bound_task(duration: float) -> str:
    """模拟 I/O 密集型任务
    
    Args:
        duration: 等待时间
        
    Returns:
        任务完成信息
    """
    time.sleep(duration)
    return f"任务完成，耗时 {duration}s"

def run_concurrent_tasks(tasks: list[Callable], args_list: list) -> list:
    """并发运行多个任务
    
    Args:
        tasks: 任务函数列表
        args_list: 参数列表
        
    Returns:
        结果列表
    """
    threads = []
    results = []
    
    for task, args in zip(tasks, args_list):
        t = threading.Thread(target=task, args=args)
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
    
    return results

if __name__ == '__main__':
    # 对比单线程和多线程
    start = time.time()
    cpu_bound_task(10_000_000)
    cpu_bound_task(10_000_000)
    print(f"单线程 CPU 任务: {time.time() - start:.2f}s")
    
    start = time.time()
    io_bound_task(1.0)
    io_bound_task(1.0)
    print(f"单线程 I/O 任务: {time.time() - start:.2f}s")
```

- [ ] **Step 3: 删除导航链接并提交**

```bash
git add "03-高级语法篇/03-并发与异步编程/01-并发基础概念.md"
git commit -m "refactor: improve 01-并发基础概念 with progressive teaching and type hints"
```

---

## Task 19: 重构 03-并发与异步编程 文档（02-多线程编程）

**Files:**
- Modify: `03-高级语法篇/03-并发与异步编程/02-多线程编程.md`

- [ ] **Step 1: 添加实际场景**

```markdown
# 多线程编程（详细版）

> Python 3.11+

## 第一部分：线程基础

### 2.1 创建线程

#### 实际场景

你的程序需要同时下载 10 个文件：
- 文件 1: 从服务器 A 下载
- 文件 2: 从服务器 B 下载
- ...

如果按顺序下载，每个文件耗时 5 秒，总共需要 50 秒。如果用多线程同时下载，理论上只需要 5 秒。

**问题：如何用 Python 多线程同时执行多个任务？**
```

- [ ] **Step 2: 添加带类型注解的示例**

```python
from __future__ import annotations
import threading
import time
from typing import Callable

def download_file(url: str, filename: str) -> str:
    """模拟下载文件
    
    Args:
        url: 文件 URL
        filename: 保存文件名
        
    Returns:
        下载完成信息
    """
    time.sleep(2)  # 模拟下载耗时
    return f"已下载 {filename}"

def concurrent_download(tasks: list[tuple[str, str]]) -> list[str]:
    """并发下载多个文件
    
    Args:
        tasks: (url, filename) 任务列表
        
    Returns:
        结果列表
    """
    threads: list[threading.Thread] = []
    results: list[str] = []
    
    def worker(url: str, filename: str) -> None:
        result = download_file(url, filename)
        results.append(result)
    
    for url, filename in tasks:
        t = threading.Thread(target=worker, args=(url, filename))
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
    
    return results

if __name__ == '__main__':
    tasks = [
        ("http://server1.com/file1", "file1.txt"),
        ("http://server2.com/file2", "file2.txt"),
        ("http://server3.com/file3", "file3.txt"),
    ]
    
    start = time.time()
    results = concurrent_download(tasks)
    print(f"耗时: {time.time() - start:.2f}s")
    for r in results:
        print(r)
```

- [ ] **Step 3: 删除导航链接并提交**

```bash
git add "03-高级语法篇/03-并发与异步编程/02-多线程编程.md"
git commit -m "refactor: improve 02-多线程编程 with progressive teaching and type hints"
```

---

## Task 20: 重构 03-并发与异步编程 文档（03-线程同步）

**Files:**
- Modify: `03-高级语法篇/03-并发与异步编程/03-线程同步.md`

- [ ] **Step 1: 添加实际场景**

```markdown
# 线程同步（详细版）

> Python 3.11+

## 第一部分：线程安全问题

### 3.1 为什么需要同步

#### 实际场景

你的程序有多个线程同时访问一个计数器：
- 线程 1: 计数器 +1
- 线程 2: 计数器 +1
- 线程 3: 计数器 +1

期望结果是计数器 = 3，但实际可能是 1 或 2。这是因为多个线程同时读写同一变量，产生了竞态条件。

**问题：如何保证多个线程安全地访问共享资源？**
```

- [ ] **Step 2: 添加带类型注解的示例**

```python
from __future__ import annotations
import threading
from typing import Final

class SafeCounter:
    """线程安全的计数器"""
    
    def __init__(self, initial: int = 0) -> None:
        self._value: int = initial
        self._lock: threading.Lock = threading.Lock()
    
    def increment(self) -> int:
        """增加计数
        
        Returns:
            增加后的值
        """
        with self._lock:
            self._value += 1
            return self._value
    
    def get_value(self) -> int:
        """获取当前值
        
        Returns:
            计数器当前值
        """
        with self._lock:
            return self._value

def worker(counter: SafeCounter, iterations: int) -> None:
    """工作线程
    
    Args:
        counter: 计数器实例
        iterations: 增加次数
    """
    for _ in range(iterations):
        counter.increment()

if __name__ == '__main__':
    counter = SafeCounter()
    threads: list[threading.Thread] = []
    
    # 创建 10 个线程，每个增加 1000 次
    for _ in range(10):
        t = threading.Thread(target=worker, args=(counter, 1000))
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
    
    print(f"最终计数: {counter.get_value()}")  # 应该是 10000
```

- [ ] **Step 3: 删除导航链接并提交**

```bash
git add "03-高级语法篇/03-并发与异步编程/03-线程同步.md"
git commit -m "refactor: improve 03-线程同步 with progressive teaching and type hints"
```

---

## Task 21: 重构 03-并发与异步编程 文档（04-多进程编程）

**Files:**
- Modify: `03-高级语法篇/03-并发与异步编程/04-多进程编程.md`

- [ ] **Step 1: 添加实际场景**

```markdown
# 多进程编程（详细版）

> Python 3.11+

## 第一部分：进程基础

### 4.1 创建进程

#### 实际场景

你需要对 100 万张图片进行压缩处理，每张图片处理耗时 0.1 秒：
- 单线程: 总耗时 100 秒
- 多线程: 受 GIL 限制，几乎无提升
- 多进程: 利用多核 CPU，8 核可以缩短到约 12.5 秒

CPU 密集型任务需要多进程才能利用多核。

**问题：如何用 Python 多进程绕过 GIL，利用多核 CPU？**
```

- [ ] **Step 2: 添加带类型注解的示例**

```python
from __future__ import annotations
import multiprocessing
import time
from typing import Sequence

def process_image(image_id: int) -> str:
    """模拟图片处理（CPU 密集型）
    
    Args:
        image_id: 图片 ID
        
    Returns:
        处理结果
    """
    # 模拟 CPU 计算
    total = 0
    for i in range(100_000):
        total += i
    return f"图片 {image_id} 处理完成"

def parallel_process(images: Sequence[int], num_processes: int = 4) -> list[str]:
    """并行处理多个图片
    
    Args:
        images: 图片 ID 序列
        num_processes: 进程数量
        
    Returns:
        处理结果列表
    """
    with multiprocessing.Pool(processes=num_processes) as pool:
        results = pool.map(process_image, images)
    return results

if __name__ == '__main__':
    # 注意：多进程必须在 if __name__ == '__main__' 下运行
    images = list(range(100))
    
    start = time.time()
    results = parallel_process(images, num_processes=4)
    elapsed = time.time() - start
    
    print(f"处理 {len(images)} 张图片，耗时 {elapsed:.2f}s")
    print(f"每张图片平均耗时: {elapsed / len(images):.4f}s")
```

- [ ] **Step 3: 删除导航链接并提交**

```bash
git add "03-高级语法篇/03-并发与异步编程/04-多进程编程.md"
git commit -m "refactor: improve 04-多进程编程 with progressive teaching and type hints"
```

---

## Task 22: 重构 03-并发与异步编程 文档（05-asyncio异步编程）

**Files:**
- Modify: `03-高级语法篇/03-并发与异步编程/05-asyncio异步编程.md`

- [ ] **Step 1: 添加实际场景**

```markdown
# asyncio 异步编程（详细版）

> Python 3.11+

## 第一部分：异步基础

### 5.1 什么是异步编程

#### 实际场景

你的程序需要调用 10 个 Web API：
- API 1: 响应时间 0.5 秒
- API 2: 响应时间 0.3 秒
- ...

如果按顺序调用，总耗时是所有响应时间之和。如果用 asyncio 同时发起请求，总耗时约等于最慢的那个 API。

**问题：如何用 Python asyncio 实现高效的异步 I/O？**
```

- [ ] **Step 2: 添加带类型注解的示例**

```python
from __future__ import annotations
import asyncio
import time
from typing import Coroutine

async def fetch_api(api_name: str, delay: float) -> str:
    """模拟 API 调用
    
    Args:
        api_name: API 名称
        delay: 响应延迟
        
    Returns:
        API 响应
    """
    await asyncio.sleep(delay)  # 模拟网络延迟
    return f"{api_name} 响应"

async def fetch_all_apis(apis: list[tuple[str, float]]) -> list[str]:
    """并发获取所有 API
    
    Args:
        apis: (api_name, delay) 列表
        
    Returns:
        所有 API 响应
    """
    tasks: list[Coroutine] = [fetch_api(name, delay) for name, delay in apis]
    results = await asyncio.gather(*tasks)
    return results

async def main() -> None:
    """主函数"""
    apis = [
        ("API-1", 0.5),
        ("API-2", 0.3),
        ("API-3", 0.8),
        ("API-4", 0.2),
        ("API-5", 0.4),
    ]
    
    start = time.time()
    results = await fetch_all_apis(apis)
    elapsed = time.time() - start
    
    print(f"调用 {len(apis)} 个 API，总耗时 {elapsed:.2f}s")
    for r in results:
        print(r)

if __name__ == '__main__':
    asyncio.run(main())
```

- [ ] **Step 3: 删除导航链接并提交**

```bash
git add "03-高级语法篇/03-并发与异步编程/05-asyncio异步编程.md"
git commit -m "refactor: improve 05-asyncio异步编程 with progressive teaching and type hints"
```

---

## Task 23: 重构 03-并发与异步编程 文档（06-并发模型选择）

**Files:**
- Modify: `03-高级语法篇/03-并发与异步编程/06-并发模型选择.md`

- [ ] **Step 1: 添加实际场景**

```markdown
# 并发模型选择（详细版）

> Python 3.11+

## 第一部分：选择正确的并发模型

### 6.1 如何选择

#### 实际场景

你的项目有多种任务类型：
- Web 请求处理：需要同时响应 100 个用户
- 图片处理：需要压缩 1000 张图片
- 数据分析：需要计算 10 万条记录的统计信息

不同的任务类型，应该用不同的并发模型。选择错误会导致性能下降甚至无提升。

**问题：如何根据任务类型选择正确的并发模型？**
```

- [ ] **Step 2: 添加决策表**

```markdown
#### 并发模型选择决策表

| 任务类型 | 特点 | 推荐模型 | 原因 |
|----------|------|----------|------|
| I/O 密集型（网络请求） | 等待时间长 | asyncio | 单线程即可，效率最高 |
| I/O 密集型（文件读写） | 等待时间长 | 多线程 | 简单易用 |
| CPU 密集型（数值计算） | 计算时间长 | 多进程 | 绕过 GIL，利用多核 |
| 混合型 | 两者都有 | 多进程 + asyncio | 组合使用 |

#### 选择流程

```
判断任务类型：
├─ I/O 密集型？
│   ├─ 是 → 需要大量并发？
│   │   ├─ 是 → asyncio（推荐）
│   │   ├─ 否 → 多线程
│   └─ 否 → CPU 密集型
│       ├─ 是 → 多进程
│       └─ 否 → 单线程足够
```

#### Python 3.11+ asyncio 改进

Python 3.11 对 asyncio 进行了重大优化：
- `asyncio.TaskGroup`：更安全的任务组管理
- 更快的协程切换
- 更好的异常处理
```

- [ ] **Step 3: 删除导航链接并提交**

```bash
git add "03-高级语法篇/03-并发与异步编程/06-并发模型选择.md"
git commit -m "refactor: improve 06-并发模型选择 with progressive teaching"
```

---

## Task 24: 更新 03-并发与异步编程 README

**Files:**
- Modify: `03-高级语法篇/03-并发与异步编程/README.md`

- [ ] **Step 1: 创建新的 README**

```markdown
# 并发与异步编程

学习 Python 并发编程，掌握多线程、多进程、asyncio 等并发模型。

---

## 章节导航

| 章节 | 文件 | 主题 |
|------|------|------|
| 01 | [01-并发基础概念.md](./01-并发基础概念.md) | 并发 vs 并行、GIL |
| 02 | [02-多线程编程.md](./02-多线程编程.md) | 线程创建、线程池 |
| 03 | [03-线程同步.md](./03-线程同步.md) | Lock、Semaphore、Event |
| 04 | [04-多进程编程.md](./04-多进程编程.md) | 进程创建、进程间通信 |
| 05 | [05-asyncio异步编程.md](./05-asyncio异步编程.md) | 协程、async/await |
| 06 | [06-并发模型选择.md](./06-并发模型选择.md) | 选择决策、最佳实践 |

---

## 示例项目

[async_demo/](./async_demo/) - 并发编程实践示例
```

- [ ] **Step 2: 提交 README**

```bash
git add "03-高级语法篇/03-并发与异步编程/README.md"
git commit -m "refactor: update 03-并发与异步编程 README with new structure"
```

---

## Task 25: 更新主 README.md

**Files:**
- Modify: `03-高级语法篇/README.md`

- [ ] **Step 1: 更新主 README**

```markdown
# 高级语法篇

学习 Python 高级语法特性，掌握模块管理、标准库、并发编程等进阶技能。

---

## 章节导航

### 01-模块与包

| 章节 | 文件 | 主题 |
|------|------|------|
| 01 | [01-模块与包/01-模块基础.md](./01-模块与包/01-模块基础.md) | 模块概念、import 语法 |
| 02 | [01-模块与包/02-自定义模块.md](./01-模块与包/02-自定义模块.md) | 创建模块、搜索路径 |
| 03 | [01-模块与包/03-包的结构.md](./01-模块与包/03-包的结构.md) | 包结构、__init__.py |
| 04 | [01-模块与包/04-导入机制.md](./01-模块与包/04-导入机制.md) | 绝对/相对导入 |
| 05 | [01-模块与包/05-pip包管理.md](./01-模块与包/05-pip包管理.md) | pip、uv 命令 |
| 06 | [01-模块与包/06-发布自己的包.md](./01-模块与包/06-发布自己的包.md) | 打包、发布 PyPI |

### 02-标准库

| 章节 | 文件 | 主题 |
|------|------|------|
| 01 | [02-标准库/01-math数学库.md](./02-标准库/01-math数学库.md) | 数学函数、常量 |
| 02 | [02-标准库/02-random随机数.md](./02-标准库/02-random随机数.md) | 随机数生成 |
| 03 | [02-标准库/03-datetime日期时间.md](./02-标准库/03-datetime日期时间.md) | 日期时间处理 |
| 04 | [02-标准库/04-os-pathlib路径操作.md](./02-标准库/04-os-pathlib路径操作.md) | 路径操作 |
| 05 | [02-标准库/05-json数据处理.md](./02-标准库/05-json数据处理.md) | JSON 编解码 |
| 06 | [02-标准库/06-文件操作.md](./02-标准库/06-文件操作.md) | 文件读写 |
| 07 | [02-标准库/07-正则表达式.md](./02-标准库/07-正则表达式.md) | 模式匹配 |

### 03-并发与异步编程

| 章节 | 文件 | 主题 |
|------|------|------|
| 01 | [03-并发与异步编程/01-并发基础概念.md](./03-并发与异步编程/01-并发基础概念.md) | 并发 vs 并行、GIL |
| 02 | [03-并发与异步编程/02-多线程编程.md](./03-并发与异步编程/02-多线程编程.md) | 线程创建、线程池 |
| 03 | [03-并发与异步编程/03-线程同步.md](./03-并发与异步编程/03-线程同步.md) | Lock、Semaphore |
| 04 | [03-并发与异步编程/04-多进程编程.md](./03-并发与异步编程/04-多进程编程.md) | 进程创建、通信 |
| 05 | [03-并发与异步编程/05-asyncio异步编程.md](./03-并发与异步编程/05-asyncio异步编程.md) | 协程、async/await |
| 06 | [03-并发与异步编程/06-并发模型选择.md](./03-并发与异步编程/06-并发模型选择.md) | 选择决策 |
```

- [ ] **Step 2: 提交主 README**

```bash
git add "03-高级语法篇/README.md"
git commit -m "refactor: update 03-高级语法篇 main README with new structure"
```

---

## Task 26: 最终验证

- [ ] **Step 1: 检查目录结构**

```bash
ls -la "03-高级语法篇/"
```

Expected output:
```
01-模块与包/
02-标准库/
03-并发与异步编程/
modules_demo/
stdlib_demo/
async_demo/
README.md
```

- [ ] **Step 2: 检查文件数量**

```bash
find "03-高级语法篇" -name "*.md" -not -name "README.md" | wc -l
```

Expected: 19 files

- [ ] **Step 3: 推送到远程**

```bash
git push
```

---

## 验收清单

- [ ] 所有目录有数字前缀（01-, 02-, 03-）
- [ ] 所有文档有 Python 3.11+ 版本说明
- [ ] 所有代码有类型注解
- [ ] 所有文档遵循 6 步渐进式教学法结构
- [ ] README.md 链接正确
- [ ] 无导航链接残留
- [ ] Git 提交清晰（每个阶段独立提交）