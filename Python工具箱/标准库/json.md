# json 模块 - JSON 数据处理

JSON 是现代程序之间交换数据最常用的格式之一。Python 内置的 `json` 模块让我们可以轻松地在 Python 数据结构与 JSON 格式之间相互转换，无需安装任何第三方库。

---

## 第一部分：什么是 JSON

### 1.1 JSON 的概念

#### 概念说明

JSON（JavaScript Object Notation）是一种轻量级的数据交换格式。虽然名字里有 JavaScript，但它早已成为所有编程语言通用的数据格式。

可以把 JSON 想象成一种**通用快递包装规范**：

- 你有一箱货物（Python 数据），需要寄给另一个城市的朋友（另一个程序或服务器）
- 双方约定好用同一种包装方式（JSON 格式）
- 不管寄件方用什么工具打包，收件方都能按规范拆开读取

```
┌─────────────────────────────────────────────────────────────────┐
│                      JSON 的定位                                  │
│                                                                  │
│   Python 程序          JSON 字符串          其他程序/服务器        │
│   ┌─────────┐         ┌─────────────┐      ┌────────────┐       │
│   │ dict    │──序列化──│ {"key":"v"} │──────│ JavaScript │       │
│   │ list    │         │ [1, 2, 3]   │      │ Java       │       │
│   │ str     │◄─反序列─│ "hello"     │◄─────│ Go / Rust  │       │
│   └─────────┘         └─────────────┘      └────────────┘       │
│                                                                  │
│   序列化：Python 数据 → JSON 字符串（打包）                        │
│   反序列化：JSON 字符串 → Python 数据（拆包）                      │
└─────────────────────────────────────────────────────────────────┘
```

#### 示例代码

```python
# 一个标准的 JSON 字符串长这样
json_string = '''
{
    "name": "张三",
    "age": 25,
    "is_student": false,
    "scores": [90, 85, 92],
    "address": {
        "city": "北京",
        "zip": "100000"
    },
    "phone": null
}
'''

# 它就是普通的字符串，但有严格的格式规范
print(type(json_string))  # <class 'str'>
print(len(json_string))   # 字符数量
```

### 1.2 JSON 的语法规则

#### 概念说明

JSON 格式有几条严格的规定，与 Python 语法有所不同，初学者需要特别注意：

```
┌─────────────────────────────────────────────────────────────────┐
│                    JSON 语法规则对比                              │
│                                                                  │
│  规则         JSON                    Python                     │
│  ─────────────────────────────────────────────────────────────  │
│  字符串       必须用双引号 "abc"        可用单引号 'abc'            │
│  布尔值       true / false            True / False              │
│  空值         null                    None                      │
│  末尾逗号     不允许                   允许                        │
│  注释         不支持                   支持 #                     │
│  键           必须是字符串             可以是任意可哈希类型           │
└─────────────────────────────────────────────────────────────────┘
```

#### 示例代码

```python
# 合法的 JSON
valid_json = '{"name": "Alice", "active": true, "score": null}'

# 非法的 JSON（常见错误）
# 错误1：使用单引号
# invalid = "{'name': 'Alice'}"

# 错误2：末尾有多余逗号
# invalid = '{"name": "Alice", "age": 25,}'

# 错误3：使用 Python 的 True/False/None
# invalid = '{"active": True, "data": None}'

# 注意：JSON 中的 true 对应 Python 的 True
import json
data = json.loads('{"active": true, "value": null}')
print(data)           # {'active': True, 'value': None}
print(type(data))     # <class 'dict'>
```

---

## 第二部分：Python 类型与 JSON 类型的对应关系

### 2.1 类型映射表

#### 概念说明

Python 和 JSON 各有自己的数据类型系统，但它们之间有清晰的对应关系。理解这张映射表，是使用 `json` 模块的基础：

```
┌────────────────────────────────────────────────────────────────┐
│              Python 类型  ↔  JSON 类型 对照表                    │
│                                                                 │
│  Python 类型        JSON 类型        示例                        │
│  ──────────────────────────────────────────────────────────    │
│  dict              object           {"key": "value"}           │
│  list / tuple      array            [1, 2, 3]                  │
│  str               string           "hello"                    │
│  int               number           42                         │
│  float             number           3.14                       │
│  True              true             true                       │
│  False             false            false                      │
│  None              null             null                       │
│                                                                 │
│  注意：tuple 序列化后变成 array，反序列化回来是 list，不是 tuple   │
└────────────────────────────────────────────────────────────────┘
```

#### 示例代码

```python
import json

# 演示各种类型的转换
python_data = {
    "字典":   {"key": "value"},          # dict → object
    "列表":   [1, 2, 3],                 # list → array
    "元组":   (4, 5, 6),                 # tuple → array（注意！）
    "字符串": "hello",                   # str → string
    "整数":   42,                        # int → number
    "浮点数": 3.14,                      # float → number
    "真值":   True,                      # True → true
    "假值":   False,                     # False → false
    "空值":   None,                      # None → null
}

json_str = json.dumps(python_data, ensure_ascii=False, indent=2)
print(json_str)
```

输出：
```json
{
  "字典": {"key": "value"},
  "列表": [1, 2, 3],
  "元组": [4, 5, 6],
  "字符串": "hello",
  "整数": 42,
  "浮点数": 3.14,
  "真值": true,
  "假值": false,
  "空值": null
}
```

### 2.2 类型转换的注意事项

