# 09-RESTful-API

> Python 3.11+

本章讲解 Flask-RESTful 扩展构建 REST API。

---

## 概念铺垫

REST（Representational State Transfer）是一种 Web API 设计风格。Flask-RESTful 基于 Flask 的 `MethodView`，通过 `Resource` 类将 HTTP 方法映射到类方法（`get()`/`post()`/`put()`/`delete()`）。Richardson 成熟度模型将 REST API 分为四级：Level 0（RPC）、Level 1（资源拆分）、Level 2（HTTP 动词+状态码）、Level 3（HATEOAS 超媒体驱动）。

Flask-RESTful 提供 `reqparse`（请求参数解析验证）、`fields`（响应字段序列化），以及通过 Blueprint 实现 API 版本控制。

---

### L1 理解层：会用

## 第一部分：Flask-RESTful 简介

### 1.1 实际场景

你需要为前端应用提供 API 接口，如获取文章列表、创建文章、更新文章、删除文章等。

**问题：如何构建规范的 REST API？**

### 1.2 安装

```bash
uv add flask-restful
```

### 1.3 基本用法

```python
from flask import Flask, request
from flask_restful import Api, Resource
from typing import Any

app: Flask = Flask(__name__)
api: Api = Api(app)


class HelloWorld(Resource):
    def get(self) -> dict[str, str]:
        return {"message": "Hello World"}

    def post(self) -> tuple[dict[str, Any], int]:
        data: dict[str, Any] = request.get_json()
        return {"received": data}, 201


# 注册资源
api.add_resource(HelloWorld, "/hello")
```

---

## 第二部分：资源类（Resource）

### 2.1 实际场景

文章 API 需要 GET 获取列表、POST 创建文章、PUT 更新文章、DELETE 删除文章。

**问题：如何用资源类组织这些操作？**

### 2.2 文章 API 示例

资源类将 HTTP 方法映射到类方法，每个方法对应一种 HTTP 操作。

```python
from flask_restful import Resource, request, abort
from typing import Any

articles_db: dict[int, dict[str, Any]] = {}  # 模拟数据库
next_id: int = 1


class ArticleList(Resource):
    """文章列表资源"""

    def get(self) -> tuple[dict[str, list], int]:
        """获取所有文章"""
        return {"articles": list(articles_db.values())}, 200

    def post(self) -> tuple[dict[str, Any], int]:
        """创建新文章"""
        data: dict[str, Any] | None = request.get_json()

        if not data or "title" not in data:
            abort(400, message="标题是必需的")

        global next_id
        article: dict[str, Any] = {
            "id": next_id,
            "title": data["title"],
            "content": data.get("content", "")
        }
        articles_db[next_id] = article
        next_id += 1

        return article, 201


class ArticleResource(Resource):
    """单篇文章资源"""

    def get(self, article_id: int) -> tuple[dict[str, Any], int]:
        """获取单篇文章"""
        article: dict[str, Any] | None = articles_db.get(article_id)
        if not article:
            abort(404, message="文章不存在")
        return article, 200

    def put(self, article_id: int) -> tuple[dict[str, Any], int]:
        """更新文章（完整更新）"""
        article: dict[str, Any] | None = articles_db.get(article_id)
        if not article:
            abort(404, message="文章不存在")

        data: dict[str, Any] = request.get_json()
        article["title"] = data.get("title", article["title"])
        article["content"] = data.get("content", article["content"])

        return article, 200

    def delete(self, article_id: int) -> tuple[str, int]:
        """删除文章"""
        if article_id not in articles_db:
            abort(404, message="文章不存在")

        del articles_db[article_id]
        return "", 204


# 注册资源
api.add_resource(ArticleList, "/api/articles")
api.add_resource(ArticleResource, "/api/articles/<int:article_id>")
```

---

## 第三部分：请求解析（reqparse）

### 3.1 实际场景

创建文章时，title 是必填项，content 是可选的，category 只能是 tech、life、work 三个选项。

**问题：如何验证和解析请求参数？**

### 3.2 请求解析示例

`reqparse` 用于解析和验证请求数据。

