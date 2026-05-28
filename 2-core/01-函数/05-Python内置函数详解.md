# 05-Python内置函数详解

> **Python 版本要求**：Python 3.11+
>
> Python 内置了 70+ 个高频使用的函数。这些函数不需要导入任何模块即可直接使用，它们构成了 Python 开发的基石。

> **贯穿项目**：functions_demo/
> **代码位置**：`app/core/builtins.py`
> **测试验证**：`cd functions_demo && uv run pytest -k TestBuiltins -v`

---

## 概念铺垫

Python 内置了 70+ 个高频使用的函数。这些函数不需要导入任何模块即可直接使用，它们构成了 Python 开发的基石。

### L1 理解层：会用

## 1. 查看内置函数

你可以通过 `dir` 命令查看所有的内置函数：

```python
# 查看当前环境所有的内置函数
print(dir(__builtins__))

# 查看帮助文档
help(print)
help(range)
```

---

## 2. 基础输入与输出

### 2.1 `print()`: 强大的输出控制

**函数签名**：`print(*objects, sep=' ', end='\n', file=None, flush=False)`

| 参数 | 类型 | 默认值 | 说明 |
| :--- | :--- | :--- | :--- |
| `*objects` | 任意类型 | 无 | **位置参数**。要打印的内容，可以传多个，如 `print(a, b, c)` |
| `sep` | 字符串 | `' '` (空格) | **分隔符**。多个 `objects` 之间的连接符 |
| `end` | 字符串 | `'\n'` (换行) | **结尾符**。打印完所有内容后追加的字符 |
| `file` | 文件对象 | `sys.stdout` | **输出目标**。默认输出到屏幕，可重定向到文件 |
| `flush` | 布尔值 | `False` | **是否强制刷新**。默认缓冲输出，设为 `True` 可立即写入 |

```python
# 基础用法
print("Hello", "World")  # 输出: Hello World

# 自定义分隔符 (sep) - 生成日期格式
print("2023", "10", "01", sep="-")  # 输出: 2023-10-01

# 自定义结尾 (end) - 进度条效果
print("Loading...", end="")
print("Done")  # 输出: Loading...Done (两行合并)

# 输出到文件 (file)
with open("log.txt", "w") as f:
    print("写入日志", file=f)
```

### 2.2 `input()`: 获取用户输入

**函数签名**：`input(prompt='')`

| 参数 | 类型 | 默认值 | 说明 |
| :--- | :--- | :--- | :--- |
| `prompt` | 字符串 | `''` (空) | **提示文本**。显示在用户输入前，如 `"请输入姓名: "` |

**注意**：`input()` 永远返回**字符串**。

```python
name = input("请输入姓名: ")
age = int(input("请输入年龄: "))  # 必须手动转换为数字
```

---

## 3. 数据类型转换

Python 提供了一组函数用于类型转换，这是处理数据清洗的核心工具。

| 函数 | 说明 | 示例 | 结果 |
| :--- | :--- | :--- | :--- |
| `int(x)` | 转为整数 | `int("3.14")` (报错), `int(3.14)` | `3` |
| `float(x)` | 转为浮点数 | `float("3.14")` | `3.14` |
| `str(x)` | 转为字符串 | `str(100)` | `"100"` |
| `bool(x)` | 转为布尔值 | `bool("")`, `bool(1)` | `False`, `True` |
| `list(x)` | 转为列表 | `list((1, 2))` | `[1, 2]` |
| `tuple(x)` | 转为元组 | `tuple([1, 2])` | `(1, 2)` |
| `set(x)` | 转为集合 (去重) | `set([1, 1, 2])` | `{1, 2}` |
| `dict(x)` | 转为字典 | `dict([("a", 1)])` | `{"a": 1}` |

---

## 4. 数学与数值运算

处理数字时，这些函数比引入 `math` 模块更轻量。

