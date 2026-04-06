# itertools 模块

> **Python 版本要求**：Python 3.11+

**导航**：

---

## 第一部分：为什么需要 itertools？

### 1.1 实际场景引入

假设你需要处理多个数据源的组合、过滤和分组：

```python
from typing import Iterator, Any

# 尝试一：手动实现笛卡尔积
def cartesian_product(list1: list[Any], list2: list[Any]) -> list[tuple[Any, Any]]:
    result: list[tuple[Any, Any]] = []
    for a in list1:
        for b in list2:
            result.append((a, b))
    return result

colors: list[str] = ["红", "绿", "蓝"]
sizes: list[str] = ["S", "M", "L"]
print(cartesian_product(colors, sizes))
# [('红', 'S'), ('红', 'M'), ('红', 'L'), ...]

# 尝试二：手动实现分组
def group_by_key(data: list[tuple[str, int]]) -> dict[str, list[int]]:
    result: dict[str, list[int]] = {}
    for key, value in data:
        if key not in result:
            result[key] = []
        result[key].append(value)
    return result

data: list[tuple[str, int]] = [("A", 1), ("A", 2), ("B", 3), ("B", 4)]
print(group_by_key(data))  # {'A': [1, 2], 'B': [3, 4]}

# 尝试三：使用 itertools（简洁高效）
import itertools

# 笛卡尔积
for item in itertools.product(colors, sizes):
    print(item, end=" ")

# 分组
for key, group in itertools.groupby(data, key=lambda x: x[0]):
    print(f"{key}: {list(group)}")
```

**问题**：如何使用 itertools 高效处理迭代器操作？

### 1.2 概念动机

itertools 提供三类函数：

```
┌─────────────────────────────────────────┐
│       itertools 模块函数分类            │
├─────────────────────────────────────────┤
│                                         │
│  无限迭代器：                           │
│  count(start, step)   - 无限计数        │
│  cycle(iterable)      - 循环迭代        │
│  repeat(elem, n)      - 重复元素        │
│                                         │
│  有限迭代器：                           │
│  chain(*iterables)    - 链接多个        │
│  islice(it, start, stop) - 切片        │
│  compress(data, selectors) - 过滤      │
│  groupby(data, key)   - 分组           │
│                                         │
│  组合迭代器：                           │
│  product(*iterables)  - 笛卡尔积       │
│  permutations(it, r)  - 排列           │
│  combinations(it, r)  - 组合           │
│  combinations_with_replacement()        │
│                       - 可重复组合      │
│                                         │
└─────────────────────────────────────────┘
```

---

## 第二部分：无限迭代器

### 2.1 count() - 无限计数

```python
import itertools
from typing import Iterator

# 从 10 开始，步长 5
counter: Iterator[int] = itertools.count(10, 5)

for i in counter:
    if i > 30:
        break
    print(i, end=" ")
# 10 15 20 25 30

# 实际应用：带索引的迭代
colors: list[str] = ["红", "绿", "蓝"]
for idx, color in zip(itertools.count(), colors):
    print(f"{idx}: {color}")
# 0: 红
# 1: 绿
# 2: 蓝
```

### 2.2 cycle() - 循环迭代

```python
import itertools
from typing import Iterator

# 无限循环
cycler: Iterator[str] = itertools.cycle(["红", "绿", "蓝"])

count: int = 0
for item in cycler:
    if count >= 6:
        break
    print(item, end=" ")
    count += 1
# 红 绿 蓝 红 绿 蓝

# 实际应用：轮询调度
servers: list[str] = ["server1", "server2", "server3"]
round_robin = itertools.cycle(servers)

for _ in range(5):
    print(f"请求发送到：{next(round_robin)}")
# server1, server2, server3, server1, server2
```

### 2.3 repeat() - 重复元素

```python
import itertools
from typing import Iterator

# 重复固定次数
for item in itertools.repeat("Hello", 3):
    print(item)
# Hello
# Hello
# Hello

# 无限重复（需要配合 break）
repeater: Iterator[str] = itertools.repeat("A")
for i, item in enumerate(repeater):
    if i >= 3:
        break
    print(item, end=" ")
# A A A

# 实际应用：填充序列
data: list[int] = [1, 2, 3]
filled: zip[tuple[int, str]] = zip(data, itertools.repeat("X"))
print(list(filled))  # [(1, 'X'), (2, 'X'), (3, 'X')]
```

