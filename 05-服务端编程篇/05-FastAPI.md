# 第 28 章 - FastAPI 详解（详细版）

本章深入讲解 FastAPI 框架，包括 Pydantic 数据验证、依赖注入系统、异步数据库、认证安全和 WebSocket 支持。

---

## 第一部分：FastAPI 简介

### 28.1 为什么选择 FastAPI

#### 概念说明

FastAPI 是一个现代、高性能的 Python Web 框架，基于 Starlette 和 Pydantic，专为构建 API 而设计。

**核心特性：**

```
┌─────────────────────────────────────────────────────────────┐
│                  FastAPI 核心特性                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   🚀 高性能                                                  │
│   • 基于 Starlette 和 uvicorn，性能媲美 NodeJS 和 Go         │
│   • 异步支持，高并发场景表现优异                            │
│                                                             │
│   📝 自动文档                                                │
│   • 自动生成 OpenAPI 规范                                    │
│   • 内置 Swagger UI (/docs) 和 ReDoc (/redoc)               │
│                                                             │
│   ✅ 类型检查                                                │
│   • 基于 Python 类型提示                                     │
│   • 自动数据验证和转换                                       │
│   • IDE 智能提示和错误检查                                   │
│                                                             │
│   🔧 依赖注入                                                │
│   • 强大的依赖注入系统                                       │
│   • 可组合、可测试、可复用                                   │
│                                                             │
│   🛡️ 生产就绪                                                │
│   • Docker 支持                                              │
│   • 完善的认证方案                                           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**FastAPI vs Flask 对比：**

| 特性 | Flask | FastAPI |
|------|-------|---------|
| 类型 | 同步 | 异步 (async/await) |
| 数据验证 | 手动 | Pydantic 自动 |
| API 文档 | 需手动配置 | 自动生成 |
| 类型提示 | 可选 | 核心特性 |
| 学习曲线 | 低 | 中等 |
| 性能 | 中等 | 高 |
| WebSocket | 需扩展 | 原生支持 |

---

### 28.2 安装与运行

#### 概念说明

FastAPI 需要配合 ASGI 服务器（如 uvicorn）运行。

**安装：**

```bash
# 创建项目
uv init my-fastapi-app
cd my-fastapi-app

# 安装 FastAPI 和 uvicorn
uv add fastapi uvicorn[standard]

# 开发环境运行
uv run uvicorn main:app --reload

# 生产环境运行
uv run uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

**第一个 FastAPI 应用：**

```python
# main.py
from fastapi import FastAPI

app = FastAPI(
    title="我的 API",
    description="一个示例 API",
    version="1.0.0"
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}
```

**访问：**
- API 根地址：http://localhost:8000
- Swagger 文档：http://localhost:8000/docs
- ReDoc 文档：http://localhost:8000/redoc

---

## 第二部分：路径操作

### 28.3 路径装饰器

#### 概念说明

FastAPI 使用装饰器定义 HTTP 方法和路径的对应关系。

**HTTP 方法装饰器：**

```python
from fastapi import FastAPI

app = FastAPI()


@app.get("/items")
async def list_items():
    """获取物品列表"""
    return {"items": []}


@app.post("/items")
async def create_item():
    """创建新物品"""
    return {"message": "创建成功"}


@app.put("/items/{item_id}")
async def update_item(item_id: int):
    """更新物品"""
    return {"item_id": item_id}


@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    """删除物品"""
    return {"message": "删除成功"}


@app.patch("/items/{item_id}")
async def patch_item(item_id: int):
    """部分更新"""
    return {"item_id": item_id}
```

---

### 28.4 路径参数

#### 概念说明

路径参数使用花括号 `{}` 包裹，函数参数名需与路径参数名一致。

**基本用法：**

