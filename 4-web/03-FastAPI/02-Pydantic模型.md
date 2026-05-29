# 02-Pydantic模型

> Python 3.11+

本章讲解 Pydantic 数据验证和模型定义。

---

## 概念铺垫

Pydantic 是 FastAPI 的数据验证基石，v2 版本将核心验证逻辑迁移到 Rust 编写的 `pydantic-core`，性能相比 v1 提升 10-40 倍。Pydantic 的工作分为两个独立管道：

```
输入管道 (Validation):
  原始输入 (dict/JSON) → Before Validator → Rust 核心验证 → After Validator → 模型实例

输出管道 (Serialization):
  模型实例 → Plain Serializer → Wrap Serializer → JSON/dict
```

**核心概念：**
- **Schema 编译**：模型定义时，Python 类型注解被编译为 pydantic-core Schema，此过程只执行一次
- **验证/序列化分离**：输入和输出使用独立的管道，互不干扰
- **Rust 引擎**：`SchemaValidator` 在 Rust 层批量执行类型检查和转换，避免 Python 函数调用开销

Pydantic 与 FastAPI 的关系：
- FastAPI 用 Pydantic 验证请求体、路径参数、查询参数
- Pydantic 的 `model_json_schema()` 为 FastAPI 生成 OpenAPI Schema
- `response_model` 利用 Pydantic 的序列化管道过滤输出字段

---

### L1 理解层：会用

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

### L2 实践层：用好

## 最佳实践

### 1. 输入输出模型完全分离

```
UserCreate (输入)          UserResponse (输出)
  username                   id
  email                      username
  password                   email
  confirm_password           is_active
                             created_at
```

- **输入模型**：包含验证规则、密码字段、确认字段
- **输出模型**：隐藏敏感字段（密码），含 `from_attributes=True` 支持 ORM 转换
- **共享基类**：`UserBase` 包含公共字段，输入和输出模型各自继承

### 2. ConfigDict 最佳配置

```python
from pydantic import BaseModel, ConfigDict


class UserResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,      # ORM 对象直接转换为模型
        str_strip_whitespace=True, # 自动去除字符串首尾空格
        validate_assignment=True,  # 属性赋值时也触发验证
        extra='forbid',            # 拒绝未定义的额外字段（安全）
    )
    id: int
    username: str
```

### 3. 验证器选择

| 验证器 | 执行时机 | 适用场景 |
|--------|----------|----------|
| `@field_validator('field')` | 单个字段验证后 | 字段格式校验、值规范化 |
| `@field_validator('field2')` with `info.data` | 单个字段验证后 | 跨字段验证（确认密码） |
| `@model_validator(mode='before')` | 所有字段验证前 | 预处理原始输入、数据转换 |
| `@model_validator(mode='after')` | 所有字段验证后 | 复杂的跨字段业务校验 |

### 4. Field 约束

- 数值：`ge`(>=), `gt`(>), `le`(<=), `lt`(<), `multiple_of`
- 字符串：`min_length`, `max_length`, `pattern`（正则）
- 通用：`default`, `default_factory`, `description`, `examples`
- 列表：`min_length`, `max_length`

## 反模式

| ❌ 反模式 | ✅ 改进 |
|-----------|---------|
| 同一个模型既做输入又做输出，密码字段暴露 | 分离为 `UserCreate` / `UserResponse` |
| 不设置 `extra='forbid'`，接受任意额外字段 | `model_config = ConfigDict(extra='forbid')` |
| 忘记 `model_rebuild()` 导致递归模型报错 | 自引用模型定义后调用 `Category.model_rebuild()` |
| 敏感数据（身份证号、银行卡）不加 `repr=False` | `Field(..., repr=False)` 避免日志泄露 |
| 使用 v1 的 `@validator`（已废弃） | 迁移到 v2 的 `@field_validator` |
| 在 `field_validator` 中做耗时 I/O | 字段验证应该是纯函数，I/O 放入 endpoint |
| `model_dump()` 后手动处理日期格式化 | 使用 `@field_serializer` 统一格式化 |

