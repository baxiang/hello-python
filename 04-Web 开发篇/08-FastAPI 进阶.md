# 第 8 章：FastAPI 进阶

深入学习 FastAPI 中间件、数据库集成、测试和性能优化。

---

## 本章目标

- 掌握中间件使用
- 集成 SQLAlchemy 数据库
- 学会后台任务
- 掌握测试方法
- 了解性能优化

---

## 8.1 中间件

### 基础中间件

```python
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
import time

app = FastAPI()

# CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# GZip 压缩
app.add_middleware(GZipMiddleware, minimum_size=1000)

# 自定义中间件
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
```

### 状态码中间件

```python
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

class CacheControlMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        
        # 静态资源缓存一年
        if request.url.path.startswith("/static"):
            response.headers["Cache-Control"] = "public, max-age=31536000"
        
        return response

app.add_middleware(CacheControlMiddleware)
```

---

## 8.2 数据库集成

### 安装依赖

```bash
pip install sqlalchemy databases
```

### 配置数据库

```python
from fastapi import FastAPI
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 模型
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)

# 依赖
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# API
from fastapi import Depends
from sqlalchemy.orm import Session

app = FastAPI()

@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users

@app.post("/users")
def create_user(
    username: str,
    email: str,
    db: Session = Depends(get_db)
):
    user = User(username=username, email=email)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
```

---

## 8.3 后台任务

### 使用 BackgroundTasks

```python
from fastapi import FastAPI, BackgroundTasks

app = FastAPI()

def write_log(message: str):
    with open("log.txt", "a") as f:
        f.write(f"{message}\n")

@app.post("/send-email/{email}")
async def send_email(email: str, background_tasks: BackgroundTasks):
    # 添加后台任务
    background_tasks.add_task(write_log, f"Email sent to {email}")
    
    return {"message": "Email is being sent"}

# 带参数的任务
def process_data(data: str, count: int):
    for i in range(count):
        print(f"Processing {data}: {i+1}/{count}")

@app.post("/process")
async def process(
    data: str,
    count: int = 5,
    background_tasks: BackgroundTasks = None
):
    background_tasks.add_task(process_data, data, count)
    return {"message": "Processing started"}
```

---

## 8.4 WebSocket

```python
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI()

# 连接管理器
class ConnectionManager:
    def __init__(self):
        self.active_connections = []
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
    
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
    
    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)
    
    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"Client {client_id}: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client {client_id} disconnected")
```

---

## 8.5 测试

### 安装依赖

```bash
pip install pytest httpx
```

### 单元测试

```python
# test_main.py
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

def test_create_user():
    response = client.post(
        "/users",
        json={"username": "test", "email": "test@example.com"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "test"
    assert "id" in data

def test_get_user():
    # 先创建
    client.post("/users", json={"username": "alice", "email": "alice@example.com"})
    
    # 再获取
    response = client.get("/users/alice")
    assert response.status_code == 200
    assert response.json()["username"] == "alice"
```

### 异步测试

```python
import pytest
from httpx import AsyncClient
from main import app

@pytest.mark.asyncio
async def test_async():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/")
        assert response.status_code == 200
```

### 运行测试

```bash
pytest test_main.py -v
```

---

## 8.6 性能优化

### 异步数据库

```python
from databases import Database

database = Database("sqlite:///test.db")

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/users")
async def get_users():
    query = "SELECT * FROM users"
    return await database.fetch_all(query)

@app.post("/users")
async def create_user(user: dict):
    query = "INSERT INTO users (username, email) VALUES (:username, :email)"
    return await database.execute(query, values=user)
```

### 缓存优化

```python
from functools import lru_cache

@lru_cache(maxsize=100)
def get_expensive_data(param: str):
    # 耗时计算
    return {"data": param, "computed": True}

@app.get("/data/{param}")
def get_data(param: str):
    return get_expensive_data(param)
```

---

## 本章总结

### 学到的技能

| 技能 | 说明 |
|------|------|
| 中间件 | CORS、GZip、自定义 |
| 数据库 | SQLAlchemy、databases |
| 后台任务 | BackgroundTasks |
| WebSocket | 实时通信 |
| 测试 | pytest、TestClient |
| 性能优化 | 异步、缓存 |

### 下一步

在 [第 9 章](./09-RESTful API 设计.md) 中，我们将学习 RESTful API 设计原则。

---

[← 上一章](./07-FastAPI 入门.md) | [下一章 →](./09-RESTful API 设计.md)