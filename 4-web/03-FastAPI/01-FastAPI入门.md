# 01-FastAPI入门

> Python 3.11+

本章讲解 FastAPI 框架基础，包括路由、参数验证和请求处理。

---

## 概念铺垫

FastAPI 构建在 Starlette（ASGI 框架）与 Pydantic（数据验证）之上，利用 Python 类型注解实现自动参数校验、序列化与 API 文档生成。理解其底层链路对深入使用至关重要：

```
HTTP Request → ASGI Server (Uvicorn) → Starlette (路由/Middleware) → FastAPI (验证/DI) → Endpoint
```

ASGI 是 Python 异步 Web 服务器的标准接口，Starlette 提供轻量级 ASGI 工具包，FastAPI 在其上增加了类型驱动的数据验证和依赖注入系统。

核心设计理念：
- **类型注解驱动**：用 Python type hints 同时完成验证、序列化、文档
- **自动文档生成**：基于 OpenAPI 3.1 规范，零额外配置
- **async 优先**：原生支持异步端点，适配高并发场景

---

### L1 理解层：会用

## 第一部分：快速开始

### 1.1 实际场景

你需要快速构建一个高性能 API 服务，要求自动生成文档、支持异步操作、有良好的类型提示。

**问题：如何用最少的代码创建一个 FastAPI 应用？**

### 1.2 安装

```bash
pip install fastapi uvicorn
```

### 1.3 第一个应用

```python
from fastapi import FastAPI

app: FastAPI = FastAPI()


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Hello, FastAPI!"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

运行：

```bash
uvicorn main:app --reload
```

访问 http://127.0.0.1:8000/docs 查看自动生成的 API 文档。

---

## 第二部分：路径参数

### 2.1 实际场景

API 需要根据 URL 中的 ID 获取对应的资源，如 `/users/1` 获取 ID 为 1 的用户。

**问题：如何从 URL 路径中提取参数？**

### 2.2 基本路径参数

```python
from fastapi import FastAPI

app: FastAPI = FastAPI()


@app.get("/users/{user_id}")
def get_user(user_id: int) -> dict[str, str | int]:
    return {"user_id": user_id, "name": f"User {user_id}"}
```

### 2.3 类型化路径参数

```python
# 整数
@app.get("/posts/{post_id}")
def get_post(post_id: int) -> dict[str, int]:
    return {"post_id": post_id}

# 字符串
@app.get("/users/{username}")
def get_user_by_name(username: str) -> dict[str, str]:
    return {"username": username}

# 浮点数
@app.get("/price/{price}")
def get_price(price: float) -> dict[str, float]:
    return {"price": price, "tax": price * 0.1}

# 布尔值
@app.get("/flag/{flag}")
def get_flag(flag: bool) -> dict[str, bool]:
    return {"flag": flag}
```

### 2.4 路径参数验证

```python
from fastapi import FastAPI, Path

app: FastAPI = FastAPI()


@app.get("/users/{user_id}")
def get_user(
    user_id: int = Path(..., ge=1, le=100, description="用户ID")
) -> dict[str, int]:
    return {"user_id": user_id}


@app.get("/posts/{post_id}")
def get_post(
    post_id: int = Path(..., gt=0, description="文章ID")
) -> dict[str, int]:
    return {"post_id": post_id}
```

---

## 第三部分：查询参数

### 3.1 实际场景

列表接口需要支持分页，如 `/items?skip=0&limit=10`。

**问题：如何处理 URL 查询字符串中的参数？**

### 3.2 基本查询参数

```python
from fastapi import FastAPI

app: FastAPI = FastAPI()


@app.get("/items")
def get_items(skip: int = 0, limit: int = 10) -> dict[str, int | list]:
    return {"skip": skip, "limit": limit, "items": []}
```

### 3.3 可选查询参数

```python
from typing import Any


@app.get("/search")
def search(q: str | None = None, page: int = 1) -> dict[str, Any]:
    return {"query": q, "page": page}
```

### 3.4 查询参数验证

```python
from fastapi import FastAPI, Query

app: FastAPI = FastAPI()


@app.get("/items")
def get_items(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    q: str | None = Query(None, min_length=3, max_length=50)
) -> dict[str, int | str | None]:
    return {"skip": skip, "limit": limit, "query": q}
```

---

## 第四部分：请求体

### 4.1 实际场景

创建用户时需要提交 JSON 数据，包含用户名、邮箱等字段。

**问题：如何接收和验证 JSON 请求体？**

### 4.2 Pydantic 模型

```python
from fastapi import FastAPI
from pydantic import BaseModel

app: FastAPI = FastAPI()


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    quantity: int = 1


@app.post("/items")
def create_item(item: Item) -> dict[str, Item]:
    return {"item": item}
```

### 4.3 多个请求体参数

```python
from fastapi import FastAPI, Body
from pydantic import BaseModel

app: FastAPI = FastAPI()


class User(BaseModel):
    username: str
    email: str


class Item(BaseModel):
    name: str
    price: float


@app.post("/users/items")
def create_user_item(
    user: User,
    item: Item,
    importance: int = Body(...)
) -> dict[str, User | Item | int]:
    return {"user": user, "item": item, "importance": importance}
```

---

## 第五部分：请求对象

### 5.1 实际场景

需要获取完整的请求信息，如请求头、请求方法、客户端 IP 等。

**问题：如何访问原始请求对象？**

### 5.2 完整请求信息

```python
from fastapi import FastAPI, Request

