# itertools 模块

> **Python 版本要求**：Python 3.11+

**贯穿项目**：日志分析系统
**本节目标**：用 `groupby()` 按小时分组统计错误数量

---

## 为什么需要 itertools？

### 问题场景：高效处理日志数据

继续日志分析系统，需要：
- 按小时分组统计错误数量
- 批量处理大量日志
- 避免手动写复杂循环

```python
# ❌ 方案一：手动分组统计（代码冗长）
from collections import defaultdict

def count_errors_by_hour_manual(logs: list[dict]) -> dict[str, int]:
    counts: defaultdict[str, int] = defaultdict(int)
    for log in logs:
        hour: str = log["timestamp"].strftime("%H:00")
        if log["level"] == "ERROR":
            counts[hour] += 1
    return dict(counts)

# ✅ 方案二：用 itertools.groupby（简洁高效）
import itertools

def count_errors_by_hour(logs: list[dict]) -> dict[str, int]:
    # 先按小时排序
    sorted_logs: list[dict] = sorted(
        logs, 
        key=lambda x: x["timestamp"].strftime("%H:00")
    )
    
    # 分组统计
    result: dict[str, int] = {}
    for hour, group in itertools.groupby(
        sorted_logs, 
        key=lambda x: x["timestamp"].strftime("%H:00")
    ):
        result[hour] = sum(1 for log in group if log["level"] == "ERROR")
    return result
```

**问题**：`itertools` 提供了哪些高效工具？如何正确使用 `groupby`？

---

## itertools：烹饪工具箱

### 生活类比

把 `itertools` 想象成烹饪工具箱：

```
┌─────────────────────────────────────────────────────────────┐
│  itertools = 烹饪工具箱                                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  手动处理 = 手工切菜                                          │
│  ─────────────────────────                                  │
│  • 每次都要自己写循环                                         │
│  • 代码冗长，容易出错                                         │
│  • 效率不高                                                  │
│                                                             │
│  itertools = 专业厨具                                        │
│  ─────────────────────────                                  │
│  • chain() = 拼盘（合并多盘菜）                               │
│  • groupby() = 分装盘（按类别分装）                          │
│  • islice() = 切片刀（只取一部分）                           │
│  • product() = 搅拌机（混合所有组合）                        │
│                                                             │
│  优势：                                                      │
│  ─────────────────────                                      │
│  • 工具现成，拿来就用                                         │
│  • 效率高，内存友好                                          │
│  • 代码简洁，易读易懂                                         │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**一句话：**
> `itertools` = Python 提供的现成迭代工具箱，拿来就用

### itertools 函数分类

```
┌─────────────────────────────────────────────────────────────┐
│       itertools 模块函数分类                                  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  无限迭代器（配合 break 或 islice 使用）：                     │
│  ───────────────────────────────────                        │
│  count(start, step)   - 无限计数                             │
│  cycle(iterable)      - 循环迭代                             │
│  repeat(elem, n)      - 重复元素                             │
│                                                             │
│  有限迭代器：                                                 │
│  ─────────────────────────                                  │
│  chain(*iterables)    - 链接多个可迭代对象                   │
│  islice(it, start, stop) - 切片迭代器                       │
│  compress(data, selectors) - 按选择器过滤                   │
│  groupby(data, key)   - 分组（需先排序）                     │
│  tee(it, n)          - 复制多个独立迭代器                    │
│                                                             │
│  组合迭代器：                                                 │
│  ─────────────────────────                                  │
│  product(*iterables)  - 笛卡尔积                             │
│  permutations(it, r)  - 排列                                 │
│  combinations(it, r)  - 组合                                 │
│  combinations_with_replacement() - 可重复组合               │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 贯穿实战：按小时分组统计错误

### groupby 工作原理

