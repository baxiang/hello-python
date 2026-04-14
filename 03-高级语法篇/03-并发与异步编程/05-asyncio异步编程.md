# asyncio 异步编程深度指南

> **本章基于 Python 3.11+**
>
> `asyncio` 是 Python 处理高并发 I/O 密集型任务的标准解决方案。它通过**单线程 + 事件循环**的机制，在不需要多线程锁的情况下，实现极高的并发性能。

---

## 1. 核心概念与模型

### 1.1 为什么需要 asyncio？
在传统的同步编程中，代码是阻塞的。例如网络请求发出后，线程会傻傻等待响应，期间什么也做不了。

**多线程 vs 异步：**
*   **多线程**：操作系统负责调度，切换成本高，且存在线程安全问题（锁、死锁）。
*   **异步 (Asyncio)**：用户态（代码层面）主动让出控制权（协作式多任务）。**没有锁**，单线程内切换，效率极高。

### 1.2 三大核心组件

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

---

## 2. 语法基础：Hello World 与避坑

### 2.1 基本语法

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

### 最简示例

```python
import asyncio

async def say_after(delay, what):
    await asyncio.sleep(delay)
    print(what)

async def main():
    print(f"开始")
    await say_after(1, 'hello')
    await say_after(2, 'world')
    print(f"结束")

asyncio.run(main())
```

### 关键代码解释

| 代码 | 含义 | 说明 |
|------|------|------|
| `async def` | 定义协程 | 函数返回协程对象 |
| `await` | 暂停等待 | 让出控制权给事件循环 |
| `asyncio.sleep()` | 异步睡眠 | 非阻塞等待 |
| `asyncio.run()` | 运行协程 | 启动事件循环 |

---

### 2.2 ⚠️ 致命陷阱：阻塞调用
在 `async` 函数中，**绝对不能使用同步阻塞代码**（如 `time.sleep`, `requests.get`）。一旦阻塞，整个事件循环都会卡死，所有其他任务都无法运行。

**对比实验：**

```python
import time
import asyncio

# ❌ 错误写法：阻塞了整个循环
async def bad_task(name):
    print(f"{name} 开始")
    time.sleep(2)  # 同步阻塞，其他任务无法执行
    print(f"{name} 结束")

# ✅ 正确写法：非阻塞
async def good_task(name):
    print(f"{name} 开始")
    await asyncio.sleep(2)  # 让出控制权
    print(f"{name} 结束")
```

### 2.3 核心机制：理解 Await 与挂起

这是异步编程中最难理解，也是最重要的概念。

#### ❌ 误区：挂起 ≠ 阻塞
*   **阻塞 (Blocking)**：像 `time.sleep()`。线程直接“卡死”，CPU 闲着，其他代码也跑不了。
*   **挂起 (Suspending/Yielding)**：遇到 `await` 时，当前协程会**主动暂停**，并**把控制权交还给事件循环**。事件循环会立刻去执行队列里的其他任务。等等待的事情办完了，事件循环再回来接着执行。

#### 生活比喻：奶茶店点单
1.  **阻塞 (Blocking)**：你在柜台前死等，店员叫后面的号你也听不见，队伍全堵死。（多线程模型）
2.  **挂起 (Await)**：你点完单拿到小票（协程对象），去座位上玩手机（交出控制权）。奶茶做好了广播叫号（I/O 完成），你才起身去取（恢复执行）。

```python
async def main():
    print("1. 开始煮咖啡")
    # await 告诉循环：我去煮咖啡了（耗时 2s），这期间你去跑别的任务
    await asyncio.sleep(2) 
    
    print("2. 咖啡好了") 
    # 只有等 2s 到了，循环才会回到这里继续执行
```

### 2.4 什么是 Awaitable 对象？

`await` 关键字后面**不能**随便跟一个整数、字符串或普通函数。它只能跟**“承诺未来会返回结果”**的对象（Awaitable 对象）。

**只有这三类对象可以被 await：**
1. **协程对象**：调用 `async def` 函数的返回值。
2. **Task 对象**：由 `asyncio.create_task()` 创建。
3. **Future 对象**：通常用于底层并发原语。

