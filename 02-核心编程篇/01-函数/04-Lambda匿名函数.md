# 04-Lambda匿名函数

> **Python 版本要求**：Python 3.11+
> **贯穿项目**：functions_demo/
> **代码位置**：`app/core/builtins.py`
> **测试验证**：`cd functions_demo && uv run pytest -k TestLambda -v`

> **本章代码基于 Python 3.11+ 编写**
>
> Lambda 是一种简洁的匿名函数，适合简单的、一次性使用的场景。

---

## 为什么需要 Lambda？一个真实的排序场景

**问题场景：**
你有一个学生成绩列表，需要按不同字段排序。

**定义函数的麻烦：**

```python
students = [
    {"name": "张三", "score": 85},
    {"name": "李四", "score": 92},
    {"name": "王五", "score": 78}
]

# 按分数排序 - 需要定义一个函数
def get_score(student):
    return student["score"]

sorted_students = sorted(students, key=get_score)
print(sorted_students)

# 按姓名排序 - 又要定义一个函数
def get_name(student):
    return student["name"]

sorted_by_name = sorted(students, key=get_name)
```

**问题：**
- 每个排序规则都要定义一个函数
- 这些函数只用一次，定义了就扔
- 代码冗余，不够简洁

**使用 Lambda 的解决方案：**

```python
students = [
    {"name": "张三", "score": 85},
    {"name": "李四", "score": 92},
    {"name": "王五", "score": 78}
]

# 按分数排序 - 一行搞定
by_score = sorted(students, key=lambda s: s["score"])
print(by_score)

# 按姓名排序 - 一行搞定
by_name = sorted(students, key=lambda s: s["name"])
print(by_name)
```

这就是 Lambda 的价值：**用一行代码替代简单的一次性函数**。

---

## Lambda 解决了什么问题？

Lambda 的本质是：**无需命名的轻量级函数**。

就像便利贴 vs 正式文件：
- Lambda：便利贴，快速记录，用完即扔
- def 函数：正式文件，需要保存，反复使用

**Lambda 的优势：**

1. **简洁**：一行代码定义函数
2. **即用**：不需要起名字
3. **内联**：直接写在调用处

**Lambda 的限制：**
- 只能有一个表达式
- 不能写复杂逻辑
- 没有文档字符串

---

## Lambda 的最简用法

```python
# 定义 lambda
square = lambda x: x ** 2

# 调用
print(square(5))  # 25

# 与普通函数对比
def square_func(x: int) -> int:
    return x ** 2

print(square_func(5))  # 25
```

---

## 第一部分：Lambda 基础语法

### 概念说明

**Lambda（匿名函数）** 是一种无需命名就能直接使用的迷你函数。

```
┌─────────────────────────────────────────────────────────────┐
│              Lambda 表达式的结构                              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   lambda  参数1, 参数2, ...  :  表达式                      │
│      │         │                  │                         │
│      │         │                  └─ 自动作为返回值          │
│      │         └─ 可以有多个参数，也可以没有                 │
│      └─ 关键字，固定写法                                      │
│                                                             │
│   三大限制：                                                 │
│   • 只能有一个表达式（不能写多行）                           │
│   • 不需要写 return（自动返回表达式结果）                    │
│   • 不能有 if/for/while 等语句（可以用三元表达式）           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Lambda 与普通函数对比

```
Lambda vs def：
┌─────────────────────────────────────────────────────────────┐
│  Lambda 与 def 函数对比                                        │
│                                                              │
│  def 函数：                                                    │
│  ─────────────────────────────                               │
│  def add(a, b):                                               │
│      return a + b                                             │
│                                                              │
│  Lambda：                                                     │
│  ─────────────────────────────                               │
│  lambda a, b: a + b                                           │
│                                                              │
│  ⚠️ Lambda 限制：                                              │
│  • 只能有一个表达式                                            │
│  • 不需要写 return（自动返回）                                 │
│  • 不能有复杂语句（if/for/while，可用三元表达式）               │
│  • 没有文档字符串                                              │
└─────────────────────────────────────────────────────────────┘
```

### 最简示例

```python
# 方式 1：普通函数
def add(a: int, b: int) -> int:
    return a + b

# 方式 2：Lambda 函数
add_lambda = lambda a, b: a + b

