# 第 24 章 - Web 基础（详细版）

本章讲解 Web 开发的理论基础，包括 HTTP 协议、URL 路由、Cookie/Session 机制以及 RESTful API 设计规范。这些知识是学习 Flask 和 FastAPI 框架的前提。

---

## 第一部分：HTTP 协议详解

### 24.1 HTTP 是什么

#### 概念说明

HTTP（HyperText Transfer Protocol，超文本传输协议）是互联网上应用最广泛的网络协议，用于客户端（通常是浏览器）和服务器之间的通信。

**核心特点：**

```
┌─────────────────────────────────────────────────────────────┐
│                    HTTP 通信模型                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   客户端 (浏览器)              服务器                        │
│   ┌─────────┐                 ┌─────────┐                  │
│   │         │  --- HTTP 请求--->│         │                  │
│   │         │                 │         │                  │
│   │         │  <---HTTP 响应---│         │                  │
│   │         │                 │         │                  │
│   └─────────┘                 └─────────┘                  │
│                                                             │
│   特点：                                                     │
│   • 无状态：每次请求独立，服务器不"记住"你                  │
│   • 请求 - 响应：客户端发起，服务器响应                      │
│   • 基于文本：HTTP/1.1 使用可读的文本格式                    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**HTTP/1.1 vs HTTP/2 vs HTTP/3：**

| 版本 | 年份 | 主要改进 |
|------|------|---------|
| HTTP/1.1 | 1999 | 持久连接、管道化 |
| HTTP/2 | 2015 | 多路复用、头部压缩、服务器推送 |
| HTTP/3 | 2022 | 基于 QUIC 协议、解决队头阻塞 |

---

### 24.2 HTTP 请求结构

#### 概念说明

HTTP 请求由三部分组成：**请求行**、**请求头**、**请求体**。

```
┌─────────────────────────────────────────────────────────────┐
│                     HTTP 请求结构                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   GET /api/users?id=123 HTTP/1.1        ← 请求行           │
│   Host: api.example.com                 ← 请求头           │
│   User-Agent: Mozilla/5.0               ← 请求头           │
│   Accept: application/json              ← 请求头           │
│   Authorization: Bearer xxxxx           ← 请求头           │
│   Content-Type: application/json        ← 请求头           │
│                                         ← 空行             │
│   {"name": "张三", "age": 25}           ← 请求体 (可选)     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**请求行三要素：**

1. **方法 (Method)**：GET、POST、PUT、DELETE 等
2. **URL**：请求的资源路径
3. **协议版本**：HTTP/1.1、HTTP/2

---

### 24.3 HTTP 方法

#### 概念说明

HTTP 方法定义了客户端希望对资源执行的操作。RESTful API 使用不同的 HTTP 方法对应 CRUD 操作。

```
┌─────────────────────────────────────────────────────────────┐
│                    HTTP 方法与 CRUD 对应关系                  │
├───────────────┬───────────────┬─────────────────────────────┤
│    HTTP 方法   │   CRUD 操作   │         说明                │
├───────────────┼───────────────┼─────────────────────────────┤
│     GET       │    Read       │ 获取资源（列表或单个）       │
│     POST      │    Create     │ 创建新资源                   │
│     PUT       │    Update     │ 完整更新资源                 │
│     PATCH     │    Update     │ 部分更新资源                 │
│     DELETE    │    Delete     │ 删除资源                     │
└───────────────┴───────────────┴─────────────────────────────┘
```

**示例：博客系统的 API 设计**

```python
# 获取文章列表
GET /api/articles

# 获取单篇文章
GET /api/articles/123

# 创建新文章
POST /api/articles
Body: {"title": "我的文章", "content": "..."}

# 更新整篇文章
PUT /api/articles/123
Body: {"title": "更新后的标题", "content": "..."}

# 部分更新（只改标题）
PATCH /api/articles/123
Body: {"title": "新标题"}

# 删除文章
DELETE /api/articles/123
```