## 何时选用什么

| 需求 | 选用方案 |
|------|---------|
| 验证单个字段值 | `@field_validator('field')` |
| 验证字段间关系 | `@field_validator` + `info.data` |
| 预处理整个输入 | `@model_validator(mode='before')` |
| 跨字段业务规则 | `@model_validator(mode='after')` |
| 格式化输出字段 | `@field_serializer('field')` |
| ORM 对象转模型 | `ConfigDict(from_attributes=True)` |
| 拒绝未知字段 | `ConfigDict(extra='forbid')` |
| 模型继承 | `class UserCreate(BaseUser)` |
| 高效 JSON 输出 | `model_dump_json()` 而非 `model_dump()` |
| JSON 输入解析 | `User.model_validate_json(json_str)` |

---

### L3 专家层：深入

## 第七部分：L3 专家层

### 7.1 Pydantic v2 的 Rust 核心（pydantic-core）验证流程

Pydantic v2 的核心验证逻辑由 Rust 编写的 `pydantic-core` 库执行，这是 v2 相比 v1 性能大幅提升的根本原因。

**验证流程：**

```
输入数据 (dict/JSON)
    │
    ▼
┌──────────────────────────────────┐
│       Python 层 (pydantic)        │
│  ┌────────────────────────────┐  │
│  │  model_validate() / __init__│  │
│  └────────────┬───────────────┘  │
│               │                   │
│               ▼                   │
│  ┌────────────────────────────┐  │
│  │  Schema 编译                │  │
│  │  Python type hints →        │  │
│  │  pydantic-core Schema       │  │
│  │  (JSON-like dict 结构)      │  │
│  └────────────┬───────────────┘  │
└───────────────┼─────────────────┘
                │ Schema dict
                ▼
┌──────────────────────────────────┐
│       Rust 层 (pydantic-core)     │
│  ┌────────────────────────────┐  │
│  │  SchemaValidator::validate_ │  │
│  │  python()                   │  │
│  │                             │  │
│  │  ┌───────────────────────┐  │  │
│  │  │ 1. 类型检查 (type)     │  │  │
│  │  │ 2. 约束验证 (ge, le)   │  │  │
│  │  │ 3. 类型转换 (coerce)   │  │  │
│  │  │ 4. 自定义 validator    │  │  │
│  │  └───────────────────────┘  │  │
│  └────────────────────────────┘  │
│               │                   │
│               ▼                   │
│  ┌────────────────────────────┐  │
│  │  返回 Python 对象            │  │
│  │  (PyModelInstance)          │  │
│  └────────────────────────────┘  │
└──────────────────────────────────┘
```

**核心概念：**
- **Schema 编译**：模型定义时，Python 类型注解被编译为 pydantic-core 的 Schema（一种 JSON-like 字典结构），此过程只执行一次
- **Rust 验证**：实际验证在 Rust 层执行，避免 Python 的函数调用开销和动态类型检查
- **`__pydantic_complete__`**：模型编译完成后标记为 True，表示 Schema 已就绪

### 7.2 数据转换管道（Validator → Serialize）

Pydantic v2 将验证（输入）和序列化（输出）明确分离为两个独立的管道。

