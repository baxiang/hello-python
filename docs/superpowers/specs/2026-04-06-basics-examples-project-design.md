# Python 基础入门篇示例工程设计

> **设计目标：** 为《Python基础入门篇》11个章节创建可运行的完整示例工程，每个章节对应独立的py文件和测试文件。

---

## 一、项目概述

### 背景与目标

**当前问题：**
- 教程文档包含大量代码示例，但散落在markdown文件中
- 学习者无法直接运行示例代码
- 缺少统一的测试验证

**改进目标：**
1. 创建集中的示例工程目录
2. 从教程文档提取所有示例代码到独立py文件
3. 为每个章节编写对应的测试文件
4. 提供统一的项目配置和运行方式

### 项目范围

**包含章节：**
- 11个主要章节（Python简介、环境搭建、变量、运算符、流程控制、字符串、列表、元组、字典、集合、推导式）
- 每个章节1个示例文件
- 9个章节需要测试文件（Python简介、环境搭建除外）

---

## 二、项目结构设计

### 目录结构

```
01-基础入门篇/
├── examples/                           # 示例工程根目录
│   ├── pyproject.toml                 # 项目配置（Python 3.11+）
│   ├── README.md                      # 示例工程说明
│   ├── src/                           # 源代码目录
│   │   ├── __init__.py
│   │   │
│   │   ├── 01_python_intro.py         # Python简介章节示例
│   │   ├── 02_environment.py          # 环境搭建章节示例
│   │   │
│   │   ├── 03_variables.py            # 变量与数据类型章节示例
│   │   ├── 04_operators.py            # 运算符章节示例
│   │   ├── 05_flow_control.py         # 流程控制章节示例
│   │   │
│   │   ├── 06_strings.py              # 字符串章节示例
│   │   │
│   │   ├── 07_lists.py                # 列表章节示例
│   │   ├── 08_tuples.py               # 元组章节示例
│   │   ├── 09_dicts.py                # 字典章节示例
│   │   ├── 10_sets.py                 # 集合章节示例
│   │   └── 11_comprehensions.py       # 推导式章节示例
│   │
│   └── tests/                         # 测试代码目录
│       ├── __init__.py
│       ├── conftest.py                # pytest配置
│       ├── test_03_variables.py
│       ├── test_04_operators.py
│       ├── test_05_flow_control.py
│       ├── test_06_strings.py
│       ├── test_07_lists.py
│       ├── test_08_tuples.py
│       ├── test_09_dicts.py
│       ├── test_10_sets.py
│       └── test_11_comprehensions.py
│
├── Python入门/                        # 教程文档（保持不变）
│   ├── 01-Python简介.md
│   └── 02-环境搭建.md
├── 基础语法/
│   ├── 01-变量与数据类型.md
│   ├── 02-运算符.md
│   └── 03-流程控制.md
├── 字符串/
│   └── 01-字符串基础.md
└── 数据结构/
    ├── 01-列表.md
    ├── 02-元组.md
    ├── 03-字典.md
    ├── 04-集合.md
    └── 05-推导式.md
```

### 文件命名规范

| 章节 | 文档路径 | 示例文件 | 测试文件 |
|------|---------|---------|---------|
| Python简介 | `Python入门/01-Python简介.md` | `src/01_python_intro.py` | 无需测试 |
| 环境搭建 | `Python入门/02-环境搭建.md` | `src/02_environment.py` | 无需测试 |
| 变量与数据类型 | `基础语法/01-变量与数据类型.md` | `src/03_variables.py` | `tests/test_03_variables.py` |
| 运算符 | `基础语法/02-运算符.md` | `src/04_operators.py` | `tests/test_04_operators.py` |
| 流程控制 | `基础语法/03-流程控制.md` | `src/05_flow_control.py` | `tests/test_05_flow_control.py` |
| 字符串 | `字符串/01-字符串基础.md` | `src/06_strings.py` | `tests/test_06_strings.py` |
| 列表 | `数据结构/01-列表.md` | `src/07_lists.py` | `tests/test_07_lists.py` |
| 元组 | `数据结构/02-元组.md` | `src/08_tuples.py` | `tests/test_08_tuples.py` |
| 字典 | `数据结构/03-字典.md` | `src/09_dicts.py` | `tests/test_09_dicts.py` |
| 集合 | `数据结构/04-集合.md` | `src/10_sets.py` | `tests/test_10_sets.py` |
| 推导式 | `数据结构/05-推导式.md` | `src/11_comprehensions.py` | `tests/test_11_comprehensions.py` |