**代码示例：**

```python
async def fetch():
    return "data"

async def main():
    # ✅ 正确：await 一个协程对象
    res = await fetch()
    
    # ✅ 正确：await 一个 Task
    task = asyncio.create_task(fetch())
    res = await task

    # ❌ 错误：await 一个普通函数 (会报错 TypeError)
    # def sync_func(): return "data"
    # await sync_func() 
```

### 2.5 ⚠️ 新手必踩：常见报错

#### 报错 1：`RuntimeWarning: coroutine 'xxx' was never awaited`
**原因**：你调用了异步函数（比如 `fetch()`），但**忘记加 `await`**。Python 只是创建了一个协程对象，但并没有运行它。
**解决**：加上 `await` 或者用 `asyncio.create_task()`。

```python
# 警告代码
async def main():
    fetch()  # 警告！函数没执行
```

#### 报错 2：`TypeError: object list can't be used in 'await' expression`
**原因**：`await` 后面跟了一个不支持异步的对象（比如列表）。
**解决**：检查你的返回值，确保调用的是异步函数，而不是已经计算好的结果。

---

## 3. 进阶并发控制

### 3.1 并发执行：asyncio.gather
当你需要同时运行多个任务并收集结果时，使用 `gather`。

```python
import asyncio

async def fetch_data(id: int) -> dict:
    print(f"正在获取数据 {id}...")
    await asyncio.sleep(1)  # 模拟网络延迟
    return {"id": id, "status": "success"}

async def main():
    # 1. 并发执行所有任务，总耗时约 1 秒
    results = await asyncio.gather(
        fetch_data(1),
        fetch_data(2),
        fetch_data(3)
    )
    print(f"结果：{results}")

    # 2. 异常处理：return_exceptions=True
    # 默认情况下，一个任务报错，gather 会立即抛出异常并停止。
    # 设为 True 可以将异常作为返回值收集，保证其他任务继续。
    # results = await asyncio.gather(..., return_exceptions=True)

asyncio.run(main())
```

### 3.2 任务调度：asyncio.create_task
如果你希望任务在后台运行，或者需要更精细的控制（如取消任务、检查状态），使用 `create_task`。

*   `gather` 关注的是**结果**。
*   `create_task` 关注的是**任务对象**。

```python
import asyncio

async def background_work():
    print("后台任务：开始")
    await asyncio.sleep(2)
    print("后台任务：完成")
    return 42

async def main():
    # 立即将协程包装为 Task 并排入事件循环
    task = asyncio.create_task(background_work())
    
    print("主程序：任务已创建，继续做其他事...")
    await asyncio.sleep(0.5)  # 模拟主程序耗时操作
    
    # 此时后台任务可能还在运行
    if not task.done():
        print("主程序：后台任务还没做完，先不等它了")
        
    # 必须等待 task 完成，否则程序退出时任务会被取消
    result = await task 
    print(f"主程序：最终结果 {result}")

asyncio.run(main())
```

### 3.3 超时控制：asyncio.wait_for
防止某个任务卡死导致程序永远挂起。

```python
import asyncio

async def slow_task():
    print("开始执行慢任务...")
    await asyncio.sleep(10) # 模拟卡死
    return "Done"

async def main():
    try:
        # 最多等待 2 秒
        result = await asyncio.wait_for(slow_task(), timeout=2.0)
        print(result)
    except asyncio.TimeoutError:
        print("超时：任务被强制取消")

asyncio.run(main())
```

### 3.4 限制并发量：asyncio.Semaphore（实战必学）
如果你有成千上万个 URL 要爬，直接全部 `gather` 会打满带宽或被封 IP。使用信号量限制同时运行的任务数。

```python
import asyncio
import random

sem = asyncio.Semaphore(3) # 最多允许 3 个并发

async def limited_task(task_id):
    # 获取信号量（如果已满 3 个，则在此等待）
    async with sem:
        print(f"任务 {task_id} 开始执行 (当前并发受限)")
        await asyncio.sleep(random.uniform(0.5, 1.5))
        print(f"任务 {task_id} 完成")

async def main():
    tasks = [asyncio.create_task(limited_task(i)) for i in range(10)]
    await asyncio.gather(*tasks)

asyncio.run(main())
```

