# Python 基础入门篇教学改进实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Improve 12 chapters in the basics section using progressive teaching approach with 6-step teaching method.

**Architecture:** Add introduction layers (steps 1-3) and application layers (steps 5-6) to each chapter, while preserving existing detailed content (step 4). Use Python 3.11+ features throughout.

**Tech Stack:** Python 3.11+, Markdown documentation, no code testing required (documentation project)

---

## File Structure

**Modified files (12 chapters):**

```
01-基础入门篇/
├── Python入门/
│   ├── 01-Python简介.md       # Add progressive layers
│   └── 02-环境搭建.md         # Add progressive layers
├── 基础语法/
│   ├── 01-变量与数据类型.md    # Add progressive layers
│   ├── 02-运算符.md            # Add progressive layers
│   ├── 03-流程控制.md          # Add progressive layers + match statement
├── 字符串/
│   ├── 01-字符串基础.md        # Add progressive layers
├── 数据结构/
│   ├── 01-列表.md              # Add progressive layers
│   ├── 02-元组.md              # Add progressive layers
│   ├── 03-字典.md              # Add progressive layers
│   ├── 04-集合.md              # Add progressive layers
│   └── 05-推导式.md            # Add progressive layers
```

**Each file modification includes:**
1. Add version notice (Python 3.11+)
2. Add introduction layers (steps 1-3)
3. Keep existing detailed content (step 4)
4. Add progressive complexity examples (step 5)
5. Add practical application example (step 6)

---

## Batch 1: Entry Threshold Chapters

### Task 1: Improve Python Introduction Chapter

**Files:**
- Modify: `01-基础入门篇/Python入门/01-Python简介.md`

- [ ] **Step 1: Read current file content**

Read the file to understand existing structure and content.

- [ ] **Step 2: Add version notice at beginning**

Add Python 3.11+ version notice after the title:

```markdown
# Python 简介

> **本章代码基于 Python 3.11+ 编写**
>
> Python 3.11+ 相比旧版本的优势：
> - 🚀 执行速度提升 10-60%
> - 🎯 错误信息更精确（指出具体行和列）
> - 💡 match 语句简化分支逻辑
> - ✨ 类型提示更简洁直观

---

```

- [ ] **Step 3: Add introduction section (step 1)**

Add after version notice:

```markdown
## 为什么学习 Python？一个真实的选择场景

**问题场景：**
你需要完成一项数据整理任务：从1000个文本文件中提取特定信息并汇总到Excel表格。

**不使用 Python 的做法：**
- 手动打开每个文件，复制粘贴需要的信息
- 耗时：约 10 小时（假设每个文件1分钟）
- 容易出错：遗漏文件、复制错误

**使用 Python 的做法：**

```python
# 自动化脚本（Python 3.11+）
import pathlib

data_dir = pathlib.Path("data_files")
results = []

for file in data_dir.glob("*.txt"):
    content = file.read_text()
    # 提取特定信息（示例）
    if "关键词" in content:
        results.append(file.name)

print(f"找到 {len(results)} 个文件")
# 耗时：约 1 分钟
```

这就是 Python 的价值：**用少量代码，自动化繁琐任务**。

---
```

- [ ] **Step 4: Add concept motivation section (step 2)**

Add after introduction:

```markdown
## Python 解决了什么问题？

Python 的本质是：**让人能用简洁的代码解决实际问题**。

就像你用 Excel 公式自动计算，而不是手动一个个算。Python 能做的更多：
- 处理大量文件和数据
- 自动化重复性工作
- 构建网站和应用
- 分析数据和制作图表
- 开发游戏和人工智能应用

**Python 的特点：**

1. **易学易用**：语法接近自然语言，新手快速上手
2. **功能强大**：从简单脚本到复杂系统都能开发
3. **生态丰富**：大量现成的工具库，不用从头写
4. **应用广泛**：数据分析、Web开发、AI、自动化等领域

---
```

- [ ] **Step 5: Add simplest example section (step 3)**

Add after concept motivation:

```markdown
## Python 的最简体验（3分钟上手）

Python 最简单的用法：打印输出和简单计算。

```python
# 打印输出
print("Hello, World!")  # 输出：Hello, World!

# 简单计算
result = 10 + 20
print(result)  # 输出：30

# 变量存储
name = "Python"
version = 3.11
print(f"{name} {version}")  # 输出：Python 3.11
```

这就是 Python 的基本用法。接下来我们详细了解 Python 的特性。

---
```

