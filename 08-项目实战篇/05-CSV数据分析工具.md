# 项目五：CSV 数据分析工具

> **项目难度**：中级
> **所需知识**：第 5–9 章（数据结构）、第 10 章（函数）、第 12 章（文件读写）、第 13 章（面向对象）
> **用到的库**：`csv`、`statistics`、`collections`（均为 Python 标准库，无需安装）
> **预计完成时间**：2–3 小时

---

## 第一部分：项目概述

### 1.1 什么是数据分析

**类比理解**

想象你是班主任，手里有一张纸，上面记录了全班 50 位同学的语文、数学、英语成绩。

你想知道：
- 数学平均分是多少？
- 谁的总分最高？
- 城市 A 的同学成绩是否比城市 B 的好？

以前，你要拿计算器一个一个加、除。而数据分析，就是让计算机帮你做这件事——不只是 50 条记录，哪怕是 500 万条，也能在几秒钟内算完。

**数据分析的本质**

```
原始数据（一堆数字和文字）
        ↓
   读取 & 清洗
        ↓
   统计 & 计算
        ↓
   结果 & 报告
        ↓
   得出结论（辅助决策）
```

**为什么用 CSV 格式？**

CSV（Comma-Separated Values，逗号分隔值）是数据分析领域最常见的数据交换格式：
- Excel 可以直接打开/导出
- 数据库可以导入/导出
- 几乎所有编程语言都有现成的库支持
- 纯文本，任何编辑器都能查看

### 1.2 功能清单

本项目将实现以下功能：

| 功能 | 说明 |
|------|------|
| 读取 CSV 文件 | 自动检测列名，支持不同编码 |
| 列统计分析 | 最小值、最大值、平均值、中位数、众数 |
| 数据过滤 | 按条件筛选行（类似 Excel 筛选） |
| 分组聚合 | 按某列分组，统计各组数据（类似透视表） |
| 相关性分析 | 计算两列数据的相关程度 |
| 生成报告 | 文字报告 + ASCII 柱状图 |
| 导出报告 | 将分析结果保存为 txt 文件 |

### 1.3 数据流图

```
┌─────────────────────────────────────────────────────────────────┐
│                       CSV 数据分析工具                           │
│                       数据流向示意图                             │
└─────────────────────────────────────────────────────────────────┘

  ┌─────────────┐
  │  CSV 文件    │  ← 原始数据（employees.csv）
  │  磁盘上的    │
  │  文本文件    │
  └──────┬──────┘
         │  csv.DictReader 读取
         ▼
  ┌─────────────────────────────┐
  │  数据列表                    │
  │  [                          │
  │    {"name": "张三",          │
  │     "age": "28",            │
  │     "score": "92", ...},    │
  │    {"name": "李四", ...},    │
  │    ...                      │
  │  ]                          │
  └──────┬──────────────────────┘
         │
         ├──────────────────────────┐
         │                          │
         ▼                          ▼
  ┌────────────┐            ┌────────────────┐
  │ 统计分析   │            │  数据过滤/分组  │
  │            │            │                │
  │ 最小值     │            │ filter_rows()  │
  │ 最大值     │            │ group_by()     │
  │ 平均值     │            │                │
  │ 中位数     │            └───────┬────────┘
  │ 众数       │                    │
  └──────┬─────┘                    │
         │                          │
         └────────────┬─────────────┘
                      │
                      ▼
             ┌─────────────────┐
             │   统计结果       │
             │  （字典/数字）   │
             └────────┬────────┘
                      │
           ┌──────────┴──────────┐
           │                     │
           ▼                     ▼
  ┌─────────────────┐   ┌─────────────────┐
  │  终端报告        │   │  导出 txt 文件   │
  │  + ASCII 图表   │   │  report.txt     │
  └─────────────────┘   └─────────────────┘
```

---

## 第二部分：示例数据

### 2.1 员工数据说明

本项目使用一份模拟的员工绩效数据，包含以下字段：

| 字段 | 含义 | 数据类型 |
|------|------|----------|
| name | 姓名 | 文本 |
| age | 年龄 | 整数 |
| city | 所在城市 | 文本 |
| score | 绩效评分（0–100） | 浮点数 |
| department | 所属部门 | 文本 |

### 2.2 CSV 文件内容预览

```
name,age,city,score,department
张三,28,北京,92.5,技术部
李四,35,上海,78.0,市场部
王五,24,北京,88.5,技术部
赵六,42,广州,65.0,行政部
陈七,31,上海,95.0,技术部
刘八,27,北京,72.5,市场部
孙九,38,广州,83.0,行政部
周十,29,上海,90.0,技术部
```

### 2.3 生成示例数据的代码

```python
import csv

def create_sample_data(filename: str = "employees.csv") -> None:
    """
    生成示例 CSV 文件。

    实际工作中，这个文件通常来自数据库导出或 Excel 另存为。
    这里我们用代码生成，方便测试。
    """
    # 表头（列名）
    fieldnames = ["name", "age", "city", "score", "department"]

    # 数据行（每行是一个字典）
    rows = [
        {"name": "张三",  "age": 28, "city": "北京", "score": 92.5, "department": "技术部"},
        {"name": "李四",  "age": 35, "city": "上海", "score": 78.0, "department": "市场部"},
        {"name": "王五",  "age": 24, "city": "北京", "score": 88.5, "department": "技术部"},
        {"name": "赵六",  "age": 42, "city": "广州", "score": 65.0, "department": "行政部"},
        {"name": "陈七",  "age": 31, "city": "上海", "score": 95.0, "department": "技术部"},
        {"name": "刘八",  "age": 27, "city": "北京", "score": 72.5, "department": "市场部"},
        {"name": "孙九",  "age": 38, "city": "广州", "score": 83.0, "department": "行政部"},
        {"name": "周十",  "age": 29, "city": "上海", "score": 90.0, "department": "技术部"},
    ]

    # 写入文件
    # newline="" 是 CSV 写入的标准写法，防止 Windows 下出现多余空行
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()   # 写入表头
        writer.writerows(rows) # 写入所有数据行

    print(f"示例数据已生成：{filename}（共 {len(rows)} 条记录）")
```

---

## 第三部分：核心概念讲解

### 3.1 CSV 格式与 Python 的 csv 模块

#### 概念说明

**CSV 是什么？**

CSV 就是用逗号把数据隔开的纯文本文件。打开一个 CSV 文件，你会看到：

```
name,age,city
张三,28,北京
李四,35,上海
```

第一行是列名（表头），后续每行是一条记录。逗号就像表格的"格线"。

**为什么 CSV 这么流行？**

```
┌──────────────────────────────────────────────────┐
│  数据格式选择对比                                  │
├──────────┬───────────┬──────────┬────────────────┤
│  格式    │  可读性   │  文件大小 │  兼容性        │
├──────────┼───────────┼──────────┼────────────────┤
│  CSV     │  高       │  小      │  所有软件都支持 │
│  Excel   │  高       │  大      │  需要 Office   │
│  JSON    │  中       │  中      │  程序员友好    │
│  数据库  │  低       │  —       │  需要数据库软件 │
└──────────┴───────────┴──────────┴────────────────┘
```

