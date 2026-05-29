# 02-HTTP状态码

> **前置知识**：01-HTTP协议基础（请求-响应模型）  
> **本章目标**：掌握常用 HTTP 状态码含义、能正确使用状态码、避免常见误用

---

## 概念铺垫

### 第一部分：状态码分类

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

---

### 第二部分：最常用状态码语义

#### 200 OK

请求成功。服务器已处理请求并返回结果。适用于 GET/PUT/PATCH 操作成功时。

#### 201 Created

资源创建成功。通常配合 `Location` 头返回新资源的 URL。适用于 POST 操作成功时。

#### 204 No Content

请求成功处理，但没有内容返回。常用于 DELETE 操作，或无需返回数据的更新。

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

请求格式有误，服务器无法解析。比如 JSON 格式错误、字段类型不匹配、缺少必填字段。

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

请求的资源不存在。注意与查询无结果区分：资源不存在是 404，查询成功但无匹配结果应返回 200 + 空列表。

#### 500 Internal Server Error

服务器内部错误。通常是代码 bug、数据库连接失败、未捕获异常等。生产环境不应暴露详细错误信息。

#### 502 vs 503

| 状态码 | 含义 | 常见场景 |
|--------|------|---------|
| 502 | 网关/代理收到上游服务器的无效响应 | Nginx 后端服务崩溃、响应格式错误 |
| 503 | 服务器暂时无法处理请求 | 维护模式、过载、限流 |

---

### L1 理解层：会用

#### 示例1：返回 200 OK

```python
# http_status_examples.py
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/api/users/{user_id}")
async def get_user(user_id: int) -> JSONResponse:
    """获取用户信息 — 成功时返回 200。"""
    user = {"id": user_id, "name": "Alice", "email": "alice@example.com"}
    return JSONResponse(status_code=200, content=user)
```

#### 示例2：返回 201 Created

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

#### 示例3：返回 204 No Content

```python
# http_status_examples.py（续）

@app.delete("/api/users/{user_id}")
async def delete_user(user_id: int) -> JSONResponse:
    """删除用户 — 成功时返回 204（无响应体）。"""
    return JSONResponse(status_code=204, content=None)
```

#### 示例4：返回 400 Bad Request

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

#### 示例5：返回 404 Not Found

```python
# http_status_examples.py（续）

@app.get("/api/users/{user_id}")
async def get_user_not_found(user_id: int) -> JSONResponse:
    """获取用户 — 不存在时返回 404。"""
    user = None  # database.get_user(user_id)
    if user is None:
        return JSONResponse(
            status_code=404,
            content={"error": f"用户 {user_id} 不存在"},
        )
    return JSONResponse(status_code=200, content=user)
```

#### 示例6：返回 500 Internal Server Error

```python
# http_status_examples.py（续）
import logging

logger = logging.getLogger(__name__)

@app.get("/api/reports/{report_id}")
async def get_report(report_id: int) -> JSONResponse:
    """获取报告 — 服务器错误时返回 500。"""
    try:
        report = {"id": report_id, "data": "report content"}
        return JSONResponse(status_code=200, content=report)
    except Exception as e:
        logger.error(f"获取报告失败: {e}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={"error": "服务器内部错误"},
        )
```

---

### L2 实践层：用好

#### 常见状态码误用

##### 误用 1：404 vs 400

| 场景 | ❌ 错误用法 | ✅ 正确用法 | 原因 |
|------|-----------|-----------|------|
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

##### 误用 2：301 vs 302

| 场景 | ❌ 错误用法 | ✅ 正确用法 | 后果 |
|------|-----------|-----------|------|
| 临时维护页面 | `301` | `302` | 301 被浏览器缓存，维护结束后仍跳转 |
| 永久更换域名 | `302` | `301` | 搜索引擎不传递权重，SEO 损失 |

**何时用 301？** — 域名永久变更、URL 结构永久重构时。  
**何时用 302？** — 临时跳转、A/B 测试、维护模式时。

##### 误用 3：总是返回 200

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
```

**这种做法的问题：**
- HTTP 状态码失去意义，无法用 HTTP 客户端的标准错误处理
- 缓存层（CDN、浏览器）无法正确缓存
- 监控工具无法基于状态码告警

#### 反模式清单

| 反模式 | 问题 | ✅ 正确做法 | 适用场景 |
|--------|------|-----------|---------|
| **总返回 200** | 状态码失去意义 | 用 4xx/5xx 表达错误 | 所有 API 端点 |
| **查询无结果返回 404** | 查询成功只是无匹配 | 返回 200 + 空列表 | 搜索/过滤/列表接口 |
| **401 和 403 混用** | 客户端无法区分处理 | 未认证 401，无权限 403 | 认证与鉴权 |
| **301 用于临时跳转** | 浏览器永久缓存 | 临时跳改用 302/307 | 维护页/AB测试 |

---

### L3 专家层：深入

#### 状态码解析流程

```
HTTP 响应状态码的解析流程：
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  服务器侧：                                                  │
│  1. 接收请求 → 路由匹配 → 调用处理函数                      │
│  2. 处理函数返回结果（或抛出异常）                          │
│  3. 框架将结果映射为状态码 + 响应体                         │
│  4. 写入 TCP 缓冲区 → 发送客户端                            │
│                                                             │
│  客户端侧：                                                  │
│  1. 接收 HTTP 响应 → 解析状态行                             │
│  2. 提取状态码（第 1 位数字决定类别）                       │
│  3. 根据状态码决定后续行为：                                │
│     • 2xx → 解析响应体                                      │
│     • 3xx → 读取 Location 头，发起新请求                    │
│     • 4xx → 客户端错误，修正请求                            │
│     • 5xx → 服务器错误，重试或报错                          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

