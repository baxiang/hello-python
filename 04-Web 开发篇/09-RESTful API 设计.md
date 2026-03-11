# 第 9 章：RESTful API 设计

掌握 RESTful API 设计原则和最佳实践。

---

## 本章目标

- 理解 REST 架构风格
- 掌握 API 设计原则
- 学会版本控制
- 实现分页和过滤
- 文档化 API

---

## 9.1 REST 基础

### 什么是 REST？

REST（Representational State Transfer）是一种架构风格，用于设计网络应用程序。

### REST 约束

1. **客户端-服务器分离**
2. **无状态**
3. **可缓存**
4. **分层系统**
5. **统一接口**

### 资源命名

```
# 资源命名规范
/users              # 用户集合
/users/123          # 特定用户
/users/123/posts    # 用户的文章
/posts              # 文章集合
/posts/456/comments # 文章的评论
```

### HTTP 方法映射

| 方法 | 用途 | 示例 |
|------|------|------|
| GET | 获取资源 | GET /users |
| POST | 创建资源 | POST /users |
| PUT | 完整更新 | PUT /users/123 |
| PATCH | 部分更新 | PATCH /users/123 |
| DELETE | 删除资源 | DELETE /users/123 |

---

## 9.2 API 设计最佳实践

### 响应格式

```json
// 成功响应
{
    "success": true,
    "data": {
        "id": 1,
        "name": "张三"
    },
    "message": "操作成功"
}

// 错误响应
{
    "success": false,
    "error": {
        "code": 400,
        "message": "请求参数错误",
        "details": []
    }
}

// 分页响应
{
    "success": true,
    "data": [...],
    "pagination": {
        "page": 1,
        "page_size": 20,
        "total": 100,
        "total_pages": 5
    }
}
```

### 状态码使用

```python
# 2xx 成功
200 OK - GET 成功
201 Created - POST 创建成功
204 No Content - DELETE 成功

# 4xx 客户端错误
400 Bad Request - 请求参数错误
401 Unauthorized - 未认证
403 Forbidden - 无权限
404 Not Found - 资源不存在
409 Conflict - 资源冲突

# 5xx 服务器错误
500 Internal Server Error - 服务器错误
503 Service Unavailable - 服务不可用
```

### 完整示例

```python
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

app = FastAPI()

# 数据模型
class User(BaseModel):
    id: int
    name: str
    email: str

class UserCreate(BaseModel):
    name: str
    email: str

# 模拟数据库
users_db = {}
user_id_counter = 1

# ============ 用户 API ============

# 获取用户列表（支持分页和过滤）
@app.get("/api/v1/users", response_model=dict)
def get_users(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    name: Optional[str] = None,
    email: Optional[str] = None
):
    # 过滤
    filtered = list(users_db.values())
    
    if name:
        filtered = [u for u in filtered if name.lower() in u['name'].lower()]
    if email:
        filtered = [u for u in filtered if email.lower() in u['email'].lower()]
    
    # 分页
    total = len(filtered)
    start = (page - 1) * page_size
    end = start + page_size
    items = filtered[start:end]
    
    return {
        "success": True,
        "data": items,
        "pagination": {
            "page": page,
            "page_size": page_size,
            "total": total,
            "total_pages": (total + page_size - 1) // page_size
        }
    }

# 获取单个用户
@app.get("/api/v1/users/{user_id}", response_model=dict)
def get_user(user_id: int):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    return {
        "success": True,
        "data": users_db[user_id]
    }

# 创建用户
@app.post("/api/v1/users", response_model=dict, status_code=201)
def create_user(user: UserCreate):
    global user_id_counter
    
    # 检查邮箱唯一
    for u in users_db.values():
        if u['email'] == user.email:
            raise HTTPException(status_code=409, detail="邮箱已被使用")
    
    user_id = user_id_counter
    user_id_counter += 1
    
    new_user = {
        "id": user_id,
        "name": user.name,
        "email": user.email,
        "created_at": datetime.now().isoformat()
    }
    
    users_db[user_id] = new_user
    
    return {
        "success": True,
        "data": new_user,
        "message": "用户创建成功"
    }

# 完整更新用户
@app.put("/api/v1/users/{user_id}", response_model=dict)
def update_user(user_id: int, user: UserCreate):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    # 检查邮箱唯一（排除自己）
    for uid, u in users_db.items():
        if uid != user_id and u['email'] == user.email:
            raise HTTPException(status_code=409, detail="邮箱已被使用")
    
    users_db[user_id].update({
        "name": user.name,
        "email": user.email,
        "updated_at": datetime.now().isoformat()
    })
    
    return {
        "success": True,
        "data": users_db[user_id],
        "message": "用户更新成功"
    }

# 删除用户
@app.delete("/api/v1/users/{user_id}", status_code=204)
def delete_user(user_id: int):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    del users_db[user_id]
    
    return None
```