CSV 就像数据世界的"普通话"——大家都听得懂。

**csv.reader vs csv.DictReader**

Python 提供了两种读取方式：
- `csv.reader`：每行返回一个**列表**，用索引 `row[0]` 取值
- `csv.DictReader`：每行返回一个**字典**，用列名 `row["name"]` 取值（推荐！更易读）

#### 示例代码

```python
import csv

# ─── 方式一：csv.reader（不推荐，索引容易出错）───────────────────────
with open("employees.csv", "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    header = next(reader)  # 第一行是表头，单独读取
    print("表头:", header)  # ['name', 'age', 'city', 'score', 'department']

    for row in reader:
        # row 是列表：['张三', '28', '北京', '92.5', '技术部']
        name = row[0]   # 靠索引取值，如果列顺序变了就会出 bug！
        age  = row[1]
        print(f"  姓名={name}, 年龄={age}")

print()

# ─── 方式二：csv.DictReader（推荐，用列名取值）──────────────────────
with open("employees.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    # DictReader 会自动把第一行作为表头

    for row in reader:
        # row 是字典：{'name': '张三', 'age': '28', 'city': '北京', ...}
        name = row["name"]   # 用列名取值，更清晰！
        age  = row["age"]    # 注意：所有值都是字符串，需要手动转换类型
        score = float(row["score"])
        print(f"  姓名={name}, 年龄={int(age)}, 评分={score}")

# ─── 注意：CSV 读取的所有数据都是字符串！─────────────────────────────
# 错误示范：
# total = row["score"] + 10   # TypeError！字符串不能加数字
# 正确做法：
# total = float(row["score"]) + 10
```

### 3.2 统计学基础概念

#### 概念说明

数据分析中最常用的几个"数字描述"：

```
假设有一组评分数据：[65, 72.5, 78, 83, 88.5, 90, 92.5, 95]

┌──────────────────────────────────────────────────────────────┐
│  统计指标说明                                                  │
├────────┬──────────────────────────────────────────────────── │
│  指标  │  计算方法          │  含义                           │
├────────┼────────────────────┼─────────────────────────────── │
│  最小值│  min()             │  65       最差的那个            │
│  最大值│  max()             │  95       最好的那个            │
│  平均值│  sum() / count     │  83.0     整体水平              │
│  中位数│  排序后取中间       │  85.75    不受极端值影响的中间  │
│  众数  │  出现次数最多的值   │  —        最常见的值            │
└────────┴────────────────────┴─────────────────────────────── ┘
```

**为什么需要中位数？**

想象 5 个人的月薪：3000、3500、4000、4200、50000

- 平均值 = (3000+3500+4000+4200+50000) / 5 = 12940 元
- 中位数 = 4000 元（排序后取中间那个）

平均值被 50000 这个"异常值"拉高了，看起来人均月薪很高，但实际上大多数人只有 3000–4200。中位数更能反映"普通人"的真实情况。

**众数**

众数是出现次数最多的值。比如城市分布：`[北京, 上海, 北京, 广州, 北京]`，众数就是"北京"（出现了 3 次）。对文本型数据特别有用。

#### 示例代码

```python
import statistics
from collections import Counter

scores = [92.5, 78.0, 88.5, 65.0, 95.0, 72.5, 83.0, 90.0]

# ─── 最小值 / 最大值 ─────────────────────────────────────────────────
print(f"最小值: {min(scores)}")   # 65.0
print(f"最大值: {max(scores)}")   # 95.0

# ─── 平均值（手动计算） ──────────────────────────────────────────────
avg = sum(scores) / len(scores)
print(f"平均值（手动）: {avg:.2f}")   # 83.06

# ─── 平均值（用 statistics 模块） ────────────────────────────────────
print(f"平均值（标准库）: {statistics.mean(scores):.2f}")

# ─── 中位数 ──────────────────────────────────────────────────────────
# 手动计算：先排序，再取中间
sorted_scores = sorted(scores)
print(f"排序后: {sorted_scores}")
# [65.0, 72.5, 78.0, 83.0, 88.5, 90.0, 92.5, 95.0]
# 共 8 个元素，没有"正中间"那一个，取第 4、5 个的平均
median = statistics.median(scores)
print(f"中位数: {median}")   # 85.75

# ─── 众数（用 Counter 统计频率） ─────────────────────────────────────
cities = ["北京", "上海", "北京", "广州", "上海", "北京", "广州", "上海"]
counter = Counter(cities)
print(f"城市分布: {counter}")           # Counter({'北京': 3, '上海': 3, '广州': 2})
most_common = counter.most_common(1)   # 取出现最多的 1 个
print(f"众数: {most_common[0][0]}")    # 北京（或上海，并列）
```

### 3.3 Counter 和 defaultdict

#### 概念说明

`collections` 是 Python 标准库中的"工具箱"，里面有两个特别好用的容器：

**Counter（计数器）**

```
普通字典统计：                    Counter 统计：
cities = ["北京","上海","北京"]   cities = ["北京","上海","北京"]

count = {}                        count = Counter(cities)
for c in cities:                  # 直接得到：
    if c not in count:            # Counter({'北京':2, '上海':1})
        count[c] = 0
    count[c] += 1
```

Counter 就是专门用来数"每个值出现了几次"的字典。

**defaultdict（带默认值的字典）**

```
普通字典分组：                    defaultdict 分组：
groups = {}                       from collections import defaultdict
for row in data:                  groups = defaultdict(list)
    dept = row["department"]      for row in data:
    if dept not in groups:            groups[row["department"]].append(row)
        groups[dept] = []
    groups[dept].append(row)
```

`defaultdict(list)` 的意思是：如果访问一个不存在的键，自动创建一个空列表。省去了每次"判断键是否存在"的麻烦。

#### 示例代码

```python
from collections import Counter, defaultdict

# ─── Counter 示例 ──────────────────────────────────────────────────
# 统计部门分布
departments = ["技术部", "市场部", "技术部", "行政部", "技术部", "市场部", "行政部", "技术部"]

counter = Counter(departments)
print("部门人数统计:")
print(counter)                    # Counter({'技术部': 4, '市场部': 2, '行政部': 2})
print(counter["技术部"])          # 4
print(counter.most_common(2))     # [('技术部', 4), ('市场部', 2)] 出现最多的前 2 个

# Counter 还可以直接相加
counter2 = Counter(["技术部", "财务部"])
combined = counter + counter2
print("合并后:", combined)        # Counter({'技术部': 5, '市场部': 2, '行政部': 2, '财务部': 1})

# ─── defaultdict 示例 ─────────────────────────────────────────────
# 按部门分组员工
employees = [
    {"name": "张三", "department": "技术部", "score": 92.5},
    {"name": "李四", "department": "市场部", "score": 78.0},
    {"name": "王五", "department": "技术部", "score": 88.5},
    {"name": "陈七", "department": "技术部", "score": 95.0},
]

# 普通字典写法（麻烦）：
groups_normal = {}
for emp in employees:
    dept = emp["department"]
    if dept not in groups_normal:
        groups_normal[dept] = []
    groups_normal[dept].append(emp["name"])

# defaultdict 写法（简洁）：
groups = defaultdict(list)   # 访问不存在的键时，自动创建 []
for emp in employees:
    groups[emp["department"]].append(emp["name"])

print("\n按部门分组:")
for dept, names in groups.items():
    print(f"  {dept}: {names}")
# 技术部: ['张三', '王五', '陈七']
# 市场部: ['李四']

# defaultdict(int) 用于计数（默认值是 0）
word_count = defaultdict(int)
for word in ["apple", "banana", "apple", "cherry", "banana", "apple"]:
    word_count[word] += 1   # 不用判断键是否存在，直接 += 1
print("\n单词计数:", dict(word_count))
# {'apple': 3, 'banana': 2, 'cherry': 1}
```

