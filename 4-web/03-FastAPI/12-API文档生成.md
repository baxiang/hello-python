# 12-API文档生成

> Python 3.11+

本章讲解 FastAPI 的 API 文档自动生成机制，包括 OpenAPI 规范、Swagger UI、ReDoc 以及如何定制文档内容。

---

## 概念铺垫

FastAPI 基于 Python 类型注解和 Pydantic 模型自动生成符合 OpenAPI 3.1 规范的文档。整个文档生成流程无需手动维护，代码即文档。

```
Python 代码 (type hints + Pydantic)
    │
    ▼ FastAPI 解析引擎
    │  ├── 路由定义 → paths
    │  ├── Pydantic 模型 → components/schemas
    │  ├── 安全方案 → components/securitySchemes
    │  └── 应用配置 → info/tags/servers
    │
    ▼
OpenAPI 3.1 JSON (/openapi.json)
    │
    ├── /docs (Swagger UI)
    └── /redoc (ReDoc)
```

**核心概念：**
- **OpenAPI Schema 生成**：首次访问 `/openapi.json` 时构建并缓存，后续请求直接返回缓存
- **Swagger UI**：交互式文档，支持 "Try it out" 在线调试
- **ReDoc**：只读文档，适合对外发布

---

### L1 理解层：会用

## 第一部分：OpenAPI 规范（L1）

### 1.1 实际场景

团队前端需要调用后端 API，但每次接口变更都需要手动更新文档，沟通成本高且容易出错。

**问题：如何让 API 文档自动保持最新？**

### 1.2 什么是 OpenAPI？

OpenAPI Specification（OAS）是描述 RESTful API 的标准格式。它用 JSON 或 YAML 定义：

```
+---------------------------------------------------+
|                OpenAPI Specification               |
+---------------------------------------------------+
|  openapi: 3.1.0                                    |
|  info:                                             |
|    title: My API                                   |
|    version: 1.0.0                                  |
|                                                    |
|  paths:                                            |
|    /items:                                         |
|      get:                                          |
|        summary: List all items                     |
|        responses:                                  |
|          200:                                      |
|            description: Successful response        |
|                                                    |
|  components:                                       |
|    schemas:                                        |
|      Item:                                         |
|        type: object                                |
|        properties:                                 |
|          id: { type: integer }                     |
|          name: { type: string }                    |
+---------------------------------------------------+
```

OpenAPI 的核心价值：

| 特性 | 说明 |
|------|------|
| 机器可读 | 工具可以自动解析和生成代码 |
| 语言无关 | 任何语言都可以编写和消费 |
| 生态丰富 | Swagger、Redoc、Postman 等工具支持 |

### 1.3 FastAPI 自动生成文档

FastAPI 基于 Pydantic 模型和 Python 类型提示，**自动**生成符合 OpenAPI 3.1 规范的 JSON：

```
+-------------------+     +-------------------+     +-------------------+
|   Python 代码     |---->|  FastAPI 引擎     |---->|  OpenAPI JSON     |
|                   |     |                   |     |                   |
|  type hints       |     |  解析类型提示     |     |  openapi.json     |
|  Pydantic models  |     |  提取模型定义     |     |  /docs (Swagger)  |
|  路由定义         |     |  组装规范结构     |     |  /redoc (ReDoc)   |
+-------------------+     +-------------------+     +-------------------+
```

启动应用后，FastAPI 默认提供三个端点：

| 端点 | 说明 |
|------|------|
| `/openapi.json` | OpenAPI 规范的 JSON 文件 |
| `/docs` | Swagger UI 交互式文档 |
| `/redoc` | ReDoc 只读文档 |

```python
from fastapi import FastAPI
from pydantic import BaseModel

app: FastAPI = FastAPI()


class Item(BaseModel):
    name: str
    price: float


@app.get("/items")
def get_items() -> list[Item]:
    return [{"name": "Apple", "price": 1.5}]


@app.post("/items")
def create_item(item: Item) -> Item:
    return item
```

启动后访问：

```bash
uvicorn main:app --reload
# 浏览器打开:
# http://127.0.0.1:8000/docs     ← Swagger UI
# http://127.0.0.1:8000/redoc    ← ReDoc
# http://127.0.0.1:8000/openapi.json  ← 原始规范
```

### 1.4 自定义文档端点

可以修改或禁用文档端点：

```python
from fastapi import FastAPI

# 自定义端点路径
app: FastAPI = FastAPI(
    docs_url="/api-docs",      # 改为 /api-docs
    redoc_url="/api-redoc",    # 改为 /api-redoc
    openapi_url="/api-spec",   # 改为 /api-spec
)

# 禁用文档（生产环境常见）
app_prod: FastAPI = FastAPI(
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
)
```

### 1.5 自定义 OpenAPI 元信息

```python
from fastapi import FastAPI

app: FastAPI = FastAPI(
    title="电商平台 API",
    description="提供商品、订单、用户等核心业务的 RESTful API",
    version="2.0.0",
    contact={
        "name": "API 支持团队",
        "email": "api-support@example.com",
        "url": "https://example.com/support",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
    terms_of_service="https://example.com/terms",
)


@app.get("/")
def root() -> dict[str, str]:
    return {"status": "ok"}
```

这些信息会显示在 Swagger UI 和 ReDoc 的顶部。

---

## 第二部分：定制 API 文档（L1）

### 2.1 实际场景

自动生成的文档只有函数名，无法表达 API 的真实含义。前端开发者看不懂 `get_items_2` 是什么。

**问题：如何让 API 文档对人类友好？**

### 2.2 使用 summary 和 description

```python
from fastapi import FastAPI

app: FastAPI = FastAPI()


@app.get(
    "/items",
    summary="获取商品列表",
    description="返回所有可用商品的列表，支持分页。默认返回前 10 条记录。",
)
def get_items() -> list[dict[str, str | float]]:
    return [{"name": "Apple", "price": 1.5}]


@app.get(
    "/items/{item_id}",
    summary="获取单个商品",
    description="根据商品 ID 获取详细信息。如果商品不存在，返回 404。",
    response_description="商品详细信息",
)
def get_item(item_id: int) -> dict[str, int | str | float]:
    return {"id": item_id, "name": f"Item {item_id}", "price": 9.99}
```

在 Swagger UI 中的效果：

```
+---------------------------------------------------+
| GET /items           获取商品列表                  |
|                                                    |
| 返回所有可用商品的列表，支持分页。                 |
| 默认返回前 10 条记录。                             |
|                                                    |
| [Try it out]  [执行]                               |
+---------------------------------------------------+
```

### 2.3 使用 tags 分组

```python
from fastapi import FastAPI

app: FastAPI = FastAPI()


# 商品相关
@app.get("/items", tags=["商品管理"])
def list_items() -> list[dict[str, str]]:
    return []


@app.post("/items", tags=["商品管理"])
def create_item() -> dict[str, int]:
    return {"id": 1}


# 用户相关
@app.get("/users", tags=["用户管理"])
def list_users() -> list[dict[str, str]]:
    return []


@app.post("/users", tags=["用户管理"])
def create_user() -> dict[str, int]:
    return {"id": 1}


# 订单相关
@app.get("/orders", tags=["订单管理"])
def list_orders() -> list[dict[str, str]]:
    return []
```

Swagger UI 会按 tag 分组显示：

```
+---------------------------------------------------+
| ▼ 商品管理                                         |
|   GET /items    获取商品列表                       |
|   POST /items   创建商品                           |
|                                                    |
| ▼ 用户管理                                         |
|   GET /users    获取用户列表                       |
|   POST /users   创建用户                           |
|                                                    |
| ▼ 订单管理                                         |
|   GET /orders   获取订单列表                       |
+---------------------------------------------------+
```

### 2.4 自定义请求和响应示例