app: FastAPI = FastAPI()


@app.get("/request-info")
async def get_request_info(request: Request) -> dict[str, str | dict]:
    return {
        "method": request.method,
        "url": str(request.url),
        "path": request.url.path,
        "query_params": dict(request.query_params),
        "headers": dict(request.headers),
        "client": request.client.host if request.client else None
    }
```

### 5.3 文件上传

```python
from fastapi import FastAPI, UploadFile, File

app: FastAPI = FastAPI()


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)) -> dict[str, str | int]:
    contents: bytes = await file.read()
    return {
        "filename": file.filename,
        "size": len(contents),
        "content_type": file.content_type
    }


@app.post("/upload-multiple")
async def upload_multiple(files: list[UploadFile] = File(...)) -> dict[str, list]:
    results: list[dict[str, str | int]] = []
    for file in files:
        contents: bytes = await file.read()
        results.append({"filename": file.filename, "size": len(contents)})
    return {"files": results}
```

---

## 第六部分：响应模型

### 6.1 实际场景

返回用户信息时不应包含密码字段，需要定义输出模型控制响应格式。

**问题：如何控制 API 响应的数据结构？**

### 6.2 响应模型定义

```python
from fastapi import FastAPI
from pydantic import BaseModel

app: FastAPI = FastAPI()


class UserIn(BaseModel):
    username: str
    email: str
    password: str


class UserOut(BaseModel):
    id: int
    username: str
    email: str


@app.post("/users", response_model=UserOut)
def create_user(user: UserIn) -> dict[str, str | int]:
    # 创建用户逻辑
    return {"id": 1, "username": user.username, "email": user.email}
```

### 6.3 列表响应

```python
class Item(BaseModel):
    id: int
    name: str
    price: float


@app.get("/items", response_model=list[Item])
def get_items() -> list[dict[str, int | str | float]]:
    return [
        {"id": 1, "name": "Apple", "price": 1.5},
        {"id": 2, "name": "Banana", "price": 0.5}
    ]
```

---

## 第七部分：HTTP 方法

### 7.1 实际场景

RESTful API 需要支持 GET、POST、PUT、DELETE 等多种 HTTP 方法。

**问题：如何为同一资源定义不同的 HTTP 方法？**

### 7.2 所有方法支持

```python
from fastapi import FastAPI

app: FastAPI = FastAPI()


@app.get("/items")
def get_items() -> dict[str, str]:
    return {"method": "GET"}


@app.post("/items")
def create_item() -> dict[str, str]:
    return {"method": "POST"}


@app.put("/items/{item_id}")
def update_item(item_id: int) -> dict[str, str | int]:
    return {"method": "PUT", "item_id": item_id}


@app.patch("/items/{item_id}")
def patch_item(item_id: int) -> dict[str, str | int]:
    return {"method": "PATCH", "item_id": item_id}


@app.delete("/items/{item_id}")
def delete_item(item_id: int) -> dict[str, str | int]:
    return {"method": "DELETE", "item_id": item_id}
```

---

## 第八部分：路由分组

### 8.1 实际场景

API 模块化组织，用户相关路由在 `/api/users`，文章相关路由在 `/api/posts`。

**问题：如何组织和分组路由？**

### 8.2 APIRouter

```python
from fastapi import APIRouter, FastAPI

app: FastAPI = FastAPI()

router: APIRouter = APIRouter(prefix="/api", tags=["API"])


@router.get("/users")
def get_users() -> list:
    return []


@router.post("/users")
def create_user() -> dict[str, int]:
    return {"id": 1}


# 在主应用注册
app.include_router(router)
```

### 8.3 路由版本控制

```python
from fastapi import FastAPI, APIRouter

app: FastAPI = FastAPI()

v1_router: APIRouter = APIRouter(prefix="/v1")
v2_router: APIRouter = APIRouter(prefix="/v2")


@v1_router.get("/users")
def get_users_v1() -> dict[str, str | list]:
    return {"version": "v1", "users": []}


@v2_router.get("/users")
def get_users_v2() -> dict[str, str | list | dict]:
    return {"version": "v2", "users": [], "metadata": {}}


app.include_router(v1_router)
app.include_router(v2_router)
```

---

## 第九部分：完整示例

```python
from fastapi import FastAPI, Path, Query, Body, Request
from pydantic import BaseModel, Field
from typing import Any

app: FastAPI = FastAPI()


# ==================== 模型 ====================
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float = Field(..., gt=0)
    quantity: int = Field(1, ge=0)


class ItemResponse(BaseModel):
    id: int
    name: str
    price: float
    quantity: int


# ==================== 路由 ====================
@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Welcome to FastAPI"}


@app.get("/items", response_model=list[ItemResponse])
def get_items(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    category: str | None = None
) -> list[dict[str, int | str | float]]:
    items: list[dict[str, int | str | float]] = [
        {"id": 1, "name": "Apple", "price": 1.5, "quantity": 10},
        {"id": 2, "name": "Banana", "price": 0.5, "quantity": 20}
    ]
    return items[skip:skip+limit]


@app.get("/items/{item_id}", response_model=ItemResponse)
def get_item(item_id: int = Path(..., ge=1)) -> dict[str, int | str | float]:
    return {"id": item_id, "name": f"Item {item_id}", "price": 9.99, "quantity": 5}


