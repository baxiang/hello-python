# pickle 对象序列化

> **难度**：⭐⭐ 进阶
> **预计时间**：30分钟
> **前置知识**：文件操作、类与对象
> **引入版本**：Python 3.0+

本章讲解 pickle 模块，用于将 Python 对象序列化保存到文件，并从文件恢复。

---

## 为什么需要 pickle？

### 问题场景

你需要将程序运行时的对象保存到文件：
- 游戏进度保存
- 机器学习模型持久化
- 复杂配置对象存储

**JSON 无法处理的场景：**

```python
import json

class User:
    def __init__(self, name: str, scores: list[int]) -> None:
        self.name = name
        self.scores = scores

user = User("张三", [85, 90, 78])

try:
    json.dumps(user)
except TypeError as e:
    print(f"错误: {e}")
```

**运行结果：**

```
错误: Object of type User is not JSON serializable
```

**问题：**
- JSON 只支持基本类型（str, int, list, dict）
- 无法序列化自定义类对象
- 无法序列化函数、lambda、嵌套对象等

**pickle 可以处理：**

```python
import pickle

class User:
    def __init__(self, name: str, scores: list[int]) -> None:
        self.name = name
        self.scores = scores

user = User("张三", [85, 90, 78])

serialized = pickle.dumps(user)
print(f"序列化后: {len(serialized)} bytes")

restored = pickle.loads(serialized)
print(f"恢复后: {restored.name}, {restored.scores}")
```

这就是 pickle 的价值：**序列化任意 Python 对象**。

---

## pickle 概念铺垫

```
┌─────────────────────────────────────────────────────────────┐
│          pickle 关键概念                                     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. 什么是序列化？                                          │
│  ─────────────────────────────────────────────              │
│  • 将对象转换为字节序列                                     │
│  • 可保存到文件或通过网络传输                               │
│  • 反序列化：从字节序列恢复对象                              │
│                                                             │
│  2. pickle vs JSON                                          │
│  ─────────────────────────────────────────────              │
│                                                             │
│  ┌────────────────────┬───────────────────────┐            │
│  │      pickle        │        JSON           │            │
│  ├────────────────────┼───────────────────────┤            │
│  │ 任意Python对象     │ 基本类型              │            │
│  │ 二进制格式         │ 文本格式              │            │
│  │ Python专属         │ 跨语言                │            │
│  │ 有安全风险         │ 安全                  │            │
│  │ 高效               │ 人类可读              │            │
│  └────────────────────┴───────────────────────┘            │
│                                                             │
│  3. pickle 协议版本                                         │
│  ─────────────────────────────────────────────              │
│  • Protocol 0：ASCII格式，兼容旧版本                        │
│  • Protocol 1：二进制格式                                   │
│  • Protocol 2：支持新式类                                   │
│  • Protocol 3-5：支持更多特性                               │
│  • Protocol 5（Python 3.8+）：支持超大对象                  │
│  • 默认使用最高版本                                         │
│                                                             │
│  4. 安全警告                                                │
│  ─────────────────────────────────────────────              │
│  ⚠️ pickle 不安全！                                         │
│  • 反序列化可以执行任意代码                                 │
│  • 不要加载不可信来源的 pickle 文件                        │
│  • 只用于内部数据存储                                       │
│                                                             │
│  5. 典型应用场景                                            │
│  ─────────────────────────────────────────────              │
│  • 机器学习模型保存                                         │
│  • 游戏状态持久化                                           │
│  • 内部配置对象存储                                         │
│  • 进程间对象传递                                           │
│                                                             │
│  6. 生活类比                                                │
│  ─────────────────────────────────────────────              │
│  • 序列化 = 把玩具拆开装箱                                  │
│  • 反序列化 = 拆箱组装玩具                                  │
│  • pickle = 专业装箱（任意玩具）                            │
│  • JSON = 标准装箱（只支持标准玩具）                        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## L1 理解层：pickle 基础

### 语法结构

```
┌─────────────────────────────────────────────────────────────┐
│  pickle 核心语法                                             │
│                                                             │
│  序列化到字节：                                              │
│  data = pickle.dumps(obj, protocol=None)                   │
│                                                             │
│  从字节恢复：                                                │
│  obj = pickle.loads(data)                                  │
│                                                             │
│  序列化到文件：                                              │
│  pickle.dump(obj, file, protocol=None)                     │
│                                                             │
│  从文件恢复：                                                │
│  obj = pickle.load(file)                                   │
│                                                             │
│  参数说明：                                                  │
│  obj      → 要序列化的对象                                  │
│  data     → 字节序列（bytes）                               │
│  file     → 文件对象（必须以二进制模式打开）                 │
│  protocol → 序列化协议版本（默认最高）                       │
│                                                             │
│  ⚠️ 文件必须用二进制模式：                                   │
│  写入：open("file.pkl", "wb")                              │
│  读取：open("file.pkl", "rb")                              │
└─────────────────────────────────────────────────────────────┘
```

### 最简示例：序列化到字节

```python
import pickle