print(add(3, 5))         # 8
print(add_lambda(3, 5))  # 8
```

### 关键代码解释

| 代码 | 含义 | 说明 |
|------|------|------|
| `lambda` | 关键字 | 固定写法 |
| `a, b` | 参数 | 可有多个或无参数 |
| `a + b` | 表达式 | 自动作为返回值 |

### 详细示例

```python
# 方式 3：立即调用（IIFE）
result = (lambda a, b: a + b)(3, 5)
print(result)  # 8
```

---

| 特性 | 普通函数（def） | Lambda 函数 |
|------|----------------|-------------|
| 关键字 | `def` | `lambda` |
| 有无名字 | 有名字 | 匿名 |
| 行数 | 多行 | 只能一行 |
| 返回值 | 需要显式 `return` | 自动返回 |
| 文档字符串 | 可以写 | 不能写 |
| 适用场景 | 复杂逻辑 | 简单的一次性函数 |

---

## 第二部分：Lambda 的各种形式

```python
# ── 无参数 ────────────────────────────────────────
say_hi = lambda: "Hi!"
print(say_hi())  # Hi!

# ── 单参数 ────────────────────────────────────────
square = lambda x: x ** 2
print(square(5))  # 25

# ── 多参数 ────────────────────────────────────────
add = lambda a, b: a + b
print(add(3, 5))  # 8

# ── 带默认参数 ────────────────────────────────────
greet = lambda name, msg="你好": f"{msg}, {name}!"
print(greet("Alice"))  # 你好, Alice!

# ── 带条件判断（三元表达式）──────────────────────
max_value = lambda a, b: a if a > b else b
print(max_value(3, 7))  # 7
```

---

## 第三部分：Lambda 的核心使用场景

### 场景一：sorted() 自定义排序

```python
# ── 对元组列表排序 ────────────────────────────────
students = [("Alice", 85), ("Bob", 92), ("Charlie", 78)]

# 按分数（第二个元素）升序
by_score = sorted(students, key=lambda x: x[1])
print(by_score)
# [('Charlie', 78), ('Alice', 85), ('Bob', 92)]

# ── 对字典列表排序 ────────────────────────────────
products = [
    {"name": "Apple", "price": 5},
    {"name": "Banana", "price": 3},
    {"name": "Orange", "price": 8},
]

by_price = sorted(products, key=lambda x: x["price"])
for p in by_price:
    print(f'{p["name"]}: ¥{p["price"]}')
# Banana: ¥3
# Apple: ¥5
# Orange: ¥8
```

### 场景二：filter() 过滤数据

```python
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# 过滤偶数
evens = list(filter(lambda x: x % 2 == 0, numbers))
print(evens)  # [2, 4, 6, 8, 10]

# 过滤大于 5 的数
big = list(filter(lambda x: x > 5, numbers))
print(big)    # [6, 7, 8, 9, 10]
```

### 场景三：map() 转换数据

```python
numbers = [1, 2, 3, 4, 5]

# 每个数平方
squares = list(map(lambda x: x ** 2, numbers))
print(squares)  # [1, 4, 9, 16, 25]

# 字符串处理
words = ["hello", "world", "python"]
upper = list(map(lambda x: x.upper(), words))
print(upper)  # ['HELLO', 'WORLD', 'PYTHON']
```

### 场景四：reduce() 归约

```python
from functools import reduce

numbers = [1, 2, 3, 4, 5]

# 求和
total = reduce(lambda x, y: x + y, numbers)
print(total)  # 15

# 求积
product = reduce(lambda x, y: x * y, numbers)
print(product)  # 120
```

---

## 何时用 Lambda，何时用 def

```
┌──────────────────────────────────────────────────────────────┐
│               Lambda 使用决策树                               │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  这个函数会在多处复用吗？                                    │
│       ├─ 是  →  用 def（给它起个好名字）                     │
│       └─ 否                                                  │
│            │                                                 │
│            ▼                                                 │
│       逻辑超过一个表达式吗？                                 │
│       ├─ 是  →  用 def（lambda 写不了）                      │
│       └─ 否                                                  │
│            │                                                 │
│            ▼                                                 │
│       需要写注释/文档说明吗？                                │
│       ├─ 是  →  用 def（lambda 没有 docstring）              │
│       └─ 否  →  可以考虑 lambda ✅                           │
│                                                              │
├──────────────────────────────────────────────────────────────┤
│  ✅ Lambda 的最佳场景：                                      │
│  • sorted / min / max 的 key 参数                            │
│  • filter / map 的转换或过滤条件                             │
│  • 简单的数学表达式                                          │
│                                                              │
│  ❌ Lambda 不适合的场景：                                    │
│  • 超过一个表达式的逻辑                                      │
│  • 需要复用的函数                                            │
│  • 赋值给变量（直接用 def 更清晰）                           │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