@app.post("/items", response_model=ItemResponse, status_code=201)
def create_item(item: Item) -> dict[str, int | str | float]:
    return {"id": 999, "name": item.name, "price": item.price, "quantity": item.quantity}


@app.put("/items/{item_id}", response_model=ItemResponse)
def update_item(item_id: int, item: Item) -> dict[str, int | str | float]:
    return {"id": item_id, "name": item.name, "price": item.price, "quantity": item.quantity}


@app.delete("/items/{item_id}", status_code=204)
def delete_item(item_id: int) -> None:
    return None


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

---

### L2 实践层：用好

## 最佳实践

### 1. sync vs async 端点选择

```
端点是否需要等待 I/O（数据库、HTTP 调用、文件读取）？
    ├── 否 ──> def（同步端点，放入线程池）
    │         适用：纯计算、内存操作
    │
    └── 是 ──> async def（异步端点，不阻塞事件循环）
              适用：数据库查询、外部 API 调用、WebSocket
```

**关键规则**：如果端点内没有任何 `await`，使用 `def` 即可。混用同步阻塞调用（如 `time.sleep`、同步 HTTP 请求）与 `async def` 会导致事件循环阻塞，其他请求无法处理。

| 场景 | 使用 | 原因 |
|------|------|------|
| 纯内存计算、静态数据 | `def` | 线程池执行，无 I/O 开销 |
| 数据库查询（同步 ORM） | `def` | SQLAlchemy 同步会话 |
| 数据库查询（异步） | `async def` | asyncpg、AsyncSession |
| 外部 HTTP 调用 | `async def` | httpx.AsyncClient |
| 文件读写 | `async def` | aiofiles |
| WebSocket | `async def` | 必须异步 |

### 2. 响应模型规范

- **始终定义 `response_model`**：过滤敏感字段（密码、内部 ID），控制输出格式
- **输入输出模型分离**：`UserCreate`（输入）vs `UserResponse`（输出），各司其职
- **使用 `status_code`**：明确指定创建返回 201、删除返回 204
- **不要直接返回 ORM 对象**：通过 `response_model` 配合 `ConfigDict(from_attributes=True)` 转换

### 3. 路由组织原则

- 单一职责：一个 router 文件一个业务域
- 版本控制：`/v1/`, `/v2/` 前缀隔离，避免破坏性变更影响旧客户端
- prefix + tags 配合：`APIRouter(prefix="/users", tags=["用户管理"])`
- 不要在根应用上堆积路由，超过 5 个端点即考虑拆分

### 4. 参数验证

- 所有路径参数用 `Path(...)` 显式声明约束（ge、le、gt、lt）
- 查询参数用 `Query()` 设置默认值和约束
- 善用 `description` 参数，它会直接出现在 OpenAPI 文档中

## 反模式

| ❌ 反模式 | ✅ 改进 |
|-----------|---------|
| `async def` 内调用 `time.sleep(5)` 或同步 `requests.get()` | 用 `await asyncio.sleep(5)` 或 `httpx.AsyncClient` |
| 不写 `response_model`，直接返回 ORM 对象 | 定义 `UserResponse` 模型，设置 `from_attributes=True` |
| 所有路由写在一个文件 | 按业务域拆分 router 文件，`app.include_router()` 注册 |
| 类型注解写 `Any` 或省略 | 精确注解：`list[ItemResponse]`、`dict[str, int]` |
| 路径参数不设置约束（`user_id: int`） | `user_id: int = Path(..., ge=1)` |
| 返回 `{"status": "ok"}` 用 200 但实际创建了新资源 | `@app.post(..., status_code=201)` |
| 多个相似的 `/items` 路由散落各处 | 用 `APIRouter(prefix="/items", tags=["商品管理"])`聚合 |

## 何时选用什么

| 需求 | 选用方案 |
|------|---------|
| 资源标识从 URL 提取 | 路径参数 `/{resource_id}` |
| 过滤、分页、搜索 | 查询参数 `?status=pending&page=2` |
| 创建/更新数据 | 请求体（Pydantic 模型） |
| 控制返回字段 | `response_model` |
| 访问原始请求信息 | `Request` 对象 |
| 按模块分离路由 | `APIRouter` + `include_router` |
| 文件上传 | `UploadFile` + `File()` |
| 版本兼容 | `APIRouter(prefix="/v1")` + `APIRouter(prefix="/v2")` |

---

### L3 专家层：深入

## 第十部分：L3 专家层

### 10.1 Starlette 底层（ASGI 框架）

FastAPI 构建在 Starlette 之上，Starlette 是一个轻量级 ASGI 框架。理解这一层有助于掌握请求处理的完整生命周期。

**请求处理链路：**

