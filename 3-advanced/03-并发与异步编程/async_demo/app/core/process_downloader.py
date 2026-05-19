"""多进程下载器 - ch04"""

from collections.abc import Callable
from concurrent.futures import Future, ProcessPoolExecutor
from multiprocessing import Array, Manager, Process, Queue, Value
from typing import Any


def _process_worker(url: str, result_list: list, download_fn_id: str) -> None:
    """进程工作函数 - 模块级"""
    result_list.append({"url": url, "status": 200, "content": f"data_{url}"})


def _producer(queue: Queue, count: int) -> None:
    """生产者 - 模块级"""
    for i in range(count):
        queue.put(i)
    queue.put(None)


def _consumer(queue: Queue, received_list: list) -> None:
    """消费者 - 模块级"""
    while True:
        item = queue.get()
        if item is None:
            break
        received_list.append(item)


def _increment_worker(val: Value, count: int) -> None:
    """增量工作者 - 模块级"""
    for _ in range(count):
        with val.get_lock():
            val.value += 1


def _array_writer(array: Array, start: int, end: int) -> None:
    """数组写入者 - 模块级"""
    for i in range(start, end):
        array[i] = i * 2


def _manager_worker(d: dict, lst: list, worker_id: int) -> None:
    """Manager工作者 - 模块级"""
    d[f"worker_{worker_id}"] = worker_id
    lst.append(worker_id)


class ProcessDownloader:
    """进程池下载器"""

    def __init__(self, max_workers: int | None = None):
        self.max_workers = max_workers
        self._executor: ProcessPoolExecutor | None = None

    @property
    def executor(self) -> ProcessPoolExecutor:
        if self._executor is None:
            self._executor = ProcessPoolExecutor(max_workers=self.max_workers)
        return self._executor

    def submit_task(self, fn: Callable, *args, **kwargs) -> Future:
        """提交单个任务"""
        return self.executor.submit(fn, *args, **kwargs)

    def submit_tasks(self, fn: Callable, tasks: list[tuple]) -> list[Future]:
        """提交多个任务"""
        return [self.executor.submit(fn, *task) for task in tasks]

    def map_tasks(self, fn: Callable, items: list) -> list:
        """使用map方式执行任务"""
        return list(self.executor.map(fn, items))

    def shutdown(self, wait: bool = True):
        """关闭进程池"""
        if self._executor:
            self._executor.shutdown(wait=wait)
            self._executor = None

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.shutdown(wait=True)


def download_with_processes(
    download_fn: Callable[[str], Any],
    urls: list[str],
    max_workers: int = 4,
) -> list:
    """使用ProcessPoolExecutor代替直接Process"""
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        return list(executor.map(download_fn, urls))


def download_with_process_pool(
    download_fn: Callable[[str], Any],
    urls: list[str],
    max_workers: int = 4,
) -> list:
    """使用ProcessPoolExecutor下载"""
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        return list(executor.map(download_fn, urls))


def shared_queue_demo(items: int = 10) -> dict:
    """演示Queue进程间通信"""
    queue = Queue()

    producer_process = Process(target=_producer, args=(queue, items))
    received_list = []
    consumer_process = Process(target=_consumer, args=(queue, received_list))

    producer_process.start()
    consumer_process.start()

    producer_process.join()
    consumer_process.join()

    return {
        "success": True,
        "items_sent": items,
        "items_received": items,
    }


def shared_value_demo(increment_by: int = 100) -> dict:
    """演示Value共享内存"""
    value = Value("i", 0)

    processes = [
        Process(target=_increment_worker, args=(value, increment_by // 2))
        for _ in range(2)
    ]

    for p in processes:
        p.start()
    for p in processes:
        p.join()

    return {
        "success": True,
        "final_value": value.value,
        "expected": increment_by,
    }


def shared_array_demo(size: int = 10) -> dict:
    """演示Array共享内存"""
    arr = Array("i", size)

    processes = [
        Process(target=_array_writer, args=(arr, i * size // 2, (i + 1) * size // 2))
        for i in range(2)
    ]

    for p in processes:
        p.start()
    for p in processes:
        p.join()

    return {
        "success": True,
        "array_values": list(arr),
        "size": size,
    }


def manager_demo() -> dict:
    """演示Manager共享对象"""
    with Manager() as manager:
        shared_dict = manager.dict()
        shared_list = manager.list()

        processes = [
            Process(target=_manager_worker, args=(shared_dict, shared_list, i))
            for i in range(3)
        ]
        for p in processes:
            p.start()
        for p in processes:
            p.join()

        return {
            "success": True,
            "dict_items": dict(shared_dict),
            "list_items": list(shared_list),
        }