#### 概念说明

有几个类型转换的细节容易踩坑，需要格外注意：

1. **tuple 转换为 array 后，读回来是 list**：JSON 只有 array，没有 tuple
2. **int 的键转换为 string 键**：JSON 的 object 键只能是字符串
3. **不支持的 Python 类型**：`set`、`datetime`、自定义对象等无法直接序列化

#### 示例代码

```python
import json

# 陷阱1：tuple 反序列化变成 list
original = {"coords": (10, 20)}
serialized = json.dumps(original)
deserialized = json.loads(serialized)

print(original["coords"])       # (10, 20) — tuple
print(deserialized["coords"])   # [10, 20] — list！类型变了

# 陷阱2：整数键变成字符串键
original = {1: "one", 2: "two"}
serialized = json.dumps(original)
deserialized = json.loads(serialized)

print(original[1])         # "one"，键是整数 1
print(deserialized["1"])   # "one"，键变成了字符串 "1"
# print(deserialized[1])   # KeyError！

# 陷阱3：set 无法序列化
try:
    json.dumps({1, 2, 3})
except TypeError as e:
    print(f"错误：{e}")    # Object of type set is not JSON serializable
```

---

## 第三部分：序列化——Python 数据转为 JSON

### 3.1 json.dumps() 基础用法

#### 概念说明

`json.dumps()` 是最常用的序列化函数。函数名中的 **s** 代表 **string**，即把 Python 数据转换成 JSON **字符串**。

```
┌──────────────────────────────────────────────────────┐
│  json.dumps(obj, *, skipkeys=False,                  │
│             ensure_ascii=True,                       │
│             indent=None,                             │
│             separators=None,                         │
│             sort_keys=False,                         │
│             default=None)                            │
│                                                      │
│  常用参数：                                            │
│  obj          要序列化的 Python 对象                   │
│  indent        缩进空格数，用于美化输出                 │
│  ensure_ascii  False 时允许非 ASCII 字符（如中文）      │
│  sort_keys     True 时按键名排序                       │
│  default       处理不支持类型的回调函数                 │
└──────────────────────────────────────────────────────┘
```

#### 示例代码

```python
import json

# 基础用法
data = {"name": "Alice", "age": 30, "active": True}

# 最简单的调用
result = json.dumps(data)
print(result)
# 输出：{"name": "Alice", "age": 30, "active": true}
print(type(result))  # <class 'str'>

# 序列化各种基本类型
print(json.dumps(42))         # 42
print(json.dumps(3.14))       # 3.14
print(json.dumps("hello"))    # "hello"
print(json.dumps(True))       # true
print(json.dumps(None))       # null
print(json.dumps([1, 2, 3]))  # [1, 2, 3]
```

### 3.2 indent 参数——美化输出

#### 概念说明

默认情况下，`json.dumps()` 输出的是紧凑的单行字符串，不易阅读。使用 `indent` 参数可以让输出变得层次分明、易于阅读——就像把压缩的文件解压展开一样。

#### 示例代码

```python
import json

config = {
    "database": {
        "host": "localhost",
        "port": 5432,
        "name": "mydb"
    },
    "debug": False,
    "allowed_hosts": ["127.0.0.1", "example.com"]
}

# 不使用 indent（紧凑格式）
compact = json.dumps(config)
print("紧凑格式：")
print(compact)
# {"database": {"host": "localhost", "port": 5432, "name": "mydb"}, ...}

print()

# 使用 indent=2（每层缩进2个空格）
pretty = json.dumps(config, indent=2)
print("美化格式（indent=2）：")
print(pretty)
# {
#   "database": {
#     "host": "localhost",
#     "port": 5432,
#     "name": "mydb"
#   },
#   "debug": false,
#   "allowed_hosts": [
#     "127.0.0.1",
#     "example.com"
#   ]
# }

# 使用 indent=4（每层缩进4个空格，常见风格）
pretty4 = json.dumps(config, indent=4)
print("美化格式（indent=4）：")
print(pretty4)
```

### 3.3 ensure_ascii=False——正确处理中文

#### 概念说明

这是处理中文数据时**最重要**的参数。默认情况下，`ensure_ascii=True`，会把所有非 ASCII 字符（包括中文）转义成 `\uXXXX` 格式，导致输出难以阅读。

设置 `ensure_ascii=False` 后，中文字符会原样保留在 JSON 字符串中。

#### 示例代码

```python
import json

data = {
    "姓名": "张三",
    "城市": "北京",
    "描述": "这是一段中文描述"
}

# 默认 ensure_ascii=True（中文被转义）
default_output = json.dumps(data)
print("默认（中文被转义）：")
print(default_output)
# {"\u59d3\u540d": "\u5f20\u4e09", "\u57ce\u5e02": "\u5317\u4eac", ...}
# 看不懂！

print()

# ensure_ascii=False（保留中文原文）
readable_output = json.dumps(data, ensure_ascii=False)
print("ensure_ascii=False（中文正常显示）：")
print(readable_output)
# {"姓名": "张三", "城市": "北京", "描述": "这是一段中文描述"}

print()

# 结合 indent 和 ensure_ascii=False，最佳可读性
best = json.dumps(data, ensure_ascii=False, indent=2)
print("最佳可读格式：")
print(best)
```

### 3.4 sort_keys 参数——排序键名

#### 概念说明

`sort_keys=True` 会让 JSON 输出时按键名的字母顺序排列。这在需要对比两个 JSON 结构，或者要生成稳定、可预期的输出时非常有用。