```python
@app.get("/users/{user_id}")
async def get_user(user_id: int):
    """获取用户 - user_id 自动转换为 int"""
    return {"user_id": user_id}


@app.get("/users/{user_id}/posts/{post_id}")
async def get_user_post(user_id: int, post_id: int):
    """多层路径参数"""
    return {"user_id": user_id, "post_id": post_id}
```

**路径参数验证：**

```python
from fastapi import Path

@app.get("/items/{item_id}")
async def read_item(
    item_id: int = Path(..., title="物品 ID", gt=0, le=1000)
):
    """
    gt=0: 必须大于 0
    le=1000: 必须小于等于 1000
    """
    return {"item_id": item_id}


@app.get("/users/{username}")
async def get_user(
    username: str = Path(..., min_length=3, max_length=50, pattern="^[a-zA-Z0-9_]+$")
):
    """
    min_length: 最小长度
    max_length: 最大长度
    pattern: 正则表达式匹配
    """
    return {"username": username}
```

---

### 28.5 查询参数

#### 概念说明

查询参数是 URL 中 `?` 后面的参数，作为函数的可选参数。

**基本用法：**

```python
@app.get("/items")
async def list_items(
    page: int = 1,
    limit: int = 10,
    sort: str = "created_at"
):
    """
    /items?page=2&limit=20&sort=name
    """
    return {"page": page, "limit": limit, "sort": sort}
```

**查询参数验证：**

```python
from fastapi import Query
from typing import Optional

@app.get("/items")
async def list_items(
    q: Optional[str] = Query(None, min_length=1, max_length=50),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    tags: list[str] = Query([])  # 多个值：?tags=python&tags=fastapi
):
    """
    Query 参数验证
    """
    return {
        "q": q,
        "page": page,
        "limit": limit,
        "tags": tags
    }
```

---

### 28.6 请求体（Pydantic 模型）

#### 概念说明

当使用 POST、PUT 等方法时，通常需要在请求体中发送数据。FastAPI 使用 Pydantic 模型定义请求体结构。

**定义 Pydantic 模型：**

```python
from pydantic import BaseModel, Field, EmailStr


class Item(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    description: str | None = Field(None, max_length=200)
    price: float = Field(..., gt=0)
    quantity: int = Field(default=1, ge=0)


class User(BaseModel):
    username: str
    email: EmailStr  # 自动验证邮箱格式
    password: str = Field(..., min_length=8)
```

**使用请求体：**

```python
@app.post("/items")
async def create_item(item: Item):
    """创建物品"""
    # item 自动验证和解析
    return {
        "message": "创建成功",
        "item": item
    }


@app.post("/users")
async def create_user(user: User):
    """创建用户"""
    return {"message": "用户创建成功", "user_id": 1}
```

**示例请求：**

```bash
curl -X POST "http://localhost:8000/items" \
  -H "Content-Type: application/json" \
  -d '{"name": "苹果", "price": 5.5, "quantity": 10}'
```

---

## 第三部分：数据验证（Pydantic）

### 28.7 字段验证器

#### 概念说明

Pydantic 提供丰富的字段验证选项，也可以使用自定义验证器。

**内置验证器：**

```python
from pydantic import BaseModel, Field, EmailStr, HttpUrl
from datetime import datetime
from typing import Optional


class Product(BaseModel):
    # 字符串验证
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field("", max_length=500)

    # 数值验证
    price: float = Field(..., gt=0)  # 大于 0
    discount: float = Field(0, ge=0, le=1)  # 0-1 之间
    stock: int = Field(0, ge=0)  # 非负整数

    # 邮箱和 URL
    contact_email: EmailStr
    website: HttpUrl

    # 可选字段
    category: Optional[str] = None

    # 日期时间
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # 列表
    tags: list[str] = Field(default_factory=list)
```

**自定义验证器：**