```python
from fastapi import FastAPI
from pydantic import BaseModel

app: FastAPI = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    description: str | None = None


@app.post(
    "/items",
    summary="创建商品",
    response_description="创建后的商品信息",
    openapi_extra={
        "requestBody": {
            "content": {
                "application/json": {
                    "example": {
                        "name": "MacBook Pro",
                        "price": 14999.0,
                        "description": "14 英寸 M3 Pro 芯片",
                    }
                }
            }
        }
    },
)
def create_item(item: Item) -> Item:
    return item
```

Swagger UI 会在请求体区域显示示例值，方便测试。

### 2.5 为路由添加 deprecated 标记

```python
from fastapi import FastAPI

app: FastAPI = FastAPI()


@app.get("/v1/items", tags=["商品管理 (已弃用)"], deprecated=True)
def get_items_v1() -> list[dict[str, str]]:
    """旧版商品接口，请使用 /v2/items"""
    return []


@app.get("/v2/items", tags=["商品管理"])
def get_items_v2() -> list[dict[str, str]]:
    return []
```

废弃的接口在文档中会显示为删除线样式，提醒使用者迁移。

### 2.6 自定义响应状态码文档

```python
from fastapi import FastAPI
from pydantic import BaseModel

app: FastAPI = FastAPI()


class ErrorResponse(BaseModel):
    detail: str


class Item(BaseModel):
    id: int
    name: str


@app.get(
    "/items/{item_id}",
    responses={
        200: {
            "description": "成功获取商品",
            "model": Item,
        },
        404: {
            "description": "商品不存在",
            "model": ErrorResponse,
            "content": {
                "application/json": {
                    "example": {"detail": "商品 ID 999 不存在"}
                }
            },
        },
        422: {
            "description": "请求参数验证失败",
        },
    },
)
def get_item(item_id: int) -> Item:
    if item_id != 1:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail=f"商品 ID {item_id} 不存在")
    return Item(id=1, name="Apple")
```

---

## 第三部分：Pydantic 模型文档（L1）

### 3.1 实际场景

前端看到 `Item` 模型的 JSON Schema，但不知道每个字段的含义和取值范围。

**问题：如何让模型字段的文档自解释？**

### 3.2 使用 Field 添加描述和示例

```python
from pydantic import BaseModel, Field


class Item(BaseModel):
    name: str = Field(
        ...,
        description="商品名称",
        min_length=1,
        max_length=100,
        examples=["iPhone 15 Pro"],
    )
    price: float = Field(
        ...,
        description="商品价格（单位：元）",
        gt=0,
        examples=[5999.0],
    )
    description: str | None = Field(
        default=None,
        description="商品详细描述，支持 Markdown 格式",
        examples=["苹果最新旗舰手机，搭载 A17 Pro 芯片"],
    )
    category: str = Field(
        default="electronics",
        description="商品分类",
        pattern="^(electronics|clothing|food|books)$",
        examples=["electronics"],
    )
    tags: list[str] = Field(
        default_factory=list,
        description="商品标签列表",
        examples=["手机", "数码", "新品"],
    )
```

在 Swagger UI 的 Schema 区域会显示：

```
+---------------------------------------------------+
| Item                                               |
|                                                    |
| name *        string         商品名称              |
|               Min length: 1                        |
|               Max length: 100                      |
|               Example: "iPhone 15 Pro"             |
|                                                    |
| price *       number         商品价格（单位：元）  |
|               > 0                                  |
|               Example: 5999                        |
|                                                    |
| description   string | null  商品详细描述           |
|               Example: "苹果最新旗舰手机..."       |
|                                                    |
| category      string         商品分类              |
|               Pattern: ^(electronics|...)          |
|               Example: "electronics"               |
|                                                    |
| tags          Array[string]  商品标签列表           |
|               Example: ["手机", "数码", "新品"]    |
+---------------------------------------------------+
```

### 3.3 使用 model_config.schema_extra 自定义

```python
from pydantic import BaseModel, ConfigDict


class Item(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "name": "MacBook Pro",
                    "price": 14999.0,
                    "description": "14 英寸 M3 Pro",
                    "category": "electronics",
                    "tags": ["笔记本", "苹果"],
                }
            ]
        }
    )

    name: str
    price: float
    description: str | None = None
    category: str = "electronics"
    tags: list[str] = []
```

### 3.4 模型级别的 description

```python
from pydantic import BaseModel, Field


class Address(BaseModel):
    """地址信息模型"""

    street: str = Field(..., description="街道地址")
    city: str = Field(..., description="城市")
    province: str = Field(..., description="省份")
    zip_code: str = Field(..., description="邮政编码", pattern=r"^\d{6}$")


class User(BaseModel):
    """
    用户信息模型

    用于用户注册和个人资料管理。
    所有字段均为必填，除非特别说明。
    """

    username: str = Field(..., description="用户名，3-50 个字符", min_length=3, max_length=50)
    email: str = Field(..., description="电子邮箱")
    age: int = Field(..., description="年龄", ge=0, le=150)
    address: Address | None = Field(default=None, description="收货地址")
```

Pydantic 的 docstring 会自动成为 Schema 的 description。

### 3.5 嵌套模型的文档展示

```python
from pydantic import BaseModel, Field


class OrderItem(BaseModel):
    """订单中的商品项"""

    product_id: int = Field(..., description="商品 ID")
    quantity: int = Field(..., description="购买数量", ge=1)
    unit_price: float = Field(..., description="单价")


class Order(BaseModel):
    """订单模型"""

    order_id: str = Field(..., description="订单号", examples=["ORD-2024-001"])
    items: list[OrderItem] = Field(..., description="订单商品列表")
    total_amount: float = Field(..., description="订单总金额")
    status: str = Field(
        ...,
        description="订单状态",
        pattern="^(pending|paid|shipped|completed|cancelled)$",
    )
```

Swagger UI 会展开嵌套模型，显示完整的层级结构：

```
+---------------------------------------------------+
| Order                                              |
|                                                    |
| order_id *    string         订单号                |
|               Example: "ORD-2024-001"              |
|                                                    |
| items *       Array[OrderItem]  订单商品列表       |
|   └─ OrderItem                                     |
|      ├─ product_id *  integer   商品 ID            |
|      ├─ quantity *    integer   购买数量 (>= 1)    |
|      └─ unit_price *  number    单价               |
|                                                    |
| total_amount * number         订单总金额           |
| status *       string         订单状态             |
+---------------------------------------------------+
```

---

### L2 实践层：用好

## 第四部分：L2 实践层

### 4.1 最佳实践

**原则：好的 API 文档 = 自解释 + 可执行 + 可信赖**

#### 每个端点都有 summary 和 description

```python
# ❌ 反模式：只有函数名
@app.get("/items")
def get_items():
    ...


# ✅ 最佳实践：清晰的描述
@app.get(
    "/items",
    summary="获取商品列表",
    description="分页获取所有已上架的商品。默认按创建时间倒序排列。",
    tags=["商品管理"],
)
def get_items(
    skip: int = Query(0, ge=0, description="跳过的记录数"),
    limit: int = Query(10, ge=1, le=100, description="返回的记录数"),
) -> list[Item]:
    ...
```

#### 为所有参数添加描述

```python
from fastapi import Query, Path


@app.get("/items/{item_id}")
def get_item(
    item_id: int = Path(..., ge=1, description="商品唯一标识符"),
    include_reviews: bool = Query(
        False, description="是否包含商品评价信息"
    ),
) -> Item:
    ...
```

#### 示例值覆盖常见场景

```python
class UserCreate(BaseModel):
    username: str = Field(
        ...,
        min_length=3,
        max_length=50,
        examples=["zhang_san", "li_si"],
    )
    password: str = Field(
        ...,
        min_length=8,
        description="密码，至少 8 个字符，包含大小写字母和数字",
        examples=["MyP@ssw0rd123"],
        json_schema_extra={"format": "password"},
    )
```

#### 错误响应也要文档化

