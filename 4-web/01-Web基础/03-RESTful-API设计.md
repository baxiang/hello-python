# 03-RESTful-API设计

> **前置知识**：01-HTTP协议基础、02-HTTP状态码  
> **本章目标**：掌握 RESTful API 设计原则、能独立设计合理的 API 接口、了解 API 版本控制

---

## L1 理解层：会用

### 第一部分：REST 是什么

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

---

### 第二部分：RESTful URL 设计

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

### PUT vs PATCH 对比

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

---

### 第三部分：请求/响应格式（JSON 标准）

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

## L2 实践层：用好

### 第四部分：最佳实践与反模式

#### RESTful API 最佳实践

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

## L3 专家层：深入

### 第五部分：底层原理

#### REST 成熟度模型（Richardson Maturity Model）

```
REST 成熟度模型（RMM）：
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  Level 0 — The Swamp of POX（Plain Old XML）                │
│  ─────────────────────────────────────────────              │
│  • 单一 URI，单一 HTTP 方法（通常是 POST）                   │
│  • 请求体中指定操作名称                                       │
│  • 例如：POST /api  {"action": "getUser", "id": 42}        │
│  • 这是 RPC 风格，不是 REST                                  │
│                                                             │
│  Level 1 — Resources                                        │
│  ─────────────────────────────────────────────              │
│  • 引入资源概念，不同资源有不同 URI                          │
│  • 但只用一个 HTTP 方法（POST）                              │
│  • 例如：POST /api/users  /  POST /api/users/42            │
│                                                             │
│  Level 2 — HTTP Verbs                                       │
│  ─────────────────────────────────────────────              │
│  • 正确使用 HTTP 方法（GET/POST/PUT/DELETE）                │
│  • 正确使用 HTTP 状态码                                    │
│  • 这就是大多数"RESTful API"到达的层级                      │
│                                                             │
│  Level 3 — Hypermedia Controls (HATEOAS)                    │
│  ─────────────────────────────────────────────              │
│  • 响应中包含相关链接，客户端可以"发现"操作                  │
│  • 例如：GET /api/users/42 返回                              │
│    {"id": 42, "name": "Alice",                              │
│     "_links": {"self": "/api/users/42",                     │
│                "orders": "/api/users/42/orders",            │
│                "delete": {"method": "DELETE",                │
│                          "href": "/api/users/42"}}}        │
│  • 客户端不需要硬编码 URL                                    │
│  • 真正的 REST 架构                                        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

#### HATEOAS 的实现原理

```python
# hateoas_demo.py
"""HATEOAS（Hypermedia as the Engine of Application State）示例。"""

from fastapi import FastAPI

app = FastAPI()


def add_links(user: dict) -> dict:
    """为资源添加超媒体链接。"""
    return {
        **user,
        "_links": {
            "self": {"href": f"/api/users/{user['id']}", "method": "GET"},
            "update": {"href": f"/api/users/{user['id']}", "method": "PUT"},
            "delete": {"href": f"/api/users/{user['id']}", "method": "DELETE"},
            "orders": {"href": f"/api/users/{user['id']}/orders", "method": "GET"},
        },
    }


@app.get("/api/users/{user_id}")
async def get_user_with_links(user_id: int) -> dict:
    """返回资源及其相关链接 — 客户端可"发现"后续操作。"""
    user = {"id": user_id, "name": "Alice", "email": "alice@example.com"}
    return add_links(user)
```

### 性能考量

| 设计选择 | 性能影响 | 说明 |
|---------|---------|------|
| URL 嵌套深度 | 无明显影响 | 但影响可读性 |
| 资源粒度 | 粗粒度减少请求数 | `/api/users?include=orders` 减少 N+1 请求 |
| 字段过滤 | 减少响应体大小 | `GET /api/users?fields=id,name` |
| 超媒体链接 | 增加响应体 ~20% | 换来客户端灵活性和自描述 |

### 设计动机

**为什么 REST 流行？**

| REST 优势 | 说明 |
|----------|------|
| 利用现有协议 | HTTP 已广泛部署，无需新协议 |
| 简单直观 | URL 就是资源地址，方法就是操作 |
| 无需专用客户端 | curl、浏览器即可调用 |
| 可缓存 | GET 响应天然可缓存 |
| 可扩展 | 添加新资源只需定义新 URL |

**REST vs RPC 对比：**

| 维度 | REST | RPC |
|------|------|-----|
| 关注点 | 资源（what） | 操作（how） |
| URL | `/api/users/42` | `/getUserById` |
| 方法 | 标准 HTTP 方法 | 通常只有 POST |
| 缓存 | GET 天然可缓存 | 需额外设计 |
| 发现性 | HATEOAS 支持 | 需查看文档 |
| 适用场景 | 公开 API、Web 服务 | 内部微服务、gRPC |

### 知识关联

```
RESTful API 知识关联：
┌───────────────────┐
│  HTTP 协议基础    │  ← 前置
│  请求/响应结构    │
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│  HTTP 状态码      │  ← 前置
│  语义与误用       │
└────────┬──────────┘
         │
         ▼
┌───────────────────────────────────┐
│        RESTful API 设计            │
│  ├── 资源命名（名词、复数）        │
│  ├── HTTP 方法映射（CRUD）         │
│  ├── 状态码正确使用                │
│  ├── 版本控制策略                 │
│  └── 错误响应格式                 │
└───────────────┬───────────────────┘
                │
       ┌────────┴────────┐
       ▼                 ▼
┌───────────────┐  ┌───────────────┐
│  Flask 框架   │  │  FastAPI 框架 │
│  传统 Web     │  │  现代 API     │
│  模板渲染     │  │  异步优先     │
└───────────────┘  └───────────────┘
```

---

## 本章小结

```
┌─────────────────────────────────────────────────────────────┐
│                  RESTful API 设计 知识要点                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   REST 核心：                                                │
│   ✓ 资源（名词复数）+ HTTP 方法（动词）                      │
│   ✓ 无状态，每次请求独立                                     │
│   ✓ 表述格式：JSON（主流）、XML、HTML                        │
│                                                             │
│   URL 设计：                                                 │
│   ✓ 用名词复数，不用动词                                     │
│   ✓ 层级不超过 2-3 级                                        │
│   ✓ 用查询参数过滤、排序、分页                               │
│                                                             │
│   HTTP 方法映射：                                            │
│   ✓ GET 获取 / POST 创建 / PUT 替换 / PATCH 部分更新         │
│   ✓ DELETE 删除                                             │
│   ✓ PUT 幂等，PATCH 不幂等                                  │
│                                                             │
│   响应格式：                                                 │
│   ✓ 标准结构：data / meta / error                           │
│   ✓ 分页：page, per_page, total, total_pages                │
│   ✓ 时间：ISO 8601 格式                                     │
│                                                             │
│   版本控制：                                                 │
│   ✓ 推荐：URL 路径版本化（/api/v1/users）                   │
│   ✓ 旧版本保留至少 6 个月                                   │
│                                                             │
│   下一步：进入 Flask 或 FastAPI 实战                         │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```
