# 第 23 章 - asyncio 高级编程（详细版）

> **本章定位**：深入理解 asyncio 的核心机制，掌握事件循环、任务调度、异步队列等高级特性，构建高性能异步应用。

---

## 第一部分：深入理解事件循环

### 20.1 什么是事件循环

#### 核心概念

```
┌─────────────────────────────────────────┐
│          事件循环（Event Loop）         │
├─────────────────────────────────────────┤
│                                         │
│  事件循环是 asyncio 的心脏，负责：      │
│  ─────────────────────────────          │
│  1. 调度和运行协程                      │
│  2. 处理 I/O 事件（网络、文件等）        │
│  3. 管理定时器和延迟任务                │
│  4. 处理进程间通信                      │
│  5. 管理任务队列和回调函数              │
│                                         │
│  ─────────────────────────────────      │
│                                         │
│  类比：餐厅服务员                       │
│  ──────────────                        │
│  服务员（事件循环）照顾多桌客人（任务） │
│  - 给 A 桌上菜 → A 桌慢慢吃（await）     │
│  - 转身给 B 桌点菜                       │
│  - B 桌点完厨房做（await）              │
│  - 转身给 C 桌结账                       │
│  - A 桌吃完了，端走盘子（任务完成）     │
│                                         │
│  一个服务员高效服务多桌，不浪费时间！   │
│                                         │
└─────────────────────────────────────────┘
```

#### 事件循环工作原理

```
┌─────────────────────────────────────────────────────────┐
│                  事件循环工作流程                       │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  while True:  # 事件循环主循环                          │
│                                                         │
│      # 1. 检查是否有就绪的任务                         │
│      ready_tasks = check_ready_tasks()                 │
│                                                         │
│      # 2. 处理 I/O 事件（使用 select/epoll/kqueue）     │
│      io_events = wait_for_io(timeout=0)                │
│                                                         │
│      # 3. 运行就绪的回调函数                           │
│      for callback in ready_callbacks:                  │
│          callback()                                    │
│                                                         │
│      # 4. 调度到期的定时任务                           │
│      schedule_timers()                                 │
│                                                         │
│      # 5. 如果没有就绪事件，等待新事件                 │
│      if not ready_tasks and not io_events:             │
│          wait_for_new_events()                         │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

#### 手动运行事件循环

```python
import asyncio

# ─────────────────────────────────────
# asyncio.run() 是高层封装，实际做了：
# ─────────────────────────────────────

# 底层实现等价于：
loop = asyncio.new_event_loop()
try:
    asyncio.set_event_loop(loop)
    task = loop.create_task(main())
    loop.run_until_complete(task)
finally:
    loop.close()
    asyncio.set_event_loop(None)

# ─────────────────────────────────────
# 显式使用事件循环
# ─────────────────────────────────────

async def say_hello():
    print("Hello")
    await asyncio.sleep(1)
    print("World")

# 创建事件循环
loop = asyncio.get_event_loop()

# 运行协程直到完成
loop.run_until_complete(say_hello())

# 运行永久循环（用于服务器）
# loop.run_forever()

# 关闭循环
loop.close()
```

---

### 20.2 事件循环的类型

```python
import asyncio

# ─────────────────────────────────────
# 1. 获取当前事件循环
# ─────────────────────────────────────

# 在协程内部获取
async def inside_coroutine():
    loop = asyncio.get_running_loop()
    print(f"当前运行中的循环：{loop}")

# 在协程外部获取（Python 3.10+）
loop = asyncio.get_event_loop()
print(f"当前线程的循环：{loop}")

# ─────────────────────────────────────
# 2. 创建新的事件循环
# ─────────────────────────────────────

new_loop = asyncio.new_event_loop()
asyncio.set_event_loop(new_loop)

# ─────────────────────────────────────
# 3. 检查循环状态
# ─────────────────────────────────────

print(f"循环是否运行中：{loop.is_running()}")
print(f"循环是否已关闭：{loop.is_closed()}")
```

---

### 20.3 在已运行的循环中创建任务

```python
import asyncio
import threading

# ─────────────────────────────────────
# 场景：从同步代码或非协程上下文启动异步任务
# ─────────────────────────────────────

async def background_task():
    await asyncio.sleep(1)
    print("后台任务完成")

def sync_function():
    """同步函数中需要启动异步任务"""
    loop = asyncio.get_running_loop()
    # 创建任务（不会立即等待）
    task = loop.create_task(background_task())
    return task

# ─────────────────────────────────────
# 在线程中启动协程
# ─────────────────────────────────────