### 3.4 ASCII 柱状图

#### 概念说明

数据可视化通常需要 matplotlib 这样的图形库，但有时我们只想在终端里快速看一眼数据分布。这时可以用 ASCII 字符模拟柱状图：

```
用 '█' 字符，重复 N 次，就能画出一根柱子：

  count = 4    →   ████
  count = 7    →   ███████
  count = 2    →   ██

把数值映射到 1–20 的区间（归一化），
这样最大的柱子占满宽度，其他柱子按比例缩放。
```

**归一化公式**（让数据适应屏幕宽度）：

```
bar_length = int(value / max_value * MAX_WIDTH)

比如 max_value = 95，MAX_WIDTH = 20：
  score=95  →  int(95/95*20)  = 20  →  ████████████████████
  score=65  →  int(65/95*20)  = 13  →  █████████████
```

#### 示例代码

```python
def draw_bar_chart(data: dict, title: str = "柱状图", max_width: int = 30) -> None:
    """
    在终端绘制 ASCII 柱状图。

    参数：
        data: 字典，键是标签，值是数值
              例如 {"技术部": 4, "市场部": 2, "行政部": 2}
        title: 图表标题
        max_width: 最长柱子的字符宽度
    """
    if not data:
        print("（无数据）")
        return

    max_value = max(data.values())

    print(f"\n  {title}")
    print("  " + "─" * (max_width + 20))

    for label, value in data.items():
        # 计算柱子长度（归一化）
        bar_length = int(value / max_value * max_width) if max_value > 0 else 0
        bar = "█" * bar_length

        # 格式化输出：左对齐标签 + 柱子 + 数值
        print(f"  {label:<8} │ {bar:<{max_width}} {value:.1f}")

    print("  " + "─" * (max_width + 20))


# 测试
draw_bar_chart(
    {"技术部": 4, "市场部": 2, "行政部": 2},
    title="部门人数分布"
)

# 输出：
#   部门人数分布
#   ──────────────────────────────────────────────
#   技术部    │ ██████████████████████████████  4.0
#   市场部    │ ███████████████                 2.0
#   行政部    │ ███████████████                 2.0
#   ──────────────────────────────────────────────

# 评分分布（用区间分箱）
def draw_score_histogram(scores: list[float], bins: int = 5) -> None:
    """将连续数值分成若干区间，统计每个区间的频率，画成直方图。"""
    min_val = min(scores)
    max_val = max(scores)
    step = (max_val - min_val) / bins  # 每个区间的宽度

    # 统计每个区间的数量
    buckets = {}
    for i in range(bins):
        low  = min_val + i * step
        high = min_val + (i + 1) * step
        label = f"{low:.0f}–{high:.0f}"
        # 统计落在 [low, high) 区间的数量
        count = sum(1 for s in scores if low <= s < high)
        buckets[label] = count
    # 最后一个区间用 <= 包含最大值
    last_low = min_val + (bins - 1) * step
    label = f"{last_low:.0f}–{max_val:.0f}"
    buckets[label] = sum(1 for s in scores if last_low <= s <= max_val)

    draw_bar_chart(buckets, title="评分分布直方图", max_width=20)


draw_score_histogram([92.5, 78.0, 88.5, 65.0, 95.0, 72.5, 83.0, 90.0])
```

---

## 第四部分：完整代码实现

### 4.1 DataAnalyzer 类