---

## 三、代码文件结构设计

### 示例文件标准结构

```python
"""
章节：XX - XXXX
文档：01-基础入门篇/XXX/XX-XXXX.md

本章示例代码包含：
1. 最简示例：基础用法
2. 渐进示例：从简单到复杂
3. 综合应用：实际场景示例

运行方式：
    uv run python src/XX_xxxx.py
    uv run pytest tests/test_XX_xxxx.py -v
"""

from typing import Any


# ============================================
# 第1部分：最简示例（对应教程"最简用法"）
# ============================================

def example_01_basic() -> None:
    """示例1：最简基础用法
    
    对应教程：XX的最简用法（3分钟上手）
    """
    print("示例1：最简基础用法")
    # 代码示例
    pass


# ============================================
# 第2部分：渐进示例（对应教程"从简单到复杂"）
# ============================================

def example_02_level1() -> None:
    """示例2：层级1 - 最简单"""
    print("示例2：层级1")
    # 代码示例
    pass


def example_03_level2() -> None:
    """示例3：层级2 - 增加复杂度"""
    print("示例3：层级2")
    # 代码示例
    pass


def example_04_level3() -> None:
    """示例4：层级3 - 进一步扩展"""
    print("示例4：层级3")
    # 代码示例
    pass


def example_05_level4() -> None:
    """示例5：层级4 - 高级用法"""
    print("示例5：层级4")
    # 代码示例
    pass


def example_06_level5() -> None:
    """示例6：层级5 - 最复杂用法"""
    print("示例6：层级5")
    # 代码示例
    pass


# ============================================
# 第3部分：综合应用（对应教程"综合应用"）
# ============================================

def example_practical() -> None:
    """综合应用：实际场景示例
    
    对应教程：综合应用：XXX示例
    """
    print("综合应用：实际场景示例")
    # 代码示例
    pass


# ============================================
# 主函数
# ============================================

def main() -> None:
    """主函数：运行所有示例"""
    print("=" * 60)
    print("章节 XX - XXXX")
    print("=" * 60)
    print()
    
    # 第1部分：最简示例
    print("【第1部分：最简示例】")
    example_01_basic()
    print()
    
    # 第2部分：渐进示例
    print("【第2部分：渐进示例】")
    for i in range(2, 7):
        func_name = f"example_0{i}_level{i-1}"
        if func_name in globals():
            globals()[func_name]()
            print()
    
    # 第3部分：综合应用
    print("【第3部分：综合应用】")
    example_practical()
    print()
    
    print("=" * 60)
    print("✅ 所有示例运行完成")
    print("=" * 60)


if __name__ == "__main__":
    main()
```

### 测试文件标准结构

```python
"""
章节：XX - XXXX 的测试
文档：01-基础入门篇/XXX/XX-XXXX.md
代码：examples/src/XX_xxxx.py
"""

import pytest
from src.XX_xxxx import (
    example_01_basic,
    example_02_level1,
    example_03_level2,
    example_04_level3,
    example_05_level4,
    example_06_level5,
    example_practical,
)


class TestExample01:
    """测试示例1：最简基础用法"""
    
    def test_basic_function(self) -> None:
        """测试基础功能"""
        # 测试代码
        pass


class TestExample02:
    """测试示例2：层级1"""
    
    def test_level1_function(self) -> None:
        """测试层级1功能"""
        # 测试代码
        pass


class TestExample03:
    """测试示例3：层级2"""
    
    def test_level2_function(self) -> None:
        """测试层级2功能"""
        # 测试代码
        pass


class TestPractical:
    """测试综合应用"""
    
    def test_practical_function(self) -> None:
        """测试综合应用功能"""
        # 测试代码
        pass
```

