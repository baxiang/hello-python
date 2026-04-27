# Web 基础（详细版）

> **前置知识**：Python 函数定义、类与对象、字典/列表操作  
> **本章目标**：理解 HTTP 协议、掌握 RESTful API 设计原则、能独立设计 API 接口

## 本篇学习路径

```
知识依赖图：
┌─────────────────────────────────────────────────────────────┐
│                    Web 基础知识依赖图                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   Python 基础（变量、函数、数据结构）                          │
│           │                                                 │
│           ↓                                                 │
│   ┌───────────────────┐                                     │
│   │  第一部分：HTTP   │  ← 请求/响应模型、状态码、版本      │
│   │  协议基础         │                                     │
│   └───────────────────┘                                     │
│           │                                                 │
│           ↓                                                 │
│   ┌───────────────────┐     ┌───────────────────┐          │
│   │  第二部分：HTTP   │────→│  第三部分：        │          │
│   │  状态码           │     │  RESTful API 设计  │          │
│   └───────────────────┘     └───────────────────┘          │
│           │                         │                      │
│           ↓                         ↓                      │
│   ┌───────────────────────────────────────────┐           │
│   │  第四部分：L2 实践层                       │           │
│   │  最佳实践 + 反模式 + 版本控制              │           │
│   └───────────────────────────────────────────┘           │
│           │                                               │
│           ↓                                               │
│   ┌───────────────────────────────────────────┐           │
│   │  第五部分：L3 专家层                       │           │
│   │  TCP 连接、性能优化、设计动机、知识关联    │           │
│   └───────────────────────────────────────────┘           │
│                                                             │
│   输出：能设计合理的 RESTful API，理解 HTTP 底层原理        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 第一部分：HTTP 协议基础

### HTTP 是什么

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

### HTTP/1.1 vs HTTP/2 vs HTTP/3

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

## 第二部分：HTTP 状态码

### 状态码分类

HTTP 状态码是三位数字，第一位数字定义类别：

```
状态码分类：
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  1xx  Informational（信息）                                  │
│  ├── 100 Continue — 客户端继续发送请求体                    │
│  └── 101 Switching Protocols — 协议切换（如 WebSocket）     │
│                                                             │
│  2xx  Success（成功）                                        │
│  ├── 200 OK — 请求成功                                      │
│  ├── 201 Created — 资源创建成功                              │
│  ├── 204 No Content — 成功但无返回内容                      │
│  └── ...                                                    │
│                                                             │
│  3xx  Redirection（重定向）                                  │
│  ├── 301 Moved Permanently — 永久重定向                      │
│  ├── 302 Found — 临时重定向                                  │
│  ├── 304 Not Modified — 资源未修改（使用缓存）               │
│  └── ...                                                    │
│                                                             │
│  4xx  Client Error（客户端错误）                             │
│  ├── 400 Bad Request — 请求格式错误                          │
│  ├── 401 Unauthorized — 未认证                              │
│  ├── 403 Forbidden — 已认证但无权限                          │
│  ├── 404 Not Found — 资源不存在                              │
│  └── ...                                                    │
│                                                             │
│  5xx  Server Error（服务器错误）                             │
│  ├── 500 Internal Server Error — 服务器内部错误              │
│  ├── 502 Bad Gateway — 网关/代理收到无效响应                 │
│  ├── 503 Service Unavailable — 服务暂时不可用                │
│  └── ...                                                    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 最常用状态码详解

#### 200 OK

请求成功。服务器已处理请求并返回结果。

```python
# http_status_examples.py
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/api/users/{user_id}")
async def get_user(user_id: int) -> JSONResponse:
    """获取用户信息 — 成功时返回 200。"""
    user = {"id": user_id, "name": "Alice", "email": "alice@example.com"}
    return JSONResponse(
        status_code=200,
        content=user,
    )
```

#### 201 Created

资源创建成功。通常配合 `Location` 头返回新资源的 URL。

