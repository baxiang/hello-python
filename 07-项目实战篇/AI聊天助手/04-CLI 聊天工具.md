# CLI 聊天工具

使用命令行界面实现一个完整的 AI 聊天工具。

---

## 1. 项目结构

```
ai-chat-cli/
├── main.py           # 主程序入口
├── chat.py           # 聊天核心逻辑
├── config.py         # 配置管理
├── history.py        # 历史记录管理
├── .env              # API Key 配置
└── requirements.txt  # 依赖列表
```

---

## 2. 核心代码实现

### 2.1 配置管理 (config.py)

```python
import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Config:
    """应用配置"""
    api_key: str = os.getenv("OPENAI_API_KEY", "")
    model: str = os.getenv("MODEL", "gpt-4o-mini")
    base_url: str = os.getenv("BASE_URL", None)  # 自定义 API 地址
    system_prompt: str = os.getenv(
        "SYSTEM_PROMPT", 
        "你是一个友好的助手，用中文回答问题"
    )
    max_history: int = int(os.getenv("MAX_HISTORY", "20"))
    
    def validate(self):
        if not self.api_key:
            raise ValueError("请设置 OPENAI_API_KEY 环境变量")
```

### 2.2 历史记录管理 (history.py)

```python
import json
import os
from datetime import datetime
from typing import List, Dict

class HistoryManager:
    def __init__(self, save_dir: str = ".chat_history"):
        self.save_dir = save_dir
        os.makedirs(save_dir, exist_ok=True)
        self.current_session: List[Dict] = []
        self.current_file: str = None
    
    def new_session(self, system_prompt: str):
        """开始新会话"""
        self.current_session = [
            {"role": "system", "content": system_prompt}
        ]
        self.current_file = datetime.now().strftime("%Y%m%d_%H%M%S.json")
    
    def add_message(self, role: str, content: str):
        """添加消息"""
        self.current_session.append({"role": role, "content": content})
    
    def trim(self, max_messages: int):
        """裁剪历史记录"""
        if len(self.current_session) > max_messages:
            system = self.current_session[0]
            recent = self.current_session[-(max_messages-1):]
            self.current_session = [system] + recent
    
    def save(self):
        """保存当前会话"""
        if self.current_file:
            filepath = os.path.join(self.save_dir, self.current_file)
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(self.current_session, f, ensure_ascii=False, indent=2)
    
    def load(self, filename: str):
        """加载历史会话"""
        filepath = os.path.join(self.save_dir, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            self.current_session = json.load(f)
        self.current_file = filename
    
    def list_sessions(self) -> List[str]:
        """列出所有会话"""
        files = sorted(os.listdir(self.save_dir), reverse=True)
        return [f for f in files if f.endswith(".json")]
```

### 2.3 聊天核心 (chat.py)

```python
from openai import OpenAI
from typing import Generator, List, Dict

class ChatEngine:
    def __init__(self, api_key: str, model: str, base_url: str = None):
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.model = model
    
    def stream_chat(
        self, 
        messages: List[Dict],
        temperature: float = 0.7
    ) -> Generator[str, None, None]:
        """流式聊天"""
        stream = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
            stream=True
        )
        
        for chunk in stream:
            delta = chunk.choices[0].delta
            if delta.content:
                yield delta.content
    
    def chat(
        self, 
        messages: List[Dict],
        temperature: float = 0.7
    ) -> str:
        """普通聊天"""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature
        )
        return response.choices[0].message.content
```

### 2.4 主程序 (main.py)