### 4.1 `abs()` 与 `round()`
```python
print(abs(-10))       # 10 (绝对值)
print(round(3.14159, 2)) # 3.14 (保留两位小数)
print(round(2.5))     # 2 (银行家舍入法：四舍六入五成双)
print(round(3.5))     # 4
```

### 4.2 `max()`, `min()` 与 `sum()`

这三个函数是处理数值集合的利器，都支持**自定义比较规则**。

#### `max()` 参数详解

**函数签名**：`max(iterable, *, key=None, default=None)` 或 `max(arg1, arg2, *args, key=None)`

| 参数 | 类型 | 默认值 | 说明 |
| :--- | :--- | :--- | :--- |
| `iterable` | 可迭代对象 | 必填 | **数据源**。如列表、元组、字典等 |
| `key` | 函数 | `None` | **比较依据**。传入一个函数，用函数的返回值作为比较标准 |
| `default` | 任意值 | `None` | **默认值**。当 `iterable` 为空时返回此值，否则报错 |

```python
nums = [10, 5, 20, 8]
print(max(nums))      # 20 (直接比较数值大小)

# key 参数详解：比较字典中的某个字段
users = [{"name": "Alice", "age": 18}, {"name": "Bob", "age": 25}]

# key=lambda u: u["age"] 表示：用每个元素的 "age" 字段来比较大小
# max 会遍历 users，对每个元素调用 lambda，返回最大的那个原始元素
print(max(users, key=lambda u: u["age"]))  
# 输出: {'name': 'Bob', 'age': 25}

# 空列表保护
empty = []
print(max(empty, default=0))  # 0 (不报错)
```

#### `min()` 参数详解
参数与 `max()` 完全一致，只是返回最小值。

```python
nums = [10, 5, 20, 8]
print(min(nums))      # 5
print(min(users, key=lambda u: u["age"]))  # {'name': 'Alice', 'age': 18}
```

#### `sum()` 参数详解

**函数签名**：`sum(iterable, start=0)`

| 参数 | 类型 | 默认值 | 说明 |
| :--- | :--- | :--- | :--- |
| `iterable` | 可迭代对象 | 必填 | **数据源**。必须是数字序列 |
| `start` | 数字 | `0` | **起始值**。累加的初始值，常用于拼接列表等技巧 |

```python
nums = [10, 5, 20, 8]
print(sum(nums))      # 43

# start 参数技巧：拼接列表（不推荐，效率低）
lists = [[1, 2], [3, 4]]
print(sum(lists, start=[]))  # [1, 2, 3, 4]
```

### 4.3 `pow()` 与 `divmod()`
```python
print(pow(2, 10))     # 1024 (等同于 2 ** 10)
print(pow(2, 10, 3))  # 1 (等同于 (2 ** 10) % 3，大数取模极快)

print(divmod(10, 3))  # (3, 1) (商，余数)，常用于分页计算
```

---

## 5. 序列与迭代操作

这是 Python 中最优雅的部分，极大简化循环逻辑。

### 5.1 `range()`: 整数序列生成器

**函数签名**：`range(stop)` 或 `range(start, stop[, step])`

| 参数 | 类型 | 默认值 | 说明 |
| :--- | :--- | :--- | :--- |
| `start` | 整数 | `0` | **起始值**。包含在序列中 |
| `stop` | 整数 | 必填 | **结束值**。**不包含**在序列中（重点！） |
| `step` | 整数 | `1` | **步长**。每次递增的值，可为负数（倒序） |

**核心规则**：`range` 生成的是 `[start, stop)` 区间的序列，**包头不包尾**。

```python
list(range(5))        # [0, 1, 2, 3, 4]   (start=0, stop=5)
list(range(1, 5))     # [1, 2, 3, 4]     (start=1, stop=5)
list(range(0, 10, 2)) # [0, 2, 4, 6, 8]  (step=2，跳着走)
list(range(5, 0, -1)) # [5, 4, 3, 2, 1]  (step=-1，倒序)
```