---

### 24.4 HTTP 状态码

#### 概念说明

HTTP 状态码是服务器对请求的响应状态的三位数字代码，分为 5 大类。

```
┌─────────────────────────────────────────────────────────────┐
│                    HTTP 状态码分类                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   1xx  信息     →  接收请求，继续处理                       │
│   2xx  成功     →  请求成功                                  │
│   3xx  重定向   →  需要进一步操作才能完成请求               │
│   4xx  客户端错误 → 请求有误，服务器无法处理                │
│   5xx  服务器错误 → 服务器处理请求失败                      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**常用状态码详解：**

| 状态码 | 名称 | 说明 | 使用场景 |
|--------|------|------|---------|
| **2xx 成功** |
| 200 | OK | 请求成功 | GET 成功、POST/PUT/DELETE 完成 |
| 201 | Created | 资源创建成功 | POST 创建新资源 |
| 204 | No Content | 成功但无返回内容 | DELETE 成功 |
| **3xx 重定向** |
| 301 | Moved Permanently | 永久重定向 | 资源 URL 已变更 |
| 302 | Found | 临时重定向 | 临时跳转 |
| 304 | Not Modified | 资源未修改 | 缓存命中 |
| **4xx 客户端错误** |
| 400 | Bad Request | 请求格式错误 | JSON 格式错误、参数缺失 |
| 401 | Unauthorized | 未授权 | 未登录、Token 过期 |
| 403 | Forbidden | 禁止访问 | 无权限访问资源 |
| 404 | Not Found | 资源不存在 | URL 错误 |
| 409 | Conflict | 冲突 | 资源已存在 |
| 422 | Unprocessable Entity | 数据验证失败 | 表单验证错误 |
| 429 | Too Many Requests | 请求过多 | 触发限流 |
| **5xx 服务器错误** |
| 500 | Internal Server Error | 服务器内部错误 | 代码异常 |
| 502 | Bad Gateway | 网关错误 | 上游服务异常 |
| 503 | Service Unavailable | 服务不可用 | 服务器过载 |

---

### 24.5 常见请求头与响应头

#### 概念说明

HTTP 头部字段提供了关于请求、响应或资源的元信息。

**常用请求头：**

| 头部字段 | 说明 | 示例 |
|----------|------|------|
| `Accept` | 客户端能接收的内容类型 | `Accept: application/json` |
| `Authorization` | 认证信息 | `Authorization: Bearer token123` |
| `Content-Type` | 请求体的媒体类型 | `Content-Type: application/json` |
| `Cookie` | 客户端的 Cookie | `Cookie: session=abc123` |
| `User-Agent` | 客户端信息 | `User-Agent: Mozilla/5.0...` |

**常用响应头：**

| 头部字段 | 说明 | 示例 |
|----------|------|------|
| `Content-Type` | 响应体的媒体类型 | `Content-Type: application/json` |
| `Set-Cookie` | 服务器设置的 Cookie | `Set-Cookie: session=xyz789; HttpOnly` |
| `Authorization` | 认证方案 | `Authorization: Bearer` |
| `X-Frame-Options` | 防止点击劫持 | `X-Frame-Options: DENY` |
| `Access-Control-Allow-Origin` | CORS 跨域 | `Access-Control-Allow-Origin: *` |

---

### 24.6 Content-Type 与 MIME 类型

#### 概念说明

Content-Type 头部指定了资源的媒体类型（MIME 类型），告诉客户端如何解析数据。

**常见 Content-Type：**

```
┌─────────────────────────────────────────────────────────────┐
│                   常见 Content-Type                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   文本类型：                                                │
│   • text/html           → HTML 文档                          │
│   • text/plain          → 纯文本                            │
│   • application/json    → JSON 数据（最常用）               │
│   • application/xml     → XML 数据                          │
│   • application/x-www-form-urlencoded → 表单数据            │
│                                                             │
│   图片类型：                                                │
│   • image/jpeg          → JPEG 图片                         │
│   • image/png           → PNG 图片                          │
│   • image/gif           → GIF 图片                          │
│   • image/webp          → WebP 图片                         │
│                                                             │
│   其他类型：                                                │
│   • multipart/form-data → 文件上传表单                      │
│   • application/octet-stream → 二进制流                    │
│   • application/pdf     → PDF 文档                          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**示例：不同 Content-Type 的请求体格式**