```python
# http_status_examples.py（续）

@app.post("/api/users")
async def create_user(name: str, email: str) -> JSONResponse:
    """创建用户 — 成功时返回 201。"""
    new_user = {"id": 42, "name": name, "email": email}
    return JSONResponse(
        status_code=201,
        content=new_user,
        headers={"Location": f"/api/users/{new_user['id']}"},
    )
```

#### 204 No Content

请求成功处理，但没有内容返回。常用于 DELETE 操作。

```python
# http_status_examples.py（续）

@app.delete("/api/users/{user_id}")
async def delete_user(user_id: int) -> JSONResponse:
    """删除用户 — 成功时返回 204（无响应体）。"""
    # 执行删除操作...
    return JSONResponse(status_code=204, content=None)
```

#### 301 Moved Permanently vs 302 Found

```
重定向对比：
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  301 永久重定向                                              │
│  ├── 旧 URL 不再使用，客户端应更新书签                        │
│  ├── 浏览器会缓存重定向结果                                   │
│  ├── SEO：权重转移到新 URL                                   │
│  └── 场景：网站域名更换、URL 结构永久变更                    │
│                                                             │
│  302 临时重定向                                              │
│  ├── 旧 URL 仍有效，只是暂时跳转                              │
│  ├── 浏览器不应缓存                                          │
│  ├── SEO：权重保留在原 URL                                    │
│  └── 场景：维护页面、A/B 测试、临时维护                      │
│                                                             │
│  记忆口诀：                                                   │
│  301 = "搬家了，以后都去新地址"                               │
│  302 = "临时出门，一会就回来"                                 │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

#### 400 Bad Request

请求格式有误，服务器无法解析。通常是客户端发送了无效数据。

```python
# http_status_examples.py（续）
from pydantic import BaseModel, EmailStr, ValidationError

class UserCreate(BaseModel):
    name: str
    email: EmailStr

@app.post("/api/users/validate")
async def create_user_validated(user_data: dict) -> JSONResponse:
    """验证用户数据 — 格式错误返回 400。"""
    try:
        user = UserCreate(**user_data)
        return JSONResponse(status_code=201, content=user.model_dump())
    except ValidationError as e:
        return JSONResponse(
            status_code=400,
            content={"error": "请求数据格式错误", "details": e.errors()},
        )
```

#### 401 Unauthorized vs 403 Forbidden

```
认证 vs 授权对比：
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  401 Unauthorized（未认证）                                  │
│  ├── "你是谁？" — 服务器不知道你的身份                        │
│  ├── 解决方案：提供有效的认证凭证（Token、Cookie）            │
│  └── 类比：进大楼时被保安拦住，因为没有门禁卡                 │
│                                                             │
│  403 Forbidden（已认证但无权限）                              │
│  ├── "我知道你是谁，但你不能进"                               │
│  ├── 解决方案：联系管理员提升权限                             │
│  └── 类比：有门禁卡但只能进 A 栋，试图进 B 栋被拒             │
│                                                             │
│  判断流程：                                                   │
│  请求到达 → 有有效凭证？ ──否──> 401                          │
│                │是                                          │
│                ↓                                             │
│           有足够权限？ ──否──> 403                            │
│                │是                                          │
│                ↓                                             │
│           处理请求 → 200                                     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

#### 404 Not Found

请求的资源不存在。

```python
# http_status_examples.py（续）

@app.get("/api/users/{user_id}")
async def get_user_not_found(user_id: int) -> JSONResponse:
    """获取用户 — 不存在时返回 404。"""
    # 模拟数据库查询返回 None
    user = None  # database.get_user(user_id)
    if user is None:
        return JSONResponse(
            status_code=404,
            content={"error": f"用户 {user_id} 不存在"},
        )
    return JSONResponse(status_code=200, content=user)
```

#### 500 Internal Server Error

服务器内部错误。通常是代码 bug、数据库连接失败等。

```python
# http_status_examples.py（续）
import logging

logger = logging.getLogger(__name__)

@app.get("/api/reports/{report_id}")
async def get_report(report_id: int) -> JSONResponse:
    """获取报告 — 服务器错误时返回 500。"""
    try:
        # 模拟可能失败的操作
        report = {"id": report_id, "data": "report content"}
        return JSONResponse(status_code=200, content=report)
    except Exception as e:
        logger.error(f"获取报告失败: {e}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={"error": "服务器内部错误"},
        )
```