```python
@app.post(
    "/orders",
    responses={
        201: {"description": "订单创建成功"},
        400: {"description": "库存不足或商品信息无效"},
        401: {"description": "未认证，请先登录"},
        404: {"description": "商品不存在"},
        422: {"description": "请求参数验证失败"},
        500: {"description": "服务器内部错误"},
    },
)
def create_order(order: OrderCreate) -> Order:
    ...
```

### 4.2 反模式

| 反模式 | 问题 | 改进 |
|--------|------|------|
| 空文档 | 只有函数名，无法理解用途 | 添加 summary + description |
| 技术术语 | 用内部概念描述 API | 用业务语言描述 |
| 缺少示例 | 调用者不知道格式 | 提供 examples |
| 不写错误码 | 调用者无法处理异常 | 文档化所有可能的响应 |
| 过时文档 | 代码改了文档没更新 | 依赖自动生成 |

```python
# ❌ 空文档 + 技术术语
@app.get("/api/v2/users/items/proc")
def process_user_items_v2():
    """处理用户物品的第二个版本"""
    ...


# ✅ 清晰的业务描述
@app.get(
    "/users/{user_id}/purchase-history",
    summary="获取用户购买记录",
    description="查询指定用户的历史购买订单，按下单时间倒序排列。",
    tags=["用户管理"],
)
def get_purchase_history(
    user_id: int = Path(..., description="用户 ID"),
    start_date: str | None = Query(None, description="起始日期，格式 YYYY-MM-DD"),
    end_date: str | None = Query(None, description="结束日期，格式 YYYY-MM-DD"),
) -> list[Order]:
    ...
```

### 4.3 生成静态文档

#### 导出 openapi.json

```python
import json
from fastapi import FastAPI

app: FastAPI = FastAPI(title="示例 API")


@app.get("/items")
def get_items() -> list[dict[str, str]]:
    return []


# 导出方式一：通过 HTTP 请求
# curl http://127.0.0.1:8000/openapi.json > openapi.json

# 导出方式二：编程方式
def export_openapi() -> None:
    spec: dict = app.openapi()
    with open("openapi.json", "w") as f:
        json.dump(spec, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    export_openapi()
    print("OpenAPI 规范已导出到 openapi.json")
```

#### 生成静态 HTML（Swagger UI）

```bash
# 安装工具
pip install swagger-ui-bundle

# Python 脚本生成静态 HTML
```

```python
from swagger_ui_bundle import swagger_ui

# 方式一：使用 Redocly CLI
# npm install -g @redocly/cli
# redocly build-docs openapi.json -o docs.html

# 方式二：使用 Swagger CLI
# npm install -g swagger-cli
# swagger-cli bundle openapi.json -o bundled.yaml
```

#### 使用 redocly 生成文档站点

```bash
# 安装 Redocly CLI
npm install -g @redocly/cli

# 生成静态站点
redocly build-docs openapi.json -o ./docs/

# 预览
redocly preview openapi.json
```

#### 完整导出脚本

```python
"""导出 API 文档到多种格式"""

import json
import subprocess
from pathlib import Path

from fastapi import FastAPI
from pydantic import BaseModel, Field

app: FastAPI = FastAPI(
    title="电商平台 API",
    version="1.0.0",
)


class Item(BaseModel):
    name: str = Field(..., description="商品名称")
    price: float = Field(..., description="价格")


@app.get("/items", summary="获取商品列表")
def get_items() -> list[Item]:
    return []


@app.post("/items", summary="创建商品")
def create_item(item: Item) -> Item:
    return item


def export_docs() -> None:
    """导出所有格式的文档"""
    output: Path = Path("api-docs")
    output.mkdir(exist_ok=True)

    # 1. 导出 openapi.json
    spec: dict = app.openapi()
    spec_path: Path = output / "openapi.json"
    with open(spec_path, "w") as f:
        json.dump(spec, f, indent=2, ensure_ascii=False)
    print(f"✓ OpenAPI JSON: {spec_path}")

    # 2. 导出 openapi.yaml
    try:
        import yaml

        yaml_path: Path = output / "openapi.yaml"
        with open(yaml_path, "w") as f:
            yaml.dump(spec, f, allow_unicode=True, sort_keys=False)
        print(f"✓ OpenAPI YAML: {yaml_path}")
    except ImportError:
        print("✗ 安装 pyyaml 以导出 YAML 格式: uv add pyyaml")

    # 3. 生成 ReDoc 静态页面
    try:
        result = subprocess.run(
            ["npx", "@redocly/cli", "build-docs", str(spec_path), "-o", str(output / "redoc.html")],
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            print(f"✓ ReDoc HTML: {output / 'redoc.html'}")
        else:
            print(f"✗ ReDoc 生成失败: {result.stderr}")
    except FileNotFoundError:
        print("✗ 需要安装 Node.js 和 npx")


if __name__ == "__main__":
    export_docs()
```

---

## 第五部分：L3 专家层

### 5.1 OpenAPI 规范结构详解

完整的 OpenAPI 3.1 规范包含以下核心部分：

```
+-----------------------------------------------------------+
|                    OpenAPI Document                        |
+-----------------------------------------------------------+
|  openapi: "3.1.0"                                          |
|                                                           |
|  info:                                                     |
|    title: "API 名称"                                       |
|    version: "1.0.0"                                        |
|    description: "API 描述"                                 |
|    contact: { name, email, url }                           |
|    license: { name, url }                                  |
|                                                           |
|  servers:                                                  |
|    - url: "https://api.example.com/v1"                     |
|      description: "生产环境"                               |
|    - url: "https://staging-api.example.com/v1"             |
|      description: "预发环境"                               |
|                                                           |
|  paths:                    ← 所有端点定义                  |
|    /items:                                                 |
|      get:                                                  |
|        summary: "..."                                      |
|        operationId: "get_items"                            |
|        tags: ["商品管理"]                                  |
|        parameters: [...]                                   |
|        responses: { 200: {...}, 404: {...} }              |
|        security: [{ "BearerAuth": [] }]                   |
|      post:                                                 |
|        requestBody: { content: {...} }                     |
|        responses: { 201: {...} }                           |
|                                                           |
|  components:               ← 可复用组件                    |
|    schemas:                                                |
|      Item:                                                 |
|        type: object                                        |
|        properties: {...}                                   |
|        required: ["name", "price"]                         |
|      ErrorResponse:                                        |
|        type: object                                        |
|        properties: { detail: { type: string } }            |
|                                                           |
|    parameters:                                             |
|      PaginationSkip:                                       |
|        name: skip                                          |
|        in: query                                           |
|        schema: { type: integer, default: 0 }              |
|                                                           |
|    securitySchemes:        ← 认证方案                      |
|      BearerAuth:                                           |
|        type: http                                            |
|        scheme: bearer                                        |
|        bearerFormat: JWT                                     |
|      ApiKeyAuth:                                           |
|        type: apiKey                                        |
|        in: header                                          |
|        name: X-API-Key                                     |
|                                                           |
|  tags:                     ← 全局标签定义                  |
|    - name: "商品管理"                                      |
|      description: "商品的增删改查"                         |
|    - name: "用户管理"                                      |
|      description: "用户注册、登录、资料管理"               |
|                                                           |
|  security:                 ← 全局安全要求                  |
|    - BearerAuth: []                                        |
+-----------------------------------------------------------+
```

### 5.2 FastAPI 的 OpenAPI 生成流程