```
HTTP Request
    │
    ▼
┌─────────────────────────────────┐
│         ASGI Server             │
│       (Uvicorn / Hypercorn)      │
└──────────────┬──────────────────┘
               │ ASGI scope / receive / send
               ▼
┌─────────────────────────────────┐
│          Starlette               │
│   ┌─────────────────────────┐    │
│   │    Middleware Stack      │    │
│   │  (CORS / GZip / etc.)   │    │
│   └────────────┬────────────┘    │
│                │                  │
│   ┌────────────▼────────────┐    │
│   │       Router              │    │
│   │  (path → endpoint map)   │    │
│   └────────────┬────────────┘    │
└───────────────┼─────────────────┘
                │
                ▼
┌─────────────────────────────────┐
│           FastAPI                │
│   ┌─────────────────────────┐    │
│   │  Param Parsing & Valid.  │    │
│   │  (Path/Query/Body)       │    │
│   └────────────┬────────────┘    │
│                │                  │
│   ┌────────────▼────────────┐    │
│   │   Dependency Injection   │    │
│   │   (solve graph + cache)  │    │
│   └────────────┬────────────┘    │
│                │                  │
│   ┌────────────▼────────────┐    │
│   │      Endpoint Call       │    │
│   │   (sync → threadpool)    │    │
│   └─────────────────────────┘    │
└─────────────────────────────────┘
```

**关键实现细节：**

- **ASGI 协议**：Starlette 实现 ASGI 3 规范，接收 `scope`（请求信息）、`receive`（协程，获取请求体）、`send`（协程，发送响应）三个参数
- **同步端点处理**：FastAPI 使用 `anyio.to_thread.run_sync` 将同步函数放入线程池执行，避免阻塞事件循环
- **路由匹配**：Starlette 使用 `compile_path` 将路径模板（如 `/items/{item_id}`）编译为正则表达式，实现 O(1) 级别的路由查找

### 10.2 Pydantic 的 JSON Schema 生成机制

FastAPI 的 OpenAPI 文档依赖于 Pydantic 的 JSON Schema 生成。

**Schema 生成流程：**

```
Pydantic Model
    │
    ▼
┌──────────────────────────────┐
│  model_json_schema()         │
│    │                         │
│    ▼                         │
│  ┌────────────────────────┐  │
│  │  Type → Schema Mapping  │  │
│  │  str  → {"type":"string"}│  │
│  │  int  → {"type":"integer"}│ │
│  │  float→ {"type":"number"}│  │
│  │  bool → {"type":"boolean"}│ │
│  │  list → {"type":"array", │  │
│  │          "items": {...}} │  │
│  └────────────────────────┘  │
│    │                         │
│    ▼                         │
│  ┌────────────────────────┐  │
│  │  Field Constraints      │  │
│  │  Field(ge=0) →          │  │
│  │    {"minimum": 0}       │  │
│  │  Field(max_length=50)→  │  │
│  │    {"maxLength": 50}    │  │
│  └────────────────────────┘  │
│    │                         │
│    ▼                         │
│  ┌────────────────────────┐  │
│  │  $defs (nested models)  │  │
│  │  $ref (references)      │  │
│  └────────────────────────┘  │
└──────────────┬───────────────┘
               ▼
        JSON Schema (dict)
               │
               ▼
┌──────────────────────────────┐
│  FastAPI OpenAPI Generator   │
│  → /openapi.json             │
│  → /docs (Swagger UI)        │
│  → /redoc (ReDoc)            │
└──────────────────────────────┘
```

**核心方法：**
- `BaseModel.model_json_schema()`：v2 方法（v1 为 `schema()`），返回符合 JSON Schema Draft 2020-12 规范的字典
- `$defs`：嵌套模型的定义被提取到顶层 `$defs` 中，通过 `$ref` 引用避免重复
- `mode` 参数：`'validation'`（输入）和 `'serialization'`（输出）可生成不同的 Schema

### 10.3 FastAPI 的 OpenAPI 文档自动生成原理

FastAPI 在应用启动时自动构建 OpenAPI schema：

```python
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

app: FastAPI = FastAPI()

# 首次访问 /openapi.json 时触发
def custom_openapi() -> dict:
    if app.openapi_schema:
        return app.openapi_schema  # 缓存结果

    openapi_schema: dict = get_openapi(
        title="My API",
        version="1.0.0",
        routes=app.routes,  # 遍历所有路由
    )
    app.openapi_schema = openapi_schema
    return openapi_schema

app.openapi = custom_openapi
```

**生成步骤：**
1. 遍历 `app.routes`，收集所有 `APIRoute` 对象
2. 从路由的 `response_model`、参数类型注解、`Field` 约束中提取 Schema
3. 合并所有模型的 JSON Schema 到 `$defs`
4. 输出标准 OpenAPI 3.1.0 格式

### 10.4 性能考量

| 维度 | 说明 | 建议 |
|------|------|------|
| 路由匹配 | 正则编译后 O(1) | 路由数量对性能影响极小 |
| 同步端点 | 通过线程池执行 | I/O 密集型用 `async def` |
| 验证开销 | Pydantic v2 使用 Rust 核心 | 大批量数据验证性能优于 v1 10-40 倍 |
| OpenAPI 生成 | 首次访问时构建并缓存 | 生产环境无额外开销 |
| 内存占用 | 每个路由注册一个 route 对象 | 数千路由仍可接受 |

### 10.5 设计动机

| 设计选择 | 原因 |
|----------|------|
| 基于 Starlette | 复用成熟的 ASGI 生态，专注数据验证与依赖注入 |
| 类型注解驱动 | 利用 Python 3.6+ 的 type hints，减少重复代码 |
| 自动文档生成 | OpenAPI 是行业标准，手动维护易出错 |
| async 优先 | 现代 Web 框架必须支持高并发 I/O |

### 10.6 知识关联