> **注意**：`range()` 返回的是**range 对象**（可迭代对象），不占用内存。它不是迭代器——`range` 对象支持 `len()`、多次遍历和索引访问，而迭代器不行。只有用 `list()` 转换时才会生成完整列表。

### 5.2 `len()`: 获取长度
```python
print(len("Python"))  # 6
print(len([1, 2, 3])) # 3
```

### 5.3 `enumerate()`: 索引与值同时获取

**函数签名**：`enumerate(iterable, start=0)`

| 参数 | 类型 | 默认值 | 说明 |
| :--- | :--- | :--- | :--- |
| `iterable` | 可迭代对象 | 必填 | **数据源**。列表、字符串、字典等 |
| `start` | 整数 | `0` | **索引起始值**。默认从 0 开始，可改为 1 |

**返回值**：生成 `(index, value)` 元组的迭代器。

```python
fruits = ["apple", "banana", "cherry"]

# 默认从 0 开始
for index, fruit in enumerate(fruits):
    print(f"索引 {index}: {fruit}")
# 输出: 索引 0: apple, 索引 1: banana...

# start=1：模拟"第 N 个"的计数
for index, fruit in enumerate(fruits, start=1):
    print(f"第{index}个水果: {fruit}")
# 输出: 第1个水果: apple, 第2个水果: banana...
```

### 5.4 `zip()`: 拉链式合并

**函数签名**：`zip(*iterables, strict=False)`

| 参数 | 类型 | 默认值 | 说明 |
| :--- | :--- | :--- | :--- |
| `*iterables` | 多个可迭代对象 | 必填 | **数据源**。传入多个序列，如 `zip(a, b, c)` |
| `strict` | 布尔值 | `False` | **严格模式 (3.10+)**。设为 `True` 时，长度不一致会报错 |

**返回值**：生成 `(item1, item2, ...)` 元组的迭代器。

```python
names = ["Alice", "Bob", "Charlie"]
ages = [20, 30]

# 默认：按最短的截断（多余的会被丢弃）
for name, age in zip(names, ages):
    print(f"{name}: {age}")
# 输出: Alice: 20, Bob: 30 (Charlie 被丢弃了！)

# 构造字典（经典用法）
print(dict(zip(names, ages)))  
# 输出: {'Alice': 20, 'Bob': 30}

# strict=True：长度不一致时报错（避免数据丢失）
# zip(names, ages, strict=True)  # ValueError: zip() argument 2 is shorter
```

### 5.5 `sorted()`: 排序神器

**函数签名**：`sorted(iterable, key=None, reverse=False)`

| 参数 | 类型 | 默认值 | 说明 |
| :--- | :--- | :--- | :--- |
| `iterable` | 可迭代对象 | 必填 | **数据源**。列表、元组、字典等 |
| `key` | 函数 | `None` | **排序依据**。用函数返回值作为排序标准 |
| `reverse` | 布尔值 | `False` | **是否倒序**。`True` 为降序，`False` 为升序 |

**返回值**：**新列表**（不修改原数据）。

```python
nums = [3, 1, 2]

# 基础排序
new_nums = sorted(nums, reverse=True)
print(new_nums) # [3, 2, 1]
print(nums)     # [3, 1, 2] (原列表不变)

# key 参数详解：按字符串长度排序
words = ["banana", "pie", "apple"]
print(sorted(words, key=len))  
# ['pie', 'apple', 'banana'] (按长度从小到大)

# key 参数详解：按字典字段排序
students = [{"name": "Bob", "score": 85}, {"name": "Alice", "score": 90}]
print(sorted(students, key=lambda s: s["score"], reverse=True))
# [{'name': 'Alice', 'score': 90}, ...] (按分数降序)
```

### 5.6 `reversed()`: 反转序列

**函数签名**：`reversed(sequence)`