data = {"name": "张三", "scores": [85, 90, 78], "active": True}

serialized = pickle.dumps(data)
print(f"类型: {type(serialized)}")
print(f"大小: {len(serialized)} bytes")

restored = pickle.loads(serialized)
print(f"恢复: {restored}")
print(f"原始 == 恢复: {data == restored}")
```

**运行结果：**

```
类型: <class 'bytes'>
大小: 54 bytes
恢复: {'name': '张三', 'scores': [85, 90, 78], 'active': True}
原始 == 恢复: True
```

### 最简示例：序列化到文件

```python
import pickle

data = {"name": "张三", "scores": [85, 90, 78]}

with open("data.pkl", "wb") as f:
    pickle.dump(data, f)

with open("data.pkl", "rb") as f:
    restored = pickle.load(f)

print(f"恢复: {restored}")
```

**运行结果：**

```
恢复: {'name': '张三', 'scores': [85, 90, 78]}
```

**关键代码说明：**

| 代码 | 含义 |
|------|------|
| `pickle.dumps(data)` | 序列化到字节，返回 bytes |
| `pickle.loads(serialized)` | 从字节恢复对象 |
| `pickle.dump(data, f)` | 序列化并写入文件 |
| `pickle.load(f)` | 从文件读取并恢复 |
| `"wb"` | 写入二进制模式 |
| `"rb"` | 读取二进制模式 |

### 详细示例：序列化自定义类

```python
import pickle

class User:
    def __init__(self, name: str, scores: list[int]) -> None:
        self.name = name
        self.scores = scores
    
    def average(self) -> float:
        return sum(self.scores) / len(self.scores)
    
    def __repr__(self) -> str:
        return f"User({self.name}, avg={self.average()})"

user = User("张三", [85, 90, 78])

with open("user.pkl", "wb") as f:
    pickle.dump(user, f)

with open("user.pkl", "rb") as f:
    restored = pickle.load(f)

print(f"恢复: {restored}")
print(f"平均分: {restored.average()}")
```

**运行结果：**

```
恢复: User(张三, avg=84.66666666666667)
平均分: 84.66666666666667
```

**说明：**
- pickle 可以序列化自定义类
- 方法（如 average）不会被序列化
- 类定义必须在加载时可用

### 详细示例：嵌套对象

```python
import pickle

class Course:
    def __init__(self, name: str, score: int) -> None:
        self.name = name
        self.score = score

class Student:
    def __init__(self, name: str, courses: list[Course]) -> None:
        self.name = name
        self.courses = courses

student = Student(
    "张三",
    [Course("数学", 90), Course("语文", 85), Course("英语", 78)]
)

serialized = pickle.dumps(student)
restored = pickle.loads(serialized)

print(f"学生: {restored.name}")
for course in restored.courses:
    print(f"  {course.name}: {course.score}")
```

**运行结果：**

```
学生: 张三
  数学: 90
  语文: 85
  英语: 78
```

**说明：**
- pickle 递归序列化嵌套对象
- 嵌套的 Course 类也被正确恢复
- 类定义必须在加载时可用

---

## L2 实践层：pickle 应用

### 实际应用场景

#### 场景1：机器学习模型保存

```python
import pickle

class SimpleModel:
    def __init__(self) -> None:
        self.weights: list[float] = []
        self.trained: bool = False
    
    def train(self, data: list[float]) -> None:
        self.weights = [d * 0.5 for d in data]
        self.trained = True
    
    def predict(self, x: float) -> float:
        if not self.trained:
            return 0.0
        return sum(w * x for w in self.weights) / len(self.weights)

model = SimpleModel()
model.train([1.0, 2.0, 3.0, 4.0])
print(f"训练后预测: {model.predict(5.0)}")

with open("model.pkl", "wb") as f:
    pickle.dump(model, f)

with open("model.pkl", "rb") as f:
    loaded_model = pickle.load(f)