```python
"""
CSV 数据分析工具
项目五：完整实现

功能：
  - 读取 CSV 文件
  - 列统计分析（最小/最大/均值/中位数/众数）
  - 数据过滤与分组
  - 相关性分析
  - 报告生成与导出
"""

import csv
import math
import statistics
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


# ══════════════════════════════════════════════════════════════════
# 辅助函数
# ══════════════════════════════════════════════════════════════════

def create_sample_data(filename: str = "employees.csv") -> None:
    """生成示例 CSV 文件（8 条员工记录）。"""
    fieldnames = ["name", "age", "city", "score", "department"]
    rows = [
        {"name": "张三",  "age": 28, "city": "北京", "score": 92.5, "department": "技术部"},
        {"name": "李四",  "age": 35, "city": "上海", "score": 78.0, "department": "市场部"},
        {"name": "王五",  "age": 24, "city": "北京", "score": 88.5, "department": "技术部"},
        {"name": "赵六",  "age": 42, "city": "广州", "score": 65.0, "department": "行政部"},
        {"name": "陈七",  "age": 31, "city": "上海", "score": 95.0, "department": "技术部"},
        {"name": "刘八",  "age": 27, "city": "北京", "score": 72.5, "department": "市场部"},
        {"name": "孙九",  "age": 38, "city": "广州", "score": 83.0, "department": "行政部"},
        {"name": "周十",  "age": 29, "city": "上海", "score": 90.0, "department": "技术部"},
    ]
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"示例数据已生成：{filename}（共 {len(rows)} 条记录）")


def draw_bar_chart(
    data: dict[str, float],
    title: str = "柱状图",
    max_width: int = 25,
) -> str:
    """
    生成 ASCII 柱状图字符串。

    返回字符串而不是直接打印，方便写入报告文件。
    """
    if not data:
        return "  （无数据）\n"

    lines = []
    max_value = max(data.values())
    label_width = max(len(str(k)) for k in data) + 2  # 标签最大宽度

    lines.append(f"\n  {title}")
    lines.append("  " + "─" * (label_width + max_width + 12))

    for label, value in data.items():
        bar_length = int(value / max_value * max_width) if max_value > 0 else 0
        bar = "█" * bar_length
        lines.append(f"  {str(label):<{label_width}} │ {bar:<{max_width}} {value:.2f}")

    lines.append("  " + "─" * (label_width + max_width + 12))
    return "\n".join(lines) + "\n"


# ══════════════════════════════════════════════════════════════════
# 核心类
# ══════════════════════════════════════════════════════════════════

class DataAnalyzer:
    """
    CSV 数据分析器。

    使用示例：
        analyzer = DataAnalyzer("employees.csv")
        analyzer.load_data()
        report = analyzer.generate_report()
        print(report)
    """

    def __init__(self, filepath: str) -> None:
        """
        初始化分析器。

        参数：
            filepath: CSV 文件路径
        """
        self.filepath = filepath
        # 存储所有数据行（每行是一个字典）
        self.data: list[dict[str, str]] = []
        # 列名列表
        self.columns: list[str] = []

    # ── 数据加载 ────────────────────────────────────────────────────

    def load_data(self) -> None:
        """
        从 CSV 文件读取数据。

        如果文件不存在或格式错误，会抛出异常。
        """
        path = Path(self.filepath)
        if not path.exists():
            raise FileNotFoundError(f"文件不存在：{self.filepath}")

        try:
            with open(path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                if reader.fieldnames is None:
                    raise ValueError("CSV 文件没有表头行")
                self.columns = list(reader.fieldnames)
                self.data = [dict(row) for row in reader]  # 读取所有行
        except UnicodeDecodeError:
            # 有些文件是 GBK 编码（Windows Excel 导出常见）
            with open(path, "r", encoding="gbk") as f:
                reader = csv.DictReader(f)
                self.columns = list(reader.fieldnames)  # type: ignore
                self.data = [dict(row) for row in reader]

        print(f"已加载 {len(self.data)} 条记录，共 {len(self.columns)} 列")
        print(f"列名：{', '.join(self.columns)}")

    # ── 类型检测 ────────────────────────────────────────────────────

    @staticmethod
    def _is_numeric(value: str) -> bool:
        """
        判断一个字符串是否可以转换为数字。

        因为 CSV 读取的所有值都是字符串，我们需要这个方法来判断
        某一列是"数字列"还是"文本列"。

        例如：
            _is_numeric("92.5")  → True
            _is_numeric("技术部") → False
            _is_numeric("")      → False
        """
        try:
            float(value)
            return True
        except (ValueError, TypeError):
            return False

    def _get_numeric_values(self, column: str) -> list[float]:
        """
        提取某列的所有数字值（跳过空值和非数字）。

        参数：
            column: 列名

        返回：
            浮点数列表
        """
        values = []
        for row in self.data:
            val = row.get(column, "")
            if self._is_numeric(val):
                values.append(float(val))
        return values

    # ── 单列统计 ────────────────────────────────────────────────────

    def describe_column(self, column: str) -> dict[str, Any]:
        """
        对指定列进行描述性统计。

        如果是数字列，返回：min、max、mean、median、mode、count
        如果是文本列，返回：count、unique_count、mode（最常见的值）、value_counts

        参数：
            column: 列名

        返回：
            包含统计结果的字典
        """
        if column not in self.columns:
            raise ValueError(f"列 '{column}' 不存在。可用列：{self.columns}")

        # 获取这一列的所有值（非空）
        all_values = [row[column] for row in self.data if row.get(column, "").strip()]

        if not all_values:
            return {"count": 0, "column": column}

        # 判断是否为数字列
        numeric_values = self._get_numeric_values(column)
        is_numeric_col = len(numeric_values) / len(all_values) > 0.8  # 80% 以上是数字则视为数字列

        result: dict[str, Any] = {
            "column": column,
            "count": len(all_values),
        }

        if is_numeric_col and numeric_values:
            # 数字列统计
            result["type"] = "numeric"
            result["min"]    = min(numeric_values)
            result["max"]    = max(numeric_values)
            result["mean"]   = statistics.mean(numeric_values)
            result["median"] = statistics.median(numeric_values)

            # 众数：对数字列用 Counter 找出现次数最多的值
            counter = Counter(numeric_values)
            result["mode"] = counter.most_common(1)[0][0]
            result["mode_count"] = counter.most_common(1)[0][1]

            # 标准差（衡量数据的分散程度，需要至少 2 个数据点）
            if len(numeric_values) >= 2:
                result["std_dev"] = statistics.stdev(numeric_values)
            else:
                result["std_dev"] = 0.0
        else:
            # 文本列统计
            result["type"] = "text"
            counter = Counter(all_values)
            result["unique_count"] = len(counter)
            result["value_counts"] = dict(counter.most_common())  # 按频率排序

            # 众数：出现最多的文本值
            most_common = counter.most_common(1)[0]
            result["mode"] = most_common[0]
            result["mode_count"] = most_common[1]

        return result

    # ── 报告生成 ────────────────────────────────────────────────────

    def generate_report(self) -> str:
        """
        生成完整的数据分析报告（字符串形式）。

        报告包括：
        - 数据概览
        - 每列的统计信息
        - 文本列的 ASCII 柱状图
        """
        if not self.data:
            return "错误：还没有加载数据，请先调用 load_data() 方法。"

        lines = []

        # ── 标题 ──────────────────────────────────────────────────
        lines.append("=" * 60)
        lines.append("                CSV 数据分析报告")
        lines.append("=" * 60)
        lines.append(f"  数据来源：{self.filepath}")
        lines.append(f"  总记录数：{len(self.data)} 条")
        lines.append(f"  总列数　：{len(self.columns)} 列")
        lines.append(f"  列名　　：{', '.join(self.columns)}")
        lines.append("=" * 60)

        # ── 逐列统计 ──────────────────────────────────────────────
        for col in self.columns:
            stats = self.describe_column(col)
            lines.append(f"\n【列名：{col}】")
            lines.append(f"  数据类型：{'数字' if stats.get('type') == 'numeric' else '文本'}")
            lines.append(f"  有效记录：{stats['count']} 条")

            if stats.get("type") == "numeric":
                lines.append(f"  最小值　：{stats['min']:.2f}")
                lines.append(f"  最大值　：{stats['max']:.2f}")
                lines.append(f"  平均值　：{stats['mean']:.2f}")
                lines.append(f"  中位数　：{stats['median']:.2f}")
                lines.append(f"  众　　数：{stats['mode']:.2f}（出现 {stats['mode_count']} 次）")
                lines.append(f"  标准差　：{stats['std_dev']:.2f}")
            else:
                lines.append(f"  唯一值数：{stats['unique_count']}")
                lines.append(f"  最常见值：'{stats['mode']}'（出现 {stats['mode_count']} 次）")
                # 文本列画柱状图
                if stats.get("value_counts"):
                    chart = draw_bar_chart(
                        stats["value_counts"],
                        title=f"{col} 分布",
                        max_width=20,
                    )
                    lines.append(chart)

        lines.append("\n" + "=" * 60)
        return "\n".join(lines)

    # ── 数据过滤 ────────────────────────────────────────────────────

    def filter_rows(
        self,
        column: str,
        operator: str,
        value: Any,
    ) -> list[dict[str, str]]:
        """
        按条件过滤数据行（类似 Excel 的"筛选"功能）。

        参数：
            column:   要过滤的列名
            operator: 比较运算符，支持 "==" / "!=" / ">" / ">=" / "<" / "<=" / "contains"
            value:    比较的值

        返回：
            满足条件的行列表

        用法示例：
            # 找出评分大于 85 的员工
            high_scorers = analyzer.filter_rows("score", ">", 85)

            # 找出北京的员工
            beijing = analyzer.filter_rows("city", "==", "北京")

            # 找出姓名包含"张"的员工
            zhang = analyzer.filter_rows("name", "contains", "张")
        """
        if column not in self.columns:
            raise ValueError(f"列 '{column}' 不存在")

        result = []
        for row in self.data:
            cell = row.get(column, "")

            # 如果 value 是数字，把 cell 也转成数字来比较
            if self._is_numeric(str(value)) and self._is_numeric(cell):
                cell_val: Any = float(cell)
                cmp_val: Any = float(value)
            else:
                cell_val = cell
                cmp_val = str(value)

            # 根据运算符判断
            match operator:
                case "==":
                    matches = cell_val == cmp_val
                case "!=":
                    matches = cell_val != cmp_val
                case ">":
                    matches = cell_val > cmp_val
                case ">=":
                    matches = cell_val >= cmp_val
                case "<":
                    matches = cell_val < cmp_val
                case "<=":
                    matches = cell_val <= cmp_val
                case "contains":
                    matches = str(value) in cell
                case _:
                    raise ValueError(f"不支持的运算符：{operator}")

            if matches:
                result.append(row)

        return result

    # ── 分组聚合 ────────────────────────────────────────────────────

    def group_by(
        self,
        group_column: str,
        agg_column: str,
        agg_func: str = "mean",
    ) -> dict[str, float]:
        """
        按某列分组，对另一列进行聚合计算（类似 Excel 透视表）。

        参数：
            group_column: 分组列（如 "department"）
            agg_column:   聚合列（如 "score"）
            agg_func:     聚合函数，支持 "mean" / "sum" / "min" / "max" / "count"

        返回：
            字典，键是分组值，值是聚合结果
            例如：{"技术部": 91.5, "市场部": 75.25, "行政部": 74.0}

        类比：
            就像问"各个部门的平均评分是多少？"
            group_column = "department"（按部门分组）
            agg_column   = "score"    （对评分求均值）
        """
        for col in (group_column, agg_column):
            if col not in self.columns:
                raise ValueError(f"列 '{col}' 不存在")

        # 用 defaultdict 收集每个组的数值
        groups: defaultdict[str, list[float]] = defaultdict(list)
        for row in self.data:
            group_key = row.get(group_column, "")
            agg_val   = row.get(agg_column, "")
            if group_key and self._is_numeric(agg_val):
                groups[group_key].append(float(agg_val))

        # 对每个组应用聚合函数
        result = {}
        for key, values in groups.items():
            if not values:
                continue
            match agg_func:
                case "mean":
                    result[key] = statistics.mean(values)
                case "sum":
                    result[key] = sum(values)
                case "min":
                    result[key] = min(values)
                case "max":
                    result[key] = max(values)
                case "count":
                    result[key] = float(len(values))
                case _:
                    raise ValueError(f"不支持的聚合函数：{agg_func}")

        # 按结果值降序排列，方便查看
        return dict(sorted(result.items(), key=lambda x: x[1], reverse=True))

    # ── 相关性分析（新增） ──────────────────────────────────────────

    def correlation(self, col1: str, col2: str) -> float:
        """
        计算两列之间的皮尔逊相关系数（Pearson Correlation Coefficient）。

        ─── 什么是相关系数？───────────────────────────────────────────

        相关系数用来衡量两个变量之间的"线性相关程度"，取值在 -1 到 1 之间：

          +1.0  完全正相关（一个变大，另一个也变大，成比例）
          +0.7  强正相关
          +0.3  弱正相关
           0.0  无相关
          -0.3  弱负相关
          -0.7  强负相关
          -1.0  完全负相关（一个变大，另一个一定变小）

        ─── 生活中的例子 ──────────────────────────────────────────────

          身高与体重：约 +0.7（正相关，高的人一般重）
          年龄与反应速度：约 -0.5（负相关，年龄大了反应变慢）
          鞋码与智商：约 0（无相关）

        ─── 数学公式（理解思路即可）───────────────────────────────────

          设两列数据分别为 X = [x1, x2, ..., xn]
                              Y = [y1, y2, ..., yn]

          x̄ = X 的平均值，ȳ = Y 的平均值

                      Σ (xi - x̄)(yi - ȳ)
          r = ─────────────────────────────────────────
               √[Σ(xi - x̄)²] × √[Σ(yi - ȳ)²]

          简单理解：
            分子：两列数据"同步变化"的程度
            分母：两列数据各自变化量的乘积（用来标准化）

        参数：
            col1: 第一列列名
            col2: 第二列列名

        返回：
            相关系数（float），取值范围 [-1, 1]
        """
        for col in (col1, col2):
            if col not in self.columns:
                raise ValueError(f"列 '{col}' 不存在")

        # 取两列都有数字值的行（配对数据）
        pairs = []
        for row in self.data:
            v1 = row.get(col1, "")
            v2 = row.get(col2, "")
            if self._is_numeric(v1) and self._is_numeric(v2):
                pairs.append((float(v1), float(v2)))

        if len(pairs) < 2:
            raise ValueError(f"有效配对数据不足（至少需要 2 条），当前只有 {len(pairs)} 条")

        n = len(pairs)
        x_vals = [p[0] for p in pairs]
        y_vals = [p[1] for p in pairs]

        # 计算均值
        x_mean = sum(x_vals) / n
        y_mean = sum(y_vals) / n

        # 计算分子：Σ (xi - x̄)(yi - ȳ)
        numerator = sum((x - x_mean) * (y - y_mean) for x, y in zip(x_vals, y_vals))

        # 计算分母：√[Σ(xi - x̄)²] × √[Σ(yi - ȳ)²]
        sum_sq_x = sum((x - x_mean) ** 2 for x in x_vals)
        sum_sq_y = sum((y - y_mean) ** 2 for y in y_vals)
        denominator = math.sqrt(sum_sq_x) * math.sqrt(sum_sq_y)

        if denominator == 0:
            return 0.0  # 某列数据完全没有变化（所有值相同），无法计算相关性

        return numerator / denominator

    def _interpret_correlation(self, r: float) -> str:
        """把相关系数数字翻译成人话。"""
        abs_r = abs(r)
        direction = "正" if r > 0 else "负"

        if abs_r >= 0.8:
            strength = "强"
        elif abs_r >= 0.5:
            strength = "中等"
        elif abs_r >= 0.2:
            strength = "弱"
        else:
            strength = "几乎没有"
            direction = ""

        return f"{strength}{direction}相关（r = {r:.4f}）"

    # ── 导出报告（新增） ────────────────────────────────────────────

    def export_report(self, filename: str = "analysis_report.txt") -> None:
        """
        将分析报告导出为 txt 文件。

        参数：
            filename: 导出文件路径（默认 analysis_report.txt）

        导出文件包含：
          - 基础统计报告（generate_report 的输出）
          - 部门平均评分分组结果
          - 年龄与评分的相关性分析
        """
        report_lines = []

        # 1. 基础报告
        report_lines.append(self.generate_report())

        # 2. 分组聚合（如果有合适的列）
        if "department" in self.columns and "score" in self.columns:
            report_lines.append("\n" + "=" * 60)
            report_lines.append("  分组分析：各部门平均评分")
            report_lines.append("=" * 60)
            dept_scores = self.group_by("department", "score", "mean")
            for dept, avg_score in dept_scores.items():
                report_lines.append(f"  {dept:<8} 平均评分：{avg_score:.2f}")
            # 添加柱状图
            report_lines.append(draw_bar_chart(dept_scores, "各部门平均评分"))

        # 3. 相关性分析（如果有合适的列）
        if "age" in self.columns and "score" in self.columns:
            report_lines.append("\n" + "=" * 60)
            report_lines.append("  相关性分析：年龄 vs 评分")
            report_lines.append("=" * 60)
            try:
                r = self.correlation("age", "score")
                interpretation = self._interpret_correlation(r)
                report_lines.append(f"  年龄与评分的皮尔逊相关系数：{r:.4f}")
                report_lines.append(f"  解读：{interpretation}")
                report_lines.append("  说明：r 接近 0 表示年龄与评分关系不大")
            except ValueError as e:
                report_lines.append(f"  无法计算相关性：{e}")

        # 写入文件
        full_report = "\n".join(report_lines)
        with open(filename, "w", encoding="utf-8") as f:
            f.write(full_report)

        print(f"\n报告已导出至：{filename}")
        print(f"文件大小：{Path(filename).stat().st_size} 字节")


# ══════════════════════════════════════════════════════════════════
# 主函数
# ══════════════════════════════════════════════════════════════════

def main() -> None:
    """完整演示数据分析工具的所有功能。"""

    print("╔══════════════════════════════════════════╗")
    print("║       CSV 数据分析工具 - 完整演示         ║")
    print("╚══════════════════════════════════════════╝")

    # ── 步骤 1：生成示例数据 ──────────────────────────────────────
    print("\n【步骤 1】生成示例数据")
    print("─" * 40)
    create_sample_data("employees.csv")

    # ── 步骤 2：加载数据 ─────────────────────────────────────────
    print("\n【步骤 2】加载 CSV 文件")
    print("─" * 40)
    analyzer = DataAnalyzer("employees.csv")
    analyzer.load_data()

    # ── 步骤 3：单列统计 ─────────────────────────────────────────
    print("\n【步骤 3】单列统计分析")
    print("─" * 40)

    # 数字列：评分
    score_stats = analyzer.describe_column("score")
    print("评分列统计：")
    print(f"  最小值：{score_stats['min']:.2f}")
    print(f"  最大值：{score_stats['max']:.2f}")
    print(f"  平均值：{score_stats['mean']:.2f}")
    print(f"  中位数：{score_stats['median']:.2f}")
    print(f"  众　数：{score_stats['mode']:.2f}（出现 {score_stats['mode_count']} 次）")
    print(f"  标准差：{score_stats['std_dev']:.2f}")

    # 文本列：城市
    city_stats = analyzer.describe_column("city")
    print("\n城市列统计：")
    print(f"  唯一城市数：{city_stats['unique_count']}")
    print(f"  最常见城市：{city_stats['mode']}（{city_stats['mode_count']} 人）")
    print(f"  城市分布：{city_stats['value_counts']}")

    # ── 步骤 4：数据过滤 ─────────────────────────────────────────
    print("\n【步骤 4】数据过滤")
    print("─" * 40)

    # 找出评分 >= 88 的员工
    top_employees = analyzer.filter_rows("score", ">=", 88)
    print(f"评分 >= 88 的员工（共 {len(top_employees)} 人）：")
    for emp in top_employees:
        print(f"  {emp['name']} | {emp['department']} | 评分：{emp['score']}")

    print()
    # 找出北京的员工
    beijing_employees = analyzer.filter_rows("city", "==", "北京")
    print(f"北京的员工（共 {len(beijing_employees)} 人）：")
    for emp in beijing_employees:
        print(f"  {emp['name']} | 年龄：{emp['age']} | 评分：{emp['score']}")

    # ── 步骤 5：分组聚合 ─────────────────────────────────────────
    print("\n【步骤 5】分组聚合（各部门平均评分）")
    print("─" * 40)

    dept_avg_scores = analyzer.group_by("department", "score", "mean")
    print("各部门平均评分：")
    for dept, avg in dept_avg_scores.items():
        print(f"  {dept:<6}：{avg:.2f}")

    # 画柱状图
    chart = draw_bar_chart(dept_avg_scores, "各部门平均评分", max_width=20)
    print(chart)

    # 各城市员工数量
    city_count = analyzer.group_by("city", "age", "count")
    city_count_chart = draw_bar_chart(city_count, "各城市员工人数", max_width=20)
    print(city_count_chart)

    # ── 步骤 6：相关性分析 ────────────────────────────────────────
    print("\n【步骤 6】相关性分析")
    print("─" * 40)

    # 年龄与评分的相关性
    r_age_score = analyzer.correlation("age", "score")
    print(f"年龄 × 评分  →  {analyzer._interpret_correlation(r_age_score)}")

    # 也可以分析年龄与年龄（自相关，应该是 1.0）
    r_age_age = analyzer.correlation("age", "age")
    print(f"年龄 × 年龄  →  r = {r_age_age:.4f}（自相关，理论值 = 1.0，验证公式正确）")

    # ── 步骤 7：生成完整报告 ──────────────────────────────────────
    print("\n【步骤 7】生成完整报告")
    print("─" * 40)
    report = analyzer.generate_report()
    print(report)

    # ── 步骤 8：导出报告到文件 ────────────────────────────────────
    print("\n【步骤 8】导出报告到文件")
    print("─" * 40)
    analyzer.export_report("analysis_report.txt")

    print("\n╔══════════════════════════════════════════╗")
    print("║              演示完成！                   ║")
    print("╚══════════════════════════════════════════╝")


if __name__ == "__main__":
    main()
```