---

## 第三部分：有限迭代器

### 3.1 chain() - 链接多个可迭代对象

```python
import itertools
from typing import Iterator, Any

# 链接多个列表
list1: list[int] = [1, 2]
list2: list[str] = ["a", "b"]
list3: list[bool] = [True, False]

chained: Iterator[Any] = itertools.chain(list1, list2, list3)
print(list(chained))  # [1, 2, 'a', 'b', True, False]

# 实际应用：展平嵌套列表
nested: list[list[int]] = [[1, 2], [3, 4], [5, 6]]
flat: Iterator[int] = itertools.chain.from_iterable(nested)
print(list(flat))  # [1, 2, 3, 4, 5, 6]
```

### 3.2 islice() - 切片

```python
import itertools
from typing import Iterator

# 切片迭代器
numbers: range = range(10)

# islice(iterable, stop)
result1: Iterator[int] = itertools.islice(numbers, 5)
print(list(result1))  # [0, 1, 2, 3, 4]

# islice(iterable, start, stop)
result2: Iterator[int] = itertools.islice(numbers, 3, 8)
print(list(result2))  # [3, 4, 5, 6, 7]

# islice(iterable, start, stop, step)
result3: Iterator[int] = itertools.islice(numbers, 3, 8, 2)
print(list(result3))  # [3, 5, 7]

# 实际应用：分页
def paginate(data: list[Any], page: int, size: int) -> Iterator[Any]:
    """分页迭代器"""
    start: int = (page - 1) * size
    return itertools.islice(data, start, start + size)

all_items: list[int] = list(range(100))
page_2: Iterator[int] = paginate(all_items, page=2, size=10)
print(list(page_2))  # [10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
```

### 3.3 compress() - 根据选择器过滤

```python
import itertools
from typing import Iterator, Any

# 根据布尔选择器过滤
data: list[str] = ["A", "B", "C", "D"]
selectors: list[bool] = [True, False, True, False]

filtered: Iterator[str] = itertools.compress(data, selectors)
print(list(filtered))  # ['A', 'C']

# 实际应用：条件过滤
users: list[dict[str, Any]] = [
    {"name": "Alice", "active": True},
    {"name": "Bob", "active": False},
    {"name": "Charlie", "active": True},
]

active: Iterator[dict[str, Any]] = itertools.compress(
    users, 
    [u["active"] for u in users]
)
print([u["name"] for u in active])  # ['Alice', 'Charlie']
```

### 3.4 groupby() - 分组

```python
import itertools
from typing import Iterator, Any

# 基本分组（需要先排序！）
data: list[tuple[str, int]] = [
    ("A", 1), ("A", 2), ("B", 3), ("B", 4)
]

for key, group in itertools.groupby(data, key=lambda x: x[0]):
    print(f"{key}: {list(group)}")
# A: [('A', 1), ('A', 2)]
# B: [('B', 3), ('B', 4)]

# 注意：groupby 要求连续相同的元素
unsorted: list[int] = [1, 2, 1, 2, 1, 2]  # 未排序
for key, group in itertools.groupby(unsorted):
    print(f"{key}: {list(group)}")
# 1: [1]
# 2: [2]
# 1: [1]
# 2: [2]
# 1: [1]
# 2: [2]

# 正确做法：先排序
sorted_data: list[int] = sorted(unsorted)
for key, group in itertools.groupby(sorted_data):
    print(f"{key}: {list(group)}")
# 1: [1, 1, 1]
# 2: [2, 2, 2]

# 实际应用：按属性分组
from dataclasses import dataclass

@dataclass
class Student:
    name: str
    grade: str

students: list[Student] = [
    Student("Alice", "A"),
    Student("Bob", "B"),
    Student("Charlie", "A"),
    Student("David", "B"),
]

# 先按成绩排序
sorted_students: list[Student] = sorted(students, key=lambda s: s.grade)

for grade, group in itertools.groupby(sorted_students, key=lambda s: s.grade):
    names: list[str] = [s.name for s in group]
    print(f"成绩 {grade}: {names}")
# 成绩 A: ['Alice', 'Charlie']
# 成绩 B: ['Bob', 'David']
```

---

## 第四部分：组合迭代器