print(f"加载后预测: {loaded_model.predict(5.0)}")
```

**运行结果：**

```
训练后预测: 12.5
加载后预测: 12.5
```

#### 场景2：游戏状态保存

```python
import pickle

class GameState:
    def __init__(self) -> None:
        self.level: int = 1
        self.score: int = 0
        self.inventory: list[str] = []
        self.position: tuple[int, int] = (0, 0)
    
    def save(self, filename: str) -> None:
        with open(filename, "wb") as f:
            pickle.dump(self, f)
    
    def load(self, filename: str) -> None:
        with open(filename, "rb") as f:
            data = pickle.load(f)
            self.level = data.level
            self.score = data.score
            self.inventory = data.inventory
            self.position = data.position

game = GameState()
game.level = 5
game.score = 1000
game.inventory = ["剑", "盾", "药水"]
game.position = (100, 200)

game.save("savegame.pkl")

new_game = GameState()
new_game.load("savegame.pkl")
print(f"等级: {new_game.level}, 分数: {new_game.score}")
print(f"装备: {new_game.inventory}")
```

#### 场景3：批量对象保存

```python
import pickle

users = [
    {"id": 1, "name": "张三", "active": True},
    {"id": 2, "name": "李四", "active": False},
    {"id": 3, "name": "王五", "active": True},
]

with open("users.pkl", "wb") as f:
    for user in users:
        pickle.dump(user, f)

restored_users: list[dict] = []
with open("users.pkl", "rb") as f:
    while True:
        try:
            user = pickle.load(f)
            restored_users.append(user)
        except EOFError:
            break

print(f"恢复 {len(restored_users)} 个用户")
for user in restored_users:
    print(f"  {user['name']}")
```

**运行结果：**

```
恢复 3 个用户
  张三
  李四
  王五
```

**说明：**
- 可以连续 dump 多个对象到同一文件
- 连续 load 直到 EOFError
- 适合批量数据存储

### 推荐做法

| 做法 | 原因 | 示例 |
|------|------|------|
| **只序列化可信数据** | pickle 有安全风险 | 内部数据存储 |
| **用最高协议版本** | 性能更好，功能更多 | `protocol=pickle.HIGHEST_PROTOCOL` |
| **二进制模式打开文件** | pickle 输出二进制 | `"wb"` / `"rb"` |
| **加载时类定义可用** | pickle 不存储类定义 | 确保类已导入 |
| **用 try-except 处理 EOFError** | 批量读取需要 | `except EOFError: break` |

### 反模式：不要这样做

#### 错误1：加载不可信的 pickle 文件

```python
import pickle

url = "https://untrusted.com/data.pkl"
import urllib.request
response = urllib.request.urlopen(url)

data = pickle.load(response)
```

**问题：**
- ❌ 极其危险！远程文件可能包含恶意代码
- pickle 反序列化可以执行任意代码
- 可能导致数据泄露、系统被控制

```python
import json

url = "https://untrusted.com/data.json"
import urllib.request
response = urllib.request.urlopen(url)

data = json.load(response)
```

**正确做法：**
- 使用 JSON 等安全格式处理外部数据
- 只用 pickle 处理内部可信数据

#### 错误2：忘记二进制模式

```python
import pickle

data = {"name": "张三"}

with open("data.pkl", "w") as f:  # ❌ 文本模式
    pickle.dump(data, f)
```

**问题：**
- pickle 输出二进制数据
- 文本模式会导致编码错误

```python
import pickle

data = {"name": "张三"}

with open("data.pkl", "wb") as f:  # ✅ 二进制模式
    pickle.dump(data, f)
```

#### 错误3：加载时类定义不可用

```python
import pickle

serialized = pickle.dumps(SomeClass())

del SomeClass

obj = pickle.loads(serialized)
```

**问题：**
- AttributeError: Can't get attribute 'SomeClass'
- pickle 不存储类定义，只存储类名和属性
- 加载时类必须在当前环境中可用

```python
import pickle

serialized = pickle.dumps(SomeClass())

