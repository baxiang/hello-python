# FastAPI Pydantic 模型

深入掌握 Pydantic 数据验证和模型定义。

---

## 1. Pydantic 基础

### 1.1 什么是 Pydantic？

Pydantic 是 Python 中用于数据验证的库，FastAPI 基于它实现请求和响应的数据验证。

### 1.2 基本模型

```python
from pydantic import BaseModel

class User(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool = True

# 创建实例
user = User(id=1, username="john", email="john@example.com")
print(user)
# id=1 username='john' email='john@example.com' is_active=True
```

---

## 2. 字段类型

### 2.1 基础类型

```python
from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime

class Model(BaseModel):
    # 基础类型
    name: str
    age: int
    price: float
    is_active: bool
    
    # 可选类型
    description: Optional[str] = None
    
    # 列表和字典
    tags: List[str] = []
    metadata: Dict[str, str] = {}
    
    # 日期时间
    created_at: datetime = None
```

### 2.2 特殊类型

```python
from pydantic import BaseModel, EmailStr, HttpUrl, UUID

class Contact(BaseModel):
    email: EmailStr           # 邮箱格式
    website: HttpUrl          # URL 格式
    uuid: UUID                # UUID 格式
    phone: str                # 电话号码

# 使用
contact = Contact(
    email="test@example.com",
    website="https://example.com",
    uuid="123e4567-e89b-12d3-a456-426614174000"
)
```

---

## 3. 字段验证

### 3.1 内置验证器

```python
from pydantic import BaseModel, Field, validator

class User(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., regex=r'^[\w\.-]+@[\w\.-]+\.\w+$')
    age: int = Field(..., ge=0, le=150)
    price: float = Field(..., gt=0)
    
    # 自定义验证器
    @validator('username')
    def username_alphanumeric(cls, v):
        assert v.isalnum(), 'must be alphanumeric'
        return v
```

### 3.2 多个字段验证

```python
from pydantic import BaseModel, field_validator

class User(BaseModel):
    password: str
    confirm_password: str
    
    @field_validator('confirm_password')
    @classmethod
    def passwords_match(cls, v, info):
        if 'password' in info.data and v != info.data['password']:
            raise ValueError('passwords do not match')
        return v
```

---

## 4. 嵌套模型

### 4.1 嵌套定义

```python
from pydantic import BaseModel
from typing import List, Optional

class Address(BaseModel):
    street: str
    city: str
    country: str
    zip_code: Optional[str] = None

class User(BaseModel):
    name: str
    email: str
    address: Optional[Address] = None
    friends: List["User"] = []

# 使用
user = User(
    name="John",
    email="john@example.com",
    address={"street": "123 Main St", "city": "Beijing", "country": "China"},
    friends=[]
)
```

### 4.2 递归模型

```python
from pydantic import BaseModel
from typing import List

class Category(BaseModel):
    id: int
    name: str
    parent_id: Optional[int] = None
    children: List["Category"] = []

# 解决递归引用
Category.model_rebuild()
```

---

## 5. 继承和组合

### 5.1 模型继承

```python
from pydantic import BaseModel

class BaseUser(BaseModel):
    id: int
    username: str
    email: str

class UserCreate(BaseUser):
    password: str

class UserResponse(BaseUser):
    is_active: bool
    created_at: str
```

### 5.2 组合模型

```python
from pydantic import BaseModel

class Price(BaseModel):
    amount: float
    currency: str = "USD"

class Product(BaseModel):
    name: str
    price: Price

# 使用
product = Product(
    name="Laptop",
    price={"amount": 999.99, "currency": "USD"}
)
```

---

## 6. 序列化

### 6.1 模型方法

```python
class User(BaseModel):
    id: int
    name: str
    email: str

user = User(id=1, name="John", email="john@example.com")

# 字典
user.dict()
# {'id': 1, 'name': 'John', 'email': 'john@example.com'}

# JSON
user.json()
# '{"id": 1, "name": "John", "email": "john@example.com"}'

# 复制
user_copy = user.copy()
user_copy2 = user.copy(update={"name": "Jane"})
```

### 6.2 配置模型

```python
from pydantic import BaseModel, ConfigDict

class User(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,  # 去除空格
        validate_assignment=True,   # 赋值时验证
        extra='forbid'             # 禁止额外字段
    )
    
    id: int
    name: str
```

---

## 7. 完整示例

```python
from fastapi import FastAPI
from pydantic import BaseModel, Field, EmailStr, field_validator
from typing import Optional, List
from datetime import datetime

app = FastAPI()

# ==================== 用户模型 ====================
class Address(BaseModel):
    street: str
    city: str
    country: str = "China"
    zip_code: Optional[str] = None

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr

class UserCreate(UserBase):
    password: str = Field(..., min_length=6)
    confirm_password: str
    
    @field_validator('confirm_password')
    @classmethod
    def passwords_match(cls, v, info):
        if 'password' in info.data and v != info.data['password']:
            raise ValueError('Passwords do not match')
        return v

class UserResponse(UserBase):
    id: int
    is_active: bool = True
    created_at: datetime
    
    class Config:
        from_attributes = True

# ==================== 文章模型 ====================
class PostBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    content: str

class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    id: int
    author_id: int
    created_at: datetime
    tags: List[str] = []
    
    class Config:
        from_attributes = True

# ==================== API 路由 ====================
users_db = {}
posts_db = {}

@app.post("/users", response_model=UserResponse, status_code=201)
def create_user(user: UserCreate):
    user_id = len(users_db) + 1
    user_data = {
        "id": user_id,
        "username": user.username,
        "email": user.email,
        "is_active": True,
        "created_at": datetime.now()
    }
    users_db[user_id] = user_data
    return user_data

@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int):
    if user_id not in users_db:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="User not found")
    return users_db[user_id]

@app.post("/posts", response_model=PostResponse, status_code=201)
def create_post(post: PostCreate, author_id: int = 1):
    post_id = len(posts_db) + 1
    post_data = {
        "id": post_id,
        "title": post.title,
        "content": post.content,
        "author_id": author_id,
        "created_at": datetime.now(),
        "tags": []
    }
    posts_db[post_id] = post_data
    return post_data

@app.get("/posts/{post_id}", response_model=PostResponse)
def get_post(post_id: int):
    if post_id not in posts_db:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Post not found")
    return posts_db[post_id]
```

---

## 总结

| 知识点 | 说明 |
|---------|------|
| BaseModel | 基础模型类 |
| Field | 字段定义和验证 |
| EmailStr/HttpUrl | 特殊类型 |
| validator | 自定义验证 |
| 嵌套模型 | 复杂数据结构 |
| 序列化 | dict/json 方法 |

---

[← 上一章](./01-FastAPI路由与参数.md) | [下一章](./03-FastAPI依赖注入.md)