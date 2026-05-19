# 08-WebSocket

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

## 第四部分：L3 专家层

### 4.1 WebSocket 握手过程（HTTP Upgrade）

WebSocket 连接始于一次 HTTP 协议的 **Upgrade** 请求，完成握手后升级为独立的 WebSocket 协议：

```
Client                              Server
  │── GET /ws ─────────────────────→│
  │   HTTP/1.1                      │
  │   Upgrade: websocket            │
  │   Connection: Upgrade           │
  │   Sec-WebSocket-Key: dGhlI...   │  ← 随机 16 字节 Base64
  │   Sec-WebSocket-Version: 13     │
  │                                 │
  │←─ 101 Switching Protocols ──────│
  │   HTTP/1.1                      │
  │   Upgrade: websocket            │
  │   Connection: Upgrade           │
  │   Sec-WebSocket-Accept: s3pP... │  ← SHA1(key + magic) 的 Base64
  │                                 │
  │═══════════════════════════════════│  ← 此后使用 WebSocket 帧通信
  │◄══════ 二进制帧 / 文本帧 ═══════►│
```

```python
# Starlette 握手验证核心逻辑（简化版）
MAGIC_STRING = "258EAFA5-E914-47DA-95CA-5AB5AC88DD11"

def compute_accept_key(key: str) -> str:
    import hashlib
    import base64
    digest = hashlib.sha1((key + MAGIC_STRING).encode()).digest()
    return base64.b64encode(digest).decode()

# FastAPI /ws 路由被调用时的流程：
# 1. ASGI scope["type"] == "websocket"
# 2. FastAPI 匹配 WebSocket 路由
# 3. 调用 websocket.accept() 时发送 101 响应
# 4. 此后通过 ASGI websocket.send / websocket.receive 消息类型通信
```

| 握手 Header | 作用 |
|-------------|------|
| `Upgrade: websocket` | 声明协议升级意图 |
| `Connection: Upgrade` | 告知中间件此连接需要升级 |
| `Sec-WebSocket-Key` | 客户端生成的随机值，防止非 WebSocket 客户端误连 |
| `Sec-WebSocket-Version` | 协议版本（当前为 13） |
| `Sec-WebSocket-Accept` | 服务端验证签名，证明理解 WebSocket 协议 |
| `Sec-WebSocket-Protocol` | 子协议协商（如 `graphql-ws`） |

### 4.2 帧结构（FIN / Opcode / Mask / Payload）

WebSocket 数据传输基于**帧（Frame）**，每帧结构如下：

```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-------+-+-------------+-------------------------------+
|F|R|R|R| opcode|M| Payload len |    Extended payload length    |
|I|S|S|S|  (4)  |A|     (7)     |             (16/64)           |
|N|V|V|V|       |S|             |   (if payload len == 126/127)  |
| |1|2|3|       |K|             |                                |
+-+-+-+-+-------+-+-------------+ - - - - - - - - - - - - - - - +
 4               5               6                               7
+-+-+-+-+-------+-+-------------+-------------------------------+
|     Extended payload length (cont.)   | Masking-key (4 bytes) |
+ - - - - - - - - - - - - - - - +-------------------------------+
| Masking-key (cont.)           |       Actual payload data     |
+-------------------------------+ - - - - - - - - - - - - - - - +
:                       Actual payload data                     :
+ - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - +
```

| 字段 | 位数 | 说明 |
|------|------|------|
| FIN | 1 bit | 1=消息最后一帧，0=还有后续帧（分片） |
| RSV1/2/3 | 3 bits | 保留位，默认为 0（扩展协议使用） |
| Opcode | 4 bits | 帧类型：`0x0` 续帧, `0x1` 文本, `0x2` 二进制, `0x8` 关闭, `0x9` Ping, `0xA` Pong |
| MASK | 1 bit | 1=客户端到服务端（必须掩码），0=服务端到客户端 |
| Payload Length | 7/23/71 bits | 数据长度：0-125 直接存储，126 用后续 2 字节，127 用后续 8 字节 |
| Masking Key | 4 bytes | 仅客户端帧有，用于对 payload 做 XOR 解码 |
| Payload Data | 可变 | 实际数据（文本需 UTF-8 编码） |

```python
# 客户端帧掩码解码（RFC 6455）
def unmask_payload(masked_data: bytes, masking_key: bytes) -> bytes:
    """客户端发送的帧数据需要与 masking_key 做 XOR 运算解码"""
    return bytes(
        masked_data[i] ^ masking_key[i % 4]
        for i in range(len(masked_data))
    )

# 示例：Opcode 含义
OPCODES: dict[int, str] = {
    0x0: "continuation",   # 分片消息的后续帧
    0x1: "text",            # 文本帧（UTF-8）
    0x2: "binary",          # 二进制帧
    0x8: "close",           # 连接关闭帧
    0x9: "ping",            # 心跳探测
    0xA: "pong",            # 心跳响应
}
```

