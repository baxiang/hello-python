"""聊天服务模块"""

from openai import OpenAI
from typing import Generator, AsyncGenerator
from ..config import config


class ChatService:
    """聊天服务"""
    
    def __init__(
        self,
        api_key: str | None = None,
        base_url: str | None = None,
        model: str | None = None
    ):
        self.client = OpenAI(
            api_key=api_key or config.api_key,
            base_url=base_url or config.base_url
        )
        self.model = model or config.model
    
    def chat(
        self,
        messages: list[dict],
        temperature: float | None = None
    ) -> str:
        """发送聊天请求"""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature or config.temperature
        )
        return response.choices[0].message.content
    
    def stream_chat(
        self,
        messages: list[dict],
        temperature: float | None = None
    ) -> Generator[str, None, None]:
        """流式聊天"""
        stream = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature or config.temperature,
            stream=True
        )
        
        for chunk in stream:
            delta = chunk.choices[0].delta
            if delta.content:
                yield delta.content
    
    async def async_stream_chat(
        self,
        messages: list[dict],
        temperature: float | None = None
    ) -> AsyncGenerator[str, None]:
        """异步流式聊天"""
        from openai import AsyncOpenAI
        
        async_client = AsyncOpenAI(
            api_key=config.api_key,
            base_url=config.base_url
        )
        
        stream = await async_client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature or config.temperature,
            stream=True
        )
        
        async for chunk in stream:
            delta = chunk.choices[0].delta
            if delta.content:
                yield delta.content