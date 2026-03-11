# FastAPI WebSocket

掌握 FastAPI WebSocket 实时通信。

---

## 1. 基础 WebSocket

### 1.1 基本使用

```python
from fastapi import FastAPI, WebSocket

app = FastAPI()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Echo: {data}")
    except Exception:
        await websocket.close()
```

### 1.2 客户端示例

```javascript
const ws = new WebSocket('ws://localhost:8000/ws');

ws.onmessage = (event) => {
    console.log('Received:', event.data);
};

ws.send('Hello Server');
```

---

## 2. 连接管理

### 2.1 连接管理器

```python
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import List

class ConnectionManager:
    def __init__(self):
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
            await manager.broadcast(f"Broadcast: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
```

---

## 3. 聊天室示例

```python
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import Dict
import json
from datetime import datetime

app = FastAPI()

class ChatManager:
    def __init__(self):
        self.users: Dict[str, WebSocket] = {}
    
    async def join(self, websocket: WebSocket, username: str):
        await websocket.accept()
        self.users[username] = websocket
        await self.broadcast(f"System: {username} joined")
    
    async def leave(self, username: str):
        if username in self.users:
            del self.users[username]
            await self.broadcast(f"System: {username} left")
    
    async def send_message(self, username: str, message: str):
        await self.broadcast(f"{username}: {message}")
    
    async def broadcast(self, message: str):
        for ws in self.users.values():
            await ws.send_text(message)

chat = ChatManager()

@app.websocket("/chat")
async def chat_websocket(websocket: WebSocket):
    username = None
    try:
        # 接收用户名
        data = await websocket.receive_text()
        data_json = json.loads(data)
        
        if data_json.get("type") == "join":
            username = data_json.get("username")
            await chat.join(websocket, username)
            
            # 消息循环
            while True:
                data = await websocket.receive_text()
                data_json = json.loads(data)
                
                if data_json.get("type") == "message":
                    await chat.send_message(username, data_json.get("message"))
    
    except WebSocketDisconnect:
        if username:
            await chat.leave(username)
```

---

## 4. 完整示例

```python
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import List, Dict
import json

app = FastAPI()

# ==================== 连接管理 ====================
class ConnectionManager:
    def __init__(self):
        self.connections: Dict[str, WebSocket] = {}
    
    async def connect(self, client_id: str, websocket: WebSocket):
        await websocket.accept()
        self.connections[client_id] = websocket
    
    def disconnect(self, client_id: str):
        if client_id in self.connections:
            del self.connections[client_id]
    
    async def send(self, client_id: str, message: str):
        if client_id in self.connections:
            await self.connections[client_id].send_text(message)
    
    async def broadcast(self, message: str):
        for ws in self.connections.values():
            await ws.send_text(message)

manager = ConnectionManager()

# ==================== WebSocket 路由 ====================
@app.websocket("/ws/{client_id}")
async def websocket_endpoint(client_id: str, websocket: WebSocket):
    await manager.connect(client_id, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            if message.get("type") == "broadcast":
                await manager.broadcast(f"[{client_id}] {message.get('content')}")
            elif message.get("type") == "private":
                target = message.get("to")
                content = f"[{client_id} -> {target}] {message.get('content')}"
                await manager.send(target, content)
                await manager.send(client_id, content)
    except WebSocketDisconnect:
        manager.disconnect(client_id)
        await manager.broadcast(f"Client {client_id} disconnected")

# ==================== HTTP 路由 ====================
@app.get("/")
def root():
    return {"message": "WebSocket server running"}
```

---

## 总结

| 知识点 | 说明 |
|---------|------|
| WebSocket | 实时通信 |
| accept/close | 连接管理 |
| receive_text | 接收消息 |
| send_text | 发送消息 |
| 连接管理器 | 广播和私聊 |

---

[← 上一章](./07-FastAPI错误处理.md) | [下一章](./09-FastAPI后台任务.md)