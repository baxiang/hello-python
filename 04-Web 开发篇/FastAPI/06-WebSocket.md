# WebSocket 支持

## WebSocket 端点

FastAPI 原生支持 WebSocket，可以建立持久的双向连接。

**基本用法：**

```python
from fastapi import FastAPI, WebSocket

app = FastAPI()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"收到消息：{data}")
```

**WebSocket 客户端：**

```javascript
const ws = new WebSocket('ws://localhost:8000/ws');

ws.onopen = () => {
  console.log('连接已建立');
  ws.send('Hello Server!');
};

ws.onmessage = (event) => {
  console.log('收到消息:', event.data);
};

ws.onclose = () => {
  console.log('连接已关闭');
};
```

---

## 连接管理

使用连接管理器管理多个 WebSocket 连接，支持广播功能。

```python
from fastapi import WebSocket
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
        """广播消息给所有连接的客户端"""
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"客户端 {client_id}: {data}", websocket)
            await manager.broadcast(f"客户端 {client_id} 说：{data}")
    except:
        manager.disconnect(websocket)
```