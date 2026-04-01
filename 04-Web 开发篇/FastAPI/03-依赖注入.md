# FastAPI 依赖注入

掌握 FastAPI 强大的依赖注入系统。

---

## 1. 依赖注入基础

### 1.1 什么是依赖注入？

依赖注入是一种设计模式，允许将依赖项从外部注入到函数或类中。

```python
from fastapi import FastAPI, Depends

app = FastAPI()

# 定义依赖
def get_database():
    return {"connection": "database"}

# 使用依赖
@app.get("/items")
def get_items(db = Depends(get_database)):
    return {"db": db}
```

---

## 2. 函数依赖

### 2.1 基本依赖函数

```python
from fastapi import FastAPI, Depends
from typing import Optional

app = FastAPI()

# 简单依赖
def get_query_param():
    return "default"

@app.get("/items")
def read_items(q: str = Depends(get_query_param)):
    return {"query": q}

# 带参数的依赖
def get_pagination(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}

@app.get("/items")
def get_items(pagination: dict = Depends(get_pagination)):
    return pagination
```

### 2.2 依赖链

```python
def get_database():
    return {"db": "connected"}

def get_current_user(db = Depends(get_database)):
    return {"username": "john", "id": 1}

@app.get("/users/me")
def read_current_user(user = Depends(get_current_user)):
    return user
```

---

## 3. 类依赖

### 3.1 类作为依赖

```python
from fastapi import FastAPI, Depends

app = FastAPI()

class Pagination:
    def __init__(self, skip: int = 0, limit: int = 10):
        self.skip = skip
        self.limit = limit

@app.get("/items")
def get_items(pagination: Pagination = Depends()):
    return {"skip": pagination.skip, "limit": pagination.limit}
```

### 3.2 带方法的类

```python
class Database:
    def __init__(self):
        self.connection = "connected"
    
    def query(self, sql: str):
        return [{"id": 1, "name": "Item 1"}]
    
    def close(self):
        self.connection = "disconnected"

def get_database():
    db = Database()
    try:
        yield db
    finally:
        db.close()

@app.get("/items")
def get_items(db: Database = Depends(get_database)):
    return db.query("SELECT * FROM items")
```

---

## 4. 依赖参数

### 4.1 路径参数

```python
def get_item_id(item_id: int):
    return item_id

@app.get("/items/{item_id}")
def read_item(item_id: int = Depends(get_item_id)):
    return {"item_id": item_id}
```

### 4.2 查询参数

```python
def get_search_query(q: str = "default"):
    return q

@app.get("/search")
def search(q: str = Depends(get_search_query)):
    return {"query": q}
```

---

## 5. 可选依赖

### 5.1 可选依赖

```python
from fastapi import Depends
from typing import Optional

def get_optional_db():
    return "db"

@app.get("/items")
def get_items(db: Optional[str] = Depends(get_optional_db, use_cache=False)):
    return {"db": db}
```

### 5.2 条件依赖

```python
def get_admin_user():
    return {"username": "admin", "role": "admin"}

def get_current_user():
    return {"username": "user", "role": "user"}

@app.get("/users")
def get_users(admin: dict = Depends(get_admin_user, use_cache=False)):
    return [admin]
```

---

## 6. 依赖注入进阶

### 6.1 依赖覆盖

```python
def get_database():
    return {"db": "production"}

app = FastAPI()

# 测试时覆盖依赖
app.dependency_overrides[get_database] = lambda: {"db": "test"}
```

### 6.2 全局依赖

```python
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

@app.middleware("http")
async def add_process_time(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Process-Time"] = "0.001"
    return response
```

---

## 7. 完整示例

```python
from fastapi import FastAPI, Depends, Header
from typing import Optional
from datetime import datetime

app = FastAPI()

# ==================== 依赖定义 ====================
class Pagination:
    def __init__(self, skip: int = 0, limit: int = 10):
        self.skip = skip
        self.limit = limit

def get_pagination(skip: int = 0, limit: int = 10) -> Pagination:
    return Pagination(skip=skip, limit=limit)

def verify_token(authorization: Optional[str] = Header(None)):
    if not authorization:
        return None
    if not authorization.startswith("Bearer "):
        return None
    token = authorization.replace("Bearer ", "")
    return {"token": token, "user_id": 1}

def get_current_user(token_data: dict = Depends(verify_token)):
    if not token_data:
        from fastapi import HTTPException
        raise HTTPException(status_code=401, detail="Not authenticated")
    return {"id": token_data["user_id"], "username": "john"}

# ==================== 路由 ====================
@app.get("/public/items")
def get_public_items(pagination: Pagination = Depends(get_pagination)):
    items = [{"id": i, "name": f"Item {i}"} for i in range(1, 101)]
    return items[pagination.skip:pagination.skip + pagination.limit]

@app.get("/private/items")
def get_private_items(
    pagination: Pagination = Depends(get_pagination),
    current_user: dict = Depends(get_current_user)
):
    items = [{"id": i, "name": f"Private Item {i}"} for i in range(1, 51)]
    return {
        "user": current_user["username"],
        "items": items[pagination.skip:pagination.skip + pagination.limit]
    }

@app.get("/profile")
def get_profile(current_user: dict = Depends(get_current_user)):
    return current_user
```

---

## 总结

| 知识点 | 说明 |
|---------|------|
| Depends | 依赖注入 |
| 函数依赖 | 简单依赖函数 |
| 类依赖 | 类作为依赖 |
| 依赖链 | 依赖嵌套 |
| 依赖覆盖 | 测试时覆盖 |
| 全局依赖 | 中间件 |

---

[← 上一章](./02-FastAPI-Pydantic模型.md) | [下一章](./04-FastAPI数据库集成.md)