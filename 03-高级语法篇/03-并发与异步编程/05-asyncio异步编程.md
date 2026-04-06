# asyncio 异步编程（详细版）

> Python 3.11+

## 第一部分：协程基础

### 5.1 async/await 语法

#### 实际场景

需要调用 10 个 Web API，每个 API 响应时间约 1 秒。如果逐个调用，总共需要 10 秒。如何让这些调用并发执行？

**问题：如何使用 async/await 实现异步编程？**

```python
from __future__ import annotations

import asyncio

async def hello() -> None:
    """异步函数（协程）"""
    print("Hello")
    await asyncio.sleep(1)  # 异步等待
    print("World")

# 运行协程
asyncio.run(hello())
```

### 5.2 协程 vs 普通函数

```
┌─────────────────────────────────────────────────────────────┐
│              协程 vs 普通函数                                │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   普通函数：                                                 │
│   • 调用后立即执行                                          │
│   • 阻塞直到返回                                            │
│   • def func():                                             │
│                                                             │
│   协程：                                                     │
│   • 调用后返回协程对象，不立即执行                          │
│   • 可以暂停和恢复                                          │
│   • async def func():                                       │
│                                                             │
│   ┌─────────────────────────────────────────────────────┐   │
│   │  普通函数执行流程                                     │   │
│   │  调用 ──► 执行 ──► 返回                              │   │
│   │          （阻塞）                                     │   │
│   └─────────────────────────────────────────────────────┘   │
│                                                             │
│   ┌─────────────────────────────────────────────────────┐   │
│   │  协程执行流程                                         │   │
│   │  调用 ──► 创建协程对象 ──► await ──► 暂停           │   │
│   │                              │                       │   │
│   │                              ▼                       │   │
│   │                           恢复 ──► 继续执行          │   │
│   │                          （非阻塞）                   │   │
│   └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 5.3 await 的作用

```python
from __future__ import annotations

import asyncio

async def fetch_data(name: str, delay: float) -> str:
    """模拟异步获取数据"""
    print(f"{name}: 开始获取")
    await asyncio.sleep(delay)  # 暂停，让出控制权
    print(f"{name}: 获取完成")
    return f"{name} 的数据"

async def main() -> None:
    # 顺序执行（串行）
    result1: str = await fetch_data("A", 1)
    result2: str = await fetch_data("B", 1)
    print(f"结果: {result1}, {result2}")
    # 总耗时约 2 秒

asyncio.run(main())
```

## 第二部分：并发执行

### 5.4 asyncio.gather

```python
from __future__ import annotations

import asyncio

async def fetch_data(name: str, delay: float) -> str:
    print(f"{name}: 开始获取")
    await asyncio.sleep(delay)
    print(f"{name}: 获取完成")
    return f"{name} 的数据"

async def main() -> None:
    # 并发执行（并行）
    results: tuple[str, ...] = await asyncio.gather(
        fetch_data("A", 1),
        fetch_data("B", 1),
        fetch_data("C", 1)
    )
    print(f"结果: {results}")
    # 总耗时约 1 秒（同时执行）

asyncio.run(main())
```

### 5.5 asyncio.create_task

```python
from __future__ import annotations

import asyncio

async def fetch_data(name: str, delay: float) -> str:
    print(f"{name}: 开始")
    await asyncio.sleep(delay)
    print(f"{name}: 完成")
    return f"{name} 的数据"

async def main() -> None:
    # 创建任务（立即调度）
    task1: asyncio.Task[str] = asyncio.create_task(fetch_data("A", 1))
    task2: asyncio.Task[str] = asyncio.create_task(fetch_data("B", 2))
    
    # 做其他事情
    print("任务已创建，做其他事情...")
    await asyncio.sleep(0.5)
    
    # 等待任务完成
    result1: str = await task1
    result2: str = await task2
    print(f"结果: {result1}, {result2}")

asyncio.run(main())
```

### 5.6 gather vs create_task

```
┌─────────────────────────────────────────────────────────────┐
│              gather vs create_task                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   asyncio.gather：                                          │
│   • 同时启动多个协程                                        │
│   • 等待所有完成                                            │
│   • 返回结果列表                                            │
│                                                             │
│   asyncio.create_task：                                      │
│   • 创建单个任务                                            │
│   • 立即调度执行                                            │
│   • 返回 Task 对象                                          │
│                                                             │
│   使用场景：                                                 │
│   • gather：批量执行，需要所有结果                          │
│   • create_task：后台任务，需要控制任务                     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## 第三部分：事件循环

### 5.7 获取事件循环

```python
from __future__ import annotations

import asyncio

async def main() -> None:
    # 获取当前运行中的事件循环
    loop: asyncio.AbstractEventLoop = asyncio.get_running_loop()
    print(f"事件循环: {loop}")

asyncio.run(main())

# 在协程外部获取
loop: asyncio.AbstractEventLoop = asyncio.get_event_loop()
print(f"当前线程的循环: {loop}")
```

