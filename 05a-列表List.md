# 第 5a 章 - 列表（List）（详细版）

## 第一部分：什么是列表

### 5a.1 列表的概念

#### 概念说明

**列表（List）** 是 Python 中最常用的数据结构，用于存储有序的元素集合。

```
┌─────────────────────────────────────────┐
│            列表的特点                   │
├─────────────────────────────────────────┤
│                                         │
│  ✅ 有序：元素有固定的顺序              │
│  ✅ 可变：可以修改、添加、删除元素      │
│  ✅ 可重复：允许有相同的元素            │
│  ✅ 异构：可以存储不同类型的元素        │
│                                         │
│  表示方法：使用方括号 []                │
│  例如：[1, 2, 3, 4, 5]                  │
│                                         │
└─────────────────────────────────────────┘
```

#### 列表的视觉表示

```
列表：fruits = ["apple", "banana", "orange"]

可视化表示：
┌─────────────────────────────────────────┐
│  索引：    0        1        2          │
│           ┌─────┐ ┌──────┐ ┌─────────┐ │
│  正向 →   │apple│ │banana│ │orange   │ │
│           └─────┘ └──────┘ └─────────┘ │
│                                         │
│  反向 →   │  -3 │ │  -2  │ │   -1    │ │
│           └─────┘ └──────┘ └─────────┘ │
└─────────────────────────────────────────┘

记忆技巧：
• 正向索引从 0 开始（从左到右）
• 反向索引从 -1 开始（从右到左）
```

---

## 第二部分：创建列表

### 5a.2 创建方式

```python
# 方式 1：使用方括号
fruits = ["apple", "banana", "orange"]
numbers = [1, 2, 3, 4, 5]

# 方式 2：创建空列表
empty_list = []
empty_list2 = list()

# 方式 3：从其他可迭代对象创建
from_string = list("hello")
print(from_string)  # ['h', 'e', 'l', 'l', 'o']

from_range = list(range(5))
print(from_range)  # [0, 1, 2, 3, 4]

from_tuple = list((1, 2, 3))
print(from_tuple)  # [1, 2, 3]

# 方式 4：列表推导式（后面详细讲）
squares = [x**2 for x in range(5)]
print(squares)  # [0, 1, 4, 9, 16]
```

#### 列表可以存储任何类型

```python
# 存储数字
numbers = [1, 2, 3, 4, 5]

# 存储字符串
names = ["Alice", "Bob", "Charlie"]

# 存储布尔值
flags = [True, False, True]

# 存储混合类型（不推荐，但可以）
mixed = [1, "hello", 3.14, True]

# 存储列表（嵌套列表）
matrix = [[1, 2], [3, 4], [5, 6]]
```

---

## 第三部分：访问列表元素

### 5a.3 索引访问

```python
fruits = ["apple", "banana", "orange", "grape"]

# 正向索引（从 0 开始）
print(fruits[0])  # 输出：apple
print(fruits[1])  # 输出：banana
print(fruits[2])  # 输出：orange
print(fruits[3])  # 输出：grape

# 反向索引（从 -1 开始）
print(fruits[-1])  # 输出：grape（最后一个）
print(fruits[-2])  # 输出：orange（倒数第二个）
print(fruits[-3])  # 输出：banana
print(fruits[-4])  # 输出：apple（第一个）
```

**索引图解：**
```
fruits = ["apple", "banana", "orange", "grape"]

正向索引：
  0        1        2        3
┌─────┐ ┌──────┐ ┌────────┐ ┌─────┐
│apple│ │banana│ │orange  │ │grape│
└─────┘ └──────┘ └────────┘ └─────┘
  -4       -3       -2        -1
反向索引：
```

#### 索引越界错误

```python
fruits = ["apple", "banana", "orange"]

# ❌ 错误：索引越界
# print(fruits[3])  # IndexError: list index out of range
# print(fruits[-4]) # IndexError: list index out of range

# ✅ 正确：安全访问
def safe_get(lst, index):
    if 0 <= index < len(lst):
        return lst[index]
    return None

print(safe_get(fruits, 1))   # banana
print(safe_get(fruits, 10))  # None
```

### 5a.4 列表切片详解

#### 基本语法

```
┌─────────────────────────────────────────┐
│          列表切片语法                    │
├─────────────────────────────────────────┤
│                                         │
│   列表 [start:end:step]                 │
│                                         │
│   参数说明：                            │
│   • start  → 起始索引（包含）           │
│   • end    → 结束索引（不包含）         │
│   • step   → 步长（默认为 1）           │
│                                         │
│   记忆口诀："包头不包尾"                │
│                                         │
└─────────────────────────────────────────┘
```

