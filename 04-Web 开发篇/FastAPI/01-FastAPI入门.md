# FastAPI 路由与参数

深入掌握 FastAPI 路由系统，包括路径参数、查询参数、请求体等。

---

## 1. 快速开始

### 1.1 安装

```bash
pip install fastapi uvicorn
```

### 1.2 第一个应用

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
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

## 2. 路径参数

### 2.1 基本路径参数

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id, "name": f"User {user_id}"}
```

### 2.2 类型化路径参数

```python
# 整数
@app.get("/posts/{post_id}")
def get_post(post_id: int):
    return {"post_id": post_id}

# 字符串
@app.get("/users/{username}")
def get_user(username: str):
    return {"username": username}

# 浮点数
@app.get("/price/{price}")
def get_price(price: float):
    return {"price": price, "tax": price * 0.1}

# 布尔值
@app.get("/flag/{flag}")
def get_flag(flag: bool):
    return {"flag": flag}
```

### 2.3 路径参数验证

```python
from fastapi import FastAPI, Path

app = FastAPI()

@app.get("/users/{user_id}")
def get_user(
    user_id: int = Path(..., ge=1, le=100, description="用户ID")
):
    return {"user_id": user_id}

@app.get("/posts/{post_id}")
def get_post(
    post_id: int = Path(..., gt=0, description="文章ID")
):
    return {"post_id": post_id}
```

---

## 3. 查询参数

### 3.1 基本查询参数

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/items")
def get_items(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit, "items": []}
```

### 3.2 可选查询参数

```python
from typing import Optional

@app.get("/search")
def search(q: Optional[str] = None, page: int = 1):
    return {"query": q, "page": page}
```

### 3.3 查询参数验证

```python
from fastapi import FastAPI, Query

app = FastAPI()

@app.get("/items")
def get_items(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    q: str = Query(None, min_length=3, max_length=50)
):
    return {"skip": skip, "limit": limit, "query": q}
```

---

## 4. 请求体

### 4.1 Pydantic 模型

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str = None
    price: float
    quantity: int = 1

@app.post("/items")
def create_item(item: Item):
    return {"item": item}
```

### 4.2 多个请求体参数

```python
from fastapi import FastAPI, Body
from pydantic import BaseModel

app = FastAPI()

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
):
    return {"user": user, "item": item, "importance": importance}
```

---

## 5. 请求对象

### 5.1 完整请求信息

```python
from fastapi import FastAPI, Request

app = FastAPI()

@app.get("/request-info")
async def get_request_info(request: Request):
    return {
        "method": request.method,
        "url": str(request.url),
        "path": request.url.path,
        "query_params": dict(request.query_params),
        "headers": dict(request.headers),
        "client": request.client.host if request.client else None
    }
```

### 5.2 文件上传

```python
from fastapi import FastAPI, UploadFile, File

app = FastAPI()

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    return {
        "filename": file.filename,
        "size": len(contents),
        "content_type": file.content_type
    }

@app.post("/upload-multiple")
async def upload_multiple(files: list[UploadFile] = File(...)):
    results = []
    for file in files:
        contents = await file.read()
        results.append({"filename": file.filename, "size": len(contents)})
    return {"files": results}
```

---

## 6. 响应模型

### 6.1 响应模型定义

```python
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, List

app = FastAPI()

class UserIn(BaseModel):
    username: str
    email: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    email: str

@app.post("/users", response_model=UserOut)
def create_user(user: UserIn):
    # 创建用户逻辑
    return {"id": 1, "username": user.username, "email": user.email}
```

### 6.2 列表响应

```python
class Item(BaseModel):
    id: int
    name: str
    price: float

@app.get("/items", response_model=List[Item])
def get_items():
    return [
        {"id": 1, "name": "Apple", "price": 1.5},
        {"id": 2, "name": "Banana", "price": 0.5}
    ]
```

---

## 7. HTTP 方法

### 7.1 所有方法支持

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/items")
def get_items():
    return {"method": "GET"}

@app.post("/items")
def create_item():
    return {"method": "POST"}

@app.put("/items/{item_id}")
def update_item(item_id: int):
    return {"method": "PUT", "item_id": item_id}

@app.patch("/items/{item_id}")
def patch_item(item_id: int):
    return {"method": "PATCH", "item_id": item_id}

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    return {"method": "DELETE", "item_id": item_id}

@app.options("/items")
def options_items():
    return {"method": "OPTIONS"}
```

---

## 8. 路由分组

### 8.1 APIRouter

```python
from fastapi import APIRouter

router = APIRouter(prefix="/api", tags=["API"])

@router.get("/users")
def get_users():
    return []

@router.post("/users")
def create_user():
    return {"id": 1}

# 在主应用注册
app.include_router(router)
```

### 8.2 路由版本控制

```python
from fastapi import FastAPI, APIRouter

app = FastAPI()

v1_router = APIRouter(prefix="/v1")
v2_router = APIRouter(prefix="/v2")

@v1_router.get("/users")
def get_users_v1():
    return {"version": "v1", "users": []}

@v2_router.get("/users")
def get_users_v2():
    return {"version": "v2", "users": [], "metadata": {}}

app.include_router(v1_router)
app.include_router(v2_router)
```

---

## 9. 完整示例

```python
from fastapi import FastAPI, Path, Query, Body, Request
from pydantic import BaseModel, Field
from typing import Optional, List

app = FastAPI()

# ==================== 模型 ====================
class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float = Field(..., gt=0)
    quantity: int = Field(1, ge=0)

class ItemResponse(BaseModel):
    id: int
    name: str
    price: float
    quantity: int

# ==================== 路由 ====================
@app.get("/")
def root():
    return {"message": "Welcome to FastAPI"}

@app.get("/items", response_model=List[ItemResponse])
def get_items(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    category: Optional[str] = None
):
    items = [
        {"id": 1, "name": "Apple", "price": 1.5, "quantity": 10},
        {"id": 2, "name": "Banana", "price": 0.5, "quantity": 20}
    ]
    return items[skip:skip+limit]

@app.get("/items/{item_id}", response_model=ItemResponse)
def get_item(item_id: int = Path(..., ge=1)):
    return {"id": item_id, "name": f"Item {item_id}", "price": 9.99, "quantity": 5}

@app.post("/items", response_model=ItemResponse, status_code=201)
def create_item(item: Item):
    return {"id": 999, "name": item.name, "price": item.price, "quantity": item.quantity}

@app.put("/items/{item_id}", response_model=ItemResponse)
def update_item(item_id: int, item: Item):
    return {"id": item_id, "name": item.name, "price": item.price, "quantity": item.quantity}

@app.delete("/items/{item_id}", status_code=204)
def delete_item(item_id: int):
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

---

[← 返回目录](../README.md) | [下一章](./02-FastAPI-Pydantic模型.md)