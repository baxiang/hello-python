# 05-asyncio异步编程

> **本章基于 Python 3.11+**
>
> `asyncio` 是 Python 处理高并发 I/O 密集型任务的标准解决方案。它通过**单线程 + 事件循环**的机制，在不需要多线程锁的情况下，实现极高的并发性能。

## 概念铺垫

### 为什么需要 asyncio？

在传统的同步编程中，代码是阻塞的。例如网络请求发出后，线程会傻傻等待响应，期间什么也做不了。

**多线程 vs 异步：**
*   **多线程**：操作系统负责调度，切换成本高，且存在线程安全问题（锁、死锁）。
*   **异步 (Asyncio)**：用户态（代码层面）主动让出控制权（协作式多任务）。**没有锁**，单线程内切换，效率极高。

### 三大核心组件

1.  **协程 (Coroutine)**：`async def` 定义的函数。它是一个可以暂停和恢复的计算过程。
2.  **事件循环 (Event Loop)**：程序运行的核心引擎。它负责监听 IO 事件，并在任务间切换。
3.  **任务 (Task)**：协程的包装器。只有被包装成 Task 放入 Loop，协程才会真正执行。

```
┌─────────────────────────────────────────────────────────────┐
│                   异步编程模型                               │
│                                                             │
│  ┌──────────┐      ┌──────────┐      ┌──────────┐           │
│  │ 协程 A   │      │ 协程 B   │      │ 协程 C   │           │
│  └────┬─────┘      └────┬─────┘      └────┬─────┘           │
│       │                 │                 │                  │
│       ▼                 ▼                 ▼                  │
│  ┌─────────────────────────────────────────────────┐        │
│  │               事件循环 (Event Loop)               │        │
│  │                                                 │        │
│  │  1. 调度 A 执行                                  │        │
│  │  2. A 遇到 await (IO 阻塞) -> 暂停 A，切到 B      │        │
│  │  3. B 遇到 await (IO 阻塞) -> 暂停 B，切到 C      │        │
│  │  4. A 的 IO 完成 -> 唤醒 A，继续执行             │        │
│  └─────────────────────────────────────────────────┘        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 理解 Await 与挂起

#### ❌ 误区：挂起 ≠ 阻塞
*   **阻塞 (Blocking)**：像 `time.sleep()`。线程直接"卡死"，CPU 闲着，其他代码也跑不了。
*   **挂起 (Suspending/Yielding)**：遇到 `await` 时，当前协程会**主动暂停**，并**把控制权交还给事件循环**。事件循环会立刻去执行队列里的其他任务。等待的事情办完了，事件循环再回来接着执行。

#### 生活比喻：奶茶店点单
1.  **阻塞 (Blocking)**：你在柜台前死等，店员叫后面的号你也听不见，队伍全堵死。（多线程模型）
2.  **挂起 (Await)**：你点完单拿到小票（协程对象），去座位上玩手机（交出控制权）。奶茶做好了广播叫号（I/O 完成），你才起身去取（恢复执行）。

### 什么是 Awaitable 对象？

`await` 关键字后面**不能**随便跟一个整数、字符串或普通函数。它只能跟**"承诺未来会返回结果"**的对象（Awaitable 对象）。

**只有这三类对象可以被 await：**
1. **协程对象**：调用 `async def` 函数的返回值。
2. **Task 对象**：由 `asyncio.create_task()` 创建。
3. **Future 对象**：通常用于底层并发原语。

---

## 分层学习

### L1 理解层：会用

#### 基本语法

**asyncio三要素：** async、await、事件循环。

```
asyncio语法：
┌─────────────────────────────────────────────────────────────┐
│  asyncio 核心语法                                              │
│                                                              │
│  async def func():    # 定义协程                              │
│      await something  # 暂停等待                              │
│                                                              │
│  asyncio.run(main())  # 启动事件循环                          │
│                                                              │
│  ⚠️ 关键概念：                                                 │
│  ─────────────────────────────                               │
│  async def    → 定义协程函数                                  │
│  await        → 暂停当前协程，等待结果                        │
│  asyncio.run  → 启动事件循环，执行协程                        │
│                                                              │
│  ⚠️ await 后面必须是 awaitable 对象：                         │
│  • 协程对象（调用 async def 函数的返回值）                     │
│  • Task 对象（asyncio.create_task() 创建）                    │
│  • Future 对象（底层并发原语）                                │
│                                                              │
│  ❌ 不能 await：普通函数、整数、字符串                         │
└─────────────────────────────────────────────────────────────┘
```

```python
# asyncio_hello_world.py
import asyncio

