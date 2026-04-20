# WebSocket（详细版）

> Python 3.11+

本章讲解 FastAPI WebSocket 实时通信。

---

## 第一部分：基础 WebSocket

### 1.1 实际场景

需要实现实时聊天功能，客户端和服务器之间保持长连接，实时推送消息。

**问题：如何使用 WebSocket 实现实时通信？**

### 1.2 基本使用

```python
from fastapi import FastAPI, WebSocket

app: FastAPI = FastAPI()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    
    try:
        while True:
            data: str = await websocket.receive_text()
            await websocket.send_text(f"Echo: {data}")
    except Exception:
        await websocket.close()
```

### 1.3 客户端示例

```javascript
const ws = new WebSocket('ws://localhost:8000/ws');

ws.onmessage = (event) => {
    console.log('Received:', event.data);
};

ws.send('Hello Server');
```

---

## 第二部分：连接管理

### 2.1 实际场景

聊天室有多个用户，需要管理所有 WebSocket 连接，支持广播消息。

**问题：如何管理多个 WebSocket 连接？**

### 2.2 连接管理器

```python
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import List


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
    
    async def connect(self, websocket: WebSocket) -> None:
        await websocket.accept()
        self.active_connections.append(websocket)
    
    def disconnect(self, websocket: WebSocket) -> None:
        self.active_connections.remove(websocket)
    
    async def send_personal_message(self, message: str, websocket: WebSocket) -> None:
        await websocket.send_text(message)
    
    async def broadcast(self, message: str) -> None:
        for connection in self.active_connections:
            await connection.send_text(message)


manager: ConnectionManager = ConnectionManager()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data: str = await websocket.receive_text()
            await manager.broadcast(f"Broadcast: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
```

---

## 第三部分：完整示例

```python
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import Dict
import json

app: FastAPI = FastAPI()


# ==================== 连接管理 ====================
class ConnectionManager:
    def __init__(self):
        self.connections: Dict[str, WebSocket] = {}
    
    async def connect(self, client_id: str, websocket: WebSocket) -> None:
        await websocket.accept()
        self.connections[client_id] = websocket
    
    def disconnect(self, client_id: str) -> None:
        if client_id in self.connections:
            del self.connections[client_id]
    
    async def send(self, client_id: str, message: str) -> None:
        if client_id in self.connections:
            await self.connections[client_id].send_text(message)
    
    async def broadcast(self, message: str) -> None:
        for ws in self.connections.values():
            await ws.send_text(message)


manager: ConnectionManager = ConnectionManager()

# ==================== WebSocket 路由 ====================
@app.websocket("/ws/{client_id}")
async def websocket_endpoint(client_id: str, websocket: WebSocket):
    await manager.connect(client_id, websocket)
    try:
        while True:
            data: str = await websocket.receive_text()
            message: dict = json.loads(data)
            
            if message.get("type") == "broadcast":
                await manager.broadcast(f"[{client_id}] {message.get('content')}")
            elif message.get("type") == "private":
                target: str = message.get("to", "")
                content: str = f"[{client_id} -> {target}] {message.get('content')}"
                await manager.send(target, content)
                await manager.send(client_id, content)
    except WebSocketDisconnect:
        manager.disconnect(client_id)
        await manager.broadcast(f"Client {client_id} disconnected")

# ==================== HTTP 路由 ====================
@app.get("/")
def root() -> dict[str, str]:
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