# 第 5 章 — functools 标准装饰器

> **Python 版本要求**：Python 3.11+
> **贯穿项目**：Web API 请求处理系统

## 为什么需要 functools？

Python 标准库 `functools` 模块提供了 **生产环境必备** 的装饰器和工具函数。与手写装饰器不同，这些装饰器由 CPython 核心团队维护，经过充分测试和性能优化。

本章覆盖五个最常用的 functools 工具：

| 装饰器 | 用途 | 典型场景 |
|--------|------|----------|
| `@lru_cache` / `@cache` | 缓存函数返回值 | 递归优化、配置解析、I/O 去重 |
| `@cached_property` | 惰性计算属性 | 报表统计、昂贵计算 |
| `@singledispatch` | 函数重载 | 多类型分发处理 |
| `@partial` | 偏函数应用 | 预设参数、函数式编程 |
| `@wraps` | 保留原函数元数据 | 手写装饰器必备 |

---

## @lru_cache / @cache：缓存原理

### 工作原理

```
┌─────────────────────────────────────────┐
│              lru_cache                   │
│  ┌─────────────────────────────────┐    │
│  │       OrderedDict (LRU)         │    │
│  │  ┌──────┬──────┬──────┐         │    │
│  │  │ key1 │ key2 │ key3 │  ...    │    │
│  │  │ val1 │ val2 │ val3 │         │    │
│  │  └──────┴──────┴──────┘         │    │
│  │    ↑ 最近使用       ↓ 最久未使用  │    │
│  └─────────────────────────────────┘    │
│                                          │
│  命中 → 直接返回                          │
│  未命中 → 执行函数 → 存入缓存              │
│  满员 → 淘汰最久未使用的条目               │
└─────────────────────────────────────────┘
```

### @lru_cache vs @cache

```python
import functools

# 有容量上限，满了自动淘汰
@functools.lru_cache(maxsize=128)
def fibonacci(n: int) -> int:
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

# 无限缓存（无 maxsize 限制）
@functools.cache
def parse_config(key: str) -> dict:
    return load_from_disk(key)
```

| 装饰器 | maxsize | 适用场景 |
|--------|---------|----------|
| `@lru_cache(maxsize=N)` | 有限（N 个条目） | 输入空间有限，防止内存泄漏 |
| `@cache` | 无限（等价于 maxsize=None） | 输入空间小且确定 |

### 缓存监控：cache_info()

```python
>>> fibonacci.cache_info()
CacheInfo(hits=56, misses=31, maxsize=128, currsize=31)

>>> parse_config.cache_info()
CacheInfo(hits=3, misses=5, maxsize=None, currsize=5)
```

| 字段 | 含义 |
|------|------|
| `hits` | 缓存命中次数 |
| `misses` | 缓存未命中次数 |
| `maxsize` | 最大容量（None 表示无限） |
| `currsize` | 当前缓存条目数 |

命中率 = hits / (hits + misses)，越低说明缓存效果越差。

### 斐波那契性能对比

```python
# 有缓存：O(n) 时间复杂度
fibonacci(30)  # ~0.001ms

# 无缓存：O(2^n) 时间复杂度
fibonacci_without_cache(30)  # ~230ms

# 加速比：约 230,000x
```

调用 `GET /api/v1/cache/fibonacci/30` 可以看到实际的性能对比数据。

### 缓存清理

```python
fibonacci.cache_clear()   # 清空缓存
fibonacci.cache_info()    # 查看统计
```

---

## @cached_property：惰性计算

### 与 @property 对比

```python
class DataReport:
    def __init__(self, data: list[int]) -> None:
        self.data = data

    # @property：每次访问都重新计算
    @property
    def total(self) -> int:
        return sum(self.data)  # 每次调用都执行

    # @cached_property：只计算一次，结果存到实例 __dict__
    @functools.cached_property
    def average(self) -> float:
        return sum(self.data) / len(self.data)  # 仅首次执行
```

| 特性 | `@property` | `@cached_property` |
|------|-------------|-------------------|
| 执行次数 | 每次访问都执行 | 仅首次执行 |
| 结果存储 | 不存储 | 存入 `instance.__dict__` |
| 适用场景 | 轻量计算、动态值 | 昂贵计算、不变值 |
| 线程安全 | 是 | 是（Python 3.8+） |

### 使用场景

- **报表统计**：总和、平均值、中位数等一次性计算
- **对象属性**：从数据库加载后不再变化的派生属性
- **懒加载**：首次使用时才初始化资源（文件连接、网络会话）

### 注意事项

- 需要 `self` 参数（只能用于实例方法）
- 计算后覆盖属性名，后续访问不再执行函数体
- 不支持 `__slots__` 的类（因为需要写入 `__dict__`）

---

## @singledispatch：函数重载

### 传统的 if-elif 写法（不推荐）

```python
def process_data(data):
    if isinstance(data, str):
        return f"String: {data.upper()}"
    elif isinstance(data, int):
        return f"Integer: {data * 2}"
    elif isinstance(data, list):
        return f"List: {len(data)} items"
    else:
        return f"Unknown type: {type(data).__name__}"
```

### singledispatch 写法（推荐）

```python
import functools

@functools.singledispatch
def process_data(data):
    return f"Unknown type: {type(data).__name__}"

@process_data.register
def _(data: str) -> str:
    return f"String: {data.upper()}"

@process_data.register
def _(data: int) -> str:
    return f"Integer: {data * 2}"

@process_data.register
def _(data: list) -> str:
    return f"List: {len(data)} items"

@process_data.register(dict)  # 也可以显式写类型
def _(data: dict) -> str:
    return f"Dict: {len(data)} keys"
```