- [ ] **Step 6: Keep existing detailed content (step 4)**

Ensure the existing detailed content sections remain intact. Only adjust their position if needed.

- [ ] **Step 7: Add progressive complexity section (step 5)**

Add before the end of the file:

```markdown
## 从简单到复杂：Python 应用的渐进示例

**层级1：单行命令**

```python
# 简单打印
print("Hello")
```

**层级2：多行脚本**

```python
# 计算并打印
a = 10
b = 20
print(f"总和：{a + b}")
```

**层级3：函数封装**

```python
# 定义函数
def calculate_sum(x: int, y: int) -> int:
    return x + y

result = calculate_sum(10, 20)
print(result)
```

**层级4：文件处理**

```python
# 读写文件
import pathlib

file = pathlib.Path("data.txt")
content = file.read_text()
print(content)
```

**层级5：数据处理**

```python
# 处理多个文件
import pathlib

data_dir = pathlib.Path("data")
for file in data_dir.glob("*.txt"):
    print(file.name)
```

---
```

- [ ] **Step 8: Add practical application section (step 6)**

Add at the end:

```markdown
## 综合应用：自动化文件整理脚本

这个示例展示 Python 在实际工作中的应用：

```python
# 文件整理脚本（Python 3.11+）
import pathlib
from datetime import datetime

def organize_files(source_dir: str) -> dict[str, int]:
    """
    按文件类型整理文件到不同文件夹
    
    Args:
        source_dir: 源目录路径
    
    Returns:
        整理后的文件统计
    """
    source = pathlib.Path(source_dir)
    stats: dict[str, int] = {}
    
    # 按扩展名分类
    for file in source.glob("*.*"):
        if file.is_file():
            ext = file.suffix.lower()
            
            # 创建分类文件夹
            target_dir = source / ext.replace(".", "")
            target_dir.mkdir(exist_ok=True)
            
            # 移动文件
            file.rename(target_dir / file.name)
            stats[ext] = stats.get(ext, 0) + 1
    
    return stats

# 使用示例
if __name__ == "__main__":
    result = organize_files("downloads")
    for ext, count in result.items():
        print(f"{ext} 文件：{count} 个")
```

**这个脚本展示了：**
- Python 处理文件的能力
- 函数的定义和调用
- 循环和条件判断
- pathlib 模块的使用
- 字典存储统计数据
- 类型提示的现代语法

---
```

- [ ] **Step 9: Commit changes**

```bash
git add 01-基础入门篇/Python入门/01-Python简介.md
git commit -m "Improve Python Introduction chapter with progressive teaching layers

Add:
- Python 3.11+ version notice
- Problem-driven introduction
- Concept motivation section  
- Simplest example section
- Progressive complexity examples
- Practical application example"
```

---

### Task 2: Improve Environment Setup Chapter

**Files:**
- Modify: `01-基础入门篇/Python入门/02-环境搭建.md`

- [ ] **Step 1: Read current file content**

Read the file to understand existing structure and content.

- [ ] **Step 2: Add version notice at beginning**

Add Python 3.11+ version notice after the title:

```markdown
# 环境搭建

> **本章代码基于 Python 3.11+ 编写**
>
> 环境搭建是学习 Python 的第一步，本章使用现代工具 uv（推荐）或传统 pip。

---

```

- [ ] **Step 3: Add introduction section (step 1)**

Add after version notice:

```markdown
## 为什么需要搭建编程环境？一个真实的对比

**问题场景：**
你想学习 Python，但不知道从哪里开始写代码。

**不搭建环境的困惑：**
- 在哪里写代码？用记事本？
- 写好的代码怎么运行？
- 代码出错了怎么调试？
- 如何安装 Python 的扩展库？

**搭建环境后的清晰流程：**

```
┌─────────────────────────────────────────────────────────┐
│          完整的 Python 编程工作流                         │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  1. 安装 Python 解释器                                  │
│     ↓                                                   │
│  2. 配置编辑器（VS Code）                                │
│     ↓                                                   │
│  3. 写代码 → 运行 → 查看结果                             │
│     ↓                                                   │
│  4. 出错 → 调试 → 修正                                   │
│     ↓                                                   │
│  5. 安装扩展库 → 扩展功能                                │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

这就是编程环境的价值：**提供完整的工具链，让编程过程顺畅**。

---
```

- [ ] **Step 4: Add concept motivation section (step 2)**

Add after introduction:

```markdown
## 编程环境解决了什么问题？

