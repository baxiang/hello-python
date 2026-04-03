"""消息存储服务"""

import sqlite3
from datetime import datetime
from typing import Optional
from pathlib import Path


class MessageStore:
    """消息存储"""
    
    def __init__(self, db_path: str = "chat.db"):
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self) -> None:
        """初始化数据库"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                content TEXT NOT NULL,
                message_type TEXT DEFAULT 'message',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_messages_created_at 
            ON messages(created_at)
        """)
        
        conn.commit()
        conn.close()
    
    def save(
        self, 
        username: str, 
        content: str, 
        message_type: str = "message"
    ) -> int:
        """保存消息"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO messages (username, content, message_type)
            VALUES (?, ?, ?)
        """, (username, content, message_type))
        
        msg_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return msg_id
    
    def get_recent(self, limit: int = 50) -> list[dict]:
        """获取最近消息"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, username, content, message_type, created_at
            FROM messages
            ORDER BY created_at DESC
            LIMIT ?
        """, (limit,))
        
        rows = cursor.fetchall()
        conn.close()
        
        messages = []
        for row in reversed(rows):
            messages.append({
                "id": row["id"],
                "username": row["username"],
                "content": row["content"],
                "type": row["message_type"],
                "timestamp": row["created_at"]
            })
        
        return messages
    
    def search(self, keyword: str, limit: int = 50) -> list[dict]:
        """搜索消息"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, username, content, message_type, created_at
            FROM messages
            WHERE content LIKE ?
            ORDER BY created_at DESC
            LIMIT ?
        """, (f"%{keyword}%", limit))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]


# 全局消息存储
store = MessageStore()