### 优势

| 对比项 | if-elif | singledispatch |
|--------|---------|----------------|
| 可扩展性 | 修改原函数 | 在任意位置 `@register` |
| 可读性 | 嵌套深 | 扁平、清晰 |
| 测试 | 一个函数包含所有逻辑 | 每个分支可独立测试 |
| 维护性 | 修改一处影响全局 | 独立注册互不影响 |

### 3.11+ 的联合类型支持

```python
# Python 3.11+ 支持联合类型注册
@process_data.register
def _(data: str | bytes) -> str:
    return f"Text: {data.decode() if isinstance(data, bytes) else data}"
```

---

## @partial：偏函数应用

### 什么是偏函数？

偏函数（Partial Application）固定了原函数的部分参数，返回一个新的函数。

```python
import functools

def format_response(status: int, message: str, content_type: str = "application/json") -> dict:
    return {"status": status, "content_type": content_type, "message": message}

# 预设 status=200
ok_response = functools.partial(format_response, 200, content_type="application/json")

# 使用：只需传 message
ok_response("success")
# → {"status": 200, "content_type": "application/json", "message": "success"}
```

### 应用场景

```python
# 1. HTTP 响应预设
ok = functools.partial(format_response, 200)
created = functools.partial(format_response, 201)
not_found = functools.partial(format_response, 404)
server_error = functools.partial(format_response, 500)

# 2. 带固定前缀的日志
import logging
log_info = functools.partial(logging.info, "MyApp:")
log_info("Server started")  # → INFO:root:MyApp: Server started

# 3. 回调函数预设参数
def on_complete(task_id, result):
    print(f"Task {task_id}: {result}")

on_complete_task_42 = functools.partial(on_complete, 42)
# 后续只需传 result
on_complete_task_42("done")  # → Task 42: done
```

### partial vs lambda

```python
# lambda 方式（可读性较差，且 __name__ 为 <lambda>）
ok = lambda msg: format_response(200, msg)

# partial 方式（保留函数信息，可序列化）
ok = functools.partial(format_response, 200)
```

---

## 贯穿实战：缓存端点

本章的缓存演示通过 FastAPI 路由提供两个端点：

### GET /api/v1/cache/fibonacci/{n}

对比 `@lru_cache` 缓存版与普通版斐波那契的性能差异：

```bash
$ curl "http://localhost:8000/api/v1/cache/fibonacci/30"
{
  "n": 30,
  "result": 832040,
  "cached_time_ms": "0.0012",
  "no_cache_time_ms": "234.5678",
  "speedup": "195473x"
}
```

### GET /api/v1/cache/config/{key}

演示 `@cache` 无限缓存，首次调用慢、后续调用快：

```bash
# 首次调用（miss）
$ curl "http://localhost:8000/api/v1/cache/config/db_host"
{
  "key": "db_host",
  "value": "value_for_db_host",
  "elapsed_ms": "100.2345",
  "cache_info": {"hits": 0, "misses": 1, "maxsize": null, "currsize": 1}
}

# 再次调用（hit）
$ curl "http://localhost:8000/api/v1/cache/config/db_host"
{
  "key": "db_host",
  "value": "value_for_db_host",
  "elapsed_ms": "0.0012",
  "cache_info": {"hits": 1, "misses": 1, "maxsize": null, "currsize": 1}
}
```

代码实现见 `app/routers/cache.py`。

---

## 自检清单

- **`@lru_cache(128)` 和 `@cache` 有什么区别？什么场景用哪个？**
- **`cache_info()` 返回的 `hits` 和 `misses` 如何计算命中率？**
- **`@cached_property` 和 `@property` 的核心区别是什么？**
- **`@singledispatch` 比 if-elif 好在哪里？**
- **`partial` 和 `lambda` 固定参数有什么优劣？**

**答案：**
1. `@lru_cache(128)` 有容量上限，超限时自动淘汰最久未使用的条目；`@cache` 无限缓存。输入空间大且不确定时用 `lru_cache`，小而确定时用 `cache`。
2. 命中率 = `hits / (hits + misses)`。越接近 100% 缓存效果越好。
3. `@property` 每次访问都重新执行函数体；`@cached_property` 只执行一次，结果缓存到实例 `__dict__` 中。
4. 可扩展性（可在任意位置 `@register`）、可读性（扁平）、测试性（分支独立）。
5. `partial` 保留函数元信息（`__name__`、`__doc__`），可序列化；`lambda` 丢失元信息且不可序列化。

---

## 能力清单

完成本章后，你应该能够：

- [ ] 使用 `@lru_cache` 优化递归函数的性能
- [ ] 使用 `@cache` 缓存配置/静态数据
- [ ] 通过 `cache_info()` 监控缓存命中率
- [ ] 使用 `@cached_property` 实现惰性计算属性
- [ ] 使用 `@singledispatch` 编写类型分派函数
- [ ] 使用 `@partial` 创建预设参数的函数
- [ ] 理解 functools 装饰器与手写装饰器的区别
- [ ] 在生产环境中合理使用缓存（防止缓存雪崩/穿透）

---

## 延伸阅读

- [functools 官方文档](https://docs.python.org/3/library/functools.html)
- [PEP 3124 — Function Overloading and Generic Functions](https://peps.python.org/pep-3124/)
- [PEP 3155 — @functools.lru_cache](https://peps.python.org/pep-3155/)
- [LRU Cache 实现原理（OrderedDict）](https://docs.python.org/3/library/collections.html#collections.OrderedDict)