---

## 渐进复杂：从简单到复杂的 Lambda

### 层级 1：简单表达式

```python
# 平方
square = lambda x: x ** 2

# 加法
add = lambda a, b: a + b
```

### 层级 2：带条件判断

```python
# 取最大值
max_val = lambda a, b: a if a > b else b

# 奇偶判断
is_even = lambda x: "偶数" if x % 2 == 0 else "奇数"
```

### 层级 3：在 sorted 中使用

```python
students = [
    {"name": "张三", "score": 85, "age": 18},
    {"name": "李四", "score": 92, "age": 19},
    {"name": "王五", "score": 78, "age": 17}
]

# 按分数降序
by_score = sorted(students, key=lambda s: s["score"], reverse=True)

# 按年龄升序
by_age = sorted(students, key=lambda s: s["age"])
```

### 层级 4：在 filter 和 map 中使用

```python
# 过滤及格的学生
data = [85, 42, 90, 58, 75, 30, 88]
passed = list(filter(lambda x: x >= 60, data))

# 转换成绩等级
grades = list(map(
    lambda x: "A" if x >= 90 else ("B" if x >= 80 else "C"),
    data
))
```

### 层级 5：链式调用

```python
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# 过滤偶数 -> 平方 -> 求和
result = sum(
    map(
        lambda x: x ** 2,
        filter(lambda x: x % 2 == 0, numbers)
    )
)
print(result)  # 2² + 4² + 6² + 8² + 10² = 4 + 16 + 36 + 64 + 100 = 220
```

**关键代码说明：**

| 代码 | 含义 | 为什么这样写 |
|------|------|-------------|
| `filter(lambda x: x % 2 == 0, numbers)` | 过滤出偶数 | 最内层先执行，筛选数据是后续操作的前提 |
| `map(lambda x: x ** 2, ...)` | 将每个元素平方 | 对已过滤的偶数集合做变换，`map` 保持惰性不立即计算 |
| `sum(...)` | 对结果求和 | 最外层聚合，三层嵌套体现"过滤→变换→归约"管道模式 |

---

## 实际应用：项目中的 Lambda

在 `functions_demo` 项目中，Lambda 与 `sorted`、`filter`、`map` 配合使用，构成了学生成绩处理的核心逻辑。

**项目代码：`app/core/builtins.py`**

```python
from app.core.builtins import sort_students, filter_passing, scale_scores

students = [
    {"name": "张三", "score": 75},
    {"name": "李四", "score": 92},
    {"name": "王五", "score": 55}
]

# sorted + lambda
sort_students(students)  
# 按分数升序: [{'name': '王五', 'score': 55}, ...]

# filter + lambda
filter_passing(students) 
# 筛选 >= 60: [{'name': '张三', ...}, {'name': '李四', ...}]

# map + lambda
scale_scores(students, 0.8)
# 缩放分数: [60.0, 73.6, 44.0]
```

**项目实现细节：**

```python
# app/core/builtins.py 中的 lambda 使用

def sort_students(students: list[dict], *, reverse: bool = False) -> list[dict]:
    """按分数排序（lambda 作为 sorted key）"""
    return sorted(students, key=lambda s: s["score"], reverse=reverse)

def filter_passing(students: list[dict], threshold: float = 60.0) -> list[dict]:
    """筛选及格学生（lambda + filter）"""
    return list(filter(lambda s: s["score"] >= threshold, students))

def scale_scores(students: list[dict], factor: float) -> list[float]:
    """等比缩放分数（lambda + map）"""
    return list(map(lambda s: round(s["score"] * factor, 2), students))
```

**关键代码说明：**