async def say_after(delay: float, what: str) -> None:
    await asyncio.sleep(delay)
    print(what)

async def main() -> None:
    print(f"开始")
    await say_after(1, 'hello')
    await say_after(2, 'world')
    print(f"结束")

asyncio.run(main())
```

| 代码 | 含义 | 说明 |
|------|------|------|
| `async def` | 定义协程 | 函数返回协程对象 |
| `await` | 暂停等待 | 让出控制权给事件循环 |
| `asyncio.sleep()` | 异步睡眠 | 非阻塞等待 |
| `asyncio.run()` | 运行协程 | 启动事件循环 |

#### 致命陷阱：阻塞调用

在 `async` 函数中，**绝对不能使用同步阻塞代码**（如 `time.sleep`, `requests.get`）。一旦阻塞，整个事件循环都会卡死，所有其他任务都无法运行。

```python
# blocking_vs_nonblocking.py
import time
import asyncio

# ❌ 错误写法：阻塞了整个循环
async def bad_task(name: str) -> None:
    print(f"{name} 开始")
    time.sleep(2)  # 同步阻塞，其他任务无法执行
    print(f"{name} 结束")

# ✅ 正确写法：非阻塞
async def good_task(name: str) -> None:
    print(f"{name} 开始")
    await asyncio.sleep(2)  # 让出控制权
    print(f"{name} 结束")
```

#### 异步时间线示例

```python
async def main():
    print("1. 开始煮咖啡")
    # await 告诉循环：我去煮咖啡了（耗时 2s），这期间你去跑别的任务
    await asyncio.sleep(2) 
    
    print("2. 咖啡好了") 
    # 只有等 2s 到了，循环才会回到这里继续执行
```

#### Awaitable 对象示例

```python
# await_demo.py
import asyncio

async def fetch() -> str:
    return "data"

async def main() -> None:
    # ✅ 正确：await 一个协程对象
    res = await fetch()
    
    # ✅ 正确：await 一个 Task
    task = asyncio.create_task(fetch())
    res = await task

    # ❌ 错误：await 一个普通函数 (会报错 TypeError)
    # def sync_func(): return "data"
    # await sync_func() 
```

#### 常见报错

**报错 1：`RuntimeWarning: coroutine 'xxx' was never awaited`**
原因：调用了异步函数但**忘记加 `await`**。Python 只是创建了一个协程对象，但并没有运行它。
解决：加上 `await` 或者用 `asyncio.create_task()`。

```python
# unawaited_coroutine_demo.py
async def main() -> None:
    fetch()  # 警告！函数没执行
```

**报错 2：`TypeError: object list can't be used in 'await' expression`**
原因：`await` 后面跟了一个不支持异步的对象（比如列表）。
解决：检查你的返回值，确保调用的是异步函数。

---

### L2 实践层：用好

#### 并发执行：asyncio.gather

当你需要同时运行多个任务并收集结果时，使用 `gather`。

```python
import asyncio

async def fetch_data(id: int) -> dict:
    print(f"正在获取数据 {id}...")
    await asyncio.sleep(1)  # 模拟网络延迟
    return {"id": id, "status": "success"}

async def main():
    # 并发执行所有任务，总耗时约 1 秒
    results = await asyncio.gather(
        fetch_data(1),
        fetch_data(2),
        fetch_data(3)
    )
    print(f"结果：{results}")

    # 异常处理：return_exceptions=True
    # 默认情况下，一个任务报错，gather 会立即抛出异常并停止。
    # 设为 True 可以将异常作为返回值收集，保证其他任务继续。

asyncio.run(main())
```

#### 任务调度：asyncio.create_task