```python
# application/json
{"name": "张三", "age": 25}

# application/x-www-form-urlencoded
name=%E5%BC%A0%E4%B8%89&age=25

# multipart/form-data
------WebKitFormBoundary7MA4YWxkTrZu0gW
Content-Disposition: form-data; name="file"; filename="test.txt"
Content-Type: text/plain

文件内容...
------WebKitFormBoundary7MA4YWxkTrZu0gW--
```

---

## 第二部分：URL 与路由设计

### 24.7 URL 结构解析

#### 概念说明

URL（统一资源定位符）用于标识互联网上资源的位置。

```
┌─────────────────────────────────────────────────────────────┐
│                      URL 结构                               │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   https://api.example.com:8443/users/123?format=json#info  │
│   │      │              │      │     │           │          │
│   │      │              │      │     │           └── 片段   │
│   │      │              │      │     └── 查询参数          │
│   │      │              │      └── 路径参数                │
│   │      │              └── 端口（可选）                   │
│   │      └── 主机名/域名                                  │
│   └── 协议（scheme）                                       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**URL 各部分说明：**

| 部分 | 说明 | 示例 |
|------|------|------|
| 协议 (Scheme) | 传输协议 | `http`、`https`、`ftp`、`ws`、`wss` |
| 主机名 | 服务器域名或 IP | `api.example.com`、`localhost` |
| 端口 | 服务端口（可省略） | `80` (HTTP)、`443` (HTTPS) |
| 路径 | 资源路径 | `/users/123` |
| 查询参数 | 附加参数 | `?format=json&page=2` |
| 片段 | 页面内锚点 | `#section1` |

---

### 24.8 路径参数 vs 查询参数

#### 概念说明

路径参数和查询参数都用于传递数据，但使用场景不同。

```
┌─────────────────────────────────────────────────────────────┐
│                路径参数 vs 查询参数                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   路径参数 (Path Parameters)                                │
│   • URL: /users/123                                         │
│   • 用途：标识特定资源                                      │
│   • 必需性：通常是必需的                                    │
│   • 语义：资源的一部分                                      │
│                                                             │
│   查询参数 (Query Parameters)                               │
│   • URL: /users?role=admin&page=2&limit=20                 │
│   • 用途：过滤、排序、分页等                                │
│   • 必需性：通常是可选的                                    │
│   • 语义：资源的修饰符                                      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**示例对比：**

```python
# 路径参数：获取 ID 为 123 的用户
GET /users/123

# 查询参数：过滤用户
GET /users?role=admin          # 过滤管理员
GET /users?status=active       # 过滤活跃用户
GET /users?page=2&limit=20     # 分页
GET /users?sort=created_at&order=desc  # 排序
```

---

### 24.9 RESTful 路由设计规范

#### 概念说明

RESTful 是一种 API 设计风格，核心思想是将一切视为资源，使用标准的 HTTP 方法操作资源。

**RESTful 设计原则：**

```
┌─────────────────────────────────────────────────────────────┐
│                 RESTful 设计原则                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   1. 使用名词（复数）表示资源                               │
│      ✓ /users    ✗ /getUsers                               │
│      ✓ /articles ✗ /articleList                            │
│                                                             │
│   2. 使用 HTTP 方法表示操作                                 │
│      ✓ GET /users    ✗ POST /getUsers                      │
│      ✓ POST /users   ✗ GET /createUser                     │
│                                                             │
│   3. 使用嵌套表示资源关系                                   │
│      /users/123/articles  → 用户 123 的文章                  │
│      /articles/456/comments → 文章 456 的评论               │
│                                                             │
│   4. 使用查询参数过滤、排序、分页                          │
│      /users?role=admin&status=active                       │
│      /articles?sort=published_at&order=desc&page=2        │
│                                                             │
│   5. 返回标准的状态码                                       │
│      200 OK, 201 Created, 404 Not Found, 400 Bad Request   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**完整示例：博客系统 API**