### 4.1 product() - 笛卡尔积

```python
import itertools
from typing import Iterator, Any

# 两个序列的笛卡尔积
colors: list[str] = ["红", "绿"]
sizes: list[str] = ["S", "M", "L"]

result: Iterator[tuple[str, str]] = itertools.product(colors, sizes)
for item in result:
    print(item, end=" ")
# ('红', 'S') ('红', 'M') ('红', 'L') ('绿', 'S') ('绿', 'M') ('绿', 'L')

# 单个序列的笛卡尔积（repeat 参数）
result2: Iterator[tuple[int, int]] = itertools.product([1, 2], repeat=2)
print(list(result2))
# [(1, 1), (1, 2), (2, 1), (2, 2)]

# 实际应用：生成所有可能的配置
models: list[str] = ["Model-A", "Model-B"]
colors2: list[str] = ["red", "blue"]
storage: list[str] = ["64GB", "128GB"]

configs: Iterator[tuple[str, str, str]] = itertools.product(models, colors2, storage)
for config in configs:
    print(f"配置：{config}")
```

### 4.2 permutations() - 排列

```python
import itertools
from typing import Iterator

# 所有排列
result: Iterator[tuple[int, int]] = itertools.permutations([1, 2, 3], 2)
print(list(result))
# [(1, 2), (1, 3), (2, 1), (2, 3), (3, 1), (3, 2)]

# 所有全排列（不指定 r）
full: Iterator[tuple[int, ...]] = itertools.permutations([1, 2, 3])
print(list(full))
# [(1, 2, 3), (1, 3, 2), (2, 1, 3), (2, 3, 1), (3, 1, 2), (3, 2, 1)]

# 实际应用：密码破解
import string

def crack_password(chars: str, length: int) -> Iterator[str]:
    """生成所有可能的密码组合"""
    for perm in itertools.permutations(chars, length):
        yield "".join(perm)

# 生成 3 位数字密码
for pwd in itertools.islice(crack_password("0123456789", 3), 5):
    print(pwd)
# 012 013 014 015 016
```

### 4.3 combinations() - 组合

```python
import itertools
from typing import Iterator

# 组合（不重复）
result: Iterator[tuple[int, int]] = itertools.combinations([1, 2, 3, 4], 2)
print(list(result))
# [(1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4)]

# 实际应用：从 5 个数字中选 3 个
from itertools import combinations

numbers: list[int] = [1, 2, 3, 4, 5]
for combo in combinations(numbers, 3):
    print(combo, end=" ")
# (1, 2, 3) (1, 2, 4) (1, 2, 5) ...

# 实际应用：彩票号码
def lottery_numbers() -> Iterator[tuple[int, ...]]:
    """生成彩票号码组合（从 35 个数字中选 5 个）"""
    return combinations(range(1, 36), 5)

# 计算总组合数
total: int = sum(1 for _ in lottery_numbers())
print(f"总组合数：{total}")  # 324632
```

### 4.4 combinations_with_replacement() - 可重复组合

```python
import itertools
from typing import Iterator

# 可重复组合
result: Iterator[tuple[int, int]] = itertools.combinations_with_replacement([1, 2, 3], 2)
print(list(result))
# [(1, 1), (1, 2), (1, 3), (2, 2), (2, 3), (3, 3)]

# 对比：普通组合不包含重复元素
normal: Iterator[tuple[int, int]] = itertools.combinations([1, 2, 3], 2)
print(list(normal))
# [(1, 2), (1, 3), (2, 3)]

# 实际应用：多选题答案
def multichoice_answers(options: str, num_choices: int) -> Iterator[str]:
    """生成多选题所有可能的答案组合"""
    for combo in itertools.combinations_with_replacement(options, num_choices):
        yield "".join(combo)

for answer in multichoice_answers("ABCD", 2):
    print(answer, end=" ")
# AA AB AC AD BB BC BD CC CD DD
```

---

## 第五部分：实际应用场景

### 5.1 数据分块处理

```python
import itertools
from typing import Iterator, Any

def chunked(iterable: Iterator[Any], size: int) -> Iterator[tuple[Any, ...]]:
    """将迭代器分块"""
    it: Iterator[Any] = iter(iterable)
    while chunk := tuple(itertools.islice(it, size)):
        yield chunk

# 使用
data: range = range(10)
for chunk in chunked(data, 3):
    print(chunk)
# (0, 1, 2)
# (3, 4, 5)
# (6, 7, 8)
# (9,)
```

