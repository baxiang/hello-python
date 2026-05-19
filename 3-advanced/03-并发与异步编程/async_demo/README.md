# 并发下载器 (downloader)

Python 并发与异步编程示例项目 - 完整的并发下载工具，覆盖6章知识点。

## 项目结构

```
async_demo/
├── app/
│   ├── core/
│   │   ├── concept.py           # ch01: 并发概念演示
│   │   ├── thread_downloader.py # ch02: 多线程下载
│   │   ├── thread_sync.py       # ch03: 线程同步
│   │   ├── process_downloader.py # ch04: 多进程下载
│   │   ├── async_downloader.py  # ch05: 异步下载
│   │   ├── strategy.py          # ch06: 策略选择
│   │   ├── task.py              # 任务定义
│   │   └── progress.py          # 进度跟踪
│   └── utils/
│       ├── helpers.py           # 辅助函数
│       └── mock_server.py       # 模拟服务器
├── tests/                       # pytest测试
└── sample_urls.txt              # 示例URL列表
```

## 安装

```bash
uv sync
```

## 知识点覆盖

### ch01 并发概念 (concept.py)

- 并发 vs 并行概念演示
- CPU密集 vs IO密集任务分类
- GIL影响演示
- threading/multiprocessing/asyncio对比

```python
from app.core import ConceptDemo, classify_task, demo_gil_impact

demo = ConceptDemo()
demo.show_threading_basics()
demo.show_multiprocessing_basics()
demo.show_async_basics()

classify_task("download_file")  # 返回: io_intensive
classify_task("compute_primes") # 返回: cpu_intensive

demo_gil_impact(iterations=10000)  # 对比线程/进程性能
```

### ch02 多线程下载 (thread_downloader.py)

- Thread创建线程
- ThreadPoolExecutor线程池
- submit/map任务提交
- as_completed结果收集

```python
from app.core import ThreadDownloader, download_with_thread_pool

downloader = ThreadDownloader(max_workers=10)
downloader.submit_task(download_fn, url)
results = downloader.map_tasks(download_fn, urls)

download_with_thread_pool(download_fn, urls, max_workers=5)
```

### ch03 线程同步 (thread_sync.py)

- Lock线程安全
- RLock可重入锁
- Semaphore限流
- Event通知
- Condition条件变量
- Barrier屏障

```python
from app.core import LockDemo, SemaphoreDemo, ThreadSafeCounter

lock_demo = LockDemo()
lock_demo.demo_lock()  # 演示竞态条件防护

semaphore = SemaphoreDemo(max_concurrent=3)
semaphore.demo_semaphore()  # 演示限流

counter = ThreadSafeCounter()
counter.increment()  # 线程安全计数
```

### ch04 多进程下载 (process_downloader.py)

- Process创建进程
- ProcessPoolExecutor进程池
- Queue进程间通信
- Value/Array共享内存
- Manager共享对象

```python
from app.core import ProcessDownloader, shared_queue_demo

downloader = ProcessDownloader(max_workers=4)
results = downloader.map_tasks(cpu_task, data)

shared_queue_demo(items=10)  # 演示Queue通信
shared_value_demo(increment_by=100)  # 演示Value共享
```

### ch05 异步下载 (async_downloader.py)

- async/await定义协程
- asyncio.run/gather
- asyncio.Queue/Lock/Semaphore
- async for/async with
- asyncio.wait_for超时

```python
from app.core import AsyncDownloader, async_download_with_gather

async def main():
    downloader = AsyncDownloader(max_concurrent=10)
    results = await downloader.download_multiple(download_fn, urls)
    
    # 或使用gather
    results = await async_download_with_gather(download_fn, urls)

asyncio.run(main())
```

### ch06 策略选择 (strategy.py)

- 线程/进程/协程场景判断
- Benchmark性能对比
- 模型自动选择

```python
from app.core import StrategySelector, choose_strategy, ConcurrencyStrategy

selector = StrategySelector()
selector.choose_for_task("download_file")  # ASYNCIO
selector.choose_for_task("compute_data")   # MULTIPROCESSING

choose_strategy(task_type="io_intensive", concurrent_count=1000)  # ASYNCIO
```

## 运行测试

```bash
uv run pytest -v
uv run pytest tests/test_async_downloader.py -v
```

## 使用示例

```python
import asyncio
from app.core import (
    ThreadDownloader,
    ProcessDownloader,
    AsyncDownloader,
    choose_strategy,
)
from app.utils import MockDownloadServer, Timer

server = MockDownloadServer()
urls = ["http://example.com/file1", "http://example.com/file2"]

strategy = choose_strategy(task_type="io_intensive", concurrent_count=len(urls))

if strategy == "asyncio":
    downloader = AsyncDownloader()
    results = asyncio.run(downloader.download_multiple(server.async_download, urls))
elif strategy == "threading":
    downloader = ThreadDownloader()
    results = downloader.map_tasks(server.download, urls)
else:
    downloader = ProcessDownloader()
    results = downloader.map_tasks(server.download, urls)

print(results)
```

## Ruff检查

```bash
uv run ruff check .
uv run ruff check --fix .
```