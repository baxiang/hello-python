# 05-functools 标准装饰器

> **Python 版本要求**：Python 3.11+
> **贯穿项目**：Web API 请求处理系统

---

## 概念铺垫

### 为什么需要 functools？

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

### L1 理解层：会用

### @lru_cache / @cache：缓存原理

#### 工作原理

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

#### @lru_cache vs @cache

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

#### 缓存监控：cache_info()

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

#### 斐波那契性能对比

```python
# 有缓存：O(n) 时间复杂度
fibonacci(30)  # ~0.001ms

# 无缓存：O(2^n) 时间复杂度
fibonacci_without_cache(30)  # ~230ms

# 加速比：约 230,000x
```

调用 `GET /api/v1/cache/fibonacci/30` 可以看到实际的性能对比数据。

#### 缓存清理

```python
fibonacci.cache_clear()   # 清空缓存
fibonacci.cache_info()    # 查看统计
```

### @cached_property：惰性计算

#### 与 @property 对比

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

#### 使用场景

- **报表统计**：总和、平均值、中位数等一次性计算
- **对象属性**：从数据库加载后不再变化的派生属性
- **懒加载**：首次使用时才初始化资源（文件连接、网络会话）

#### 注意事项

- 需要 `self` 参数（只能用于实例方法）
- 计算后覆盖属性名，后续访问不再执行函数体
- 不支持 `__slots__` 的类（因为需要写入 `__dict__`）

### @singledispatch：函数重载

#### 传统的 if-elif 写法（不推荐）

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

#### singledispatch 写法（推荐）

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

#### 优势

| 对比项 | if-elif | singledispatch |
|--------|---------|----------------|
| 可扩展性 | 修改原函数 | 在任意位置 `@register` |
| 可读性 | 嵌套深 | 扁平、清晰 |
| 测试 | 一个函数包含所有逻辑 | 每个分支可独立测试 |
| 维护性 | 修改一处影响全局 | 独立注册互不影响 |

#### 3.11+ 的联合类型支持

```python
# Python 3.11+ 支持联合类型注册
@process_data.register
def _(data: str | bytes) -> str:
    return f"Text: {data.decode() if isinstance(data, bytes) else data}"
```

### @partial：偏函数应用

#### 什么是偏函数？

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

#### 应用场景

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

#### partial vs lambda

```python
# lambda 方式（可读性较差，且 __name__ 为 <lambda>）
ok = lambda msg: format_response(200, msg)

# partial 方式（保留函数信息，可序列化）
ok = functools.partial(format_response, 200)
```

### 贯穿实战：缓存端点

本章的缓存演示通过 FastAPI 路由提供两个端点：

#### GET /api/v1/cache/fibonacci/{n}

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

#### GET /api/v1/cache/config/{key}

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

### L2 实践层：用好

#### 推荐做法

| 做法 | 原因 | 示例 |
|------|------|------|
| **递归函数用 `@lru_cache`** | 从 O(2ⁿ) 降到 O(n) | `@lru_cache(maxsize=128) def fib(n):` |
| **输入空间有限用 `@cache`** | 无限缓存，简单直接 | `@cache def get_config(key):` |
| **输入空间无限用 `@lru_cache(maxsize=N)`** | 防止内存泄漏 | `@lru_cache(maxsize=1024) def query(id):` |
| **固定参数用 `partial`** | 比 lambda 更清晰，保留元信息 | `ok = partial(format_response, 200)` |
| **类型分发用 `singledispatch`** | 比 if-elif 可扩展 | `@singledispatch def process(data):` |
| **昂贵计算用 `@cached_property`** | 惰性计算，避免重复 | `@cached_property def stats(self):` |
| **参数必须可哈希** | lru_cache 依赖 dict 键 | 列表/字典/set 不能直接作为参数 |

#### 反模式：不要这样做

```python
# ❌ 错误：用可变对象（不可哈希）作为 lru_cache 的参数
@functools.lru_cache
def bad_cache(data: list):  # TypeError: unhashable type: 'list'
    return sum(data)
# ✅ 正确：转换为可哈希类型
@functools.lru_cache
def good_cache(data: tuple):  # tuple 可哈希
    return sum(data)

# ❌ 错误：cached_property 用于动态值（数据会变化）
class BadConfig:
    def __init__(self):
        self._count = 0

    @functools.cached_property
    def count(self):
        self._count += 1  # 只想计算一次！但后续调用返回缓存值
        return self._count
# ✅ 正确：cached_property 用于不变值；动态值用 @property

# ❌ 错误：singledispatch 默认分支抛异常而非提供兼容处理
@functools.singledispatch
def process(data):
    raise TypeError(f"Unsupported type: {type(data)}")  # 不够友好
# ✅ 正确：默认分支提供兜底逻辑或明确日志
@functools.singledispatch
def process(data):
    logging.warning(f"Falling back to default handler for {type(data)}")
    return str(data)

# ❌ 错误：partial 绑定可变参数后共享状态
defaults = []
add_to_list = functools.partial(defaults.append, 1)
add_to_list()  # defaults 现在是 [1]
add_to_list()  # defaults 现在是 [1, 1] — 副作用共享
```

