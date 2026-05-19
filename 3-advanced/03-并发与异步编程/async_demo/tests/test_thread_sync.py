"""线程同步测试"""

import time
from threading import Thread

from app.core.thread_sync import (
    BarrierDemo,
    ConditionDemo,
    EventDemo,
    LockDemo,
    RLockDemo,
    SemaphoreDemo,
    ThreadSafeCounter,
)


class TestLockDemo:
    def test_lock_demo_basic(self):
        demo = LockDemo()
        result = demo.demo_lock()
        assert result["final_value"] == result["expected"]
        assert result["race_condition"] is False

    def test_lock_demo_without_lock(self):
        demo = LockDemo()
        result = demo.demo_without_lock()
        assert result["race_condition"] == (result["final_value"] != result["expected"])


class TestRLockDemo:
    def test_rlock_reentrant(self):
        demo = RLockDemo()
        result = demo.demo_rlock()
        assert result["success"] is True
        assert result["acquired_count"] == 2

    def test_rlock_nested_calls(self):
        demo = RLockDemo()
        result = demo.nested_lock_calls()
        assert result["success"] is True


class TestSemaphoreDemo:
    def test_semaphore_limit(self):
        demo = SemaphoreDemo(max_concurrent=2)
        result = demo.demo_semaphore()
        assert result["max_concurrent"] <= 2
        assert result["total_tasks"] == result["completed_tasks"]

    def test_semaphore_demo_basic(self):
        demo = SemaphoreDemo(max_concurrent=3)
        result = demo.demo_semaphore()
        assert result["success"] is True


class TestEventDemo:
    def test_event_demo(self):
        demo = EventDemo()
        result = demo.demo_event()
        assert result["event_triggered"] is True
        assert result["waiters_notified"] > 0

    def test_event_wait_timeout(self):
        demo = EventDemo()
        result = demo.wait_with_timeout(timeout=0.1)
        assert result["timed_out"] is True


class TestConditionDemo:
    def test_condition_demo(self):
        demo = ConditionDemo()
        result = demo.demo_condition()
        assert result["producer_done"] is True
        assert result["consumer_done"] is True
        assert result["items_consumed"] > 0

    def test_condition_producer_consumer(self):
        demo = ConditionDemo()
        result = demo.producer_consumer_demo(items=5)
        assert result["items_produced"] == 5
        assert result["items_consumed"] == 5


class TestBarrierDemo:
    def test_barrier_demo(self):
        demo = BarrierDemo(parties=3)
        result = demo.demo_barrier()
        assert result["all_arrived"] is True
        assert len(result["arrival_times"]) == 3

    def test_barrier_waits_for_all(self):
        demo = BarrierDemo(parties=2)
        start = time.time()
        demo.demo_barrier()
        elapsed = time.time() - start
        assert elapsed < 0.5


class TestThreadSafeCounter:
    def test_counter_basic(self):
        counter = ThreadSafeCounter()
        assert counter.get() == 0
        counter.increment()
        assert counter.get() == 1
        counter.decrement()
        assert counter.get() == 0

    def test_counter_thread_safe(self):
        counter = ThreadSafeCounter()

        def increment_many():
            for _ in range(1000):
                counter.increment()

        threads = [Thread(target=increment_many) for _ in range(5)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert counter.get() == 5000

    def test_counter_with_lock(self):
        counter = ThreadSafeCounter()
        results = []

        def worker():
            old = counter._value
            time.sleep(0.001)
            counter.set_value(old + 1)
            results.append(counter.get())

        threads = [Thread(target=worker) for _ in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert len(results) == 10