---

## 四、项目配置设计

### pyproject.toml

```toml
[project]
name = "python-basics-examples"
version = "0.1.0"
description = "Python基础入门篇示例代码"
requires-python = ">=3.11"
dependencies = []

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "pytest-cov>=4.0.0",
    "ruff>=0.1.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = "test_*.py"
python_classes = "Test*"
python_functions = "test_*"
addopts = "-v --tb=short"

[tool.coverage.run]
source = ["src"]
omit = ["src/__init__.py"]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "if __name__ == .__main__.:",
]

[tool.ruff]
line-length = 88
target-version = "py311"

[tool.ruff.lint]
select = ["E", "F", "I", "N", "W", "UP", "B", "SIM"]
ignore = ["E501"]

[tool.ruff.lint.isort]
known-first-party = ["src"]
```

### conftest.py

```python
"""
pytest 配置文件
"""

import pytest
import sys
from pathlib import Path

# 添加 src 目录到 Python 路径
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))


def pytest_configure(config: pytest.Config) -> None:
    """pytest 配置"""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
```

---

## 五、README.md 设计

```markdown
# Python 基础入门篇示例代码

本目录包含《Python基础入门篇》所有章节的可运行示例代码和测试。

## 项目结构

```
examples/
├── pyproject.toml     # 项目配置
├── README.md          # 本文件
├── src/               # 示例代码
│   ├── 01_python_intro.py
│   ├── 02_environment.py
│   ├── 03_variables.py
│   ├── ...
│   └── 11_comprehensions.py
└── tests/             # 测试代码
    ├── test_03_variables.py
    ├── test_04_operators.py
    └── ...
```

## 快速开始

### 安装依赖

```bash
cd examples
uv sync
```

### 运行示例

```bash
# 运行单个章节示例
uv run python src/03_variables.py

# 运行流程控制章节（包含 match 语句）
uv run python src/05_flow_control.py
```

### 运行测试

```bash
# 运行所有测试
uv run pytest

# 运行单个章节测试
uv run pytest tests/test_03_variables.py -v

# 查看测试覆盖率
uv run pytest --cov=src --cov-report=html
open htmlcov/index.html
```

## 章节列表

| 编号 | 章节名称 | 示例文件 | 测试文件 | 文档位置 |
|-----|---------|---------|---------|---------|
| 01 | Python简介 | `src/01_python_intro.py` | - | `Python入门/01-Python简介.md` |
| 02 | 环境搭建 | `src/02_environment.py` | - | `Python入门/02-环境搭建.md` |
| 03 | 变量与数据类型 | `src/03_variables.py` | `tests/test_03_variables.py` | `基础语法/01-变量与数据类型.md` |
| 04 | 运算符 | `src/04_operators.py` | `tests/test_04_operators.py` | `基础语法/02-运算符.md` |
| 05 | 流程控制 | `src/05_flow_control.py` | `tests/test_05_flow_control.py` | `基础语法/03-流程控制.md` |
| 06 | 字符串 | `src/06_strings.py` | `tests/test_06_strings.py` | `字符串/01-字符串基础.md` |
| 07 | 列表 | `src/07_lists.py` | `tests/test_07_lists.py` | `数据结构/01-列表.md` |
| 08 | 元组 | `src/08_tuples.py` | `tests/test_08_tuples.py` | `数据结构/02-元组.md` |
| 09 | 字典 | `src/09_dicts.py` | `tests/test_09_dicts.py` | `数据结构/03-字典.md` |
| 10 | 集合 | `src/10_sets.py` | `tests/test_10_sets.py` | `数据结构/04-集合.md` |
| 11 | 推导式 | `src/11_comprehensions.py` | `tests/test_11_comprehensions.py` | `数据结构/05-推导式.md` |

## 代码说明

### 每个示例文件的结构

1. **最简示例** (`example_01_basic`)：对应教程"最简用法"
2. **渐进示例** (`example_02` - `example_06`)：对应教程"从简单到复杂"
3. **综合应用** (`example_practical`)：对应教程"综合应用"

### 运行方式

每个示例文件都可以独立运行：

```bash
# 运行变量章节示例
uv run python src/03_variables.py

