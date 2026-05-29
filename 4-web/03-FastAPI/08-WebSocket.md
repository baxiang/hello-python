# 08-WebSocket

> Python 3.11+

本章讲解 FastAPI WebSocket 实时通信。

---

## 概念铺垫

WebSocket 通过 HTTP Upgrade 机制建立持久化的双向连接，协议从 HTTP/1.1 升级为 WebSocket（`ws://` 或加密 `wss://`），之后通过帧（Frame）进行数据交换。

```
HTTP 握手阶段：
  Client ── GET /ws (Upgrade: websocket) ──→ Server
  Client ←── 101 Switching Protocols ────── Server

WebSocket 通信阶段：
  Client ════ 帧 (Frame) ════ Server
```

**核心概念：**
- **握手**：客户端发送 `Upgrade: websocket` 请求头，服务端验证并返回 `101` 状态码，此后使用 WebSocket 帧通信
- **帧结构**：每个帧包含 FIN（分片标志）、Opcode（帧类型：文本/二进制/关闭/Ping/Pong）、MASK（客户端掩码 XOR）、Payload 数据
- **Ping/Pong**：应用层心跳机制，Ping 帧 (0x9) 探测连接，Pong 帧 (0xA) 响应，与 TCP Keep-Alive 互补
- **客户端掩码**：RFC 6455 规定客户端到服务端的帧必须用 4 字节密钥 XOR 编码，防止缓存污染攻击

FastAPI 的 `WebSocket` 类封装了 ASGI websocket 协议：`accept()` 握手、`receive_text()`/`receive_bytes()` 接收、`send_text()`/`send_bytes()` 发送、`close()` 优雅关闭。

---

### L1 理解层：会用

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

### L2 实践层：用好

## 最佳实践

### 1. 在 accept() 前认证

```python
@app.websocket("/ws")
async def ws_endpoint(websocket: WebSocket, token: str = Query(...)):
    # 在 accept 前验证 token
    user = verify_token(token)
    if not user:
        await websocket.close(code=1008)  # Policy Violation
        return

    await websocket.accept()
    # 后续通信...
```

**关键点**：`accept()` 之前可以拒绝连接，避免无效连接占用资源。使用查询参数传递 token（浏览器 WebSocket API 不支持自定义请求头）。

### 2. 心跳保活

```python
import asyncio

@app.websocket("/ws/{client_id}")
async def ws_endpoint(client_id: str, websocket: WebSocket):
    await websocket.accept()

    async def heartbeat():
        try:
            while True:
                await asyncio.sleep(30)
                await websocket.send_json({"type": "ping"})
        except Exception:
            pass

    task = asyncio.create_task(heartbeat())
    try:
        while True:
            data = await websocket.receive_json()
            if data.get("type") == "pong":
                continue  # 心跳响应
            # 处理业务消息...
    except WebSocketDisconnect:
        pass
    finally:
        task.cancel()
```

**为什么需要心跳**：Nginx 等反向代理有 `proxy_read_timeout`（默认 60s），空闲连接超时后会被断开。Ping/Pong 可保持应用层活跃。

### 3. 连接管理器线程安全

```python
import asyncio

class ConnectionManager:
    def __init__(self):
        self.connections: dict[str, WebSocket] = {}
        self._lock = asyncio.Lock()

    async def connect(self, client_id: str, websocket: WebSocket):
        await websocket.accept()
        async with self._lock:
            self.connections[client_id] = websocket

    async def disconnect(self, client_id: str):
        async with self._lock:
            self.connections.pop(client_id, None)

    async def broadcast(self, message: str):
        async with self._lock:
            disconnected = []
            for cid, ws in self.connections.items():
                try:
                    await ws.send_text(message)
                except Exception:
                    disconnected.append(cid)
            for cid in disconnected:
                self.connections.pop(cid, None)
```

## 反模式