```
                    FastAPI 入门
                         │
        ┌────────────────┼────────────────┐
        ▼                ▼                ▼
    Starlette      Pydantic         OpenAPI
    (ASGI 层)     (验证层)         (文档层)
        │                │                │
        ▼                ▼                ▼
    Uvicorn      JSON Schema       Swagger UI
    (服务器)     (数据描述)         ReDoc
        │                │                │
        └────────────────┼────────────────┘
                         ▼
                  02-Pydantic 模型
                  03-依赖注入
                  04-数据库集成
```

---

## 渐进式代码示例

### Level 1：最简应用（单文件原型）

适合快速原型验证、学习单个 API 行为：

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"id": user_id, "name": f"User_{user_id}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=8000)
```

### Level 2：结构化应用（分模块）

适合小型项目，引入路由拆分和请求体验证：

```
project/
├── main.py           # 入口
├── routers/
│   ├── users.py      # 用户路由
│   └── items.py      # 商品路由
└── schemas/
    ├── user.py       # Pydantic 模型
    └── item.py
```

```python
# routers/users.py
from fastapi import APIRouter
from schemas.user import UserCreate, UserResponse

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserResponse, status_code=201)
def create_user(user: UserCreate):
    return {"id": 1, **user.model_dump()}

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int):
    return {"id": user_id, "name": "test", "email": "t@t.com"}
```

```python
# main.py
from fastapi import FastAPI
from routers import users, items

app = FastAPI(title="My API", version="1.0.0")
app.include_router(users.router)
app.include_router(items.router)
```

### Level 3：进阶应用（中间件 + 生命周期）

适合中型项目，引入中间件、lifespan 事件、异常处理器：

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import time


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时
    print("Starting up...")
    yield
    # 关闭时
    print("Shutting down...")


app = FastAPI(lifespan=lifespan)


@app.middleware("http")
async def timing_middleware(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    elapsed = time.perf_counter() - start
    response.headers["X-Response-Time"] = f"{elapsed:.4f}"
    return response


@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    return JSONResponse(status_code=400, content={"detail": str(exc)})
```

### Level 4：生产级结构（分层架构）

适合大型团队，引入 repository 模式、service 层、配置管理：

```
project/
├── main.py                 # 应用入口
├── api/
│   ├── deps.py             # 依赖注入
│   └── v1/
│       ├── router.py       # 路由聚合
│       ├── users.py        # 用户端点
│       └── items.py        # 商品端点
├── core/
│   ├── config.py           # 配置管理（pydantic-settings）
│   └── security.py         # 认证逻辑
├── models/
│   └── user.py             # ORM 模型
├── schemas/
│   └── user.py             # Pydantic 模型
├── services/
│   └── user.py             # 业务逻辑
├── repositories/
│   └── user.py             # 数据访问
└── db/
    ├── session.py          # 数据库会话
    └── base.py             # 声明式基类
```

```python
# core/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./app.db"
    SECRET_KEY: str
    ENVIRONMENT: str = "development"
    UVICORN_WORKERS: int = 4

    model_config = {"env_file": ".env"}

settings = Settings()
```

```python
# api/v1/users.py
from fastapi import APIRouter, Depends
from api.deps import get_current_user, get_db
from services.user import UserService
from schemas.user import UserCreate, UserResponse

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserResponse, status_code=201)
async def create_user(
    user_in: UserCreate,
    db=Depends(get_db),
):
    service = UserService(db)
    return await service.create(user_in)

@router.get("/me", response_model=UserResponse)
async def read_me(
    current_user=Depends(get_current_user),
    db=Depends(get_db),
):
    service = UserService(db)
    return await service.get(current_user.id)
```

---

## 常见坑点排查

### 坑点 1：`async def` 端点内调用同步阻塞 I/O

**症状：** API 响应时间极长，并发请求全部超时

```python
# ❌ 错误代码
import time

@app.get("/slow")
async def slow_endpoint():
    time.sleep(5)  # 阻塞整个事件循环 5 秒！
    return {"status": "done"}
```

**错误输出：**
```
并发发送 10 个请求，第一个请求耗时 5s，后续 9 个请求累计耗时 5s~10s+
```

**根因分析：** `time.sleep()` 是同步阻塞调用，在 `async def` 中直接调用会阻塞 asyncio 事件循环，导致在此期间所有其他协程无法调度执行。

**修复方案：**

```python
import asyncio

@app.get("/slow")
async def slow_endpoint():
    await asyncio.sleep(5)  # ✅ 释放控制权给事件循环
    return {"status": "done"}
```

| 预防措施 | 说明 |
|---------|------|
| 事件循环阻塞检测 | `PYTHONASYNCIODEBUG=1` 开启 asyncio 调试模式，检测长时间阻塞 |
| 使用 `anyio.to_thread.run_sync` | 将同步操作显式放入线程池 |
| 代码审查 checklist | 确认 `async def` 端点中所有 I/O 调用都是异步的 |

### 坑点 2：路径参数顺序导致路由匹配错误

**症状：** `/items/featured` 接口返回 422 验证错误或匹配到错误的处理函数

```python
# ❌ 错误：具体路径定义在动态路径之后
@app.get("/items/{item_id}")
def get_item(item_id: int):
    return {"id": item_id}

@app.get("/items/featured")
def get_featured_items():
    return {"items": []}

# GET /items/featured → 422: "featured" 不是有效的 int
```

**根因分析：** Starlette 按路由注册顺序匹配，`/items/{item_id}` 先注册，`"featured"` 被当作 `item_id` 尝试转为 `int` 而失败。