| 代码 | 含义 | 为什么这样写 |
|------|------|-------------|
| `sorted(students, key=lambda s: s["score"])` | 按分数排序 | lambda 内联在 `key` 参数中，符合"一次性使用"的最佳实践 |
| `filter(lambda s: s["score"] >= threshold, students)` | 过滤及格学生 | lambda 定义过滤条件，`filter` 返回迭代器，`list()` 转换为列表 |
| `map(lambda s: round(s["score"] * factor, 2), students)` | 缩放分数 | lambda 对每个学生做分数变换，`round` 控制精度 |

---

## L2 实践层：最佳实践

### 推荐做法

| 做法 | 原因 | 示例 |
|------|------|------|
| **用于简单一次性函数** | lambda 的核心定位，简洁不冗余 | `sorted(items, key=lambda x: x[0])` |
| **作为 key 参数** | sorted/min/max 的标准用法 | `max(users, key=lambda u: u["score"])` |
| **作为 filter/map 条件** | 函数式编程的惯用法 | `filter(lambda x: x > 0, nums)` |
| **保持简单** | 可读性优先，一行能读懂 | `lambda x: x * 2` |
| **避免赋值给变量** | def 函数更清晰，有名字和文档 | 不要写 `f = lambda x: x + 1` |
| **复杂逻辑用 def** | lambda 写不了多行，也难调试 | 多步骤逻辑拆成 def 函数 |

### 反模式：不要这样做

```python
# ❌ 把 lambda 赋值给变量（失去命名意义）
add = lambda a, b: a + b

# 问题：
# 1. lambda 本意是"匿名"，赋值给变量违背设计初衷
# 2. 没有 docstring，help(add) 看不到说明
# 3. 调试时函数名显示为 '<lambda>'，难以追踪
# 4. IDE 无法提供类型提示和参数信息
```

```python
# ✅ 正确做法：用 def 定义需要复用的函数
def add(a: int, b: int) -> int:
    """计算两个数的和"""
    return a + b

# 有名字、有文档、有类型提示
help(add)  # 可以查看文档
```

```python
# ❌ lambda 内写复杂逻辑
process = lambda x: (
    x * 2 if x > 0 else
    x * -1 if x < 0 else
    0
)

# 问题：
# 1. 多行三元表达式难以阅读
# 2. 无法添加注释
# 3. 无法处理异常
# 4. 维护困难
```

```python
# ✅ 正确做法：用 def 函数展开逻辑
def process(x: int) -> int:
    """处理数值：正数乘2，负数取反，零返回零"""
    if x > 0:
        return x * 2
    elif x < 0:
        return x * -1
    else:
        return 0

# 逻辑清晰，可以添加注释和异常处理
```

```python
# ❌ lambda 内调用复杂函数
validate = lambda data: (
    check_format(data) and
    check_length(data) and
    check_content(data) and
    check_signature(data)
)

# 问题：lambda 只适合简单表达式，不适合串联多个函数调用
```

```python
# ✅ 正确做法：用 def 函数组合逻辑
def validate(data: dict) -> bool:
    """验证数据完整性"""
    checks = [
        check_format,
        check_length,
        check_content,
        check_signature
    ]
    return all(check(data) for check in checks)

# 或者更直观的写法
def validate(data: dict) -> bool:
    if not check_format(data):
        return False
    if not check_length(data):
        return False
    if not check_content(data):
        return False
    if not check_signature(data):
        return False
    return True
```

```python
# ❌ lambda 内使用副作用操作
[print(x) for x in items]  # 用 lambda 但只是为了副作用

# 或
save_all = lambda items: [save(item) for item in items]

# 问题：
# 1. lambda 应返回有意义的结果，不只是执行操作
# 2. 副作用操作用 for 循环更清晰
# 3. 创建无用列表浪费内存
```

```python
# ✅ 正确做法：副作用操作用 for 循环
for x in items:
    print(x)

for item in items:
    save(item)

# 或者写一个正常的函数
def save_all(items: list) -> None:
    """保存所有项目"""
    for item in items:
        save(item)
```

```python
# ❌ 过度嵌套的 lambda
result = map(
    lambda x: filter(
        lambda y: y > x,
        data
    ),
    thresholds
)

# 问题：
# 1. lambda 嵌套难以理解
# 2. 返回的是迭代器的迭代器，需要多次转换
# 3. 调试困难
```