---

## 9.3 API 版本控制

### URL 版本控制

```python
# v1 版本
@app.get("/api/v1/users")
def get_users_v1():
    return {"version": "v1", "data": []}

# v2 版本
@app.get("/api/v2/users")
def get_users_v2():
    return {"version": "v2", "data": [], "metadata": {}}
```

### Header 版本控制

```python
from fastapi import Header

@app.get("/api/users")
def get_users(
    accept_version: str = Header("v1", regex="^v[12]$")
):
    if accept_version == "v1":
        return {"version": "v1", "data": []}
    return {"version": "v2", "data": [], "metadata": {}}
```

---

## 9.4 过滤和排序

### 过滤参数

```python
@app.get("/api/v1/users")
def get_users(
    # 过滤参数
    name_contains: Optional[str] = None,
    email_contains: Optional[str] = None,
    is_active: Optional[bool] = None,
    
    # 排序参数
    sort_by: str = "created_at",
    sort_order: str = "asc"
):
    query = list(users_db.values())
    
    # 过滤
    if name_contains:
        query = [u for u in query if name_contains.lower() in u['name'].lower()]
    if email_contains:
        query = [u for u in query if email_contains.lower() in u['email'].lower()]
    if is_active is not None:
        query = [u for u in query if u.get('is_active', True) == is_active]
    
    # 排序
    reverse = sort_order.lower() == "desc"
    query.sort(key=lambda x: x.get(sort_by, ''), reverse=reverse)
    
    return {"data": query}
```

---

## 9.5 API 文档

### OpenAPI 文档

FastAPI 自动生成 OpenAPI 文档：

- **Swagger UI**: `/docs`
- **ReDoc**: `/redoc`

### 自定义文档

```python
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

app = FastAPI(
    title="用户管理系统 API",
    description="提供用户管理的 RESTful API 接口",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# 自定义 OpenAPI schema
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title="用户管理系统 API",
        version="1.0.0",
        description="提供用户管理的 RESTful API 接口",
        routes=app.routes
    )
    
    # 添加自定义信息
    openapi_schema["info"]["contact"] = {
        "name": "API Support",
        "email": "support@example.com"
    }
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
```

---

## 9.6 错误处理

### 统一错误响应

```python
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

app = FastAPI()

# 自定义错误类
class APIException(Exception):
    def __init__(self, code: int, message: str, details: dict = None):
        self.code = code
        self.message = message
        self.details = details or []

# 注册异常处理器
@app.exception_handler(APIException)
async def api_exception_handler(request: Request, exc: APIException):
    return JSONResponse(
        status_code=exc.code,
        content={
            "success": False,
            "error": {
                "code": exc.code,
                "message": exc.message,
                "details": exc.details
            }
        }
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=400,
        content={
            "success": False,
            "error": {
                "code": 400,
                "message": "请求参数验证失败",
                "details": exc.errors()
            }
        }
    )

# 使用自定义异常
@app.get("/users/{user_id}")
def get_user(user_id: int):
    if user_id < 0:
        raise APIException(400, "ID 不能为负数")
    return {"id": user_id}
```

---

## 本章总结

### 学到的技能

| 技能 | 说明 |
|------|------|
| REST 原则 | 架构风格和约束 |
| 资源命名 | URL 设计 |
| 响应格式 | 统一响应结构 |
| 版本控制 | URL/Header 版本 |
| 过滤排序 | 查询参数 |
| 文档 | OpenAPI |

### 下一步

在 [第 10 章](./10-WebSocket 通信.md) 中，我们将学习 WebSocket 实时通信。

---

[← 上一章](./08-FastAPI 进阶.md) | [下一章 →](./10-WebSocket 通信.md)