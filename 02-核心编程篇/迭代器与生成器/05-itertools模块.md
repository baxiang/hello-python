# itertools 模块

本章讲解 Python itertools 模块的常用函数，用于高效处理迭代器。

---

## 无限迭代器

### count() - 无限计数

```python
import itertools

for i in itertools.count(10, 5):  # 从 10 开始，步长 5
    if i > 30:
        break
    print(i, end=" ")
# 10 15 20 25 30
```

### cycle() - 循环迭代

```python
import itertools

count = 0
for item in itertools.cycle(["红", "绿", "蓝"]):
    if count >= 6:
        break
    print(item, end=" ")
    count += 1
# 红 绿 蓝 红 绿 蓝
```

### repeat() - 重复元素

```python
import itertools

for item in itertools.repeat("Hello", 3):
    print(item)
# Hello
# Hello
# Hello
```

---

## 有限迭代器

### chain() - 链接多个可迭代对象

```python
import itertools

for item in itertools.chain([1, 2], ["a", "b"], [True, False]):
    print(item, end=" ")
# 1 2 a b True False
```

### islice() - 切片

```python
import itertools

numbers = range(10)
for item in itertools.islice(numbers, 3, 8, 2):
    print(item, end=" ")
# 3 5 7（从索引 3 到 8，步长 2）
```

### compress() - 根据选择器过滤

```python
import itertools

data = ["A", "B", "C", "D"]
selectors = [True, False, True, False]
for item in itertools.compress(data, selectors):
    print(item, end=" ")
# A C
```

### groupby() - 分组

```python
import itertools

data = [("A", 1), ("A", 2), ("B", 3), ("B", 4)]
for key, group in itertools.groupby(data, key=lambda x: x[0]):
    print(f"{key}: {list(group)}")
# A: [('A', 1), ('A', 2)]
# B: [('B', 3), ('B', 4)]
```

---

## 组合迭代器

### product() - 笛卡尔积

```python
import itertools

for item in itertools.product("ABC", [1, 2]):
    print(item, end=" ")
# ('A', 1) ('A', 2) ('B', 1) ('B', 2) ('C', 1) ('C', 2)
```

### permutations() - 排列

```python
import itertools

for item in itertools.permutations([1, 2, 3], 2):
    print(item, end=" ")
# (1, 2) (1, 3) (2, 1) (2, 3) (3, 1) (3, 2)
```

### combinations() - 组合

```python
import itertools

for item in itertools.combinations([1, 2, 3], 2):
    print(item, end=" ")
# (1, 2) (1, 3) (2, 3)
```

### combinations_with_replacement() - 可重复组合

```python
import itertools

for item in itertools.combinations_with_replacement([1, 2, 3], 2):
    print(item, end=" ")
# (1, 1) (1, 2) (1, 3) (2, 2) (2, 3) (3, 3)
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
│   ✓ groupby()：分组                                         │
│                                                             │
│   组合迭代器：                                               │
│   ✓ product()：笛卡尔积                                     │
│   ✓ permutations()：排列                                    │
│   ✓ combinations()：组合                                    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```