def run_async_in_thread(coroutine, loop):
    """在线程中运行协程"""
    future = asyncio.run_coroutine_threadsafe(coroutine, loop)
    return future.result()  # 阻塞等待结果

# 主循环
async def main():
    loop = asyncio.get_running_loop()

    # 在另一个线程运行协程
    future = asyncio.run_coroutine_threadsafe(
        background_task(),
        loop
    )

    # 可以在这里做其他事情
    await asyncio.sleep(0.5)

    # 等待结果
    await future

# asyncio.run(main())
```

---

### 20.4 事件循环的回调机制

```python
import asyncio
import time

# ─────────────────────────────────────
# call_soon - 尽快执行（下一轮循环）
# ─────────────────────────────────────

async def demo_call_soon():
    loop = asyncio.get_running_loop()

    def callback(name):
        print(f"回调执行：{name}")

    # 尽快调度（但不立即执行）
    loop.call_soon(callback, "任务 1")
    loop.call_soon(callback, "任务 2")

    print("call_soon 已调度")

    # 需要 await 让出控制权，回调才会执行
    await asyncio.sleep(0)
    print("第一次 sleep 后")

    await asyncio.sleep(0)
    print("第二次 sleep 后")

# ─────────────────────────────────────
# call_later - 延迟执行
# ─────────────────────────────────────

async def demo_call_later():
    loop = asyncio.get_running_loop()

    def callback(delay_name):
        print(f"{delay_name} 在 {time.strftime('%X')} 执行")

    print(f"开始时间：{time.strftime('%X')}")

    # 1 秒后执行
    handle1 = loop.call_later(1, callback, "延迟 1 秒")

    # 2 秒后执行
    handle2 = loop.call_later(2, callback, "延迟 2 秒")

    # 等待足够时间让回调执行
    await asyncio.sleep(2.5)

    # 取消调度
    # handle1.cancel()

# ─────────────────────────────────────
# call_at - 在指定时间执行
# ─────────────────────────────────────

async def demo_call_at():
    loop = asyncio.get_running_loop()

    # 获取当前事件循环时间
    current_time = loop.time()

    # 5 秒后执行
    loop.call_at(current_time + 5, lambda: print("5 秒到了！"))

    await asyncio.sleep(5.1)

# asyncio.run(demo_call_soon())
```

---

## 第二部分：asyncio.Queue 异步队列

### 20.5 Queue 基础

#### 为什么需要异步队列

```
┌─────────────────────────────────────────┐
│     生产者 - 消费者模型的异步版本       │
├─────────────────────────────────────────┤
│                                         │
│  问题：标准 queue.Queue 是同步的       │
│  ─────────────────────────────          │
│  • put() 会阻塞整个事件循环            │
│  • get() 会阻塞整个事件循环            │
│  • 导致其他协程无法运行                  │
│                                         │
│  解决：使用 asyncio.Queue              │
│  ─────────────────────────────          │
│  • put() 是协程，await 等待             │
│  • get() 是协程，await 等待             │
│  • 不会阻塞，等待时其他协程可运行      │
│                                         │
└─────────────────────────────────────────┘
```

#### 基本使用

```python
import asyncio

async def producer(queue, name, count):
    """生产者：生产数据放入队列"""
    for i in range(count):
        item = f"{name} 生产的消息 {i}"

        # put 是协程，队列满时会等待
        await queue.put(item)
        print(f"放入：{item}")

        await asyncio.sleep(0.1)  # 模拟生产时间

    # 放入结束标记
    await queue.put(None)

async def consumer(queue, name):
    """消费者：从队列取出数据处理"""
    while True:
        # get 是协程，队列空时会等待
        item = await queue.get()

        # 检查结束标记
        if item is None:
            # 重新放入，让其他消费者也能退出
            await queue.put(None)
            break

        print(f"{name} 消费：{item}")
        await asyncio.sleep(0.2)  # 模拟消费时间

        # 标记任务完成
        queue.task_done()

async def main():
    # 创建队列（maxsize=5 表示最多容纳 5 个元素）
    queue = asyncio.Queue(maxsize=5)

    # 创建生产者
    producer_task = asyncio.create_task(
        producer(queue, "生产者", 10)
    )

    # 创建多个消费者
    consumer_tasks = [
        asyncio.create_task(consumer(queue, f"消费者-{i}"))
        for i in range(3)
    ]

    # 等待生产者完成
    await producer_task

    # 等待队列中所有任务处理完成
    await queue.join()

    # 取消消费者（因为 None 标记可能没被所有消费者处理）
    for task in consumer_tasks:
        task.cancel()

    await asyncio.gather(*consumer_tasks, return_exceptions=True)

