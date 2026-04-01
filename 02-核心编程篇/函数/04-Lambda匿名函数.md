# Lambda 匿名函数

本章讲解 Python Lambda 匿名函数的语法和使用场景。

---

## 什么是 Lambda

### 概念说明

**Lambda（匿名函数）** 是一种无需命名就能直接使用的迷你函数。

```
┌────────────────────────────────────────────────────┐
│              Lambda 表达式的结构                    │
├────────────────────────────────────────────────────┤
│                                                    │
│   lambda  参数1, 参数2, ...  :  表达式             │
│      │         │                  │                │
│      │         │                  └─ 自动作为返回值 │
│      │         └─ 可以有多个参数，也可以没有        │
│      └─ 关键字，固定写法                           │
│                                                    │
│   三大限制：                                       │
│   • 只能有一个表达式（不能写多行）                 │
│   • 不需要写 return（自动返回表达式结果）           │
│   • 不能有 if/for/while 等语句（可以用三元表达式） │
│                                                    │
└────────────────────────────────────────────────────┘
```

---

## Lambda 与普通函数对比

```python
# ── 方式 1：普通函数 ──────────────────────────────
def add(a, b):
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

## Lambda 的各种形式

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

## Lambda 的核心使用场景

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
┌──────────────────────────────────────────────────────┐
│               Lambda 使用决策树                       │
├──────────────────────────────────────────────────────┤
│                                                      │
│  这个函数会在多处复用吗？                            │
│       ├─ 是  →  用 def（给它起个好名字）             │
│       └─ 否                                          │
│            │                                         │
│            ▼                                         │
│       逻辑超过一个表达式吗？                         │
│       ├─ 是  →  用 def（lambda 写不了）              │
│       └─ 否                                          │
│            │                                         │
│            ▼                                         │
│       需要写注释/文档说明吗？                        │
│       ├─ 是  →  用 def（lambda 没有 docstring）      │
│       └─ 否  →  可以考虑 lambda ✅                   │
│                                                      │
├──────────────────────────────────────────────────────┤
│  ✅ Lambda 的最佳场景：                              │
│  • sorted / min / max 的 key 参数                    │
│  • filter / map 的转换或过滤条件                     │
│  • 简单的数学表达式                                  │
│                                                      │
│  ❌ Lambda 不适合的场景：                            │
│  • 超过一个表达式的逻辑                              │
│  • 需要复用的函数                                    │
│  • 赋值给变量（直接用 def 更清晰）                   │
│                                                      │
└──────────────────────────────────────────────────────┘
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