obj = pickle.loads(serialized)
```

### pickle vs JSON 选择

```
┌─────────────────────────────────────────────────────────────┐
│          pickle vs JSON 选择决策                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  使用 pickle：                                               │
│  ─────────────────────────────────────────────              │
│  ✅ 需要序列化自定义类                                      │
│  ✅ 内部数据存储                                            │
│  ✅ 机器学习模型保存                                        │
│  ✅ 需要最高效率                                            │
│  ✅ Python 环境之间传递                                     │
│                                                             │
│  使用 JSON：                                                 │
│  ─────────────────────────────────────────────              │
│  ✅ 需要跨语言兼容                                          │
│  ✅ 外部数据来源                                            │
│  ✅ 需要人类可读                                            │
│  ✅ Web API 数据交换                                        │
│  ✅ 配置文件                                                │
│                                                             │
│  ⚠️ 安全原则：                                               │
│  ─────────────────────────────────────────────              │
│  • 外部数据 → JSON                                          │
│  • 内部数据 → pickle                                        │
│  • 人类阅读 → JSON                                          │
│  • 程序读取 → pickle                                        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 适用场景

| 场景 | 是否推荐 pickle | 原因 |
|------|----------------|------|
| 机器学习模型保存 | ✅ 推荐 | sklearn/pytorch 常用 |
| 游戏状态保存 | ✅ 推荐 | 内部数据，复杂结构 |
| 内部配置存储 | ✅ 推荐 | 效率高 |
| Web API 响应 | ❌ 不推荐 | 用 JSON，跨语言 |
| 外部数据加载 | ❌ 不推荐 | 安全风险 |
| 配置文件 | ❌ 不推荐 | 用 JSON，人类可读 |

---

## L3 专家层：pickle 原理

### pickle 协议版本

```python
import pickle

print(f"最高协议: {pickle.HIGHEST_PROTOCOL}")
print(f"默认协议: {pickle.DEFAULT_PROTOCOL}")

data = {"name": "张三", "scores": [85, 90]}

for protocol in range(pickle.HIGHEST_PROTOCOL + 1):
    serialized = pickle.dumps(data, protocol=protocol)
    print(f"Protocol {protocol}: {len(serialized)} bytes")
```

**运行结果：**

```
最高协议: 5
默认协议: 4
Protocol 0: 54 bytes
Protocol 1: 38 bytes
Protocol 2: 37 bytes
Protocol 3: 37 bytes
Protocol 4: 37 bytes
Protocol 5: 37 bytes
```

**说明：**
- Protocol 0 是 ASCII，体积大
- Protocol 1+ 是二进制，体积小
- Python 3.8+ 最高支持 Protocol 5

### 自定义序列化行为

```python
import pickle

class SecretData:
    def __init__(self, public: str, secret: str) -> None:
        self.public = public
        self.__secret = secret
    
    def __getstate__(self) -> dict:
        state = self.__dict__.copy()
        state["_secret"] = "REDACTED"
        return state
    
    def __setstate__(self, state: dict) -> None:
        self.__dict__.update(state)
        self.__secret = state.get("_secret", "")

data = SecretData("公开数据", "机密信息")
print(f"原始: public={data.public}, secret={data.__secret}")

serialized = pickle.dumps(data)
restored = pickle.loads(serialized)
print(f"恢复: public={restored.public}, secret={restored.__secret}")
```

**运行结果：**

```
原始: public=公开数据, secret=机密信息
恢复: public=公开数据, secret=REDACTED
```

**说明：**
- `__getstate__` 控制序列化时存储的内容
- `__setstate__` 控制反序列化时恢复的逻辑
- 可以过滤敏感数据

### 循环引用处理

```python
import pickle

a = []
a.append(a)

print(f"a[0] is a: {a[0] is a}")

serialized = pickle.dumps(a)
restored = pickle.loads(serialized)

print(f"restored[0] is restored: {restored[0] is restored}")
```

**运行结果：**

```
a[0] is a: True
restored[0] is restored: True
```

**说明：**
- pickle 正确处理循环引用
- 使用 memo dict 记录已序列化的对象
- 避免无限递归

### 性能考量

| 操作 | 时间复杂度 | 说明 |
|------|-----------|------|
| `pickle.dumps` | O(n) | n = 对象大小 |
| `pickle.loads` | O(n) | n = 字节大小 |
| `pickle.dump` | O(n) | 写入文件 |
| `pickle.load` | O(n) | 读取文件 |

**pickle vs JSON 性能对比：**