#### 502 Bad Gateway vs 503 Service Unavailable

| 状态码 | 含义 | 常见场景 |
|--------|------|---------|
| 502 | 网关/代理收到上游服务器的无效响应 | Nginx 后端服务崩溃、响应格式错误 |
| 503 | 服务器暂时无法处理请求 | 维护模式、过载、限流 |

### 常见状态码误用

#### 误用 1：404 vs 400

| 场景 | 错误用法 | 正确用法 | 原因 |
|------|---------|---------|------|
| 请求参数格式错误 | `404` | `400` | 资源存在，只是请求数据不对 |
| 请求的 URL 路径不存在 | `400` | `404` | 资源本身不存在 |
| 查询条件过滤后无结果 | `404` | `200` + 空列表 | 查询成功，只是没有匹配数据 |

```python
# status_code_mistakes.py
# 正确区分 400 和 404 的示例

@app.get("/api/users/search")
async def search_users(query: str, page: int = 1) -> JSONResponse:
    """搜索用户 — 无结果返回 200 + 空列表，不是 404。"""
    if page < 1:
        return JSONResponse(
            status_code=400,
            content={"error": "页码必须大于 0"},
        )
    
    # 搜索无结果 ≠ 404，因为 /api/users/search 这个端点存在
    results: list[dict] = []  # search_database(query)
    return JSONResponse(status_code=200, content={"data": results, "total": 0})
```

#### 误用 2：301 vs 302

| 场景 | 错误用法 | 正确用法 | 后果 |
|------|---------|---------|------|
| 临时维护页面 | `301` | `302` | 301 被浏览器缓存，维护结束后仍跳转 |
| 永久更换域名 | `302` | `301` | 搜索引擎不传递权重，SEO 损失 |

#### 误用 3：总是返回 200

有些 API 在业务错误时也返回 200，在响应体中用 `code` 字段标识错误：

```python
# status_code_mistakes.py
# ❌ 反模式：用 200 + 业务码表示错误

@app.post("/api/users/bad-practice")
async def create_user_bad(user_data: dict) -> JSONResponse:
    """反模式：所有请求都返回 200，用业务码区分。"""
    if not user_data.get("email"):
        return JSONResponse(
            status_code=200,  # ❌ 应该是 400
            content={"code": 1001, "message": "邮箱不能为空"},
        )
    # ...
```

这种做法的问题：
- HTTP 状态码失去意义，无法用 HTTP 客户端的标准错误处理
- 缓存层（CDN、浏览器）无法正确缓存
- 监控工具无法基于状态码告警

---

## 第三部分：RESTful API 设计原则

### REST 是什么

REST（Representational State Transfer，表述性状态转移）是一种架构风格，由 Roy Fielding 在 2000 年的博士论文中提出。