```python
from flask_restful import reqparse

# 创建解析器
parser: reqparse.RequestParser = reqparse.RequestParser()
parser.add_argument(
    "title",
    type=str,
    required=True,
    help="标题是必需的",
    location="json"
)
parser.add_argument(
    "content",
    type=str,
    required=False,
    default="",
    help="文章内容",
    location="json"
)
parser.add_argument(
    "category",
    type=str,
    choices=["tech", "life", "work"],  # 限制选项
    required=False,
    location="json"
)
parser.add_argument(
    "tags",
    type=list,
    action="append",  # 允许多个值
    location="json"
)


class ArticleCreate(Resource):
    def post(self) -> tuple[dict[str, Any], int]:
        args: dict[str, Any] = parser.parse_args()

        article: dict[str, Any] = {
            "title": args["title"],
            "content": args["content"],
            "category": args.get("category"),
            "tags": args.get("tags", [])
        }

        return article, 201
```

### 3.3 location 参数

```python
# 从不同位置获取参数
parser.add_argument("name", location="args")      # 查询参数 ?name=xxx
parser.add_argument("data", location="json")      # JSON 请求体
parser.add_argument("file", location="files")     # 上传文件
parser.add_argument("token", location="headers")  # 请求头
parser.add_argument("id", location="form")        # 表单数据
```

---

## 第四部分：字段序列化

### 4.1 实际场景

返回的文章数据需要格式化，日期字段需要特定格式，嵌套的用户对象需要只返回部分字段。

**问题：如何控制响应数据的格式？**

### 4.2 字段序列化示例

使用 `fields` 模块可以控制响应数据的格式和结构。

```python
from flask_restful import fields, marshal_with
from typing import Any

# 定义字段
article_fields: dict[str, fields.Field] = {
    "id": fields.Integer,
    "title": fields.String,
    "content": fields.String,
    "created_at": fields.DateTime,
}

# 嵌套字段
author_fields: dict[str, fields.Field] = {
    "id": fields.Integer,
    "name": fields.String,
    "email": fields.String,
}

article_with_author: dict[str, fields.Field] = {
    "id": fields.Integer,
    "title": fields.String,
    "author": fields.Nested(author_fields),
}


class ArticleAPI(Resource):
    @marshal_with(article_fields)
    def get(self, article_id: int) -> dict[str, Any]:
        article: dict[str, Any] = Article.query.get_or_404(article_id)
        return article  # 自动序列化为指定格式
```

---

## 第五部分：API 版本控制

### 5.1 实际场景

API 升级后，旧版本的客户端仍然需要访问旧 API，新客户端使用新 API。

**问题：如何同时支持多个 API 版本？**

### 5.2 版本控制示例

使用蓝图实现 API 版本隔离，支持多版本并存。

```python
from flask import Flask, Blueprint
from flask_restful import Api

app: Flask = Flask(__name__)

# 创建版本蓝图
api_v1: Blueprint = Blueprint("api_v1", __name__, url_prefix="/api/v1")
api_v2: Blueprint = Blueprint("api_v2", __name__, url_prefix="/api/v2")

api_v1_api: Api = Api(api_v1)
api_v2_api: Api = Api(api_v2)


# v1 API 路由
class ArticleListV1(Resource):
    def get(self) -> dict[str, Any]:
        return {"version": "v1", "articles": []}


api_v1_api.add_resource(ArticleListV1, "/articles")


# v2 API 路由（新功能）
class ArticleListV2(Resource):
    def get(self) -> dict[str, Any]:
        # v2 支持更多过滤选项
        return {
            "version": "v2",
            "articles": [],
            "filters": ["author", "category", "tag"]
        }


api_v2_api.add_resource(ArticleListV2, "/articles")

# 注册蓝图
app.register_blueprint(api_v1)
app.register_blueprint(api_v2)
```

---

### L2 实践层：用好

| 做法 | 原因 | 示例 |
|------|------|------|
| 统一错误响应格式 | 前端易解析 | `{"error":{"code":"...","message":"..."}}` |
| 使用正确 HTTP 状态码 | 语义明确 | 201 Created、204 No Content、404 Not Found |
| API 版本控制（URL 路径） | 向后兼容 | `/api/v1/articles`、`/api/v2/articles` |
| `reqparse` 白名单验证 | 防止注入未预期字段 | `location="json"` + `required=True` |
| `marshal_with` 序列化 | 控制输出字段 | 隐藏内部字段、格式化日期 |

#### 反模式

```python
# ❌ 错误：POST 返回 200
def post(self):
    return {"created": article}, 200  # 应为 201

# ✅ 正确：POST 返回 201 Created
def post(self):
    return article, 201

# ❌ 错误：所有错误用 500
abort(500, message="Not Found")  # 应为 404
```

#### REST 成熟度目标

| 项目规模 | 建议目标 |
|---------|---------|
| 内部工具 API | Level 1-2 |
| 公开 API | Level 2（最低）+ Level 3 可选项 |
| 微服务间通信 | Level 1-2 足够 |