```python
# ✅ 正确做法：用命名函数或推导式
def filter_above_threshold(threshold: int) -> list[int]:
    """过滤大于阈值的数据"""
    return [y for y in data if y > threshold]

result = [filter_above_threshold(t) for t in thresholds]

# 或用普通函数
def get_filtered_results(thresholds: list[int], data: list[int]) -> list[list[int]]:
    """获取各阈值过滤结果"""
    return [[y for y in data if y > t] for t in thresholds]
```

```python
# ❌ 用 lambda 模仿闭包（不必要）
make_adder = lambda x: lambda y: x + y

add5 = make_adder(5)
print(add5(3))  # 8

# 问题：两层 lambda，难以理解和调试
```

```python
# ✅ 正确做法：用 def 函数创建闭包
def make_adder(x: int) -> Callable[[int], int]:
    """创建加法器"""
    def adder(y: int) -> int:
        return x + y
    return adder

add5 = make_adder(5)
print(add5(3))  # 8

# 有名字、有文档、更清晰
```

### Lambda vs def 选择指南

| 特性 | Lambda | def 函数 | 选择建议 |
|------|--------|----------|----------|
| 定义方式 | 一行表达式 | 多行语句块 | 逻辑复杂选 def |
| 命名 | 匿名 | 有名字 | 复用选 def |
| 文档 | 无 docstring | 可写 docstring | 需要文档选 def |
| 类型提示 | 难添加 | 可完整添加 | 需类型提示选 def |
| 异常处理 | 不支持 | 支持 | 需异常处理选 def |
| 调试 | 函数名显示 `<lambda>` | 显示实际名字 | 需调试选 def |
| 性能 | 无差别 | 无差别 | 不作为选择依据 |

---

## L3 专家层：底层原理

### Lambda 与 def 的内部实现差异

Lambda 和 def 创建的函数对象在底层结构上几乎相同，但在代码对象（`__code__`）中有细微差别。

```python
# Lambda 函数对象
square_lambda = lambda x: x ** 2

# def 函数对象
def square_def(x: int) -> int:
    return x ** 2

# 对比内部属性
print(square_lambda.__name__)  # '<lambda>'
print(square_def.__name__)     # 'square_def'

print(square_lambda.__doc__)   # None
print(square_def.__doc__)      # None（没写 docstring，但可以写）

# 代码对象几乎一致
print(square_lambda.__code__.co_code)  # 字节码
print(square_def.__code__.co_code)     # 相同的字节码
```

**关键差异：**

| 属性 | Lambda | def | 影响 |
|------|--------|-----|------|
| `__name__` | `'<lambda>'` | 实际函数名 | 调试时栈追踪不同 |
| `__doc__` | 始终 `None` | 可自定义 | help() 显示不同 |
| `__code__` | 相同 | 相同 | 执行性能无差别 |
| `__annotations__` | 空 | 可有类型提示 | IDE 支持不同 |

### Lambda 的编译与执行

Python 在编译 lambda 时，会将其转换为与 def 等价的字节码。

```python
import dis

# Lambda 字节码
add_lambda = lambda a, b: a + b
dis.dis(add_lambda)
#   0 LOAD_FAST    0 (a)
#   2 LOAD_FAST    1 (b)
#   4 BINARY_ADD
#   6 RETURN_VALUE

# def 字节码
def add_def(a: int, b: int) -> int:
    return a + b
dis.dis(add_def)
#   0 LOAD_FAST    0 (a)
#   2 LOAD_FAST    1 (b)
#   4 BINARY_ADD
#   6 RETURN_VALUE
```

两者生成的字节码完全一致，**lambda 没有运行时性能优势或劣势**。

### 闭包中的 Lambda：捕获时机陷阱

Lambda 在闭包中使用时，变量的捕获时机是一个常见陷阱。

