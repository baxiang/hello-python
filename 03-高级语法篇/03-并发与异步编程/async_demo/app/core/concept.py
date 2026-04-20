"""并发概念演示 - ch01"""

import asyncio
import time
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from dataclasses import dataclass
from multiprocessing import cpu_count
from threading import Thread


def _cpu_bound_worker(n: int) -> int:
    """CPU密集型工作函数 - 模块级函数以便pickle"""
    result = 0
    for i in range(n):
        result += i
    return result


def _simple_worker(task_id: int) -> int:
    """简单工作函数 - 模块级函数以便pickle"""
    return task_id


@dataclass
class TaskClassification:
    task_type: str
    recommended: str
    reason: str


class ConceptDemo:
    """并发概念演示类"""

    def __init__(self, name: str = "ConceptDemo"):
        self.name = name

    def show_threading_basics(self) -> dict:
        """演示线程基础"""
        results = []

        def worker(task_id: int):
            time.sleep(0.01)
            results.append(task_id)

        threads = [Thread(target=worker, args=(i,)) for i in range(3)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        return {"threads_created": len(threads), "results": results}

    def show_multiprocessing_basics(self) -> dict:
        """演示进程基础"""
        with ProcessPoolExecutor(max_workers=2) as executor:
            list(executor.map(_simple_worker, [0, 1]))

        return {"processes_created": 2, "cpu_count": cpu_count()}

    def show_async_basics(self) -> dict:
        """演示异步基础"""

        async def worker(task_id: int):
            await asyncio.sleep(0.01)
            return task_id

        async def run():
            tasks = [worker(i) for i in range(3)]
            results = await asyncio.gather(*tasks)
            return results

        results = asyncio.run(run())
        return {"coroutines_created": len(results), "results": results}


def classify_task(task_name: str) -> dict:
    """根据任务名分类任务类型"""
    cpu_intensive_keywords = [
        "compute",
        "calculate",
        "process_image",
        "encode",
        "decode",
        "compress",
        "encrypt",
    ]
    io_intensive_keywords = [
        "download",
        "upload",
        "read_file",
        "write_file",
        "network",
        "request",
        "database",
    ]

    task_lower = task_name.lower()

    for keyword in cpu_intensive_keywords:
        if keyword in task_lower:
            return {
                "type": "cpu_intensive",
                "recommended": "multiprocessing",
                "reason": f"CPU密集型任务，关键词'{keyword}'匹配",
            }

    for keyword in io_intensive_keywords:
        if keyword in task_lower:
            return {
                "type": "io_intensive",
                "recommended": "asyncio",
                "reason": f"IO密集型任务，关键词'{keyword}'匹配",
            }

    return {
        "type": "mixed",
        "recommended": "hybrid",
        "reason": "混合型任务，需根据具体场景选择",
    }


def demo_gil_impact(iterations: int = 100000) -> dict:
    """演示GIL对多线程的影响"""
    thread_count = 2
    chunk = iterations // thread_count

    start = time.time()
    with ThreadPoolExecutor(max_workers=thread_count) as executor:
        list(executor.map(_cpu_bound_worker, [chunk] * thread_count))
    thread_time = time.time() - start

    start = time.time()
    with ProcessPoolExecutor(max_workers=thread_count) as executor:
        list(executor.map(_cpu_bound_worker, [chunk] * thread_count))
    process_time = time.time() - start

    return {
        "iterations": iterations,
        "thread_time": round(thread_time, 4),
        "process_time": round(process_time, 4),
        "speedup": round(thread_time / process_time, 2) if process_time > 0 else 0,
        "conclusion": "多进程在CPU密集型任务上通常更快",
    }


def explain_concurrency_vs_parallelism() -> dict:
    """解释并发与并行的区别"""
    return {
        "definition": {
            "concurrency": "多个任务在同一时间段内交替执行（单核也可以）",
            "parallelism": "多个任务在同一时刻同时执行（需要多核）",
        },
        "example": {
            "concurrency": "单核CPU上切换执行多个线程",
            "parallelism": "多核CPU上每个核心执行一个线程",
        },
        "python_context": {
            "threading": "并发（受GIL限制，同一时刻只有一个线程执行Python字节码）",
            "multiprocessing": "并行（每个进程有自己的Python解释器和GIL）",
            "asyncio": "并发（单线程事件循环，适合IO密集型）",
        },
        "when_to_use": {
            "threading": "IO密集型任务，如网络请求、文件读写",
            "multiprocessing": "CPU密集型任务，如计算、图像处理",
            "asyncio": "高并发IO任务，如大量网络请求",
        },
    }