---

### L3 专家层：深入

## 第六部分：L3 专家层

### 6.1 REST 成熟度模型（Richardson Maturity Model）

RESTful API 的设计质量可通过 Richardson Maturity Model（RMM）划分为四个等级，级别越高，API 的 REST 纯度越高。

#### 成熟度层级

```
+--------------------------------------------------+
| Level 3: HATEOAS                                 |
|  响应包含超媒体链接，驱动客户端状态转移           |
+--------------------------------------------------+
| Level 2: HTTP Verbs                              |
|  正确使用 GET/POST/PUT/DELETE + 状态码            |
+--------------------------------------------------+
| Level 1: Resources                               |
|  将 URI 拆分为独立资源（/users, /articles）       |
+--------------------------------------------------+
| Level 0: POX (Plain Old XML/JSON)                |
|  单一端点，通过请求体区分操作（RPC 风格）          |
+--------------------------------------------------+
```

```python
from typing import Any

# Level 0: RPC 风格 — 所有操作走同一个端点
@app.route("/api", methods=["POST"])
def rpc_endpoint() -> dict[str, Any]:
    data: dict[str, Any] = request.get_json()
    action: str = data["action"]  # "getArticle", "createArticle", ...
    if action == "getArticle":
        return get_article(data["id"])
    return {"error": "unknown action"}

# Level 1: 资源 — 不同资源用不同 URI
# GET    /api/articles
# GET    /api/articles/1
# DELETE /api/articles/1

# Level 2: HTTP 动词 + 状态码
@app.route("/api/articles/<int:article_id>", methods=["PUT"])
def update_article(article_id: int) -> tuple[dict[str, Any], int]:
    # 使用 PUT 语义：完整替换
    article: Article | None = Article.query.get(article_id)
    if not article:
        return {"error": "not found"}, 404
    # ... 更新逻辑
    return article.to_dict(), 200

# Level 3: HATEOAS — 响应包含操作链接
def article_with_links(article: Article) -> dict[str, Any]:
    return {
        "id": article.id,
        "title": article.title,
        "_links": {
            "self":       {"href": f"/api/articles/{article.id}"},
            "author":     {"href": f"/api/users/{article.author_id}"},
            "comments":   {"href": f"/api/articles/{article.id}/comments"},
            "update":     {"href": f"/api/articles/{article.id}", "method": "PUT"},
            "delete":     {"href": f"/api/articles/{article.id}", "method": "DELETE"},
        }
    }
```

#### 性能考量

| 成熟度等级 | 开发成本 | 客户端复杂度 | 缓存友好度 | 适用场景 |
|-----------|---------|-------------|-----------|---------|
| Level 0 | 低 | 低 | 差（全 POST） | 内部 RPC 服务 |
| Level 1 | 低 | 中 | 中 | 简单 CRUD API |
| Level 2 | 中 | 中 | 好 | 主流 REST API |
| Level 3 | 高 | 高 | 极好 | 公开 API 平台 |

#### 设计动机

| 为什么升级 | 解决的问题 |
|-----------|-----------|
| L0 → L1 | 资源定位不清晰，所有操作耦合在一个端点 |
| L1 → L2 | 无法利用 HTTP 语义（状态码、方法语义、中间件缓存） |
| L2 → L3 | 客户端需硬编码 URI，服务端结构变化需客户端同步更新 |

### 6.2 HATEOAS 的实现原理

HATEOAS（Hypermedia As The Engine Of Application State）要求服务端在响应中提供可操作的链接，使客户端能够动态发现可用操作。

#### 链接注入机制

```
+----------------+      +-------------------+      +------------------+
| Resource View  | ---> | Link Builder      | ---> | Response Builder |
| (Article data) |      | (生成 href/method)|      | (组装 JSON 响应)  |
+----------------+      +-------------------+      +------------------+
         |                         |                        |
         v                         v                        v
   原始数据对象              路由反向解析               带 _links 的 JSON
   Article(id=1)          url_for('article')        {data, _links}
```

