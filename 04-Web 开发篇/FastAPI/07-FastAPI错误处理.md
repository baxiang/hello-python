# FastAPI 错误处理

掌握 FastAPI 异常处理和自定义错误响应。

---

## 1. HTTPException

### 1.1 基本使用

```python
from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get("/items/{item_id}")
def read_item(item_id: int):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return items_db[item_id]
```

### 1.2 自定义状态码

```python
from fastapi import HTTPException, status

@app.post("/users")
def create_user(user: UserCreate):
    if user.email in existing_emails:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    return {"id": 1, "email": user.email}
```

---

## 2. 自定义异常

### 2.1 定义异常类

```python
from fastapi import HTTPException

class ItemNotFoundException(HTTPException):
    def __init__(self, item_id: int):
        super().__init__(
            status_code=404,
            detail=f"Item {item_id} not found"
        )

class ValidationException(HTTPException):
    def __init__(self, field: str, message: str):
        super().__init__(
            status_code=422,
            detail={"field": field, "message": message}
        )
```

### 2.2 使用自定义异常

```python
@app.get("/items/{item_id}")
def read_item(item_id: int):
    if item_id not in items_db:
        raise ItemNotFoundException(item_id)
    return items_db[item_id]
```

---

## 3. 异常处理器

### 3.1 注册处理器

```python
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

app = FastAPI()

@app.exception_handler(ItemNotFoundException)
async def item_not_found_handler(request: Request, exc: ItemNotFoundException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": "Item Not Found", "message": exc.detail}
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"error": "Validation Error", "details": exc.errors()}
    )
```

### 3.2 全局错误处理

```python
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"error": "Internal Server Error", "message": str(exc)}
    )
```

---

## 4. 完整示例

```python
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel

app = FastAPI()

# 自定义异常
class BusinessException(Exception):
    def __init__(self, code: int, message: str):
        self.code = code
        self.message = message

# 异常处理器
@app.exception_handler(BusinessException)
async def business_exception_handler(request: Request, exc: BusinessException):
    return JSONResponse(
        status_code=exc.code,
        content={"error": exc.message}
    )

@app.exception_handler(RequestValidationError)
async def validation_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "error": "Validation Error",
            "details": exc.errors()
        }
    )

# 模型
class Item(BaseModel):
    name: str
    price: float

# 路由
items_db = {1: {"name": "Apple", "price": 1.5}}

@app.get("/items/{item_id}")
def get_item(item_id: int):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return items_db[item_id]

@app.post("/items")
def create_item(item: Item):
    if item.price < 0:
        raise BusinessException(400, "Price cannot be negative")
    item_id = len(items_db) + 1
    items_db[item_id] = item.dict()
    return {"id": item_id, "item": item}

@app.get("/error")
def trigger_error():
    raise BusinessException(418, "I'm a teapot")
```

---

## 总结

| 知识点 | 说明 |
|---------|------|
| HTTPException | HTTP 异常 |
| 自定义异常 | 业务异常 |
| 异常处理器 | 全局处理 |
| 错误响应 | 统一格式 |

---

[← 上一章](./06-FastAPI中间件.md) | [下一章](./08-FastAPI-WebSocket.md)