如果你希望任务在后台运行，或者需要更精细的控制（如取消任务、检查状态），使用 `create_task`。

*   `gather` 关注的是**结果**。
*   `create_task` 关注的是**任务对象**。

```python
# create_task_demo.py
import asyncio

async def background_work() -> int:
    print("后台任务：开始")
    await asyncio.sleep(2)
    print("后台任务：完成")
    return 42

async def main() -> None:
    task = asyncio.create_task(background_work())
    
    print("主程序：任务已创建，继续做其他事...")
    await asyncio.sleep(0.5)
    
    if not task.done():
        print("主程序：后台任务还没做完，先不等它了")
        
    result = await task 
    print(f"主程序：最终结果 {result}")

asyncio.run(main())
```

#### 超时控制：asyncio.wait_for

防止某个任务卡死导致程序永远挂起。

```python
# wait_for_timeout_demo.py
import asyncio

async def slow_task() -> str:
    print("开始执行慢任务...")
    await asyncio.sleep(10)  # 模拟卡死
    return "Done"

async def main() -> None:
    try:
        result = await asyncio.wait_for(slow_task(), timeout=2.0)
        print(result)
    except asyncio.TimeoutError:
        print("超时：任务被强制取消")

asyncio.run(main())
```

#### 限制并发量：asyncio.Semaphore

如果你有成千上万个 URL 要爬，直接全部 `gather` 会打满带宽或被封 IP。使用信号量限制同时运行的任务数。

```python
# semaphore_limited_demo.py
import asyncio
import random

sem = asyncio.Semaphore(3)  # 最多允许 3 个并发

async def limited_task(task_id: int) -> None:
    async with sem:
        print(f"任务 {task_id} 开始执行 (当前并发受限)")
        await asyncio.sleep(random.uniform(0.5, 1.5))
        print(f"任务 {task_id} 完成")

async def main() -> None:
    tasks = [asyncio.create_task(limited_task(i)) for i in range(10)]
    await asyncio.gather(*tasks)

asyncio.run(main())
```

#### Python 3.11+ TaskGroup（结构化并发）

在旧版本中，`gather` 有一个缺点：如果一个任务失败，它可能不会优雅地取消其他正在运行的任务。**TaskGroup** 引入了结构化并发，更安全。

**优势**：
1.  **自动管理**：组内任务会自动创建和跟踪。
2.  **错误隔离与清理**：任何一个任务抛出异常，组内其他任务会被自动取消，并清理资源。

```python
# taskgroup_demo.py
import asyncio

async def risky_task(name: str, fail: bool = False) -> str:
    print(f"{name} 开始")
    await asyncio.sleep(1)
    if fail:
        raise ValueError(f"{name} 失败了！")
    print(f"{name} 完成")
    return name

async def main() -> None:
    async with asyncio.TaskGroup() as tg:
        task1 = tg.create_task(risky_task("Task-1"))
        task2 = tg.create_task(risky_task("Task-2", fail=True))  # 这个会报错
        task3 = tg.create_task(risky_task("Task-3"))

    # 如果 Task-2 失败，整个 with 块会抛出 ValueError，
    # 并且 Task-1 和 Task-3 会被自动取消（如果还没完成）。

asyncio.run(main())
```

#### 拯救同步代码：run_in_executor

**场景**：你必须调用一个第三方库，但它只提供同步阻塞的 API（比如 `requests` 而不是 `aiohttp`，或者 CPU 密集型计算）。
如果在 `async def` 里直接调用，会卡死整个程序。此时需要**线程池执行器**。

```python
# run_in_executor_demo.py
import asyncio
import time

def blocking_sync_code() -> str:
    print("阻塞中...")
    time.sleep(2)  # 这里的 sleep 是阻塞的
    return "同步任务完成"

async def main() -> None:
    loop = asyncio.get_running_loop()
    
    result = await loop.run_in_executor(None, blocking_sync_code)
    print(result)
    
    print("主循环并没有被卡死！")

asyncio.run(main())
```

#### 生产者-消费者模型

使用 `asyncio.Queue` 在协程间安全地传递数据。这是构建异步爬虫、消息处理系统的核心模式。

