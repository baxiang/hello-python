# 01-HTTP协议基础

> **前置知识**：Python 函数定义、类与对象  
> **本章目标**：理解 HTTP 请求-响应模型、掌握请求/响应结构、了解 HTTP 版本演进

---

## L1 理解层：会用

### 第一部分：HTTP 是什么

HTTP（HyperText Transfer Protocol，超文本传输协议）是互联网上应用最广泛的网络协议。它是 Web 通信的基础——浏览器访问网页、手机 App 获取数据、微服务之间调用接口，都依赖 HTTP。

**核心理解点：**

```
┌─────────────────────────────────────────────────────────────┐
│          HTTP 关键概念                                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. 请求-响应模型                                            │
│  ─────────────────────────────────────────────              │
│  客户端（浏览器）发起请求 → 服务器处理 → 返回响应            │
│  一次请求对应一次响应，不会主动推送                           │
│                                                             │
│  2. 无状态协议                                               │
│  ─────────────────────────────────────────────              │
│  每次请求独立，服务器不记住上一次请求                         │
│  （通过 Cookie/Session 机制实现"有状态"）                    │
│                                                             │
│  3. 基于 TCP                                                  │
│  ─────────────────────────────────────────────              │
│  HTTP 本身是应用层协议，依赖 TCP 提供可靠传输                │
│  默认端口：80（HTTP）/ 443（HTTPS）                          │
│                                                             │
│  4. 客户端-服务器架构                                        │
│  ─────────────────────────────────────────────              │
│  客户端：浏览器、手机 App、命令行工具（curl）                │
│  服务器：Nginx、Gunicorn、uWSGI 等                           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**通信流程示意：**

```
客户端                            服务器
  │                                 │
  │  ┌──────────────────────┐       │
  │  │   HTTP Request       │       │
  │  │   GET /api/users     │       │
  │  │   Host: example.com  │       │
  │  └──────────────────────┘       │
  │────────────────────────────────>│
  │                                 │  处理请求
  │                                 │  查询数据库
  │                                 │
  │  ┌──────────────────────┐       │
  │  │   HTTP Response      │       │
  │  │   200 OK             │       │
  │  │   Content-Type: ...  │       │
  │  │   [{"id": 1, ...}]   │       │
  │  └──────────────────────┘       │
  │<────────────────────────────────│
  │                                 │