| 参数 | 类型 | 说明 |
| :--- | :--- | :--- |
| `sequence` | 序列对象 | **数据源**。必须是支持索引的对象（如列表、字符串），不能是生成器 |

**返回值**：反转迭代器（不直接返回列表）。

```python
nums = [1, 2, 3]
rev_nums = list(reversed(nums))
print(rev_nums) # [3, 2, 1]
```

---

## 6. 函数式编程核心

### 6.1 `map()`: 映射

**函数签名**：`map(function, iterable, *iterables)`

| 参数 | 类型 | 说明 |
| :--- | :--- | :--- |
| `function` | 函数 | **处理函数**。对每个元素执行的转换逻辑 |
| `iterable` | 可迭代对象 | **数据源**。被处理的序列 |
| `*iterables` | 多个可迭代对象 | **多数据源**。传入多个序列时，函数需接收多个参数 |

**返回值**：迭代器（惰性计算，不占内存）。

```python
nums = [1, 2, 3]

# 单序列映射：每个元素平方
squared = list(map(lambda x: x**2, nums)) 
print(squared)  # [1, 4, 9]

# 多序列映射：向量加法
a = [1, 2]
b = [10, 20]
added = list(map(lambda x, y: x + y, a, b))
print(added)  # [11, 22]

# 实战技巧：配合生成器表达式省括号
total = sum(map(int, ["1", "2", "3"]))  # 6
```

### 6.2 `filter()`: 过滤

**函数签名**：`filter(function, iterable)`

| 参数 | 类型 | 说明 |
| :--- | :--- | :--- |
| `function` | 函数或 `None` | **筛选函数**。返回 `True` 的元素保留；若传 `None`，保留所有真值元素 |
| `iterable` | 可迭代对象 | **数据源** |

**返回值**：迭代器。

```python
nums = [1, 2, 3, 4, 5, 6]

# 过滤偶数
evens = list(filter(lambda x: x % 2 == 0, nums))
print(evens)  # [2, 4, 6]

# function=None：过滤掉所有"假值"（0, None, "", False）
values = [0, 1, "hello", "", None, True]
truthy = list(filter(None, values))
print(truthy)  # [1, 'hello', True]
```

---

### 6.3 `any()` 与 `all()`: 逻辑聚合

这两个函数用于判断可迭代对象中的元素是否**部分满足**或**全部满足**某个条件。它们是布尔逻辑的"聚合器"，非常适合与**生成器表达式**配合使用。

#### `any()`: 只要有一个为真

**函数签名**：`any(iterable)`

| 参数 | 类型 | 说明 |
| :--- | :--- | :--- |
| `iterable` | 可迭代对象 | **数据源**。包含任意元素的序列 |

**返回值**：`bool`。如果**至少有一个**元素的布尔值为 `True`，返回 `True`；否则返回 `False`。如果可迭代对象为空，返回 `False`。

**短路特性**：一旦发现第一个为真的元素，立即返回 `True`，不再检查剩余元素。

```python
scores = [50, 60, 95, 40]

# 判断是否有人及格 (>=60)
has_passed = any(s >= 60 for s in scores)
print(has_passed)  # True (因为 60 和 95 满足条件)

# 判断是否包含特定字符
text = "Python is fun!"
print(any(char.isdigit() for char in text))  # False (没有数字)
```

#### `all()`: 全部为真

**函数签名**：`all(iterable)`

| 参数 | 类型 | 说明 |
| :--- | :--- | :--- |
| `iterable` | 可迭代对象 | **数据源** |

**返回值**：`bool`。如果**所有**元素的布尔值都为 `True`，返回 `True`；否则返回 `False`。如果可迭代对象为空，返回 `True`（空真）。

**短路特性**：一旦发现第一个为假的元素，立即返回 `False`。

