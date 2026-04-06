# FastAPI 入门（详细版）

> Python 3.11+

本章讲解 FastAPI 框架基础，包括路由、参数验证和请求处理。

---

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

## 总结

| 知识点 | 说明 |
|---------|------|
| 路径参数 | `/items/{id}` |
| 查询参数 | `?skip=0&limit=10` |
| 请求体 | POST 数据 |
| 响应模型 | response_model |
| HTTP 方法 | GET/POST/PUT/DELETE |
| APIRouter | 路由分组 |