```
REST 核心概念：
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  1. 资源（Resource）                                         │
│  ─────────────────────────────────────────────              │
│  网络上的任何可命名实体——用户、文章、订单                     │
│  每个资源有唯一 URI 标识                                     │
│  资源不是数据本身，而是"抽象概念"                             │
│                                                             │
│  2. 表述（Representation）                                   │
│  ─────────────────────────────────────────────              │
│  资源在客户端和服务器之间传递时的格式                         │
│  同一资源可有多种表述：JSON、XML、HTML                        │
│  客户端通过 Accept 头指定想要的格式                          │
│                                                             │
│  3. 状态转移（State Transfer）                               │
│  ─────────────────────────────────────────────              │
│  客户端通过操作资源的表述来改变服务器端状态                   │
│  GET：获取当前状态                                           │
│  POST：创建新状态                                           │
│  PUT：替换状态                                              │
│  DELETE：删除状态                                           │
│                                                             │
│  4. 无状态（Stateless）                                     │
│  ─────────────────────────────────────────────              │
│  服务器不保存客户端上下文                                    │
│  每个请求包含足够信息让服务器独立处理                         │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### RESTful URL 设计

**核心原则：URL 表示资源，操作由 HTTP 方法决定。**

```
URL 设计规范：
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  ✅ 用名词，不用动词                                          │
│  ├── ✅ /api/users          （资源：用户集合）               │
│  ├── ✅ /api/users/42       （资源：ID=42 的用户）          │
│  └── ❌ /api/getUser        （动词：GET 已表达操作）         │
│                                                             │
│  ✅ 用复数名词                                                │
│  ├── ✅ /api/users          （统一、一致）                   │
│  └── ❌ /api/user           （容易与单数资源混淆）           │
│                                                             │
│  ✅ 层级不超过 3 级                                           │
│  ├── ✅ /api/users/42/orders       （用户的订单）            │
│  ├── ✅ /api/users/42/orders/99    （用户的某笔订单）        │
│  └── ❌ /api/users/42/orders/99/items/5/payments           │
│                                                             │
│  ✅ 用连字符 - 分隔单词                                      │
│  ├── ✅ /api/blog-posts       （推荐）                       │
│  ├── ⚠️ /api/blog_posts       （可接受）                     │
│  └── ❌ /api/blogPosts        （camelCase 不适合 URL）       │
│                                                             │
│  ✅ 查询参数用于过滤、排序、分页                               │
│  ├── ✅ /api/users?status=active&role=admin                 │
│  ├── ✅ /api/users?sort=created_at&order=desc               │
│  └── ✅ /api/users?page=2&per_page=20                       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### HTTP 方法映射

```
CRUD 操作与 HTTP 方法映射：
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  CRUD        HTTP 方法    URL                幂等    安全    │
│  ──────────  ──────────  ────────────────── ────── ──────  │
│  Create      POST        /api/users         ❌     ❌       │
│  Read        GET         /api/users         ✅     ✅       │
│                          /api/users/42      ✅     ✅       │
│  Update      PUT         /api/users/42      ✅     ❌       │
│              PATCH       /api/users/42      ❌     ❌       │
│  Delete      DELETE      /api/users/42      ✅     ❌       │
│                                                             │
│  特殊操作                                                     │
│  ──────────  ──────────  ────────────────── ────── ──────  │
│  批量操作    POST        /api/users/batch   ❌     ❌       │
│  搜索        GET         /api/users/search  ✅     ✅       │
│  上传文件    POST        /api/users/42/avatar ❌   ❌       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**PUT vs PATCH 对比：**

```
PUT vs PATCH：
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  PUT — 完整替换                                              │
│  ├── 发送完整资源表示                                        │
│  ├── 缺失的字段会被清空或设为默认值                           │
│  └── 场景：编辑表单，提交所有字段                            │
│                                                             │
│  PATCH — 部分更新                                           │
│  ├── 只发送需要修改的字段                                    │
│  ├── 未提及的字段保持不变                                    │
│  └── 场景：只修改邮箱、只修改密码                            │
│                                                             │
│  示例：用户 {name: "Alice", email: "a@x.com", age: 30}      │
│                                                             │
│  PUT  /api/users/42  {email: "b@y.com"}                     │
│  → 结果：{name: null, email: "b@y.com", age: null}          │
│     （未提供的字段被清空）                                   │
│                                                             │
│  PATCH /api/users/42 {email: "b@y.com"}                     │
│  → 结果：{name: "Alice", email: "b@y.com", age: 30}         │
│     （只修改 email，其他不变）                               │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 请求/响应格式（JSON 标准）