编程环境的本质是：**为代码提供"生存空间"和"运行能力"**。

就像鱼需要水才能游泳，代码需要环境才能运行。

**编程环境的组成部分：**

1. **Python 解释器**：将代码翻译成机器能执行的指令
2. **编辑器**：写代码的工具（推荐 VS Code）
3. **包管理器**：安装和管理扩展库（推荐 uv）
4. **终端/命令行**：运行代码的入口

**为什么推荐 uv 而非 pip？**

uv 是新一代 Python 包管理器，优势：
- 🚀 速度快（比 pip 快 10-100 倍）
- 🎯 自动管理虚拟环境
- ✨ 统一工具链（pip、pip-tools、virtualenv 的功能合并）

---
```

- [ ] **Step 5: Add simplest example section (step 3)**

Add after concept motivation:

```markdown
## 环境搭建的最简流程（5分钟上手）

最简单的环境搭建只需要3步：

```bash
# 步骤 1：安装 uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# 步骤 2：安装 Python
uv python install 3.11

# 步骤 3：验证安装
uv run python --version
# 输出：Python 3.11.x
```

安装完成后，立即可以运行代码：

```bash
uv run python -c "print('Hello, Python 3.11!')"
# 输出：Hello, Python 3.11!
```

这就是环境搭建的基本流程。接下来我们详细了解各个步骤。

---
```

- [ ] **Step 6: Keep existing detailed content (step 4)**

Ensure the existing detailed content sections remain intact, including:
- Python 安装详解
- 编辑器配置
- 包管理器使用
- 常见问题解答

- [ ] **Step 7: Add progressive complexity section (step 5)**

Add before the end:

```markdown
## 从简单到复杂：环境配置的渐进示例

**层级1：单文件脚本**

```bash
# 创建并运行单个 Python 文件
uv run python hello.py
```

**层级2：创建项目结构**

```bash
# 初始化项目
uv init my-project
cd my-project
uv run python main.py
```

**层级3：添加依赖库**

```bash
# 添加第三方库
uv add requests
uv run python main.py
```

**层级4：虚拟环境管理**

```bash
# 创建独立环境
uv venv
source .venv/bin/activate  # Linux/Mac
# 或 .venv\Scripts\activate  # Windows
```

**层级5：多项目环境隔离**

```bash
# 不同项目使用不同 Python 版本
uv python install 3.11
uv python install 3.12

# 项目A使用 3.11
cd project-a
uv python pin 3.11

# 项目B使用 3.12  
cd project-b
uv python pin 3.12
```

---
```

- [ ] **Step 8: Add practical application section (step 6)**

Add at the end:

```markdown
## 综合应用：完整的 Python 项目初始化流程

这个示例展示从零创建一个完整项目：

```bash
# 项目初始化完整流程（Python 3.11+）

# 1. 创建项目
uv init data-analysis-project
cd data-analysis-project

# 2. 安装 Python
uv python install 3.11

# 3. 添加依赖
uv add pandas matplotlib jupyter

# 4. 创建项目结构
mkdir -p src data notebooks tests

# 5. 创建示例代码
cat > src/main.py << 'EOF'
"""数据分析示例"""
import pandas as pd
import matplotlib.pyplot as plt

def analyze_data(file_path: str) -> pd.DataFrame:
    """读取并分析数据"""
    df = pd.read_csv(file_path)
    return df.describe()

if __name__ == "__main__":
    result = analyze_data("data/sample.csv")
    print(result)
EOF

# 6. 运行代码
uv run python src/main.py

# 7. 启动 Jupyter Notebook（交互式编程）
uv run jupyter notebook
```

**项目结构示例：**

```
data-analysis-project/
├── pyproject.toml       # 项目配置
├── src/
│   └── main.py          # 主代码
├── data/
│   └── sample.csv       # 数据文件
├── notebooks/
│   └── analysis.ipynb   # Jupyter 笔记本
├── tests/
│   └── test_main.py     # 测试代码
└── .venv/               # 虚拟环境（自动创建）
```

---
```

- [ ] **Step 9: Commit changes**

```bash
git add 01-基础入门篇/Python入门/02-环境搭建.md
git commit -m "Improve Environment Setup chapter with progressive teaching layers