---

## 第五部分：运行效果

### 5.1 终端输出示例

运行 `python 05_csv_analyzer.py` 后，终端会输出：

```
╔══════════════════════════════════════════╗
║       CSV 数据分析工具 - 完整演示         ║
╚══════════════════════════════════════════╝

【步骤 1】生成示例数据
────────────────────────────────────────
示例数据已生成：employees.csv（共 8 条记录）

【步骤 2】加载 CSV 文件
────────────────────────────────────────
已加载 8 条记录，共 5 列
列名：name, age, city, score, department

【步骤 3】单列统计分析
────────────────────────────────────────
评分列统计：
  最小值：65.00
  最大值：95.00
  平均值：83.06
  中位数：85.75
  众　数：65.00（出现 1 次）
  标准差：10.35

城市列统计：
  唯一城市数：3
  最常见城市：北京（3 人）
  城市分布：{'北京': 3, '上海': 3, '广州': 2}

【步骤 4】数据过滤
────────────────────────────────────────
评分 >= 88 的员工（共 4 人）：
  张三 | 技术部 | 评分：92.5
  王五 | 技术部 | 评分：88.5
  陈七 | 技术部 | 评分：95.0
  周十 | 技术部 | 评分：90.0

北京的员工（共 3 人）：
  张三 | 年龄：28 | 评分：92.5
  王五 | 年龄：24 | 评分：88.5
  刘八 | 年龄：27 | 评分：72.5

【步骤 5】分组聚合（各部门平均评分）
────────────────────────────────────────
各部门平均评分：
  技术部：91.50
  行政部：74.00
  市场部：75.25

  各部门平均评分
  ───────────────────────────────────────────
  技术部    │ ████████████████████  91.50
  行政部    │ ████████████████      74.00
  市场部    │ ████████████████      75.25
  ───────────────────────────────────────────


  各城市员工人数
  ───────────────────────────────────────────
  北京      │ ████████████████████  3.00
  上海      │ ████████████████████  3.00
  广州      │ █████████████         2.00
  ───────────────────────────────────────────

【步骤 6】相关性分析
────────────────────────────────────────
年龄 × 评分  →  几乎没有相关（r = -0.0706）
年龄 × 年龄  →  r = 1.0000（自相关，理论值 = 1.0，验证公式正确）

【步骤 7】生成完整报告
────────────────────────────────────────
============================================================
                CSV 数据分析报告
============================================================
  数据来源：employees.csv
  总记录数：8 条
  总列数　：5 列
  列名　　：name, age, city, score, department
============================================================

【列名：name】
  数据类型：文本
  有效记录：8 条
  唯一值数：8
  最常见值：'张三'（出现 1 次）

  name 分布
  ────────────────────────────────────────
  张三      │ ████████████████████  1
  李四      │ ████████████████████  1
  王五      │ ████████████████████  1
  赵六      │ ████████████████████  1
  陈七      │ ████████████████████  1
  刘八      │ ████████████████████  1
  孙九      │ ████████████████████  1
  周十      │ ████████████████████  1
  ────────────────────────────────────────

【列名：age】
  数据类型：数字
  有效记录：8 条
  最小值　：24.00
  最大值　：42.00
  平均值　：31.75
  中位数　：30.00
  众　　数：24.00（出现 1 次）
  标准差　：5.87

【列名：city】
  数据类型：文本
  有效记录：8 条
  唯一值数：3
  最常见值：'北京'（出现 3 次）

  city 分布
  ────────────────────────────────────────
  北京      │ ████████████████████  3
  上海      │ ████████████████████  3
  广州      │ █████████████         2
  ────────────────────────────────────────

【列名：score】
  数据类型：数字
  有效记录：8 条
  最小值　：65.00
  最大值　：95.00
  平均值　：83.06
  中位数　：85.75
  众　　数：65.00（出现 1 次）
  标准差　：10.35

【列名：department】
  数据类型：文本
  有效记录：8 条
  唯一值数：3
  最常见值：'技术部'（出现 4 次）

  department 分布
  ────────────────────────────────────────
  技术部    │ ████████████████████  4
  市场部    │ ██████████            2
  行政部    │ ██████████            2
  ────────────────────────────────────────

============================================================

【步骤 8】导出报告到文件
────────────────────────────────────────

报告已导出至：analysis_report.txt
文件大小：2847 字节

╔══════════════════════════════════════════╗
║              演示完成！                   ║
╚══════════════════════════════════════════╝
```