```python
# async_producer_consumer.py
import asyncio

async def producer(queue: asyncio.Queue[int]) -> None:
    for i in range(5):
        print(f"生产数据: {i}")
        await queue.put(i)  # 放入队列
        await asyncio.sleep(0.1)
    
    await queue.put(None)  # 放入结束标记

async def consumer(queue: asyncio.Queue[int]) -> None:
    while True:
        item = await queue.get()  # 阻塞直到有数据
        if item is None:
            print("收到结束标记，停止消费")
            break
        print(f"消费数据: {item} (处理耗时)")
        await asyncio.sleep(0.3)  # 模拟处理耗时

async def main() -> None:
    queue: asyncio.Queue[int] = asyncio.Queue(maxsize=10)
    
    await asyncio.gather(
        producer(queue),
        consumer(queue),
    )

asyncio.run(main())
```

**关键代码说明：**

| 代码 | 含义 | 为什么这样写 |
|------|------|-------------|
| `asyncio.Queue(maxsize=10)` | 有界异步队列 | `maxsize` 限制队列长度；当队列满时，`put()` 会自动挂起生产者，实现背压（backpressure）控制 |
| `await queue.put(i)` | 异步放入数据 | 队列满时 `await` 让出控制权，不阻塞事件循环，等有空位时再继续 |
| `item = await queue.get()` | 异步取出数据 | 队列空时 `await` 挂起消费者，直到生产者放入数据才恢复，无需轮询 |
| `await queue.put(None)` | 发送结束标记 | 用哨兵值 `None` 通知消费者"没有更多数据"，比 `Event` 标志更适合队列场景 |
| `if item is None: break` | 收到哨兵值时退出循环 | 消费者检测到结束标记后退出，而不依赖外部 `stop_event`，逻辑自包含 |

#### 异步迭代与上下文

```python
# async_iterator_demo.py
import asyncio

class AsyncIterator:
    def __init__(self, count: int) -> None:
        self.count = count
        self.current = 0
    
    def __aiter__(self) -> "AsyncIterator":
        return self
    
    async def __anext__(self) -> int:
        if self.current >= self.count:
            raise StopAsyncIteration
        
        await asyncio.sleep(0.1)  # 模拟异步获取数据
        self.current += 1
        return self.current

async def main() -> None:
    async for item in AsyncIterator(3):
        print(f"获取到 item: {item}")

asyncio.run(main())
```

#### 调试与异常处理

**开启调试模式：**
1.  **命令行运行**：`PYTHONASYNCIODEBUG=1 python main.py`
2.  **代码开启**：`asyncio.run(main(), debug=True)`

**后台任务的异常陷阱：**

如果你使用 `create_task` 创建了后台任务，但**没有 `await` 它**，且任务中途报错：
*   默认情况下，Python 会静默吞掉异常，只在程序退出时打印一个 `Task exception was never retrieved` 的警告。

**解决方案：**
1.  **务必 `await`**：尽可能在某个地方等待任务结束。
2.  **使用 TaskGroup**：3.11+ 的 `TaskGroup` 会自动传播异常。
3.  **添加 `add_done_callback`**：为任务绑定一个回调函数来处理错误。

```python
# async_debug_callback_demo.py
import asyncio

async def buggy_task() -> None:
    print("任务开始")
    await asyncio.sleep(0.5)
    raise ValueError("出错了！")

def handle_exception(task: asyncio.Task) -> None:
    if task.exception():
        print(f"捕获到后台任务异常: {task.exception()}")

async def main() -> None:
    task = asyncio.create_task(buggy_task())
    task.add_done_callback(handle_exception)
    await asyncio.sleep(1)

asyncio.run(main())
```

#### 优雅取消

```python
# graceful_shutdown_demo.py
import asyncio
import signal

async def main() -> None:
    stop_event = asyncio.Event()
    
    loop = asyncio.get_running_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, stop_event.set)
    
    print("运行中... 按 Ctrl+C 退出")
    await stop_event.wait()
    print("\n收到退出信号，正在清理资源...")

asyncio.run(main())
```

#### 异步安全锁