**修复方案：**

```python
# ✅ 正确：固定路径定义在动态路径之前
@app.get("/items/featured")
def get_featured_items():
    return {"items": []}

@app.get("/items/{item_id}")
def get_item(item_id: int):
    return {"id": item_id}
```

### 坑点 3：`response_model` 遗漏导致敏感字段泄露

**症状：** 用户查询接口意外返回了 `hashed_password`、`internal_id` 等敏感字段

```python
# ❌ 直接返回 ORM 对象，包含所有字段
@app.get("/users/{user_id}")
def get_user(user_id: int, db=Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    return user  # 返回了 hashed_password, internal_id 等
```

**根因分析：** 当不使用 `response_model` 时，FastAPI 不会过滤输出字段。ORM 对象的所有属性都会被序列化到响应中。

**修复方案：**

```python
class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    model_config = {"from_attributes": True}

@app.get("/users/{user_id}", response_model=UserResponse)  # ✅
def get_user(user_id: int, db=Depends(get_db)):
    return db.query(User).filter(User.id == user_id).first()
```

### 坑点 4：文件上传未设置大小限制

**症状：** 用户上传超大文件导致服务器内存耗尽（OOM）

```python
# ❌ 无大小限制
@app.post("/upload")
async def upload(file: UploadFile):  # 可接收任意大小文件
    contents = await file.read()     # 全部读入内存
    return {"size": len(contents)}
```

**修复方案：**

```python
from fastapi import File
SECRET_KEY = "supersecret"  # for illustration - use env var

@app.post("/upload")
async def upload(file: UploadFile = File(..., max_length=10 * 1024 * 1024)):  # ✅ 限 10MB
    contents = await file.read()
    return {"size": len(contents)}
```

### 坑点排查速查表

| 症状 | 可能原因 | 排查命令/方法 |
|------|---------|-------------|
| 接口返回 422 | Pydantic 验证失败 | 查看 `/docs` 中 Schema 示例，检查请求体格式 |
| `async def` 端点响应极慢 | 事件循环被阻塞 | `PYTHONASYNCIODEBUG=1` 检测慢回调 |
| 数据库连接超时 | 连接池耗尽 | `SQLALCHEMY_WARN_20=1` 检查连接创建/释放 |
| Swagger UI 加载失败 | CORS 或静态资源 | 检查浏览器 DevTools Network 面板 |
| `reload` 模式不生效 | 文件监听路径错误 | 确保 `--reload-dir` 指向正确的包目录 |
| POST 请求返回 405 | 方法不允许 | 检查是否有对应 `@app.post` 装饰器 |

---

## 调试与排错技巧

### 完整调试会话：排查 500 Internal Server Error

**场景：** 创建一个用户时，服务端返回 500 错误，日志中没有任何有用信息。

**步骤 1：开启详细日志**

```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("uvicorn.error")
logger.setLevel(logging.DEBUG)
```

同时启动 uvicorn 时传入额外参数：

```bash
uvicorn main:app --reload --log-level debug --access-log
```

**步骤 2：添加全局异常处理器捕获未处理异常**

```python
import traceback
from fastapi import Request
from fastapi.responses import JSONResponse

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    traceback.print_exc()  # 打印完整堆栈
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc), "type": type(exc).__name__},
    )
```

**步骤 3：使用中间件记录请求上下文**

```python
@app.middleware("http")
async def debug_middleware(request: Request, call_next):
    print(f"\n[DEBUG] {request.method} {request.url}")
    print(f"[DEBUG] Headers: {dict(request.headers)}")
    body = await request.body()
    print(f"[DEBUG] Body: {body[:500]}")
    # 重建 request（body 只能读一次）
    async def receive():
        return {"type": "http.request", "body": body}
    request._receive = receive
    response = await call_next(request)
    print(f"[DEBUG] Status: {response.status_code}")
    return response
```

**步骤 4：使用 IPDB 进行交互式调试**

```python
@app.post("/users")
async def create_user(user: UserCreate):
    import ipdb; ipdb.set_trace()  # 断点
    # ... 业务逻辑
```

**步骤 5：使用 `pdb` 追踪特定条件下的请求**

```python
@app.post("/users")
async def create_user(user: UserCreate):
    if user.email == "debug@test.com":
        breakpoint()  # Python 3.7+ 内置断点
    return {"id": 1, **user.model_dump()}
```

### 常见调试工具速查

| 工具 | 用途 | 用法 |
|------|------|------|
| `uvicorn --log-level debug` | 查看请求/响应详细日志 | 启动参数 |
| `breakpoint()` / `pdb` | 交互式断点调试 | 代码中插入 |
| `traceback.print_exc()` | 打印完整异常堆栈 | 异常处理器中 |
| `fastapi.testclient.TestClient` | 单元测试 + 请求模拟 | pytest 测试用例 |
| `curl -v` | 查看完整 HTTP 交互 | 命令行测试 |
| `httpx` + `asyncio` | 异步并发测试 | 压力测试脚本 |
| `/docs` Swagger UI | 交互式 API 测试 | 浏览器访问 |
| `middleware` + `print` | 请求/响应日志 | 自定义中间件 |

### 性能分析技巧