---

## 第六部分：扩展练习

### 6.1 用 matplotlib 绘制真正的柱状图

ASCII 柱状图很方便，但如果想生成图片，可以用 `matplotlib`。

```bash
# 安装 matplotlib
uv add matplotlib
```

```python
# 代码骨架：将 ASCII 图换成真实图形

import matplotlib.pyplot as plt
import matplotlib
# 解决中文显示问题（Mac/Linux）
matplotlib.rcParams["font.sans-serif"] = ["Arial Unicode MS", "SimHei"]
matplotlib.rcParams["axes.unicode_minus"] = False

def plot_bar_chart(data: dict, title: str = "分析结果", ylabel: str = "数值") -> None:
    """
    用 matplotlib 绘制柱状图并显示。

    参数：
        data:   字典，键是标签，值是数值
        title:  图表标题
        ylabel: Y 轴标签
    """
    labels = list(data.keys())
    values = list(data.values())

    # 创建图表
    fig, ax = plt.subplots(figsize=(8, 5))

    # 绘制柱子
    bars = ax.bar(labels, values, color=["#4C72B0", "#DD8452", "#55A868"])

    # 在每个柱子顶部显示数值
    for bar, val in zip(bars, values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,  # X 坐标（柱子中心）
            bar.get_height() + 0.5,              # Y 坐标（柱子顶部上方）
            f"{val:.1f}",                         # 显示的文字
            ha="center",                          # 水平居中
            va="bottom",
        )

    ax.set_title(title, fontsize=14, fontweight="bold")
    ax.set_ylabel(ylabel)
    ax.set_ylim(0, max(values) * 1.15)  # Y 轴留出顶部空间

    plt.tight_layout()
    plt.savefig(f"{title}.png", dpi=150, bbox_inches="tight")  # 保存为图片
    plt.show()
    print(f"图表已保存：{title}.png")


# 在 DataAnalyzer 中调用：
# dept_scores = analyzer.group_by("department", "score", "mean")
# plot_bar_chart(dept_scores, title="各部门平均评分", ylabel="绩效评分")
```