#### 304 Not Modified 的缓存机制

```python
# conditional_request_demo.py
"""演示 304 Not Modified 的缓存机制。"""

from fastapi import FastAPI, Request
from fastapi.responses import Response, JSONResponse
import hashlib
import time

app = FastAPI()

# 模拟资源数据
RESOURCE_DATA = '{"id": 1, "name": "Alice"}'
RESOURCE_ETAG = '"' + hashlib.md5(RESOURCE_DATA.encode()).hexdigest()[:8] + '"'

@app.get("/api/users/{user_id}")
async def get_user_cached(user_id: int, request: Request) -> Response:
    """带条件请求的端点 — 支持 304 缓存。"""
    # 检查客户端缓存
    if_none_match = request.headers.get("if-none-match")
    if if_none_match == RESOURCE_ETAG:
        return Response(status_code=304, headers={"ETag": RESOURCE_ETAG})
    
    return JSONResponse(
        status_code=200,
        content={"id": user_id, "name": "Alice"},
        headers={"ETag": RESOURCE_ETAG},
    )
```

#### 性能考量

| 状态码 | 响应体大小 | 缓存策略 | 说明 |
|--------|-----------|---------|------|
| 200 | 完整响应体 | 根据 Cache-Control | 正常响应 |
| 204 | 0 字节 | 不可缓存 | DELETE 常用 |
| 301 | 极小（可空） | 永久缓存 | 浏览器缓存直到清除 |
| 304 | 0 字节 | 沿用之前缓存 | 零传输，节省带宽 |
| 400 | 错误描述 | 不可缓存 | 客户端需修正 |
| 404 | 错误描述 | 可短期缓存 | 避免重复请求不存在资源 |
| 500 | 错误描述 | 不可缓存 | 服务器需修复 |

#### 设计动机

**为什么有这么多状态码？**

| 设计选择 | 原因 |
|---------|------|
| 3 位数字 | 第一位分类，后两位细分，人类可读 |
| 区分 4xx/5xx | 客户端 vs 服务器责任明确 |
| 201 vs 200 | 创建成功应返回 201，客户端知道可以 GET 新资源 |
| 401 vs 403 | 未认证 vs 无权限，客户端处理方式不同 |

#### 知识关联

```
HTTP 状态码知识关联：
┌───────────────────┐
│  HTTP 请求        │
│  方法 + URL + 头  │
└────────┬──────────┘
         │
         ▼
┌───────────────────────────────────┐
│       服务器处理                  │
│                                   │
│  成功 ──> 2xx                     │
│  ├── 200 OK（通用成功）           │
│  ├── 201 Created（新建资源）      │
│  └── 204 No Content（无返回体）   │
│                                   │
│  重定向 ──> 3xx                   │
│  ├── 301 永久                    │
│  ├── 302 临时                    │
│  └── 304 缓存命中                │
│                                   │
│  客户端错误 ──> 4xx               │
│  ├── 400 格式错误                │
│  ├── 401 未认证                  │
│  ├── 403 无权限                  │
│  └── 404 资源不存在              │
│                                   │
│  服务器错误 ──> 5xx               │
│  ├── 500 内部错误                │
│  ├── 502 网关错误                │
│  └── 503 服务不可用              │
└───────────────────────────────────┘
```

---

## 本章小结

```
┌─────────────────────────────────────────────────────────────┐
│                      HTTP 状态码 知识要点                     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   状态码分类：                                               │
│   ✓ 1xx 信息 / 2xx 成功 / 3xx 重定向                        │
│   ✓ 4xx 客户端错误 / 5xx 服务器错误                         │
│                                                             │
│   最常用状态码：                                             │
│   ✓ 200 OK / 201 Created / 204 No Content                  │
│   ✓ 301 永久重定向 / 302 临时重定向 / 304 缓存命中          │
│   ✓ 400 请求错误 / 401 未认证 / 403 无权限 / 404 不存在     │
│   ✓ 500 服务器错误 / 502 网关错误 / 503 服务不可用          │
│                                                             │
│   常见误用：                                                 │
│   ✓ 404 vs 400：资源不存在 vs 请求格式错误                   │
│   ✓ 401 vs 403：未认证 vs 无权限                            │
│   ✓ 301 vs 302：永久 vs 临时                                │
│   ✓ 查询无结果 ≠ 404，应返回 200 + 空列表                   │
│                                                             │
│   下一步：RESTful API 设计原则                               │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```