```python
from flask import url_for
from typing import Any

class HALResponse:
    """Hypertext Application Language 响应包装器"""

    def __init__(self, data: dict[str, Any], links: dict[str, dict[str, str]] | None = None) -> None:
        self._embedded: dict[str, Any] = data
        self._links: dict[str, dict[str, str]] = links or {}
        if "self" not in self._links:
            self._links["self"] = {"href": "/"}

    def add_link(self, rel: str, href: str, method: str = "GET") -> None:
        self._links[rel] = {"href": href, "method": method}

    def to_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = {"_links": self._links}
        result.update(self._embedded)
        return result


def build_article_response(article: Article) -> dict[str, Any]:
    hal: HALResponse = HALResponse(
        data={"id": article.id, "title": article.title},
        links={"self": {"href": url_for("article_detail", article_id=article.id, _external=True)}}
    )
    hal.add_link("author", url_for("user_detail", user_id=article.author_id, _external=True))
    hal.add_link("comments", url_for("article_comments", article_id=article.id, _external=True))
    hal.add_link("update", url_for("article_detail", article_id=article.id, _external=True), method="PUT")
    hal.add_link("delete", url_for("article_detail", article_id=article.id, _external=True), method="DELETE")
    return hal.to_dict()
```

### 6.3 Flask-RESTful 的 Resource 分派机制

Flask-RESTful 通过 `Api.add_resource()` 将 Resource 类注册到路由，其内部通过反射机制将 HTTP 方法分派到对应的方法。

#### 分派流程

```
+-----------+     +----------------+     +-------------------+     +-------------+
| HTTP      | --->| Flask Router   | --->| Api.dispatch_request|->| Resource    |
| Request   |     | (URL匹配)      |     | (查找Resource类)  |     | .method()   |
+-----------+     +----------------+     +-------------------+     +-------------+
      |                    |                      |                        |
      v                    v                      v                        v
  GET /api/          匹配到 ArticleList     getattr(resource,           执行 get()
  articles<id>                              "get")(article_id)           返回 JSON
```

```python
# Flask-RESTful 内部简化实现
from flask.views import MethodView
from typing import Callable, Any

class Resource(MethodView):
    """Resource 基类 — 继承 MethodView"""

    methods: list[str] = ["GET", "POST", "PUT", "DELETE", "PATCH"]

    def dispatch_request(self, *args: Any, **kwargs: Any) -> Any:
        # 1. 确定 HTTP 方法
        http_method: str = request.method.upper()

        # 2. 检查是否实现了该方法
        method: Callable[..., Any] | None = getattr(self, http_method.lower(), None)
        if method is None:
            abort(405)

        # 3. 执行方法并返回结果
        resp: Any = method(*args, **kwargs)
        return self.make_response(resp)


class Api:
    def add_resource(
        self,
        resource: type[Resource],
        *urls: str,
        **kwargs: Any
    ) -> None:
        # 为每个 URL 创建 Resource 实例并注册到 Flask
        for url in urls:
            endpoint: str = kwargs.pop("endpoint", None) or resource.__name__.lower()
            view_func: Callable = resource.as_view(endpoint, api=self)
            self.app.add_url_rule(url, view_func=view_func, **kwargs)
```

#### 设计动机

| 机制 | 解决的问题 |
|-----|-----------|
| MethodView 继承 | 复用 Flask 内置的 HTTP 方法分派，不重复造轮子 |
| `as_view()` | 将类转换为 WSGI 可调用的函数，每次请求创建新实例 |
| `make_response()` | 自动将 dict/list 序列化为 JSON，设置 Content-Type |
| URL 参数传递 | 路由变量 `<int:article_id>` 自动作为方法参数传入 |

### 6.4 知识关联

```
+---------------------+          +------------------------+          +--------------------+
| Richardson Maturity |          | HATEOAS                |          | Flask-RESTful      |
| Model               |          |                        |          | Dispatch           |
+---------------------+          +------------------------+          +--------------------+
|  L0: RPC            |          |  _links 字段注入       |          |  MethodView        |
|  L1: Resources      |--------->|  url_for 反向解析      |<---------|  getattr dispatch  |
|  L2: HTTP Verbs     |          |  HAL/JSON-LD 格式      |          |  as_view()         |
|  L3: Hypermedia     |          |  客户端动态发现        |          |  make_response()   |
+---------------------+          +------------------------+          +--------------------+
         |                                 |                                 |
         v                                 v                                 v
+---------------------------------------------------------------------------+
|                          设计目标                                          |
|  可发现性 · 可缓存性 · 可组合性 · 松耦合 · 向后兼容                        |
+---------------------------------------------------------------------------+
```

---

## 总结

| 知识点 | 说明 |
|---------|------|
| Resource | 资源类 |
| HTTP 方法 | GET, POST, PUT, DELETE |
| reqparse | 请求参数解析 |
| fields | 响应字段序列化 |
| 版本控制 | Blueprint 实现 |