### 3.5 Python 3.11+ 新特性：TaskGroup (结构化并发)
在旧版本中，`gather` 有一个缺点：如果一个任务失败，它可能不会优雅地取消其他正在运行的任务。**TaskGroup** 引入了结构化并发，更安全。

**优势**：
1.  **自动管理**：组内任务会自动创建和跟踪。
2.  **错误隔离与清理**：任何一个任务抛出异常，组内其他任务会被自动取消，并清理资源。

```python
import asyncio

async def risky_task(name: str, fail: bool = False):
    print(f"{name} 开始")
    await asyncio.sleep(1)
    if fail:
        raise ValueError(f"{name} 失败了！")
    print(f"{name} 完成")
    return name

async def main():
    # 使用 TaskGroup
    async with asyncio.TaskGroup() as tg:
        task1 = tg.create_task(risky_task("Task-1"))
        task2 = tg.create_task(risky_task("Task-2", fail=True))  # 这个会报错
        task3 = tg.create_task(risky_task("Task-3"))

    # 如果 Task-2 失败，整个 with 块会抛出 ValueError，
    # 并且 Task-1 和 Task-3 会被自动取消（如果还没完成）。
    print(f"Task 1 result: {task1.result()}") 

asyncio.run(main())
```

### 3.6 拯救同步代码：run_in_executor
**场景**：你必须调用一个第三方库，但它只提供同步阻塞的 API（比如 `requests` 而不是 `aiohttp`，或者 CPU 密集型计算）。
如果在 `async def` 里直接调用，会卡死整个程序。此时需要**线程池执行器**。

```python
import asyncio
import time

# 这是一个无法修改的同步阻塞函数
def blocking_sync_code():
    print("阻塞中...")
    time.sleep(2)  # 这里的 sleep 是阻塞的
    return "同步任务完成"

async def main():
    loop = asyncio.get_running_loop()
    
    # 将同步函数扔进默认的线程池中运行，不会阻塞主循环
    result = await loop.run_in_executor(None, blocking_sync_code)
    print(result)
    
    print("主循环并没有被卡死！")

asyncio.run(main())
```

---

## 4. 架构模式：生产者-消费者模型

使用 `asyncio.Queue` 在协程间安全地传递数据。这是构建异步爬虫、消息处理系统的核心模式。

```python
import asyncio

async def producer(queue: asyncio.Queue):
    for i in range(5):
        print(f"生产数据: {i}")
        await queue.put(i)  # 放入队列
        await asyncio.sleep(0.1)
    
    # 放入结束标记
    await queue.put(None)

async def consumer(queue: asyncio.Queue):
    while True:
        item = await queue.get()  # 阻塞直到有数据
        if item is None:
            print("收到结束标记，停止消费")
            break
        print(f"消费数据: {item} (处理耗时)")
        await asyncio.sleep(0.3)  # 模拟处理耗时

async def main():
    queue = asyncio.Queue(maxsize=10)
    
    # 启动生产者和多个消费者
    await asyncio.gather(
        producer(queue),
        consumer(queue),
        # 可以启动多个 consumer 实现并发消费
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

---

## 5. 异步迭代与上下文

### 5.1 async for 与 async with
用于处理异步数据流或异步资源管理（如异步数据库连接）。

```python
import asyncio

class AsyncIterator:
    def __init__(self, count):
        self.count = count
        self.current = 0
    
    def __aiter__(self):
        return self
    
    async def __anext__(self):
        if self.current >= self.count:
            raise StopAsyncIteration
        
        await asyncio.sleep(0.1) # 模拟异步获取数据
        self.current += 1
        return self.current

async def main():
    # 异步遍历
    async for item in AsyncIterator(3):
        print(f"获取到 item: {item}")

    # 异步上下文管理器 (async with)
    # 适用于 aiohttp 等需要优雅关闭连接的库
    pass