```

### HTTP 请求结构

一个 HTTP 请求由四个部分组成：请求行、请求头（Headers）、空行、请求体（Body）。

```
HTTP 请求结构：
┌─────────────────────────────────────────────────────────────┐
│  请求行：方法 SP 请求目标 SP 协议版本 CRLF                   │
│  例如：GET /api/users HTTP/1.1                               │
├─────────────────────────────────────────────────────────────┤
│  请求头（Headers）：                                          │
│  Host: api.example.com                                       │
│  Content-Type: application/json                              │
│  Authorization: Bearer <token>                               │
│  User-Agent: Mozilla/5.0 ...                                 │
│  Accept: application/json                                    │
├─────────────────────────────────────────────────────────────┤
│  空行（CRLF）—— 分隔头部与正文                                │
├─────────────────────────────────────────────────────────────┤
│  请求体（Body）—— 仅 POST/PUT/PATCH 有                       │
│  {"name": "Alice", "email": "alice@example.com"}            │
└─────────────────────────────────────────────────────────────┘
```

**HTTP 方法（Method）说明：**

| 方法 | 用途 | 安全 | 幂等 | 有请求体 |
|------|------|------|------|---------|
| `GET` | 获取资源 | ✅ 是 | ✅ 是 | ❌ 无 |
| `POST` | 创建资源 | ❌ 否 | ❌ 否 | ✅ 有 |
| `PUT` | 完整替换资源 | ❌ 否 | ✅ 是 | ✅ 有 |
| `PATCH` | 部分更新资源 | ❌ 否 | ❌ 否 | ✅ 有 |
| `DELETE` | 删除资源 | ❌ 否 | ✅ 是 | ❌ 通常无 |
| `HEAD` | 获取响应头（无正文） | ✅ 是 | ✅ 是 | ❌ 无 |
| `OPTIONS` | 查询服务器支持的方法 | ✅ 是 | ✅ 是 | ❌ 无 |

> **安全（Safe）**：不会修改服务器状态  
> **幂等（Idempotent）**：多次执行结果与一次相同

### HTTP 响应结构

响应同样由四部分组成：状态行、响应头、空行、响应体。

```
HTTP 响应结构：
┌─────────────────────────────────────────────────────────────┐
│  状态行：协议版本 SP 状态码 SP 原因短语 CRLF                 │
│  例如：HTTP/1.1 200 OK                                       │
├─────────────────────────────────────────────────────────────┤
│  响应头（Headers）：                                          │
│  Content-Type: application/json; charset=utf-8              │
│  Content-Length: 128                                         │
│  Server: gunicorn/21.2.0                                     │
│  Cache-Control: no-cache                                     │
│  X-Request-Id: abc-123-def                                   │
├─────────────────────────────────────────────────────────────┤
│  空行（CRLF）                                                 │
├─────────────────────────────────────────────────────────────┤
│  响应体（Body）：                                             │
│  {"id": 1, "name": "Alice", "email": "alice@example.com"}   │
└─────────────────────────────────────────────────────────────┘
```

---

### 第二部分：HTTP/1.1 vs HTTP/2 vs HTTP/3

```
HTTP 版本演进：
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  HTTP/1.0（1996）                                            │
│  ├── 每次请求建立新 TCP 连接                                 │
│  ├── 不支持持久连接                                          │
│  └── 无 Host 头（无法虚拟主机）                               │
│           │                                                 │
│           ↓                                                 │
│  HTTP/1.1（1997）— 当前最广泛使用                             │
│  ├── 持久连接（Keep-Alive）默认开启                          │
│  ├── 管道化（Pipelining）— 实际很少用                        │
│  ├── 分块传输编码（Chunked Transfer）                        │
│  ├── 引入 Host 头                                            │
│  └── 队头阻塞（Head-of-Line Blocking）                       │
│           │                                                 │
│           ↓                                                 │
│  HTTP/2（2015）                                              │
│  ├── 二进制协议（非文本）                                     │
│  ├── 多路复用（Multiplexing）— 解决队头阻塞                   │
│  ├── 头部压缩（HPACK）                                       │
│  ├── 服务器推送（Server Push）                               │
│  └── 同一 TCP 连接上并行传输多个请求                          │
│           │                                                 │
│           ↓                                                 │
│  HTTP/3（2022）                                              │
│  ├── 基于 QUIC 协议（UDP 而非 TCP）                          │
│  ├── 彻底解决队头阻塞（传输层）                               │
│  ├── 更快的连接建立（0-RTT/1-RTT）                           │
│  ├── 内置加密（TLS 1.3）                                     │
│  └── 更好的网络切换（如 WiFi 切 5G）                          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**版本对比：**

| 特性 | HTTP/1.1 | HTTP/2 | HTTP/3 |
|------|----------|--------|--------|
| 传输层 | TCP | TCP | UDP (QUIC) |
| 连接数 | 多连接并发 | 单连接多路复用 | 单连接多路复用 |
| 队头阻塞 | 有 | 应用层无，传输层有 | 无 |
| 头部压缩 | 无 | HPACK | QPACK |
| 加密 | 可选（HTTPS） | 可选（实践中必选） | 强制加密 |
| 连接建立 | 3 次握手 | 3 次握手 + TLS | 0-RTT / 1-RTT |

---

## L2 实践层：用好

### 第三部分：实战代码

#### 用 Python 发送 HTTP 请求