#### 示例代码

```python
import json

user = {
    "username": "alice",
    "email": "alice@example.com",
    "age": 28,
    "active": True,
    "created_at": "2024-01-15"
}

# 不排序（保持原始顺序）
print("不排序：")
print(json.dumps(user, indent=2))

print()

# 排序键名
print("按键名排序（sort_keys=True）：")
print(json.dumps(user, indent=2, sort_keys=True))
# {
#   "active": true,
#   "age": 28,
#   "created_at": "2024-01-15",
#   "email": "alice@example.com",
#   "username": "alice"
# }
```

---

## 第四部分：反序列化——JSON 转为 Python 数据

### 4.1 json.loads() 基础用法

#### 概念说明

`json.loads()` 是 `json.dumps()` 的逆操作，把 JSON 字符串解析成 Python 数据结构。同样，函数名中的 **s** 代表 **string**。

#### 示例代码

```python
import json

# 基础用法
json_string = '{"name": "Bob", "age": 25, "active": true, "score": null}'

data = json.loads(json_string)
print(data)
# {'name': 'Bob', 'age': 25, 'active': True, 'score': None}

print(type(data))           # <class 'dict'>
print(data["name"])         # Bob
print(data["active"])       # True（注意：已经是 Python 的 True）
print(data["score"])        # None（注意：已经是 Python 的 None）

# 解析 JSON 数组
json_array = '[1, 2, 3, "hello", true, null]'
result = json.loads(json_array)
print(result)               # [1, 2, 3, 'hello', True, None]
print(type(result))         # <class 'list'>

# 解析嵌套结构
json_nested = '''
{
    "user": {
        "name": "Charlie",
        "hobbies": ["读书", "编程", "跑步"]
    }
}
'''
nested_data = json.loads(json_nested)
print(nested_data["user"]["name"])       # Charlie
print(nested_data["user"]["hobbies"])    # ['读书', '编程', '跑步']
```

### 4.2 反序列化的类型注意事项

#### 概念说明

反序列化时，有几个类型转换细节需要注意，避免程序出现意外的 bug。

#### 示例代码

```python
import json

# 注意1：所有 JSON 对象的键，反序列化后都是字符串
json_str = '{"1": "one", "2": "two"}'
data = json.loads(json_str)
print(data)          # {'1': 'one', '2': 'two'}
print(type(list(data.keys())[0]))  # <class 'str'>，键是字符串

# 注意2：JSON 数字可能是 int 或 float
json_nums = '{"integer": 42, "float": 3.14}'
nums = json.loads(json_nums)
print(type(nums["integer"]))  # <class 'int'>
print(type(nums["float"]))    # <class 'float'>

# 注意3：JSON 数组变成 Python list（不是 tuple）
json_array = '[[1, 2], [3, 4]]'
result = json.loads(json_array)
print(type(result[0]))  # <class 'list'>

# 注意4：解析错误时会抛出 JSONDecodeError
try:
    bad_json = "{'name': 'Alice'}"  # 单引号，非法 JSON
    json.loads(bad_json)
except json.JSONDecodeError as e:
    print(f"JSON 格式错误：{e}")
    # JSON 格式错误：Expecting property name enclosed in double quotes: line 1 column 2 (char 1)
```

---

## 第五部分：文件操作——读写 JSON 文件

### 5.1 json.dump() 写入文件

#### 概念说明

`json.dump()`（没有末尾的 s）直接把 Python 数据序列化后写入文件对象，省去了手动调用 `dumps()` 再写文件的步骤。

#### 示例代码

```python
import json

config = {
    "app_name": "MyApp",
    "version": "1.0.0",
    "debug": False,
    "database": {
        "host": "localhost",
        "port": 5432
    },
    "features": ["login", "dashboard", "reports"]
}

# 写入 JSON 文件
with open("config.json", "w", encoding="utf-8") as f:
    json.dump(config, f, ensure_ascii=False, indent=2)

print("配置文件已保存！")

# 写入包含中文的数据
user_data = {
    "用户列表": [
        {"姓名": "张三", "年龄": 25},
        {"姓名": "李四", "年龄": 30}
    ]
}

with open("users.json", "w", encoding="utf-8") as f:
    json.dump(user_data, f, ensure_ascii=False, indent=4)

print("用户数据已保存！")
```

### 5.2 json.load() 读取文件

#### 概念说明

`json.load()`（没有末尾的 s）从文件对象中读取 JSON 数据并反序列化为 Python 数据结构。

#### 示例代码

```python
import json

# 读取 JSON 文件
try:
    with open("config.json", "r", encoding="utf-8") as f:
        config = json.load(f)
    
    print(f"应用名称：{config['app_name']}")
    print(f"版本：{config['version']}")
    print(f"调试模式：{config['debug']}")
    print(f"数据库主机：{config['database']['host']}")

except FileNotFoundError:
    print("配置文件不存在，使用默认配置")
    config = {"debug": True}

except json.JSONDecodeError as e:
    print(f"配置文件格式错误：{e}")
    config = {}

# 读取用户数据
try:
    with open("users.json", "r", encoding="utf-8") as f:
        user_data = json.load(f)
    
    for user in user_data["用户列表"]:
        print(f"姓名：{user['姓名']}，年龄：{user['年龄']}")

except FileNotFoundError:
    print("用户数据文件不存在")
```

---