```python
# ❌ 闭包中的 lambda 捕获的是变量引用，不是值
funcs = []
for i in range(5):
    funcs.append(lambda: i)  # 所有 lambda 共享同一个 i

print([f() for f in funcs])  # [4, 4, 4, 4, 4]（不是 [0, 1, 2, 3, 4]）

# 原因：lambda 捕获的是变量 i 的引用
# 循环结束后 i = 4，所有 lambda 返回 4

# ✅ 用默认参数冻结当前值
funcs = []
for i in range(5):
    funcs.append(lambda i=i: i)  # 默认参数在定义时求值

print([f() for f in funcs])  # [0, 1, 2, 3, 4]
```

**原理：**
- Lambda 中的自由变量（如 `i`）是**延迟绑定**的——在调用时才查找值
- 默认参数（如 `i=i`）是**立即绑定**的——在定义时求值并冻结
- 这不是 lambda 的特殊行为，def 闭包有同样的问题，但 lambda 更容易触发

### 函数式编程的 Pythonic 替代

Python 的 lambda 远不如其他语言（如 Haskell、Scala）的匿名函数强大。Pythonic 的做法是优先使用推导式。

```python
# Lambda + filter → 列表推导式
numbers = [1, 2, 3, 4, 5, 6]

# 函数式写法
evens = list(filter(lambda x: x % 2 == 0, numbers))

# Pythonic 写法（推荐）
evens = [x for x in numbers if x % 2 == 0]

# Lambda + map → 列表推导式
# 函数式写法
squares = list(map(lambda x: x ** 2, numbers))

# Pythonic 写法（推荐）
squares = [x ** 2 for x in numbers]
```

**何时保留 lambda：**
- `sorted()`/`min()`/`max()` 的 `key` 参数（推导式无法替代）
- 简单的内联回调（如 `on_click=lambda: ...`）
- 需要惰性求值的场景（`map`/`filter` 返回迭代器，推导式立即计算）

### 设计动机

Python 为什么这样设计 lambda？

| 设计选择 | 厳因 | 替代方案对比 |
|----------|------|-------------|
| 只允许一个表达式 | 保持简洁，避免滥用 | JavaScript 允许多行箭头函数 |
| 无需 return | 单表达式自动返回，减少语法噪音 | Rust 闭包也省略 return |
| 无 docstring | 匿名函数不需要文档，复杂逻辑应用 def | Haskell 的 where 子句可附文档 |
| `__name__` 为 `<lambda>` | 调试时可识别匿名来源 | Scala 给匿名函数生成编号名 |

### 知识关联

```
Lambda 知识关联图：
                    ┌───────────────┐
                    │  __code__     │
                    │  字节码等价   │
                    └───────────────┘
                          │
                          ↓
┌─────────────┐     ┌───────────────┐     ┌───────────────┐
│  闭包捕获   │────→│    Lambda     │────→│  默认参数冻结 │
│  延迟绑定   │     │  底层原理     │     │  立即绑定     │
└─────────────┘     └───────────────┘     └───────────────┘
                          │
                          ↓
                    ┌───────────────┐
                    │  推导式替代   │
                    │  Pythonic 写法│
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
│                      Lambda 匿名函数 知识要点                  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   L1 理解层：                                                │
│   ✓ 语法：lambda 参数: 表达式                               │
│   ✓ 自动返回表达式结果                                      │
│   ✓ 只能有一个表达式                                        │
│   ✓ 用于 sorted/filter/map/reduce 的参数                    │
│                                                             │
│   L2 实践层：                                                │
│   ✓ 用于简单一次性函数，不赋值给变量                        │
│   ✓ 作为 key/filter/map 参数的标准用法                      │
│   ✓ 保持简单：一行能读懂                                    │
│   ✓ 复杂逻辑、复用函数、需文档时用 def                      │
│   ✓ 副作用操作用 for 循环，不隐藏在 lambda 里               │
│                                                             │
│   L3 专家层：                                                │
│   ✓ lambda 与 def 字节码等价，无性能差异                    │
│   ✓ 闭包中 lambda 延迟绑定，默认参数立即绑定                │
│   ✓ 推导式是 filter/map 的 Pythonic 替代                    │
│   ✓ lambda 只允许单表达式是防止滥用的设计决策                │
│                                                             │
│   选择指南：                                                 │
│   ✓ 简单一次性 → lambda                                     │
│   ✓ 复杂或复用 → def                                        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 交互演示

运行项目 CLI 查看本章代码的实际执行效果：

```bash
cd functions_demo && uv run python -m app   # 选 4
```

