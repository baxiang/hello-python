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
不仅仅是打印，支持格式化、分隔符定制、文件重定向。

```python
# 基础用法
print("Hello", "World")  # 输出: Hello World

# 自定义分隔符 (sep)
print("2023", "10", "01", sep="-")  # 输出: 2023-10-01

# 自定义结尾 (end)，默认是 \n
print("Loading...", end="")
print("Done")  # 输出: Loading...Done

# 输出到文件
with open("log.txt", "w") as f:
    print("写入日志", file=f)
```

### 2.2 `input()`: 获取用户输入
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
支持传入 `key` 参数来指定比较依据。

```python
nums = [10, 5, 20, 8]
print(max(nums))      # 20
print(min(nums))      # 5
print(sum(nums))      # 43

# 高级用法：根据 key 比较
users = [{"name": "Alice", "age": 18}, {"name": "Bob", "age": 25}]
print(max(users, key=lambda u: u["age"]))  
# 输出: {'name': 'Bob', 'age': 25}
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
**注意**：返回的是一个对象，而不是列表（省内存）。

```python
list(range(5))        # [0, 1, 2, 3, 4]
list(range(1, 5))     # [1, 2, 3, 4]
list(range(0, 10, 2)) # [0, 2, 4, 6, 8]
```

### 5.2 `len()`: 获取长度
```python
print(len("Python"))  # 6
print(len([1, 2, 3])) # 3
```

### 5.3 `enumerate()`: 索引与值同时获取
**反模式**：`for i in range(len(list))`
**推荐模式**：`for i, item in enumerate(list)`

```python
fruits = ["apple", "banana", "cherry"]
for index, fruit in enumerate(fruits, start=1):
    print(f"第{index}个水果: {fruit}")
```

### 5.4 `zip()`: 拉链式合并
将多个可迭代对象打包成元组。

```python
names = ["Alice", "Bob"]
ages = [20, 30]

for name, age in zip(names, ages):
    print(f"{name} is {age} years old")

# 构造字典
print(dict(zip(names, ages)))  
# 输出: {'Alice': 20, 'Bob': 30}
```

### 5.5 `sorted()` 与 `reversed()`

| 函数 | 说明 | 返回值 |
| :--- | :--- | :--- |
| `sorted(iterable)` | 排序（升序） | 返回**新列表** |
| `reversed(seq)` | 反转序列 | 返回**反转迭代器** (非列表) |

```python
nums = [3, 1, 2]

# sorted 返回新列表，不修改原列表
new_nums = sorted(nums, reverse=True)
print(new_nums) # [3, 2, 1]
print(nums)     # [3, 1, 2] (不变)

# reversed 返回迭代器，需要 list() 转换
rev_nums = list(reversed(nums))
print(rev_nums) # [2, 1, 3]
```

---

## 6. 函数式编程核心

### 6.1 `map()`: 映射
对序列中的每个元素应用函数。
**替代方案**：通常可以用列表推导式 `[func(x) for x in items]` 替代，但在处理简单函数时 `map` 依然简洁。

```python
nums = [1, 2, 3]
# 方式 1：使用 map
squared = list(map(lambda x: x**2, nums)) 

# 方式 2：多个序列映射 (如向量加法)
a = [1, 2]
b = [10, 20]
added = list(map(lambda x, y: x + y, a, b)) # [11, 22]
```

### 6.2 `filter()`: 过滤
筛选满足条件的元素。
**替代方案**：`[x for x in items if condition]`

```python
nums = [1, 2, 3, 4, 5, 6]
evens = list(filter(lambda x: x % 2 == 0, nums))
print(evens) # [2, 4, 6]
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