# asyncio.run(main())
```

---

### 20.6 Queue 类型对比

```python
import asyncio

async def demo_queue_types():
    # ──────────────────────────────────
    # asyncio.Queue - 普通队列（FIFO）
    # ──────────────────────────────────
    queue = asyncio.Queue()
    await queue.put(1)
    await queue.put(2)
    await queue.put(3)

    print(f"Queue: {await queue.get()}")  # 1
    print(f"Queue: {await queue.get()}")  # 2
    print(f"Queue: {await queue.get()}")  # 3

    # ──────────────────────────────────
    # asyncio.PriorityQueue - 优先级队列
    # ──────────────────────────────────
    pqueue = asyncio.PriorityQueue()

    # (优先级，数据) - 优先级数字越小越优先
    await pqueue.put((3, "低优先级"))
    await pqueue.put((1, "高优先级"))
    await pqueue.put((2, "中优先级"))

    print(f"Priority: {await pqueue.get()}")  # (1, '高优先级')
    print(f"Priority: {await pqueue.get()}")  # (2, '中优先级')
    print(f"Priority: {await pqueue.get()}")  # (3, '低优先级')

    # ──────────────────────────────────
    # asyncio.LifoQueue - 后进先出（LIFO）
    # ──────────────────────────────────
    lifo = asyncio.LifoQueue()

    await lifo.put("第一个")
    await lifo.put("第二个")
    await lifo.put("第三个")

    print(f"LIFO: {await lifo.get()}")  # 第三个
    print(f"LIFO: {await lifo.get()}")  # 第二个
    print(f"LIFO: {await lifo.get()}")  # 第一个

# asyncio.run(demo_queue_types())
```

---

### 20.7 Queue 实用方法

```python
import asyncio

async def demo_queue_methods():
    queue = asyncio.Queue(maxsize=3)

    # ──────────────────────────────────
    # put_nowait - 非阻塞放入
    # ──────────────────────────────────
    try:
        queue.put_nowait(1)
        queue.put_nowait(2)
        queue.put_nowait(3)
        # queue.put_nowait(4)  # 队列满，抛出 QueueFull
    except asyncio.QueueFull:
        print("队列已满！")

    # ──────────────────────────────────
    # get_nowait - 非阻塞获取
    # ──────────────────────────────────
    print(f"大小：{queue.qsize()}")  # 3
    print(f"是否空：{queue.empty()}")  # False
    print(f"是否满：{queue.full()}")  # True

    item = queue.get_nowait()
    print(f"获取：{item}")  # 1

    # ──────────────────────────────────
    # join - 等待所有任务完成
    # ──────────────────────────────────
    queue2 = asyncio.Queue()

    async def worker():
        while True:
            item = await queue2.get()
            if item is None:
                break
            print(f"处理：{item}")
            await asyncio.sleep(0.1)
            queue2.task_done()  # 标记任务完成

    # 启动工作线程
    task = asyncio.create_task(worker())

    # 放入任务
    for i in range(5):
        await queue2.put(i)

    # 等待所有任务完成
    await queue2.join()
    print("所有任务已完成！")

    # 停止 worker
    await queue2.put(None)
    await task
```

---

### 20.8 实战：使用队列进行限流

```python
import asyncio
import time

class RateLimiter:
    """使用队列实现限流器"""

    def __init__(self, rate):
        """
        rate: 每秒允许的请求数
        """
        self.queue = asyncio.Queue(maxsize=rate)
        self.rate = rate

    async def acquire(self):
        """获取许可（如果达到限流则等待）"""
        await self.queue.put(None)

    async def _refill(self):
        """补充许可令牌"""
        while True:
            await asyncio.sleep(1 / self.rate)
            try:
                self.queue.get_nowait()
            except asyncio.QueueEmpty:
                pass

    async def start(self):
        """启动限流器"""
        # 初始化填满队列
        for _ in range(self.rate):
            await self.queue.put(None)
        # 启动后台补充任务
        asyncio.create_task(self._refill())

async def fetch(limiter, task_id):
    """模拟受限的请求"""
    await limiter.acquire()
    print(f"[{time.strftime('%X')}] 任务 {task_id} 执行")
    await asyncio.sleep(0.1)
    return f"任务 {task_id} 完成"