```
┌─────────────────────────────────────────────────────────────┐
│                    博客系统 API 设计                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   文章资源：                                                │
│   GET    /api/articles          → 获取文章列表              │
│   GET    /api/articles/{id}     → 获取单篇文章              │
│   POST   /api/articles          → 创建新文章                │
│   PUT    /api/articles/{id}     → 更新整篇文章              │
│   PATCH  /api/articles/{id}     → 部分更新文章              │
│   DELETE /api/articles/{id}     → 删除文章                  │
│                                                             │
│   嵌套资源（文章的评论）：                                  │
│   GET    /api/articles/{id}/comments     → 获取评论列表    │
│   POST   /api/articles/{id}/comments     → 添加评论        │
│   DELETE /api/articles/{id}/comments/{cid} → 删除评论      │
│                                                             │
│   过滤与分页：                                              │
│   GET /api/articles?author=123&status=published            │
│   GET /api/articles?page=2&limit=10&sort=created_at       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

### 24.10 API 版本控制

#### 概念说明

随着 API 的演进，可能需要引入不兼容的变更。版本控制允许同时支持多个 API 版本。

**版本控制策略：**

| 方式 | 示例 | 优点 | 缺点 |
|------|------|------|------|
| **URL 路径** | `/api/v1/users` | 简单直观、易调试 | URL 冗长 |
| **请求头** | `Accept: application/vnd.api.v1+json` | URL 简洁 | 不易调试 |
| **查询参数** | `/api/users?version=1` | 简单 | 不推荐用于生产 |

**推荐：URL 路径版本控制**

```python
# v1 版本
GET /api/v1/articles

# v2 版本（引入新特性）
GET /api/v2/articles  # 支持更多过滤选项
```

---

## 第三部分：Cookie 与 Session

### 24.11 为什么需要 Cookie 和 Session

#### 概念说明

HTTP 是无状态协议，服务器无法区分两次请求是否来自同一用户。Cookie 和 Session 就是为了解决这个问题。

```
┌─────────────────────────────────────────────────────────────┐
│              无状态 vs 有状态                               │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   无状态 HTTP：                                             │
│   请求 1: "你好" → 服务器 → "你好！"                        │
│   请求 2: "我是谁" → 服务器 → "我不知道你是谁"             │
│                                                             │
│   有状态（Cookie/Session）：                               │
│   请求 1: "你好" → 服务器 → "你好！这是你的 ID: 123"       │
│   请求 2: "我是谁 (ID:123)" → 服务器 → "你是张三"          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

### 24.12 Cookie 原理与属性

#### 概念说明

Cookie 是服务器发送到用户浏览器并保存在本地的一小段数据。浏览器会在后续请求中自动携带 Cookie。

**Cookie 工作流程：**