```python
import cProfile
import pstats
import io

def profile_endpoint():
    pr = cProfile.Profile()
    pr.enable()
    # ... 测试代码 ...
    pr.disable()
    s = io.StringIO()
    ps = pstats.Stats(pr, stream=s).sort_stats("cumulative")
    ps.print_stats(20)
    print(s.getvalue())
```

---

## 进阶用法

### ASGI vs WSGI 深度对比

ASGI (Asynchronous Server Gateway Interface) 和 WSGI (Web Server Gateway Interface) 是 Python Web 服务器的两种接口标准。

```
WSGI (同步模型)：
Client → Web Server (Gunicorn) → WSGI App (Flask/Django)
         每个请求占用一个线程/进程
         线程数 = 并发上限
         阻塞 I/O 会饿死其他请求

ASGI (异步模型)：
Client → ASGI Server (Uvicorn) → ASGI App (FastAPI/Starlette)
         事件循环管理所有请求
         并发上限 = 事件循环吞吐
         阻塞 I/O 不会饿死其他请求（协程切换）
```

| 维度 | WSGI | ASGI |
|------|------|------|
| 并发模型 | 同步（线程/进程池） | 异步（事件循环 + 协程） |
| 协议支持 | HTTP 1.x | HTTP 1.x / 2 / WebSocket / SSE |
| C10K 场景 | 受限于线程数（~几百） | 轻松 10K+ 并发连接 |
| 线程开销 | 每线程 ~8MB 栈 | 每协程 ~KB 级 |
| 代表服务器 | Gunicorn, uWSGI | Uvicorn, Hypercorn, Daphne |
| 代表框架 | Flask, Django (WSGI 模式) | FastAPI, Starlette, Django (ASGI 模式) |
| 兼容性 | 所有 Python Web 框架 | 仅 ASGI 框架 |
| 接口参数 | `(environ, start_response)` | `(scope, receive, send)` |

**ASGI 接口三要素：**

```python
async def asgi_app(scope, receive, send):
    """
    scope:   dict — 连接信息（type, method, path, headers 等）
    receive: awaitable — 接收客户端消息（HTTP body / WebSocket message）
    send:    awaitable — 发送响应消息
    """
    assert scope["type"] == "http"
    await send({
        "type": "http.response.start",
        "status": 200,
        "headers": [(b"content-type", b"application/json")],
    })
    await send({
        "type": "http.response.body",
        "body": b'{"status": "ok"}',
    })
```

### Uvicorn Worker 类型精讲

Uvicorn 支持多种 worker 实现，每种针对不同的性能场景：

```
uvicorn 启动模式：
    ├── 单进程 (默认)
    │     uvicorn main:app
    │     适用：开发环境、低负载
    │
    ├── --workers N（多进程）
    │     uvicorn main:app --workers 4
    │     适用：生产环境，充分利用多核 CPU
    │     每个 worker 独立的事件循环 + 连接池
    │
    └── Gunicorn + uvicorn workers
          gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
          适用：更强的进程管理、优雅重启、信号处理
```

| Worker 类型 | 底层实现 | 适用场景 |
|------------|---------|---------|
| 默认 (uvloop + httptools) | Cython 优化的 uvloop（替代 asyncio 事件循环） + 纯 C httptools（HTTP 解析） | 生产环境，追求极限性能 |
| `--loop asyncio` | 标准库 asyncio | 兼容性优先，或 Windows 环境 |
| `--http h11` | 纯 Python HTTP 解析（h11 库） | httptools 不可用时降级 |
| `UvicornWorker`（Gunicorn） | Gunicorn 进程管理 + Uvicorn 事件循环 | 需要 Gunicorn 的进程管理能力 |
| `UvicornH11Worker`（Gunicorn） | Gunicorn + h11 HTTP 解析 | 纯 Python 环境 |

uvloop 性能提升原理：

```
标准 asyncio 事件循环：
  Python 实现，每次 I/O 就绪检查都有 Python 函数调用开销

uvloop：
  基于 libuv（Node.js 的事件循环引擎），C 语言实现
  核心 I/O 就绪检查在 C 层执行，避免 Python 调用开销
  性能接近 Go/Node.js 的事件循环水平
```

```python
# 查看当前使用的实现
import asyncio
import uvicorn

# uvloop 可用时会自动启用
if hasattr(asyncio, "all_tasks"):  # uvloop 特征
    print("Running with uvloop + httptools")

# 显式配置
uvicorn.run(
    "main:app",
    host="0.0.0.0",
    port=8000,
    loop="uvloop",        # 事件循环
    http="httptools",     # HTTP 解析器
    workers=4,            # 进程数
    backlog=2048,         # TCP 连接队列长度
    limit_concurrency=1000,  # 最大并发连接数
    limit_max_requests=10000,  # 每个 worker 处理 N 个请求后重启
)
```

### 请求/响应生命周期精确时间线

```
时间线 (ms)：
│
├─ T0    ── TCP 连接到达，Uvicorn accept()
├─ T1    ── httptools 解析 HTTP 请求行 + 请求头
├─ T2    ── 构造 ASGI scope dict
├─ T3    ── 外层中间件 (CORS) 开始
├─ T4    ── 内层中间件 (Timing) 开始
├─ T5    ── Starlette Router 路由匹配
├─ T6    ── FastAPI 参数解析 & Pydantic 验证
├─ T7    ── FastAPI 依赖注入图解析 & 执行
├─ T8    ── Endpoint 函数执行
│          │
│          ├── T8.1  数据库查询 (await)
│          ├── T8.2  Redis 缓存读取 (await)
│          └── T8.3  第三方 API 调用 (await)
│
├─ T9    ── 响应构造 & response_model 验证
├─ T10   ── 内层中间件 响应后处理
├─ T11   ── GZip 压缩 (如果响应体 > minimum_size)
├─ T12   ── 外层中间件 CORS headers 添加
├─ T13   ── httptools 序列化 HTTP 响应
└─ T14   ── TCP 发送完成
```