### 5.8 事件循环的工作方式

```
┌─────────────────────────────────────────────────────────────┐
│              事件循环工作流程                                │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   事件循环                                                   │
│   ┌─────────────────────────────────────────────────────┐   │
│   │                                                     │   │
│   │   任务队列                                          │   │
│   │   ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐                │   │
│   │   │Task1│ │Task2│ │Task3│ │Task4│                │   │
│   │   └─────┘ └─────┘ └─────┘ └─────┘                │   │
│   │                                                     │   │
│   │   循环：                                            │   │
│   │   1. 从队列取出任务                                 │   │
│   │   2. 执行到 await                                   │   │
│   │   3. 暂停任务，放回队列                             │   │
│   │   4. 取出下一个任务                                 │   │
│   │   5. 重复...                                        │   │
│   │                                                     │   │
│   └─────────────────────────────────────────────────────┘   │
│                                                             │
│   单线程，通过任务切换实现并发                              │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## 第四部分：异步迭代

### 5.9 async for

```python
from __future__ import annotations

import asyncio

async def async_generator() -> asyncio.AsyncGenerator[int, None]:
    """异步生成器"""
    for i in range(5):
        await asyncio.sleep(0.1)
        yield i

async def main() -> None:
    # 异步迭代
    async for item in async_generator():
        print(item)

asyncio.run(main())
```

### 5.10 async with

```python
from __future__ import annotations

import asyncio

class AsyncContext:
    async def __aenter__(self) -> AsyncContext:
        print("进入异步上下文")
        await asyncio.sleep(0.1)
        return self
    
    async def __aexit__(self, exc_type: type | None, exc_val: Exception | None, exc_tb: object) -> None:
        print("退出异步上下文")
        await asyncio.sleep(0.1)

async def main() -> None:
    async with AsyncContext() as ctx:
        print("在异步上下文中")

asyncio.run(main())
```

## 第五部分：异步网络请求

### 5.11 aiohttp 示例

```python
from __future__ import annotations

import asyncio
import aiohttp

async def fetch(url: str) -> str:
    """异步获取 URL"""
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()

async def main() -> None:
    urls: list[str] = [
        "https://httpbin.org/delay/1",
        "https://httpbin.org/delay/1",
        "https://httpbin.org/delay/1"
    ]
    
    # 并发获取
    tasks: list[asyncio.Task[str]] = [fetch(url) for url in urls]
    results: list[str] = await asyncio.gather(*tasks)
    
    for i, result in enumerate(results):
        print(f"URL {i+1}: {len(result)} 字节")

asyncio.run(main())
```

## 第六部分：超时和取消

### 5.12 asyncio.wait_for

```python
from __future__ import annotations

import asyncio

async def slow_operation() -> str:
    await asyncio.sleep(10)
    return "完成"

async def main() -> None:
    try:
        # 设置超时
        result: str = await asyncio.wait_for(slow_operation(), timeout=2.0)
        print(result)
    except asyncio.TimeoutError:
        print("操作超时")

asyncio.run(main())
```

### 5.13 取消任务

```python
from __future__ import annotations

import asyncio

async def long_task() -> None:
    try:
        for i in range(10):
            await asyncio.sleep(1)
            print(f"执行中... {i+1}/10")
    except asyncio.CancelledError:
        print("任务被取消")
        raise

async def main() -> None:
    task: asyncio.Task[None] = asyncio.create_task(long_task())
    
    await asyncio.sleep(3)
    task.cancel()  # 取消任务
    
    try:
        await task
    except asyncio.CancelledError:
        print("任务已取消")

asyncio.run(main())
```

## 本章小结

```
┌─────────────────────────────────────────────────────────────┐
│                      asyncio 异步编程 知识要点               │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   协程基础：                                                 │
│   ✓ async def 定义协程                                      │
│   ✓ await 等待协程完成                                      │
│   ✓ asyncio.run() 运行                                      │
│                                                             │
│   并发执行：                                                 │
│   ✓ asyncio.gather() 批量并发                               │
│   ✓ asyncio.create_task() 创建任务                          │
│                                                             │
│   事件循环：                                                 │
│   ✓ 单线程任务调度                                          │
│   ✓ asyncio.get_running_loop()                              │
│                                                             │
│   异步特性：                                                 │
│   ✓ async for 异步迭代                                      │
│   ✓ async with 异步上下文                                   │
│                                                             │
│   超时取消：                                                 │
│   ✓ asyncio.wait_for() 超时                                 │
│   ✓ task.cancel() 取消                                      │
│                                                             │
│   适用场景：                                                 │
│   ✓ I/O 密集型任务                                          │
│   ✓ 网络请求、数据库操作                                    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```