```
┌─────────────────────────────────────────────────────────────┐
│  groupby 分组流程                                             │
│                                                             │
│  原理：只对连续相同的元素分组                                  │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ 示例：groupby([1, 1, 1, 2, 2, 3, 3, 3])             │   │
│  │                                                      │   │
│  │  原序列：[1, 1, 1, 2, 2, 3, 3, 3]                    │   │
│  │           │     │   │     │                         │   │
│  │           ↓     ↓   ↓     ↓                         │   │
│  │  分组1：  [1, 1, 1]                                  │   │
│  │  分组2：      [2, 2]                                 │   │
│  │  分组3：          [3, 3, 3]                          │   │
│  │                                                      │   │
│  │  ⚠️ 如果未排序：[1, 2, 1, 2, 1]                      │   │
│  │  分组会变成：[1], [2], [1], [2], [1]（错误！）       │   │
│  │                                                      │   │
│  │  ✅ 正确做法：先排序再分组                            │   │
│  │                                                      │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 实现按小时分组统计

```python
import itertools
from datetime import datetime
from collections.abc import Iterator

def generate_sample_logs() -> Iterator[dict]:
    """生成示例日志数据
    
    贯穿项目：日志分析系统
    用于演示 groupby 分组统计
    """
    sample_data: list[tuple[str, str]] = [
        ("2024-01-19 10:00:15", "ERROR"),
        ("2024-01-19 10:05:30", "INFO"),
        ("2024-01-19 10:10:00", "ERROR"),
        ("2024-01-19 11:00:15", "WARN"),
        ("2024-01-19 11:05:30", "ERROR"),
        ("2024-01-19 11:10:00", "INFO"),
        ("2024-01-19 12:00:15", "ERROR"),
        ("2024-01-19 12:05:30", "ERROR"),
    ]
    
    for ts_str, level in sample_data:
        yield {
            "timestamp": datetime.strptime(ts_str, "%Y-%m-%d %H:%M:%S"),
            "level": level,
            "message": f"{level} log entry"
        }

def count_errors_by_hour(logs: Iterator[dict]) -> dict[str, int]:
    """按小时分组统计错误数量
    
    贯穿项目：日志分析系统
    核心功能：使用 groupby 按时间分组
    """
    # 关键：先按小时排序
    sorted_logs: list[dict] = sorted(
        list(logs),
        key=lambda x: x["timestamp"].strftime("%H:00")
    )
    
    # 分组并统计
    result: dict[str, int] = {}
    for hour, group in itertools.groupby(
        sorted_logs, 
        key=lambda x: x["timestamp"].strftime("%H:00")
    ):
        # 统计该小时的错误数量
        error_count: int = sum(1 for log in group if log["level"] == "ERROR")
        result[hour] = error_count
    
    return result

# 使用示例
logs = generate_sample_logs()
hourly_errors = count_errors_by_hour(logs)

for hour, count in sorted(hourly_errors.items()):
    print(f"{hour} - 错误数：{count}")
# 10:00 - 错误数：2
# 11:00 - 错误数：1
# 12:00 - 错误数：2
```

**关键代码说明：**

| 代码 | 含义 | 为什么这样写 |
|------|------|-------------|
| `sorted(logs, key=lambda x: x["timestamp"].strftime("%H:00"))` | 按小时排序 | `groupby` 只对连续相同元素分组，必须先排序 |
| `itertools.groupby(sorted_logs, key=lambda ...)` | 分组 | 按小时键分组，返回 (key, group_iterator) |
| `sum(1 for log in group if log["level"] == "ERROR")` | 统计错误数 | group 是迭代器，需要立即消费 |

---

## 常用 itertools 函数

### chain()：合并多个数据源

```python
import itertools
from collections.abc import Iterator

def merge_log_sources(*files: str) -> Iterator[str]:
    """合并多个日志文件
    
    贯穿项目：日志分析系统
    功能：用 chain 合并多个文件流
    """
    # 打开所有文件并链接
    file_iterators: list[Iterator[str]] = [
        (line.strip() for line in open(f, encoding="utf-8"))
        for f in files
    ]
    return itertools.chain(*file_iterators)

# 使用：合并三个日志文件
for line in itertools.islice(merge_log_sources("app.log", "error.log", "debug.log"), 10):
    print(line[:50])
```

### islice()：切片迭代器

```python
import itertools

# 分页读取
def get_log_page(logs: list[str], page: int, size: int) -> list[str]:
    """获取指定页的日志"""
    start: int = (page - 1) * size
    return list(itertools.islice(logs, start, start + size))

