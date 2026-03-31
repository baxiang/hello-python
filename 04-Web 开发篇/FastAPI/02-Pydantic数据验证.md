# Pydantic 数据验证

## 请求体模型

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

---

## 字段验证器

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
from pydantic import BaseModel, field_validator
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

## 嵌套模型

Pydantic 模型可以嵌套，用于表示复杂的数据结构。

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

---

## 响应模型

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