```python
from pydantic import BaseModel, field_validator, ValidationError
from datetime import datetime


class Article(BaseModel):
    title: str
    content: str
    published_at: datetime | None = None

    @field_validator('title')
    @classmethod
    def title_not_empty(cls, v):
        if not v.strip():
            raise ValueError('标题不能为空')
        return v.strip()

    @field_validator('published_at')
    @classmethod
    def published_not_future(cls, v):
        if v and v > datetime.utcnow():
            raise ValueError('发布时间不能是未来')
        return v

    @field_validator('content')
    @classmethod
    def content_min_length(cls, v):
        if len(v) < 10:
            raise ValueError('内容至少 10 个字符')
        return v
```

---

### 28.8 嵌套模型

#### 概念说明

Pydantic 模型可以嵌套，用于表示复杂的数据结构。

**示例代码：**

```python
from pydantic import BaseModel


class Address(BaseModel):
    street: str
    city: str
    state: str
    zip_code: str


class User(BaseModel):
    id: int
    name: str
    email: str
    address: Address  # 嵌套模型


class OrderItem(BaseModel):
    product_id: int
    quantity: int
    price: float


class Order(BaseModel):
    id: int
    user: User  # 嵌套 User 模型
    items: list[OrderItem]  # 列表中包含模型
    total: float
```

**使用示例：**

```python
@app.post("/orders")
async def create_order(order: Order):
    return {
        "order_id": order.id,
        "user_name": order.user.name,
        "city": order.user.address.city,
        "item_count": len(order.items),
        "total": order.total
    }
```

---

### 28.9 响应模型

#### 概念说明

`response_model` 用于控制响应数据的格式，可以排除敏感字段。

```python
from pydantic import BaseModel, EmailStr
from fastapi import FastAPI

app = FastAPI()


class UserIn(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserOut(BaseModel):
    username: str
    email: EmailStr
    # 不包含 password


class UserInDB(BaseModel):
    username: str
    email: EmailStr
    password_hash: str
    disabled: bool = False


@app.post("/users", response_model=UserOut)
async def create_user(user: UserIn):
    """创建用户，响应不包含密码"""
    return {
        "username": user.username,
        "email": user.email
    }


@app.get("/users/{username}", response_model=UserOut)
async def get_user(username: str):
    """获取用户"""
    return {
        "username": username,
        "email": "user@example.com"
    }
```

**排除字段：**

```python
@app.get("/secret", response_model=UserOut, response_model_exclude={"email"})
async def get_secret_user():
    """排除 email 字段"""
    return {"username": "admin"}
```

---

## 第四部分：依赖注入系统

### 28.10 Depends 使用

#### 概念说明

FastAPI 的依赖注入系统允许定义可复用的依赖关系，自动处理认证、数据库会话等。

**基本用法：**

```python
from fastapi import Depends, FastAPI

app = FastAPI()


# 定义依赖
async def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}


@app.get("/items")
async def read_items(commons: dict = Depends(common_parameters)):
    return commons


@app.get("/users")
async def read_users(commons: dict = Depends(common_parameters)):
    return commons
```

---

### 28.11 依赖类

#### 概念说明

可以使用类作为依赖，通过 `__call__` 方法实现。

```python
from fastapi import Depends, HTTPException, status


class Pagination:
    """分页依赖"""

    def __init__(self, page: int = 1, limit: int = 10):
        self.page = page
        self.limit = limit

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.limit


@app.get("/items")
async def list_items(pagination: Pagination = Depends()):
    skip = pagination.offset
    limit = pagination.limit
    return {"skip": skip, "limit": limit}
```

