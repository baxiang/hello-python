# json 模块参考（详细版）

> Python 3.11+

JSON（JavaScript Object Notation）是一种轻量级数据交换格式，Python 的 json 模块提供 JSON 数据的编码和解码功能。

---

## 第一部分：JSON 基础操作

### 5.1 编码（Python → JSON）

#### 实际场景

在 Web API 开发中，后端需要将 Python 对象转换为 JSON 格式返回给前端；在配置文件存储时，需要将字典数据序列化为 JSON 文件。

**问题：如何将 Python 字典、列表转换为 JSON 字符串？如何控制格式化输出？**

```python
import json
from typing import Any

data: dict[str, Any] = {'name': '张三', 'age': 25, 'city': '北京'}

json_str: str = json.dumps(data)
print(json_str)  # {"name": "\u5f20\u4e09", "age": 25, "city": "\u5317\u4eac"}

json_str_formatted: str = json.dumps(data, indent=2, ensure_ascii=False)
print(json_str_formatted)
# {
#   "name": "张三",
#   "age": 25,
#   "city": "北京"
# }

with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
```

### 5.2 解码（JSON → Python）

#### 实际场景

从前端接收 JSON 数据时，需要将 JSON 字符串解析为 Python 对象；读取配置文件时，需要将 JSON 文件反序列化为字典。

**问题：如何将 JSON 字符串转换为 Python 字典？如何处理 Unicode 编码问题？**

```python
import json

json_str: str = '{"name": "张三", "age": 25}'
data: dict[str, Any] = json.loads(json_str)
print(data)  # {'name': '张三', 'age': 25}
print(data['name'])  # 张三

with open('data.json', 'r', encoding='utf-8') as f:
    data: dict[str, Any] = json.load(f)
print(data)
```

---

## 第二部分：类型映射与参数

### 5.3 类型映射

#### 实际场景

理解 JSON 与 Python 类型之间的映射关系，有助于正确处理数据序列化和反序列化，避免类型转换错误。

**问题：Python 的 None 在 JSON 中如何表示？JSON 的数组会转换成什么 Python 类型？**

**Python → JSON 类型映射：**

| Python 类型 | JSON 类型 |
|-------------|-----------|
| dict | object |
| list, tuple | array |
| str | string |
| int, float | number |
| True | true |
| False | false |
| None | null |

**JSON → Python 类型映射：**

| JSON 类型 | Python 类型 |
|-----------|-------------|
| object | dict |
| array | list |
| string | str |
| number (int) | int |
| number (real) | float |
| true | True |
| false | False |
| null | None |

### 5.4 dumps 常用参数

#### 实际场景

在实际项目中，需要控制 JSON 输出格式：压缩传输、美化显示、排序键值等。

**问题：如何生成紧凑的 JSON 用于网络传输？如何让 JSON 保留中文字符而不是 Unicode 转义？**

```python
import json
from typing import Any

data: dict[str, Any] = {'name': '张三', 'scores': [95, 87, 92]}

json_indented: str = json.dumps(data, indent=2)
json_unicode: str = json.dumps(data, ensure_ascii=False)
json_sorted: str = json.dumps(data, sort_keys=True)
json_compact: str = json.dumps(data, separators=(',', ':'))

data_with_nonstr_key: dict[Any, Any] = {1: 'one', 'two': 2}
json_skipkeys: str = json.dumps(data_with_nonstr_key, skipkeys=True)
```

---

## 第三部分：自定义编解码

### 5.5 自定义编码

#### 实际场景

Python 的 datetime 对象、set 集合等类型无法直接序列化为 JSON，需要自定义编码逻辑。

**问题：如何将 datetime 对象序列化为 JSON？如何处理自定义类的序列化？**

```python
import json
from datetime import datetime
from typing import Any

data: dict[str, Any] = {
    'name': '张三',
    'created_at': datetime.now()
}

def json_serializer(obj: Any) -> str:
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")

json_str: str = json.dumps(data, default=json_serializer)
print(json_str)
```

**使用 JSONEncoder 子类：**