| ❌ 反模式 | ✅ 改进 |
|-----------|---------|
| accept 前不验证身份 | 在 accept 前验证 token，拒绝未授权连接 |
| 无心跳机制，连接静默断开 | 30-60 秒间隔的 Ping/Pong 心跳 |
| 广播时连接断开导致所有连接阻塞 | 广播时逐个 try/except，记录失败连接后移除 |
| 在 ws handler 中执行同步阻塞操作 | 异步操作或用 `asyncio.to_thread()` |
| 不处理 `WebSocketDisconnect` 异常 | 始终 try/except WebSocketDisconnect |
| 生产环境使用 `ws://` | 使用 `wss://`（TLS 加密） |
| 连接管理器无锁保护 | 使用 `asyncio.Lock` 防止并发修改 |

## 何时选用什么

| 需求 | 选用方案 |
|------|---------|
| 双向实时通信 | WebSocket |
| 服务端单向推送（无需客户端响应） | SSE (Server-Sent Events) |
| 低频更新（分钟级） | HTTP 轮询（最简单） |
| 聊天应用、在线协作 | WebSocket + 连接管理器 |
| 股票行情、体育比分 | WebSocket + 广播 |
| 文件上传进度 | WebSocket + 二进制帧 |
| 需要认证的 WebSocket | `Query(token=...)` + accept 前验证 |

---

### L3 专家层：深入

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

## 常见坑点排查

### 坑点 1：Nginx 代理后 WebSocket 连接立即断开

**错误现象**：开发环境 WebSocket 正常工作，部署到 Nginx 后连接建立后立即 404/502。

**根因**：Nginx 默认不转发 WebSocket 的 Upgrade 头。需要显式配置：

```nginx
# ❌ 不正确的 Nginx 配置
location /ws {
    proxy_pass http://backend:8000;
}

# ✅ 正确的 Nginx 配置
location /ws {
    proxy_pass http://backend:8000;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_read_timeout 3600s;  # 长连接超时设置
    proxy_send_timeout 3600s;
}
```

### 坑点 2：广播时一个断开连接导致全部阻塞

**错误现象**：

```python
async def broadcast(self, message: str):
    for ws in self.active_connections:
        await ws.send_text(message)  # 一个断开，全部阻塞！
```

当 `active_connections` 列表中有一个 WebSocket 已断开时，`send_text()` 会抛异常，导致剩余连接收不到消息。

**修复**：

```python
async def broadcast(self, message: str):
    disconnected = []
    for ws in self.active_connections:
        try:
            await ws.send_text(message)
        except Exception:
            disconnected.append(ws)
    for ws in disconnected:
        self.active_connections.remove(ws)
```

### 坑点 3：在 WebSocket handler 中调用同步阻塞函数

**错误现象**：WebSocket 连接建立后，服务端越来越慢，最终所有 WebSocket 连接都卡住。

**根因**：`time.sleep()` 或同步数据库查询在 async handler 中直接调用，阻塞了整个事件循环。

```python
# ❌ 同步阻塞（阻塞事件循环）
@app.websocket("/ws")
async def ws(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        result = heavy_sync_computation(data)  # 阻塞 5 秒！
        await websocket.send_text(result)
```

**修复**：

```python
import asyncio

# ✅ 将同步操作放到线程池
@app.websocket("/ws")
async def ws(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        result = await asyncio.to_thread(heavy_sync_computation, data)
        await websocket.send_text(result)
```

### 坑点 4：accept() 之前尝试 send 操作

**错误现象**：

```python
@app.websocket("/ws")
async def ws(websocket: WebSocket):
    await websocket.send_text("Welcome!")  # RuntimeError!
    await websocket.accept()
```

**根因**：ASGI WebSocket 协议规定，服务端必须在 `accept()` 之后才能发送消息。发送必须在握手完成后进行。

**修复**：始终先 `accept()`：

```python
@app.websocket("/ws")
async def ws(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_text("Welcome!")
```

