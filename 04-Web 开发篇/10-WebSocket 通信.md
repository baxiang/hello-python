# 第 10 章：WebSocket 通信

掌握 WebSocket 实时通信技术。

---

## 本章目标

- 理解 WebSocket 原理
- 掌握 FastAPI WebSocket
- 实现聊天室应用
- 了解 Socket.IO

---

## 10.1 WebSocket 基础

### 什么是 WebSocket？

WebSocket 是一种在单个 TCP 连接上进行全双工通信的协议，适用于实时应用。

### WebSocket vs HTTP

| 特性 | HTTP | WebSocket |
|------|------|-----------|
| 连接方式 | 请求-响应 | 持久连接 |
| 通信方向 | 半双工 | 全双工 |
| 实时性 | 轮询 | 推送 |
| 资源消耗 | 每次请求 | 单一连接 |

---

## 10.2 FastAPI WebSocket

### 基础示例

```python
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    
    try:
        while True:
            # 接收消息
            data = await websocket.receive_text()
            
            # 发送消息
            await websocket.send_text(f"收到: {data}")
            
    except WebSocketDisconnect:
        print("客户端断开连接")
```

### 客户端示例

```javascript
// 浏览器端
const ws = new WebSocket('ws://localhost:8000/ws');

ws.onopen = () => {
    console.log('连接成功');
    ws.send('Hello Server');
};

ws.onmessage = (event) => {
    console.log('收到:', event.data);
};

ws.onerror = (error) => {
    console.error('错误:', error);
};

ws.onclose = () => {
    console.log('连接关闭');
};
```

---

## 10.3 连接管理器

```python
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import List

app = FastAPI()

class ConnectionManager:
    def __init__(self):
        # 活跃连接
        self.active_connections: List[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
    
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
    
    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)
    
    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"广播: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
```

---

## 10.4 聊天室应用

```python
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import Dict, List
import json
from datetime import datetime

app = FastAPI()

# 用户信息
class User:
    def __init__(self, websocket: WebSocket, username: str):
        self.websocket = websocket
        self.username = username

# 聊天室管理器
class ChatRoom:
    def __init__(self):
        self.users: Dict[str, User] = {}
    
    async def join(self, websocket: WebSocket, username: str):
        await websocket.accept()
        self.users[username] = User(websocket, username)
        
        # 通知其他人
        await self.broadcast(f"系统: {username} 加入了聊天室")
        
        # 发送用户列表
        await self.send_user_list()
    
    async def leave(self, username: str):
        if username in self.users:
            del self.users[username]
            await self.broadcast(f"系统: {username} 离开了聊天室")
            await self.send_user_list()
    
    async def send_message(self, username: str, message: str):
        await self.broadcast(f"{username}: {message}")
    
    async def broadcast(self, message: str):
        for user in self.users.values():
            await user.websocket.send_text(message)
    
    async def send_user_list(self):
        user_list = list(self.users.keys())
        message = json.dumps({
            "type": "user_list",
            "data": user_list
        })
        for user in self.users.values():
            await user.websocket.send_text(message)

chat_room = ChatRoom()

@app.websocket("/chat")
async def chat_endpoint(websocket: WebSocket):
    username = None
    
    try:
        # 接收用户名
        data = await websocket.receive_text()
        data_json = json.loads(data)
        
        if data_json.get("type") == "join":
            username = data_json.get("username")
            await chat_room.join(websocket, username)
            
            # 消息循环
            while True:
                data = await websocket.receive_text()
                data_json = json.loads(data)
                
                if data_json.get("type") == "message":
                    message = data_json.get("message")
                    await chat_room.send_message(username, message)
    
    except WebSocketDisconnect:
        if username:
            await chat_room.leave(username)
```

---

## 10.5 Socket.IO

### 安装

```bash
pip install python-socketio aiohttp
```

### 服务端

```python
import socketio

sio = socketio.AsyncServer()
app = socketio.ASGIApp(sio)

@sio.event
async def connect(sid, environ):
    print(f"客户端连接: {sid}")

@sio.event
async def disconnect(sid):
    print(f"客户端断开: {sid}")

@sio.event
async def chat_message(sid, data):
    # 广播消息
    await sio.emit("chat_message", data)

@sio.event
async def private_message(sid, data):
    # 发送私聊消息
    await sio.emit("chat_message", data, room=data["to"])
```

### 客户端

```javascript
// 浏览器端
const socket = io('http://localhost:8000');

socket.on('connect', () => {
    console.log('已连接');
});

socket.on('chat_message', (data) => {
    console.log('收到消息:', data);
});

socket.emit('chat_message', {message: 'Hello'});
```

---

## 10.6 实战：实时通知系统

```python
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from typing import Dict, List
import asyncio

app = FastAPI()

# 通知类型
class NotificationType(str):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    SUCCESS = "success"

# 通知模型
class Notification(BaseModel):
    type: NotificationType
    title: str
    message: str
    timestamp: str = None

# 通知管理器
class NotificationManager:
    def __init__(self):
        self.subscribers: Dict[str, WebSocket] = {}
    
    async def subscribe(self, user_id: str, websocket: WebSocket):
        await websocket.accept()
        self.subscribers[user_id] = websocket
    
    async def unsubscribe(self, user_id: str):
        if user_id in self.subscribers:
            await self.subscribers[user_id].close()
            del self.subscribers[user_id]
    
    async def send_notification(self, user_id: str, notification: Notification):
        if user_id in self.subscribers:
            await self.subscribers[user_id].send_json(notification.dict())
    
    async def broadcast(self, notification: Notification):
        for websocket in self.subscribers.values():
            await websocket.send_json(notification.dict())

manager = NotificationManager()

# WebSocket 端点
@app.websocket("/ws/notifications/{user_id}")
async def notifications(websocket: WebSocket, user_id: str):
    await manager.subscribe(user_id, websocket)
    
    try:
        while True:
            # 保持连接
            await websocket.receive_text()
    except WebSocketDisconnect:
        await manager.unsubscribe(user_id)

# 发送通知的 API
@app.post("/notify/{user_id}")
async def send_notification(user_id: str, notification: Notification):
    await manager.send_notification(user_id, notification)
    return {"status": "sent"}

@app.post("/notify/broadcast")
async def broadcast_notification(notification: Notification):
    await manager.broadcast(notification)
    return {"status": "broadcasted"}
```

---

## 本章总结

### 学到的技能

| 技能 | 说明 |
|------|------|
| WebSocket 基础 | 协议和原理 |
| FastAPI WebSocket | 端点和连接 |
| 连接管理 | 广播和私聊 |
| 聊天室 | 实时聊天应用 |
| Socket.IO | 跨平台实时通信 |

### 下一步

在 [第 11 章](./11-Web 项目实战.md) 中，我们将进行完整的项目实战。

---

[← 上一章](./09-RESTful API 设计.md) | [下一章 →](./11-Web 项目实战.md)