### 4.3 连接保活（Ping/Pong）

WebSocket 基于 TCP，需要应用层心跳检测连接存活：

```
Client                              Server
  │                                 │
  │── Ping (0x9, optional data) ──→│
  │                                 │
  │←─ Pong (0xA, same data) ──────│  ← 必须原样返回 data
  │                                 │
  │                                 │
  │  ... 空闲一段时间 ...             │
  │                                 │
  │←─ Ping ────────────────────────│  ← 服务端主动探测
  │                                 │
  │── Pong ───────────────────────→│  ← 客户端回应
  │                                 │
  │  (超时未收到 Pong → 判定断连)    │
```

```python
import asyncio
from fastapi import FastAPI, WebSocket

app: FastAPI = FastAPI()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket) -> None:
    await websocket.accept()
    
    # 启动心跳任务
    async def ping_loop() -> None:
        try:
            while True:
                await asyncio.sleep(30)  # 每 30 秒发送一次 Ping
                await websocket.send_bytes(b"")  # 触发 ASGI ping
        except Exception:
            pass
    
    ping_task: asyncio.Task = asyncio.create_task(ping_loop())
    
    try:
        while True:
            data: str = await websocket.receive_text()
            await websocket.send_text(f"Echo: {data}")
    except Exception:
        pass
    finally:
        ping_task.cancel()
        await websocket.close()
```

| 机制 | 说明 |
|------|------|
| Ping 帧 (0x9) | 心跳探测，可携带最多 125 字节数据 |
| Pong 帧 (0xA) | 必须回复，data 字段与 Ping 一致 |
| 超时检测 | 发送 Ping 后启动定时器，超时未收到 Pong 视为断连 |
| 代理层问题 | Nginx 等代理可能有 `proxy_read_timeout`，超时后主动断开 TCP |
| ws vs wss | `wss://` 使用 TLS 加密，防中间人探测/劫持 |

### 4.4 性能考量

| 操作 | 耗时级别 | 说明 |
|------|----------|------|
| HTTP 握手 | ~1ms | 一次完整的 HTTP 请求-响应 |
| 帧封装/解封装 | ~0.001ms/帧 | 纯内存操作 |
| 客户端掩码（XOR） | ~0.01ms/帧 | 逐字节异或，125 字节以内可忽略 |
| Ping/Pong | ~0.001ms | 控制帧，无 payload 开销 |
| 单连接消息吞吐 | ~10000 msg/s | 受限于 asyncio 事件循环 |
| 并发连接数 | ~10000-50000 | 受限于文件描述符和内存 |

### 4.5 设计动机

| 设计选择 | 动机 |
|----------|------|
| HTTP Upgrade 握手 | 复用现有 HTTP 基础设施（端口、防火墙、代理） |
| 客户端帧必须掩码 | 防止早期 HTTP/1.1 中间缓存污染攻击 |
| 服务端帧不掩码 | 服务端可控，无需额外 XOR 开销 |
| Ping/Pong 控制帧 | 应用层心跳，与 TCP Keep-Alive 互补（TCP 检测网络层，Ping/Pong 检测应用层） |
| FastAPI 的 `websocket.accept()` | 显式接受连接，允许在 accept 前做认证检查（如 query 参数中的 token） |

### 4.6 知识关联

```
WebSocket
├── 握手协议
│   ├── HTTP/1.1 Upgrade 请求
│   ├── Sec-WebSocket-Key → Sec-WebSocket-Accept (SHA1)
│   └── 101 Switching Protocols
│
├── 帧格式（RFC 6455）
│   ├── FIN：分片控制
│   ├── Opcode：帧类型（text/binary/close/ping/pong）
│   ├── MASK：客户端掩码（XOR）
│   └── Payload Length：变长编码（7/23/71 bits）
│
├── 连接管理
│   ├── accept()：握手接受
│   ├── receive_text()/receive_bytes()：接收消息
│   ├── send_text()/send_bytes()：发送消息
│   └── close()：优雅关闭（发送 Close 帧）
│
├── 保活机制
│   ├── Ping/Pong 控制帧
│   ├── 心跳间隔（30-60s）
│   └── 超时检测（断连判定）
│
├── 安全考量
│   ├── wss:// 加密传输
│   ├── 认证（accept 前验证 token）
│   └── 掩码防缓存污染
│
└── 生产实践
    ├── 连接管理器（广播/私聊）
    ├── 消息序列化（JSON / MessagePack）
    ├── 分片处理（大消息拆分）
    └── Nginx 配置（proxy_read_timeout, upgrade header）
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