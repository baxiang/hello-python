# json 模块参考

Python json 模块提供 JSON 数据的编码和解码功能。

---

## 基本操作

### 编码（Python → JSON）

```python
import json

# 字典转 JSON 字符串
data = {'name': '张三', 'age': 25, 'city': '北京'}
json_str = json.dumps(data)
print(json_str)  # {"name": "\u5f20\u4e09", "age": 25, "city": "\u5317\u4eac"}

# 格式化输出
json_str = json.dumps(data, indent=2, ensure_ascii=False)
print(json_str)
# {
#   "name": "张三",
#   "age": 25,
#   "city": "北京"
# }

# 写入文件
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
```

### 解码（JSON → Python）

```python
import json

# JSON 字符串转字典
json_str = '{"name": "张三", "age": 25}'
data = json.loads(json_str)
print(data)  # {'name': '张三', 'age': 25}
print(data['name'])  # 张三

# 从文件读取
with open('data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
print(data)
```

---

## 类型映射

### Python → JSON

| Python 类型 | JSON 类型 |
|-------------|-----------|
| dict | object |
| list, tuple | array |
| str | string |
| int, float | number |
| True | true |
| False | false |
| None | null |

### JSON → Python

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

---

## dumps 参数

### 常用参数

```python
import json

data = {'name': '张三', 'scores': [95, 87, 92]}

# indent - 缩进
json_str = json.dumps(data, indent=2)

# ensure_ascii - 非 ASCII 字符
json_str = json.dumps(data, ensure_ascii=False)  # 保留中文

# sort_keys - 键排序
json_str = json.dumps(data, sort_keys=True)

# separators - 分隔符（压缩输出）
json_str = json.dumps(data, separators=(',', ':'))

# skipkeys - 跳过非字符串键
data = {1: 'one', 'two': 2}
json_str = json.dumps(data, skipkeys=True)  # {"two": 2}
```

---

## 自定义编码

### default 参数

```python
import json
from datetime import datetime

data = {
    'name': '张三',
    'created_at': datetime.now()
}

# 默认无法序列化 datetime
# json.dumps(data)  # TypeError

# 自定义编码函数
def json_serializer(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")

json_str = json.dumps(data, default=json_serializer)
print(json_str)  # {"name": "张三", "created_at": "2024-03-15T14:30:45"}
```

### JSONEncoder 子类

```python
import json
from datetime import datetime

class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, set):
            return list(obj)
        return super().default(obj)

data = {
    'time': datetime.now(),
    'tags': {'python', 'json', 'web'}
}

json_str = json.dumps(data, cls=CustomEncoder)
print(json_str)
```

---

## 自定义解码

### object_hook

```python
import json
from datetime import datetime

json_str = '{"name": "张三", "created_at": "2024-03-15T14:30:00"}'

def json_decoder(obj):
    for key, value in obj.items():
        if key.endswith('_at') and isinstance(value, str):
            try:
                obj[key] = datetime.fromisoformat(value)
            except ValueError:
                pass
    return obj

data = json.loads(json_str, object_hook=json_decoder)
print(data['created_at'])  # 2024-03-15 14:30:00
print(type(data['created_at']))  # <class 'datetime.datetime'>
```

---

## 常用示例

### 配置文件

```python
import json
from pathlib import Path

def load_config(config_file):
    """加载配置文件"""
    with open(config_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_config(config_file, config):
    """保存配置文件"""
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

# 使用
config = {
    'database': {
        'host': 'localhost',
        'port': 5432,
        'name': 'myapp'
    },
    'debug': True
}

save_config('config.json', config)
loaded = load_config('config.json')
print(loaded['database']['host'])  # localhost
```

### API 响应

```python
import json

def api_response(data, status='success'):
    """生成 API 响应"""
    return json.dumps({
        'status': status,
        'data': data,
        'timestamp': datetime.now().isoformat()
    }, ensure_ascii=False)

response = api_response({'user': '张三', 'score': 95})
print(response)
```

### 数据持久化

```python
import json
from pathlib import Path

class JsonDB:
    """简单的 JSON 数据库"""
    
    def __init__(self, filepath):
        self.filepath = Path(filepath)
        self.data = self._load()
    
    def _load(self):
        if self.filepath.exists():
            return json.loads(self.filepath.read_text())
        return {}
    
    def _save(self):
        self.filepath.write_text(json.dumps(self.data, indent=2, ensure_ascii=False))
    
    def get(self, key, default=None):
        return self.data.get(key, default)
    
    def set(self, key, value):
        self.data[key] = value
        self._save()
    
    def delete(self, key):
        if key in self.data:
            del self.data[key]
            self._save()

# 使用
db = JsonDB('data.json')
db.set('user', {'name': '张三', 'age': 25})
print(db.get('user'))
```

---

## 异常处理

```python
import json

def safe_loads(json_str):
    """安全解析 JSON"""
    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        print(f"JSON 解析错误: {e}")
        return None

# 测试
data = safe_loads('{"name": "张三"}')  # 正常
data = safe_loads('{"name": 张三}')    # 错误，缺少引号
```

**常见异常：**

| 异常 | 说明 |
|------|------|
| `json.JSONDecodeError` | JSON 解析错误 |
| `TypeError` | 不支持的类型 |
| `ValueError` | 无效值 |