## 第六部分：记忆口诀——s 结尾处理字符串，无 s 处理文件

### 6.1 四个核心函数一览

#### 概念说明

`json` 模块最核心的四个函数，用一句话记住：**有 s 处理字符串，无 s 处理文件**。

```
┌─────────────────────────────────────────────────────────────────┐
│                  json 模块四大核心函数                             │
│                                                                  │
│  序列化方向                                                        │
│  Python 数据 ──────────────────────────────► JSON               │
│                                                                  │
│         dumps(obj)   → 返回 JSON 字符串（s = string）            │
│         dump(obj, f) → 直接写入文件 f（无 s = file）             │
│                                                                  │
│  反序列化方向                                                      │
│  Python 数据 ◄──────────────────────────────── JSON             │
│                                                                  │
│         loads(s)     → 解析 JSON 字符串（s = string）            │
│         load(f)      → 从文件 f 读取解析（无 s = file）           │
│                                                                  │
│  ┌──────────┬─────────────┬───────────────────────────────┐     │
│  │ 函数     │ 输入/输出   │ 用途                           │     │
│  ├──────────┼─────────────┼───────────────────────────────┤     │
│  │ dumps()  │ 返回字符串  │ 序列化为字符串（网络传输等）    │     │
│  │ dump()   │ 写入文件    │ 序列化到文件（保存配置等）      │     │
│  │ loads()  │ 接收字符串  │ 解析字符串（处理 API 响应等）   │     │
│  │ load()   │ 读取文件    │ 从文件反序列化（读取配置等）    │     │
│  └──────────┴─────────────┴───────────────────────────────┘     │
└─────────────────────────────────────────────────────────────────┘
```

#### 示例代码

```python
import json

data = {"message": "你好", "count": 42}

# ── 有 s：操作字符串 ──────────────────────────
# dumps：Python → JSON 字符串
json_str = json.dumps(data, ensure_ascii=False)
print(type(json_str))   # <class 'str'>

# loads：JSON 字符串 → Python
parsed = json.loads(json_str)
print(type(parsed))     # <class 'dict'>

# ── 无 s：操作文件 ────────────────────────────
# dump：Python → 文件
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False)

# load：文件 → Python
with open("data.json", "r", encoding="utf-8") as f:
    loaded = json.load(f)
print(type(loaded))     # <class 'dict'>
```

---

## 第七部分：高级用法

### 7.1 处理日期时间对象

#### 概念说明

`datetime` 是 Python 中最常用的类型之一，但 JSON 原生不支持它。有几种常见的处理方式：

1. **转为字符串**（最常用）：序列化时转成 ISO 格式字符串，读取时再解析回来
2. **自定义序列化器**：通过 `default` 参数或继承 `JSONEncoder`

#### 示例代码

```python
import json
from datetime import datetime, date

# 方法一：序列化前手动转为字符串
data = {
    "event": "会议",
    "time": datetime.now().isoformat(),   # 转为 ISO 格式字符串
    "date": date.today().isoformat()
}
print(json.dumps(data, ensure_ascii=False, indent=2))

# 方法二：使用 default 参数——自定义序列化回调
def custom_serializer(obj):
    """处理 json 模块无法序列化的类型"""
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError(f"类型 {type(obj)} 无法序列化")

data_with_datetime = {
    "event": "生日派对",
    "created_at": datetime(2024, 6, 1, 14, 30, 0),
    "event_date": date(2024, 6, 15)
}

result = json.dumps(
    data_with_datetime,
    default=custom_serializer,
    ensure_ascii=False,
    indent=2
)
print(result)

# 方法三：继承 JSONEncoder（适合需要复用的场景）
class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        return super().default(obj)

result2 = json.dumps(
    data_with_datetime,
    cls=DateTimeEncoder,
    ensure_ascii=False,
    indent=2
)
print(result2)
```

### 7.2 处理自定义对象

#### 概念说明

当需要序列化自定义类的实例时，需要定义如何把对象转成可序列化的字典。反序列化时，通过 `object_hook` 参数把字典还原成对象。

#### 示例代码

```python
import json

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __repr__(self):
        return f"Point({self.x}, {self.y})"

class Rectangle:
    def __init__(self, top_left: Point, bottom_right: Point):
        self.top_left = top_left
        self.bottom_right = bottom_right
    
    def __repr__(self):
        return f"Rectangle({self.top_left}, {self.bottom_right})"

# 序列化自定义对象：转为字典
def encode_shape(obj):
    if isinstance(obj, Point):
        return {"__type__": "Point", "x": obj.x, "y": obj.y}
    if isinstance(obj, Rectangle):
        return {
            "__type__": "Rectangle",
            "top_left": encode_shape(obj.top_left),
            "bottom_right": encode_shape(obj.bottom_right)
        }
    raise TypeError(f"无法序列化类型：{type(obj)}")

rect = Rectangle(Point(0, 10), Point(20, 0))
json_str = json.dumps(rect, default=encode_shape, indent=2)
print("序列化结果：")
print(json_str)

# 反序列化自定义对象：通过 object_hook 还原
def decode_shape(dct):
    if "__type__" not in dct:
        return dct
    if dct["__type__"] == "Point":
        return Point(dct["x"], dct["y"])
    if dct["__type__"] == "Rectangle":
        return Rectangle(dct["top_left"], dct["bottom_right"])
    return dct

restored = json.loads(json_str, object_hook=decode_shape)
print("\n反序列化结果：")
print(restored)              # Rectangle(Point(0, 10), Point(20, 0))
print(type(restored))        # <class '__main__.Rectangle'>
print(type(restored.top_left))  # <class '__main__.Point'>
```