# 输出示例：
# ============================================================
# 章节 03 - 变量与数据类型
# ============================================================
#
# 【第1部分：最简示例】
# 示例1：最简基础用法
# ...
```

## 技术要求

- Python 3.11+
- 使用现代类型提示语法（`list[int]` 而非 `List[int]`）
- 所有代码通过 ruff 检查
- 所有测试通过 pytest 验证

## 学习建议

1. 先阅读教程文档
2. 运行对应的示例代码
3. 修改示例代码，观察结果
4. 运行测试，验证理解

## License

MIT
```

---

## 六、代码提取策略

### 提取规则

**从教程文档提取代码的映射关系：**

| 教程章节 | 代码位置 | 函数名称 | 说明 |
|---------|---------|---------|------|
| "为什么需要...？" | 注释 | - | 作为文件头部说明 |
| "解决了什么问题？" | 注释 | - | 作为文件头部说明 |
| "最简用法（3分钟上手）" | 第1部分 | `example_01_basic()` | 最简单的可运行示例 |
| "从简单到复杂 层级1" | 第2部分 | `example_02_level1()` | 第一层复杂度 |
| "从简单到复杂 层级2" | 第2部分 | `example_03_level2()` | 第二层复杂度 |
| "从简单到复杂 层级3" | 第2部分 | `example_04_level3()` | 第三层复杂度 |
| "从简单到复杂 层级4" | 第2部分 | `example_05_level4()` | 第四层复杂度 |
| "从简单到复杂 层级5" | 第2部分 | `example_06_level5()` | 第五层复杂度 |
| "综合应用：XXX" | 第3部分 | `example_practical()` | 综合应用示例 |
| 其他代码块 | 辅助函数 | 按需命名 | 作为辅助功能 |

### 提取示例

**教程内容：**

```markdown
## 为什么需要列表？一个真实的批量数据场景

**问题场景：**
你在开发一个学生成绩管理系统...

**使用列表的解决方案：**
```python
scores: list[int] = [85, 92, 78, 96, 88]
average: float = sum(scores) / len(scores)
```

## 列表的最简用法（3分钟上手）

```python
fruits: list[str] = ["苹果", "香蕉", "橘子"]
print(fruits[0])  # 苹果
```

## 从简单到复杂：列表的渐进应用

**层级1：基础列表操作**
```python
shopping = ["牛奶", "面包", "鸡蛋"]
shopping.append("苹果")
```
```

**提取后的代码文件：**