async def main():
    # 限制每秒 2 个请求
    limiter = RateLimiter(rate=2)
    await limiter.start()

    # 创建 10 个任务
    tasks = [
        asyncio.create_task(fetch(limiter, i))
        for i in range(10)
    ]

    results = await asyncio.gather(*tasks)
    print(f"\n所有任务完成：{results}")

# asyncio.run(main())
```

---

## 第三部分：Task 任务管理

### 20.9 创建和管理任务

```python
import asyncio

async def worker(name, delay):
    """工作协程"""
    try:
        for i in range(5):
            await asyncio.sleep(delay)
            print(f"{name} - 第 {i+1} 次执行")
        return f"{name} 正常完成"
    except asyncio.CancelledError:
        print(f"{name} 被取消")
        raise

async def demo_task_management():
    # ──────────────────────────────────
    # 创建任务
    # ──────────────────────────────────
    task1 = asyncio.create_task(worker("任务 A", 0.5), name="Task-A")
    task2 = asyncio.create_task(worker("任务 B", 0.7), name="Task-B")

    # ──────────────────────────────────
    # 获取任务信息
    # ──────────────────────────────────
    print(f"任务名称：{task1.get_name()}")
    print(f"任务是否完成：{task1.done()}")
    print(f"任务是否正在运行：{not task1.done() and not task1.cancelled()}")

    # ──────────────────────────────────
    # 获取任务结果
    # ──────────────────────────────────
    result = await task1
    print(f"任务 1 结果：{result}")

    # ──────────────────────────────────
    # 取消任务
    # ──────────────────────────────────
    task2.cancel()
    try:
        await task2
    except asyncio.CancelledError:
        print("任务 2 已被取消")

    # ──────────────────────────────────
    # 等待多个任务
    # ──────────────────────────────────
    tasks = [
        asyncio.create_task(worker(f"任务-{i}", 0.3))
        for i in range(5)
    ]

    # 等待所有完成
    results = await asyncio.gather(*tasks, return_exceptions=True)
    print(f"所有结果：{results}")
```

---

### 20.10 任务组（TaskGroup）- Python 3.11+

```python
import asyncio

# ─────────────────────────────────────
# Python 3.11+ 新增的任务组
# ─────────────────────────────────────

async def risky_task(name, should_fail=False):
    """可能失败的任务"""
    await asyncio.sleep(0.5)
    if should_fail:
        raise ValueError(f"{name} 出错了")
    return f"{name} 成功"

async def demo_taskgroup():
    # 任务组自动处理异常和取消
    async with asyncio.TaskGroup() as tg:
        task1 = tg.create_task(risky_task("任务 1"))
        task2 = tg.create_task(risky_task("任务 2", should_fail=True))
        task3 = tg.create_task(risky_task("任务 3"))

        # 如果任一任务失败，其他任务会被自动取消
        print(f"任务 1 结果：{task1.result()}")
        print(f"任务 2 结果：{task2.result()}")
        print(f"任务 3 结果：{task3.result()}")

# 异常会被收集并抛出 ExceptionGroup
try:
    asyncio.run(demo_taskgroup())
except ExceptionGroup as eg:
    print(f"捕获到异常组：{eg.exceptions}")
```

---

### 20.11 并发控制 - Semaphore

```python
import asyncio

async def limited_worker(worker_id, semaphore):
    """受信号量限制的工作器"""
    async with semaphore:
        print(f"worker-{worker_id} 开始执行")
        await asyncio.sleep(1)
        print(f"worker-{worker_id} 完成")
    return f"worker-{worker_id} 结果"

async def demo_semaphore():
    # 最多允许 3 个任务同时执行
    semaphore = asyncio.Semaphore(3)

    # 创建 10 个任务
    tasks = [
        asyncio.create_task(limited_worker(i, semaphore))
        for i in range(10)
    ]

    results = await asyncio.gather(*tasks)
    print(f"所有结果：{results}")

    # 输出特点：
    # 最多 3 个 worker 同时"开始执行"
    # 一个完成后，下一个才开始

# asyncio.run(demo_semaphore())
```

---

## 第四部分：异步迭代器和生成器

### 20.12 异步迭代器

```python
import asyncio

# ─────────────────────────────────────
# 异步迭代器类
# ─────────────────────────────────────

class AsyncRange:
    """异步版本的 range"""

    def __init__(self, start, end, delay=0.1):
        self.start = start
        self.end = end
        self.delay = delay
        self.current = start

    def __aiter__(self):
        """返回异步迭代器"""
        return self

    async def __anext__(self):
        """异步获取下一个值"""
        if self.current >= self.end:
            raise StopAsyncIteration
        value = self.current
        self.current += 1
        await asyncio.sleep(self.delay)  # 模拟异步操作
        return value