Add:
- Python 3.11+ version notice
- Problem-driven introduction
- Concept motivation section
- Simplest example section
- Progressive complexity examples
- Practical application example with uv workflow"
```

---

## Batch 2: Basic Syntax Chapters

### Task 3: Improve Variables and Data Types Chapter

**Files:**
- Modify: `01-基础入门篇/基础语法/01-变量与数据类型.md`

- [ ] **Step 1: Read current file content**

Read the file (already done in previous exploration, but verify current state).

- [ ] **Step 2: Add version notice at beginning**

Add Python 3.11+ version notice after the title:

```markdown
# 变量与数据类型

> **本章代码基于 Python 3.11+ 编写**
>
> 变量是程序存储数据的基本方式，理解变量和数据类型是编程的第一步。

---

```

- [ ] **Step 3: Add introduction section (step 1)**

Insert before existing "什么是变量" section:

```markdown
## 为什么需要变量？一个真实的存储场景

**问题场景：**
你在开发一个学生信息管理程序，需要存储每个学生的姓名、年龄、成绩。

**不使用变量的困惑：**
- 如何在程序中"记住"这些数据？
- 数据处理完后还能找到吗？
- 如何在程序的不同地方使用相同的数据？

**使用变量的解决方案：**

```python
# 用变量存储学生信息
name = "张三"
age = 18
score = 85.5

# 在程序中多次使用
print(f"学生姓名：{name}")  # 输出：张三
print(f"年龄：{age}岁")     # 输出：18岁
print(f"成绩：{score}分")   # 输出：85.5分

# 数据仍然保留，可以继续使用
average = score / 3  # 计算平均分
```

这就是变量的价值：**用一个名字，存储和复用数据**。

---
```

- [ ] **Step 4: Add concept motivation section (step 2)**

Add after introduction:

```markdown
## 变量解决了什么问题？

变量的本质是：**给数据一个"名字"，方便存储和引用**。

就像你给文件贴标签，方便以后找到。变量就是程序中的"标签"。

**变量的优势：**

1. **存储数据**：程序运行时保存信息
2. **复用数据**：同一个数据多次使用，不用重复写
3. **修改数据**：可以随时更新存储的内容
4. **传递数据**：在不同地方传递和处理数据

**数据类型的作用：**

数据类型告诉程序"这个变量是什么"，就像标签上的说明：
- `int`：整数（如年龄：18）
- `float`：浮点数（如成绩：85.5）
- `str`：字符串（如姓名："张三"）
- `bool`：布尔值（如是否通过：True）

---
```

- [ ] **Step 5: Keep existing content but reorder**

Keep existing sections but ensure they follow the 6-step structure. The existing "什么是变量" becomes part of step 4 (detailed explanation).

- [ ] **Step 6: Add progressive complexity section (step 5)**

Add before the end:

```markdown
## 从简单到复杂：变量的渐进应用

**层级1：单个变量**

```python
# 最简单的变量
name: str = "Python"
print(name)
```

**层级2：多个变量**

```python
# 多个相关变量
name: str = "张三"
age: int = 18
score: float = 85.5

print(f"{name}, {age}岁, {score}分")
```

**层级3：变量交换**

```python
# Python 特有的变量交换
a: int = 10
b: int = 20
a, b = b, a  # 一行完成交换
print(a, b)  # 输出：20 10
```

**层级4：动态变量**

```python
# 变量可以改变类型（Python 动态类型特性）
x: int | str = 10
x = "现在是字符串"
print(x)
```

**层级5：变量与运算**

```python
# 变量参与计算
price: float = 99.9
quantity: int = 3
total: float = price * quantity
print(f"总价：{total:.2f}")
```

---
```

- [ ] **Step 7: Add practical application section (step 6)**

Add at the end:

```markdown
## 综合应用：学生信息管理示例

这个示例综合运用变量和数据类型：

```python
# 学生信息管理（Python 3.11+）
from typing import Any

def main() -> None:
    # 存储多个学生信息
    students: list[dict[str, Any]] = [
        {"name": "张三", "age": 18, "scores": [85, 90, 78]},
        {"name": "李四", "age": 19, "scores": [92, 88, 95]},
        {"name": "王五", "age": 17, "scores": [78, 82, 88]}
    ]
    
    # 处理每个学生数据
    for student in students:
        name: str = student["name"]
        age: int = student["age"]
        scores: list[int] = student["scores"]
        
        # 计算平均分（变量运算）
        average: float = sum(scores) / len(scores)
        
        # 判断是否通过（布尔变量）
        passed: bool = average >= 60
        
        # 输出信息
        print(f"{name}({age}岁): 平均分 {average:.1f} - {'通过' if passed else '未通过'}")

if __name__ == "__main__":
    main()
```