```
+-------------------------------------------------------------------+
|                     FastAPI 文档生成流程                           |
+-------------------------------------------------------------------+
|                                                                   |
|  1. 路由注册                                                       |
|     @app.get("/items")                                            |
|     def get_items(skip: int = 0) -> list[Item]:                   |
|        │                                                          |
|        ▼                                                          |
|  2. 解析函数签名                                                    |
|     ├─ 路径参数: item_id (Path)                                    |
|     ├─ 查询参数: skip (Query)                                      |
|     ├─ 请求体: item: Item (Body via Pydantic)                      |
|     └─ 返回类型: list[Item] → Response Schema                      |
|        │                                                          |
|        ▼                                                          |
|  3. 生成 JSON Schema                                               |
|     ├─ 从 Pydantic model 提取字段定义                              |
|     ├─ 转换为 JSON Schema Draft 2020-12 格式                       |
|     └─ 处理嵌套模型、泛型、可选类型                                 |
|        │                                                          |
|        ▼                                                          |
|  4. 组装 OpenAPI 文档                                               |
|     ├─ paths: 所有路由 → 操作对象                                   |
|     ├─ components.schemas: 所有 Pydantic 模型                      |
|     ├─ components.securitySchemes: 认证配置                        |
|     └─ info/tags/servers: 应用级配置                               |
|        │                                                          |
|        ▼                                                          |
|  5. 输出                                                           |
|     ├─ /openapi.json  ← JSON 响应                                 |
|     ├─ /docs          ← Swagger UI (加载 openapi.json)             |
|     └─ /redoc         ← ReDoc (加载 openapi.json)                 |
|                                                                   |
+-------------------------------------------------------------------+
```

查看 FastAPI 生成的完整 OpenAPI 规范：

```python
import json
from fastapi import FastAPI
from pydantic import BaseModel, Field

app: FastAPI = FastAPI(title="示例 API")


class Item(BaseModel):
    name: str = Field(..., description="商品名称")
    price: float = Field(..., description="价格", gt=0)


@app.get("/items", summary="获取商品列表")
def get_items(skip: int = 0) -> list[Item]:
    return []


# 打印生成的 OpenAPI 规范
if __name__ == "__main__":
    spec: dict = app.openapi()
    print(json.dumps(spec, indent=2, ensure_ascii=False))
```

输出示例：

```json
{
  "openapi": "3.1.0",
  "info": {
    "title": "示例 API",
    "version": "0.1.0"
  },
  "paths": {
    "/items": {
      "get": {
        "summary": "获取商品列表",
        "operationId": "get_items_items_get",
        "parameters": [
          {
            "name": "skip",
            "in": "query",
            "required": false,
            "schema": {
              "type": "integer",
              "default": 0,
              "title": "Skip"
            }
          }
        ],
        "responses": {
          "200": {
            "description": "Successful Response",
            "content": {
              "application/json": {
                "schema": {
                  "items": { "$ref": "#/components/schemas/Item" },
                  "type": "array"
                }
              }
            }
          }
        }
      }
    }
  },
  "components": {
    "schemas": {
      "Item": {
        "properties": {
          "name": { "type": "string", "title": "Name", "description": "商品名称" },
          "price": { "type": "number", "title": "Price", "description": "价格", "exclusiveMinimum": 0 }
        },
        "required": ["name", "price"],
        "type": "object",
        "title": "Item"
      }
    }
  }
}
```

### 5.3 自定义 OpenAPI Schema

当自动生成的文档不满足需求时，可以完全自定义：

```python
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

app: FastAPI = FastAPI()


def custom_openapi() -> dict:
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema: dict = get_openapi(
        title="自定义 API",
        version="2.0.0",
        description="这是一个自定义 OpenAPI 文档的示例",
        routes=app.routes,
    )

    # 添加自定义扩展
    openapi_schema["info"]["x-logo"] = {
        "url": "https://example.com/logo.png"
    }

    # 添加自定义扩展字段
    openapi_schema["x-custom-extension"] = {
        "version": "2.0",
        "environment": "production",
    }

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


@app.get("/items")
def get_items() -> list[dict[str, str]]:
    return []
```

### 5.4 安全方案文档

```python
from fastapi import FastAPI, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

app: FastAPI = FastAPI()

# 定义安全方案
security: HTTPBearer = HTTPBearer(
    description="输入 JWT Token，格式: Bearer <token>"
)


@app.get(
    "/protected",
    security=[security],
    summary="受保护的端点",
    description="需要有效的 JWT Token 才能访问",
)
def protected_endpoint(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> dict[str, str]:
    return {"token": credentials.credentials}
```

生成的 OpenAPI 中会包含：

```json
{
  "components": {
    "securitySchemes": {
      "HTTPBearer": {
        "type": "http",
        "scheme": "bearer",
        "description": "输入 JWT Token，格式: Bearer <token>"
      }
    }
  }
}
```

Swagger UI 会自动显示 Authorize 按钮。

### 5.5 与其他文档工具对比

| 工具 | 类型 | 特点 | 适用场景 |
|------|------|------|----------|
| **FastAPI 自动生成** | 代码驱动 | 零配置、实时同步 | Python 后端项目 |
| **Swagger Editor** | 手动编写 | 可视化编辑、在线协作 | API 设计阶段 |
| **Stoplight Studio** | 可视化设计 | GUI 设计、团队协作 | 大型团队 API 设计 |
| **Redocly** | 文档渲染 | 美观的静态文档站点 | 对外 API 文档发布 |
| **Apifox/Postman** | 测试 + 文档 | 接口测试、Mock 服务 | 团队协作测试 |

```
+---------------------------------------------------+
|              文档工具选择决策树                      |
+---------------------------------------------------+
|                                                   |
|  使用 FastAPI？                                    |
|  ├── 是 → 使用内置文档（/docs, /redoc）            |
|  │         └── 需要对外发布？                      |
|  │             └── 是 → 用 Redocly 生成静态站点    |
|  │                                                 |
|  └── 否 → API 设计阶段？                           |
|              ├── 是 → Swagger Editor / Stoplight   |
|              └── 否 → 需要测试？                   |
|                  └── 是 → Apifox / Postman         |
|                                                   |
+---------------------------------------------------+
```

### 5.6 知识关联图

```
+-------------------------------------------------------------------+
|                    API 文档知识图谱                                |
+-------------------------------------------------------------------+
|                                                                   |
|   +----------------+      +----------------+      +-------------+ |
|   |  Python 类型   |─────>|  Pydantic 模型 |─────>| JSON Schema | |
|   |  提示          |      |  Field/Config  |      |  生成       | |
|   +----------------+      +----------------+      +-------------+ |
|          │                       │                       │        |
|          │                       │                       │        |
|          ▼                       ▼                       ▼        |
|   +----------------------------------------------------------------+|
|   |                    FastAPI 路由定义                             ||
|   |  @app.get() / @app.post() / summary / description / tags       ||
|   +----------------------------------------------------------------+|
|                              │                                      |
|                              ▼                                      |
|   +---------------------------------------------------------------+ |
|   |                    OpenAPI 3.1 规范                            | |
|   |  paths / components.schemas / securitySchemes / tags          | |
|   +---------------------------------------------------------------+ |
|                              │                                      |
|              ┌───────────────┼───────────────┐                      |
|              ▼               ▼               ▼                      |
|   +----------------+  +----------------+  +----------------+        |
|   |  Swagger UI    |  |  ReDoc         |  |  静态文档       |        |
|   |  /docs         |  |  /redoc        |  |  Redocly CLI   |        |
|   |  交互式测试    |  |  只读展示      |  |  离线发布      |        |
|   +----------------+  +----------------+  +----------------+        |
|                                                                   |
+-------------------------------------------------------------------+
```

---

## 第六部分：完整示例