```python
"""
章节：07 - 列表
文档：01-基础入门篇/数据结构/01-列表.md

本章示例代码包含：
1. 最简示例：列表基础用法
2. 渐进示例：从基础操作到嵌套列表
3. 综合应用：学生成绩管理示例

运行方式：
    uv run python src/07_lists.py
    uv run pytest tests/test_07_lists.py -v
"""

from typing import Any


# ============================================
# 第1部分：最简示例
# ============================================

def example_01_basic() -> None:
    """示例1：列表最简用法
    
    对应教程：列表的最简用法（3分钟上手）
    """
    print("示例1：列表最简用法")
    
    fruits: list[str] = ["苹果", "香蕉", "橘子"]
    print(f"列表：{fruits}")
    print(f"第一个元素：{fruits[0]}")
    
    # 修改元素
    fruits[0] = "西瓜"
    print(f"修改后：{fruits}")


# ============================================
# 第2部分：渐进示例
# ============================================

def example_02_level1() -> None:
    """示例2：层级1 - 基础操作"""
    print("示例2：层级1 - 基础操作")
    
    shopping: list[str] = ["牛奶", "面包", "鸡蛋"]
    print(f"购物清单：{shopping}")
    
    shopping.append("苹果")
    print(f"添加后：{shopping}")


# ... 更多示例函数


# ============================================
# 主函数
# ============================================

def main() -> None:
    """主函数：运行所有示例"""
    print("=" * 60)
    print("章节 07 - 列表")
    print("=" * 60)
    print()
    
    example_01_basic()
    print()
    
    example_02_level1()
    print()
    
    print("=" * 60)
    print("✅ 所有示例运行完成")
    print("=" * 60)


if __name__ == "__main__":
    main()
```

---

## 七、实施策略

### 实施顺序

分3个批次实施：

**批次1：项目初始化**
1. 创建项目目录结构
2. 编写 pyproject.toml
3. 编写 README.md
4. 创建 conftest.py

**批次2：提取示例代码（按章节顺序）**
1. `01_python_intro.py` - Python简介
2. `02_environment.py` - 环境搭建
3. `03_variables.py` - 变量与数据类型
4. `04_operators.py` - 运算符
5. `05_flow_control.py` - 流程控制
6. `06_strings.py` - 字符串
7. `07_lists.py` - 列表
8. `08_tuples.py` - 元组
9. `09_dicts.py` - 字典
10. `10_sets.py` - 集合
11. `11_comprehensions.py` - 推导式

**批次3：编写测试文件**
1. `test_03_variables.py`
2. `test_04_operators.py`
3. `test_05_flow_control.py`
4. `test_06_strings.py`
5. `test_07_lists.py`
6. `test_08_tuples.py`
7. `test_09_dicts.py`
8. `test_10_sets.py`
9. `test_11_comprehensions.py`

### 质量标准

**代码质量：**
- ✅ 所有代码使用 Python 3.11+ 类型提示
- ✅ 所有代码通过 ruff 检查
- ✅ 所有函数有文档字符串

**测试质量：**
- ✅ 所有测试通过 `pytest` 运行
- ✅ 测试覆盖率 > 80%
- ✅ 每个示例函数至少有1个测试

**文档质量：**
- ✅ 每个文件顶部有章节和文档对应说明
- ✅ 每个函数有对应教程章节说明
- ✅ README.md 有完整的使用说明

---

## 八、验收标准

### 功能验收

- ✅ 所有示例代码可以独立运行
- ✅ 所有测试通过 `pytest`
- ✅ 示例文件与教程文档一一对应
- ✅ 可以通过 `uv run python src/XX_xxxx.py` 运行任意章节

### 文档验收

- ✅ README.md 有完整的项目说明
- ✅ 每个代码文件有章节对应说明
- ✅ 每个测试文件有章节对应说明

### 质量验收

- ✅ `uv run ruff check src tests` 通过
- ✅ `uv run pytest --cov=src` 覆盖率 > 80%
- ✅ 所有代码使用现代 Python 3.11+ 语法

---

## 九、后续优化方向

完成本次项目后，可以考虑的后续优化：

1. **扩展到其他篇章**：为核心编程篇、高级语法篇创建类似示例工程
2. **增加 Jupyter Notebook**：为交互式学习提供 .ipynb 文件
3. **增加练习题**：为每个章节添加练习题和答案
4. **增加 CI/CD**：使用 GitHub Actions 自动运行测试

---

**设计完成时间：** 2026-04-06

**下一步：** 用户审阅本设计文档，确认后进入实施计划编写阶段