**这个示例展示了：**
- 不同类型变量的定义和使用
- 变量之间的运算
- 布尔变量的判断应用
- 变量在函数中的传递
- 现代类型提示语法

---
```

- [ ] **Step 8: Commit changes**

```bash
git add 01-基础入门篇/基础语法/01-变量与数据类型.md
git commit -m "Improve Variables and Data Types chapter with progressive teaching layers

Add:
- Python 3.11+ version notice
- Problem-driven introduction
- Concept motivation section
- Progressive complexity examples
- Practical application example"
```

---

### Task 4: Improve Operators Chapter

**Files:**
- Modify: `01-基础入门篇/基础语法/02-运算符.md`

- [ ] **Step 1: Read current file content**

Read the file to understand existing structure.

- [ ] **Step 2: Add version notice and introduction layers**

Add similar structure as previous chapters:
- Python 3.11+ version notice
- Introduction: "为什么需要运算符？一个真实的计算场景"
- Concept motivation: "运算符解决了什么问题？"
- Simplest example: "运算符的最简用法"

Example introduction:

```markdown
## 为什么需要运算符？一个真实的计算场景

**问题场景：**
你在开发一个购物计算程序，需要计算总价、折扣、税费。

**不使用运算符的困惑：**
- 如何在程序中进行数学计算？
- 如何判断价格是否达到折扣门槛？
- 如何组合多个条件？

**使用运算符的解决方案：**

```python
# 购物计算
price: float = 100.0
quantity: int = 3

# 算术运算符：计算总价
total: float = price * quantity

# 比较运算符：判断是否享受折扣
has_discount: bool = total >= 200

# 逻辑运算符：组合多个条件
is_member: bool = True
final_discount: float = 0.9 if (has_discount and is_member) else 1.0

final_price: float = total * final_discount
print(f"原价：{total}元，折后：{final_price}元")
```

这就是运算符的价值：**让程序能够进行计算和判断**。

---
```

- [ ] **Step 3: Keep existing detailed content**

Ensure all operator types (算术、比较、逻辑、位运算、成员、身份) remain intact.

- [ ] **Step 4: Add progressive complexity and practical application**

Add step 5 and step 6 sections similar to previous chapters.

- [ ] **Step 5: Commit changes**

```bash
git add 01-基础入门篇/基础语法/02-运算符.md
git commit -m "Improve Operators chapter with progressive teaching layers"
```

---

### Task 5: Improve Flow Control Chapter (with match statement)

**Files:**
- Modify: `01-基础入门篇/基础语法/03-流程控制.md`

- [ ] **Step 1: Read current file content**

Read the file to understand existing structure.

- [ ] **Step 2: Add version notice and introduction layers**

Add introduction focusing on decision-making:

```markdown
## 为什么需要流程控制？一个真实的决策场景

**问题场景：**
你在开发一个自动售货机程序，需要根据用户投入金额决定可以购买的饮料。

**不使用流程控制的困惑：**
- 程序只能"直线执行"，无法根据条件做出不同反应
- 如何处理"如果...就...否则..."的情况？

**使用流程控制的解决方案：**

```python
# 自动售货机决策
money: float = 4.0

# 使用 if 判断
if money >= 5:
    print("可以购买可乐（5元）")
elif money >= 4:
    print("可以购买雪碧（4元）")
elif money >= 3:
    print("可以购买矿泉水（3元）")
else:
    print("金额不足，请继续投币")
```

这就是流程控制的价值：**让程序能够根据条件做出决策**。

---
```

- [ ] **Step 3: Add detailed match statement section**

Ensure match statement (Python 3.10+) has comprehensive coverage in step 4:

```markdown
### match 语句详解（Python 3.10+）

**match 语句是 Python 3.10 引入的新特性，用于模式匹配。**

**基础用法：**

```python
# 替代复杂的 if-elif chain
status: str = "success"

match status:
    case "success":
        print("操作成功")
    case "error":
        print("操作失败")
    case "pending":
        print("处理中")
    case _:
        print("未知状态")  # _ 是通配符
```

**高级用法：结构模式匹配**

```python
# 匹配数据结构
def process_command(cmd: dict[str, str]) -> str:
    match cmd:
        case {"action": "move", "direction": d}:
            return f"向{d}移动"
        case {"action": "attack", "target": t}:
            return f"攻击{t}"
        case {"action": "quit"}:
            return "退出游戏"
        case _:
            return "未知命令"

# 使用示例
cmd1: dict[str, str] = {"action": "move", "direction": "北"}
print(process_command(cmd1))  # 输出：向北移动

cmd2: dict[str, str] = {"action": "attack", "target": "怪物"}
print(process_command(cmd2))  # 输出：攻击怪物
```