async def demo_async_iterator():
    async for num in AsyncRange(0, 5):
        print(f"获取到：{num}")

# asyncio.run(demo_async_iterator())
```

---

### 20.13 异步生成器

```python
import asyncio

# ─────────────────────────────────────
# 异步生成器函数
# ─────────────────────────────────────

async def async_range(start, end, delay=0.1):
    """异步生成器"""
    for i in range(start, end):
        await asyncio.sleep(delay)
        yield i

async def demo_async_generator():
    async for num in async_range(0, 5):
        print(f"生成器产生：{num}")

# ─────────────────────────────────────
# 异步生成器表达式
# ─────────────────────────────────────

async def async_squares():
    """异步生成器表达式"""
    async_gen = (i * i async for i in async_range(1, 5))
    async for square in async_gen:
        print(f"平方：{square}")

# ─────────────────────────────────────
# 收集异步生成器的结果
# ─────────────────────────────────────

async def demo_async_comprehension():
    # 异步列表推导式
    squares = [i * i async for i in async_range(1, 5)]
    print(f"平方列表：{squares}")  # [1, 4, 9, 16]

    # 带条件的异步推导式
    even_squares = [i * i async for i in async_range(1, 10) if i % 2 == 0]
    print(f"偶数平方：{even_squares}")  # [4, 16, 36, 64]

# asyncio.run(demo_async_generator())
```

---

## 第五部分：实际应用场景

### 20.14 并发爬虫

```python
import asyncio
import aiohttp
from typing import List, Dict

class AsyncCrawler:
    """异步爬虫类"""

    def __init__(self, max_concurrent=10):
        self.semaphore = asyncio.Semaphore(max_concurrent)
        self.results: Dict[str, any] = {}

    async def fetch(self, session: aiohttp.ClientSession, url: str) -> Dict:
        """获取单个 URL"""
        async with self.semaphore:
            try:
                async with session.get(url, timeout=10) as response:
                    html = await response.text()
                    return {
                        "url": url,
                        "status": response.status,
                        "size": len(html),
                        "success": True
                    }
            except asyncio.TimeoutError:
                return {"url": url, "success": False, "error": "超时"}
            except Exception as e:
                return {"url": url, "success": False, "error": str(e)}

    async def crawl(self, urls: List[str]) -> List[Dict]:
        """并发爬取多个 URL"""
        async with aiohttp.ClientSession() as session:
            tasks = [self.fetch(session, url) for url in urls]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            return results

    async def crawl_with_progress(self, urls: List[str]):
        """带进度显示的爬取"""
        async with aiohttp.ClientSession() as session:
            tasks = [self.fetch(session, url) for url in urls]
            total = len(tasks)
            completed = 0

            for task in asyncio.as_completed(tasks):
                result = await task
                completed += 1
                print(f"进度：{completed}/{total} ({completed/total*100:.1f}%)")
                yield result

async def demo_crawler():
    urls = [
        "https://www.python.org",
        "https://www.github.com",
        "https://www.stackoverflow.com",
        "https://www.reddit.com",
        "https://www.wikipedia.org",
    ]

    crawler = AsyncCrawler(max_concurrent=3)
    results = await crawler.crawl(urls)

    for result in results:
        if isinstance(result, dict):
            status = "成功" if result.get("success") else f"失败：{result.get('error')}"
            print(f"{result['url']}: {status}")

# asyncio.run(demo_crawler())
```

---

### 20.15 异步 WebSocket 服务器

```python
# 需要安装：pip install websockets
import asyncio
import websockets

async def handle_client(websocket, path):
    """处理单个 WebSocket 连接"""
    print(f"客户端连接：{websocket.remote_address}")

    try:
        async for message in websocket:
            print(f"收到：{message}")

            # 处理消息
            response = f"服务器收到：{message}"

            # 发送响应
            await websocket.send(response)
    except websockets.exceptions.ConnectionClosed:
        print(f"客户端断开连接")

async def websocket_server():
    """启动 WebSocket 服务器"""
    server = await websockets.serve(
        handle_client,
        "localhost",
        8765,
        ping_interval=30,  # 每 30 秒 ping 一次
        ping_timeout=10,   # 10 秒超时
    )
    print("WebSocket 服务器启动：ws://localhost:8765")
    await server.wait_closed()