### 7.3 处理特殊数值

#### 概念说明

Python 的 `float` 有 `nan`（非数字）和 `inf`（无穷大）两个特殊值，但标准 JSON 不支持它们。`json` 模块的默认行为是输出非标准的 `NaN` 和 `Infinity`，这在某些严格的 JSON 解析器中会报错。

#### 示例代码

```python
import json
import math

# 默认行为：输出非标准的 NaN 和 Infinity
data = {"value": float("nan"), "limit": float("inf")}
result = json.dumps(data)
print(result)   # {"value": NaN, "limit": Infinity}（非标准 JSON！）

# 解决方案：序列化前替换特殊值
def sanitize_float(obj):
    """把特殊浮点数替换为 None 或字符串"""
    if isinstance(obj, float):
        if math.isnan(obj):
            return None
        if math.isinf(obj):
            return None  # 或者返回 "Infinity" 字符串
    raise TypeError(f"无法序列化类型：{type(obj)}")

safe_result = json.dumps(data, default=sanitize_float)
print(safe_result)  # {"value": null, "limit": null}
```

---

## 第八部分：综合实例

### 8.1 配置文件管理

#### 概念说明

JSON 是存储应用配置的常用格式。下面实现一个带默认值回退、自动创建和安全读写的配置管理器。

#### 示例代码

```python
import json
import os

CONFIG_FILE = "app_config.json"

DEFAULT_CONFIG = {
    "app_name": "MyApplication",
    "version": "1.0.0",
    "debug": False,
    "log_level": "INFO",
    "database": {
        "host": "localhost",
        "port": 5432,
        "name": "mydb",
        "pool_size": 5
    },
    "server": {
        "host": "0.0.0.0",
        "port": 8080,
        "workers": 4
    },
    "features": {
        "enable_cache": True,
        "cache_ttl": 300
    }
}

def load_config(filepath: str = CONFIG_FILE) -> dict:
    """读取配置文件，若文件不存在则返回默认配置"""
    if not os.path.exists(filepath):
        print(f"配置文件 {filepath} 不存在，使用默认配置")
        return DEFAULT_CONFIG.copy()
    
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            config = json.load(f)
        print(f"配置文件加载成功：{filepath}")
        return config
    except json.JSONDecodeError as e:
        print(f"配置文件格式错误：{e}，使用默认配置")
        return DEFAULT_CONFIG.copy()

def save_config(config: dict, filepath: str = CONFIG_FILE) -> bool:
    """保存配置到 JSON 文件"""
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        print(f"配置文件已保存：{filepath}")
        return True
    except IOError as e:
        print(f"保存配置文件失败：{e}")
        return False

def update_config(key_path: str, value, filepath: str = CONFIG_FILE):
    """更新配置中的某个值（支持点分路径，如 'database.host'）"""
    config = load_config(filepath)
    
    keys = key_path.split(".")
    target = config
    for key in keys[:-1]:
        target = target.setdefault(key, {})
    target[keys[-1]] = value
    
    save_config(config, filepath)
    print(f"已更新 {key_path} = {value}")

# 使用示例
config = load_config()
print(f"应用：{config['app_name']} v{config['version']}")
print(f"数据库：{config['database']['host']}:{config['database']['port']}")

# 修改并保存
config["debug"] = True
config["server"]["port"] = 9090
save_config(config)

# 通过路径更新单个键
update_config("database.host", "db.example.com")
update_config("features.enable_cache", False)
```

### 8.2 用户数据持久化

#### 概念说明

用 JSON 文件实现简单的用户数据存储，包含增删改查操作。

#### 示例代码

```python
import json
import os
from datetime import datetime

USERS_FILE = "users.json"

def load_users() -> list:
    """加载所有用户数据"""
    if not os.path.exists(USERS_FILE):
        return []
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_users(users: list) -> None:
    """保存用户数据到文件"""
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)

def add_user(name: str, email: str, role: str = "user") -> dict:
    """添加新用户"""
    users = load_users()
    
    # 检查邮箱是否已存在
    if any(u["email"] == email for u in users):
        print(f"错误：邮箱 {email} 已存在")
        return {}
    
    new_user = {
        "id": len(users) + 1,
        "name": name,
        "email": email,
        "role": role,
        "created_at": datetime.now().isoformat(),
        "active": True
    }
    users.append(new_user)
    save_users(users)
    print(f"用户 {name} 已添加，ID = {new_user['id']}")
    return new_user

def find_user(user_id: int) -> dict:
    """根据 ID 查找用户"""
    users = load_users()
    for user in users:
        if user["id"] == user_id:
            return user
    return {}

def update_user(user_id: int, **kwargs) -> bool:
    """更新用户信息"""
    users = load_users()
    for user in users:
        if user["id"] == user_id:
            user.update(kwargs)
            save_users(users)
            print(f"用户 ID={user_id} 已更新：{kwargs}")
            return True
    print(f"用户 ID={user_id} 不存在")
    return False

def delete_user(user_id: int) -> bool:
    """删除用户"""
    users = load_users()
    original_count = len(users)
    users = [u for u in users if u["id"] != user_id]
    if len(users) < original_count:
        save_users(users)
        print(f"用户 ID={user_id} 已删除")
        return True
    print(f"用户 ID={user_id} 不存在")
    return False

# 使用示例
add_user("张三", "zhangsan@example.com", "admin")
add_user("李四", "lisi@example.com")
add_user("王五", "wangwu@example.com")

user = find_user(2)
print(f"\n查找用户2：{user['name']} ({user['email']})")

update_user(2, name="李四（已更新）", role="moderator")

all_users = load_users()
print(f"\n当前所有用户（共 {len(all_users)} 人）：")
for u in all_users:
    status = "活跃" if u["active"] else "禁用"
    print(f"  [{u['id']}] {u['name']} - {u['role']} - {status}")

delete_user(3)
```

