"""任务定义测试"""

import time

from app.core.task import (
    DownloadResult,
    DownloadTask,
    TaskPriority,
    TaskStatus,
    create_download_task,
)


class TestDownloadTask:
    def test_init(self):
        task = DownloadTask(url="http://example.com")
        assert task.url == "http://example.com"
        assert task.status == TaskStatus.PENDING

    def test_init_with_priority(self):
        task = DownloadTask(url="http://example.com", priority=TaskPriority.HIGH)
        assert task.priority == TaskPriority.HIGH

    def test_start(self):
        task = DownloadTask(url="http://example.com")
        task.start()
        assert task.status == TaskStatus.RUNNING
        assert task.started_at is not None

    def test_complete(self):
        task = DownloadTask(url="http://example.com")
        task.start()
        task.complete({"data": "content"})
        assert task.status == TaskStatus.COMPLETED
        assert task.result is not None
        assert task.completed_at is not None

    def test_fail(self):
        task = DownloadTask(url="http://example.com")
        task.start()
        task.fail("Connection error")
        assert task.status == TaskStatus.FAILED
        assert task.error == "Connection error"

    def test_retry_count(self):
        task = DownloadTask(url="http://example.com", max_retries=3)
        assert task.max_retries == 3
        task.increment_retry()
        assert task.retry_count == 1
        assert task.can_retry() is True
        task.increment_retry()
        task.increment_retry()
        assert task.can_retry() is False

    def test_duration(self):
        task = DownloadTask(url="http://example.com")
        task.start()
        time.sleep(0.05)
        duration = task.duration()
        assert duration >= 0.05


class TestDownloadResult:
    def test_init(self):
        result = DownloadResult(url="http://example.com", success=True)
        assert result.url == "http://example.com"
        assert result.success is True

    def test_init_with_data(self):
        result = DownloadResult(
            url="http://example.com", success=True, data={"content": "abc"}
        )
        assert result.data == {"content": "abc"}

    def test_init_with_error(self):
        result = DownloadResult(
            url="http://example.com", success=False, error="timeout"
        )
        assert result.error == "timeout"


class TestTaskPriority:
    def test_priority_values(self):
        assert TaskPriority.LOW.value == 1
        assert TaskPriority.NORMAL.value == 2
        assert TaskPriority.HIGH.value == 3
        assert TaskPriority.CRITICAL.value == 4


class TestTaskStatus:
    def test_status_values(self):
        assert TaskStatus.PENDING.value == "pending"
        assert TaskStatus.RUNNING.value == "running"
        assert TaskStatus.COMPLETED.value == "completed"
        assert TaskStatus.FAILED.value == "failed"
        assert TaskStatus.CANCELLED.value == "cancelled"


class TestCreateDownloadTask:
    def test_create_basic(self):
        task = create_download_task("http://example.com")
        assert task.url == "http://example.com"
        assert task.status == TaskStatus.PENDING

    def test_create_with_priority(self):
        task = create_download_task("http://example.com", priority=TaskPriority.HIGH)
        assert task.priority == TaskPriority.HIGH