all_logs: list[str] = [f"Log entry {i}" for i in range(100)]
page_3: list[str] = get_log_page(all_logs, page=3, size=10)
print(page_3)  # ['Log entry 20', ..., 'Log entry 29']
```

### count() 和 cycle()：无限迭代

```python
import itertools

# count：无限计数（配合 islice）
for idx in itertools.islice(itertools.count(1), 5):
    print(idx)  # 1, 2, 3, 4, 5

# cycle：循环迭代（轮询服务器）
servers: list[str] = ["server1", "server2", "server3"]
round_robin = itertools.cycle(servers)

for _ in range(5):
    print(f"请求发送到：{next(round_robin)}")
# server1, server2, server3, server1, server2
```

### product() 和 combinations()：组合生成

```python
import itertools

# product：笛卡尔积（生成所有配置）
models: list[str] = ["A", "B"]
colors: list[str] = ["red", "blue"]
for config in itertools.product(models, colors):
    print(f"配置：{config}")
# ('A', 'red'), ('A', 'blue'), ('B', 'red'), ('B', 'blue')

# combinations：组合（从5个选3个）
for combo in itertools.combinations(range(5), 3):
    print(combo)
# (0, 1, 2), (0, 1, 3), ...
```

---

## 推荐做法与反模式

### 推荐做法

| 做法 | 原因 | 示例 |
|------|------|------|
| **groupby 前先排序** | 只对连续相同元素分组 | `groupby(sorted(data))` |
| **用 chain 代替列表相加** | 避免创建中间列表 | `chain(list1, list2)` |
| **islice 切片迭代器** | 迭代器不支持普通切片 | `islice(gen, 5, 10)` |
| **无限迭代器配合终止** | 防止无限循环 | `islice(count(), 10)` |

### 反模式：不要这样做

```python
# ❌ 错误：groupby 不排序
import itertools

data: list[int] = [1, 2, 1, 2, 1]
for key, group in itertools.groupby(data):
    print(f"{key}: {list(group)}")
# 1: [1], 2: [2], 1: [1], 2: [2], 1: [1] ← 分成多组！

# ✅ 正确：先排序
sorted_data: list[int] = sorted(data)
for key, group in itertools.groupby(sorted_data):
    print(f"{key}: {list(group)}")
# 1: [1, 1, 1], 2: [2, 2] ← 正确分组
```

```python
# ❌ 错误：无限迭代器无终止
import itertools
for i in itertools.count():  # 无限循环！
    print(i)

# ✅ 正确：使用 islice 或 break
for i in itertools.islice(itertools.count(), 10):
    print(i)
```

### 适用场景

| 场景 | 推荐 | 函数 |
|------|------|------|
| 合并多个数据源 | ✅ | `chain()` |
| 分组统计 | ✅ | `groupby()` + 排序 |
| 分页读取 | ✅ | `islice()` |
| 生成所有组合 | ✅ | `product()` |
| 轮询调度 | ✅ | `cycle()` |
| 带索引遍历 | ❌ | 用 `enumerate()` |

---

## 自检清单

回答以下问题，检查你是否掌握了核心概念：

1. `groupby()` 为什么必须先排序？
2. `chain()` 和列表相加有什么区别？
3. 如何安全使用无限迭代器？
4. `product()` 和 `combinations()` 有什么区别？
5. `tee()` 有什么陷阱？

**答案**：

1. `groupby` 只对连续相同元素分组，未排序会错误分组
2. `chain` 惰性连接无中间列表，列表相加创建新列表
3. 配合 `islice()` 或 `break` 限制次数
4. `product` 是笛卡尔积（所有组合），`combinations` 是从 n 选 r（不重复）
5. `tee` 后原迭代器会缓存数据，两个迭代器不要差距太大

---

## 本章能力清单

**学完本章，你能够：**

- [x] 用 `groupby()` 按小时分组统计日志错误
- [x] 用 `chain()` 合并多个日志数据源
- [x] 用 `islice()` 实现日志分页读取
- [x] 正确使用无限迭代器（count、cycle）
- [x] 理解 groupby 必须先排序的原因

**前置知识检查**：
- 你是否掌握了生成器基础？ ← 第3节

**下一步学习**：
- 异步生成器（async yield 流处理） → 第6节

---

**导航**：