```python
scores = [60, 75, 80, 90]

# 判断是否全部及格
all_passed = all(s >= 60 for s in scores)
print(all_passed)  # True

# 判断是否包含非法字符（全是字母和数字）
password = "pass123"
is_valid = all(c.isalnum() for c in password)
print(is_valid)  # True

# 空列表的情况
print(all([]))  # True (空集逻辑为真)
```

#### 组合实战：数据校验

这两个函数常用于数据清洗和校验：

```python
users = [
    {"name": "Alice", "age": 20, "email": "alice@test.com"},
    {"name": "Bob", "age": 30, "email": "bob@test.com"},
]

# 校验 1: 是否所有人的邮箱都包含 '@' ?
valid_emails = all("@" in u["email"] for u in users)
print(valid_emails)  # True

# 校验 2: 是否有人未成年 (<18) ?
has_minor = any(u["age"] < 18 for u in users)
print(has_minor)  # False

# 常见陷阱：不要用 list 推导式，用生成器表达式省内存
# ✅ 推荐（惰性求值，短路后停止）
any(x > 100 for x in range(1000000))

# ❌ 不推荐（立即创建完整列表，浪费内存）
any([x > 100 for x in range(1000000)])
```

---

## 7. 对象属性与类型检查

### 7.1 `type()` 与 `isinstance()`
```python
x = [1, 2]
print(type(x) == list)           # True
print(isinstance(x, list))       # True (推荐，支持继承判断)
```

### 7.2 `dir()`: 查看属性
查看对象支持的所有方法和属性。
```python
print(dir("string"))  # 查看字符串有哪些方法，如 upper, split...
```

### 7.3 `id()`: 内存地址
```python
a = 10
b = 10
print(id(a) == id(b))  # True (小整数缓存)
```

### 7.4 `hasattr()`, `getattr()`, `setattr()`
动态操作对象属性，常用于编写通用框架或反射机制。

```python
class User:
    def __init__(self):
        self.name = "Alice"

u = User()
print(hasattr(u, "name"))  # True
print(getattr(u, "name"))  # Alice
setattr(u, "age", 18)      # 动态添加属性
print(u.age)               # 18
```

---

## 8. 其他重要函数

### 8.1 `open()`: 文件操作
```python
# 推荐写法：使用上下文管理器自动关闭文件
with open("test.txt", "w", encoding="utf-8") as f:
    f.write("Hello")
```

### 8.2 `eval()` 与 `exec()`
*   `eval(expression)`: 执行字符串表达式并**返回值**。
*   `exec(statement)`: 执行字符串代码块，**不返回值**。

> **警告**：严禁对用户输入直接使用 `eval`，存在严重的安全漏洞（代码注入风险）。

```python
result = eval("1 + 1")
print(result)  # 2

exec("x = 10; print(x)")  # 10
```

---

## 9. 综合实战

### 案例：内置函数组合应用

以下示例来自 `app/core/builtins.py`，展示了 `min`/`max`/`sum`/`len`、`sorted` + `enumerate`、`all` 等内置函数的实际组合用法。

```python
from app.core.builtins import score_stats, rank_students, all_passed

scores = [85, 92, 55, 60, 99]

# 统计 (min, max, sum, len)
print(score_stats(scores))
# {'min': 55, 'max': 99, 'total': 391, 'count': 5, 'average': 78.2}

students = [
    {"name": "Alice", "score": 85},
    {"name": "Bob", "score": 92},
]

# 排名 (sorted + enumerate)
print(rank_students(students))
# [(1, {'name': 'Bob', 'score': 92}), (2, {'name': 'Alice', 'score': 85})]

# 校验 (all)
print(all_passed(students, 90))  # False (Alice < 90)
```

**关键代码说明：**

