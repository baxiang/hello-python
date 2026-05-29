# 05-json数据处理

> Python 3.11+

---

## 为什么需要 json 模块？

### 问题场景

你开发了一个用户管理接口，需要把 Python 字典返回给前端：

```python
user = {"name": "张三", "age": 25, "vip": True, "address": None}

# ❌ 直接拼字符串：容易出错，特殊字符没转义
result = str(user)   # {'name': '张三', ...}  Python 语法，前端无法解析

# ✅ 用 json 模块：生成标准 JSON，全球通用
import json
result = json.dumps(user, ensure_ascii=False)
# {"name": "张三", "age": 25, "vip": true, "address": null}
```

JSON 是前后端、跨语言传数据的通用格式，`json` 模块是处理它的标准工具。

---

## 概念铺垫

`json` 模块在 CPython 中由 C 扩展实现（`Modules/_json.c`，约 2000 行），提供高性能的 JSON 编解码。其核心是两个 C 类型：`JSONEncoder` 和 `JSONDecoder`，通过 `object_hook` 和 `default` 回调实现与 Python 对象的桥接。

```
┌──────────────────────────────────────────────────────────────┐
│          json 模块编解码流程                                  │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│   序列化流程（Python → JSON）：                                │
│   ┌─────────┐    ┌──────────┐    ┌──────────┐    ┌────────┐ │
│   │ Python  │───→│_make_iter│───→│_encoder  │───→│ JSON   │ │
│   │  对象   │    │ _encode  │    │ C 扩展   │    │ 字符串  │ │
│   └─────────┘    └──────────┘    └──────────┘    └────────┘ │
│        │                            │                        │
│        ↓ default=func               ↓ cls=JSONEncoder        │
│   不支持的类型 → 调用 default    自定义整个编码逻辑             │
│                                                              │
│   反序列化流程（JSON → Python）：                              │
│   ┌─────────┐    ┌──────────┐    ┌──────────┐    ┌────────┐ │
│   │  JSON   │───→│ JSON     │───→│_decoder  │───→│ Python │ │
│   │  字符串 │    │  解析器  │    │ C 扩展   │    │  对象   │ │
│   └─────────┘    └──────────┘    └──────────┘    └────────┘ │
│                                        │                      │
│                                        ↓ object_hook         │
│                                  每个 {} → 回调函数            │
│                                                              │
│   性能关键：C 扩展中 JSON 扫描和 UTF-8 编解码比纯 Python      │
│   快 10-50 倍。python -m json.tool 格式化工具也在内部使用      │
│   同样的 C 编码器。                                          │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

### L1 理解层：会用

## JSON 格式介绍

### 什么是 JSON

JSON（JavaScript Object Notation）是一种用纯文本表示结构化数据的格式。它独立于编程语言，被广泛用于 Web API、配置文件、数据存储。

一个完整的 JSON 文档示例，包含所有六种类型：

```json
{
  "name": "张三",
  "age": 25,
  "score": 98.5,
  "is_vip": true,
  "deleted_at": null,
  "tags": ["python", "web", "api"],
  "address": {
    "city": "北京",
    "zip": "100000"
  }
}
```

### JSON 的六种数据类型

```
┌──────────────────────────────────────────────────────────────┐
│                    JSON 六种数据类型                          │
├────────────┬──────────────────────┬──────────────────────────┤
│  类型       │  示例                │  说明                    │
├────────────┼──────────────────────┼──────────────────────────┤
│  string    │  "hello"  "张三"     │  必须用双引号，不能单引号  │
│  number    │  25  98.5  -3  1e10  │  整数或浮点数，无引号      │
│  boolean   │  true  false         │  全小写，无引号            │
│  null      │  null                │  全小写，无引号            │
│  array     │  [1, "a", true]      │  方括号，元素可混合类型    │
│  object    │  {"key": "value"}    │  花括号，键必须是字符串    │
└────────────┴──────────────────────┴──────────────────────────┘
```

### JSON 格式规则

```json
{
  "valid_string": "必须双引号",
  "number": 42,
  "float": 3.14,
  "bool_true": true,
  "bool_false": false,
  "nothing": null,
  "array": [1, 2, 3],
  "nested": {"inner": "value"}
}
```

### JSON 键的规则

JSON 规范（RFC 8259）强制要求：**键必须是双引号包裹的字符串**，没有例外。

```
┌─────────────────────────────────────────────────────────────────┐
│                    JSON 键的合法与非法写法                        │
├───────────────────────────────┬─────────────────────────────────┤
│  写法                          │  结果                           │
├───────────────────────────────┼─────────────────────────────────┤
│  {"name": "张三"}              │  ✅ 合法                        │
│  {'name': '张三'}              │  ❌ 单引号，非法                 │
│  {name: "张三"}                │  ❌ 无引号，非法                 │
│  {1: "one"}                   │  ❌ 数字键，非法                 │
│  {true: "yes"}                │  ❌ 布尔键，非法                 │
└───────────────────────────────┴─────────────────────────────────┘
```

Python dict 键可以是任意可哈希类型，而 JSON 只认字符串键。这也是 `json.dumps` 遇到非字符串键会报 `TypeError` 的原因——加 `skipkeys=True` 可跳过这些键而不报错：

```python
import json