### 坑点排查表

| 现象 | 根因 | 修复 | 预防 |
|------|------|------|------|
| Nginx 下 WebSocket 404/502 | 缺少 Upgrade/Connection 头配置 | 添加 `proxy_set_header Upgrade` | Nginx 配置模板中包含 WebSocket 配置 |
| 广播消息丢失 | 一个断连阻塞全部 | try/except 逐个发送 | 连接管理器使用 `asyncio.Lock` |
| 所有 WebSocket 卡顿 | 同步函数阻塞事件循环 | `asyncio.to_thread()` | 代码审查检查 handler 中的同步调用 |
| `send_text` 前报 RuntimeError | 未 `accept()` 就发送 | 先 `accept()` 再发送 | handler 首行写 `await ws.accept()` |
| 内存持续增长 | 断开的连接未从列表移除 | broadcast 时清理断连 | 添加心跳机制自动清理 |
| 消息重复 | 客户端重连后旧连接未清理 | 使用 client_id 覆盖旧连接 | 维护 `{client_id: WebSocket}` |

---

## 进阶用法

### 5.1 房间/频道系统

```python
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Query
from typing import Annotated
import asyncio
import json


class RoomManager:
    """基于房间/频道的连接管理器"""

    def __init__(self):
        # {room_name: {client_id: WebSocket}}
        self.rooms: dict[str, dict[str, WebSocket]] = {}
        self._lock = asyncio.Lock()

    async def join(self, room: str, client_id: str, websocket: WebSocket) -> None:
        await websocket.accept()
        async with self._lock:
            if room not in self.rooms:
                self.rooms[room] = {}
            self.rooms[room][client_id] = websocket
        await self.broadcast(room, {
            "type": "system",
            "client_id": client_id,
            "event": "joined",
            "room": room,
        })

    async def leave(self, room: str, client_id: str) -> None:
        async with self._lock:
            if room in self.rooms:
                self.rooms[room].pop(client_id, None)
                if not self.rooms[room]:
                    del self.rooms[room]
        await self.broadcast(room, {
            "type": "system",
            "client_id": client_id,
            "event": "left",
            "room": room,
        })

    async def broadcast(self, room: str, message: dict) -> None:
        members = list(self.rooms.get(room, {}).items())
        disconnected = []
        for cid, ws in members:
            try:
                await ws.send_json(message)
            except Exception:
                disconnected.append(cid)
        if disconnected:
            async with self._lock:
                for cid in disconnected:
                    self.rooms.get(room, {}).pop(cid, None)

    async def send_to(self, room: str, client_id: str, message: dict) -> bool:
        if room in self.rooms and client_id in self.rooms[room]:
            try:
                await self.rooms[room][client_id].send_json(message)
                return True
            except Exception:
                await self.leave(room, client_id)
        return False

    def room_info(self, room: str) -> dict:
        return {
            "room": room,
            "members": len(self.rooms.get(room, {})),
        }

    def all_rooms(self) -> list[dict]:
        return [{"name": r, "members": len(m)} for r, m in self.rooms.items()]


room_manager = RoomManager()

@app.websocket("/ws/{room}")
async def room_websocket(
    room: str,
    websocket: WebSocket,
    client_id: Annotated[str, Query()],
):
    await room_manager.join(room, client_id, websocket)
    try:
        while True:
            data = await websocket.receive_json()
            msg_type = data.get("type")

            if msg_type == "broadcast":
                await room_manager.broadcast(room, {
                    "type": "message",
                    "from": client_id,
                    "content": data.get("content", ""),
                })
            elif msg_type == "private":
                target = data.get("to", "")
                await room_manager.send_to(room, target, {
                    "type": "private",
                    "from": client_id,
                    "content": data.get("content", ""),
                })
            elif msg_type == "ping":
                await websocket.send_json({"type": "pong"})

    except WebSocketDisconnect:
        await room_manager.leave(room, client_id)


# HTTP 端点获取房间信息
@app.get("/rooms")
def get_rooms() -> list[dict]:
    return room_manager.all_rooms()


@app.get("/rooms/{room}")
def get_room(room: str) -> dict:
    return room_manager.room_info(room)
```