#### 适用场景

| 场景 | 是否推荐 | 原因 |
|------|---------|------|
| 斐波那契/递归优化 | ✅ 强制推荐 | 无 lru_cache 的递归 fibonacci 不可用 |
| 数据库查询缓存 | ✅ 推荐 | 相同查询结果可复用，减少 I/O |
| 配置文件读取 | ✅ 推荐 | 配置不变，`@cache` 完美适用 |
| 用户请求级缓存（单次） | ❌ 不推荐 | lru_cache 跨请求共享，可能泄露用户数据 |
| Web API 响应缓存 | ⚠️ 慎重 | 需结合 TTL 或主动失效，lru_cache 无过期机制 |
| 高并发环境 | ✅ 可用 | lru_cache 内部有锁（Python 3.12+ 优化为无锁） |

---

### L3 专家层：深入

#### Python 如何实现：lru_cache 内部结构

`lru_cache` 在 CPython 中的实现不是一个简单的 dict，而是基于**双向循环链表**：

```
┌─────────────────────────────────────────────────────────────┐
│  lru_cache 内部 = 字典 + 双向循环链表                            │
│                                                             │
│  ┌───────────────────────────────────────────────────────┐ │
│  │                    双向循环链表                          │ │
│  │                                                         │ │
│  │  sentinel (哨兵节点) ←→ root                            │ │
│  │     ↑                    ↓                               │ │
│  │  [Node]  ←→  [Node]  ←→  [Node]  ←→  [Node]          │ │
│  │  最久未用                         最近使用               │ │
│  │  (LRU)                           (MRU)                 │ │
│  │                                                         │ │
│  └───────────────────────────────────────────────────────┘ │
│                                                             │
│  每个节点 (C 结构体 lru_cache_node)：                          │
│  ┌─────────────────────┐                                    │
│  │ prev  │ next        │  ← 链表指针                        │
│  │ key   │ value       │  ← 缓存键值                        │
│  └─────────────────────┘                                    │
│                                                             │
│  哈希表 (dict): key → Node 的快速查找                        │
│                                                             │
│  操作复杂度：                                                  │
│  ─────────────────                                          │
│  • 查找 (hit)    ：O(1)  哈希表查找 → 节点移到链表头部        │
│  • 插入 (miss)   ：O(1)  计算 → 插入哈希表 + 链表头部        │
│  • 淘汰 (evict)  ：O(1)  取链表尾部 → 删除哈希表 + 移除节点  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**源码位置**：CPython `Modules/_functoolsmodule.c` 中的 `lru_cache_new`、`bounded_lru_cache_wrapper`。

**Python 3.12 优化**：使用 `dict` 原生维护插入序（Python 3.7+ dict 是有序的），在 maxsize=None（即 `@cache`）场景下不再需要链表，直接使用 dict 的插入序作为 LRU 序。

#### singledispatch 注册表

`singledispatch` 内部维护一个 **注册表（registry）**，将类型映射到对应的处理函数：

```
┌─────────────────────────────────────────────────────────────┐
│  singledispatch 注册表                                        │
│                                                             │
│  @singledispatch                                            │
│  def process(data):  ← 默认实现                              │
│                                                             │
│  process.registry:                                           │
│  ┌──────────┬───────────────────────────────┐               │
│  │ 类型     │ 处理函数                       │               │
│  ├──────────┼───────────────────────────────┤               │
│  │ object   │ process (默认)                 │               │
│  │ str      │ _(data: str)                   │               │
│  │ int      │ _(data: int)                   │               │
│  │ list     │ _(data: list)                  │               │
│  │ dict     │ _(data: dict)                  │               │
│  │ str|bytes│ _(data: str | bytes)           │               │
│  └──────────┴───────────────────────────────┘               │
│                                                             │
│  分发规则（MRO 遍历）：                                        │
│  ─────────────────────────                                  │
│  process("hello")                                           │
│    → 类型 str                                                │
│    → registry.get(str) → 找到！执行 str 版本                 │
│                                                             │
│  process(MySubclass())  # MySubclass 未注册                  │
│    → 类型 MySubclass                                         │
│    → registry.get(MySubclass) → 未找到                       │
│    → 遍历 MRO: MySubclass → Parent → object                 │
│    → registry.get(Parent) → 找到？执行。否则到 object         │
│    → registry.get(object) → 默认实现                         │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

验证代码：

