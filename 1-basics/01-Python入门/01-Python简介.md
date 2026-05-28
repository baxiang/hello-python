# 01-Python简介

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
results: list[str] = []

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

## 概念铺垫

## 什么是 Python

### 概念说明

**Python** 是一种高级、通用、解释型的编程语言，由荷兰程序员 **吉多·范罗苏姆（Guido van Rossum）** 于 1989 年圣诞节期间开始创建。

```
┌─────────────────────────────────────────┐
│          Python 名称的由来              │
├─────────────────────────────────────────┤
│                                         │
│  Python 的名字来源于英国喜剧团体        │
│  "Monty Python's Flying Circus"         │
│  （蒙提·派森的飞行马戏团）               │
│                                         │
│  与"蟒蛇"的意思无关！                   │
│  （虽然 Python 的 logo 是两条蛇）         │
│                                         │
└─────────────────────────────────────────┘
```

---

## Python 的特点

```
┌─────────────────────────────────────────┐
│          Python 主要特点                 │
├─────────────────────────────────────────┤
│                                         │
│  📖 简洁易读                            │
│     语法接近英语，代码清晰易懂          │
│                                         │
│  🎯 开源免费                            │
│     完全免费使用，社区活跃              │
│                                         │
│  🔄 跨平台                              │
│     Windows、Mac、Linux 都能运行        │
│                                         │
│  📦 丰富的库                            │
│     大量现成的代码可以使用              │
│                                         │
│  🌍 多用途                              │
│     Web、数据分析、AI、自动化等         │
│                                         │
└─────────────────────────────────────────┘
```

---

## Python 能做什么

### 应用领域

```
┌─────────────────────────────────────────┐
│         Python 应用领域                 │
├─────────────────────────────────────────┤
│                                         │
│  🌐 Web 开发                             │
│     网站、Web 应用、API 接口             │
│     常用框架：Django, Flask, FastAPI   │
│                                         │
│  📊 数据分析                            │
│     数据处理、统计分析、可视化          │
│     用库：Pandas, NumPy, Matplotlib  │
│                                         │
│  🤖 人工智能                            │
│     机器学习、深度学习、神经网络        │
│     常用库：TensorFlow, PyTorch        │
│                                         │
│  🤖 自动化脚本                          │
│     文件处理、定时任务、网络爬虫        │
│     常用库：Requests, BeautifulSoup    │
│                                         │
│  🎮 游戏开发                            │
│     2D 游戏、游戏原型                   │
│     常用库：Pygame                      │
│                                         │
│  🔬 科学计算                            │
│     物理模拟、生物信息、金融量化        │
│     常用库：SciPy, SymPy               │
│                                         │
└─────────────────────────────────────────┘
```

### 知名公司和项目

```python
# 使用 Python 的知名公司/项目

"""
Google
  - YouTube 的后端大量使用 Python
  - Google 搜索的部分功能

Instagram
  - 最初完全用 Django（Python 框架）构建

Netflix
  - 推荐算法使用 Python
  - 内容分析系统

NASA
  - 科学计算和数据处理

Dropbox
  - 创始人就是 Python 的作者 Guido
"""
```

---

## Python 版本选择

### 版本历史

```
┌─────────────────────────────────────────┐
│          Python 版本时间线               │
├─────────────────────────────────────────┤
│                                         │
│  1991 年  - Python 1.0 发布             │
│  2000 年  - Python 2.0 发布             │
│  2008 年  - Python 3.0 发布             │
│  2020 年  - Python 2 停止维护 ⚠️        │
│                                         │
│  📌 当前最新稳定版：Python 3.12+        │
│                                         │
└─────────────────────────────────────────┘
```

### Python 2 vs Python 3

```
┌─────────────────┬───────────┬───────────┐
│      特性       │  Python 2 │  Python 3 │
├─────────────────┼───────────┼───────────┤
│  print 语句     │ print "x" │ print("x")│
│  整数除法       │ 5/2 = 2   │ 5/2 = 2.5 │
│  字符串编码     │ ASCII     │ Unicode   │
│  维护状态       │ 已停止    │ 活跃维护  │
│  推荐使用       │ ❌ 不要学 │ ✅ 学这个 │
└─────────────────┴───────────┴───────────┘
```

### 学习建议

