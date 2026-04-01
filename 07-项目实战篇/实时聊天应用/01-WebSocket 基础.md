# WebSocket 基础

学习 WebSocket 协议原理和 Python 实现方式。

---

## 1. WebSocket 简介

### 1.1 什么是 WebSocket

```
┌─────────────────────────────────────────────────────────────┐
│                  HTTP vs WebSocket                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   HTTP（请求-响应模式）：                                    │
│   客户端 ──请求──→ 服务器                                    │
│   客户端 ←──响应── 服务器                                    │
│   特点：单向、短连接                                         │
│                                                             │
│   WebSocket（全双工通信）：                                  │
│   客户端 ←──消息──→ 服务器                                   │
│   特点：双向、长连接、实时                                   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 1.2 WebSocket 应用场景

| 场景 | 说明 |
|------|------|
| 聊天应用 | 实时消息推送 |
| 协作编辑 | 多人同时编辑文档 |
| 实时数据 | 股票行情、体育比分 |
| 游戏 | 多人在线游戏 |
| 通知推送 | 系统通知、消息提醒 |

---

## 2. WebSocket 连接过程

### 2.1 握手过程

```
客户端                                    服务器
   │                                        │
   │  1. HTTP GET /ws (Upgrade 请求)        │
   │ ──────────────────────────────────────→│
   │                                        │
   │  2. HTTP 101 Switching Protocols       │
   │ ←──────────────────────────────────────│
   │                                        │
   │  3. WebSocket 连接建立                  │
   │ ←────────── 双向通信 ──────────────────→│
   │                                        │
```

### 2.2 握手请求示例

```http
GET /ws/chat HTTP/1.1
Host: example.com
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==
Sec-WebSocket-Version: 13
```

### 2.3 握手响应示例

```http
HTTP/1.1 101 Switching Protocols
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Accept: s3pPLMBiTxaQ9kYGzzhZRbK+xOo=
```

---

## 3. Python WebSocket 库

### 3.1 常用库对比

| 库 | 特点 | 适用场景 |
|---|------|---------|
| websockets | 纯异步、轻量 | 简单 WebSocket 服务 |
| FastAPI WebSocket | 集成 FastAPI | Web 应用 |
| Socket.IO | 功能丰富、兼容性好 | 复杂实时应用 |

### 3.2 使用 websockets 库

```bash
uv add websockets
```

```python
import asyncio
import websockets

async def echo(websocket):
    """回显服务器"""
    async for message in websocket:
        print(f"收到消息: {message}")
        await websocket.send(f"Echo: {message}")

async def main():
    async with websockets.serve(echo, "localhost", 8765):
        print("WebSocket 服务器运行在 ws://localhost:8765")
        await asyncio.Future()  # 永久运行

asyncio.run(main())
```

### 3.3 客户端连接

```python
import asyncio
import websockets

async def client():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        # 发送消息
        await websocket.send("Hello, Server!")
        
        # 接收消息
        response = await websocket.recv()
        print(f"收到: {response}")

asyncio.run(client())
```

---

## 4. FastAPI WebSocket

### 4.1 基本 WebSocket 端点

```python
from fastapi import FastAPI, WebSocket

app = FastAPI()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    # 接受连接
    await websocket.accept()
    
    try:
        while True:
            # 接收消息
            data = await websocket.receive_text()
            
            # 发送消息
            await websocket.send_text(f"Message received: {data}")
    
    except Exception as e:
        print(f"连接断开: {e}")

# 运行: uvicorn main:app --reload
```

### 4.2 连接管理器

```python
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import List

app = FastAPI()

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        """接受新连接"""
        await websocket.accept()
        self.active_connections.append(websocket)
    
    def disconnect(self, websocket: WebSocket):
        """断开连接"""
        self.active_connections.remove(websocket)
    
    async def send_personal(self, message: str, websocket: WebSocket):
        """发送私聊消息"""
        await websocket.send_text(message)
    
    async def broadcast(self, message: str):
        """广播消息给所有连接"""
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await manager.connect(websocket)
    
    try:
        while True:
            data = await websocket.receive_text()
            # 广播给所有人
            await manager.broadcast(f"用户 {client_id}: {data}")
    
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"用户 {client_id} 离开了聊天")
```

---

## 5. 消息格式设计

### 5.1 JSON 消息格式

```python
import json
from enum import Enum

class MessageType(str, Enum):
    JOIN = "join"        # 加入聊天
    LEAVE = "leave"      # 离开聊天
    MESSAGE = "message"  # 普通消息
    USERS = "users"      # 用户列表

def create_message(msg_type: MessageType, **data) -> str:
    """创建 JSON 消息"""
    return json.dumps({
        "type": msg_type.value,
        "data": data
    })

# 使用示例
join_msg = create_message(MessageType.JOIN, username="Alice")
# {"type": "join", "data": {"username": "Alice"}}

chat_msg = create_message(MessageType.MESSAGE, 
    username="Alice", 
    content="Hello!"
)
# {"type": "message", "data": {"username": "Alice", "content": "Hello!"}}
```

### 5.2 消息解析

```python
def parse_message(raw: str) -> dict:
    """解析消息"""
    try:
        msg = json.loads(raw)
        msg_type = MessageType(msg["type"])
        return {
            "type": msg_type,
            "data": msg.get("data", {})
        }
    except (json.JSONDecodeError, ValueError) as e:
        return {"type": None, "error": str(e)}
```

---

## 本章小结

```
┌─────────────────────────────────────────────────────────────┐
│                    WebSocket 知识要点                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   协议特点：                                                 │
│   ✓ 全双工通信                                              │
│   ✓ 长连接                                                  │
│   ✓ 实时推送                                                │
│                                                             │
│   Python 实现：                                              │
│   ✓ websockets 库（纯异步）                                 │
│   ✓ FastAPI WebSocket（推荐）                               │
│                                                             │
│   连接管理：                                                 │
│   ✓ ConnectionManager 类                                    │
│   ✓ 广播和私聊                                              │
│                                                             │
│   消息格式：                                                 │
│   ✓ JSON 结构化消息                                         │
│   ✓ 消息类型枚举                                            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

[← 返回目录](./README.md) | [下一章：聊天服务器 →](./02-聊天服务器.md)