```python
# rest_api_formats.py
"""RESTful API 标准请求/响应格式示例。"""

# ── 创建资源 ────────────────────────────────────────────────
# 请求：
#   POST /api/users
#   Content-Type: application/json
#
#   {
#     "name": "张三",
#     "email": "zhangsan@example.com",
#     "role": "editor"
#   }

# 响应（201 Created）：
#   HTTP/1.1 201 Created
#   Location: /api/users/42
#   Content-Type: application/json
#
#   {
#     "id": 42,
#     "name": "张三",
#     "email": "zhangsan@example.com",
#     "role": "editor",
#     "created_at": "2024-01-15T10:30:00Z",
#     "updated_at": "2024-01-15T10:30:00Z"
#   }

# ── 获取资源集合 ─────────────────────────────────────────────
# 请求：
#   GET /api/users?status=active&page=1&per_page=20

# 响应（200 OK）：
#   {
#     "data": [
#       {"id": 1, "name": "Alice", "email": "a@x.com"},
#       {"id": 2, "name": "Bob", "email": "b@x.com"}
#     ],
#     "meta": {
#       "page": 1,
#       "per_page": 20,
#       "total": 156,
#       "total_pages": 8
#     },
#     "links": {
#       "self": "/api/users?page=1",
#       "next": "/api/users?page=2",
#       "last": "/api/users?page=8"
#     }
#   }

# ── 错误响应 ─────────────────────────────────────────────────
# 响应（400 Bad Request）：
#   {
#     "error": {
#       "code": "VALIDATION_ERROR",
#       "message": "请求数据验证失败",
#       "details": [
#         {
#           "field": "email",
#           "message": "邮箱格式不正确"
#         }
#       ]
#     }
#   }
```

---

## 第四部分：L2 实践层

### RESTful API 最佳实践

| 做法 | 原因 | 示例 |
|------|------|------|
| **资源用名词复数** | 统一风格，符合集合语义 | `GET /api/users` |
| **嵌套不超过 2 层** | 避免 URL 过深，保持简单 | `/api/users/{id}/orders` |
| **用 HTTP 状态码表达结果** | 客户端可标准化处理 | 200/201/400/404/500 |
| **响应体包含 `data`/`meta`/`error`** | 结构一致，易于解析 | 见上方响应格式 |
| **分页用查询参数** | 不污染资源路径 | `?page=2&per_page=20` |
| **时间用 ISO 8601 格式** | 国际标准，跨时区友好 | `"2024-01-15T10:30:00Z"` |
| **使用一致的命名风格** | 降低认知负担 | 全用 snake_case |
| **API 加版本前缀** | 便于向后兼容 | `/api/v1/users` |

### 常见反模式

#### 反模式 1：动词 URL

```python
# ❌ 动词 URL（反模式）
@app.post("/api/getUser")
@app.post("/api/createUser")
@app.post("/api/updateUser")
@app.post("/api/deleteUser")

# ✅ RESTful 设计
@app.get("/api/users/{user_id}")      # 获取
@app.post("/api/users")               # 创建
@app.put("/api/users/{user_id}")      # 更新
@app.delete("/api/users/{user_id}")   # 删除
```

**问题：**
- HTTP 方法已表达操作意图，URL 再用动词是冗余
- 违反 REST 的资源导向原则
- 客户端无法利用 HTTP 语义（缓存、重试）

#### 反模式 2：用 GET 做修改操作

```python
# ❌ 用 GET 修改数据（反模式）
@app.get("/api/users/{user_id}/activate")
@app.get("/api/users/{user_id}/delete")

# ✅ 正确做法
@app.post("/api/users/{user_id}/activate")   # 激活（非幂等操作用 POST）
@app.delete("/api/users/{user_id}")          # 删除
```

**问题：**
- GET 应该是安全的（不修改服务器状态）
- 浏览器预加载、搜索引擎爬虫会自动访问 GET URL
- 代理和 CDN 会缓存 GET 响应

#### 反模式 3：过度嵌套

```python
# ❌ 过度嵌套（反模式）
@app.get("/api/users/{user_id}/posts/{post_id}/comments/{comment_id}/likes")

# ✅ 扁平化设计
@app.get("/api/comments/{comment_id}/likes")  # 直接访问
# 或通过查询参数关联
@app.get("/api/likes?comment_id={comment_id}")
```

**问题：**
- URL 过深难以理解和维护
- 暗示数据模型过度耦合
- 深层资源通常有独立的管理需求

#### 反模式 4：用查询参数传递操作

```python
# ❌ 查询参数表达操作（反模式）
@app.get("/api/users?method=delete&id=42")
@app.post("/api/data?action=export&format=csv")

# ✅ 正确做法
@app.delete("/api/users/42")
@app.post("/api/data/export", response_model=dict)
```

