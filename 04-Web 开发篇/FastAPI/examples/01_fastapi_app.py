# FastAPI 示例

"""
FastAPI Web 框架示例
包含：路由、依赖注入、Pydantic 模型、异步
"""

from fastapi import FastAPI, Depends, HTTPException, Query
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

app = FastAPI(
    title="FastAPI 示例",
    description="FastAPI Web 框架示例",
    version="0.1.0"
)


# 1. Pydantic 模型
class UserBase(BaseModel):
    """用户基础模型"""
    name: str
    email: EmailStr


class UserCreate(UserBase):
    """用户创建模型"""
    password: str


class UserResponse(UserBase):
    """用户响应模型"""
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# 2. 模拟数据库
class Database:
    """模拟数据库"""
    def __init__(self):
        self.users = {}
        self.next_id = 1
    
    def create_user(self, user: UserCreate) -> UserResponse:
        user_data = UserResponse(
            id=self.next_id,
            name=user.name,
            email=user.email,
            created_at=datetime.now()
        )
        self.users[self.next_id] = user_data
        self.next_id += 1
        return user_data
    
    def get_user(self, user_id: int) -> Optional[UserResponse]:
        return self.users.get(user_id)
    
    def get_users(self) -> list[UserResponse]:
        return list(self.users.values())


db = Database()


# 3. 依赖注入
def get_database():
    """获取数据库实例"""
    return db


# 4. 基本路由
@app.get("/")
def index():
    """首页"""
    return {"message": "Hello, FastAPI!"}


@app.get("/hello/{name}")
def hello(name: str):
    """问候"""
    return {"message": f"Hello, {name}!"}


# 5. 查询参数
@app.get("/items/")
def read_items(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=100)
):
    """分页查询"""
    return {"skip": skip, "limit": limit}


# 6. REST API
@app.post("/users", response_model=UserResponse, status_code=201)
def create_user(
    user: UserCreate,
    database: Database = Depends(get_database)
):
    """创建用户"""
    return database.create_user(user)


@app.get("/users", response_model=list[UserResponse])
def get_users(database: Database = Depends(get_database)):
    """获取用户列表"""
    return database.get_users()


@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    database: Database = Depends(get_database)
):
    """获取单个用户"""
    user = database.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return user


# 7. 异步路由
@app.get("/async-example")
async def async_example():
    """异步示例"""
    import asyncio
    await asyncio.sleep(0.1)
    return {"message": "异步处理完成"}


# 8. 中间件
from fastapi import Request
import time


@app.middleware("http")
async def add_process_time(request: Request, call_next):
    """添加处理时间"""
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


# 9. 异常处理
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    """验证错误处理"""
    return JSONResponse(
        status_code=422,
        content={"error": "数据验证失败", "details": exc.errors()}
    )


if __name__ == "__main__":
    import uvicorn
    print("=" * 40)
    print("FastAPI 示例")
    print("=" * 40)
    print("\n访问 http://127.0.0.1:8000")
    print("API 文档: http://127.0.0.1:8000/docs")
    print("\n路由:")
    print("  GET  /              - 首页")
    print("  GET  /hello/{name}  - 问候")
    print("  GET  /items/        - 分页查询")
    print("  POST /users         - 创建用户")
    print("  GET  /users         - 用户列表")
    print("  GET  /users/{id}    - 获取用户")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)