```
┌─────────────────────────────────────────┐
│              ⭐ 重要提示 ⭐               │
├─────────────────────────────────────────┤
│                                         │
│  一定要学习 Python 3！                   │
│                                         │
│  Python 2 已在 2020 年停止维护，         │
│  所有新库和新功能都只支持 Python 3。     │
│                                         │
│  本教程全部基于 Python 3.11+！           │
│                                         │
└─────────────────────────────────────────┘
```

---

### L1 理解层：会用

## Python 的最简体验

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

**关键代码说明：**

| 代码 | 含义 | 为什么这样写 |
|------|------|-------------|
| `pathlib.Path(source_dir)` | 将字符串路径转为 Path 对象 | Path 对象支持 `/` 拼接和 `.glob()` 等方法 |
| `source.glob("*.*")` | 匹配目录下所有带扩展名的文件 | `*.*` 表示"名字任意.扩展名任意" |
| `file.suffix.lower()` | 获取文件扩展名并转小写 | 统一大小写，避免 `.JPG` 和 `.jpg` 被分开统计 |
| `ext.replace(".", "")` | 去掉扩展名中的点 | 把 `.txt` 变成 `txt`，用作文件夹名 |
| `target_dir.mkdir(exist_ok=True)` | 创建目录，已存在不报错 | 多个同类型文件时只创建一次目录 |
| `file.rename(target_dir / file.name)` | 将文件移动到目标目录 | `Path / name` 用 `/` 拼接路径，等同于 `os.path.join` |
| `stats.get(ext, 0) + 1` | 读取当前计数，默认 0，再加 1 | 字典中不存在该键时返回默认值 0，避免 KeyError |

---

### L2 实践层：用好

#### 推荐做法

| 做法 | 原因 | 示例 |
|------|------|------|
| 学习选择 Python 3.11+ | 3.11 是主流稳定版本，3.12+ 引入新语法特性 | `uv python install 3.11` |
| 初学用 VSCode 作为编辑器 | 轻量、免费、扩展生态丰富，一个编辑器搞定多种语言 | 安装 Python + Pylance 扩展 |
| 专业开发用 PyCharm | 重构、调试、数据库工具集成更强大，Python 专项优化 | PyCharm Professional |
| 使用 uv 管理 Python 版本 | 统一工具链，比 pip 快 10-100 倍，自动管理虚拟环境 | `uv python install 3.11` |

#### 反模式：不要这样做

```python
# ❌ 错误做法：学习 Python 2
# Python 2 已于 2020 年停止维护，语法落后，社区不再支持
# 所有新库（Pandas 2.0+、FastAPI 等）只支持 Python 3

# ❌ 错误做法：用记事本写 Python 代码
# 没有语法高亮、自动补全、错误提示，效率极低
# 缩进错误难以发现，调试无从下手
```

```python
# ✅ 正确做法
# 使用 Python 3.11+，配合 VSCode 或 PyCharm
# 享受语法高亮、代码补全、调试等现代开发体验
```

#### 适用场景

| 场景 | 是否推荐 | 原因 |
|------|---------|------|
| 零基础入门 Python | ✅ Python 3.11+ | 语法现代，教程和社区资源丰富 |
| 学习数据分析 | ✅ Python 3 + Jupyter | 交互式探索数据，即时反馈 |
| 学习 Web 开发 | ✅ Python 3 + FastAPI | 现代框架，性能优秀 |
| 维护旧项目 | ⚠️ 确认项目 Python 版本 | 旧项目可能使用 Python 2，需评估迁移成本 |
| 多语言开发（前端+后端）| ✅ VSCode | 一个编辑器支持所有语言 |
| 纯 Python 专业开发 | ✅ PyCharm | Python 专项优化，功能更深度 |

---

## 本章小结

```
┌─────────────────────────────────────────────────────────────┐
│                      Python 简介 知识要点                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   Python 特点：                                              │
│   ✓ 简洁易读、开源免费、跨平台                              │
│   ✓ 丰富的库、多用途                                        │
│                                                             │
│   应用领域：                                                 │
│   ✓ Web 开发、数据分析、人工智能                            │
│   ✓ 自动化脚本、游戏开发、科学计算                          │
│                                                             │
│   版本选择：                                                 │
│   ✓ 选择 Python 3.11+                                       │
│   ✓ Python 2 已停止维护                                     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```