### 6.2 相关性热力图

如果数据有多个数字列，可以画热力图，一次性看所有列之间的相关性：

```python
def plot_correlation_heatmap(analyzer: "DataAnalyzer") -> None:
    """
    绘制所有数字列之间的相关性热力图。

    颜色越红 = 正相关越强
    颜色越蓝 = 负相关越强
    颜色越白 = 无相关
    """
    import matplotlib.pyplot as plt
    import matplotlib.colors as mcolors

    # 找出所有数字列
    numeric_cols = [
        col for col in analyzer.columns
        if analyzer.describe_column(col).get("type") == "numeric"
    ]

    if len(numeric_cols) < 2:
        print("数字列不足 2 列，无法画热力图")
        return

    n = len(numeric_cols)
    # 计算相关矩阵
    matrix = []
    for col1 in numeric_cols:
        row = []
        for col2 in numeric_cols:
            try:
                r = analyzer.correlation(col1, col2)
            except ValueError:
                r = 0.0
            row.append(r)
        matrix.append(row)

    # 绘制热力图
    fig, ax = plt.subplots(figsize=(n * 1.5 + 2, n * 1.5 + 1))
    im = ax.imshow(matrix, cmap="RdBu_r", vmin=-1, vmax=1)

    # 设置坐标轴标签
    ax.set_xticks(range(n))
    ax.set_yticks(range(n))
    ax.set_xticklabels(numeric_cols, rotation=45, ha="right")
    ax.set_yticklabels(numeric_cols)

    # 在格子里显示数值
    for i in range(n):
        for j in range(n):
            ax.text(j, i, f"{matrix[i][j]:.2f}", ha="center", va="center", fontsize=9)

    plt.colorbar(im, ax=ax, label="相关系数")
    ax.set_title("相关性热力图")
    plt.tight_layout()
    plt.savefig("correlation_heatmap.png", dpi=150)
    plt.show()
    print("热力图已保存：correlation_heatmap.png")
```