| 代码 | 含义 | 为什么这样写 |
|------|------|-------------|
| `min(scores)` / `max(scores)` | 获取最低/最高分 | 内置函数 C 实现，比手动遍历更快 |
| `sum(scores) / len(scores)` | 计算平均值 | `sum` 和 `len` 均为 O(n)/O(1) 高效操作 |
| `sorted(students, key=..., reverse=True)` | 按分数降序排序 | `sorted` 返回新列表，不修改原始数据 |
| `enumerate(sorted_list, start=1)` | 从 1 开始生成名次 | 替代手动维护计数器，代码更简洁 |
| `all(s["score"] >= threshold for s in students)` | 检查是否全部达标 | 生成器表达式 + 短路求值，遇到不满足立即返回 `False` |

---

## L2 实践层：最佳实践

### 推荐做法

| 做法 | 原因 | 示例 |
|------|------|------|
| **enumerate 替代 range(len)** | 更 Pythonic，同时获取索引和值 | `for i, v in enumerate(data):` |
| **zip 并行遍历** | 避免手动索引，代码更清晰 | `for name, score in zip(names, scores):` |
| **sorted 的 key 参数** | 比自定义比较函数更简洁高效 | `sorted(items, key=lambda x: x["age"])` |
| **生成器表达式 + any/all** | 惰性求值 + 短路，节省内存 | `any(x > 0 for x in data)` |
| **用 isinstance 而非 type** | 支持继承判断，更健壮 | `isinstance(x, int)` 而非 `type(x) == int` |
| **上下文管理器操作文件** | 自动关闭，防止资源泄漏 | `with open(...) as f:` |

### 反模式：不要这样做

```python
# ❌ 用 range(len(...)) 遍历
for i in range(len(fruits)):
    print(fruits[i])

# ✅ 用 enumerate
for i, fruit in enumerate(fruits):
    print(f"第{i}个: {fruit}")
```

```python
# ❌ 手动并行遍历
for i in range(len(names)):
    print(names[i], scores[i])

# ✅ 用 zip
for name, score in zip(names, scores):
    print(f"{name}: {score}")
```

```python
# ❌ sorted + lambda 做简单属性取值
sorted(students, key=lambda s: s["score"])

# ✅ 如果只需按单一属性排序，operator.itemgetter 更快
from operator import itemgetter
sorted(students, key=itemgetter("score"))
```

```python
# ❌ 对 eval 传入用户输入
user_input = input("请输入表达式: ")
result = eval(user_input)  # 严重安全漏洞！

# ✅ 用 ast.literal_eval 解析安全字面量
import ast
user_input = input("请输入列表: ")
result = ast.literal_eval(user_input)  # 只解析字面量，不执行代码
```

```python
# ❌ 用 sum 拼接列表（O(n²) 性能）
lists = [[1, 2], [3, 4], [5, 6]]
result = sum(lists, start=[])  # 每次拼接都创建新列表

# ✅ 用列表推导式或 itertools.chain
result = [x for sub in lists for x in sub]  # O(n)

from itertools import chain
result = list(chain.from_iterable(lists))  # O(n)，更高效
```

### 适用场景

| 场景 | 是否推荐 | 原因 |
|------|---------|------|
| 数据统计（min/max/sum/len） | ✅ 推荐 | C 实现，比手动循环快 |
| 排序与排名（sorted + key） | ✅ 推荐 | 灵活且不修改原数据 |
| 并行遍历（zip） | ✅ 推荐 | 比手动索引安全 |
| 数据校验（any/all） | ✅ 推荐 | 短路求值，性能好 |
| 类型转换 | ✅ 推荐 | 内置函数，零依赖 |
| eval 执行字符串 | ❌ 不推荐 | 安全风险极高 |
| sum 拼接列表 | ❌ 不推荐 | O(n²) 性能问题 |

---

## L3 专家层：底层原理

### 内置函数的 C 实现优势

Python 的内置函数大多用 C 实现，比纯 Python 循环快 10-100 倍。