```
输入管道 (Validation)                  输出管道 (Serialization)
┌──────────────────────┐              ┌──────────────────────┐
│  原始输入 (dict/JSON) │              │  Python 模型实例       │
│         │            │              │         │            │
│         ▼            │              │         ▼            │
│  ┌──────────────┐    │              │  ┌──────────────┐    │
│  │ Before Val.  │    │              │  │ Plain Ser.   │    │
│  │ (转换输入)    │    │              │  │ (直接输出)    │    │
│  └──────┬───────┘    │              │  └──────┬───────┘    │
│         │            │              │         │            │
│         ▼            │              │         ▼            │
│  ┌──────────────┐    │              │  ┌──────────────┐    │
│  │ Core Validate│    │              │  │ Wrap Ser.    │    │
│  │ (Rust 引擎)   │    │              │  │ (包装输出)    │    │
│  └──────┬───────┘    │              │  └──────┬───────┘    │
│         │            │              │         │            │
│         ▼            │              │         ▼            │
│  ┌──────────────┐    │              │  ┌──────────────┐    │
│  │ After Val.   │    │              │  │ 格式化为      │    │
│  │ (后处理)      │    │              │  │ JSON/dict    │    │
│  └──────┬───────┘    │              │  └──────────────┘    │
│         │            │              │                       │
│         ▼            │              │                       │
│  模型实例 (Model)     │              │                       │
└──────────────────────┘              └──────────────────────┘
```

**关键装饰器：**
- `@field_validator('field')`：在核心验证后执行（after 模式），用于自定义验证逻辑
- `@field_serializer('field')`：在序列化时执行，用于格式化输出（如日期格式化）
- `@model_validator(mode='before')`：在核心验证前执行，用于预处理原始输入数据
- `@model_validator(mode='after')`：在核心验证后执行，用于跨字段验证

### 7.3 性能对比（Pydantic v1 vs v2）

| 操作 | v1 (纯 Python) | v2 (Rust 核心) | 提升倍数 |
|------|----------------|----------------|----------|
| 简单模型验证 | ~50 μs | ~3 μs | ~17x |
| 嵌套模型验证 | ~200 μs | ~8 μs | ~25x |
| 含自定义 validator | ~100 μs | ~15 μs | ~7x |
| `model_dump()` | ~30 μs | ~5 μs | ~6x |
| `model_dump_json()` | ~80 μs | ~10 μs | ~8x |
| 模型实例化 (1000 次) | ~50 ms | ~3 ms | ~17x |

**性能差异原因：**
- v1 使用 Python 的 `__init__` + 手动验证逻辑，每次验证都有大量 Python 函数调用
- v2 将验证编译为 Rust 的 `SchemaValidator`，在 Rust 层批量执行类型检查和转换
- v2 的序列化使用 Rust 的 `to_json` 直接生成 JSON 字符串，避免中间 dict 转换

### 7.4 性能考量

| 维度 | 说明 | 建议 |
|------|------|------|
| Schema 编译 | 模型首次使用时编译，后续复用 | 启动时预热模型可避免冷启动延迟 |
| 自定义 validator | 回退到 Python 执行 | 高频场景尽量用内置约束 |
| `model_dump()` | 返回 Python dict | 大批量数据用 `model_dump(mode='python')` |
| `model_dump_json()` | 直接返回 JSON 字符串 | API 响应优先使用，减少中间转换 |
| `extra='forbid'` | 额外字段检查有开销 | 仅在安全敏感场景使用 |

### 7.5 设计动机

| 设计选择 | 原因 |
|----------|------|
| Rust 核心 | Python 验证性能瓶颈明显，Rust 提供零成本抽象 |
| 验证/序列化分离 | 输入和输出通常需要不同的处理逻辑 |
| Schema 编译时 | 避免运行时重复解析类型注解 |
| `ConfigDict` | 替代 v1 的 `class Config`，支持继承和合并 |

### 7.6 知识关联

```
                    Pydantic 模型
                         │
        ┌────────────────┼────────────────┐
        ▼                ▼                ▼
    pydantic-core   JSON Schema      序列化
    (Rust 验证)    (文档生成)        (输出管道)
        │                │                │
        ▼                ▼                ▼
    类型转换        OpenAPI 规范      model_dump
    约束验证        $defs/$ref       model_dump_json
        │                │                │
        └────────────────┼────────────────┘
                         ▼
                  01-FastAPI 入门
                  04-数据库集成
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
