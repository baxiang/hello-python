# 迭代器与生成器

Python 迭代器与生成器示例项目，覆盖第 01-06 章（迭代基础 → 自定义迭代器 → 生成器 → 高级特性 → itertools → 异步生成器）。

## 场景

日志流处理系统：通过 LogEntry、迭代器、生成器等方式，演示如何处理日志流的遍历、过滤、聚合和异步产出。

## 项目结构

```
iterators_demo/
├── pyproject.toml
├── app/
│   ├── __init__.py
│   ├── core/
│   │   └── iterators.py    # ch01-06: 迭代器、生成器、itertools、异步生成器
│   └── utils/
│       └── helpers.py      # 格式化、批量生成器
└── tests/
    └── test_iterators.py   # 25 个测试
```

## 安装

```bash
uv sync
```

## 使用示例

```python
from app.core.iterators import (
    LogEntry, LogIterator, LogCollection,
    log_generator, filter_by_level, fibonacci,
    log_accumulator, merge_logs,
    take_first_n, group_by_level,
    async_log_stream, collect_async
)
import asyncio

# ch01: 迭代协议
entries = [LogEntry("INFO", "启动"), LogEntry("ERROR", "失败")]
list(LogIterator(entries))

# ch02: 自定义迭代器
collection = LogCollection(entries)
collection.add(LogEntry("WARN", "警告"))
list(collection)  # 可多次迭代

# ch03: 生成器
list(filter_by_level(entries, "ERROR"))
list(itertools.islice(fibonacci(), 10))  # 前 10 个斐波那契数

# ch04: send() / throw() / yield from
gen = log_accumulator()
next(gen)
gen.send(LogEntry("INFO", "msg"))  # → 1

# ch05: itertools
group_by_level(entries)  # → {"ERROR": [...], "INFO": [...]}

# ch06: 异步生成器
async def main():
    result = await collect_async(entries)
asyncio.run(main())
```

## 运行测试

```bash
uv run pytest               # 全部测试
uv run pytest -k "generat"  # 只运行生成器相关测试
uv run pytest -k "async"    # 只运行异步测试
```

## 章节映射

| 代码文件 | 对应章节 | 核心内容 |
|---------|---------|---------|
| `iterators.py` | ch01 | iter()/next()、StopIteration、可迭代 vs 迭代器 |
| `iterators.py` | ch02 | LogIterator（__iter__/__next__）、LogCollection（多次迭代） |
| `iterators.py` | ch03 | yield 生成器函数、生成器表达式、无限序列 |
| `iterators.py` | ch04 | send() 双向通信、throw() 注入异常、yield from 委托 |
| `iterators.py` | ch05 | islice/chain/takewhile/groupby/count |
| `iterators.py` | ch06 | async def + yield、async for |