#### 切片示例

```python
numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

# 基本切片
print(numbers[2:5])    # [2, 3, 4] - 索引 2 到 4（不包含 5）
print(numbers[0:3])    # [0, 1, 2] - 前 3 个元素

# 省略 start（从开头开始）
print(numbers[:5])     # [0, 1, 2, 3, 4] - 前 5 个

# 省略 end（到结尾结束）
print(numbers[5:])     # [5, 6, 7, 8, 9] - 从索引 5 到结尾

# 省略 start 和 end（复制整个列表）
print(numbers[:])      # [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

# 使用负索引
print(numbers[-3:])    # [7, 8, 9] - 最后 3 个
print(numbers[:-3])    # [0, 1, 2, 3, 4, 5, 6] - 除了最后 3 个

# 使用步长
print(numbers[::2])    # [0, 2, 4, 6, 8] - 每隔一个
print(numbers[1::2])   # [1, 3, 5, 7, 9] - 所有奇数位置

# 反转列表
print(numbers[::-1])   # [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
```

**切片图解：**
```
numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
                  │           │
              start=2      end=5（不包含）
                  │           │
                  ▼           ▼
结果：[2, 3, 4]
       │  │  │
      索引 2  3  4

"包头不包尾"：包含 start，不包含 end
```

---

## 第四部分：修改列表

### 5a.5 修改元素

```python
fruits = ["apple", "banana", "orange"]

# 修改单个元素
fruits[1] = "blueberry"
print(fruits)  # ['apple', 'blueberry', 'orange']

# 修改多个元素（切片赋值）
fruits[0:2] = ["AA", "BB"]
print(fruits)  # ['AA', 'BB', 'orange']
```

**修改过程图解：**
```
修改前：
fruits = ["apple", "banana", "orange"]
                  │
                  ▼ 修改为 "blueberry"
fruits = ["apple", "blueberry", "orange"]
```

#### 切片赋值的特殊用法

```python
numbers = [1, 2, 3, 4, 5]

# 在开头插入
numbers[0:0] = [0, 0]
print(numbers)  # [0, 0, 1, 2, 3, 4, 5]

# 在末尾插入
numbers[len(numbers):] = [6, 7]
print(numbers)  # [0, 0, 1, 2, 3, 4, 5, 6, 7]

# 替换多个元素
numbers[1:4] = [99]
print(numbers)  # [0, 99, 4, 5, 6, 7]
```

---

## 第五部分：列表方法详解

### 5a.6 添加元素

```python
fruits = ["apple", "banana"]

# append() - 在末尾添加一个元素
fruits.append("orange")
print(fruits)  # ['apple', 'banana', 'orange']

# insert() - 在指定位置插入
fruits.insert(1, "apricot")  # 在索引 1 处插入
print(fruits)  # ['apple', 'apricot', 'banana', 'orange']

# extend() - 扩展列表（添加多个元素）
fruits.extend(["mango", "peach"])
print(fruits)  # ['apple', 'apricot', 'banana', 'orange', 'mango', 'peach']

# 也可以用 + 运算符
more_fruits = ["watermelon", "cherry"]
all_fruits = fruits + more_fruits
print(all_fruits)
```

**添加方法对比：**
```
fruits = ["apple", "banana"]

append("orange"):
  └── 在末尾添加单个元素
  → ['apple', 'banana', 'orange']

insert(1, "apricot"):
  └── 在指定位置插入单个元素
  → ['apple', 'apricot', 'banana']

extend(["mango", "peach"]):
  └── 在末尾添加多个元素
  → ['apple', 'banana', 'mango', 'peach']
```

### 5a.7 删除元素

```python
fruits = ["apple", "banana", "orange", "grape", "banana"]

# remove() - 删除第一个匹配的元素
fruits.remove("banana")  # 只删除第一个 "banana"
print(fruits)  # ['apple', 'orange', 'grape', 'banana']

# pop() - 删除并返回指定位置的元素
last = fruits.pop()      # 删除最后一个
print(f"删除：{last}")   # banana
print(fruits)            # ['apple', 'orange', 'grape']

first = fruits.pop(0)    # 删除第一个
print(f"删除：{first}")  # apple
print(fruits)            # ['orange', 'grape']

# del - 删除语句（不是方法）
del fruits[0]            # 删除索引 0 的元素
print(fruits)            # ['grape']

# clear() - 清空列表
fruits.clear()
print(fruits)            # []
```