```python
"""
完整 API 文档示例

展示如何为一个电商平台编写完善的 API 文档。
包含：模型描述、参数文档、响应文档、安全方案、标签分组。
"""

from fastapi import FastAPI, Depends, HTTPException, Query, Path, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field, ConfigDict
from typing import Any

app: FastAPI = FastAPI(
    title="电商平台 API",
    description="""
## 概述

提供商品浏览、订单管理、用户认证等核心功能。

## 认证

大部分接口需要 JWT Token 认证。在右上角点击 **Authorize** 按钮，
输入你的 Token（格式：`Bearer <your-token>`）。

## 版本

当前版本：v2.0

## 速率限制

所有接口默认限制为 100 次/分钟。
    """,
    version="2.0.0",
    contact={
        "name": "API 支持",
        "email": "api@example.com",
    },
    license_info={
        "name": "MIT",
    },
)

security: HTTPBearer = HTTPBearer()


# ==================== 模型定义 ====================

class Address(BaseModel):
    """收货地址"""

    province: str = Field(..., description="省份", examples=["广东省"])
    city: str = Field(..., description="城市", examples=["深圳市"])
    district: str = Field(..., description="区县", examples=["南山区"])
    street: str = Field(..., description="详细地址", examples=["科技园南路 88 号"])
    zip_code: str = Field(..., description="邮政编码", pattern=r"^\d{6}$", examples=["518000"])


class ItemBase(BaseModel):
    """商品基础信息"""

    name: str = Field(
        ...,
        description="商品名称",
        min_length=1,
        max_length=200,
        examples=["iPhone 15 Pro Max 256GB"],
    )
    description: str | None = Field(
        default=None,
        description="商品详细描述",
        examples=["苹果最新旗舰手机，搭载 A17 Pro 芯片，钛金属设计"],
    )
    price: float = Field(
        ...,
        description="销售价格（单位：元）",
        gt=0,
        examples=[9999.0],
    )
    stock: int = Field(
        default=0,
        description="库存数量",
        ge=0,
        examples=[100],
    )


class ItemCreate(ItemBase):
    """创建商品请求"""

    category_id: int = Field(..., description="分类 ID", ge=1, examples=[1])
    tags: list[str] = Field(
        default_factory=list,
        description="商品标签",
        examples=["手机", "数码", "新品"],
    )


class ItemResponse(ItemBase):
    """商品响应"""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="商品 ID", examples=[1])
    category_id: int = Field(..., description="分类 ID", examples=[1])
    tags: list[str] = Field(default_factory=list, description="商品标签")
    created_at: str = Field(..., description="创建时间", examples=["2024-01-15T10:30:00"])


class OrderItem(BaseModel):
    """订单商品项"""

    item_id: int = Field(..., description="商品 ID", examples=[1])
    quantity: int = Field(..., description="购买数量", ge=1, examples=[2])


class OrderCreate(BaseModel):
    """创建订单请求"""

    items: list[OrderItem] = Field(..., description="商品列表", min_length=1)
    address: Address = Field(..., description="收货地址")
    remark: str | None = Field(
        default=None,
        description="订单备注",
        max_length=500,
        examples=["请在工作日配送"],
    )


class OrderResponse(BaseModel):
    """订单响应"""

    order_id: str = Field(..., description="订单号", examples=["ORD-2024-0115-001"])
    items: list[dict[str, Any]] = Field(..., description="订单商品")
    total_amount: float = Field(..., description="订单总金额", examples=[19998.0])
    status: str = Field(
        ...,
        description="订单状态",
        examples=["pending"],
    )
    address: Address = Field(..., description="收货地址")
    created_at: str = Field(..., description="下单时间")


class ErrorResponse(BaseModel):
    """错误响应"""

    detail: str = Field(..., description="错误信息")


class TokenResponse(BaseModel):
    """Token 响应"""

    access_token: str = Field(..., description="访问令牌")
    token_type: str = Field(default="bearer", description="令牌类型")


# ==================== 认证路由 ====================

@app.post(
    "/auth/login",
    summary="用户登录",
    description="使用用户名和密码登录，获取 JWT Token。Token 有效期 24 小时。",
    response_model=TokenResponse,
    tags=["认证"],
    responses={
        200: {"description": "登录成功，返回 Token"},
        401: {"description": "用户名或密码错误", "model": ErrorResponse},
        422: {"description": "请求参数验证失败"},
    },
)
def login(
    username: str = Query(..., description="用户名", min_length=3),
    password: str = Query(..., description="密码", min_length=6),
) -> dict[str, str]:
    return {"access_token": "eyJhbGciOiJIUzI1NiIs...", "token_type": "bearer"}


# ==================== 商品路由 ====================

@app.get(
    "/items",
    summary="获取商品列表",
    description="""
分页获取商品列表。

- 默认按创建时间倒序排列
- 支持按分类筛选
- 支持按关键词搜索
    """,
    response_model=list[ItemResponse],
    tags=["商品管理"],
    responses={
        200: {"description": "成功返回商品列表"},
        422: {"description": "请求参数验证失败"},
    },
)
def list_items(
    skip: int = Query(0, ge=0, description="跳过的记录数"),
    limit: int = Query(10, ge=1, le=100, description="返回的记录数"),
    category_id: int | None = Query(None, ge=1, description="按分类筛选"),
    keyword: str | None = Query(None, min_length=1, max_length=50, description="搜索关键词"),
) -> list[dict[str, Any]]:
    return []


@app.get(
    "/items/{item_id}",
    summary="获取商品详情",
    description="根据商品 ID 获取详细信息，包括库存、价格、分类等。",
    response_model=ItemResponse,
    tags=["商品管理"],
    responses={
        200: {"description": "成功获取商品信息"},
        404: {"description": "商品不存在", "model": ErrorResponse},
        422: {"description": "商品 ID 格式错误"},
    },
)
def get_item(
    item_id: int = Path(..., ge=1, description="商品 ID"),
) -> dict[str, Any]:
    return {
        "id": item_id,
        "name": "iPhone 15 Pro Max",
        "price": 9999.0,
        "stock": 100,
        "description": "苹果最新旗舰手机",
        "category_id": 1,
        "tags": ["手机", "数码"],
        "created_at": "2024-01-15T10:30:00",
    }


@app.post(
    "/items",
    summary="创建商品",
    description="添加新商品到平台。需要管理员权限。",
    response_model=ItemResponse,
    status_code=201,
    tags=["商品管理"],
    responses={
        201: {"description": "商品创建成功"},
        401: {"description": "未认证", "model": ErrorResponse},
        403: {"description": "权限不足", "model": ErrorResponse},
        422: {"description": "请求参数验证失败"},
    },
)
def create_item(
    item: ItemCreate,
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> dict[str, Any]:
    return {
        "id": 1,
        "name": item.name,
        "price": item.price,
        "stock": item.stock,
        "description": item.description,
        "category_id": item.category_id,
        "tags": item.tags,
        "created_at": "2024-01-15T10:30:00",
    }


@app.put(
    "/items/{item_id}",
    summary="更新商品",
    description="更新商品信息。部分更新请使用 PATCH 方法。",
    response_model=ItemResponse,
    tags=["商品管理"],
    responses={
        200: {"description": "更新成功"},
        404: {"description": "商品不存在", "model": ErrorResponse},
        401: {"description": "未认证"},
    },
)
def update_item(
    item_id: int = Path(..., ge=1, description="商品 ID"),
    item: ItemCreate = ...,
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> dict[str, Any]:
    return {"id": item_id, "name": item.name, "price": item.price, "stock": item.stock, "description": item.description, "category_id": item.category_id, "tags": item.tags, "created_at": "2024-01-15T10:30:00"}


@app.delete(
    "/items/{item_id}",
    summary="删除商品",
    description="软删除商品。商品状态变为已下架，不会从数据库中物理删除。",
    status_code=204,
    tags=["商品管理"],
    responses={
        204: {"description": "删除成功"},
        404: {"description": "商品不存在"},
        401: {"description": "未认证"},
    },
)
def delete_item(
    item_id: int = Path(..., ge=1, description="商品 ID"),
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> None:
    return None


# ==================== 订单路由 ====================

@app.post(
    "/orders",
    summary="创建订单",
    description="""
提交新订单。

**注意事项：**
- 库存不足时会返回 400 错误
- 订单创建后状态为 `pending`（待支付）
- 30 分钟内未支付会自动取消
    """,
    response_model=OrderResponse,
    status_code=201,
    tags=["订单管理"],
    responses={
        201: {"description": "订单创建成功"},
        400: {"description": "库存不足", "model": ErrorResponse},
        401: {"description": "未认证"},
        422: {"description": "请求参数验证失败"},
    },
)
def create_order(
    order: OrderCreate,
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> dict[str, Any]:
    return {
        "order_id": "ORD-2024-0115-001",
        "items": [{"item_id": i.item_id, "quantity": i.quantity} for i in order.items],
        "total_amount": 19998.0,
        "status": "pending",
        "address": order.address.model_dump(),
        "created_at": "2024-01-15T10:30:00",
    }


@app.get(
    "/orders/{order_id}",
    summary="获取订单详情",
    description="查询订单的完整信息，包括商品列表、金额、物流状态等。",
    response_model=OrderResponse,
    tags=["订单管理"],
    responses={
        200: {"description": "成功获取订单信息"},
        404: {"description": "订单不存在"},
        401: {"description": "未认证"},
    },
)
def get_order(
    order_id: str = Path(..., description="订单号", examples=["ORD-2024-0115-001"]),
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> dict[str, Any]:
    return {
        "order_id": order_id,
        "items": [{"item_id": 1, "quantity": 2}],
        "total_amount": 19998.0,
        "status": "pending",
        "address": {"province": "广东省", "city": "深圳市", "district": "南山区", "street": "科技园南路 88 号", "zip_code": "518000"},
        "created_at": "2024-01-15T10:30:00",
    }
```