```python
import timeit

data = list(range(10000))

# 纯 Python 循环求和
def loop_sum(nums):
    total = 0
    for n in nums:
        total += n
    return total

# 内置 sum
loop_time = timeit.timeit("loop_sum(data)", globals=globals(), number=1000)
builtin_time = timeit.timeit("sum(data)", globals=globals(), number=1000)

print(f"纯 Python: {loop_time:.4f}s")
print(f"内置 sum:  {builtin_time:.4f}s")
# 纯 Python: 0.35s
# 内置 sum:  0.02s  ← 快约 15 倍
```

**性能对比表：**

| 操作 | 纯 Python | 内置函数 | 加速比 |
|------|----------|---------|--------|
| 求和 | for 循环 | `sum()` | ~15x |
| 最大值 | for + if | `max()` | ~10x |
| 排序 | 手动冒泡 | `sorted()` | ~50x |
| 成员检查 | for + == | `in`（集合） | ~100x |

### sorted() 的 TimSort 算法

Python 的 `sorted()` 使用 **TimSort** 算法，是一种混合了归并排序和插入排序的高效算法。

```
TimSort 特性：
┌─────────────────────────────────────────────────────────────┐
│                   TimSort 算法特点                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  时间复杂度：                                                │
│  • 最优：O(n)    ← 数据已部分有序时                         │
│  • 平均：O(n log n)                                        │
│  • 最差：O(n log n)                                        │
│                                                             │
│  空间复杂度：O(n)                                           │
│                                                             │
│  核心优化：                                                  │
│  • 识别"有序子序列"（run），直接利用不重排                   │
│  • 小段用插入排序（常数因子更小）                            │
│  • 稳定排序：相同 key 的元素保持原始顺序                    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

```python
# 稳定排序的验证
students = [
    {"name": "Alice", "score": 85},
    {"name": "Bob", "score": 85},
    {"name": "Charlie", "score": 92},
]

# 按分数排序，Alice 和 Bob 分数相同，顺序不变
result = sorted(students, key=lambda s: s["score"])
# Alice 仍在 Bob 前面（稳定排序保证）
```

### 可迭代对象 vs 迭代器 vs 生成器

内置函数中很多返回"迭代器"，理解这三者的区别很重要。

```
┌─────────────────────────────────────────────────────────────┐
│          可迭代对象 vs 迭代器 vs 生成器                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  可迭代对象（Iterable）：                                    │
│  • 实现了 __iter__() 方法                                   │
│  • 可以被 for 遍历                                          │
│  • 可以重复遍历                                             │
│  • 例：list, str, dict, range, set                          │
│                                                             │
│  迭代器（Iterator）：                                        │
│  • 同时实现 __iter__() 和 __next__() 方法                   │
│  • 惰性求值，按需生成元素                                   │
│  • 只能遍历一次，耗尽后抛 StopIteration                     │
│  • 例：map, filter, zip, enumerate, reversed 的返回值       │
│                                                             │
│  生成器（Generator）：                                       │
│  • 迭代器的子集，用 yield 或生成器表达式创建                 │
│  • 例：(x**2 for x in range(10))                           │
│                                                             │
│  ⚠️ range 是可迭代对象，不是迭代器！                        │
│  • range 支持 len()、索引访问、重复遍历                     │
│  • 迭代器不支持这些操作                                     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

```python
# range 不是迭代器
r = range(5)
print(len(r))    # 5 ← 迭代器没有 len
print(r[2])      # 2 ← 迭代器不支持索引
print(list(r))   # [0, 1, 2, 3, 4]
print(list(r))   # [0, 1, 2, 3, 4] ← 可以重复遍历

# map 是迭代器
m = map(str, [1, 2, 3])
# print(len(m))  # TypeError ← 迭代器没有 len
print(list(m))   # ['1', '2', '3']
print(list(m))   # [] ← 耗尽了，只能遍历一次
```

### key 参数的内部机制

`sorted()`、`min()`、`max()` 的 `key` 参数内部使用 **Schwartzian 变换**（装饰-排序-去装饰）。