```python
#!/usr/bin/env python3
"""
AI 聊天 CLI 工具
"""
import sys
from config import Config
from chat import ChatEngine
from history import HistoryManager

# ANSI 颜色代码
class Colors:
    USER = "\033[92m"      # 绿色
    ASSISTANT = "\033[94m" # 蓝色
    SYSTEM = "\033[93m"    # 黄色
    ERROR = "\033[91m"     # 红色
    RESET = "\033[0m"

def print_user(text: str):
    print(f"{Colors.USER}你: {text}{Colors.RESET}")

def print_assistant(text: str):
    print(f"{Colors.ASSISTANT}AI: {text}{Colors.RESET}", end="", flush=True)

def print_system(text: str):
    print(f"{Colors.SYSTEM}[系统] {text}{Colors.RESET}")

def print_error(text: str):
    print(f"{Colors.ERROR}[错误] {text}{Colors.RESET}")

def print_help():
    """打印帮助信息"""
    help_text = """
命令列表:
  /help      显示帮助
  /new       开始新会话
  /history   显示历史会话
  /load <n>  加载第 n 个历史会话
  /clear     清屏
  /quit      退出程序
"""
    print(help_text)

def main():
    # 初始化
    config = Config()
    config.validate()
    
    chat = ChatEngine(
        api_key=config.api_key,
        model=config.model,
        base_url=config.base_url
    )
    
    history = HistoryManager()
    history.new_session(config.system_prompt)
    
    print_system("AI 聊天工具已启动，输入 /help 查看命令")
    
    while True:
        try:
            # 读取用户输入
            user_input = input("\n你: ").strip()
            
            if not user_input:
                continue
            
            # 处理命令
            if user_input.startswith("/"):
                cmd = user_input.lower()
                
                if cmd == "/quit" or cmd == "/exit":
                    history.save()
                    print_system("再见！")
                    break
                    
                elif cmd == "/help":
                    print_help()
                    
                elif cmd == "/new":
                    history.save()
                    history.new_session(config.system_prompt)
                    print_system("已开始新会话")
                    
                elif cmd == "/history":
                    sessions = history.list_sessions()
                    if sessions:
                        print("历史会话:")
                        for i, s in enumerate(sessions[:10], 1):
                            print(f"  {i}. {s}")
                    else:
                        print("暂无历史会话")
                        
                elif cmd.startswith("/load "):
                    try:
                        n = int(cmd.split()[1])
                        sessions = history.list_sessions()
                        history.load(sessions[n-1])
                        print_system(f"已加载会话: {sessions[n-1]}")
                    except (IndexError, ValueError):
                        print_error("无效的会话编号")
                        
                elif cmd == "/clear":
                    print("\033[2J\033[H")  # 清屏
                    
                else:
                    print_error(f"未知命令: {cmd}")
                continue
            
            # 普通聊天
            print_user(user_input)
            history.add_message("user", user_input)
            
            # 裁剪历史
            history.trim(config.max_history)
            
            # 流式输出
            print_assistant("")
            full_response = ""
            
            for chunk in chat.stream_chat(history.current_session):
                print(chunk, end="", flush=True)
                full_response += chunk
            
            print()  # 换行
            
            # 保存回复
            history.add_message("assistant", full_response)
            
        except KeyboardInterrupt:
            print("\n")
            history.save()
            print_system("已保存会话，再见！")
            break
            
        except Exception as e:
            print_error(str(e))

if __name__ == "__main__":
    main()
```

---

## 3. 使用说明

### 3.1 安装依赖

```bash
# 创建项目
uv init ai-chat-cli
cd ai-chat-cli

# 安装依赖
uv add openai python-dotenv
```

### 3.2 配置

```bash
# 创建 .env 文件
cat > .env << EOF
OPENAI_API_KEY=your-api-key
MODEL=gpt-4o-mini
MAX_HISTORY=20
EOF
```

### 3.3 运行

```bash
uv run python main.py
```

---

## 4. 功能演示

```
AI 聊天工具已启动，输入 /help 查看命令

你: 你好

你: 你好
AI: 你好！我是你的 AI 助手，有什么可以帮助你的吗？

你: 介绍一下 Python

你: 介绍一下 Python
AI: Python 是一种高级编程语言...

你: /new
[系统] 已开始新会话

你: /quit
[系统] 再见！
```

---

## 本章小结

```
┌─────────────────────────────────────────────────────────────┐
│                    CLI 聊天工具知识要点                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   项目结构：                                                 │
│   ✓ config.py 配置管理                                      │
│   ✓ chat.py 聊天核心                                        │
│   ✓ history.py 历史记录                                     │
│   ✓ main.py 主程序                                          │
│                                                             │
│   功能实现：                                                 │
│   ✓ 命令解析 (/help, /new, /quit)                          │
│   ✓ 流式输出                                                │
│   ✓ 会话管理                                                │
│   ✓ ANSI 颜色输出                                           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

[← 上一章：流式响应](./03-流式响应.md) | [下一章：Web 聊天界面 →](./05-Web%20聊天界面.md)