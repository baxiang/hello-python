# 装饰器与闭包

Python 装饰器与闭包示例项目，覆盖第 01-04 章（装饰器基础 → 闭包 → lru_cache/partial → 带参数/叠加/类装饰器）。

## 场景

API 请求处理中间件：通过日志记录、计时、限流、重试、验证等装饰器，演示 Python 装饰器的各种模式。

## 项目结构

```
decorators_demo/
├── pyproject.toml
├── app/
│   ├── __init__.py
│   ├── core/
│   │   └── decorators.py   # ch01-04: 装饰器、闭包、lru_cache、带参数装饰器
│   └── utils/
│       └── helpers.py      # 计数器闭包、装饰器组合
└── tests/
    └── test_decorators.py  # 25 个测试
```

## 安装

```bash
uv sync
```

## 使用示例

```python
from app.core.decorators import (
    log_call, timer, make_counter, make_rate_limiter,
    expensive_parse, retry, validate_positive, singleton
)

# ch01: 基础装饰器
@log_call
def add(a, b): return a + b

@timer
def slow_func(): ...
slow_func()
print(slow_func.last_elapsed)  # 上次耗时

# ch02: 闭包 + nonlocal
cnt = make_counter()
cnt(), cnt(), cnt()  # → 1, 2, 3

limiter = make_rate_limiter(max_calls=2)

# ch03: lru_cache + partial
expensive_parse("/api/data")  # 第一次慢，后续直接返回缓存

# ch04: 带参数装饰器 + 叠加
@retry(max_attempts=3)
@validate_positive
def sqrt(x): return x ** 0.5

# ch04: 类装饰器（单例）
@singleton
class Config: ...
c1, c2 = Config(), Config()
c1 is c2  # → True
```

## 运行测试

```bash
uv run pytest               # 全部测试
uv run pytest -k "closure"  # 只运行闭包测试
uv run pytest -k "retry"    # 只运行重试测试
```

## 章节映射

| 代码文件 | 对应章节 | 核心内容 |
|---------|---------|---------|
| `decorators.py` | ch01 | @语法糖、@wraps、log_call、timer |
| `decorators.py` | ch02 | 闭包、nonlocal、make_counter、make_rate_limiter |
| `decorators.py` | ch03 | @lru_cache 缓存、functools.partial 偏函数 |
| `decorators.py` | ch04 | 带参数装饰器（retry）、叠加装饰器、类装饰器（singleton） |
| `helpers.py` | ch02 | counter() 闭包、compose_decorators 装饰器组合 |