```python
# sorted 内部等价逻辑（简化版）
def sorted_with_key(iterable, key=None, reverse=False):
    if key is None:
        return sorted(iterable, reverse=reverse)

    # 1. 装饰：对每个元素计算 key 值，打包为 (key_value, original)
    decorated = [(key(item), item) for item in iterable]

    # 2. 排序：按 key_value 排序（每个元素的 key 只计算一次）
    decorated.sort(reverse=reverse)

    # 3. 去装饰：取出原始元素
    return [item for _, item in decorated]

# 优势：key 函数对每个元素只调用一次
# 而传统的 cmp 函数每对元素比较都要调用，O(n log n) 次比较
```

### 设计动机

Python 为什么把这些函数设计为内置？

| 设计选择 | 原因 | 替代方案对比 |
|----------|------|-------------|
| 内置而非模块 | 高频使用，省去 import | Java 的 Collections.sort() 需导入 |
| key 而非 cmp | 每元素调用一次 vs 每对比较调用 | Python 2 的 cmp 已废弃 |
| 返回迭代器 | 惰性求值，节省内存 | Python 2 的 map/filter 返回列表 |
| range 不生成列表 | 惰性范围对象，O(1) 内存 | Python 2 的 range() 生成完整列表 |
| sorted 返回新列表 | 不修改原数据，纯函数风格 | list.sort() 原地修改 |

### 知识关联

```
内置函数知识关联图：
                    ┌───────────────┐
                    │   C 实现      │
                    │   性能优势    │
                    └───────────────┘
                          │
                          ↓
┌─────────────┐     ┌───────────────┐     ┌───────────────┐
│  TimSort    │────→│  sorted/key   │────→│ Schwartzian   │
│  稳定排序   │     │  机制         │     │ 变换          │
└─────────────┘     └───────────────┘     └───────────────┘
                          │
                          ↓
                    ┌───────────────┐
                    │ 迭代器 vs     │
                    │ 可迭代对象    │
                    └───────────────┘
                          │
                          ↓
                    ┌───────────────┐
                    │   装饰器      │
                    │   函数包装    │
                    └───────────────┘
```

---

## 本章小结

```
┌─────────────────────────────────────────────────────────────┐
│                   内置函数核心记忆图谱                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  L1 理解层：                                                │
│  输入输出：print(sep, end), input                           │
│  类型转换：int, float, str, bool, list, tuple, set, dict    │
│  数值运算：abs, round, max, min, sum, divmod, pow           │
│  迭代操作：range, len, enumerate, zip, sorted, reversed     │
│  高阶函数：map, filter, any, all                              │
│  对象检查：type, isinstance, id, dir, callable              │
│                                                             │
│  ★ 重点推荐：                                               │
│  1. enumerate 替代 range(len(...))                         │
│  2. zip 用于并行遍历                                        │
│  3. sorted 的 key 参数                                      │
│                                                             │
│  L2 实践层：                                                │
│  ✓ enumerate/zip 替代手动索引                               │
│  ✓ 生成器表达式 + any/all 短路求值                          │
│  ✓ isinstance 优于 type 检查                                │
│  ✓ 禁止 eval 用户输入，用 ast.literal_eval                  │
│  ✓ sum 拼接列表是 O(n²)，用 itertools.chain                │
│                                                             │
│  L3 专家层：                                                │
│  ✓ 内置函数 C 实现，比纯 Python 快 10-100 倍               │
│  ✓ sorted 使用 TimSort（稳定、自适应 O(n)~O(n log n)）     │
│  ✓ range 是可迭代对象不是迭代器，支持 len/索引/重复遍历     │
│  ✓ key 参数使用 Schwartzian 变换，每元素只计算一次          │
│  ✓ 迭代器只能遍历一次，可迭代对象可重复遍历                 │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 交互演示

运行项目 CLI 查看本章代码的实际执行效果：

```bash
cd functions_demo && uv run python -m app   # 选 5
```