```
┌─────────────────────────────────────────────────────────────┐
│                    Cookie 工作流程                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   1. 首次请求（无 Cookie）                                  │
│      浏览器                  服务器                         │
│         │  GET /login        │                             │
│         │ ─────────────────> │                             │
│         │                     │ 创建 Session                │
│         │  Set-Cookie:       │                             │
│         │  session_id=abc123 │                             │
│         │ <───────────────── │                             │
│         │                     │                             │
│   2. 后续请求（自动携带 Cookie）                            │
│      浏览器                  服务器                         │
│         │  GET /profile      │                             │
│         │  Cookie:           │                             │
│         │  session_id=abc123 │                             │
│         │ ─────────────────> │ 查找 Session                 │
│         │                     │ 返回用户信息                │
│         │ <───────────────── │                             │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Cookie 属性详解：**

| 属性 | 说明 | 示例 |
|------|------|------|
| `Name=Value` | Cookie 名称和值 | `session_id=abc123` |
| `Expires` | 过期时间 | `Expires=Wed, 09 Jun 2027 10:18:14 GMT` |
| `Max-Age` | 有效期（秒） | `Max-Age=3600` |
| `Domain` | 生效域名 | `Domain=example.com` |
| `Path` | 生效路径 | `Path=/admin` |
| `Secure` | 仅 HTTPS 传输 | `Secure` |
| `HttpOnly` | 禁止 JavaScript 访问 | `HttpOnly` |
| `SameSite` | 跨站限制 | `SameSite=Strict` |

**设置 Cookie 的响应头：**

```http
Set-Cookie: session_id=abc123; Max-Age=3600; Path=/; Secure; HttpOnly; SameSite=Strict
```

---

### 24.13 Session 机制

#### 概念说明

Session 是服务器端的会话存储机制，用于保存用户状态。Session ID 通过 Cookie 传递给服务器。

**Session 工作流程：**

```
┌─────────────────────────────────────────────────────────────┐
│                    Session 工作流程                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   客户端                    服务器                 存储       │
│   ┌─────┐                  ┌─────┐               ┌─────┐   │
│   │     │  1. 登录请求      │     │               │     │   │
│   │     │ ───────────────> │     │               │     │   │
│   │     │                  │     │ 2. 创建 Session       │   │
│   │     │                  │     │ ─────────────> │     │   │
│   │     │                  │     │    session_123  │     │   │
│   │     │  3. 返回 Session ID│     │               │     │   │
│   │     │ <─────────────── │     │               │     │   │
│   │     │    (Cookie)      │     │               │     │   │
│   │     │                  │     │               │     │   │
│   │     │  4. 后续请求      │     │               │     │   │
│   │     │ (携带 Session ID) │     │               │     │   │
│   │     │ ───────────────> │     │ 5. 查询 Session     │   │
│   │     │                  │     │ ─────────────> │     │   │
│   │     │                  │     │ 返回用户数据    │     │   │
│   │     │ <─────────────── │     │               │     │   │
│   └─────┘                  └─────┘               └─────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Session 存储方式：**

| 存储方式 | 优点 | 缺点 | 适用场景 |
|----------|------|------|---------|
| **内存** | 快速、简单 | 重启丢失、无法共享 | 开发环境 |
| **Redis** | 快速、持久化、可共享 | 需额外服务 | 生产环境 |
| **数据库** | 持久化、易查询 | 较慢 | 小型应用 |
| **客户端 Cookie** | 无服务器存储压力 | 大小限制、安全性 | JWT 场景 |

---

### 24.14 Token 认证与 JWT

#### 概念说明

JWT（JSON Web Token）是一种基于 Token 的认证方案，将用户信息编码在 Token 中，服务器无需存储 Session。

**JWT 结构：**

```
┌─────────────────────────────────────────────────────────────┐
│                     JWT 结构                                │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.                    │
│   └──────────────┘                                         │
│        Header (算法和类型)                                  │
│                                                             │
│   eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6 "John"}            │
│   └────────────────────────────────────┘                    │
│        Payload (用户数据)                                   │
│                                                             │
│   SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c               │
│   └────────────────────────────────────┘                    │
│        Signature (签名，防止篡改)                           │
│                                                             │
│   格式：Header.Payload.Signature                            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**JWT vs Session 对比：**

| 特性 | Session | JWT |
|------|---------|-----|
| 存储位置 | 服务器 | 客户端 |
| 服务器压力 | 需存储 | 无存储 |
| 跨域支持 | 较复杂 | 原生支持 |
| 安全性 | 依赖 Session ID 保护 | 依赖签名密钥 |
| 可扩展性 | 需共享 Session | 天然无状态 |
| 适用场景 | 传统 Web 应用 | API、微服务、移动端 |

**JWT 认证流程：**

```python
# 1. 用户登录，服务器生成 JWT
POST /api/login
Body: {"username": "张三", "password": "123456"}
Response: {"token": "eyJhbGciOiJIUzI1NiIs..."}

