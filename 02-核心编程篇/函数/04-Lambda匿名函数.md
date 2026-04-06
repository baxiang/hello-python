# 第 4 章：Lambda 匿名函数

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

## Lambda 的最简用法（3分钟上手）

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

```python
# ── 方式 1：普通函数 ──────────────────────────────
def add(a: int, b: int) -> int:
    return a + b

print(add(3, 5))  # 8

# ── 方式 2：Lambda 函数 ───────────────────────────
add_lambda = lambda a, b: a + b

print(add_lambda(3, 5))  # 8

# ── 方式 3：立即调用 ──────────────────────────────
result = (lambda a, b: a + b)(3, 5)
print(result)  # 8
```

**对比表：**

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

---

## 实际应用：数据处理管道

```python
from typing import Any


def process_data(
    data: list[dict[str, Any]],
    sort_key: str = "score",
    min_value: float = 0,
    top_n: int = 5
) -> list[dict[str, Any]]:
    """
    数据处理管道
    
    Args:
        data: 原始数据
        sort_key: 排序字段
        min_value: 最小值过滤
        top_n: 返回前 N 条
    
    Returns:
        处理后的数据
    """
    # 1. 过滤
    filtered = list(filter(lambda x: x.get(sort_key, 0) >= min_value, data))
    
    # 2. 排序
    sorted_data = sorted(filtered, key=lambda x: x.get(sort_key, 0), reverse=True)
    
    # 3. 取前 N 条
    return sorted_data[:top_n]


# 使用
students = [
    {"name": "张三", "score": 85, "age": 18},
    {"name": "李四", "score": 92, "age": 19},
    {"name": "王五", "score": 78, "age": 17},
    {"name": "赵六", "score": 88, "age": 18},
    {"name": "钱七", "score": 65, "age": 20},
    {"name": "孙八", "score": 95, "age": 17}
]

# 获取成绩前 3 名
top_3 = process_data(students, sort_key="score", top_n=3)
for s in top_3:
    print(f"{s['name']}: {s['score']}分")

# 获取成绩 80 分以上的学生
above_80 = process_data(students, min_value=80)
print(f"80分以上人数：{len(above_80)}")
```

---

## 本章小结

```
┌─────────────────────────────────────────────────────────────┐
│                      Lambda 匿名函数 知识要点                 │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   语法：                                                     │
│   ✓ lambda 参数: 表达式                                     │
│   ✓ 自动返回表达式结果                                      │
│   ✓ 只能有一个表达式                                        │
│                                                             │
│   使用场景：                                                 │
│   ✓ sorted() 的 key 参数                                    │
│   ✓ filter() 的过滤条件                                     │
│   ✓ map() 的转换规则                                        │
│   ✓ reduce() 的归约操作                                     │
│                                                             │
│   选择指南：                                                 │
│   ✓ 简单一次性函数 → lambda                                 │
│   ✓ 复杂或复用函数 → def                                    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

[← 上一章：变量作用域](./03-变量作用域.md) | [返回目录](../README.md)