### 5.2 带认证的 WebSocket + REST 混合架构

```python
import jwt
from datetime import datetime, timedelta
from fastapi import WebSocketDisconnect


SECRET_KEY = "your-secret-key"

def create_token(user_id: int) -> str:
    return jwt.encode({
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(hours=24),
    }, SECRET_KEY, algorithm="HS256")

def verify_token(token: str) -> dict | None:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except jwt.PyJWTError:
        return None


@app.websocket("/ws/protected")
async def protected_ws(
    websocket: WebSocket,
    token: Annotated[str, Query()],
):
    # 在 accept 前验证
    payload = verify_token(token)
    if not payload:
        await websocket.close(code=1008, reason="Authentication failed")
        return

    user_id = payload["user_id"]
    await websocket.accept()
    await websocket.send_json({"type": "welcome", "user_id": user_id})

    try:
        while True:
            data = await websocket.receive_json()
            await websocket.send_json({
                "type": "echo",
                "user_id": user_id,
                "data": data,
            })
    except WebSocketDisconnect:
        pass


# REST 端点配套查询
@app.get("/ws/online-users")
def online_users() -> list[dict]:
    """查询所有在线的 WebSocket 用户"""
    result = []
    for room, members in room_manager.rooms.items():
        for cid in members:
            result.append({"client_id": cid, "room": room})
    return result
```

### 5.3 指数退避重连策略（客户端）

```javascript
class ReconnectingWebSocket {
    constructor(url, maxRetries = 10, initialDelay = 1000) {
        this.url = url;
        this.maxRetries = maxRetries;
        this.initialDelay = initialDelay;
        this.retryCount = 0;
        this.connect();
    }

    connect() {
        this.ws = new WebSocket(this.url);

        this.ws.onopen = () => {
            console.log('Connected');
            this.retryCount = 0;  // 重置计数
        };

        this.ws.onclose = (event) => {
            if (event.code === 1008) {
                console.error('Auth failed, not reconnecting');
                return;
            }
            if (this.retryCount < this.maxRetries) {
                const delay = this.initialDelay * Math.pow(2, this.retryCount);
                const jitter = delay * (0.5 + Math.random() * 0.5);
                console.log(`Reconnecting in ${Math.round(jitter)}ms (attempt ${this.retryCount + 1})`);
                setTimeout(() => {
                    this.retryCount++;
                    this.connect();
                }, jitter);
            } else {
                console.error('Max retries reached');
            }
        };

        this.ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            if (data.type === 'ping') {
                this.ws.send(JSON.stringify({type: 'pong'}));
            }
            this.onMessage?.(data);
        };
    }

    send(data) {
        if (this.ws.readyState === WebSocket.OPEN) {
            this.ws.send(JSON.stringify(data));
        } else {
            console.warn('WebSocket not connected, message queued');
        }
    }

    close() {
        this.maxRetries = 0;
        this.ws.close();
    }
}
```

### 5.4 生产级 Nginx WebSocket 代理配置

```nginx
upstream websocket_backend {
    least_conn;
    server backend1:8000 weight=1 max_fails=3 fail_timeout=30s;
    server backend2:8000 weight=1 max_fails=3 fail_timeout=30s;
}

map $http_upgrade $connection_upgrade {
    default upgrade;
    ''      close;
}

server {
    listen 443 ssl http2;
    server_name api.example.com;

    ssl_certificate     /etc/ssl/certs/api.crt;
    ssl_certificate_key /etc/ssl/private/api.key;

    location /ws/ {
        proxy_pass http://websocket_backend;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection $connection_upgrade;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        proxy_read_timeout 86400s;   # 24 小时长连接超时
        proxy_send_timeout 86400s;
        proxy_connect_timeout 10s;

        # WebSocket 不需要缓冲
        proxy_buffering off;
    }

    # REST API 正常代理
    location /api/ {
        proxy_pass http://websocket_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 5.5 大消息分片处理

当 WebSocket 消息超过帧大小限制（默认为 1MB）时，需要分片传输：

```python
import asyncio