**匹配多个值：**

```python
# 使用 | 匹配多个值
grade: str = "B"

match grade:
    case "A" | "A+":
        print("优秀")
    case "B" | "B+":
        print("良好")
    case "C":
        print("中等")
    case _:
        print("需要努力")
```

**匹配序列：**

```python
# 匹配列表结构
def analyze_list(items: list[int]) -> str:
    match items:
        case []:
            return "空列表"
        case [x]:
            return f"单元素：{x}"
        case [x, y]:
            return f"两个元素：{x} 和 {y}"
        case [first, *rest]:
            return f"首元素：{first}, 其余：{rest}"
        case _:
            return "未知结构"

print(analyze_list([]))           # 空列表
print(analyze_list([1]))          # 单元素：1
print(analyze_list([1, 2, 3, 4])) # 首元素：1, 其余：[2, 3, 4]
```

**match vs if-elif 对比：**

| 特性 | if-elif | match |
|------|---------|-------|
| 适用场景 | 简单条件判断 | 模式匹配、结构解构 |
| 代码可读性 | 条件多时较复杂 | 结构清晰 |
| 功能 | 基础判断 | 高级模式匹配 |
| 版本要求 | 所有版本 | Python 3.10+ |

---
```

- [ ] **Step 4: Add progressive complexity with match statement**

```markdown
## 从简单到复杂：流程控制的渐进应用

**层级1：单一条件**

```python
# 简单 if
age: int = 18
if age >= 18:
    print("成年人")
```

**层级2：多条件判断**

```python
# if-elif-else
score: int = 85
if score >= 90:
    print("优秀")
elif score >= 60:
    print("通过")
else:
    print("不及格")
```

**层级3：嵌套条件**

```python
# 嵌套 if
score: int = 85
has_bonus: bool = True

if score >= 60:
    if has_bonus:
        print("通过 + 加分")
    else:
        print("通过")
```

**层级4：循环 + 条件**

```python
# 筛选数据
scores: list[int] = [85, 45, 92, 58, 78]
passed: list[int] = []

for score in scores:
    if score >= 60:
        passed.append(score)

print(f"通过人数：{len(passed)}")
```

**层级5：match 语句应用**

```python
# 使用 match 简化判断（Python 3.10+）
action: str = "attack"

match action:
    case "move":
        print("移动")
    case "attack":
        print("攻击")
    case "defend":
        print("防御")
    case _:
        print("未知动作")
```

---
```

- [ ] **Step 5: Add practical application (vending machine)**

Use the vending machine example from design document.

- [ ] **Step 6: Commit changes**

```bash
git add 01-基础入门篇/基础语法/03-流程控制.md
git commit -m "Improve Flow Control chapter with progressive teaching and match statement

Add:
- Python 3.11+ version notice
- Problem-driven introduction
- Detailed match statement section (Python 3.10+)
- Progressive complexity examples including match
- Practical vending machine application"
```

---

## Batch 3: String Processing Chapter

### Task 6: Improve String Basics Chapter

**Files:**
- Modify: `01-基础入门篇/字符串/01-字符串基础.md`

- [ ] **Step 1: Read current file content**

Read the file to understand existing structure.

- [ ] **Step 2: Add version notice and introduction layers**

Add introduction focusing on text processing:

```markdown
## 为什么需要字符串？一个真实的文本处理场景

**问题场景：**
你在开发一个日志分析程序，需要从日志中提取时间、错误类型等信息。

**不使用字符串处理的困惑：**
- 如何在程序中表示和操作文本？
- 如何从长文本中提取特定部分？
- 如何格式化输出信息？

**使用字符串的解决方案：**

```python
# 日志分析示例
log: str = "[2024-01-15 10:30:45] ERROR: Connection failed"

# 提取时间（字符串切片）
time: str = log[1:20]
print(f"时间：{time}")

# 判断错误类型（字符串查找）
if "ERROR" in log:
    print("发现错误日志")

# 格式化输出（f-string）
error_type: str = "Connection"
print(f"错误类型：{error_type}")
```

这就是字符串的价值：**让程序能够处理和分析文本数据**。

---
```

- [ ] **Step 3: Add concept motivation**

```markdown
## 字符串解决了什么问题？

