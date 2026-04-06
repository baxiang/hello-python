# Pydantic 模型（详细版）

> Python 3.11+

本章讲解 Pydantic 数据验证和模型定义。

---

## 第一部分：Pydantic 基础

### 1.1 实际场景

API 接收用户注册数据时，需要验证邮箱格式、密码长度、必填字段等。

**问题：如何优雅地定义和验证数据结构？**

### 1.2 什么是 Pydantic？

Pydantic 是 Python 中用于数据验证的库，FastAPI 基于它实现请求和响应的数据验证。

### 1.3 基本模型

```python
from pydantic import BaseModel


class User(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool = True


# 创建实例
user: User = User(id=1, username="john", email="john@example.com")
print(user)
# id=1 username='john' email='john@example.com' is_active=True
```

---

## 第二部分：字段类型

### 2.1 实际场景

用户模型需要不同类型的字段：姓名是字符串、年龄是整数、标签是字符串列表。

**问题：如何定义各种类型的字段？**

### 2.2 基础类型

```python
from pydantic import BaseModel
from datetime import datetime


class Model(BaseModel):
    # 基础类型
    name: str
    age: int
    price: float
    is_active: bool
    
    # 可选类型
    description: str | None = None
    
    # 列表和字典
    tags: list[str] = []
    metadata: dict[str, str] = {}
    
    # 日期时间
    created_at: datetime | None = None
```

### 2.3 特殊类型

```python
from pydantic import BaseModel, EmailStr, HttpUrl
from uuid import UUID


class Contact(BaseModel):
    email: EmailStr           # 邮箱格式
    website: HttpUrl          # URL 格式
    uuid: UUID                # UUID 格式
    phone: str                # 电话号码


# 使用
contact: Contact = Contact(
    email="test@example.com",
    website="https://example.com",
    uuid=UUID("123e4567-e89b-12d3-a456-426614174000")
)
```

---

## 第三部分：字段验证

### 3.1 实际场景

用户名需要 3-50 字符，年龄需要 0-150，邮箱需要特定格式。

**问题：如何添加字段级别的验证？**

### 3.2 内置验证器

```python
from pydantic import BaseModel, Field, field_validator


class User(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., pattern=r'^[\w\.-]+@[\w\.-]+\.\w+$')
    age: int = Field(..., ge=0, le=150)
    price: float = Field(..., gt=0)
    
    # 自定义验证器
    @field_validator('username')
    @classmethod
    def username_alphanumeric(cls, v: str) -> str:
        if not v.isalnum():
            raise ValueError('must be alphanumeric')
        return v
```

### 3.3 多个字段验证

```python
from pydantic import BaseModel, field_validator


class User(BaseModel):
    password: str
    confirm_password: str
    
    @field_validator('confirm_password')
    @classmethod
    def passwords_match(cls, v: str, info) -> str:
        if 'password' in info.data and v != info.data['password']:
            raise ValueError('passwords do not match')
        return v
```

---

## 第四部分：嵌套模型

### 4.1 实际场景

用户有地址信息，地址包含街道、城市、国家等字段，需要嵌套结构。

**问题：如何定义复杂嵌套的数据模型？**

### 4.2 嵌套定义

```python
from pydantic import BaseModel


class Address(BaseModel):
    street: str
    city: str
    country: str
    zip_code: str | None = None


class User(BaseModel):
    name: str
    email: str
    address: Address | None = None
    friends: list["User"] = []


# 使用
user: User = User(
    name="John",
    email="john@example.com",
    address={"street": "123 Main St", "city": "Beijing", "country": "China"},
    friends=[]
)
```

### 4.3 递归模型

```python
from pydantic import BaseModel


class Category(BaseModel):
    id: int
    name: str
    parent_id: int | None = None
    children: list["Category"] = []


# 解决递归引用
Category.model_rebuild()
```

---

## 第五部分：继承和组合

### 5.1 实际场景

创建用户和响应用户有共同字段，但创建时需要密码，响应时不显示密码。

**问题：如何复用模型定义？**

### 5.2 模型继承

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

### 5.3 组合模型

```python
from pydantic import BaseModel


class Price(BaseModel):
    amount: float
    currency: str = "USD"


class Product(BaseModel):
    name: str
    price: Price


# 使用
product: Product = Product(
    name="Laptop",
    price={"amount": 999.99, "currency": "USD"}
)
```

---

## 第六部分：序列化

### 6.1 实际场景

需要将模型转换为字典或 JSON 字符串，用于 API 响应或存储。

**问题：如何序列化和反序列化模型？**

### 6.2 模型方法

```python
from pydantic import BaseModel


class User(BaseModel):
    id: int
    name: str
    email: str


user: User = User(id=1, name="John", email="john@example.com")

# 字典
user_dict: dict = user.model_dump()
# {'id': 1, 'name': 'John', 'email': 'john@example.com'}

# JSON
user_json: str = user.model_dump_json()
# '{"id": 1, "name": "John", "email": "john@example.com"}'
```

### 6.3 配置模型

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

## 第七部分：完整示例

```python
from fastapi import FastAPI
from pydantic import BaseModel, Field, EmailStr, field_validator
from datetime import datetime
from typing import Any

app: FastAPI = FastAPI()


# ==================== 用户模型 ====================
class Address(BaseModel):
    street: str
    city: str
    country: str = "China"
    zip_code: str | None = None


class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr


class UserCreate(UserBase):
    password: str = Field(..., min_length=6)
    confirm_password: str
    
    @field_validator('confirm_password')
    @classmethod
    def passwords_match(cls, v: str, info) -> str:
        if 'password' in info.data and v != info.data['password']:
            raise ValueError('Passwords do not match')
        return v


class UserResponse(UserBase):
    id: int
    is_active: bool = True
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


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
    tags: list[str] = []
    
    model_config = ConfigDict(from_attributes=True)


# ==================== API 路由 ====================
users_db: dict[int, dict[str, Any]] = {}
posts_db: dict[int, dict[str, Any]] = {}


@app.post("/users", response_model=UserResponse, status_code=201)
def create_user(user: UserCreate) -> dict[str, Any]:
    user_id: int = len(users_db) + 1
    user_data: dict[str, Any] = {
        "id": user_id,
        "username": user.username,
        "email": user.email,
        "is_active": True,
        "created_at": datetime.now()
    }
    users_db[user_id] = user_data
    return user_data


@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int) -> dict[str, Any]:
    if user_id not in users_db:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="User not found")
    return users_db[user_id]
```

---

## 总结

| 知识点 | 说明 |
|---------|------|
| BaseModel | 基础模型类 |
| Field | 字段定义和验证 |
| EmailStr/HttpUrl | 特殊类型 |
| field_validator | 自定义验证 |
| 嵌套模型 | 复杂数据结构 |
| model_dump | 序列化方法 |