**认证依赖：**

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    """获取当前用户"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无效的认证凭证",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = get_user_from_db(username)
    if user is None:
        raise credentials_exception

    return user


@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    """需要认证的路由"""
    return current_user
```

---

### 28.12 全局依赖

#### 概念说明

可以在 Router 或 FastAPI 应用级别设置依赖。

```python
from fastapi import APIRouter, Depends, FastAPI

# Router 级别的依赖
router = APIRouter(
    prefix="/admin",
    dependencies=[Depends(check_admin_permission)]
)


# 应用级别的依赖
app = FastAPI(dependencies=[Depends(log_request)])


# 在特定路由上添加依赖
@app.get("/protected", dependencies=[Depends(get_current_user)])
async def protected():
    return {"message": "受保护的资源"}
```

---

## 第五部分：数据库集成

### 28.13 SQLAlchemy 异步

#### 概念说明

FastAPI 支持异步数据库操作，使用 `asyncpg`（PostgreSQL）或 `aiosqlite`（SQLite）。

**安装：**

```bash
uv add sqlalchemy[asyncio] aiosqlite
```

**数据库配置：**

```python
# database.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite+aiosqlite:///./test.db"

engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()


async def get_db() -> AsyncSession:
    """数据库会话依赖"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
```

**模型定义：**

```python
# models.py
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
```

---

### 28.14 CRUD 封装

#### 概念说明

将数据库操作封装为 CRUD 函数，便于复用。

```python
# crud.py
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models import User
from schemas import UserCreate


async def get_user(db: AsyncSession, user_id: int) -> User | None:
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()


async def get_user_by_username(db: AsyncSession, username: str) -> User | None:
    result = await db.execute(select(User).where(User.username == username))
    return result.scalar_one_or_none()


async def get_users(db: AsyncSession, skip: int = 0, limit: int = 10) -> list[User]:
    result = await db.execute(select(User).offset(skip).limit(limit))
    return result.scalars().all()


async def create_user(db: AsyncSession, user: UserCreate) -> User:
    db_user = User(username=user.username, email=user.email)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def delete_user(db: AsyncSession, user_id: int) -> bool:
    user = await get_user(db, user_id)
    if user:
        await db.delete(user)
        await db.commit()
        return True
    return False
```

**路由使用：**

```python
# routes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
import crud
import schemas

router = APIRouter(prefix="/users", tags=["用户"])


@router.get("/", response_model=list[schemas.UserOut])
async def list_users(
    skip: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_db)
):
    users = await crud.get_users(db, skip=skip, limit=limit)
    return users


@router.get("/{user_id}", response_model=schemas.UserOut)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return user


@router.post("/", response_model=schemas.UserOut)
async def create_user(user: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = await crud.get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="用户名已存在")
    return await crud.create_user(db, user)
```

---

## 第六部分：认证与安全

### 28.15 OAuth2 Password Flow

#### 概念说明

OAuth2 Password Flow 是一种简单的认证流程，用户直接使用用户名和密码获取 Token。

**完整实现：**

```python
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from pydantic import BaseModel

# 配置
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# 密码哈希
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()


# 数据模型
class Token(BaseModel):
    access_token: str
    token_type: str


class UserInDB(BaseModel):
    username: str
    email: str
    password_hash: str
    disabled: bool | None = None


# 工具函数
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无效的认证凭证",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return username


@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """获取 Token"""
    # 验证用户（这里简化处理，实际应从数据库查询）
    user_password = "secret"  # 实际应从数据库获取
    if form_data.username != "admin" or not verify_password(form_data.password, user_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": form_data.username},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me")
async def read_users_me(current_user: str = Depends(get_current_user)):
    """获取当前用户信息"""
    return {"username": current_user}
```

**前端登录示例：**

```javascript
// 登录
const response = await fetch('/token', {
  method: 'POST',
  headers: {'Content-Type': 'application/x-www-form-urlencoded'},
  body: new URLSearchParams({
    'grant_type': 'password',
    'username': 'admin',
    'password': 'secret'
  })
});
const {access_token} = await response.json();

// 使用 Token 访问受保护接口
const userResponse = await fetch('/users/me', {
  headers: {'Authorization': `Bearer ${access_token}`}
});
```

---

## 第七部分：WebSocket 支持

### 28.16 WebSocket 端点

#### 概念说明

FastAPI 原生支持 WebSocket，可以建立持久的双向连接。

**基本用法：**

```python
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLContent

