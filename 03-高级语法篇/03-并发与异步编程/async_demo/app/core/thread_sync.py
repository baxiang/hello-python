"""线程同步机制 - ch03"""

import time
from dataclasses import dataclass, field
from threading import Barrier, Condition, Event, Lock, RLock, Semaphore, Thread
from typing import Any


class LockDemo:
    """Lock演示 - 基本互斥锁"""

    def __init__(self):
        self._lock = Lock()
        self._counter = 0

    def demo_lock(self) -> dict:
        """演示使用Lock防止竞态条件"""
        self._counter = 0
        iterations = 1000

        def increment_with_lock():
            for _ in range(iterations):
                with self._lock:
                    self._counter += 1

        threads = [Thread(target=increment_with_lock) for _ in range(5)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        expected = 5 * iterations
        return {
            "final_value": self._counter,
            "expected": expected,
            "race_condition": self._counter != expected,
        }

    def demo_without_lock(self) -> dict:
        """演示不使用Lock的竞态条件"""
        self._counter = 0
        iterations = 1000

        def increment_without_lock():
            for _ in range(iterations):
                self._counter += 1

        threads = [Thread(target=increment_without_lock) for _ in range(5)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        expected = 5 * iterations
        return {
            "final_value": self._counter,
            "expected": expected,
            "race_condition": self._counter != expected,
        }


class RLockDemo:
    """RLock演示 - 可重入锁"""

    def __init__(self):
        self._rlock = RLock()
        self._acquired_count = 0

    def demo_rlock(self) -> dict:
        """演示RLock的可重入特性"""
        with self._rlock:
            self._acquired_count += 1
            with self._rlock:
                self._acquired_count += 1

        return {
            "success": True,
            "acquired_count": self._acquired_count,
        }

    def nested_lock_calls(self) -> dict:
        """演示嵌套调用"""
        with self._rlock:
            self._outer_method()

        return {"success": True}

    def _outer_method(self):
        with self._rlock:
            self._inner_method()

    def _inner_method(self):
        with self._rlock:
            pass


class SemaphoreDemo:
    """Semaphore演示 - 信号量限流"""

    def __init__(self, max_concurrent: int = 3):
        self._semaphore = Semaphore(max_concurrent)
        self._max_concurrent = max_concurrent
        self._current_concurrent = 0
        self._max_observed = 0
        self._lock = Lock()

    def demo_semaphore(self) -> dict:
        """演示Semaphore限制并发数"""
        self._current_concurrent = 0
        self._max_observed = 0
        completed = 0
        completion_lock = Lock()

        def worker(worker_id: int):
            nonlocal completed
            with self._semaphore:
                with self._lock:
                    self._current_concurrent += 1
                    self._max_observed = max(
                        self._max_observed, self._current_concurrent
                    )

                time.sleep(0.01)

                with self._lock:
                    self._current_concurrent -= 1

                with completion_lock:
                    completed += 1

        threads = [Thread(target=worker, args=(i,)) for i in range(6)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        return {
            "success": True,
            "max_concurrent": self._max_observed,
            "total_tasks": 6,
            "completed_tasks": completed,
        }


class EventDemo:
    """Event演示 - 事件通知"""

    def __init__(self):
        self._event = Event()

    def demo_event(self) -> dict:
        """演示Event的通知机制"""
        results = {"waiters_notified": 0, "event_triggered": False}

        def waiter():
            self._event.wait()
            with self._lock:
                results["waiters_notified"] += 1

        self._lock = Lock()
        threads = [Thread(target=waiter) for _ in range(3)]
        for t in threads:
            t.start()

        time.sleep(0.05)
        self._event.set()
        results["event_triggered"] = True

        for t in threads:
            t.join()

        return results

    def wait_with_timeout(self, timeout: float) -> dict:
        """演示带超时的等待"""
        self._event.clear()
        result = self._event.wait(timeout=timeout)
        return {"timed_out": not result}


class ConditionDemo:
    """Condition演示 - 条件变量"""

    def __init__(self):
        self._condition = Condition()
        self._items: list[Any] = []
        self._producer_done = False

    def demo_condition(self) -> dict:
        """演示Condition的生产者-消费者模式"""
        results = {"items_consumed": 0, "producer_done": False, "consumer_done": False}

        def producer():
            for i in range(5):
                with self._condition:
                    self._items.append(i)
                    self._condition.notify()
                time.sleep(0.01)

            with self._condition:
                self._producer_done = True
                self._condition.notify_all()

            results["producer_done"] = True

        def consumer():
            consumed = 0
            while True:
                with self._condition:
                    while not self._items and not self._producer_done:
                        self._condition.wait()

                    if not self._items and self._producer_done:
                        break

                    while self._items:
                        self._items.pop()
                        consumed += 1

            results["items_consumed"] = consumed
            results["consumer_done"] = True

        producer_thread = Thread(target=producer)
        consumer_thread = Thread(target=consumer)

        producer_thread.start()
        consumer_thread.start()

        producer_thread.join()
        consumer_thread.join()

        return results

    def producer_consumer_demo(self, items: int = 5) -> dict:
        """完整的生产者-消费者演示"""
        results = {"items_produced": 0, "items_consumed": 0}

        def producer():
            for i in range(items):
                with self._condition:
                    self._items.append(i)
                    results["items_produced"] += 1
                    self._condition.notify()

            with self._condition:
                self._producer_done = True
                self._condition.notify_all()

        def consumer():
            while True:
                with self._condition:
                    while not self._items and not self._producer_done:
                        self._condition.wait()

                    if not self._items and self._producer_done:
                        break

                    while self._items:
                        self._items.pop()
                        results["items_consumed"] += 1

        producer_thread = Thread(target=producer)
        consumer_thread = Thread(target=consumer)

        producer_thread.start()
        consumer_thread.start()

        producer_thread.join()
        consumer_thread.join()

        return results


class BarrierDemo:
    """Barrier演示 - 屏障同步"""

    def __init__(self, parties: int = 3):
        self._barrier = Barrier(parties)
        self._parties = parties

    def demo_barrier(self) -> dict:
        """演示Barrier同步多个线程"""
        arrival_times: list[float] = []
        lock = Lock()

        def worker():
            arrival = time.time()
            with lock:
                arrival_times.append(arrival)
            self._barrier.wait()

        threads = [Thread(target=worker) for _ in range(self._parties)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        time_diff = max(arrival_times) - min(arrival_times)
        return {
            "all_arrived": True,
            "arrival_times": arrival_times,
            "max_time_diff": round(time_diff, 4),
        }


@dataclass
class ThreadSafeCounter:
    """线程安全计数器"""

    _value: int = 0
    _lock: Lock = field(default_factory=Lock)

    def increment(self) -> int:
        with self._lock:
            self._value += 1
            return self._value

    def decrement(self) -> int:
        with self._lock:
            self._value -= 1
            return self._value

    def get(self) -> int:
        with self._lock:
            return self._value

    def set_value(self, value: int) -> None:
        with self._lock:
            self._value = value

    @property
    def lock(self) -> Lock:
        return self._lock