### API 版本控制策略

```
API 版本控制策略：
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  策略 1：URL 路径版本化（推荐，最常用）                       │
│  ─────────────────────────────────────────────              │
│  /api/v1/users                                              │
│  /api/v2/users                                              │
│  ✅ 优点：直观、易发现、浏览器可访问                          │
│  ❌ 缺点：URL 与资源路径耦合                                  │
│                                                             │
│  策略 2：请求头版本化                                        │
│  ─────────────────────────────────────────────              │
│  Accept: application/vnd.myapi.v1+json                      │
│  ✅ 优点：URL 干净                                            │
│  ❌ 缺点：不易发现、浏览器无法直接访问                        │
│                                                             │
│  策略 3：查询参数版本化                                      │
│  ─────────────────────────────────────────────              │
│  /api/users?version=1                                       │
│  ✅ 优点：灵活、不影响路径                                    │
│  ❌ 缺点：容易被忽略、缓存混乱                                │
│                                                             │
│  建议：                                                       │
│  • 公开 API：用 URL 路径版本化（开发者友好）                  │
│  • 内部 API：用请求头版本化（保持 URL 干净）                  │
│  • 版本递增：v1 → v2 → v3，不跳过版本号                      │
│  • 废弃策略：新版本上线后，旧版本保留至少 6 个月              │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

```python
# api_versioning.py
"""API 版本控制示例 — URL 路径版本化。"""

from fastapi import APIRouter, FastAPI

app = FastAPI()

# v1 路由
v1_router = APIRouter(prefix="/api/v1")

@v1_router.get("/users/{user_id}")
async def get_user_v1(user_id: int) -> dict:
    """v1：返回用户基本信息。"""
    return {"id": user_id, "name": "Alice", "email": "alice@v1.com"}

# v2 路由
v2_router = APIRouter(prefix="/api/v2")

@v2_router.get("/users/{user_id}")
async def get_user_v2(user_id: int) -> dict:
    """v2：增加更多字段。"""
    return {
        "id": user_id,
        "name": "Alice",
        "email": "alice@v2.com",
        "avatar_url": "https://example.com/avatar.jpg",
        "created_at": "2024-01-15T10:30:00Z",
    }

app.include_router(v1_router)
app.include_router(v2_router)
```

---

## 第五部分：L3 专家层

### HTTP 底层原理

#### TCP 连接与三次握手

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

```python
# tcp_connection_demo.py
"""演示 TCP 连接对 HTTP 性能的影响。"""

import socket
import time

def measure_http_overhead(host: str = "httpbin.org", port: int = 80) -> float:
    """测量建立 TCP 连接的时间开销。"""
    start = time.perf_counter()
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))  # TCP 三次握手
    
    connect_time = time.perf_counter() - start
    
    # 发送最简 HTTP 请求
    request = b"GET /get HTTP/1.1\r\nHost: httpbin.org\r\nConnection: close\r\n\r\n"
    sock.sendall(request)
    
    # 接收响应
    response = b""
    while True:
        chunk = sock.recv(4096)
        if not chunk:
            break
        response += chunk
    
    sock.close()  # TCP 四次挥手
    
    total_time = time.perf_counter() - start
    
    print(f"TCP 连接建立: {connect_time * 1000:.1f} ms")
    print(f"完整请求-响应: {total_time * 1000:.1f} ms")
    
    return connect_time

if __name__ == "__main__":
    measure_http_overhead()
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
│  Connection 头控制：                                         │
│  Connection: keep-alive  （保持连接）                         │
│  Connection: close       （响应后关闭）                       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