虽然 asyncio 是单线程的，但如果在 `await` 处交出控制权时，共享数据正处于"中间状态"，其他任务读取就会出错。
此时需要**异步锁**。

**警告**：千万不要在 async 代码中使用 `threading.Lock`，因为它会阻塞整个事件循环！

```python
# async_lock_demo.py
import asyncio

balance: int = 100
lock = asyncio.Lock()

async def withdraw(amount: int) -> None:
    global balance
    async with lock:
        if balance >= amount:
            await asyncio.sleep(0.1) 
            balance -= amount
            print(f"取款 {amount} 成功，余额: {balance}")
        else:
            print("余额不足")

async def main() -> None:
    await asyncio.gather(withdraw(50), withdraw(60))

asyncio.run(main())
```

#### 推荐做法表

| 推荐做法 | 说明 | 为什么 |
|----------|------|--------|
| **绝不阻塞** | ❌ `time.sleep()`, `requests.get()` / ✅ `await asyncio.sleep()`, `aiohttp` | 一次阻塞卡死整个事件循环 |
| **必须 Await** | 调用 async 函数必须加 `await` 或 `create_task` | 否则函数从未执行 |
| **IO 密集用 async** | 网络、DB、文件 I/O 用 asyncio | CPU 密集应使用多进程 |
| **限制并发量** | 使用 `asyncio.Semaphore` | 防止打满带宽或触发限流 |
| **优先 TaskGroup** | Python 3.11+ 用 `TaskGroup` 替代 `gather` | 自动取消兄弟任务，防止资源泄漏 |
| **绑定异常回调** | 用 `add_done_callback` 处理后台任务异常 | 默认异常被静默吞噬 |

#### 反模式对比

| ❌ 反模式 | ✅ 正确做法 | 说明 |
|-----------|------------|------|
| **async 中用 `time.sleep()`** | `await asyncio.sleep()` | 同步阻塞卡死整个事件循环 |
| **async 中用 `requests`** | `aiohttp` 或 `run_in_executor` | 同上 |
| **忘记 `await` 协程** | 加 `await` 或 `create_task` | 协程从未执行，仅打印警告 |
| **使用 `threading.Lock`** | 使用 `asyncio.Lock` | 同步锁阻塞事件循环 |
| **不收集后台任务异常** | `add_done_callback` 或 `TaskGroup` | 异常被静默吞噬 |

#### 适用场景表

| 场景 | 推荐工具 | 说明 |
|------|---------|------|
| Web 爬虫（10000+ URL） | asyncio + aiohttp + Semaphore | 单线程处理上万个连接 |
| Web API 服务器 | FastAPI / Sanic | 原生异步，高并发 |
| 数据库批量查询 | asyncpg / SQLAlchemy async | 异步驱动，连接池复用 |
| 消息消费 (Kafka/RabbitMQ) | asyncio.Queue + 消费者协程 | 生产者-消费者模型 |
| CPU 密集型计算 | ❌ 不用 asyncio，改用多进程 | asyncio 无法加速 CPU 计算 |
| 调用同步第三方库 | `loop.run_in_executor()` | 将同步代码移到线程池 |

#### TaskGroup vs Gather

*   **Gather**：适合"一荣俱荣"或需要收集所有结果（即使部分失败）。
*   **TaskGroup**：适合"一损俱损"的场景。如果子任务失败，自动取消兄弟任务，防止资源浪费。推荐 Python 3.11+ 优先使用。

---

### L3 专家层：深入

#### 事件循环的 OS 级实现原理图

事件循环是对 OS **I/O 多路复用**机制的封装：

