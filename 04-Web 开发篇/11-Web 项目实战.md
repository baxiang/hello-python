# 第 11 章：Web 项目实战

综合运用所学知识，开发完整的博客 API 系统。

---

## 项目目标

- 构建完整的 RESTful API
- 实现用户认证
- 掌握数据库设计
- 学会测试和部署

---

## 11.1 项目结构

```
blog-api/
├── app/
│   ├── __init__.py
│   ├── main.py              # 应用入口
│   ├── config.py             # 配置
│   ├── models/               # 数据模型
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── post.py
│   │   └── comment.py
│   ├── schemas/             # Pydantic 模型
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── post.py
│   │   └── comment.py
│   ├── routers/              # 路由
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── users.py
│   │   ├── posts.py
│   │   └── comments.py
│   ├── services/             # 业务逻辑
│   │   └── __init__.py
│   └── utils/                # 工具
│       ├── __init__.py
│       └── security.py
├── tests/                    # 测试
│   └── test_api.py
├── requirements.txt
├── .env
└── README.md
```

---

## 11.2 配置文件

```python
# app/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Blog API"
    VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # 数据库
    DATABASE_URL: str = "sqlite:///./blog.db"
    
    # JWT
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    class Config:
        env_file = ".env"

settings = Settings()
```

---

## 11.3 数据模型

```python
# app/models/user.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(200), nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    posts = relationship("Post", back_populates="author")
    comments = relationship("Comment", back_populates="author")
```

```python
# app/models/post.py
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base

class Post(Base):
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    slug = Column(String(200), unique=True, nullable=False, index=True)
    content = Column(Text, nullable=False)
    summary = Column(String(500))
    published = Column(Boolean, default=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    author = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post")
```

---

## 11.4 路由实现

```python
# app/routers/posts.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.user import User
from app.models.post import Post
from app.schemas.post import PostCreate, PostResponse, PostUpdate
from app.utils.security import get_current_user

router = APIRouter(prefix="/posts", tags=["Posts"])

@router.get("", response_model=List[PostResponse])
def get_posts(
    skip: int = 0,
    limit: int = 20,
    published: bool = True,
    db: Session = Depends(get_db)
):
    query = db.query(Post)
    
    if published is not None:
        query = query.filter(Post.published == published)
    
    posts = query.order_by(Post.created_at.desc()).offset(skip).limit(limit).all()
    return posts

@router.get("/{post_id}", response_model=PostResponse)
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@router.post("", response_model=PostResponse, status_code=201)
def create_post(
    post: PostCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # 创建文章
    db_post = Post(
        title=post.title,
        slug=post.slug,
        content=post.content,
        summary=post.summary,
        published=post.published,
        author_id=current_user.id
    )
    
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    
    return db_post

@router.put("/{post_id}", response_model=PostResponse)
def update_post(
    post_id: int,
    post_update: PostUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    post = db.query(Post).filter(Post.id == post_id).first()
    
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    if post.author_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    update_data = post_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(post, key, value)
    
    db.commit()
    db.refresh(post)
    
    return post

@router.delete("/{post_id}", status_code=204)
def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    post = db.query(Post).filter(Post.id == post_id).first()
    
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    if post.author_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    db.delete(post)
    db.commit()
    
    return None
```

---

## 11.5 主应用

```python
# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import engine, Base
from app.routers import auth, users, posts, comments

# 创建数据库表
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(auth.router, prefix="/api")
app.include_router(users.router, prefix="/api")
app.include_router(posts.router, prefix="/api")
app.include_router(comments.router, prefix="/api")

@app.get("/")
def root():
    return {"message": "Blog API", "version": settings.VERSION}

@app.get("/health")
def health_check():
    return {"status": "ok"}
```

---

## 11.6 测试

```python
# tests/test_api.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Blog API", "version": "1.0.0"}

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_create_user():
    response = client.post(
        "/api/users",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpass123"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "testuser"
    assert "id" in data
```

---

## 本章总结

### 项目完成

恭喜完成 Web 开发篇的学习！通过本篇的学习，你已经掌握了：

1. **Web 基础** - HTTP 协议、URL、请求响应
2. **前端技术** - HTML、CSS、JavaScript
3. **Flask 框架** - 入门、进阶、高级
4. **FastAPI 框架** - 入门、进阶
5. **RESTful API** - 设计原则和最佳实践
6. **WebSocket** - 实时通信
7. **项目实战** - 完整博客 API 系统

---

## 后续学习建议

- 学习前端框架（Vue.js、React）
- 掌握 Docker 容器化部署
- 学习 CI/CD 持续集成
- 探索微服务架构

---

[← 上一章](./10-WebSocket 通信.md) | [返回目录](./README.md)