字符串的本质是：**用程序处理文本数据**。

就像你用 Word 编辑文档，Python 用字符串处理文本。

**字符串的常见用途：**

1. **存储文本**：用户输入、文件内容、日志信息
2. **提取信息**：从长文本中找到特定内容
3. **格式化输出**：生成清晰易读的输出
4. **文本分析**：统计、搜索、替换

---
```

- [ ] **Step 4: Keep existing detailed content**

Ensure all string operations (创建、索引、切片、方法、格式化) remain intact.

- [ ] **Step 5: Add progressive complexity and practical application**

Add examples showing text processing progression.

- [ ] **Step 6: Commit changes**

```bash
git add 01-基础入门篇/字符串/01-字符串基础.md
git commit -m "Improve String Basics chapter with progressive teaching layers"
```

---

## Batch 4: Data Structure Chapters

### Task 7: Improve List Chapter

**Files:**
- Modify: `01-基础入门篇/数据结构/01-列表.md`

- [ ] **Step 1: Read current file content**

Read the file (already explored, but verify current state).

- [ ] **Step 2: Add version notice and all 6 steps**

This chapter has extensive existing content (819 lines). Apply the 6-step structure:
- Version notice
- Introduction (使用成绩管理场景)
- Concept motivation
- Simplest example
- Keep all existing detailed content
- Add progressive complexity (层级1-4)
- Add practical application (学生成绩管理)

- [ ] **Step 3: Commit changes**

```bash
git add 01-基础入门篇/数据结构/01-列表.md
git commit -m "Improve List chapter with complete 6-step teaching structure"
```

---

### Task 8: Improve Tuple Chapter

**Files:**
- Modify: `01-基础入门篇/数据结构/02-元组.md`

- [ ] **Step 1: Read current file content**

Read the file to understand existing structure.

- [ ] **Step 2: Add introduction focusing on immutable data**

```markdown
## 为什么需要元组？一个不可变数据的需求场景

**问题场景：**
你在开发一个配置管理系统，需要存储固定的配置项（如数据库连接信息）。

**问题：**
- 用列表存储配置，可能被意外修改
- 如何确保某些数据不被改变？

**使用元组的解决方案：**

```python
# 数据库配置（不可变）
db_config: tuple[str, str, int] = ("localhost", "mydb", 3306)

# 元组无法修改，保护配置安全
# db_config[0] = "newhost"  # TypeError: 不能修改

# 但可以创建新元组
new_config: tuple[str, str, int] = ("newhost", db_config[1], db_config[2])
```

这就是元组的价值：**保护重要数据不被意外修改**。

---
```

- [ ] **Step 3: Add all layers and commit**

```bash
git add 01-基础入门篇/数据结构/02-元组.md
git commit -m "Improve Tuple chapter with progressive teaching layers"
```

---

### Task 9: Improve Dictionary Chapter

**Files:**
- Modify: `01-基础入门篇/数据结构/03-字典.md`

- [ ] **Step 1: Read and improve**

Add introduction focusing on key-value mapping:

```markdown
## 为什么需要字典？一个键值映射的需求场景

**问题场景：**
你在开发一个学生成绩查询系统，需要通过学号快速找到学生姓名和成绩。

**不使用字典的方案（列表）：**

```python
# 用列表存储（查找麻烦）
students: list[list[str | int]] = [
    ["001", "张三", 85],
    ["002", "李四", 92],
    ["003", "王五", 78]
]

# 查找学号 002 的学生
for student in students:
    if student[0] == "002":
        print(student[1])  # 输出：李四
```

**问题：**
- 查找慢（需要遍历）
- 索引不直观（0、1、2代表什么？）

**使用字典的解决方案：**

```python
# 用字典存储（键值映射）
students: dict[str, dict[str, int]] = {
    "001": {"name": "张三", "score": 85},
    "002": {"name": "李四", "score": 92},
    "003": {"name": "王五", "score": 78}
}

# 直接通过键查找（O(1) 查询）
print(students["002"]["name"])  # 输出：李四
```

这就是字典的价值：**用"键"快速找到"值"**。

---
```

- [ ] **Step 2: Commit**

```bash
git add 01-基础入门篇/数据结构/03-字典.md
git commit -m "Improve Dictionary chapter with progressive teaching layers"
```

---

### Task 10: Improve Set Chapter

**Files:**
- Modify: `01-基础入门篇/数据结构/04-集合.md`

- [ ] **Step 1: Add introduction focusing on uniqueness**

```markdown
## 为什么需要集合？一个去重的需求场景

