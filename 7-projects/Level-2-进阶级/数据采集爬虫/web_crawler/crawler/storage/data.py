"""数据存储"""

import json
import csv
import sqlite3
from pathlib import Path
from typing import Any
from datetime import datetime


class DataStorage:
    """数据存储"""
    
    def __init__(self, output_dir: str = "output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def save_json(self, data: list[dict] | dict, filename: str) -> str:
        """保存为 JSON"""
        filepath = self.output_dir / filename
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return str(filepath)
    
    def save_csv(self, data: list[dict], filename: str) -> str:
        """保存为 CSV"""
        if not data:
            return ""
        
        filepath = self.output_dir / filename
        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
        return str(filepath)
    
    def save_jsonl(self, data: list[dict], filename: str) -> str:
        """保存为 JSON Lines"""
        filepath = self.output_dir / filename
        with open(filepath, "w", encoding="utf-8") as f:
            for item in data:
                f.write(json.dumps(item, ensure_ascii=False) + "\n")
        return str(filepath)


class SQLiteStorage:
    """SQLite 存储"""
    
    def __init__(self, db_path: str = "crawler.db"):
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self) -> None:
        """初始化数据库"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS pages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT UNIQUE NOT NULL,
                title TEXT,
                content TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        conn.close()
    
    def save(self, url: str, title: str, content: str) -> int:
        """保存页面"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT OR REPLACE INTO pages (url, title, content)
            VALUES (?, ?, ?)
        """, (url, title, content))
        
        page_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return page_id
    
    def get_all(self) -> list[dict]:
        """获取所有数据"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM pages ORDER BY created_at DESC")
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    def search(self, keyword: str) -> list[dict]:
        """搜索"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM pages 
            WHERE title LIKE ? OR content LIKE ?
            ORDER BY created_at DESC
        """, (f"%{keyword}%", f"%{keyword}%"))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]