### 8.3 API 响应数据处理

#### 概念说明

与 Web API 交互时，响应数据通常是 JSON 格式的字符串。结合 `requests` 库（或标准库的 `urllib`），可以方便地处理 API 数据。

#### 示例代码

```python
import json

# 模拟一个 API 返回的 JSON 响应字符串
# 实际使用时，这来自 requests.get(url).text 或 response.json()
api_response = '''
{
    "status": "success",
    "code": 200,
    "data": {
        "total": 3,
        "page": 1,
        "items": [
            {
                "id": 101,
                "title": "Python 入门指南",
                "author": "张老师",
                "tags": ["python", "入门", "教程"],
                "published": true,
                "views": 15230
            },
            {
                "id": 102,
                "title": "JSON 数据处理",
                "author": "李工程师",
                "tags": ["json", "数据处理"],
                "published": true,
                "views": 8765
            },
            {
                "id": 103,
                "title": "数据库设计草稿",
                "author": "王设计师",
                "tags": ["数据库"],
                "published": false,
                "views": 0
            }
        ]
    },
    "timestamp": "2024-06-01T10:30:00"
}
'''

def process_api_response(json_str: str) -> list:
    """解析 API 响应，提取已发布的文章"""
    try:
        response = json.loads(json_str)
        
        # 检查响应状态
        if response.get("status") != "success":
            print(f"API 返回错误状态：{response.get('status')}")
            return []
        
        items = response["data"]["items"]
        
        # 过滤已发布的文章，并按浏览量排序
        published = [item for item in items if item["published"]]
        published.sort(key=lambda x: x["views"], reverse=True)
        
        return published
    
    except json.JSONDecodeError as e:
        print(f"JSON 解析失败：{e}")
        return []
    except KeyError as e:
        print(f"数据结构异常，缺少字段：{e}")
        return []

articles = process_api_response(api_response)
print(f"已发布文章（按浏览量排序）：")
for article in articles:
    tags_str = "、".join(article["tags"])
    print(f"  [{article['id']}] {article['title']}")
    print(f"       作者：{article['author']}  |  浏览量：{article['views']:,}  |  标签：{tags_str}")
```

### 8.4 JSON 文件模拟简单数据库

#### 概念说明

对于小型项目，可以用 JSON 文件实现一个简单的键值存储，支持持久化。

#### 示例代码

```python
import json
import os
from typing import Any, Optional

class JsonDatabase:
    """基于 JSON 文件的简单键值数据库"""
    
    def __init__(self, filepath: str):
        self.filepath = filepath
        self._data = self._load()
    
    def _load(self) -> dict:
        """从文件加载数据"""
        if not os.path.exists(self.filepath):
            return {}
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(f"警告：数据库文件损坏，已重置")
            return {}
    
    def _save(self) -> None:
        """将数据保存到文件"""
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(self._data, f, ensure_ascii=False, indent=2)
    
    def set(self, key: str, value: Any) -> None:
        """设置键值"""
        self._data[key] = value
        self._save()
    
    def get(self, key: str, default: Any = None) -> Any:
        """获取键值"""
        return self._data.get(key, default)
    
    def delete(self, key: str) -> bool:
        """删除键"""
        if key in self._data:
            del self._data[key]
            self._save()
            return True
        return False
    
    def exists(self, key: str) -> bool:
        """检查键是否存在"""
        return key in self._data
    
    def keys(self) -> list:
        """返回所有键"""
        return list(self._data.keys())
    
    def clear(self) -> None:
        """清空所有数据"""
        self._data = {}
        self._save()
    
    def __len__(self) -> int:
        return len(self._data)
    
    def __repr__(self) -> str:
        return f"JsonDatabase('{self.filepath}', {len(self)} keys)"

# 使用示例
db = JsonDatabase("store.json")

# 存储各种类型的数据
db.set("counter", 0)
db.set("user_prefs", {"theme": "dark", "language": "zh"})
db.set("recent_files", ["/home/user/a.py", "/home/user/b.py"])
db.set("greeting", "你好，世界")

print(f"数据库：{db}")
print(f"计数器：{db.get('counter')}")
print(f"用户偏好：{db.get('user_prefs')}")
print(f"最近文件：{db.get('recent_files')}")

# 更新
current_counter = db.get("counter", 0)
db.set("counter", current_counter + 1)
print(f"计数器自增后：{db.get('counter')}")

# 检查和删除
print(f"greeting 存在：{db.exists('greeting')}")
db.delete("greeting")
print(f"删除后 greeting 存在：{db.exists('greeting')}")
print(f"不存在的键（带默认值）：{db.get('greeting', '（已删除）')}")

print(f"\n所有键：{db.keys()}")
```

---

## 第九部分：常见错误与调试

