"""进度跟踪测试"""

import asyncio

import pytest

from app.core.progress import (
    AsyncProgressTracker,
    ProgressTracker,
    ThreadSafeProgress,
    create_progress_tracker,
)


class TestProgressTracker:
    def test_init(self):
        tracker = ProgressTracker(total=10)
        assert tracker.total == 10
        assert tracker.completed == 0

    def test_increment(self):
        tracker = ProgressTracker(total=10)
        tracker.increment()
        assert tracker.completed == 1
        tracker.increment(5)
        assert tracker.completed == 6

    def test_percentage(self):
        tracker = ProgressTracker(total=100)
        tracker.increment(25)
        assert tracker.percentage() == 25.0

    def test_remaining(self):
        tracker = ProgressTracker(total=10)
        tracker.increment(3)
        assert tracker.remaining() == 7

    def test_is_complete(self):
        tracker = ProgressTracker(total=5)
        tracker.increment(5)
        assert tracker.is_complete() is True

    def test_report(self):
        tracker = ProgressTracker(total=10)
        tracker.increment(3)
        report = tracker.report()
        assert "total" in report
        assert "completed" in report
        assert "remaining" in report
        assert "percentage" in report


class TestThreadSafeProgress:
    def test_init(self):
        progress = ThreadSafeProgress(total=10)
        assert progress.total == 10
        assert progress.get_completed() == 0

    def test_increment_thread_safe(self):
        progress = ThreadSafeProgress(total=100)

        from threading import Thread

        def increment_many():
            for _ in range(20):
                progress.increment()

        threads = [Thread(target=increment_many) for _ in range(5)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert progress.get_completed() == 100

    def test_set_completed(self):
        progress = ThreadSafeProgress(total=10)
        progress.set_completed(5)
        assert progress.get_completed() == 5


class TestAsyncProgressTracker:
    @pytest.mark.asyncio
    async def test_init(self):
        tracker = AsyncProgressTracker(total=10)
        assert tracker.total == 10
        assert await tracker.get_completed() == 0

    @pytest.mark.asyncio
    async def test_increment(self):
        tracker = AsyncProgressTracker(total=10)
        await tracker.increment()
        assert await tracker.get_completed() == 1

    @pytest.mark.asyncio
    async def test_increment_concurrent(self):
        tracker = AsyncProgressTracker(total=100)

        async def increment_many():
            for _ in range(20):
                await tracker.increment()

        await asyncio.gather(*[increment_many() for _ in range(5)])
        assert await tracker.get_completed() == 100


class TestCreateProgressTracker:
    def test_create_thread_safe(self):
        tracker = create_progress_tracker(total=10, thread_safe=True)
        assert isinstance(tracker, ThreadSafeProgress)

    def test_create_basic(self):
        tracker = create_progress_tracker(total=10, thread_safe=False)
        assert isinstance(tracker, ProgressTracker)