# asyncio.run(websocket_server())
```

---

### 20.16 异步数据库操作

```python
# 需要安装：pip install aiosqlite
import asyncio
import aiosqlite

async def demo_async_database():
    # 连接数据库
    async with aiosqlite.connect("demo.db") as db:
        # 创建表
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT
            )
        """)

        # 插入数据
        users = [
            ("Alice", "alice@example.com"),
            ("Bob", "bob@example.com"),
            ("Charlie", "charlie@example.com"),
        ]
        await db.executemany(
            "INSERT INTO users (name, email) VALUES (?, ?)",
            users
        )
        await db.commit()

        # 查询数据
        async with db.execute("SELECT * FROM users") as cursor:
            async for row in cursor:
                print(f"用户：{row}")

# asyncio.run(demo_async_database())
```

---

## 第六部分：高级技巧

### 20.17 优雅地关闭异步服务

```python
import asyncio
import signal

class GracefulShutdown:
    """优雅关闭服务"""

    def __init__(self):
        self.shutdown_event = asyncio.Event()
        self.tasks = []

    def handle_signal(self, sig):
        """信号处理器"""
        print(f"\n收到信号 {sig.name}，开始关闭...")
        self.shutdown_event.set()

    async def run_with_shutdown(self, coro):
        """运行协程并监听关闭信号"""
        loop = asyncio.get_running_loop()

        # 注册信号处理
        for sig in (signal.SIGINT, signal.SIGTERM):
            try:
                loop.add_signal_handler(sig, self.handle_signal, sig)
            except NotImplementedError:
                pass  # Windows 不支持

        task = asyncio.create_task(coro)
        self.tasks.append(task)

        try:
            # 等待任务完成或关闭信号
            await asyncio.wait(
                [task, asyncio.create_task(self.shutdown_event.wait())],
                return_when=asyncio.FIRST_COMPLETED
            )
        finally:
            # 取消所有任务
            for t in self.tasks:
                if not t.done():
                    t.cancel()

            # 等待任务取消完成
            if self.tasks:
                await asyncio.gather(*self.tasks, return_exceptions=True)

async def long_running_service():
    """长时间运行的服务"""
    while True:
        print("服务运行中...")
        await asyncio.sleep(1)

async def main():
    shutdown = GracefulShutdown()
    await shutdown.run_with_shutdown(long_running_service())
    print("服务已关闭")

# asyncio.run(main())
```

---

### 20.18 异步锁和同步原语

```python
import asyncio

async def demo_async_primitives():
    # ──────────────────────────────────
    # asyncio.Lock - 异步互斥锁
    # ──────────────────────────────────
    lock = asyncio.Lock()
    shared_resource = 0

    async def worker_with_lock(worker_id):
        nonlocal shared_resource
        async with lock:
            temp = shared_resource
            await asyncio.sleep(0.1)
            shared_resource = temp + 1
            print(f"Worker {worker_id}: {shared_resource}")

    await asyncio.gather(*[worker_with_lock(i) for i in range(5)])
    print(f"最终值：{shared_resource}")

    # ──────────────────────────────────
    # asyncio.Event - 异步事件
    # ──────────────────────────────────
    event = asyncio.Event()

    async def waiter(event, name):
        print(f"{name} 等待事件")
        await event.wait()
        print(f"{name} 事件触发！")

    async def setter(event):
        await asyncio.sleep(1)
        print("触发事件！")
        event.set()

    await asyncio.gather(
        waiter(event, "等待者 A"),
        waiter(event, "等待者 B"),
        setter(event)
    )

    # ──────────────────────────────────
    # asyncio.Condition - 异步条件变量
    # ──────────────────────────────────
    condition = asyncio.Condition()
    data_ready = False

    async def producer():
        nonlocal data_ready
        async with condition:
            await asyncio.sleep(1)
            data_ready = True
            print("数据已准备好")
            condition.notify_all()

    async def consumer():
        nonlocal data_ready
        async with condition:
            while not data_ready:
                print("等待数据...")
                await condition.wait()
            print("获取到数据！")

    await asyncio.gather(producer(), consumer())

    # ──────────────────────────────────
    # asyncio.Semaphore - 异步信号量
    # ──────────────────────────────────
    semaphore = asyncio.Semaphore(2)

    async def limited_worker(worker_id):
        async with semaphore:
            print(f"Worker {worker_id} 开始")
            await asyncio.sleep(0.5)
            print(f"Worker {worker_id} 完成")

    await asyncio.gather(*[limited_worker(i) for i in range(5)])

# asyncio.run(demo_async_primitives())
```

---

### 20.19 使用 asyncio.Barrier 同步点

```python
import asyncio

async def barrier_demo():
    """使用 Barrier 同步多个任务"""

    # 创建 barrier，需要 3 个任务到达才能继续
    barrier = asyncio.Barrier(3)

    async def worker(worker_id):
        print(f"Worker {worker_id} 到达 barrier")

        # 等待所有 worker 到达
        await barrier.wait()

        print(f"Worker {worker_id} 通过 barrier")

        # 做一些工作
        await asyncio.sleep(0.5)
        print(f"Worker {worker_id} 完成")

    # 3 个 worker 同时运行
    await asyncio.gather(
        worker(1),
        worker(2),
        worker(3)
    )

# asyncio.run(barrier_demo())
```

---

## 第七部分：性能优化和最佳实践

### 20.20 避免阻塞事件循环

```python
import asyncio
import time

# ─────────────────────────────────────
# ❌ 错误：阻塞事件循环
# ─────────────────────────────────────

async def bad_blocking():
    """错误示例：使用 time.sleep 阻塞"""
    print("开始")
    time.sleep(1)  # 阻塞整个事件循环 1 秒！
    print("结束")

# ─────────────────────────────────────
# ✅ 正确：使用异步等待
# ─────────────────────────────────────

async def good_nonblocking():
    """正确示例：使用 asyncio.sleep"""
    print("开始")
    await asyncio.sleep(1)  # 非阻塞，让出控制权
    print("结束")

# ─────────────────────────────────────
# CPU 密集型任务的异步处理
# ─────────────────────────────────────

def cpu_intensive_work(data):
    """CPU 密集型计算（阻塞）"""
    return sum(i * i for i in range(data))

async def process_with_executor():
    """使用线程池/进程池避免阻塞"""
    loop = asyncio.get_running_loop()

    # 在线程池运行（适合 I/O 密集型）
    result = await loop.run_in_executor(
        None,  # 使用默认线程池
        cpu_intensive_work,
        1000000
    )
    print(f"结果：{result}")

    # 在进程池运行（适合 CPU 密集型）
    with asyncio.ProcessPoolExecutor() as executor:
        result = await loop.run_in_executor(
            executor,
            cpu_intensive_work,
            1000000
        )
        print(f"进程池结果：{result}")

# asyncio.run(process_with_executor())
```

---

### 20.21 批量处理和分组

```python
import asyncio
import aiohttp

async def fetch_batch(session, url):
    """批量获取"""
    async with session.get(url) as response:
        return await response.text()

async def process_in_batches(urls, batch_size=10):
    """分批处理 URL"""
    results = []

    async with aiohttp.ClientSession() as session:
        for i in range(0, len(urls), batch_size):
            batch = urls[i:i + batch_size]
            print(f"处理批次 {i//batch_size + 1}")

            # 并发处理当前批次
            batch_results = await asyncio.gather(
                *[fetch_batch(session, url) for url in batch]
            )
            results.extend(batch_results)

            # 批次间短暂暂停，避免压垮服务器
            await asyncio.sleep(0.1)

    return results
```

---

### 20.22 超时和重试机制

```python
import asyncio
import random

async def fetch_with_retry(url, max_retries=3, backoff=1):
    """带重试和超时的获取"""
    for attempt in range(max_retries):
        try:
            # 使用 wait_for 添加超时
            async with asyncio.timeout(10):  # Python 3.11+
                # 模拟网络请求
                await asyncio.sleep(random.uniform(0.1, 0.5))
                if random.random() < 0.3:  # 30% 失败率
                    raise ConnectionError("连接失败")
                return f"成功获取 {url}"
        except asyncio.TimeoutError:
            print(f"超时（尝试 {attempt + 1}/{max_retries}）")
        except ConnectionError as e:
            print(f"错误：{e}（尝试 {attempt + 1}/{max_retries}）")

        if attempt < max_retries - 1:
            # 指数退避
            wait_time = backoff * (2 ** attempt)
            print(f"等待 {wait_time} 秒后重试")
            await asyncio.sleep(wait_time)

    raise Exception(f"重试 {max_retries} 次后仍失败")

async def main():
    try:
        result = await fetch_with_retry("https://example.com")
        print(result)
    except Exception as e:
        print(f"最终失败：{e}")

# asyncio.run(main())
```

---

## 第八部分：综合实战项目

### 20.23 异步任务调度器

```python
import asyncio
from dataclasses import dataclass
from typing import Callable, Any, Optional
from enum import Enum

class TaskStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

@dataclass
class Task:
    id: str
    func: Callable
    args: tuple = ()
    kwargs: dict = None
    status: TaskStatus = TaskStatus.PENDING
    result: Any = None
    error: Optional[Exception] = None

class AsyncTaskScheduler:
    """异步任务调度器"""

    def __init__(self, max_concurrent=5):
        self.semaphore = asyncio.Semaphore(max_concurrent)
        self.tasks: dict[str, Task] = {}
        self.queue = asyncio.PriorityQueue()
        self.results = asyncio.Queue()

    async def submit(self, task: Task, priority: int = 0):
        """提交任务"""
        self.tasks[task.id] = task
        await self.queue.put((priority, task))

    async def _execute(self, task: Task):
        """执行单个任务"""
        async with self.semaphore:
            task.status = TaskStatus.RUNNING
            print(f"执行任务：{task.id}")

            try:
                kwargs = task.kwargs or {}
                if asyncio.iscoroutinefunction(task.func):
                    result = await task.func(*task.args, **kwargs)
                else:
                    result = task.func(*task.args, **kwargs)

                task.result = result
                task.status = TaskStatus.COMPLETED
            except Exception as e:
                task.error = e
                task.status = TaskStatus.FAILED
            finally:
                await self.results.put(task)

    async def run(self):
        """运行调度器"""
        workers = []

        while not self.queue.empty():
            priority, task = await self.queue.get()
            worker = asyncio.create_task(self._execute(task))
            workers.append(worker)

        # 等待所有任务完成
        await asyncio.gather(*workers)

        # 收集结果
        results = []
        while not self.results.empty():
            results.append(await self.results.get())

        return results

# 使用示例
async def example_task(name, delay):
    await asyncio.sleep(delay)
    return f"任务 {name} 完成"

async def demo_scheduler():
    scheduler = AsyncTaskScheduler(max_concurrent=3)

    # 提交任务（优先级越低越先执行）
    await scheduler.submit(Task("t1", example_task, args=("A", 0.5)), priority=1)
    await scheduler.submit(Task("t2", example_task, args=("B", 0.3)), priority=2)
    await scheduler.submit(Task("t3", example_task, args=("C", 0.7)), priority=1)

    results = await scheduler.run()

    for task in results:
        print(f"{task.id}: {task.status.value} - {task.result or task.error}")

# asyncio.run(demo_scheduler())
```

---

## 本章总结

### 核心知识点

| 知识点 | 类/函数 | 应用场景 |
|--------|---------|----------|
| 事件循环 | `asyncio.get_event_loop()` | 手动控制异步执行 |
| 回调调度 | `call_soon()`, `call_later()` | 定时任务和回调 |
| 异步队列 | `asyncio.Queue` | 生产者 - 消费者模型 |
| 优先级队列 | `asyncio.PriorityQueue` | 任务优先级调度 |
| 任务管理 | `create_task()`, `TaskGroup` | 并发任务控制 |
| 限流 | `Semaphore` | 控制并发数量 |
| 异步迭代 | `async for`, `__aiter__` | 流式数据处理 |
| 同步原语 | `Lock`, `Event`, `Condition`, `Barrier` | 协程间同步 |

### 最佳实践

```
┌─────────────────────────────────────────┐
│         asyncio 最佳实践                │
├─────────────────────────────────────────┤
│                                         │
│  ✅ 推荐：                              │
│  • 使用 asyncio.Queue 而非 queue.Queue │
│  • 用 Semaphore 控制并发数              │
│  • 添加超时处理（asyncio.timeout）      │
│  • 使用 TaskGroup 管理任务组（3.11+）   │
│  • 优雅处理取消和关闭                   │
│  • CPU 密集型用 run_in_executor         │
│                                         │
│  ❌ 避免：                              │
│  • time.sleep() 阻塞事件循环            │
│  • 无限制的并发任务                     │
│  • 忘记处理异常和超时                   │
│  • 在不该 await 的地方 await            │
│                                         │
└─────────────────────────────────────────┘
```

### asyncio.Queue vs queue.Queue

| 特性 | asyncio.Queue | queue.Queue |
|------|---------------|-------------|
| 使用场景 | 异步协程 | 多线程 |
| put() | 协程（需 await） | 同步方法 |
| get() | 协程（需 await） | 同步方法 |
| 阻塞行为 | 让出控制权 | 阻塞线程 |
| 线程安全 | 不需要（单线程） | 需要 |

---

[上一章](./22-列表推导式.md) | [返回大纲](./00-Python学习大纲.md)