### 9.1 JSONDecodeError——解析失败

#### 概念说明

`json.JSONDecodeError` 是解析 JSON 字符串失败时抛出的异常，通常是因为 JSON 格式不符合规范。

#### 示例代码

```python
import json

def safe_parse(json_str: str) -> Optional[Any]:
    """安全地解析 JSON 字符串，失败时返回 None"""
    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        # e.msg: 错误类型描述
        # e.lineno: 出错行号
        # e.colno: 出错列号
        # e.pos: 出错的字符位置
        print(f"JSON 解析失败：")
        print(f"  错误描述：{e.msg}")
        print(f"  位置：第 {e.lineno} 行第 {e.colno} 列（字符位置 {e.pos}）")
        print(f"  问题字符串：{json_str[max(0, e.pos-10):e.pos+10]!r}")
        return None

# 常见的 JSON 格式错误
test_cases = [
    ("{'name': 'Alice'}",        "使用单引号"),
    ('{"name": "Alice",}',       "末尾多余逗号"),
    ('{"active": True}',         "使用 Python 的 True"),
    ('{"value": undefined}',     "使用未定义值"),
    ('{"text": "line1\nline2"}', "字符串中包含未转义换行"),
    ('{"name": "Bob"',           "缺少结束括号"),
]

for json_str, description in test_cases:
    print(f"\n测试：{description}")
    print(f"  输入：{json_str!r}")
    result = safe_parse(json_str)
    if result is not None:
        print(f"  结果：{result}")
```

### 9.2 TypeError——不可序列化的类型

#### 概念说明

当尝试序列化 JSON 不支持的 Python 类型时，会抛出 `TypeError`。常见的不可序列化类型包括：`set`、`datetime`、自定义类实例、`bytes` 等。

#### 示例代码

```python
import json
from datetime import datetime

# 会触发 TypeError 的情况
problematic_data = [
    ({1, 2, 3},                      "set 类型"),
    (datetime.now(),                  "datetime 对象"),
    (b"bytes data",                   "bytes 类型"),
    (lambda x: x,                     "函数/lambda"),
    (object(),                        "自定义对象"),
]

for obj, description in problematic_data:
    try:
        json.dumps(obj)
        print(f"{description}：序列化成功（意外）")
    except TypeError as e:
        print(f"{description}：{e}")

print()

# 解决方案：使用 default 参数统一处理
def flexible_serializer(obj):
    """通用序列化处理器"""
    if isinstance(obj, set):
        return sorted(list(obj))       # set → 排序后的 list
    if isinstance(obj, datetime):
        return obj.isoformat()          # datetime → ISO 字符串
    if isinstance(obj, bytes):
        return obj.decode("utf-8", errors="replace")  # bytes → 字符串
    # 对于其他不支持的类型，返回其字符串表示
    return str(obj)

data = {
    "tags": {1, 2, 3},
    "timestamp": datetime.now(),
    "raw": b"hello bytes"
}
result = json.dumps(data, default=flexible_serializer, ensure_ascii=False, indent=2)
print(result)
```

### 9.3 中文乱码问题

#### 概念说明

中文乱码是最常见的问题之一，通常由以下两个原因导致：
1. 序列化时没有设置 `ensure_ascii=False`，中文被转义
2. 读写文件时没有指定 `encoding="utf-8"`

#### 示例代码

```python
import json

data = {"message": "你好世界", "city": "北京"}

# 问题1：ensure_ascii=True（默认）导致中文转义
print("问题：中文被转义")
print(json.dumps(data))
# {"message": "\u4f60\u597d\u4e16\u754c", "city": "\u5317\u4eac"}

print()

# 解决：设置 ensure_ascii=False
print("解决：设置 ensure_ascii=False")
print(json.dumps(data, ensure_ascii=False))
# {"message": "你好世界", "city": "北京"}

print()

# 问题2：写文件时编码不匹配
# 错误示范（在某些系统上可能导致乱码）
# with open("bad.json", "w") as f:  # 没有指定编码
#     json.dump(data, f, ensure_ascii=False)

# 正确示范：始终明确指定 UTF-8 编码
with open("correct.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

with open("correct.json", "r", encoding="utf-8") as f:
    loaded = json.load(f)

print(f"正确读取中文：{loaded['message']}")  # 你好世界

# 最佳实践总结
print("\n中文处理最佳实践：")
print("1. dumps/dump：始终加 ensure_ascii=False")
print("2. open()：始终加 encoding='utf-8'")
print("3. 这两点缺一不可！")
```

---

## 第十部分：JSON 与 Python 字典的区别

### 10.1 核心区别对比

#### 概念说明

很多初学者会混淆 JSON 字符串和 Python 字典。它们看起来相似，但本质上是两种完全不同的东西：

```
┌─────────────────────────────────────────────────────────────────┐
│              JSON 字符串  vs  Python 字典                         │
│                                                                  │
│  维度          JSON 字符串              Python 字典               │
│  ──────────────────────────────────────────────────────────     │
│  本质          普通文本字符串            内存中的数据结构           │
│  类型          str                      dict                     │
│  键的引号      必须用双引号              可以不用引号               │
│  布尔值        true / false             True / False             │
│  空值          null                     None                     │
│  末尾逗号      不允许                   允许                       │
│  注释          不支持                   支持（代码注释）            │
│  操作方式      字符串操作               字典方法（.get, .keys）     │
│  存储/传输     适合                     不适合（需转换）            │
│  运算          不可以直接运算            可以直接存取、修改          │
└─────────────────────────────────────────────────────────────────┘
```