MAX_FRAME_SIZE = 1024 * 1024  # 1MB


@app.websocket("/ws/large-files")
async def large_file_ws(websocket: WebSocket):
    await websocket.accept()

    async def send_large(data: bytes, chunk_size: int = 65536):
        """分片发送大数据块"""
        for i in range(0, len(data), chunk_size):
            chunk = data[i:i + chunk_size]
            await websocket.send_bytes(chunk)
            if i + chunk_size < len(data):
                await asyncio.sleep(0.01)  # 微小的让步，避免阻塞

    async def receive_large() -> bytes:
        """分片接收大数据块"""
        chunks = bytearray()
        while True:
            msg = await websocket.receive()
            if "bytes" in msg:
                chunks.extend(msg["bytes"])
            if "text" in msg and msg["text"] == "EOF":
                break
        return bytes(chunks)

    try:
        # 发送
        big_data = b"x" * (10 * 1024 * 1024)  # 10MB 测试数据
        await send_large(big_data)
        await websocket.send_text("EOF")
        print("Sent 10MB file")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await websocket.close()
```

### 5.6 ASGI WebSocket 协议底层事件

```python
@app.websocket("/ws/protocol-debug")
async def protocol_debug(websocket: WebSocket):
    await websocket.accept()

    # ASGI WebSocket 的三种核心事件:
    # 1. websocket.receive → {"type": "websocket.receive", "bytes": b"...", "text": "..."}
    # 2. websocket.send    → sub-type: "websocket.send", "websocket.close"
    # 3. websocket.disconnect → {"type": "websocket.disconnect", "code": 1000}

    try:
        while True:
            raw = await websocket.receive()

            match raw["type"]:
                case "websocket.receive":
                    if "text" in raw:
                        print(f"Got text: {raw['text'][:50]}...")
                    elif "bytes" in raw:
                        print(f"Got bytes: {len(raw['bytes'])} bytes")
                case "websocket.disconnect":
                    print(f"Disconnect: code={raw.get('code', 'none')}")
                    break
    except Exception:
        pass
    finally:
        try:
            await websocket.close(code=1000)
        except Exception:
            pass
```

---

## 调试与排错技巧

### 技巧 1：WebSocket 连接状态监控

```python
@app.websocket("/ws/monitored")
async def monitored_ws(websocket: WebSocket):
    await websocket.accept()
    state = {"connected": True, "messages": 0, "bytes_sent": 0, "bytes_received": 0}
    try:
        while True:
            data = await websocket.receive_text()
            state["messages"] += 1
            state["bytes_received"] += len(data.encode())
            response = f"Echo ({state['messages']}): {data}"
            await websocket.send_text(response)
            state["bytes_sent"] += len(response.encode())
            if state["messages"] % 100 == 0:
                print(f"Stats: {state}")
    except WebSocketDisconnect:
        state["connected"] = False
        print(f"Final stats: {state}")
```

### 技巧 2：使用 wscat 手动测试 WebSocket

```bash
# 安装 wscat
npm install -g wscat

# 连接 WebSocket
wscat -c "ws://localhost:8000/ws" -H "Authorization: Bearer token123"

# 连接带查询参数的 WebSocket
wscat -c "ws://localhost:8000/ws?token=abc123"

# 发送 JSON 消息
> {"type": "chat", "content": "hello"}
< {"type": "chat", "from": "system", "content": "Echo: hello"}