### FastAPI vs Flask vs Django-Ninja 决策矩阵

| 维度 | FastAPI | Flask | Django-Ninja |
|------|---------|-------|-------------|
| **异步支持** | 原生 async/await，一等公民 | Flask 2.0+ 支持 async，生态仍以同步为主 | 原生 async，建立在 Django 异步能力之上 |
| **类型注解** | Pydantic 驱动，自动验证+文档 | 需要手动或 marshmallow | Pydantic 驱动（FastAPI 同风格） |
| **OpenAPI 文档** | 自动生成 /docs + /redoc | 需 flask-swagger 等第三方 | 自动生成（FastAPI 同风格） |
| **性能 (RPS)** | ~25,000 (async) | ~3,500 (sync) / ~5,000 (async) | ~20,000 (async) |
| **依赖注入** | 内置，图解析，yield 生命周期 | 需 inject 等第三方 | 通过 Django 中间件 + 装饰器模拟 |
| **WebSocket** | 原生支持 | 需 flask-socketio | 原生支持 |
| **文件上传** | UploadFile，异步流式 | request.files | Django File 对象 |
| **生态/插件** | 快速增长 | 最成熟，插件最多 | Django 生态（ORM、Admin、Auth） |
| **学习曲线** | 平缓（类型注解驱动） | 平缓 | 需先理解 Django |
| **适用场景** | 高性能 API、微服务、ML 推理服务 | CMS、管理后台、快速原型 | Django 项目增加高质量 API |
| **数据库 ORM** | 自由选择 (SQLAlchemy, asyncpg) | SQLAlchemy (最常用) | Django ORM (内置) |
| **认证** | 内置 OAuth2 + 自定义依赖 | Flask-Login / Flask-JWT-Extended | Django 认证系统 |
| **生产部署** | Uvicorn + Gunicorn | Gunicorn / uWSGI | Daphne / Uvicorn + ASGI |

**选型决策流程：**

```
你的项目需求是什么？

├── 纯 API/微服务
│   ├── 需要高性能 + async → FastAPI
│   ├── Django 已有项目 → Django-Ninja
│   └── 简单快速 → FastAPI (最简配置)
│
├── 全栈 Web (SSR + API)
│   ├── 重型框架 + Admin → Django + Django-Ninja
│   ├── 轻量灵活 → Flask
│   └── 现代 async → FastAPI + Jinja2
│
├── ML/AI 推理服务 → FastAPI（async + Pydantic 完美匹配）
├── 实时通信 (WebSocket/SSE) → FastAPI
└── 企业内部工具 → Flask（生态成熟）
```

### 性能基准测试

使用 `wrk` 进行压力测试，对比不同配置的吞吐量：

```bash
# 安装 wrk: brew install wrk (macOS) / apt install wrk (Linux)

# 测试同步端点
wrk -t4 -c100 -d30s http://localhost:8000/items

# 测试异步端点
wrk -t4 -c100 -d30s http://localhost:8000/async-items
```

| 配置 | 请求/sec | 平均延迟 | P99 延迟 |
|------|---------|---------|---------|
| 单进程 Uvicorn (同步端点) | ~3,500 | 28ms | 120ms |
| 单进程 Uvicorn (async 端点) | ~8,200 | 12ms | 45ms |
| 4 workers (sync) | ~12,000 | 8ms | 35ms |
| 4 workers (async) | ~28,000 | 3.5ms | 12ms |
| 4 workers + uvloop | ~35,000 | 2.8ms | 10ms |

> 注：实际数值取决于硬件、端点复杂度、数据库延迟。以上为本地 M1 Mac 上简单 JSON 响应的参考值。

### 第三方集成：httpx 异步 HTTP 客户端

```python
import httpx
from fastapi import FastAPI

app = FastAPI()

@app.get("/proxy/github/{username}")
async def proxy_github(username: str):
    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(
            f"https://api.github.com/users/{username}",
            headers={"Accept": "application/vnd.github.v3+json"},
        )
        response.raise_for_status()
        return response.json()
```

### 第三方集成：structlog 结构化日志

```python
import structlog
from fastapi import Request

logger = structlog.get_logger()

@app.middleware("http")
async def structlog_middleware(request: Request, call_next):
    structlog.contextvars.bind_contextvars(
        method=request.method,
        path=request.url.path,
        client=request.client.host if request.client else None,
    )
    response = await call_next(request)
    logger.info(
        "request_completed",
        status_code=response.status_code,
        user_agent=request.headers.get("user-agent"),
    )
    structlog.contextvars.clear_contextvars()
    return response
```

---

## 总结

| 知识点 | 说明 |
|---------|------|
| 路径参数 | `/items/{id}` |
| 查询参数 | `?skip=0&limit=10` |
| 请求体 | POST 数据 |
| 响应模型 | response_model |
| HTTP 方法 | GET/POST/PUT/DELETE |
| APIRouter | 路由分组 |