#### 示例代码

```python
import json

# Python 字典（内存中的数据结构）
python_dict = {"name": "Alice", "age": 30, "active": True, "data": None}
print("Python 字典：")
print(f"  类型：{type(python_dict)}")     # <class 'dict'>
print(f"  访问：{python_dict['name']}")   # Alice
print(f"  方法：{list(python_dict.keys())}")  # ['name', 'age', 'active', 'data']

print()

# JSON 字符串（文本格式）
json_string = '{"name": "Alice", "age": 30, "active": true, "data": null}'
print("JSON 字符串：")
print(f"  类型：{type(json_string)}")     # <class 'str'>
print(f"  长度：{len(json_string)} 字符")
# 不能直接访问字段，必须先解析
# print(json_string["name"])  # TypeError！

print()

# 转换方向
print("转换：")
as_json = json.dumps(python_dict, ensure_ascii=False)
as_dict = json.loads(as_json)
print(f"  dict → JSON：{as_json}")
print(f"  JSON → dict：{as_dict}")
print(f"  往返后相等：{python_dict == as_dict}")  # True（基本类型相同时）

print()

# 常见误区：字符串不是字典
print("常见误区：")
json_like = '{"x": 1}'
print(f"  这是字符串：{type(json_like)}")
# json_like["x"]  # TypeError: string indices must be integers

parsed = json.loads(json_like)
print(f"  解析后才是字典：{type(parsed)}")
print(f"  正确访问：{parsed['x']}")       # 1
```

### 10.2 选择使用哪种形式

#### 概念说明

了解何时使用 JSON 字符串，何时使用 Python 字典，对编写清晰的代码很有帮助：

```
┌─────────────────────────────────────────────────────────────────┐
│                    使用场景决策图                                  │
│                                                                  │
│  需要在程序内部处理数据？                                           │
│  ────────────────────────                                        │
│  是 → 使用 Python 字典（dict）                                    │
│       可以直接访问、修改、遍历                                      │
│                                                                  │
│  需要存储到文件或通过网络传输？                                      │
│  ────────────────────────────                                    │
│  是 → 转换为 JSON 字符串                                           │
│       使用 json.dumps() 或 json.dump()                           │
│                                                                  │
│  从文件或网络收到数据？                                             │
│  ──────────────────────                                          │
│  是 → 解析为 Python 字典                                          │
│       使用 json.loads() 或 json.load()                           │
└─────────────────────────────────────────────────────────────────┘
```

#### 示例代码

```python
import json

# 典型的数据流程：接收 → 处理 → 保存

# 1. 从外部接收 JSON 数据（字符串形式）
received_json = '{"orders": [{"id": 1, "amount": 99.9}, {"id": 2, "amount": 199.0}]}'

# 2. 解析为 Python 字典，便于程序内部处理
orders_data = json.loads(received_json)

# 3. 在 Python 中处理数据（使用字典方法）
total = sum(order["amount"] for order in orders_data["orders"])
orders_data["total"] = total
orders_data["order_count"] = len(orders_data["orders"])

# 4. 保存到文件（转换回 JSON）
with open("orders.json", "w", encoding="utf-8") as f:
    json.dump(orders_data, f, ensure_ascii=False, indent=2)

print(f"订单总数：{orders_data['order_count']}")
print(f"订单总额：{orders_data['total']}")
```

---

## 总结

本章介绍了 Python `json` 模块的核心用法，以下是关键要点回顾：

```
┌─────────────────────────────────────────────────────────────────┐
│                      json 模块知识地图                            │
│                                                                  │
│  核心函数（口诀：有 s 处理字符串，无 s 处理文件）                    │
│  ┌───────────┬────────────────────────────────────────┐        │
│  │ dumps()   │ Python → JSON 字符串                    │        │
│  │ dump()    │ Python → JSON 文件                      │        │
│  │ loads()   │ JSON 字符串 → Python                    │        │
│  │ load()    │ JSON 文件 → Python                      │        │
│  └───────────┴────────────────────────────────────────┘        │
│                                                                  │
│  重要参数                                                         │
│  ┌──────────────────┬────────────────────────────────┐         │
│  │ ensure_ascii=False│ 保留中文等非 ASCII 字符         │         │
│  │ indent=2          │ 美化输出，添加缩进              │         │
│  │ sort_keys=True    │ 按键名排序输出                  │         │
│  │ default=func      │ 处理不支持类型的回调            │         │
│  └──────────────────┴────────────────────────────────┘         │
│                                                                  │
│  常见异常                                                         │
│  ┌────────────────────┬──────────────────────────────┐         │
│  │ JSONDecodeError    │ JSON 格式错误，解析失败         │         │
│  │ TypeError          │ 遇到不支持的 Python 类型        │         │
│  └────────────────────┴──────────────────────────────┘         │
│                                                                  │
│  最佳实践                                                         │
│  1. 处理中文：始终加 ensure_ascii=False                           │
│  2. 文件读写：始终指定 encoding="utf-8"                           │
│  3. 异常处理：捕获 JSONDecodeError 和 TypeError                   │
│  4. 调试输出：使用 indent=2 让 JSON 可读                          │
└─────────────────────────────────────────────────────────────────┘
```

---

[返回索引](../README.md) | [返回 11-模块与包](../11-模块与包.md)