```python
# http_request_demo.py
"""使用 Python 标准库和 requests 发送 HTTP 请求。"""

import urllib.request
import json

# ── 方式 1：标准库 urllib ────────────────────────────────────

def fetch_with_urllib(url: str) -> dict:
    """使用 urllib 发送 GET 请求。"""
    req = urllib.request.Request(
        url,
        headers={"Accept": "application/json"},
    )
    with urllib.request.urlopen(req) as response:
        data: bytes = response.read()
        return json.loads(data)

# ── 方式 2：requests 库（推荐） ──────────────────────────────

import requests

def fetch_with_requests(url: str) -> dict:
    """使用 requests 发送 GET 请求（推荐）。"""
    response = requests.get(url, headers={"Accept": "application/json"})
    response.raise_for_status()  # 4xx/5xx 抛出异常
    return response.json()

# ── 方式 3：POST 请求 ────────────────────────────────────────

def create_resource(url: str, data: dict) -> dict:
    """发送 POST 请求创建资源。"""
    response = requests.post(
        url,
        json=data,  # 自动设置 Content-Type: application/json
        headers={"Authorization": "Bearer your-token"},
    )
    response.raise_for_status()
    return response.json()

if __name__ == "__main__":
    # 示例
    user = fetch_with_requests("https://httpbin.org/get")
    print(f"请求成功: {user['url']}")
```

### 连接池与 Keep-Alive

```python
# connection_pool_demo.py
"""演示 Session 连接池的效果。"""

import requests
import time

def benchmark_session(url: str = "https://httpbin.org/get", n: int = 10) -> None:
    """对比使用和不使用 Session 的性能差异。"""
    # 使用 Session（自动复用连接，Keep-Alive）
    session = requests.Session()
    start = time.perf_counter()
    for _ in range(n):
        session.get(url)
    session_time = time.perf_counter() - start

    # 不使用 Session（每次新建 TCP 连接）
    start = time.perf_counter()
    for _ in range(n):
        requests.get(url)
    no_session_time = time.perf_counter() - start

    print(f"使用 Session（Keep-Alive）: {session_time * 1000:.1f} ms")
    print(f"不使用 Session             : {no_session_time * 1000:.1f} ms")
    print(f"性能提升: {(no_session_time / session_time - 1) * 100:.0f}%")

if __name__ == "__main__":
    benchmark_session()
```

### 常见反模式

| 反模式 | 问题 | 正确做法 |
|--------|------|---------|
| **每次请求新建连接** | TCP 握手开销大 | 使用 `requests.Session()` |
| **忽略响应状态码** | 错误被静默吞掉 | 调用 `response.raise_for_status()` |
| **不设置超时** | 请求可能永久挂起 | `requests.get(url, timeout=5)` |
| **用 GET 做修改操作** | 违反 HTTP 语义 | 用 POST/PUT/DELETE |

---

## L3 专家层：深入

### 第四部分：底层原理

#### TCP 三次握手

HTTP 依赖 TCP 提供可靠传输。在发送 HTTP 请求之前，必须先建立 TCP 连接。

```
TCP 三次握手：
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  客户端                                服务器                │
│    │                                      │                 │
│    │  ① SYN（我想连接，初始序列号=x）       │                 │
│    │─────────────────────────────────────>│                 │
│    │                                      │                 │
│    │  ② SYN-ACK（我同意，我的序列号=y）    │                 │
│    │<─────────────────────────────────────│                 │
│    │                                      │                 │
│    │  ③ ACK（收到，连接建立）               │                 │
│    │─────────────────────────────────────>│                 │
│    │                                      │                 │
│    │  ← 连接建立，开始传输 HTTP 数据 →      │                 │
│    │                                      │                 │
│                                                             │
│  耗时：至少 1 个 RTT（Round Trip Time）                      │
│  HTTPS：额外需要 TLS 握手（1-2 个 RTT）                      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

#### Keep-Alive 连接复用

```
Keep-Alive 工作原理：
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  不使用 Keep-Alive：                                         │
│  ┌─────┐  ┌─────┐  ┌─────┐  ┌─────┐  ┌─────┐               │
│  │握手 │→│请求 │→│响应 │→│挥手 │→│握手 │→ ...               │
│  └─────┘  └─────┘  └─────┘  └─────┘  └─────┘               │
│  每个请求都要经历完整的 TCP 连接生命周期                        │
│                                                             │
│  使用 Keep-Alive（HTTP/1.1 默认）：                           │
│  ┌──────────────────────────────────────────────┐           │
│  │ 握手 → 请求 → 响应 → 请求 → 响应 → ... → 挥手 │          │
│  └──────────────────────────────────────────────┘           │
│  一次握手，多次请求                                          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 性能考量

**连接建立耗时对比：**

