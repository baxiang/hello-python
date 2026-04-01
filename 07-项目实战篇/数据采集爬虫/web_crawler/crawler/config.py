"""配置管理"""

import os
import random
from dataclasses import dataclass, field
from dotenv import load_dotenv

load_dotenv()


@dataclass
class Config:
    """爬虫配置"""
    
    # 请求配置
    timeout: float = field(default_factory=lambda: float(os.getenv("TIMEOUT", "10")))
    retry_times: int = field(default_factory=lambda: int(os.getenv("RETRY_TIMES", "3")))
    retry_delay: float = field(default_factory=lambda: float(os.getenv("RETRY_DELAY", "1.0")))
    
    # 延迟配置
    min_delay: float = field(default_factory=lambda: float(os.getenv("MIN_DELAY", "0.5")))
    max_delay: float = field(default_factory=lambda: float(os.getenv("MAX_DELAY", "2.0")))
    
    # 存储配置
    output_dir: str = field(default_factory=lambda: os.getenv("OUTPUT_DIR", "output"))
    output_format: str = field(default_factory=lambda: os.getenv("OUTPUT_FORMAT", "json"))
    
    # 代理配置
    proxy: str | None = field(default_factory=lambda: os.getenv("PROXY"))
    
    @staticmethod
    def get_user_agent() -> str:
        """获取随机 User-Agent"""
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
        ]
        return random.choice(user_agents)
    
    def get_headers(self) -> dict:
        """获取请求头"""
        return {
            "User-Agent": self.get_user_agent(),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
        }
    
    def get_delay(self) -> float:
        """获取随机延迟"""
        return random.uniform(self.min_delay, self.max_delay)


config = Config()