**问题场景：**
你在分析用户访问日志，需要统计有多少个不同用户访问过网站。

**不使用集合的方案（列表）：**

```python
# 用户访问日志（可能有重复）
user_ids: list[str] = ["user1", "user2", "user1", "user3", "user2", "user4"]

# 统计不同用户
unique: list[str] = []
for uid in user_ids:
    if uid not in unique:
        unique.append(uid)

print(f"不同用户：{len(unique)}")  # 输出：4
```

**问题：**
- 需要手动检查重复
- 查找慢（每次都要遍历）

**使用集合的解决方案：**

```python
# 用集合自动去重
user_ids: list[str] = ["user1", "user2", "user1", "user3", "user2", "user4"]
unique: set[str] = set(user_ids)

print(f"不同用户：{len(unique)}")  # 输出：4
```

这就是集合的价值：**自动去除重复，快速判断存在**。

---
```

- [ ] **Step 2: Commit**

```bash
git add 01-基础入门篇/数据结构/04-集合.md
git commit -m "Improve Set chapter with progressive teaching layers"
```

---

### Task 11: Improve Comprehension Chapter

**Files:**
- Modify: `01-基础入门篇/数据结构/05-推导式.md`

- [ ] **Step 1: Add introduction focusing on efficiency**

```markdown
## 为什么需要推导式？一个高效数据转换场景

**问题场景：**
你需要从一个数字列表中筛选出所有偶数并计算平方。

**不使用推导式的方案（循环）：**

```python
# 传统循环方式
numbers: list[int] = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
result: list[int] = []

for n in numbers:
    if n % 2 == 0:  # 筛选偶数
        result.append(n ** 2)  # 计算平方

print(result)  # 输出：[4, 16, 36, 64, 100]
```

**问题：**
- 代码较长（4行）
- 需要先创建空列表

**使用推导式的解决方案：**

```python
# 列表推导式（一行搞定）
numbers: list[int] = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
result: list[int] = [n ** 2 for n in numbers if n % 2 == 0]

print(result)  # 输出：[4, 16, 36, 64, 100]
```

这就是推导式的价值：**简洁高效地转换数据**。

---
```

- [ ] **Step 2: Commit**

```bash
git add 01-基础入门篇/数据结构/05-推导式.md
git commit -m "Improve Comprehension chapter with progressive teaching layers"
```

---

## Batch 5: Final Validation

### Task 12: Validate All Chapters

**Files:**
- All 12 modified chapters

- [ ] **Step 1: Verify Python 3.11+ syntax**

Check all code examples use modern Python 3.11+ features:
- `list[int]` not `List[int]`
- `dict[str, Any]` not `Dict[str, Any]`  
- `X | None` not `Optional[X]`
- Match statement examples (流程控制章节)

- [ ] **Step 2: Verify 6-step structure**

For each chapter, verify:
- ✅ Version notice present
- ✅ Introduction section (step 1)
- ✅ Concept motivation (step 2)
- ✅ Simplest example (step 3)
- ✅ Detailed content intact (step 4)
- ✅ Progressive complexity (step 5)
- ✅ Practical application (step 6)

- [ ] **Step 3: Verify content quality**

- Introduction scenarios are relevant and realistic
- Concept explanations are clear and通俗
- Progressive examples have clear hierarchy
- Practical applications show knowledge integration

- [ ] **Step 4: Final commit**

```bash
git add .
git commit -m "Complete Python basics teaching improvement for all 12 chapters

Implemented 6-step teaching method:
1. Problem-driven introduction
2. Concept motivation
3. Simplest example
4. Detailed explanation
5. Progressive complexity
6. Practical application

All chapters updated with Python 3.11+ features and modern type hints."
```

- [ ] **Step 5: Update README if needed**

Update chapter descriptions to reflect new teaching approach.

---

## Summary

**Total tasks: 12**
- Batch 1: 2 tasks (Python入门)
- Batch 2: 3 tasks (基础语法)
- Batch 3: 1 task (字符串)
- Batch 4: 5 tasks (数据结构)
- Batch 5: 1 task (验证)

**Estimated time: 4-6 hours**

**Key principles:**
- Preserve existing detailed content
- Add introduction and application layers
- Use Python 3.11+ features consistently
- Clear progressive complexity hierarchy
- Practical and relevant examples

---

Plan complete. Ready for execution.