**删除方法对比：**
```
fruits = ["apple", "banana", "orange"]

remove("banana"):
  └── 按值删除，只删第一个
  → ['apple', 'orange']

pop():
  └── 删除最后一个，返回被删元素
  → 返回 "orange"，列表变为 ['apple', 'banana']

pop(1):
  └── 删除指定位置，返回被删元素
  → 返回 "banana"，列表变为 ['apple', 'orange']

del fruits[0]:
  └── 按索引删除，不返回值
  → ['banana', 'orange']

clear():
  └── 清空所有元素
  → []
```

### 5a.8 查找和统计

```python
fruits = ["apple", "banana", "orange", "banana", "grape"]

# index() - 查找元素的索引
print(fruits.index("banana"))        # 1（第一个 "banana" 的位置）
print(fruits.index("banana", 2))     # 3（从索引 2 开始找）
print(fruits.index("banana", 2, 4))  # 3（在索引 2-4 之间找）

# count() - 统计元素出现次数
print(fruits.count("banana"))  # 2
print(fruits.count("apple"))   # 1
print(fruits.count("mango"))   # 0

# len() - 获取列表长度（内置函数）
print(len(fruits))  # 5
```

### 5a.9 排序和反转

```python
numbers = [3, 1, 4, 1, 5, 9, 2, 6]

# sort() - 排序（修改原列表）
numbers.sort()
print(numbers)  # [1, 1, 2, 3, 4, 5, 6, 9]

# 降序排序
numbers.sort(reverse=True)
print(numbers)  # [9, 6, 5, 4, 3, 2, 1, 1]

# 自定义排序键
words = ["apple", "pie", "cherry", "dog"]
words.sort(key=len)  # 按长度排序
print(words)  # ['pie', 'dog', 'apple', 'cherry']

# reverse() - 反转列表（不排序）
numbers = [1, 2, 3, 4, 5]
numbers.reverse()
print(numbers)  # [5, 4, 3, 2, 1]

# 使用切片反转（不修改原列表）
numbers = [1, 2, 3, 4, 5]
reversed_numbers = numbers[::-1]
print(reversed_numbers)  # [5, 4, 3, 2, 1]
print(numbers)           # [1, 2, 3, 4, 5]（原列表不变）
```

**sort() vs sorted()：**
```python
numbers = [3, 1, 4, 1, 5]

# sort() - 修改原列表
numbers.sort()
print(numbers)  # [1, 1, 3, 4, 5]（原列表已修改）

# sorted() - 不修改原列表，返回新列表
numbers = [3, 1, 4, 1, 5]
sorted_numbers = sorted(numbers)
print(sorted_numbers)  # [1, 1, 3, 4, 5]（新列表）
print(numbers)         # [3, 1, 4, 1, 5]（原列表不变）
```

---

## 第六部分：列表操作符

### 5a.10 常用操作符

```python
# 列表拼接（+）
list1 = [1, 2, 3]
list2 = [4, 5, 6]
result = list1 + list2
print(result)  # [1, 2, 3, 4, 5, 6]

# 列表重复（*）
numbers = [1, 2]
repeated = numbers * 3
print(repeated)  # [1, 2, 1, 2, 1, 2]

# 成员检查（in）
fruits = ["apple", "banana", "orange"]
print("apple" in fruits)     # True
print("mango" in fruits)     # False
print("mango" not in fruits) # True

# 列表比较
print([1, 2, 3] == [1, 2, 3])  # True
print([1, 2, 3] == [3, 2, 1])  # False
```

---

## 第七部分：练习题

### 练习 1：列表操作

```python
# 1. 创建一个包含 1-10 的列表
numbers = list(range(1, 11))

# 2. 添加 11-15
numbers.extend(range(11, 16))

# 3. 删除第 3 个元素
numbers.pop(2)

# 4. 反转列表
numbers.reverse()

# 5. 排序（降序）
numbers.sort(reverse=True)

print(numbers)
```

### 练习 2：列表去重

```python
# 不使用 set，手动去重
numbers = [1, 2, 2, 3, 3, 3, 4, 4, 5]

# 方法 1：使用辅助列表
unique = []
for num in numbers:
    if num not in unique:
        unique.append(num)
print(unique)

# 方法 2：使用 set（更简单）
unique = list(set(numbers))
print(unique)
```

---

## 本章总结

```
列表常用方法速查：
  添加：append, extend, insert
  删除：remove, pop, del, clear
  查找：index, count, len
  排序：sort, sorted, reverse
```

---

[上一章](./04-流程控制.md) | [下一章](./05b-元组Tuple.md)
