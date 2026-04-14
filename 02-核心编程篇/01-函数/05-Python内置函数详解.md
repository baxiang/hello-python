# Python 内置函数详解

> **本章基于 Python 3.11+**
>
> Python 内置了 70+ 个高频使用的函数。这些函数不需要导入任何模块即可直接使用，它们构成了 Python 开发的基石。

---

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

## 3. 函数的定义与参数基础

在深入学习内置函数之前，我们需要快速复习一下函数的语法。**理解“参数传递方式”是掌握内置函数高级用法（如 `key` 参数）的前提。**

### 3.1 函数的基本结构
```python
def 函数名(参数 1, 参数 2):
    # 函数体
    return 返回值
```

### 3.2 核心：三种参数传递方式

Python 函数调用非常灵活，主要分为以下三种情况：

#### 1. 位置参数 (Positional Arguments)
**按顺序传值**，这是最基础的方式。
*   **示例**：`pow(2, 10)`
    *   第 1 个位置传 `2`（底数）。
    *   第 2 个位置传 `10`（指数）。
    *   **规则**：顺序不能乱，必须对应函数的定义。

#### 2. 关键字参数 (Keyword Arguments)
**通过 `参数名=值` 的形式传值**。
*   **示例**：`max(data, key=len)`
    *   `data` 是位置参数。
    *   `key=len` 是关键字参数。
*   **优势**：
    1.  **顺序不限**：`max(key=len, iterable=data)` 效果一样。
    2.  **可读性强**：看到 `key` 就知道是在指定比较依据。
*   **应用**：内置函数中大量的可选配置（如 `print` 的 `sep`, `end`, `file`）都通过这种方式设置。

#### 3. 默认参数 (Default Arguments)
函数定义时预设了值，**调用时可以省略**。
*   **示例**：`int("100")`
    *   函数定义其实是 `int(x, base=10)`。
    *   因为我们平时都转十进制，所以省略了 `base`。
*   **规则**：如果你想转二进制，就需要显式传入：`int("1010", base=2)`。

### 3.3 避坑指南
在调用内置函数时，**位置参数必须放在关键字参数前面**。
*   ❌ 错误：`max(key=len, data)` (关键字参数跑到了位置参数前面)
*   ✅ 正确：`max(data, key=len)`

---

## 4. 数据类型转换

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

> **注意**：`range()` 返回的是**迭代器对象**，不占用内存。只有用 `list()` 转换时才会生成完整列表。

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

### 案例：数据处理流水线
**需求**：有一组杂乱的字符串数字，过滤掉非数字字符，计算平均值，并保留两位小数。

```python
data = ["10", "20", "abc", "30", "", "50"]

# 1. 过滤并转换 (列表推导式通常比 map+filter 更易读)
valid_nums = [int(x) for x in data if x.isdigit()]

# 2. 计算总和与平均值
total = sum(valid_nums)
average = round(total / len(valid_nums), 2) if valid_nums else 0

print(f"有效数据: {valid_nums}")
print(f"总和: {total}, 平均值: {average}")
```

**关键代码说明：**

| 代码 | 含义 | 为什么这样写 |
|------|------|-------------|
| `x.isdigit()` | 过滤掉非纯数字字符串 | 避免 `int("")`、`int("abc")` 引发 ValueError |
| `[int(x) for x in data if x.isdigit()]` | 过滤并转换一步完成 | 列表推导式比 `map`+`filter` 更易读，且只遍历一次 |
| `round(total / len(valid_nums), 2)` | 保留两位小数 | `round` 内置实现精确舍入，比字符串格式化更适合用于后续计算 |
| `if valid_nums else 0` | 防止空列表除零 | 过滤后可能没有有效数据，需要在使用前做空值保护 |

---

## 本章小结

```
┌─────────────────────────────────────────────────────────────┐
│                   内置函数核心记忆图谱                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  输入输出：print(sep, end), input                           │
│  类型转换：int, float, str, bool, list, tuple, set, dict    │
│  数值运算：abs, round, max, min, sum, divmod, pow           │
│  迭代操作：range, len, enumerate, zip, sorted, reversed     │
│  高阶函数：map, filter                                      │
│  对象检查：type, isinstance, id, dir, callable              │
│                                                             │
│  ★ 重点推荐：                                               │
│  1. enumerate 替代 range(len(...))                         │
│  2. zip 用于并行遍历                                        │
│  3. sorted 的 key 参数                                      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```