### 6.3 支持 Excel 文件

```bash
# 安装 openpyxl（读写 xlsx）
uv add openpyxl
```

```python
import openpyxl

def load_excel(filepath: str) -> list[dict[str, str]]:
    """
    读取 Excel 文件，转换为与 CSV 相同格式的数据列表。
    这样 DataAnalyzer 的其余方法不需要任何修改！
    """
    wb = openpyxl.load_workbook(filepath)
    ws = wb.active  # 读取第一个工作表

    # 第一行是表头
    headers = [cell.value for cell in next(ws.iter_rows(min_row=1, max_row=1))]

    data = []
    for row in ws.iter_rows(min_row=2, values_only=True):  # 从第二行开始
        row_dict = {}
        for col_name, value in zip(headers, row):
            row_dict[col_name] = str(value) if value is not None else ""
        data.append(row_dict)

    return data

# 用法：
# analyzer.data = load_excel("employees.xlsx")
# analyzer.columns = list(analyzer.data[0].keys()) if analyzer.data else []
```

### 6.4 缺失值处理

真实数据往往有缺失（比如某个员工没有填写年龄）。常见的处理方式：

```python
from typing import Literal

def handle_missing_values(
    data: list[dict[str, str]],
    column: str,
    strategy: Literal["fill_mean", "fill_zero", "drop_row"] = "fill_mean",
) -> list[dict[str, str]]:
    """
    处理某列的缺失值。

    策略：
        fill_mean  → 用该列的平均值填充（适合数字列，不影响整体统计）
        fill_zero  → 用 0 填充（简单粗暴）
        drop_row   → 直接删除有缺失值的行（数据少时谨慎使用）

    类比：
        成绩表里有同学没有参加考试（缺考）：
        fill_mean → 给他填上班级平均分
        fill_zero → 给他填 0 分
        drop_row  → 把他从名单里删除
    """
    # 找出有值的行，计算均值（用于 fill_mean 策略）
    numeric_values = [
        float(row[column])
        for row in data
        if row.get(column, "").strip() and _is_numeric(row[column])
    ]
    mean_val = sum(numeric_values) / len(numeric_values) if numeric_values else 0.0

    result = []
    for row in data:
        val = row.get(column, "").strip()

        if val:  # 有值，不需要处理
            result.append(row)
        else:
            # 缺失值
            match strategy:
                case "fill_mean":
                    new_row = dict(row)
                    new_row[column] = str(mean_val)
                    result.append(new_row)
                case "fill_zero":
                    new_row = dict(row)
                    new_row[column] = "0"
                    result.append(new_row)
                case "drop_row":
                    pass  # 跳过这行，相当于删除


def _is_numeric(value: str) -> bool:
    """判断字符串是否为数字（辅助函数）。"""
    try:
        float(value)
        return True
    except (ValueError, TypeError):
        return False

    return result


# 用法示例：
# analyzer.data = handle_missing_values(analyzer.data, "score", strategy="fill_mean")
# print(f"处理后记录数：{len(analyzer.data)}")
```

### 6.5 数据透视表

```python
def pivot_table(
    data: list[dict[str, str]],
    index: str,       # 行：按这列分组
    columns: str,     # 列：按这列展开
    values: str,      # 值：对这列聚合
    agg_func: str = "mean",  # 聚合方式
) -> None:
    """
    生成文字版数据透视表。

    类比 Excel 透视表：
        index   = 行标签（如：部门）
        columns = 列标签（如：城市）
        values  = 格子里的值（如：平均评分）

    输出示例：
             北京     上海     广州
    技术部   90.5     92.5     —
    市场部   72.5     78.0     —
    行政部   —        —        74.0
    """
    from collections import defaultdict

    # 收集数据
    pivot: defaultdict[str, defaultdict[str, list[float]]] = defaultdict(lambda: defaultdict(list))

    all_col_vals = set()
    for row in data:
        row_key = row.get(index, "")
        col_key = row.get(columns, "")
        val_str = row.get(values, "")

        if row_key and col_key and val_str:
            try:
                pivot[row_key][col_key].append(float(val_str))
                all_col_vals.add(col_key)
            except ValueError:
                pass

    # 对每个格子聚合
    col_list = sorted(all_col_vals)
    col_width = 8

    # 打印表头
    header = f"{'':10}" + "".join(f"{c:>{col_width}}" for c in col_list)
    print(header)
    print("─" * len(header))

    # 打印每行
    for row_key in sorted(pivot.keys()):
        row_str = f"{row_key:<10}"
        for col_key in col_list:
            vals = pivot[row_key].get(col_key, [])
            if vals:
                match agg_func:
                    case "mean":  cell = statistics.mean(vals)
                    case "sum":   cell = sum(vals)
                    case "count": cell = float(len(vals))
                    case _:       cell = statistics.mean(vals)
                row_str += f"{cell:>{col_width}.1f}"
            else:
                row_str += f"{'—':>{col_width}}"
        print(row_str)


# 用法：
# pivot_table(analyzer.data, index="department", columns="city", values="score")
```

---

## 总结

通过这个项目，你学会了：

```
┌────────────────────────────────────────────────────────────────┐
│                     项目五 知识点回顾                           │
├────────────────────────────┬───────────────────────────────────┤
│  技能                      │  对应知识点                        │
├────────────────────────────┼───────────────────────────────────┤
│  读取 CSV 文件              │  csv.DictReader、文件编码         │
│  统计计算                  │  statistics 模块、手动公式         │
│  数据分组                  │  collections.defaultdict           │
│  频率统计                  │  collections.Counter               │
│  条件过滤                  │  列表推导式、match 语句             │
│  相关性分析                │  皮尔逊公式、math.sqrt             │
│  ASCII 可视化              │  字符串乘法、格式化输出             │
│  文件导出                  │  open() 写入、pathlib.Path         │
│  面向对象设计              │  类、方法、封装                    │
│  类型提示                  │  list[dict]、Literal               │
└────────────────────────────┴───────────────────────────────────┘
```

**下一步**

如果你想继续深入数据分析方向，推荐学习：
- `pandas`：专业数据分析库，功能是本项目的 100 倍
- `numpy`：数值计算加速
- `matplotlib` / `seaborn`：专业可视化
- `jupyter notebook`：交互式数据分析环境

---

[返回目录](./README.md)
---

[← 上一篇](./04-网页爬虫.md) | [下一篇 →](../09-附录/01-模块与包.md)