# ❌ 数字键 → TypeError
# json.dumps({1: "one"})

# ✅ skipkeys=True：跳过非字符串键
print(json.dumps({1: "one", "two": 2}, skipkeys=True))
# {"two": 2}   — 数字键 1 被静默丢弃
```

**四个最常见的格式错误：**

```
❌  {'name': '张三'}          键和值用了单引号（Python 语法，不是 JSON）
❌  {name: "张三"}            键没有引号
❌  {"name": "张三",}         末尾多了逗号（trailing comma）
❌  {"name": "张三" // 注释}  JSON 不支持注释
```

---

## 第一部分：四个核心函数与参数

### 1.1 概念动机

`json` 模块只有四个核心函数，两对镜像关系：

```
┌──────────────────────────────────────────────────────────────┐
│                   四个核心函数关系                            │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│   字符串操作：                                               │
│     Python 对象  →  JSON 字符串    json.dumps()              │
│     JSON 字符串  →  Python 对象    json.loads()              │
│                                                              │
│   文件操作：                                                 │
│     Python 对象  →  JSON 文件      json.dump()               │
│     JSON 文件    →  Python 对象    json.load()               │
│                                                              │
│   记忆口诀：带 s 的操作字符串（s = string）                   │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

### 1.2 最简示例

```python
import json

data = {"name": "张三", "age": 25}

# 序列化：Python → JSON 字符串
s = json.dumps(data)            # '{"name": "\\u5f20\\u4e09", "age": 25}'

# 反序列化：JSON 字符串 → Python
d = json.loads(s)               # {'name': '张三', 'age': 25}

# 写文件
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f)

# 读文件
with open("data.json", encoding="utf-8") as f:
    d = json.load(f)
```

### 1.3 详细讲解：dumps 参数全表

`json.dumps(obj, *, skipkeys=False, ensure_ascii=True, check_circular=True, allow_nan=True, cls=None, indent=None, separators=None, default=None, sort_keys=False)`

| 参数 | 类型 | 默认值 | 含义 |
|------|------|--------|------|
| `obj` | any | — | 要序列化的 Python 对象（必填） |
| `ensure_ascii` | bool | `True` | `True`：非 ASCII 字符转义为 `\uXXXX`；`False`：保留原字符（中文直接输出） |
| `indent` | int\|str\|None | `None` | `None`：紧凑单行；整数 N：缩进 N 个空格；字符串：用该字符串缩进 |
| `sort_keys` | bool | `False` | `True`：所有 object 的键按字母顺序排序，便于比较和版本控制 |
| `separators` | tuple\|None | `None` | `(item_sep, key_sep)`；紧凑格式用 `(',', ':')` 去掉空格 |
| `default` | callable\|None | `None` | 遇到无法序列化的类型时调用此函数，应返回可序列化的值或抛 `TypeError` |
| `cls` | type\|None | `None` | 自定义 `JSONEncoder` 子类，比 `default` 更灵活 |
| `skipkeys` | bool | `False` | `True`：跳过非字符串的键；`False`：遇到非字符串键抛 `TypeError` |
| `allow_nan` | bool | `True` | `True`：允许 `float('nan')`、`float('inf')`（非标准 JSON）；`False`：遇到则抛 `ValueError` |
| `check_circular` | bool | `True` | `True`：检查循环引用，发现则抛 `ValueError`；`False`：跳过检查（略微提速） |

```python
import json
from typing import Any

data: dict[str, Any] = {"city": "北京", "name": "张三", "scores": [95, 87]}

# ensure_ascii=False：中文直接输出，不转义
print(json.dumps(data, ensure_ascii=False))
# {"city": "北京", "name": "张三", "scores": [95, 87]}

# indent=2：美化缩进
print(json.dumps(data, indent=2, ensure_ascii=False))
# {
#   "city": "北京",
#   "name": "张三",
#   "scores": [
#     95,
#     87
#   ]
# }

# sort_keys=True：键排序（city < name < scores）
print(json.dumps(data, sort_keys=True, ensure_ascii=False))
# {"city": "北京", "name": "张三", "scores": [95, 87]}

# separators=(',', ':')：去掉所有空格，最小体积，适合网络传输
print(json.dumps(data, separators=(",", ":"), ensure_ascii=False))
# {"city":"北京","name":"张三","scores":[95,87]}

# skipkeys=True：跳过非字符串键而不是报错
mixed_keys: dict[Any, Any] = {1: "one", "two": 2, (3,): "tuple_key"}
print(json.dumps(mixed_keys, skipkeys=True))
# {"two": 2}
```

### 1.4 详细讲解：loads 参数全表

`json.loads(s, *, cls=None, object_hook=None, parse_float=None, parse_int=None, parse_constant=None, object_pairs_hook=None)`

| 参数 | 类型 | 默认值 | 含义 |
|------|------|--------|------|
| `s` | str\|bytes | — | 要解析的 JSON 字符串（必填） |
| `object_hook` | callable\|None | `None` | 每次解析完一个 JSON object `{}` 后调用，传入 `dict`，返回值替换原 `dict`；常用于转换特定字段类型 |
| `parse_float` | callable\|None | `None` | 解析浮点数时调用的函数，默认 `float`；可传 `decimal.Decimal` 获得精确小数 |
| `parse_int` | callable\|None | `None` | 解析整数时调用的函数，默认 `int` |
| `object_pairs_hook` | callable\|None | `None` | 与 `object_hook` 类似，但传入有序的 `[(key, value), ...]` 列表，优先级高于 `object_hook` |
| `cls` | type\|None | `None` | 自定义 `JSONDecoder` 子类 |

```python
import json
from decimal import Decimal
from typing import Any

# object_hook：把所有 _at 结尾的字段自动转 datetime
from datetime import datetime

def parse_dates(obj: dict[str, Any]) -> dict[str, Any]:
    for key, val in obj.items():
        if key.endswith("_at") and isinstance(val, str):
            try:
                obj[key] = datetime.fromisoformat(val)
            except ValueError:
                pass
    return obj

data = json.loads(
    '{"name": "张三", "created_at": "2024-01-15T10:00:00"}',
    object_hook=parse_dates,
)
print(type(data["created_at"]))  # <class 'datetime.datetime'>

# parse_float：用 Decimal 替代 float，避免浮点精度问题
price_data = json.loads('{"price": 9.99}', parse_float=Decimal)
print(type(price_data["price"]))  # <class 'decimal.Decimal'>
print(price_data["price"])        # 9.99（精确值，不是 9.990000000000001）
```

### 1.5 实际应用：dump / load 文件操作

`json.dump()` 和 `json.load()` 接受的参数与 `dumps`/`loads` 完全相同，只是第二个参数换成了文件对象：

```python
# json.dump(obj, fp, **同 dumps 的所有参数)
# json.load(fp,    **同 loads 的所有参数)
```

```python
import json
from pathlib import Path
from typing import Any

config: dict[str, Any] = {
    "app": "MyShop",
    "debug": True,
    "database": {"host": "localhost", "port": 5432},
}

config_path = Path("config.json")

# 写文件：indent + ensure_ascii=False 让文件人类可读
with config_path.open("w", encoding="utf-8") as f:
    json.dump(config, f, indent=2, ensure_ascii=False)

# 读文件
with config_path.open(encoding="utf-8") as f:
    loaded: dict[str, Any] = json.load(f)

print(loaded["app"])   # MyShop
```

**关键代码说明：**

| 代码 | 含义 | 为什么这样写 |
|------|------|-------------|
| `ensure_ascii=False` | 非 ASCII 字符直接写入，不转义 | 中文变成 `\u5f20\u4e09` 可读性差；写文件时关闭转义，文件内容人类友好 |
| `indent=2` | 每层缩进 2 个空格 | 无缩进时整个 JSON 挤在一行，读写配置文件时需要可读格式 |
| `separators=(",", ":")` | 去掉分隔符后的空格 | 网络传输时最小化体积，减少流量；不需要人读时使用 |
| `parse_float=Decimal` | 用 `Decimal` 解析浮点数 | 金融金额等场景下 `float` 精度不足，`9.99` 存成 `9.990000000000001` |

---

## 第二部分：Python ↔ JSON 类型映射

### 2.1 概念动机

序列化时 Python 类型会按固定规则转换为 JSON 类型，反序列化时则按另一套规则转回。理解这两张映射表，能避免"存进去的是 tuple，读出来变成 list"这类困惑。

### 2.2 最简示例

```python
import json

# 存一个 tuple
data = {"pair": (1, 2)}
s = json.dumps(data)
print(s)                          # {"pair": [1, 2]}  — tuple 变成了 array

restored = json.loads(s)
print(type(restored["pair"]))     # <class 'list'>  — array 还原为 list，不是 tuple
```

### 2.3 详细讲解：两张映射表

**Python → JSON（序列化）：**

| Python 类型 | JSON 类型 | 备注 |
|------------|----------|------|
| `dict` | object `{}` | 键必须是字符串；非字符串键需 `skipkeys=True` 跳过或报错 |
| `list` | array `[]` | 元素类型可混合 |
| `tuple` | array `[]` | **tuple 转为 array，反序列化后变 list** |
| `str` | string `""` | — |
| `int` | number | — |
| `float` | number | `nan`/`inf` 非标准 JSON，默认允许但可用 `allow_nan=False` 禁止 |
| `True` | `true` | 注意大小写变化 |
| `False` | `false` | — |
| `None` | `null` | — |
| `set`、`datetime`、自定义类 | ❌ 报 `TypeError` | 需用 `default` 或 `cls` 自定义处理 |

**JSON → Python（反序列化）：**

| JSON 类型 | Python 类型 | 备注 |
|----------|------------|------|
| object `{}` | `dict` | 可用 `object_hook` 替换为自定义类型 |
| array `[]` | `list` | — |
| string `""` | `str` | — |
| number（整数） | `int` | — |
| number（小数） | `float` | 可用 `parse_float=Decimal` 替换 |
| `true` | `True` | — |
| `false` | `False` | — |
| `null` | `None` | — |

### 2.4 渐进复杂化

```python
import json

# 验证各类型转换
original = {
    "string": "hello",
    "integer": 42,
    "float_num": 3.14,
    "bool_t": True,
    "bool_f": False,
    "nothing": None,
    "array": [1, "two", True],
    "nested": {"inner": 99},
    "tuple_val": (10, 20),       # 注意：tuple → array
}

s = json.dumps(original, ensure_ascii=False)
restored = json.loads(s)

print(type(restored["tuple_val"]))   # <class 'list'>  ← tuple 变了
print(restored["bool_t"])            # True
print(restored["nothing"])           # None
```

---

## 第三部分：自定义编解码

### 3.1 概念动机

`datetime`、`set`、`Path`、自定义类等 Python 类型不在 JSON 规范里，直接 `dumps` 会报 `TypeError`，需要告诉 json 模块"遇到这种类型，转成什么 JSON 值"。

### 3.2 最简示例

```python
import json
from datetime import datetime

data = {"name": "张三", "created_at": datetime(2024, 1, 15, 10, 0)}

# ❌ 直接序列化报错
# json.dumps(data)  # TypeError: Object of type datetime is not JSON serializable

# ✅ 用 default 参数
def to_json(obj: object) -> str:
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"{type(obj)} 不可序列化")

print(json.dumps(data, default=to_json, ensure_ascii=False))
# {"name": "张三", "created_at": "2024-01-15T10:00:00"}
```

### 3.3 详细讲解：default 函数 vs JSONEncoder 子类

**方式 1：`default` 参数（简洁，适合少数类型）**

```python
import json
from datetime import datetime
from pathlib import Path
from typing import Any


def custom_default(obj: Any) -> Any:
    if isinstance(obj, datetime):
        return obj.isoformat()
    if isinstance(obj, Path):
        return str(obj)
    if isinstance(obj, set):
        return sorted(obj)   # set → 排序后的 list，保证输出稳定
    raise TypeError(f"{type(obj).__name__} 不可序列化")


data: dict[str, Any] = {
    "time": datetime(2024, 1, 15, 10, 0),
    "path": Path("/tmp/data"),
    "tags": {"python", "web"},
}
print(json.dumps(data, default=custom_default, ensure_ascii=False))
# {"time": "2024-01-15T10:00:00", "path": "/tmp/data", "tags": ["python", "web"]}
```

**方式 2：`JSONEncoder` 子类（结构清晰，适合多类型或复用）**

```python
import json
from datetime import datetime
from typing import Any


class AppEncoder(json.JSONEncoder):
    """应用级通用编码器"""

    def default(self, obj: Any) -> Any:
        if isinstance(obj, datetime):
            return {"__type__": "datetime", "value": obj.isoformat()}
        if isinstance(obj, set):
            return sorted(obj)
        return super().default(obj)  # 其他不认识的类型，交给父类抛 TypeError


data: dict[str, Any] = {
    "time": datetime(2024, 1, 15),
    "tags": {"python", "web"},
}
print(json.dumps(data, cls=AppEncoder, indent=2))
# {
#   "time": {"__type__": "datetime", "value": "2024-01-15T00:00:00"},
#   "tags": ["python", "web"]
# }
```

### 3.4 渐进复杂化：object_hook 自定义解码

`object_hook` 在每个 `{}` 解析完后被调用，可在反序列化时把特定结构还原为 Python 对象：

```python
import json
from datetime import datetime
from typing import Any


def decode_hook(obj: dict[str, Any]) -> Any:
    """把 {"__type__": "datetime", "value": "..."} 还原为 datetime"""
    if obj.get("__type__") == "datetime":
        return datetime.fromisoformat(obj["value"])
    return obj


json_str = '{"time": {"__type__": "datetime", "value": "2024-01-15T00:00:00"}, "name": "张三"}'
data = json.loads(json_str, object_hook=decode_hook)

print(data["time"])           # 2024-01-15 00:00:00
print(type(data["time"]))     # <class 'datetime.datetime'>
```

**关键代码说明：**

| 代码 | 含义 | 为什么这样写 |
|------|------|-------------|
| `raise TypeError(...)` 在 `default` 末尾 | 让未处理的类型抛出有意义的错误 | 不能静默忽略，否则调用方不知道数据丢失 |
| `super().default(obj)` 在 `JSONEncoder.default` 末尾 | 把不认识的类型交给父类处理 | 父类会抛 `TypeError`，保证未处理类型有明确报错 |
| `{"__type__": "datetime", "value": "..."}` | 在 JSON 中嵌入类型标记 | 纯文本无法区分 `"2024-01-15"` 是日期还是普通字符串，加标记让反序列化时能识别 |
| `sorted(obj)` 序列化 set | 固定输出顺序 | set 本身无序，每次输出顺序不同；排序后输出稳定，便于比较和测试 |

---

## 第四部分：实际应用

### 4.1 概念动机

JSON 在实际项目中最常见的两个用途：**配置文件**（读写 JSON 文件）和 **轻量级数据持久化**（用 JSON 文件替代数据库）。

### 4.2 最简示例：配置文件读写

```python
import json
from pathlib import Path

config = {"debug": True, "port": 8080}
path = Path("config.json")

path.write_text(json.dumps(config, indent=2), encoding="utf-8")
loaded = json.loads(path.read_text(encoding="utf-8"))
print(loaded["port"])  # 8080
```

### 4.3 详细讲解：配置管理器

```python
# config_manager.py
import json
from pathlib import Path
from typing import Any


class ConfigManager:
    """JSON 配置文件管理器"""

    def __init__(self, path: str | Path, defaults: dict[str, Any] | None = None) -> None:
        self.path = Path(path)
        self._data: dict[str, Any] = defaults.copy() if defaults else {}
        if self.path.exists():
            self._data.update(json.loads(self.path.read_text(encoding="utf-8")))

    def get(self, key: str, default: Any = None) -> Any:
        return self._data.get(key, default)

    def set(self, key: str, value: Any) -> None:
        self._data[key] = value
        self._save()

    def _save(self) -> None:
        self.path.write_text(
            json.dumps(self._data, indent=2, ensure_ascii=False, sort_keys=True),
            encoding="utf-8",
        )


# 使用
cfg = ConfigManager("app_config.json", defaults={"debug": False, "port": 8080})
cfg.set("debug", True)
print(cfg.get("port"))   # 8080
```

### 4.4 渐进复杂化：轻量级键值数据库

```python
# json_db.py
import json
from pathlib import Path
from typing import Any


class JsonDB:
    """JSON 文件键值存储"""

    def __init__(self, filepath: str | Path) -> None:
        self.filepath = Path(filepath)
        self._data: dict[str, Any] = self._load()

    def _load(self) -> dict[str, Any]:
        if self.filepath.exists():
            return json.loads(self.filepath.read_text(encoding="utf-8"))
        return {}

    def _save(self) -> None:
        self.filepath.write_text(
            json.dumps(self._data, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

    def get(self, key: str, default: Any = None) -> Any:
        return self._data.get(key, default)

    def set(self, key: str, value: Any) -> None:
        self._data[key] = value
        self._save()

    def delete(self, key: str) -> None:
        if key in self._data:
            del self._data[key]
            self._save()

    def all(self) -> dict[str, Any]:
        return dict(self._data)


# 使用
db = JsonDB("store.json")
db.set("user:1", {"name": "张三", "age": 25})
db.set("user:2", {"name": "李四", "age": 30})
print(db.get("user:1"))          # {'name': '张三', 'age': 25}
print(db.get("user:99", "N/A"))  # N/A
db.delete("user:2")
```

**关键代码说明：**

| 代码 | 含义 | 为什么这样写 |
|------|------|-------------|
| `self.filepath.read_text(encoding="utf-8")` | 用 pathlib 读文件 | 自动处理打开/关闭，比 `open/read/close` 更简洁，不会忘记关闭 |
| `if self.filepath.exists()` | 文件不存在时返回空字典 | 首次创建数据库时文件还不存在，应初始化为空而非报错 |
| `json.dumps(..., sort_keys=True)` | 保存时键排序 | 键顺序固定，git diff 时看不到无意义的键序变化 |
| `_save()` 在 `set`/`delete` 末尾调用 | 写穿策略 | 每次修改立即落盘，内存和文件始终一致；简单场景不需要显式事务 |

---

### L2 实践层：用好

```
┌──────────────────────────────────────────────────────────────┐
│                   json 模块使用指南                           │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│   序列化：                                                   │
│   ✓ 中文内容必加 ensure_ascii=False                          │
│   ✓ 写文件用 indent=2，便于人工查看                           │
│   ✓ 网络传输用 separators=(',',':')，减小体积                │
│                                                              │
│   反序列化：                                                 │
│   ✓ 外部数据一定要 try/except JSONDecodeError                │
│   ✓ 金融金额用 parse_float=Decimal                           │
│   ✓ 需要自动转类型用 object_hook                             │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

#### 推荐做法

| 做法 | 原因 | 示例 |
|------|------|------|
| `ensure_ascii=False` | 中文直接输出，可读性强 | `json.dumps(data, ensure_ascii=False)` |
| 写配置文件加 `indent=2` | 人类可读，版本控制友好 | `json.dump(cfg, f, indent=2)` |
| 网络传输加 `separators=(',',':')` | 去掉空格，减小传输体积 | `json.dumps(data, separators=(',',':'))` |
| 外部 JSON 用 `try/except JSONDecodeError` | 外部数据格式不可信 | 见反模式对比 |
| 金融金额用 `parse_float=Decimal` | 避免浮点精度问题 | `json.loads(s, parse_float=Decimal)` |
| 保存时 `sort_keys=True` | git diff 稳定，键序不乱跳 | `json.dumps(data, sort_keys=True)` |

#### 反模式：不要这样做

```python
# ❌ 不加 ensure_ascii=False 存中文
s = json.dumps({"name": "张三"})
# '{"name": "\\u5f20\\u4e09"}'  — 不可读

# ❌ 不捕获异常直接解析外部 JSON
data = json.loads(user_input)  # 用户输入格式错误直接崩溃

# ❌ 用 str() 代替 json.dumps()
result = str({"name": "张三", "vip": True})
# "{'name': '张三', 'vip': True}"  — 单引号，前端无法解析

# ❌ 序列化 datetime 前不转换
import json
from datetime import datetime
json.dumps({"time": datetime.now()})  # TypeError

# ❌ 用 json 存储二进制（图片、音频等）
# json 只处理文本，二进制需先 base64 编码
```

```python
# ✅ 正确做法对比
import json
from datetime import datetime

# 中文正确处理
s = json.dumps({"name": "张三"}, ensure_ascii=False)

# 安全解析外部 JSON
try:
    data = json.loads(user_input)
except json.JSONDecodeError as e:
    print(f"格式错误：{e}")
    data = {}

# datetime 正确序列化
json.dumps({"time": datetime.now()}, default=lambda o: o.isoformat())
```

#### 常见陷阱

| 陷阱 | 现象 | 解决方案 |
|------|------|---------|
| 中文变成 `\uXXXX` | `"name": "\u5f20\u4e09"` | 加 `ensure_ascii=False` |
| tuple 序列化后变 list | `(1,2)` → `[1,2]`，读回来是 list | JSON 无 tuple 类型，这是预期行为；需要 tuple 时读取后手动转 |
| datetime 不可序列化 | `TypeError: Object of type datetime is not JSON serializable` | 用 `default` 参数或 `JSONEncoder` 子类 |
| 浮点精度丢失 | `9.99` 变成 `9.990000000000001` | 金融场景用 `parse_float=Decimal` |
| 键排序每次不同 | 同内容 JSON 字符串不等，diff 有噪声 | 加 `sort_keys=True` |
| 解析用户输入不捕获异常 | 格式错误时程序崩溃 | `try/except json.JSONDecodeError` |

#### 适用场景

| 场景 | 是否推荐 | 说明 |
|------|---------|------|
| Web API 请求/响应体 | ✅ 推荐 | JSON 是 REST API 的标准格式 |
| 配置文件（人工编辑） | ✅ 推荐 | 用 `indent=2`，可读性好 |
| 轻量级本地数据存储 | ✅ 推荐 | 适合数据量小、无并发的场景 |
| 大量结构化数据 | ⚠️ 慎用 | 考虑 SQLite 或数据库 |
| 二进制数据（图片等） | ❌ 不适合 | 需先 base64 编码，体积膨胀 |
| 需要注释的配置文件 | ❌ 不适合 | JSON 不支持注释，改用 TOML |

---

### L3 专家层：深入

#### Python 如何实现

`json` 模块的核心编解码由 C 扩展 `_json` 实现（`Modules/_json.c`，约 2000 行）。纯 Python 的 `json/encoder.py` 和 `json/decoder.py` 作为 fallback 存在：

```
┌──────────────────────────────────────────────────────────────┐
│          json 模块 C 实现架构                                 │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│   json/__init__.py                                           │
│   ├── JSONEncoder (Python类，继承 _json.Encoder)             │
│   │   └── default() → Python 回调（不可序列化类型）            │
│   │   └── encode()   → C 扩展 _json.encode_basestring_ascii  │
│   │                                                    等    │
│   ├── JSONDecoder (Python类，继承 _json.Decoder)             │
│   │   └── object_hook  → Python 回调（解析 {} 后）            │
│   │   └── parse_float  → Python 回调（解析数字后）            │
│   │                                                          │
│   _json C 扩展（Modules/_json.c）：                           │
│   · 手写递归下降 JSON 解析器（非基于正则/状态机库）           │
│   · 直接操作 PyUnicode 对象，避免中间字符串分配                │
│   · 使用 Py_ssize_t 处理大整数溢出                            │
│   · scanstring() 处理转义和 Unicode 编码                      │
│   · 浮点数解析：调用 PyOS_string_to_double（最终到 strtod）   │
│                                                              │
│   性能关键路径：                                              │
│   · 字符串扫描：C 层逐字符扫描，零 Python 对象开销            │
│   · 数字解析：strtod() 直接 C 调用                            │
│   · object_hook 调用：每个 {} 解析后回调 Python 函数          │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

```python
# 验证：json 编码器是 C 扩展
import json

# C 编码器
c_encoder = json._default_encoder  # 内部使用 C 编码器
print(type(c_encoder))  # <class '_json.Encoder'>

# Python 编码器（用于不支持的类型时）
encoder = json.JSONEncoder()
print(type(encoder))  # <class 'json.encoder.JSONEncoder'>

# 验证编码器的 C 加速
import timeit

data = {"key" + str(i): "value" + str(i) for i in range(1000)}

# C 编码器（默认）
t1 = timeit.timeit(lambda: json.dumps(data), number=1000)
# 强制使用 Python 编码器（通过子类覆盖 speedups=False）
class PyEncoder(json.JSONEncoder):
    pass
# 注意：JSONEncoder 默认也会用 C 加速；要纯 Python 需 import json.encoder
# 这里用纯 Python 的 scanstring 对比
print(f"C 编码器:    {t1:.4f}s / 1000 calls")

# 验证：object_hook 回调的性能开销
import json

def slow_hook(d):
    """每个 {} 都会调用此函数"""
    # 模拟检查所有字段
    for k, v in d.items():
        if isinstance(v, dict):
            pass  # 嵌套检查
    return d

large_json = json.dumps({"data": [{"id": i, "name": f"item_{i}"} for i in range(1000)]})

# 不带 hook
t_no_hook = timeit.timeit(lambda: json.loads(large_json), number=100)
# 带 hook（每个对象都被遍历）
t_with_hook = timeit.timeit(lambda: json.loads(large_json, object_hook=slow_hook), number=100)
print(f"无 hook:      {t_no_hook:.4f}s / 100 calls")
print(f"有 hook:      {t_with_hook:.4f}s / 100 calls")
# object_hook 对所有嵌套字典都触发，数量多时开销显著
```

```python
# 验证：bytearray 和 memoryview 的 JSON 处理
import json

# JSON 标准要求输入为字符串，但 json.loads 也接受 bytes/bytearray
data_bytes = b'{"key": "value"}'
result = json.loads(data_bytes)
print(result)  # {'key': 'value'}

# CPython 内部：_json.c 中 scanstring 函数
# 处理 \uXXXX Unicode 转义 → 直接写入 PyUnicode 对象
# 处理 \n \t \r \b \f 等转义 → switch-case 快速跳转

import dis
# json.dumps 是 built-in_function_or_method（C 实现）
print(dis.dis(json.dumps))
# 只显示一行：C 函数，没有 Python 字节码
```

#### 性能考量

| 操作 | 复杂度 | 说明 |
|------|--------|------|
| `json.dumps(dict)` | O(n) | n=JSON 输出长度，C 编码器线性扫描 |
| `json.loads(str)` | O(n) | n=输入长度，递归下降解析 |
| `json.dumps` + `ensure_ascii=True` | O(n) | 额外 Unicode 转义，约慢 10-20% |
| `json.dumps` + `indent=2` | O(n) | 额外空格分配，约慢 5-10% |
| `json.loads` + `object_hook` | O(n + m*k) | m={} 数量，k=hook 复杂度 |
| `json.loads` + `parse_float=Decimal` | O(n) | Decimal 构造比 float 慢 10x |

```python
# 验证：ensure_ascii 性能差异
import json, timeit

cn_data = {"城市": "北京", "地区": "朝阳区"}

t_ascii = timeit.timeit(lambda: json.dumps(cn_data, ensure_ascii=True), number=100000)
t_no_ascii = timeit.timeit(lambda: json.dumps(cn_data, ensure_ascii=False), number=100000)
print(f"ensure_ascii=True:  {t_ascii:.4f}s / 100K")
print(f"ensure_ascii=False: {t_no_ascii:.4f}s / 100K")
# ensure_ascii=False 略快（省去 Unicode 转义步骤）
```

#### 知识关联

```
┌──────────────────────────────────────────────────────────────┐
│          json 模块知识关联图                                  │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│   ┌──────────┐     ┌──────────┐     ┌───────────┐          │
│   │   json   │────→│  _json   │────→│ C 编码器  │          │
│   │  模块    │     │  C 扩展  │     │ strtod()  │          │
│   └──────────┘     └──────────┘     └───────────┘          │
│        │                                                      │
│        ↓                                                      │
│   ┌──────────┐     ┌──────────┐     ┌───────────┐          │
│   │  orjson  │     │  Rust    │     │ 3-5x 提速 │          │
│   │  ujson   │────→│  实现    │────→│ 第三方    │          │
│   │  rapidjson│    │          │     │ 高性能库  │          │
│   └──────────┘     └──────────┘     └───────────┘          │
│                                                              │
│   ┌──────────┐     ┌──────────┐     ┌───────────┐          │
│   │  pickle  │     │  二进制  │     │ Python    │          │
│   │          │────→│  专有    │────→│ 内部传递  │          │
│   └──────────┘     └──────────┘     └───────────┘          │
│                                                              │
│   ┌──────────┐     ┌──────────┐     ┌───────────┐          │
│   │ decimal  │     │  精确    │     │ 金融金额  │          │
│   │  模块    │────→│  十进制  │────→│ 无精度损失│          │
│   └──────────┘     └──────────┘     └───────────┘          │
│                                                              │
│   选择决策：                                                  │
│   Web API  → json（标准模块，功能完整）                        │
│   高性能   → orjson（Rust 实现，3-5x 更快）                   │
│   金融精度 → json.loads(s, parse_float=Decimal)              │
│   Python 内部 → pickle                                       │
│                                                              │
│   object_hook 使用注意：                                      │
│   · 对 JSON 中每个 {} 都会调用（包括嵌套），数量级可能很大     │
│   · 配合 object_pairs_hook 可保持插入顺序                     │
│   · 大量数据时考虑先 load 再后处理，而非 hook 逐个回调        │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

---

## 本章小结

```
┌──────────────────────────────────────────────────────────────┐
│                   json 模块 知识要点                          │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│   JSON 格式：六种类型（string/number/boolean/null/array/object）│
│   规则：键必须双引号、无尾逗号、无注释                        │
│                                                              │
│   四个核心函数：                                             │
│   dumps(obj)   Python → 字符串    loads(s)  字符串 → Python  │
│   dump(obj,fp) Python → 文件      load(fp)  文件  → Python   │
│                                                              │
│   重要参数：                                                 │
│   ensure_ascii=False   中文直接输出                          │
│   indent=2             美化缩进                              │
│   separators=(',',':') 紧凑格式                              │
│   sort_keys=True       键排序                                │
│   default=func         自定义序列化                          │
│   object_hook=func     自定义反序列化                        │
│   parse_float=Decimal  精确浮点数                            │
│                                                              │
│   L3 要点: C 扩展 _json → 递归下降解析器 → object_hook 桥接  │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```
