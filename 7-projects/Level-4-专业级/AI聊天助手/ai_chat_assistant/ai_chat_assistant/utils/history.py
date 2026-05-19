"""对话历史管理"""

import json
import os
from datetime import datetime
from pathlib import Path
from ..config import config


class HistoryManager:
    """对话历史管理器"""
    
    def __init__(self, history_dir: str | None = None):
        self.history_dir = Path(history_dir or config.history_dir)
        self.history_dir.mkdir(parents=True, exist_ok=True)
        self.messages: list[dict] = []
        self.current_session: str | None = None
    
    def new_session(self, system_prompt: str | None = None) -> str:
        """创建新会话"""
        session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.current_session = session_id
        self.messages = [
            {"role": "system", "content": system_prompt or config.system_prompt}
        ]
        self.save()
        return session_id
    
    def add_message(self, role: str, content: str) -> None:
        """添加消息"""
        self.messages.append({"role": role, "content": content})
    
    def get_messages(self) -> list[dict]:
        """获取所有消息"""
        return self.messages.copy()
    
    def trim(self, max_messages: int | None = None) -> None:
        """裁剪历史记录"""
        max_msg = max_messages or config.max_history
        if len(self.messages) > max_msg:
            system = self.messages[0] if self.messages[0]["role"] == "system" else None
            recent = self.messages[-(max_msg - 1):]
            self.messages = [system] + recent if system else recent
    
    def save(self) -> None:
        """保存当前会话"""
        if not self.current_session:
            return
        
        filepath = self.history_dir / f"{self.current_session}.json"
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(self.messages, f, ensure_ascii=False, indent=2)
    
    def load(self, session_id: str) -> list[dict]:
        """加载历史会话"""
        filepath = self.history_dir / f"{session_id}.json"
        with open(filepath, "r", encoding="utf-8") as f:
            self.messages = json.load(f)
        self.current_session = session_id
        return self.messages
    
    def list_sessions(self) -> list[str]:
        """列出所有会话"""
        sessions = []
        for f in self.history_dir.glob("*.json"):
            sessions.append(f.stem)
        return sorted(sessions, reverse=True)
    
    def clear(self) -> None:
        """清空当前会话"""
        self.messages = []
        self.current_session = None