```python
import json
from datetime import datetime
from typing import Any, Set

class CustomEncoder(json.JSONEncoder):
    def default(self, obj: Any) -> Any:
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, set):
            return list(obj)
        return super().default(obj)

data: dict[str, Any] = {
    'time': datetime.now(),
    'tags': {'python', 'json', 'web'}
}

json_str: str = json.dumps(data, cls=CustomEncoder)
print(json_str)
```

### 5.6 自定义解码

#### 实际场景

JSON 字符串中的日期时间字段需要自动转换为 Python datetime 对象，而不是保留为字符串。

**问题：如何在解析 JSON 时自动识别并转换特定字段？**

```python
import json
from datetime import datetime
from typing import Any

json_str: str = '{"name": "张三", "created_at": "2024-03-15T14:30:00"}'

def json_decoder(obj: dict[str, Any]) -> dict[str, Any]:
    for key, value in obj.items():
        if key.endswith('_at') and isinstance(value, str):
            try:
                obj[key] = datetime.fromisoformat(value)
            except ValueError:
                pass
    return obj

data: dict[str, Any] = json.loads(json_str, object_hook=json_decoder)
print(data['created_at'])  # 2024-03-15 14:30:00
print(type(data['created_at']))  # <class 'datetime.datetime'>
```

---

## 第四部分：实际应用

### 5.7 配置文件管理

#### 实际场景

应用程序需要读取和保存配置信息，如数据库连接参数、API 密钥等。

**问题：如何设计一个简单易用的 JSON 配置管理工具？**

```python
import json
from pathlib import Path
from typing import Any

def load_config(config_file: str | Path) -> dict[str, Any]:
    with open(config_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_config(config_file: str | Path, config: dict[str, Any]) -> None:
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

config: dict[str, Any] = {
    'database': {
        'host': 'localhost',
        'port': 5432,
        'name': 'myapp'
    },
    'debug': True
}

save_config('config.json', config)
loaded: dict[str, Any] = load_config('config.json')
print(loaded['database']['host'])
```

### 5.8 API 响应生成

#### 实际场景

Web API 需要返回统一格式的 JSON 响应，包含状态码、数据和时间戳。

**问题：如何生成符合 RESTful 规范的 JSON 响应？**

```python
import json
from datetime import datetime
from typing import Any

def api_response(data: Any, status: str = 'success') -> str:
    return json.dumps({
        'status': status,
        'data': data,
        'timestamp': datetime.now().isoformat()
    }, ensure_ascii=False)

response: str = api_response({'user': '张三', 'score': 95})
print(response)
```

### 5.9 数据持久化

#### 实际场景

简单应用需要一个轻量级的本地数据库，JSON 文件是一种便捷的选择。

**问题：如何实现一个简单的键值存储数据库？**

```python
import json
from pathlib import Path
from typing import Any

class JsonDB:
    def __init__(self, filepath: str | Path) -> None:
        self.filepath: Path = Path(filepath)
        self.data: dict[str, Any] = self._load()
    
    def _load(self) -> dict[str, Any]:
        if self.filepath.exists():
            return json.loads(self.filepath.read_text())
        return {}
    
    def _save(self) -> None:
        self.filepath.write_text(
            json.dumps(self.data, indent=2, ensure_ascii=False)
        )
    
    def get(self, key: str, default: Any = None) -> Any:
        return self.data.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        self.data[key] = value
        self._save()
    
    def delete(self, key: str) -> None:
        if key in self.data:
            del self.data[key]
            self._save()

db: JsonDB = JsonDB('data.json')
db.set('user', {'name': '张三', 'age': 25})
print(db.get('user'))
```

---

## 第五部分：异常处理

### 5.10 JSON 异常处理

#### 实际场景

在解析来自网络或用户输入的 JSON 数据时，可能会遇到格式错误，需要妥善处理。

**问题：如何安全地解析 JSON 并给出友好的错误提示？**

```python
import json
from typing import Any

def safe_loads(json_str: str) -> dict[str, Any] | None:
    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        print(f"JSON 解析错误: {e}")
        return None

data: dict[str, Any] | None = safe_loads('{"name": "张三"}')
data = safe_loads('{"name": 张三}')
```

**常见异常：**

| 异常 | 说明 |
|------|------|
| `json.JSONDecodeError` | JSON 解析错误 |
| `TypeError` | 不支持的类型 |
| `ValueError` | 无效值 |