```python
import functools

@functools.singledispatch
def process(data):
    return f"default: {data}"

@process.register(str)
def _(data):
    return f"str: {data}"

# 查看注册表
print(process.registry)
# {object: <function process at ...>, str: <function _ at ...>}

# 查看分发类型
print(process.dispatch(str))   # <function _ at ...>
print(process.dispatch(int))   # <function process at ...> (回退到 object)
```

#### wraps 内部实现（descriptor 视角）

`wraps` 返回的 `partial(update_wrapper, ...)` 在应用后会做两件事：
1. 将 `WRAPPER_ASSIGNMENTS` 中列出的属性从 wrapped 复制到 wrapper
2. 将 `WRAPPER_UPDATES` 中的属性合并（更新 `__dict__`）
3. 设置 `wrapper.__wrapped__ = wrapped`

```python
# CPython functools.update_wrapper 简化版实现
WRAPPER_ASSIGNMENTS = ('__module__', '__name__', '__qualname__',
                       '__annotations__', '__doc__')
WRAPPER_UPDATES = ('__dict__',)

def update_wrapper(wrapper, wrapped, assigned=WRAPPER_ASSIGNMENTS,
                   updated=WRAPPER_UPDATES):
    for attr in assigned:
        try:
            value = getattr(wrapped, attr)
        except AttributeError:
            pass
        else:
            setattr(wrapper, attr, value)
    for attr in updated:
        getattr(wrapper, attr).update(getattr(wrapped, attr, {}))
    wrapper.__wrapped__ = wrapped  # 保留原函数引用
    return wrapper
```

#### 性能考量

| 操作 | 时间复杂度 | 说明 |
|------|-----------|------|
| `lru_cache` hit | O(1) | 哈希查找 + 链表操作 |
| `lru_cache` miss | O(1) | 计算 + 插入 |
| `lru_cache` evict | O(1) | 移除尾部节点 |
| `cached_property` 首次访问 | O(1) + 计算开销 | 算一次，存入 `self.__dict__` |
| `cached_property` 再次访问 | O(1) | 直接从 `self.__dict__` 读取 |
| `singledispatch` 分发 | O(1) + MRO 遍历 | 已注册类型 O(1)，未注册走 MRO |
| `partial` 调用 | O(1) | 与正常函数调用几乎无差 |

| 缓存方案 | 查找开销 | 淘汰开销 | 线程安全 | 内存节流 |
|----------|---------|---------|---------|---------|
| `@cache` | O(1) | N/A | 是 | 手动 clear |
| `@lru_cache(128)` | O(1) | O(1) | 是 | 自动 |
| 手写 dict 缓存 | O(1) | 需手写 | 需加锁 | 需手写 |
| Redis 缓存 | 网络 I/O | TTL 自动 | 天然 | 自动 |
| `cached_property` | O(1) | N/A | 是 | 跟随实例生命周期 |

#### 知识关联

```
┌─────────────────────────────────────────────────────────────┐
│  知识关联图：functools → 函数式编程 → 性能优化                 │
│                                                             │
│  第 5 章：functools 标准装饰器                                 │
│  ┌──────────────────────────────────────┐                   │
│  │ • lru_cache / cache                  │                   │
│  │ • cached_property                    │                   │
│  │ • singledispatch (泛型函数)          │                   │
│  │ • partial (偏函数)                   │                   │
│  │ • wraps (元数据保留)                 │                   │
│  └──────────┬───────────────────────────┘                   │
│             │                                                │
│    ┌────────┼───────────────┬──────────────┐                 │
│    ↓        ↓               ↓              ↓                 │
│  functools itertools       operator      more-itertools     │
│  reduce    accumulate      itemgetter    lru_cache替代      │
│  cmp_to_key chain          methodcaller  (第三方增强)        │
│                                                             │
│  Python 函数式编程工具箱：                                     │
│  ─────────────────────────────                               │
│  functools: reduce, partial, cache, singledispatch          │
│  itertools: accumulate, chain, combinations, groupby        │
│  operator: itemgetter, methodcaller, attrgetter             │
│  more-itertools: chunked, flatten, spy, peekable            │
│                                                             │
│  缓存层级选择指南：                                            │
│  ─────────────────                                            │
│  • 函数级缓存 (进程内)  → @lru_cache / @cache                │
│  • 实例级缓存 (对象内)  → @cached_property                   │
│  • 模块级缓存 (全局)    → dict + 手动管理                    │
│  • 分布式缓存 (跨进程)  → Redis / Memcached                  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

### 自检清单

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

### 能力清单

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

### 延伸阅读

- [functools 官方文档](https://docs.python.org/3/library/functools.html)
- [PEP 3124 — Function Overloading and Generic Functions](https://peps.python.org/pep-3124/)
- [PEP 3155 — @functools.lru_cache](https://peps.python.org/pep-3155/)
- [LRU Cache 实现原理（OrderedDict）](https://docs.python.org/3/library/collections.html#collections.OrderedDict)
