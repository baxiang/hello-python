# API 文档生成（详细版）

> Python 3.11+

本章讲解 FastAPI 的 API 文档自动生成机制，包括 OpenAPI 规范、Swagger UI、ReDoc 以及如何定制文档内容。

---

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