```
┌─────────────────────────────────────────────────────────────┐
│              事件循环底层机制                                 │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   操作系统 I/O 多路复用：                                    │
│   ┌──────────────────────────────────────────────────┐      │
│   │  Linux:    epoll (O(1) 就绪检查)                  │      │
│   │  macOS:    kqueue (类似 epoll)                    │      │
│   │  Windows:  IOCP (完成端口)                        │      │
│   └──────────────────────────────────────────────────┘      │
│                                                             │
│   事件循环工作流程：                                          │
│   1. 注册 I/O 事件到 epoll/kqueue                           │
│   2. epoll_wait() 阻塞等待                                  │
│   3. 有 I/O 事件就绪 → 返回就绪列表                         │
│   4. 将就绪的回调加入任务队列                               │
│   5. 执行回调函数                                           │
│   6. 重复步骤 2-5                                           │
│                                                             │
│   为什么高效？                                                │
│   • 单线程处理成千上万个连接                                │
│   • 不需要为每个连接创建线程                                │
│   • epoll 的 O(1) 就绪检查比 select 的 O(n) 快             │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

#### 协程与生成器的关系

`async def` 在字节码层面是基于 **生成器（generator）** 实现的：

```python
# generator_coroutine_relation.py
"""
协程本质上是增强的生成器。

Python 3.5+ 的 async def 是基于 yield from 的语法糖。
在字节码层面，协程就是带特殊标志的生成器对象。
"""
import asyncio

async def my_coro() -> str:
    await asyncio.sleep(1)
    return "done"

# 大致等价于（简化示意）：
def my_generator():
    yield asyncio.sleep(1)  # 暂停点
    return "done"

import types
coro = my_coro()
print(isinstance(coro, types.CoroutineType))  # True
coro.close()  # 记得清理
```

#### 性能考量表

| 操作 | 时间 | 说明 |
|------|------|------|
| `asyncio.sleep(0)` | ~1μs | 让出控制权，最快切换 |
| `create_task()` | ~5μs | 包装协程并入队 |
| `gather()` N 任务 | ~N×5μs | 线性创建开销 |
| 协程切换 | ~0.5μs | 比线程快 1000 倍 |
| 事件循环迭代 | ~1μs | 无任务时 |
| 连接 10K 个 socket | ~10MB 内存 | 远少于 10K 线程的 ~10GB |

**并发量对比：**

| 方式 | 最大并发连接 | 内存占用（10000 连接） | 上下文切换开销 |
|------|-------------|----------------------|---------------|
| 多线程 | ~1000-3000 | ~10GB（每线程 ~1MB 栈） | ~1-10μs |
| asyncio | ~100,000+ | ~50-100MB | ~0.5μs |

#### 设计动机

| Python 设计选择 | 原因 |
|-----------------|------|
| 单线程事件循环 | 避免锁，简化并发模型 |
| `await` 关键字 | 显式标注暂停点，代码可读性好 |
| `asyncio.run()` 单次调用 | 避免嵌套事件循环的复杂性 |
| TaskGroup（3.11+） | 结构化并发，自动资源清理 |

#### 知识关联图

```
asyncio 知识关联：
┌───────────────────┐
│  async/await      │ ← 语法基础
└────────┬──────────┘
         │
         ▼
┌───────────────────┐     ┌───────────────────┐
│  事件循环         │────→│  I/O 多路复用     │
│  EventLoop        │     │  epoll/kqueue     │
└────────┬──────────┘     └───────────────────┘
         │
    ┌────┴────┐
    ▼         ▼
┌────────┐ ┌───────────┐
│ Task   │ │ gather()  │
│ 任务   │ │ 聚合结果  │
└────┬───┘ └───────────┘
     │
     ▼
┌───────────────────┐
│ TaskGroup (3.11+) │
│ 结构化并发        │
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│ async with/for    │
│ 异步资源管理      │
└───────────────────┘
```

---

## 本章小结

```
┌─────────────────────────────────────────────────────────────┐
│                   asyncio 知识图谱                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. 核心三要素：协程 (Coroutine), 事件循环 (Event Loop),    │
│     任务 (Task)                                              │
│                                                             │
│  2. 必背口诀：                                               │
│     • 同步阻塞是死敌 (No time.sleep/requests)                │
│     • IO 密集用 Async (Network, DB, File IO)                 │
│     • CPU 密集用多进程 (Multiprocessing)                     │
│                                                             │
│  3. 常用 API：                                               │
│     • asyncio.run()：程序入口                                │
│     • asyncio.gather()：并发聚合                             │
│     • asyncio.create_task()：后台任务                        │
│     • asyncio.Semaphore()：并发限流 (生产必备)               │
│     • asyncio.Queue()：数据管道 (生产者/消费者)              │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```