---

## 常见坑点排查

### 坑点 1：自定义 openapi() 函数后文档不更新

**错误现象**：修改了路由或模型后，`/docs` 页面仍然显示旧内容。

**根因**：自定义 `app.openapi()` 函数中，`openapi_schema` 被缓存后不再重新生成。

**修复**：确保在开发环境禁用缓存，或每次强制重建：

```python
def custom_openapi() -> dict:
    # 开发模式每次都重新生成
    if app.openapi_schema and not settings.debug:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# 或者在启动时设置
@app.on_event("startup")
def clear_openapi_cache():
    app.openapi_schema = None
```

### 坑点 2：`responses` 参数中模型引用不生效

**错误现象**：

```python
@app.get("/items/{item_id}", responses={404: {"model": ErrorResponse}})
def get_item(item_id: int):
    ...
# Swagger 中 404 response 仍然是默认格式，没有 ErrorResponse schema
```

**根因**：`responses` 中的 `model` 参数用于生成 OpenAPI schema 文档，但不改变实际响应行为。实际返回什么由你的代码决定。

**修复**：同时定义文档和实际行为：

```python
@app.get(
    "/items/{item_id}",
    responses={
        200: {"description": "Success", "model": ItemResponse},
        404: {"description": "Not Found", "model": ErrorResponse},
    },
)
def get_item(item_id: int):
    item = find_item(item_id)
    if not item:
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found")
    return item
```

### 坑点 3：`response_model` 与 `responses` 冲突

**错误现象**：

```python
@app.get(
    "/items",
    response_model=list[ItemResponse],  # 全局返回模型
    responses={200: {"model": PaginatedResponse[ItemResponse]}},  # 冲突！
)
def get_items():
    ...
```

**根因**：当同时指定 `response_model` 和 `responses` 中的 200 模型时，`response_model` 优先级更高，`responses` 中的 200 会被忽略。

**修复**：只用一种方式定义成功响应：

```python
# 方式一：用 response_model
@app.get("/items", response_model=list[ItemResponse])
def get_items(): ...

# 方式二：用 responses 定义所有状态码
@app.get("/items", responses={
    200: {"model": list[ItemResponse]},
    422: {"description": "Validation Error"},
})
def get_items(): ...
```

### 坑点 4：Pydantic v2 的 `examples` vs `json_schema_extra`

**错误现象**：

```python
class Item(BaseModel):
    name: str = Field(..., example="test")  # Pydantic v1 写法，v2 中不显示！
```

**根因**：Pydantic v2 中 `Field(example=)` 不再直接用于 JSON Schema，需要使用 `examples`（复数）或 `json_schema_extra`。

**修复**：

```python
class Item(BaseModel):
    # ✅ Pydantic v2 正确写法
    name: str = Field(..., examples=["test"])

    # 或者
    name: str = Field(..., json_schema_extra={"example": "test"})
```

### 坑点排查表

| 现象 | 根因 | 修复 | 预防 |
|------|------|------|------|
| /docs 内容不更新 | openapi_schema 缓存 | 开发环境每次重建 | `debug=True` 时跳过缓存 |
| response model 不在 Schema 中 | `model` 只写文档不改变行为 | 同时定义 model 和实际 return 类型 | 检查 `response_model` 和 `responses` |
| 200 响应 Schema 错误 | response_model 覆盖 responses | 只用一种方式 | 统一风格 |
| `example=` 不显示 | Pydantic v1 vs v2 差异 | 使用 `examples=[]` | 升级后检查所有 Field |
| /docs 白屏 | Swagger JS CDN 被墙 | 使用本地 Swagger 资源 | `swagger_ui_parameters` |
| tags 元数据丢失 | tags 顺序不正确 | 使用 `openapi_tags` | FastAPI() 的 `openapi_tags` 参数 |

---

## 进阶用法

### 7.1 Swagger UI 自定义：修改 CSS/JS/Favicon

```python
from fastapi import FastAPI
from fastapi.openapi.docs import (
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)

app = FastAPI(
    docs_url=None,  # 禁用默认 /docs
    redoc_url=None,
)


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url or "/openapi.json",
        title=f"{app.title} - API Docs",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="/static/swagger-ui-bundle.js",     # 本地 JS
        swagger_css_url="/static/swagger-ui.css",           # 本地 CSS
        swagger_favicon_url="/static/favicon.ico",          # 自定义 favicon
    )


@app.get("/docs/oauth2-redirect", include_in_schema=False)
async def swagger_ui_redirect():
    return get_swagger_ui_oauth2_redirect_html()


# 通过 swagger_ui_parameters 自定义 Swagger UI 行为
app = FastAPI(
    swagger_ui_parameters={
        "deepLinking": True,          # URL 锚点直接链接到具体端点
        "defaultModelsExpandDepth": 1, # Schema 默认展开一层
        "defaultModelExpandDepth": 1,
        "displayRequestDuration": True, # 显示请求耗时
        "filter": True,                # 启用搜索过滤
        "syntaxHighlight.activate": True,
        "syntaxHighlight.theme": "monokai",
        "tryItOutEnabled": True,       # 默认开启 Try it out
        "persistAuthorization": True,  # 刷新后保持认证状态
    }
)
```

### 7.2 自定义 Swagger UI 注入 CSS

```python
# static/custom-swagger.css
custom_css = """
.swagger-ui .topbar {
    background-color: #1a1a2e;
}
.swagger-ui .topbar .download-url-wrapper .select-label {
    color: #eee;
}
.swagger-ui .info .title {
    color: #16213e;
}
.swagger-ui .scheme-container {
    background-color: #f8f9fa;
    box-shadow: none;
}
.swagger-ui .opblock-tag {
    border-bottom: 2px solid #e9ecef;
}
.swagger-ui .opblock.opblock-get {
    border-color: #61affe;
    background: rgba(97,175,254,.1);
}
.swagger-ui .opblock.opblock-post {
    border-color: #49cc90;
    background: rgba(73,204,144,.1);
}
.swagger-ui .opblock.opblock-put {
    border-color: #fca130;
    background: rgba(252,161,48,.1);
}
.swagger-ui .opblock.opblock-delete {
    border-color: #f93e3e;
    background: rgba(249,62,62,.1);
}
"""

@app.get("/custom-swagger.css", include_in_schema=False)
def swagger_css():
    from fastapi.responses import Response
    return Response(content=custom_css, media_type="text/css")


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui():
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="API Docs",
        swagger_css_url="/custom-swagger.css",
    )
```

### 7.3 安全方案文档（OAuth2 + Bearer 完整示例）