```python
# keepalive_demo.py
"""演示 Keep-Alive 连接复用的效果。"""

import requests
import time

def benchmark_keepalive(url: str = "https://httpbin.org/get", n: int = 10) -> None:
    """对比使用和不使用 Keep-Alive 的性能差异。"""
    # 使用 Session（自动复用连接）
    session = requests.Session()
    
    start = time.perf_counter()
    for _ in range(n):
        session.get(url)
    session_time = time.perf_counter() - start
    
    # 不使用 Session（每次新建连接）
    start = time.perf_counter()
    for _ in range(n):
        requests.get(url)
    no_session_time = time.perf_counter() - start
    
    print(f"使用 Session（Keep-Alive）: {session_time * 1000:.1f} ms")
    print(f"不使用 Session             : {no_session_time * 1000:.1f} ms")
    print(f"性能提升: {(no_session_time / session_time - 1) * 100:.0f}%")

if __name__ == "__main__":
    benchmark_keepalive()
```

### 性能考量

```
HTTP 性能优化矩阵：
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  优化维度          技术                    效果              │
│  ──────────────    ───────────────────     ─────────────    │
│  连接复用          Keep-Alive              减少握手开销      │
│                    HTTP/2 多路复用         减少连接数        │
│                                                             │
│  头部优化           HPACK 压缩             减少头部大小      │
│                    减少 Cookie 大小        每次请求都发送    │
│                                                             │
│  传输优化           Gzip/Brotli 压缩       减少传输体积      │
│                    分块传输（Chunked）     无需 Content-Length │
│                    流式响应                首字节时间更短    │
│                                                             │
│  缓存               ETag / Last-Modified   减少重复传输      │
│                    Cache-Control           控制缓存策略      │
│                    304 Not Modified        零字节传输        │
│                                                             │
│  并发               连接池                 避免重复建连      │
│                    HTTP/2 Server Push      主动推送资源      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

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
        headers={"X-Transfer-Encoding": "chunked"},
    )
```

### 设计动机

#### 为什么 HTTP 是无状态的？

```
HTTP 无状态设计动机：
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  问题背景（1990 年代初）：                                    │
│  ─────────────────────────────────────────────              │
│  • 服务器资源极其有限（内存、CPU）                            │
│  • Web 是超文档系统，不是应用平台                             │
│  • 连接是短暂的——获取一个 HTML 页面就断开                    │
│                                                             │
│  无状态的好处：                                               │
│  ─────────────────────────────────────────────              │
│  1. 简化服务器设计 — 不需要维护会话状态                       │
│  2. 水平扩展容易 — 任何服务器都能处理任何请求                 │
│  3. 容错性好 — 服务器崩溃不影响其他请求                       │
│  4. 缓存友好 — 相同请求可以安全缓存                           │
│                                                             │
│  无状态的代价：                                               │
│  ─────────────────────────────────────────────              │
│  1. 每次请求需重新认证 — 通过 Token/Cookie 解决              │
│  2. 购物车/会话需外部存储 — Redis、数据库                     │
│  3. 用户体验需额外设计 — Session 机制                         │
│                                                             │
│  演进：                                                       │
│  ─────────────────────────────────────────────              │
│  Cookie（1994）→ Session（服务器端存储）→ JWT（自包含令牌）  │
│  都是在无状态协议之上构建"有状态"体验                          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

#### 为什么 REST 流行？

```
REST 流行的原因：
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  REST 出现之前：                                              │
│  ─────────────────────────────────────────────              │
│  • SOAP/WSDL：复杂的 XML 协议，需要专用工具                  │
│  • RPC 风格：方法调用隐藏了网络语义                           │
│  • 缺乏统一标准，每个系统都有自己的 API 设计                  │
│                                                             │
│  REST 的优势：                                                │
│  ─────────────────────────────────────────────              │
│  1. 利用现有协议 — HTTP 已广泛部署                            │
│  2. 简单直观 — URL 就是资源地址，方法就是操作                │
│  3. 无需专用客户端 — curl、浏览器即可调用                     │
│  4. 可缓存 — GET 响应天然可缓存                               │
│  5. 可扩展 — 添加新资源只需定义新 URL                         │
│                                                             │
│  对比 RPC：                                                   │
│  ─────────────────────────────────────────────              │
│  RPC：getUserById(42)           → 方法调用风格                │
│  REST：GET /api/users/42        → 资源操作风格               │
│                                                             │
│  RPC 关注"怎么做"（how），REST 关注"是什么"（what）          │
│  REST 更符合 Web 的本质——资源的操作                           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 知识关联图

