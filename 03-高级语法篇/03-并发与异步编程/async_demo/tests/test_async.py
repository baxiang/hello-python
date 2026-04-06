"""异步测试"""

import asyncio
from app.core.async_ops import async_task, run_concurrent_tasks


def test_async_task():
    async def run():
        result = await async_task("test", 0.1)
        assert result["name"] == "test"
        assert result["delay"] == 0.1
    
    asyncio.run(run())


def test_run_concurrent_tasks():
    async def run():
        tasks = [("task1", 0.1), ("task2", 0.1)]
        results = await run_concurrent_tasks(tasks)
        assert len(results) == 2
    
    asyncio.run(run())