asyncio.run(main())
```

---

## 6. 调试与异常处理

### 6.1 开启调试模式
异步代码报错往往只显示一行堆栈，很难定位。开启调试模式后，Python 会报告：
*   **执行缓慢的回调**（谁阻塞了循环？）
*   **未被 await 的协程**（内存泄漏警告）

**开启方法：**
1.  **命令行运行**：`PYTHONASYNCIODEBUG=1 python main.py`
2.  **代码开启**：
    ```python
    asyncio.run(main(), debug=True)
    ```

### 6.2 后台任务的异常陷阱
如果你使用 `create_task` 创建了后台任务，但**没有 `await` 它**，且任务中途报错，会发生什么？
*   默认情况下，Python 会静默吞掉异常，只在程序退出时打印一个 `Task exception was never retrieved` 的警告。

**解决方案：**
1.  **务必 `await`**：尽可能在某个地方等待任务结束。
2.  **使用 TaskGroup**：3.11+ 的 `TaskGroup` 会自动传播异常。
3.  **添加 `add_done_callback`**：为任务绑定一个回调函数来处理错误。

```python
import asyncio

async def buggy_task():
    print("任务开始")
    await asyncio.sleep(0.5)
    raise ValueError("出错了！")

def handle_exception(task: asyncio.Task):
    if task.exception():
        print(f"捕获到后台任务异常: {task.exception()}")

async def main():
    # 创建任务
    task = asyncio.create_task(buggy_task())
    
    # 绑定异常处理回调
    task.add_done_callback(handle_exception)
    
    # 假装去忙别的事
    await asyncio.sleep(1)

asyncio.run(main())
```

### 6.3 优雅取消 (Graceful Shutdown)
当收到 `SIGINT` (Ctrl+C) 时，如何确保数据库连接关闭、文件保存完成？
使用 `asyncio.gather` 配合信号处理。

```python
import asyncio
import signal

async def main():
    stop_event = asyncio.Event()
    
    # 监听退出信号
    loop = asyncio.get_running_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, stop_event.set)
    
    print("运行中... 按 Ctrl+C 退出")
    await stop_event.wait()
    print("\n收到退出信号，正在清理资源...")
    # 执行清理逻辑

asyncio.run(main())
```

### 6.4 异步安全锁 (asyncio.Lock)
虽然 asyncio 是单线程的，但如果在 `await` 处交出控制权时，共享数据正处于“中间状态”，其他任务读取就会出错。
此时需要**异步锁**。

**⚠️ 警告**：千万不要在 async 代码中使用 `threading.Lock`，因为它会阻塞整个事件循环！

```python
import asyncio

balance = 100
lock = asyncio.Lock()

async def withdraw(amount):
    global balance
    # 获取锁
    async with lock:
        if balance >= amount:
            # 模拟耗时操作（此处交出控制权）
            await asyncio.sleep(0.1) 
            balance -= amount
            print(f"取款 {amount} 成功，余额: {balance}")
        else:
            print("余额不足")

async def main():
    # 并发取款，Lock 保证数据安全
    await asyncio.gather(withdraw(50), withdraw(60))

asyncio.run(main())
```

---

## 7. 最佳实践与原则

### 7.1 异步编程三大铁律
1.  **绝不阻塞 (Never Block)**：
    *   ❌ `time.sleep()`, `requests.get()`, `input()`.
    *   ✅ `await asyncio.sleep()`, `aiohttp`, `run_in_executor`.
2.  **必须 Await (Always Await)**：
    *   调用 async 函数必须加 `await` 或 `create_task`，否则它只是一个未执行的“尸体”对象。
3.  **区分任务类型**：
    *   🚀 **I/O 密集型**（网络、DB、文件）：**用 Asyncio**。
    *   🧮 **CPU 密集型**（图像处理、加密、复杂计算）：**用 Multiprocessing**。Asyncio 无法加速 CPU 计算。

### 7.2 什么时候用 TaskGroup vs Gather？
*   **Gather**：适合“一荣俱荣”或需要收集所有结果（即使部分失败）。
*   **TaskGroup**：适合“一损俱损”的场景。如果子任务失败，自动取消兄弟任务，防止资源浪费。推荐 Python 3.11+ 优先使用。

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