app = FastAPI()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"收到消息：{data}")
```

**WebSocket 客户端：**

```javascript
const ws = new WebSocket('ws://localhost:8000/ws');

ws.onopen = () => {
  console.log('连接已建立');
  ws.send('Hello Server!');
};

ws.onmessage = (event) => {
  console.log('收到消息:', event.data);
};

ws.onclose = () => {
  console.log('连接已关闭');
};
```

---

### 28.17 连接管理

#### 概念说明

使用连接管理器管理多个 WebSocket 连接，支持广播功能。

```python
from fastapi import WebSocket
from typing import List


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        """广播消息给所有连接的客户端"""
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"客户端 {client_id}: {data}", websocket)
            await manager.broadcast(f"客户端 {client_id} 说：{data}")
    except:
        manager.disconnect(websocket)
```

---

## 第八部分：自动文档

### 28.18 Swagger UI 和 ReDoc

#### 概念说明

FastAPI 自动生成 OpenAPI 文档，提供两种风格的文档界面。

**访问文档：**
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
- OpenAPI JSON: `http://localhost:8000/openapi.json`

**自定义文档配置：**

```python
app = FastAPI(
    title="我的 API",
    description="这是一个示例 API，用于演示 FastAPI 功能",
    version="1.0.0",
    docs_url="/docs",      # Swagger UI 路径
    redoc_url="/redoc",    # ReDoc 路径
    openapi_url="/openapi.json"
)
```

**为路由添加文档：**

```python
@app.post(
    "/items",
    summary="创建物品",
    description="创建一个新的物品，需要提供名称和价格",
    tags=["物品管理"],
    response_description="创建的物品信息"
)
async def create_item(item: Item):
    ...
```

---

## 本章小结

```
┌─────────────────────────────────────────────────────────────┐
│                      第 28 章 知识要点                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   FastAPI 基础：                                             │
│   ✓ 安装：fastapi + uvicorn[standard]                       │
│   ✓ 路径装饰器：@app.get/post/put/delete/patch              │
│   ✓ 自动文档：/docs (Swagger)、/redoc (ReDoc)               │
│                                                             │
│   路径参数与查询参数：                                        │
│   ✓ 路径参数：{item_id}、类型转换、Path 验证                  │
│   ✓ 查询参数：函数参数、Query 验证、默认值                    │
│   ✓ 请求体：Pydantic 模型、自动验证                           │
│                                                             │
│   Pydantic 数据验证：                                         │
│   ✓ 字段验证：Field、min_length、gt/lt/ge/le                │
│   ✓ 自定义验证器：@field_validator                          │
│   ✓ 嵌套模型：模型嵌套、列表包含模型                        │
│   ✓ 响应模型：response_model、字段排除                      │
│                                                             │
│   依赖注入：                                                 │
│   ✓ Depends()：依赖函数、依赖类                             │
│   ✓ OAuth2：OAuth2PasswordBearer、Token 认证                 │
│   ✓ 全局依赖：Router 依赖、应用级依赖                       │
│                                                             │
│   数据库集成：                                               │
│   ✓ 异步 SQLAlchemy：AsyncSession、create_async_engine      │
│   ✓ 会话管理：get_db 依赖、上下文管理器                      │
│   ✓ CRUD 封装：查询、创建、更新、删除                        │
│                                                             │
│   认证安全：                                                 │
│   ✓ OAuth2 Password Flow：login_for_access_token            │
│   ✓ JWT Token：create_access_token、jwt.decode              │
│   ✓ 密码哈希：passlib、CryptContext、bcrypt                 │
│                                                             │
│   WebSocket：                                                │
│   ✓ 端点：@app.websocket、websocket.accept()                │
│   ✓ 连接管理：ConnectionManager、广播                       │
│   ✓ 实时通信：receive_text/send_text                        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```
---

[← 上一篇](./04-Flask高级.md) | [下一篇 →](./06-服务端项目实战.md)
