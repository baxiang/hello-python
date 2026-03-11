# 第 7 章：FastAPI 入门

掌握现代 Python Web 框架 FastAPI。

---

## 本章目标

- 理解 FastAPI 优势
- 掌握 Pydantic 数据验证
- 学会依赖注入
- 使用自动 API 文档

---

## 7.1 FastAPI 简介

### 什么是 FastAPI？

FastAPI 是一个现代、快速的 Python Web 框架，用于构建 API。支持自动生成文档、类型提示和异步处理。

### 安装

```bash
pip install fastapi uvicorn
```

### 第一个 FastAPI 应用

```python
# main.py
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello, World!"}

@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id, "name": "Item"}

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

## 7.2 Pydantic 数据验证

### 基本模型

```python
from fastapi import FastAPI
from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime

app = FastAPI()

# 请求模型
class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)
    age: Optional[int] = Field(None, ge=0, le=150)

# 响应模型
class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime
    
    class Config:
        from_attributes = True

# 使用模型
@app.post("/users", response_model=UserResponse)
def create_user(user: UserCreate):
    # user 已经被自动验证
    return {
        "id": 1,
        "username": user.username,
        "email": user.email,
        "created_at": datetime.now()
    }
```

### 嵌套模型

```python
from pydantic import BaseModel
from typing import List, Optional

class Address(BaseModel):
    street: str
    city: str
    country: str

class User(BaseModel):
    name: str
    email: str
    address: Optional[Address] = None
    tags: List[str] = []

# 创建用户
new_user = User(
    name="张三",
    email="zhangsan@example.com",
    address={"street": "中关村", "city": "北京", "country": "中国"},
    tags=["开发者", "Python"]
)
```

### 数据验证

```python
from pydantic import validator, field_validator

class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    confirm_password: str
    
    # 实例方法验证
    @field_validator('username')
    @classmethod
    def username_alphanumeric(cls, v):
        if not v.isalnum():
            raise ValueError('用户名只能包含字母和数字')
        return v
    
    # 跨字段验证
    @field_validator('confirm_password')
    @classmethod
    def passwords_match(cls, v, info):
        if 'password' in info.data and v != info.data['password']:
            raise ValueError('两次密码不一致')
        return v
```

---

## 7.3 路由和参数

### 路径参数

```python
from fastapi import FastAPI, Path

app = FastAPI()

@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id}

@app.get("/posts/{post_id}")
def get_post(
    post_id: int = Path(..., ge=1, description="文章ID")
):
    return {"post_id": post_id}
```

### 查询参数

```python
from fastapi import Query

@app.get("/users")
def get_users(
    skip: int = 0,
    limit: int = Query(100, ge=1, le=1000),
    search: str = None
):
    return {
        "skip": skip,
        "limit": limit,
        "search": search
    }
```

### 请求体

```python
from fastapi import Body

@app.post("/users")
def create_user(
    username: str = Body(...),
    email: str = Body(...)
):
    return {"username": username, "email": email}
```

### 文件上传

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
        results.append({
            "filename": file.filename,
            "size": len(contents)
        })
    return {"files": results}
```

---

## 7.4 依赖注入

### 依赖函数

```python
from fastapi import Depends, Header

# 简单依赖
def get_db():
    db = "database_connection"
    try:
        yield db
    finally:
        pass  # 关闭连接

@app.get("/items")
def read_items(db = Depends(get_db)):
    return {"db": db}

# 带参数的依赖
def get_pagination(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}

@app.get("/users")
def get_users(pagination: dict = Depends(get_pagination)):
    return pagination
```

### 类依赖

```python
class Pagination:
    def __init__(self, skip: int = 0, limit: int = 10):
        self.skip = skip
        self.limit = limit

@app.get("/posts")
def get_posts(pagination: Pagination = Depends()):
    return {"skip": pagination.skip, "limit": pagination.limit}
```

### 可选依赖

```python
from fastapi import Depends

def get_optional_db():
    return "db"

@app.get("/items")
def get_items(db: str = Depends(get_optional_db, use_cache=False)):
    return {"db": db}
```

---

## 7.5 响应模型

```python
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    description: Optional[str] = None

class ItemResponse(Item):
    id: int
    created_at: datetime

# 响应模型
@app.post("/items", response_model=ItemResponse)
def create_item(item: Item):
    return {
        "id": 1,
        "name": item.name,
        "price": item.price,
        "description": item.description,
        "created_at": datetime.now()
    }

# 列表响应
@app.get("/items", response_model=List[ItemResponse])
def get_items():
    return [
        {"id": 1, "name": "Apple", "price": 1.5, "description": None, "created_at": datetime.now()},
        {"id": 2, "name": "Banana", "price": 0.5, "description": None, "created_at": datetime.now()},
    ]
```

---

## 7.6 错误处理

```python
from fastapi import FastAPI, HTTPException

app = FastAPI()

items = {"1": "Apple", "2": "Banana"}

@app.get("/items/{item_id}")
def get_item(item_id: str):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item_id": item_id, "name": items[item_id]}

# 自定义错误处理器
from fastapi import Request
from fastapi.responses import JSONResponse

@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=400,
        content={"error": "Value Error", "message": str(exc)}
    )

@app.get("/error")
def trigger_error():
    raise ValueError("This is a custom error")
```

---

## 7.7 实战：RESTful API

```python
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import uuid

app = FastAPI(title="Todo API")

# 数据模型
class TodoCreate(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False

class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

class TodoResponse(BaseModel):
    id: str
    title: str
    description: Optional[str]
    completed: bool
    created_at: datetime

# 内存存储
todos = {}

# CRUD 操作
@app.post("/todos", response_model=TodoResponse)
def create_todo(todo: TodoCreate):
    todo_id = str(uuid.uuid4())
    todo_data = {
        "id": todo_id,
        "title": todo.title,
        "description": todo.description,
        "completed": todo.completed,
        "created_at": datetime.now()
    }
    todos[todo_id] = todo_data
    return todo_data

@app.get("/todos", response_model=List[TodoResponse])
def get_todos(completed: Optional[bool] = None):
    result = list(todos.values())
    
    if completed is not None:
        result = [t for t in result if t["completed"] == completed]
    
    return result

@app.get("/todos/{todo_id}", response_model=TodoResponse)
def get_todo(todo_id: str):
    if todo_id not in todos:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todos[todo_id]

@app.put("/todos/{todo_id}", response_model=TodoResponse)
def update_todo(todo_id: str, todo: TodoUpdate):
    if todo_id not in todos:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    todo_data = todos[todo_id]
    
    if todo.title is not None:
        todo_data["title"] = todo.title
    if todo.description is not None:
        todo_data["description"] = todo.description
    if todo.completed is not None:
        todo_data["completed"] = todo.completed
    
    return todo_data

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: str):
    if todo_id not in todos:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    del todos[todo_id]
    return {"message": "Todo deleted"}

# 运行后访问 http://127.0.0.1:8000/docs 查看交互式 API 文档
```

---

## 本章总结

### 学到的技能

| 技能 | 说明 |
|------|------|
| FastAPI 基础 | 框架和运行 |
| Pydantic | 数据验证和模型 |
| 路由参数 | 路径、查询、请求体 |
| 依赖注入 | Depends 用法 |
| 响应模型 | 响应数据验证 |
| 错误处理 | HTTPException |

### 下一步

在 [第 8 章](./08-FastAPI 进阶.md) 中，我们将学习 FastAPI 进阶内容。

---

[← 上一章](./06-Flask 高级.md) | [下一章 →](./08-FastAPI 进阶.md)