# 发送二进制消息（hex）
> --binary 48656c6c6f
```

### 技巧 3：连接泄漏检测

```python
import gc

@app.get("/debug/ws-connections")
def debug_ws_connections() -> dict:
    """查看当前所有 WebSocket 连接状态"""
    rooms_info = []
    for room_name, members in room_manager.rooms.items():
        for cid, ws in members:
            rooms_info.append({
                "room": room_name,
                "client_id": cid,
                "client_state": ws.client_state.name if ws.client_state else "unknown",
            })
    return {
        "total_rooms": len(room_manager.rooms),
        "connections": rooms_info,
    }
```

{% hint style="warning" %}
**生产环境禁用** `/debug/ws-connections` 端点，或添加管理员认证，避免暴露内部状态。
{% endhint %}

---

## 生产部署架构

### 多 Worker 跨进程广播（Redis Pub/Sub）

当有多个 Worker 进程时，WebSocket 连接分散在不同进程上：

```
                     Nginx (upstream)
                          │
          ┌───────────────┼───────────────┐
          ▼               ▼               ▼
    ┌──────────┐    ┌──────────┐    ┌──────────┐
    │ Worker 1 │    │ Worker 2 │    │ Worker 3 │
    │ WS: A,B  │    │ WS: C,D  │    │ WS: E,F  │
    └────┬─────┘    └────┬─────┘    └────┬─────┘
         │               │               │
         └───────────────┼───────────────┘
                         │
                   ┌─────┴─────┐
                   │   Redis   │  ← Pub/Sub 实现跨进程广播
                   └───────────┘
```

```python
import redis.asyncio as redis
import json
import asyncio


class DistributedConnectionManager:
    """支持多进程的 WebSocket 连接管理器"""

    def __init__(self, redis_url: str = "redis://localhost:6379"):
        self.redis = redis.from_url(redis_url)
        self.local_connections: dict[str, WebSocket] = {}
        self._pubsub: redis.client.PubSub | None = None
        self._listener_task: asyncio.Task | None = None
        self._lock = asyncio.Lock()

    async def start(self):
        self._pubsub = self.redis.pubsub()
        await self._pubsub.subscribe("ws:broadcast")
        self._listener_task = asyncio.create_task(self._listen())

    async def _listen(self):
        """监听 Redis 广播消息并推送到本地连接"""
        async for message in self._pubsub.listen():
            if message["type"] == "message":
                data = json.loads(message["data"])
                for ws in list(self.local_connections.values()):
                    try:
                        await ws.send_json(data)
                    except Exception:
                        pass

    async def connect(self, client_id: str, websocket: WebSocket):
        await websocket.accept()
        async with self._lock:
            self.local_connections[client_id] = websocket

    async def disconnect(self, client_id: str):
        async with self._lock:
            self.local_connections.pop(client_id, None)

    async def broadcast(self, message: dict):
        """跨进程广播：发布到 Redis，所有进程的 listener 都会收到"""
        await self.redis.publish("ws:broadcast", json.dumps(message))

    async def send_personal(self, client_id: str, message: dict):
        if client_id in self.local_connections:
            try:
                await self.local_connections[client_id].send_json(message)
            except Exception:
                await self.disconnect(client_id)


# lifespan 中启动
@asynccontextmanager
async def lifespan(app: FastAPI):
    distributed_manager = DistributedConnectionManager()
    await distributed_manager.start()
    app.state.ws_manager = distributed_manager
    yield
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
| 房间/频道系统 | 多房间隔离、按房间广播 |
| 认证 (accept 前) | Query 参数传 token，accept 前验证 |
| 指数退避重连 | 客户端自动重连策略 |
| Nginx 代理配置 | Upgrade/Connection 头、长连接超时 |
| 大消息分片 | 超过 1MB 消息的分片收发 |
| ASGI 底层事件 | websocket.receive/send/disconnect |
