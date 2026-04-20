"""模拟下载服务器"""

import asyncio
import random
import time
from dataclasses import dataclass
from typing import Any


@dataclass
class MockServerConfig:
    """模拟服务器配置"""

    response_time: float = 0.1
    failure_rate: float = 0.0
    max_response_size: int = 1024


class MockDownloadServer:
    """模拟下载服务器"""

    def __init__(self, config: MockServerConfig | None = None):
        self.config = config or MockServerConfig()
        self._request_count = 0
        self._successful_count = 0
        self._failed_count = 0

    def download(self, url: str) -> dict[str, Any]:
        """模拟同步下载"""
        self._request_count += 1

        if random.random() < self.config.failure_rate:
            self._failed_count += 1
            return {
                "url": url,
                "success": False,
                "error": "Simulated download failure",
                "status": 500,
            }

        time.sleep(self.config.response_time)

        self._successful_count += 1
        content = self._generate_content(url)

        return {
            "url": url,
            "success": True,
            "content": content,
            "size": len(content),
            "status": 200,
            "response_time": self.config.response_time,
        }

    async def async_download(self, url: str) -> dict[str, Any]:
        """模拟异步下载"""
        self._request_count += 1

        if random.random() < self.config.failure_rate:
            self._failed_count += 1
            return {
                "url": url,
                "success": False,
                "error": "Simulated download failure",
                "status": 500,
            }

        await asyncio.sleep(self.config.response_time)

        self._successful_count += 1
        content = self._generate_content(url)

        return {
            "url": url,
            "success": True,
            "content": content,
            "size": len(content),
            "status": 200,
            "response_time": self.config.response_time,
        }

    def _generate_content(self, url: str) -> str:
        """生成模拟内容"""
        size = min(
            self.config.max_response_size,
            random.randint(100, self.config.max_response_size),
        )
        return f"Content from {url}: " + "x" * (
            size - len(f"Content from {url}: ")
        )

    def get_stats(self) -> dict[str, int]:
        """获取统计"""
        return {
            "total_requests": self._request_count,
            "successful": self._successful_count,
            "failed": self._failed_count,
        }

    def reset_stats(self) -> None:
        """重置统计"""
        self._request_count = 0
        self._successful_count = 0
        self._failed_count = 0


def create_mock_server(
    response_time: float = 0.1,
    failure_rate: float = 0.0,
) -> MockDownloadServer:
    """创建模拟服务器"""
    config = MockServerConfig(
        response_time=response_time,
        failure_rate=failure_rate,
    )
    return MockDownloadServer(config)


def mock_download_function(url: str) -> dict[str, Any]:
    """模块级mock下载函数"""
    time.sleep(0.01)
    return {"url": url, "success": True, "content": f"Mock content for {url}"}


async def async_mock_download_function(url: str) -> dict[str, Any]:
    """模块级异步mock下载函数"""
    await asyncio.sleep(0.01)
    return {"url": url, "success": True, "content": f"Mock content for {url}"}
