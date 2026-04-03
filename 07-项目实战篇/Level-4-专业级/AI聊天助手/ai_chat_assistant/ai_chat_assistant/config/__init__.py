"""配置管理模块"""

import os
from dataclasses import dataclass, field
from dotenv import load_dotenv

load_dotenv()


@dataclass
class Config:
    """应用配置"""
    
    # API 配置
    api_key: str = field(default_factory=lambda: os.getenv("OPENAI_API_KEY", ""))
    base_url: str | None = field(default_factory=lambda: os.getenv("BASE_URL") or None)
    model: str = field(default_factory=lambda: os.getenv("MODEL", "gpt-4o-mini"))
    
    # 对话配置
    system_prompt: str = field(
        default_factory=lambda: os.getenv(
            "SYSTEM_PROMPT", 
            "你是一个友好的 AI 助手，用中文回答问题。"
        )
    )
    max_history: int = field(default_factory=lambda: int(os.getenv("MAX_HISTORY", "20")))
    temperature: float = field(default_factory=lambda: float(os.getenv("TEMPERATURE", "0.7")))
    
    # 存储配置
    history_dir: str = field(default_factory=lambda: os.getenv("HISTORY_DIR", ".chat_history"))
    
    def validate(self) -> None:
        """验证配置"""
        if not self.api_key:
            raise ValueError("请设置 OPENAI_API_KEY 环境变量")


# 全局配置实例
config = Config()