```python
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
    HTTPBearer,
    APIKeyHeader,
    APIKeyQuery,
)

# Bearer Token
bearer_scheme = HTTPBearer(
    scheme_name="JWT",
    description="输入 JWT token: Bearer <your-token>",
    bearerFormat="JWT",
)

# OAuth2 密码流
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/token",
    scheme_name="OAuth2Password",
    description="OAuth2 密码授权模式",
    scopes={
        "read": "读取权限",
        "write": "写入权限",
        "admin": "管理员权限",
    },
)

# API Key（请求头）
api_key_header = APIKeyHeader(
    name="X-API-Key",
    scheme_name="ApiKeyHeader",
    description="通过请求头 X-API-Key 传递 API Key",
)

# API Key（查询参数）
api_key_query = APIKeyQuery(
    name="api_key",
    scheme_name="ApiKeyQuery",
    description="通过查询参数 ?api_key=xxx 传递 API Key",
)

app = FastAPI(
    title="安全 API",
    version="1.0.0",
    # 全局安全方案（Swagger UI 中显示在所有端点）
    swagger_ui_init_oauth={
        "clientId": "your-client-id",
        "clientSecret": "your-client-secret",
        "appName": "API Docs",
        "scopes": "read write",
    },
)


@app.post("/auth/token", tags=["认证"])
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> dict:
    """获取访问令牌"""
    return {
        "access_token": "eyJhbGciOi...",
        "token_type": "bearer",
    }


@app.get("/public", tags=["公开"])
def public_endpoint() -> dict:
    """无需认证的公开端点"""
    return {"message": "Public data"}


@app.get(
    "/protected/jwt",
    tags=["受保护"],
    dependencies=[Depends(bearer_scheme)],  # 需要 Bearer Token
    responses={401: {"description": "无效的 JWT Token"}},
)
def protected_jwt() -> dict:
    return {"message": "Protected by JWT"}


@app.get(
    "/protected/api-key-header",
    tags=["受保护"],
    dependencies=[Depends(api_key_header)],
)
def protected_api_key_header() -> dict:
    return {"message": "Protected by API Key (Header)"}


@app.get(
    "/protected/oauth2",
    tags=["受保护"],
    dependencies=[Depends(oauth2_scheme)],
)
def protected_oauth2() -> dict:
    return {"message": "Protected by OAuth2"}


# 生成的 OpenAPI 中会包含所有安全方案
# components.securitySchemes:
#   JWT: { type: http, scheme: bearer, bearerFormat: JWT }
#   OAuth2Password: { type: oauth2, flows: { password: ... } }
#   ApiKeyHeader: { type: apiKey, in: header, name: X-API-Key }
#   ApiKeyQuery: { type: apiKey, in: query, name: api_key }
```

### 7.4 API 版本化文档

```python
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

app = FastAPI(docs_url=None, openapi_url=None)


# ===== v1 路由 =====
v1_app = FastAPI(
    title="API v1",
    version="1.0.0-deprecated",
    description="## API v1（已弃用，请迁移到 v2）",
    docs_url=None,
    openapi_url=None,
)

@v1_app.get("/items", tags=["商品"], deprecated=True)
def v1_get_items() -> list[dict]:
    return [{"id": 1, "name": "Apple"}]

@v1_app.get("/users", tags=["用户"], deprecated=True)
def v1_get_users() -> list[dict]:
    return [{"id": 1, "name": "Alice"}]


# ===== v2 路由 =====
v2_app = FastAPI(
    title="API v2",
    version="2.0.0",
    description="## API v2（当前版本）",
    docs_url=None,
    openapi_url=None,
)

@v2_app.get("/items", tags=["商品"])
def v2_get_items() -> list[dict]:
    return [{"id": 1, "name": "Apple Pro"}]

@v2_app.get("/users", tags=["用户"])
def v2_get_users() -> list[dict]:
    return [{"id": 1, "name": "Alice Wang"}]


# ===== 挂载子应用 =====
app.mount("/v1", v1_app)
app.mount("/v2", v2_app)


# ===== 自定义文档端点 =====
def get_versioned_openapi(version: str) -> dict:
    if version == "v1":
        target = v1_app
        spec = get_openapi(
            title="API v1 (Deprecated)",
            version="1.0.0",
            routes=v1_app.routes,
            description="## Deprecated — 请使用 /v2",
        )
    else:
        target = v2_app
        spec = get_openapi(
            title="API v2",
            version="2.0.0",
            routes=v2_app.routes,
        )
    return spec


@app.get("/v1/openapi.json", include_in_schema=False)
def v1_openapi() -> dict:
    return get_versioned_openapi("v1")


@app.get("/v2/openapi.json", include_in_schema=False)
def v2_openapi() -> dict:
    return get_versioned_openapi("v2")


@app.get("/v1/docs", include_in_schema=False)
async def v1_docs():
    from fastapi.openapi.docs import get_swagger_ui_html
    return get_swagger_ui_html(
        openapi_url="/v1/openapi.json",
        title="API v1 - Deprecated",
    )


@app.get("/v2/docs", include_in_schema=False)
async def v2_docs():
    from fastapi.openapi.docs import get_swagger_ui_html
    return get_swagger_ui_html(
        openapi_url="/v2/openapi.json",
        title="API v2",
    )


@app.get("/docs", include_in_schema=False)
async def docs_index():
    """文档首页：列出所有版本"""
    from fastapi.responses import HTMLResponse
    return HTMLResponse("""
    <html>
    <head><title>API Documentation</title></head>
    <body>
        <h1>API Versions</h1>
        <ul>
            <li><a href="/v2/docs">API v2 (Current)</a></li>
            <li><a href="/v1/docs">API v1 (Deprecated)</a></li>
        </ul>
    </body>
    </html>
    """)
```

### 7.5 生成客户端 SDK

```bash
# 方式一：openapi-generator（最通用）
npm install -g @openapitools/openapi-generator-cli

# 生成 Python 客户端
openapi-generator-cli generate \
  -i http://localhost:8000/openapi.json \
  -g python \
  -o ./generated/python-client \
  --additional-properties=packageName=my_api_client

# 生成 TypeScript 客户端
openapi-generator-cli generate \
  -i http://localhost:8000/openapi.json \
  -g typescript-axios \
  -o ./generated/ts-client

# 方式二：fastapi-code-generator（FastAPI 专用）
pip install fastapi-code-generator

# 生成 Python 客户端代码
fastapi-codegen --input openapi.json --output client.py
```

```python
# Python 脚本：程序化生成客户端
import subprocess
import json

def generate_clients(openapi_url: str, output_dir: str):
    """自动生成多语言客户端"""

    languages = {
        "python": {"packageName": "api_client", "projectName": "my-api-client"},
        "typescript-axios": {"npmName": "@my/api-client"},
        "go": {"packageName": "apiclient"},
    }

    for lang, props in languages.items():
        cmd = [
            "openapi-generator-cli", "generate",
            "-i", openapi_url,
            "-g", lang,
            "-o", f"{output_dir}/{lang}",
        ]
        for k, v in props.items():
            cmd.extend(["--additional-properties", f"{k}={v}"])

        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✓ Generated {lang} client")
        else:
            print(f"✗ Failed to generate {lang}: {result.stderr[:200]}")

if __name__ == "__main__":
    generate_clients(
        "http://localhost:8000/openapi.json",
        "./generated-clients",
    )
```

### 7.6 多场景请求/响应示例