| 场景 | 首次请求 | 后续请求（复用连接） | 说明 |
|------|---------|-------------------|------|
| HTTP/1.1 无 Keep-Alive | ~100ms | ~100ms | 每次完整握手 |
| HTTP/1.1 + Keep-Alive | ~100ms | ~10ms | 省去握手 |
| HTTP/2 多路复用 | ~100ms | ~10ms | 并行传输 |
| HTTP/3 (QUIC) | ~50ms | ~5ms | 0-RTT 恢复 |

**分块传输编码（Chunked Transfer Encoding）：**

```python
# chunked_transfer.py
"""分块传输编码示例 — 适用于大数据流式响应。"""

from collections.abc import AsyncGenerator
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

app = FastAPI()

async def data_stream() -> AsyncGenerator[bytes, None]:
    """模拟流式数据生成器。"""
    for i in range(5):
        yield f"数据块 {i}\n".encode("utf-8")

@app.get("/api/stream")
async def stream_data() -> StreamingResponse:
    """流式响应 — 使用分块传输，无需预先计算 Content-Length。
    
    适用场景：
    - 大数据导出（无需加载到内存）
    - 实时日志输出
    - SSE（Server-Sent Events）
    """
    return StreamingResponse(
        data_stream(),
        media_type="text/plain",
    )
```

### 设计动机

**为什么 HTTP 是无状态的？**

| 设计选择 | 原因 | 影响 |
|---------|------|------|
| 无状态协议 | 1990 年代服务器资源有限 | 简化设计，水平扩展容易 |
| 每次请求独立 | 任何服务器都能处理任何请求 | 容错性好，缓存友好 |
| Cookie/Session 补救 | 实际需要"有状态"体验 | 在无状态之上构建状态 |

### 知识关联

```
HTTP 协议知识关联：
┌───────────────────┐
│  TCP/IP 协议栈    │  ← 前置知识
│  三次握手/挥手    │
└────────┬──────────┘
         │
         ▼
┌───────────────────┐     ┌───────────────────┐
│  HTTP/1.1         │────→│  HTTP/2           │
│  文本/Keep-Alive  │     │  二进制/多路复用  │
└────────┬──────────┘     └────────┬──────────┘
         │                         │
         ▼                         ▼
┌─────────────────────────────────────────┐
│         HTTP 请求-响应模型               │
│  ┌───────────┐     ┌───────────┐       │
│  │ 请求       │     │ 响应       │       │
│  │ 方法/URL  │────→│ 状态码/   │       │
│  │ 头部/正文 │     │ 头部/正文 │       │
│  └───────────┘     └───────────┘       │
└─────────────────┬───────────────────────┘
                  │
         ┌────────┴────────┐
         ▼                 ▼
┌───────────────┐  ┌───────────────┐
│  HTTP/3       │  │  HTTPS        │
│  QUIC/UDP     │  │  TLS 加密     │
│  0-RTT        │  │  证书验证     │
└───────────────┘  └───────────────┘
```

---

## 本章小结

```
┌─────────────────────────────────────────────────────────────┐
│                      HTTP 协议基础 知识要点                   │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   HTTP 是什么：                                              │
│   ✓ 请求-响应模型，客户端发起 → 服务器响应                   │
│   ✓ 无状态协议，每次请求独立                                 │
│   ✓ 基于 TCP，默认端口 80/443                               │
│                                                             │
│   请求结构：                                                 │
│   ✓ 请求行（方法 + URL + 协议版本）                          │
│   ✓ 请求头（Host, Content-Type, Authorization）              │
│   ✓ 请求体（仅 POST/PUT/PATCH）                             │
│                                                             │
│   响应结构：                                                 │
│   ✓ 状态行（协议版本 + 状态码 + 原因短语）                   │
│   ✓ 响应头（Content-Type, Content-Length, Server）           │
│   ✓ 响应体（JSON/HTML/二进制数据）                           │
│                                                             │
│   版本演进：                                                 │
│   ✓ HTTP/1.1：持久连接，队头阻塞                             │
│   ✓ HTTP/2：二进制，多路复用，头部压缩                       │
│   ✓ HTTP/3：QUIC/UDP，0-RTT，强制加密                       │
│                                                             │
│   下一步：HTTP 状态码 → RESTful API 设计                    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```