# 2. 后续请求携带 JWT
GET /api/profile
Headers: {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIs..."}

# 3. 服务器验证 JWT
# - 解析 Payload
# - 验证签名
# - 提取用户信息
```

---

## 第四部分：RESTful API 设计

### 24.15 错误处理规范

#### 概念说明

统一的错误响应格式有助于客户端处理错误。

**推荐错误响应格式：**

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "数据验证失败",
    "details": [
      {
        "field": "email",
        "message": "邮箱格式不正确"
      },
      {
        "field": "password",
        "message": "密码长度至少 8 位"
      }
    ]
  }
}
```

**HTTP 状态码使用指南：**

| 场景 | 状态码 | 说明 |
|------|--------|------|
| 成功 | 200 | 操作成功 |
| 创建成功 | 201 | 资源创建成功 |
| 删除成功 | 204 | 无返回内容 |
| 参数错误 | 400 | 请求格式错误 |
| 未授权 | 401 | 未登录或 Token 过期 |
| 无权限 | 403 | 无访问权限 |
| 不存在 | 404 | 资源不存在 |
| 冲突 | 409 | 资源已存在 |
| 验证失败 | 422 | 数据验证失败 |
| 限流 | 429 | 请求过于频繁 |
| 服务器错误 | 500 | 代码异常 |

---

### 24.16 响应格式规范

#### 概念说明

统一的响应格式有助于前端处理数据。

**成功响应格式：**

```json
{
  "data": {
    "id": 123,
    "name": "张三",
    "email": "zhangsan@example.com"
  },
  "meta": {
    "request_id": "abc123",
    "timestamp": "2027-03-09T10:18:14Z"
  }
}
```

**列表响应格式：**

```json
{
  "data": [
    {"id": 1, "name": "文章 1"},
    {"id": 2, "name": "文章 2"}
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 100,
    "pages": 5
  }
}
```

---

## 本章小结

```
┌─────────────────────────────────────────────────────────────┐
│                      第 24 章 知识要点                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   HTTP 协议：                                                │
│   ✓ 请求结构：请求行 + 请求头 + 请求体                       │
│   ✓ HTTP 方法：GET/POST/PUT/PATCH/DELETE                    │
│   ✓ 状态码：2xx 成功、4xx 客户端错误、5xx 服务器错误          │
│   ✓ 头部字段：Content-Type、Authorization、Cookie          │
│                                                             │
│   URL 与路由：                                               │
│   ✓ URL 结构：协议 + 域名 + 路径 + 查询参数                  │
│   ✓ 路径参数：标识资源 /users/{id}                          │
│   ✓ 查询参数：过滤排序 /users?role=admin                    │
│   ✓ RESTful 设计：名词复数、HTTP 方法操作资源                │
│                                                             │
│   Cookie 与 Session：                                        │
│   ✓ Cookie：客户端存储、自动携带                           │
│   ✓ Session：服务器存储、Session ID 标识                    │
│   ✓ JWT：无状态认证、Token 携带用户信息                      │
│                                                             │
│   API 设计规范：                                             │
│   ✓ 统一错误格式                                             │
│   ✓ 统一响应格式                                             │
│   ✓ 版本控制：/api/v1/                                      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```
---

[← 上一篇](../04-专题深入篇/04-asyncio高级编程.md) | [下一篇 →](./02-Flask快速上手.md)