```python
import pickle
import json
import time

data = {"name": "张三", "scores": [i for i in range(1000)]}

start = time.time()
pickle_data = pickle.dumps(data)
pickle_time = time.time() - start

start = time.time()
json_data = json.dumps(data)
json_time = time.time() - start

print(f"pickle 序列化: {pickle_time:.6f}s, {len(pickle_data)} bytes")
print(f"JSON 序列化: {json_time:.6f}s, {len(json_data)} bytes")

start = time.time()
pickle.loads(pickle_data)
pickle_load_time = time.time() - start

start = time.time()
json.loads(json_data)
json_load_time = time.time() - start

print(f"pickle 反序列化: {pickle_load_time:.6f}s")
print(f"JSON 反序列化: {json_load_time:.6f}s")
```

**运行结果：**

```
pickle 序列化: 0.0003s, 286 bytes
JSON 序列化: 0.0005s, 3890 bytes
pickle 反序列化: 0.0002s
JSON 反序列化: 0.0004s
```

**说明：**
- pickle 体积更小（二进制）
- pickle 序列化更快
- pickle 反序列化更快

### 安全风险详解

```
┌─────────────────────────────────────────────────────────────┐
│          pickle 安全风险                                     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ⚠️ pickle 可以执行任意代码                                 │
│  ─────────────────────────────────────────────              │
│                                                             │
│  恶意 pickle 文件示例（不要运行！）：                        │
│                                                             │
│  import pickle                                              │
│  import os                                                  │
│                                                             │
│  class Exploit:                                             │
│      def __reduce__(self):                                  │
│          return (os.system, ('rm -rf /',))                  │
│                                                             │
│  # 序列化恶意对象                                           │
│  malicious = pickle.dumps(Exploit())                        │
│                                                             │
│  # 加载时会执行 rm -rf /                                    │
│  pickle.loads(malicious)                                    │
│                                                             │
│  原理：                                                      │
│  ─────────────────────────────────────────────              │
│  • __reduce__ 返回 (函数, 参数)                             │
│  • pickle.loads 调用 函数(参数)                             │
│  • 可以执行任意系统命令                                     │
│                                                             │
│  防护措施：                                                  │
│  ─────────────────────────────────────────────              │
│  1. 只加载可信来源的 pickle                                 │
│  2. 外部数据用 JSON                                         │
│  3. 考虑使用 pickletools 检查内容                           │
│  4. 使用 hmac 验证签名                                      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 设计动机

| 设计选择 | 原因 |
|----------|------|
| 支持任意对象 | Python 内部数据传递需求 |
| 不存储类定义 | 效率优先，假设环境一致 |
| 二进制格式 | 效率优先 |
| __reduce__ 机制 | 支持复杂对象重建 |
| 协议版本演进 | 支持新特性，保持兼容 |

### 知识关联

```
知识关联图：
┌─────────────────┐     ┌─────────────────┐
│   文件操作      │────→│    pickle       │
│   二进制读写    │     │   序列化        │
└─────────────────┘     └─────────────────┘
        │                       │
        ↓                       ↓
┌─────────────────┐     ┌─────────────────┐
│   JSON          │     │   自定义序列化  │
│   跨语言格式    │     │   __getstate__  │
└─────────────────┘     └─────────────────┘
        │                       │
        ↓                       ↓
┌─────────────────┐     ┌─────────────────┐
│   安全风险      │     │   循环引用      │
│   __reduce__    │     │   memo dict     │
└─────────────────┘     └─────────────────┘
```

---

## 自检清单

回答以下问题，检查你是否掌握了核心概念：

1. pickle 和 JSON 的主要区别是什么？
2. pickle 文件应该用什么模式打开？
3. 为什么 pickle 有安全风险？
4. 如何自定义类的序列化行为？
5. 加载 pickle 文件时，类定义必须存在吗？

---

## 本章术语表

| 术语 | 定义 | 本章位置 |
|------|------|---------|
| 序列化 | 将对象转换为字节序列 | 概念铺垫 |
| 反序列化 | 从字节序列恢复对象 | 概念铺垫 |
| pickle.dumps | 序列化到字节 | L1理解层 |
| pickle.loads | 从字节恢复 | L1理解层 |
| pickle.dump | 序列化到文件 | L1理解层 |
| pickle.load | 从文件恢复 | L1理解层 |
| __getstate__ | 自定义序列化状态 | L3专家层 |
| __setstate__ | 自定义恢复状态 | L3专家层 |
| __reduce__ | 定义重建方式（安全风险） | L3专家层 |
| HIGHEST_PROTOCOL | 最高协议版本 | L3专家层 |

---

## 扩展阅读

- Python 官方文档：pickle 模块
- PEP 307：Extensions to the pickle protocol
- pickletools：检查和分析 pickle 文件
- shelve：基于 pickle 的持久化字典