### 5.2 滑动窗口

```python
import itertools
from typing import Iterator, Any

def sliding_window(iterable: Iterator[Any], size: int) -> Iterator[tuple[Any, ...]]:
    """滑动窗口"""
    iters: tuple[Iterator[Any], ...] = itertools.tee(iterable, size)
    for i, it in enumerate(iters):
        for _ in range(i):
            next(it, None)
    return zip(*iters)

# 使用
data: list[int] = [1, 2, 3, 4, 5]
for window in sliding_window(iter(data), 3):
    print(window)
# (1, 2, 3)
# (2, 3, 4)
# (3, 4, 5)
```

### 5.3 批量并行处理

```python
import itertools
from typing import Iterator, Any

def parallel_batches(iterable: Iterator[Any], n: int) -> Iterator[tuple[Any, ...]]:
    """将数据分成 n 个并行批次"""
    iters: tuple[Iterator[Any], ...] = itertools.tee(iterable, n)
    return tuple(
        itertools.islice(it, i, None, n)
        for i, it in enumerate(iters)
    )

# 使用
data: range = range(10)
batch1, batch2, batch3 = parallel_batches(data, 3)
print(list(batch1))  # [0, 3, 6, 9]
print(list(batch2))  # [1, 4, 7]
print(list(batch3))  # [2, 5, 8]
```

### 5.4 配置组合生成

```python
import itertools
from typing import Iterator, Any

def generate_configs(**options: list[Any]) -> Iterator[dict[str, Any]]:
    """生成所有可能的配置组合"""
    keys: list[str] = list(options.keys())
    values: list[list[Any]] = list(options.values())
    
    for combo in itertools.product(*values):
        yield dict(zip(keys, combo))

# 使用
configs: Iterator[dict[str, Any]] = generate_configs(
    model=["A", "B"],
    color=["red", "blue"],
    size=["S", "M", "L"]
)

for i, config in enumerate(configs, 1):
    print(f"{i}: {config}")
# 1: {'model': 'A', 'color': 'red', 'size': 'S'}
# 2: {'model': 'A', 'color': 'red', 'size': 'M'}
# ...
```

---

## itertools 速查表

```
┌─────────────────────────────────────────┐
│       itertools 模块常用函数            │
├─────────────────────────────────────────┤
│                                         │
│  无限迭代器：                           │
│  count(start, step)   - 无限计数        │
│  cycle(iterable)      - 循环迭代        │
│  repeat(elem, n)      - 重复元素        │
│                                         │
│  有限迭代器：                           │
│  chain(*iterables)    - 链接多个        │
│  islice(it, start, stop) - 切片        │
│  compress(data, selectors) - 过滤      │
│  groupby(data, key)   - 分组           │
│  tee(it, n)          - 复制迭代器      │
│                                         │
│  组合迭代器：                           │
│  product(*iterables)  - 笛卡尔积       │
│  permutations(it, r)  - 排列           │
│  combinations(it, r)  - 组合           │
│  combinations_with_replacement()        │
│                       - 可重复组合      │
│                                         │
└─────────────────────────────────────────┘
```

---

## 本章小结

```
┌─────────────────────────────────────────────────────────────┐
│                      itertools 模块 知识要点                  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   无限迭代器：                                               │
│   ✓ count()：无限计数                                       │
│   ✓ cycle()：循环迭代                                       │
│   ✓ repeat()：重复元素                                      │
│                                                             │
│   有限迭代器：                                               │
│   ✓ chain()：链接多个可迭代对象                             │
│   ✓ islice()：切片                                          │
│   ✓ compress()：条件过滤                                    │
│   ✓ groupby()：分组（需要先排序）                           │
│                                                             │
│   组合迭代器：                                               │
│   ✓ product()：笛卡尔积                                     │
│   ✓ permutations()：排列                                    │
│   ✓ combinations()：组合                                    │
│   ✓ combinations_with_replacement()：可重复组合             │
│                                                             │
│   实际应用：                                                 │
│   ✓ 数据分块                                                │
│   ✓ 滑动窗口                                                │
│   ✓ 配置生成                                                │
│   ✓ 密码破解                                                │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**导航**：