```python
from pydantic import BaseModel, Field
from fastapi import FastAPI
from typing import Annotated


class UserCreate(BaseModel):
    """用户注册请求"""

    username: str = Field(
        ...,
        min_length=3,
        max_length=30,
        pattern=r"^[a-zA-Z0-9_]+$",
        json_schema_extra={
            "examples": ["john_doe", "alice_wang"],
            "invalid_examples": {
                "too_short": {"value": "ab", "reason": "长度不足 3 个字符"},
                "special_char": {"value": "john@doe", "reason": "包含非法字符 @"},
                "too_long": {"value": "a" * 31, "reason": "超过 30 个字符限制"},
            },
        },
    )
    email: str = Field(
        ...,
        json_schema_extra={
            "examples": ["john@example.com"],
            "format": "email",
        },
    )
    role: str = Field(
        default="user",
        pattern="^(user|admin|moderator)$",
        json_schema_extra={
            "examples": ["user", "admin"],
            "invalid_examples": {
                "invalid_role": {"value": "superuser", "reason": "角色不存在"},
            },
        },
    )


class UserResponse(BaseModel):
    """用户注册成功响应"""
    id: int = Field(examples=[1])
    username: str = Field(examples=["john_doe"])
    email: str = Field(examples=["john@example.com"])
    role: str = Field(examples=["user"])


class ValidationErrorDetail(BaseModel):
    field: str = Field(examples=["email"])
    message: str = Field(examples=["不是有效的邮箱格式"])


class ErrorResponse(BaseModel):
    detail: str = Field(examples=["请求参数验证失败"])


@app.post(
    "/users",
    summary="注册新用户",
    description="""
注册新的用户账号。

## 请求示例

### 成功场景
```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "role": "user"
}
```

### 参数校验失败
```json
{
  "username": "ab",
  "email": "not-an-email",
  "role": "superuser"
}
```

响应 422:
```json
{
  "detail": "请求参数验证失败"
}
```
    """,
    response_model=UserResponse,
    status_code=201,
    responses={
        201: {"description": "注册成功", "model": UserResponse},
        400: {"description": "用户名或邮箱已被注册", "model": ErrorResponse},
        422: {"description": "参数验证失败", "model": ErrorResponse},
    },
    openapi_extra={
        "x-code-samples": [
            {"lang": "Python", "source": "import requests\nr = requests.post(...)"},
            {"lang": "JavaScript", "source": "fetch('/users', { method: 'POST', ... })"},
            {"lang": "curl", "source": "curl -X POST http://localhost:8000/users -H 'Content-Type: application/json' -d '{\"username\":\"...\"}'"},
        ],
    },
)
def create_user(user: UserCreate) -> dict:
    return {
        "id": 1,
        "username": user.username,
        "email": user.email,
        "role": user.role,
    }
```

### 7.7 自定义 OpenAPI 钩子：自动添加通用参数

```python
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.routing import APIRoute


def add_common_parameters(openapi_schema: dict) -> dict:
    """为所有 GET 端点自动添加通用分页参数到 OpenAPI schema"""

    for path, methods in openapi_schema.get("paths", {}).items():
        for method, operation in methods.items():
            if method.lower() == "get" and method != "parameters":
                params = operation.get("parameters", [])

                # 只在没有自定义分页参数时添加
                has_page = any(p.get("name") == "page" for p in params)
                if not has_page:
                    params.append({
                        "name": "page",
                        "in": "query",
                        "required": False,
                        "schema": {"type": "integer", "default": 1, "minimum": 1},
                        "description": "页码，从 1 开始",
                    })
                    params.append({
                        "name": "size",
                        "in": "query",
                        "required": False,
                        "schema": {"type": "integer", "default": 20, "minimum": 1, "maximum": 100},
                        "description": "每页记录数",
                    })

                operation["parameters"] = params

    return openapi_schema


def custom_openapi_with_hooks() -> dict:
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        routes=app.routes,
    )

    # 钩子 1：添加通用分页参数
    openapi_schema = add_common_parameters(openapi_schema)

    # 钩子 2：添加服务器列表
    openapi_schema["servers"] = [
        {"url": "https://api.example.com/v2", "description": "生产环境"},
        {"url": "https://staging-api.example.com/v2", "description": "预发布环境"},
        {"url": "http://localhost:8000", "description": "本地开发"},
    ]

    # 钩子 3：修改所有 JSON 响应的默认 content-type
    for path, methods in openapi_schema.get("paths", {}).items():
        for method, operation in methods.items():
            if method in ("parameters", "servers"):
                continue
            responses = operation.get("responses", {})
            for status_code, response in responses.items():
                if "content" in response and "application/json" in response.get("content", {}):
                    # 确保 application/json 是默认格式
                    pass

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi_with_hooks


@app.get("/items")
def get_items():
    """通过钩子自动添加了 page 和 size 参数"""
    return []
```

---

## 调试与排错技巧

### 技巧 1：查看完整的 OpenAPI JSON

```bash
# 命令行查看
curl -s http://localhost:8000/openapi.json | python -m json.tool > openapi.json
code openapi.json  # VS Code 打开查看

# 浏览器直接访问
open http://localhost:8000/openapi.json
```

### 技巧 2：检查 Schema 是否包含预期模型

```python
def debug_schemas(app: FastAPI) -> set[str]:
    """打印所有已注册的 Schema 名称"""
    spec = app.openapi()
    schemas = spec.get("components", {}).get("schemas", {})
    print(f"Registered schemas ({len(schemas)}):")
    for name in sorted(schemas.keys()):
        print(f"  - {name}")

    # 检查是否有未引用的 Schema
    refs = set()
    import json
    spec_str = json.dumps(spec)
    import re
    for match in re.findall(r'"\$ref":\s*"#/components/schemas/(\w+)"', spec_str):
        refs.add(match)

    unused = set(schemas.keys()) - refs
    if unused:
        print(f"\nUnreferenced schemas: {unused}")
    return set(schemas.keys())
```

### 技巧 3：验证 Swagger UI 资源加载

```bash
# 检查 Swagger UI 是否从 CDN 加载（可能被墙）
curl -s http://localhost:8000/docs | grep "swagger-ui"

# 输出类似:
# <script src="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js"></script>
# <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css">

# 如果 CDN 不可达，使用本地资源或国内镜像
app = FastAPI(
    swagger_js_url="https://cdn.bootcdn.net/ajax/libs/swagger-ui/5.10.5/swagger-ui-bundle.js",
    swagger_css_url="https://cdn.bootcdn.net/ajax/libs/swagger-ui/5.10.5/swagger-ui.css",
)
```

{% hint style="tip" %}
**文档质量评分**：一个良好的 API 文档应满足：
1. 所有端点都有 `summary` + `description`
2. 所有参数都有 `description` + `examples`
3. 所有可能的状态码都有 `responses` 定义
4. 模型字段都有 `Field(description=..., examples=...)`
5. 认证方式在 `/docs` 的 Authorize 面板中可配置
6. 提供至少一个完整的请求/响应示例
{% endhint %}

---

## 总结

| 知识点 | 说明 |
|--------|------|
| OpenAPI 规范 | RESTful API 的标准描述格式 |
| /docs | Swagger UI 交互式文档 |
| /redoc | ReDoc 只读文档 |
| summary/description | 端点的标题和详细说明 |
| tags | 端点分组 |
| Field(description) | 字段级文档 |
| responses | 多状态码文档 |
| securitySchemes | 认证方案文档 |
| openapi_extra | 自定义扩展 |
| 静态导出 | openapi.json → HTML |
| 自定义 CSS/JS | Swagger UI 定制主题和品牌 |
| OAuth2 文档 | 完整的 OAuth2 密码流 / Bearer 文档 |
| API 版本化 | 多版本共存、独立 /docs 端点 |
| 客户端 SDK 生成 | openapi-generator 自动生成多语言 SDK |
| 多场景示例 | 成功/失败/校验错误的完整示例 |
| OpenAPI 钩子 | 自动添加通用参数、服务器列表等 |

```
+---------------------------------------------------+
|               API 文档生成全景图                    |
+---------------------------------------------------+
|                                                   |
|  代码定义 ──┐                                     |
|             │    +-------------+    +-----------+ |
|  类型提示 ──┼───>│  FastAPI    ├───>│ OpenAPI   | |
|             │    │  解析引擎   │    │ 3.1 JSON  | |
|  Pydantic ──┤    +-------------+    +-----------+ |
|  模型       │                          │          |
|             │              ┌───────────┼────────┐ |
|             │              ▼           ▼        ▼ |
|             │         /docs      /redoc   /openapi|
|             │       (Swagger)  (ReDoc)   .json    |
|             │                                      |
|  手动增强 ──┘    summary, description, tags,      |
|                  Field(), examples, responses      |
+---------------------------------------------------+
```