```
Web 基础知识关联：
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│                    ┌───────────────┐                        │
│                    │  TCP/IP 协议  │  ← 前置知识            │
│                    │  三次握手     │                        │
│                    └───────┬───────┘                        │
│                            │                                │
│                            ↓                                │
│  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐  │
│  │  HTTP/1.1     │─→│  HTTP/2       │─→│  HTTP/3       │  │
│  │  文本协议      │  │  二进制协议    │  │  QUIC/UDP     │  │
│  │  Keep-Alive   │  │  多路复用     │  │  0-RTT        │  │
│  └───────┬───────┘  └───────────────┘  └───────────────┘  │
│          │                                                 │
│          ↓                                                 │
│  ┌───────────────┐     ┌───────────────┐                  │
│  │  HTTP 请求    │     │  HTTP 响应    │                  │
│  │  方法/URL/    │     │  状态码/      │                  │
│  │  头部/正文    │     │  头部/正文    │                  │
│  └───────┬───────┘     └───────┬───────┘                  │
│          │                     │                           │
│          └──────────┬──────────┘                           │
│                     ↓                                      │
│  ┌───────────────────────────────────┐                    │
│  │        RESTful API 设计           │                    │
│  │  ├── 资源命名（名词、复数）        │                    │
│  │  ├── HTTP 方法映射（CRUD）         │                    │
│  │  ├── 状态码使用                   │                    │
│  │  ├── 版本控制策略                 │                    │
│  │  └── 错误响应格式                 │                    │
│  └───────────────────┬───────────────┘                    │
│                      │                                    │
│           ┌──────────┼──────────┐                         │
│           ↓          ↓          ↓                         │
│  ┌──────────────┐ ┌──────────┐ ┌──────────────┐          │
│  │  Flask       │ │ FastAPI  │ │  性能优化     │          │
│  │  传统 Web    │ │ 现代 API  │ │  缓存/压缩    │          │
│  │  模板渲染    │ │ 异步优先  │ │  连接池       │          │
│  └──────────────┘ └──────────┘ └──────────────┘          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 本章总结

```
本章知识回顾：
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  HTTP 协议基础                                               │
│  ├── 请求-响应模型：客户端发起 → 服务器响应                  │
│  ├── 请求结构：方法 + URL + Headers + Body                  │
│  ├── 响应结构：状态码 + Headers + Body                      │
│  └── 版本演进：HTTP/1.1 → HTTP/2 → HTTP/3                   │
│                                                             │
│  HTTP 状态码                                                 │
│  ├── 2xx 成功 / 3xx 重定向 / 4xx 客户端错误 / 5xx 服务器错误 │
│  ├── 最常用：200, 201, 400, 401, 403, 404, 500             │
│  └── 常见误用：404 vs 400, 401 vs 403, 301 vs 302          │
│                                                             │
│  RESTful API 设计                                            │
│  ├── URL 用名词复数，层级不超过 2 级                         │
│  ├── HTTP 方法映射 CRUD：GET/POST/PUT/DELETE                │
│  ├── PUT 全量替换，PATCH 部分更新                            │
│  └── JSON 标准响应格式：data/meta/error                     │
│                                                             │
│  L2 实践层                                                   │
│  ├── 最佳实践：资源命名、状态码、版本控制                    │
│  ├── 反模式：动词 URL、GET 做修改、过度嵌套                  │
│  └── 版本控制：URL 路径（推荐）、请求头、查询参数            │
│                                                             │
│  L3 专家层                                                   │
│  ├── TCP 三次握手 + Keep-Alive 连接复用                     │
│  ├── 性能优化：头部压缩、分块传输、流式响应                  │
│  └── 设计动机：无状态简化扩展，REST 利用现有协议             │
│                                                             │
│  学习路径：                                                   │
│  HTTP 基础 → 状态码 → RESTful 设计 → 实践层 → 专家层        │
│            │                                                │
│            ↓                                                │
│  下一章：Flask / FastAPI 框架实战                             │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```
