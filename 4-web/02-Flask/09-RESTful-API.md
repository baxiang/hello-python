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

---

## 第六部分：HATEOAS 深层实现

### 6.1 实际场景

前端需要动态发现 API 的可用操作，而不是硬编码 URL。

**问题：如何在 API 响应中嵌入可操作的超媒体链接？**

### 6.2 HATEOAS 响应构建器

```python
from flask import url_for, request
from typing import Any

class HATEOASBuilder:
    """HATEOAS 响应构建器"""

    def __init__(self, data: dict[str, Any]) -> None:
        self._data: dict[str, Any] = data
        self._links: dict[str, dict[str, str]] = {}
        self._embedded: dict[str, Any] = {}

    def add_link(self, rel: str, href: str, method: str = "GET",
                 title: str | None = None) -> "HATEOASBuilder":
        self._links[rel] = {
            "href": href,
            "method": method,
            **({"title": title} if title else {})
        }
        return self

    def add_embedded(self, rel: str, resource: dict[str, Any]) -> "HATEOASBuilder":
        self._embedded[rel] = resource
        return self

    def build(self) -> dict[str, Any]:
        result: dict[str, Any] = dict(self._data)
        if self._links:
            result["_links"] = self._links
        if self._embedded:
            result["_embedded"] = self._embedded
        return result


class ArticleHATEOAS:
    """文章资源 HATEOAS 链接生成"""

    @staticmethod
    def single(article: Article, include_author: bool = False) -> dict[str, Any]:
        builder = HATEOASBuilder({
            "id": article.id,
            "title": article.title,
            "content": article.content,
            "created_at": article.created_at.isoformat(),
        })

        article_id = article.id
        builder.add_link(
            "self",
            url_for("api.article_detail", article_id=article_id, _external=True)
        )
        builder.add_link(
            "collection",
            url_for("api.article_list", _external=True)
        )
        builder.add_link(
            "author",
            url_for("api.user_detail", user_id=article.author_id, _external=True)
        )

        # 条件链接：仅当有权限或状态允许时添加
        if article.is_editable_by(current_user):
            builder.add_link("update",
                url_for("api.article_detail", article_id=article_id, _external=True),
                method="PUT"
            )
            builder.add_link("delete",
                url_for("api.article_detail", article_id=article_id, _external=True),
                method="DELETE"
            )

        return builder.build()

    @staticmethod
    def collection(articles: list[Article], page: int, per_page: int,
                   total: int) -> dict[str, Any]:
        builder = HATEOASBuilder({
            "items": [ArticleHATEOAS.single(a) for a in articles],
            "page": page,
            "per_page": per_page,
            "total": total,
        })

        base_url = url_for("api.article_list", _external=True)

        builder.add_link("self", f"{base_url}?page={page}&per_page={per_page}")

        if page > 1:
            builder.add_link("prev", f"{base_url}?page={page-1}&per_page={per_page}")
        if page * per_page < total:
            builder.add_link("next", f"{base_url}?page={page+1}&per_page={per_page}")

        builder.add_link("search",
            f"{base_url}?search={{query}}",
            title="搜索文章",
        )

        return builder.build()
```

### 6.3 客户端 HATEOAS 消费示例

```python
# 客户端利用 _links 导航，无需硬编码 URL
import requests

def navigate_api(entry_point: str = "http://localhost:5000/api/") -> None:
    """客户端通过 _links 动态导航 API"""
    response = requests.get(entry_point)
    api_root = response.json()

    # 通过 _links 发现资源
    articles_url = api_root["_links"]["articles"]["href"]
    articles_resp = requests.get(articles_url)
    articles_data = articles_resp.json()

    # 遍历文章列表
    for article in articles_data["items"]:
        print(f"  {article['title']}")

    # 通过 _links 翻页
    next_url = articles_data["_links"]["next"]["href"]
    next_page = requests.get(next_url)
```

---

## 第七部分：API 版本控制策略

### 7.1 实际场景

API 升级后，旧客户端不能立即升级，需要同时维护 v1 和 v2。

**问题：API 版本控制有哪些策略？如何选择？**

### 7.2 三种版本控制策略对比

```
API 版本控制策略：
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  策略一：URL 路径版本（最常用）                               │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  /api/v1/users                                      │    │
│  │  /api/v2/users                                      │    │
│  │  优点：直观、浏览器可测试、CDN 缓存友好               │    │
│  │  缺点：URL 变化，REST 纯化论者认为不 RESTful          │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                             │
│  策略二：请求头版本（Accept Header）                         │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  Accept: application/vnd.myapp.v2+json               │    │
│  │  优点：URL 不变，RESTful 更"纯"                      │    │
│  │  缺点：调试不便，浏览器难测试                         │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                             │
│  策略三：查询参数版本                                       │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  /api/users?version=2                                │    │
│  │  优点：极简单                                         │    │
│  │  缺点：缓存键复杂，语义模糊                           │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 7.3 URL 路径版本 + 请求头版本的混合实现

```python
from flask import Blueprint, request, abort
from flask_restful import Api, Resource
from typing import Callable

def create_versioned_api(app: Flask) -> dict[str, Blueprint]:
    """创建多版本 API 蓝图"""

    api_v1 = Blueprint("api_v1", __name__, url_prefix="/api/v1")
    api_v2 = Blueprint("api_v2", __name__, url_prefix="/api/v2")

    # 注册
    app.register_blueprint(api_v1)
    app.register_blueprint(api_v2)

    return {"v1": api_v1, "v2": api_v2}


def versioned_route(version_map: dict[str, Callable]):
    """
    同一 URL 根据版本分发到不同处理器

    用法：
    @versioned_route({"v1": v1_handler, "v2": v2_handler})
    def handle():
        pass
    """
    def decorator(f: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            # 从请求中检测版本
            version = detect_api_version()
            handler = version_map.get(version)
            if handler is None:
                abort(400, f"Unsupported API version: {version}")
            return handler(*args, **kwargs)
        wrapper.__name__ = f.__name__
        return wrapper
    return decorator


def detect_api_version() -> str:
    """检测 API 版本：URL 优先，请求头次之"""
    # 方式一：URL 路径 /api/v1/...
    if "/v1/" in request.path:
        return "v1"
    if "/v2/" in request.path:
        return "v2"

    # 方式二：请求头 Accept: application/vnd.myapp.v2+json
    accept = request.headers.get("Accept", "")
    for v in ["v3", "v2", "v1"]:
        if f"vnd.myapp.{v}+json" in accept:
            return v

    # 默认
    return "v1"
```

### 7.4 版本兼容性与废弃策略

```python
# API 响应中添加弃用警告头
from functools import wraps
from datetime import datetime, timedelta

def deprecation_notice(sunset_date: str, alternative: str) -> Callable:
    """
    在响应头中标记 API 为废弃状态
    sunset_date: ISO 8601 格式的废弃日期
    alternative: 替代 API 的 endpoint
    """
    def decorator(f: Callable) -> Callable:
        @wraps(f)
        def wrapper(*args, **kwargs):
            response = f(*args, **kwargs)
            if isinstance(response, tuple):
                body, status_code, headers = response[0], response[1], {}
                if len(response) > 2:
                    headers = response[2]
            else:
                body, status_code, headers = response, 200, {}

            headers["Sunset"] = sunset_date
            headers["Deprecation"] = "true"
            headers["Link"] = f'<{url_for(alternative, _external=True)}>; rel="alternate"'

            return body, status_code, headers
        return wrapper
    return decorator
```

---

## 第八部分：请求/响应编组（Marshalling）模式

### 8.1 实际场景

同一个用户模型在不同场景下需要返回不同字段（列表页 vs 详情页 vs 公开页）。

**问题：如何灵活地在不同场景下返回不同的数据结构？**

### 8.2 场景化 Marshal 模式

```python
from flask_restful import fields, marshal_with, marshal
from typing import Any

# 用户模型：多种序列化方案
user_public_fields: dict[str, fields.Raw] = {
    "id": fields.Integer,
    "username": fields.String,
    "avatar_url": fields.String(attribute="avatar"),
}

user_private_fields: dict[str, fields.Raw] = {
    **user_public_fields,
    "email": fields.String,
    "created_at": fields.DateTime(dt_format="iso8601"),
}

user_admin_fields: dict[str, fields.Raw] = {
    **user_private_fields,
    "role": fields.String,
    "last_login": fields.DateTime(dt_format="iso8601"),
    "is_active": fields.Boolean,
}

# 部分响应：根据查询参数 ?fields=id,username,email 返回子集
def marshal_with_partial(field_map: dict[str, fields.Raw]):
    """根据 ?fields 参数返回子集字段"""
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            requested_fields = request.args.get("fields", "")
            if requested_fields:
                field_names = set(requested_fields.split(","))
                filtered = {
                    k: v for k, v in field_map.items()
                    if k in field_names
                }
            else:
                filtered = field_map
            result = f(*args, **kwargs)
            return marshal(result, filtered)
        return wrapper
    return decorator


class UserResource(Resource):
    def get(self, user_id: int) -> dict[str, Any]:
        user = User.query.get_or_404(user_id)
        requesting_user = get_request_user()

        # 根据请求者角色选择序列化方案
        if requesting_user.id == user.id:
            return marshal(user, user_private_fields)
        elif requesting_user.role == "admin":
            return marshal(user, user_admin_fields)
        else:
            return marshal(user, user_public_fields)
```

### 8.3 输入编组（Request Deserialization）

```python
from marshmallow import Schema, fields, validate, ValidationError
from flask import request

class ArticleSchema(Schema):
    """文章输入验证与反序列化"""
    title = fields.Str(required=True, validate=validate.Length(min=1, max=200))
    content = fields.Str(required=True, validate=validate.Length(min=1))
    category = fields.Str(
        validate=validate.OneOf(["tech", "life", "work"]),
        missing="tech"
    )
    tags = fields.List(fields.Str(), missing=[])
    published = fields.Bool(missing=False)
    scheduled_at = fields.DateTime(missing=None)

    class Meta:
        unknown = "RAISE"  # 拒绝未知字段


class ArticleOutputSchema(Schema):
    """文章输出序列化"""
    id = fields.Int(dump_only=True)
    title = fields.Str()
    content = fields.Str()
    category = fields.Str()
    tags = fields.List(fields.Str())
    published = fields.Bool()
    created_at = fields.DateTime(dump_only=True)


class ArticleCreateResource(Resource):
    def post(self) -> tuple[dict[str, Any], int]:
        schema = ArticleSchema()

        try:
            data = schema.load(request.get_json() or {})
        except ValidationError as e:
            return {"errors": e.messages}, 400

        article = Article(
            title=data["title"],
            content=data["content"],
            category=data["category"],
            tags=data["tags"],
            published=data["published"],
        )
        db.session.add(article)
        db.session.commit()

        return ArticleOutputSchema().dump(article), 201
```

---

## 第九部分：分页与游标导航

### 9.1 实际场景

文章列表有 100 万条，传统的 OFFSET/LIMIT 分页性能差。

**问题：如何实现高性能的游标分页？**

### 9.2 偏移分页 vs 游标分页

```
偏移分页（OFFSET/LIMIT）：
┌─────────────────────────────────────────────────────────────┐
│  SELECT * FROM articles ORDER BY id LIMIT 20 OFFSET 500000  │
│                                                             │
│  问题：数据库需要扫描前 500,000 行再跳过                     │
│  偏移越大越慢，并发写入时导致重复或跳行                       │
└─────────────────────────────────────────────────────────────┘

游标分页（Cursor-based）：
┌─────────────────────────────────────────────────────────────┐
│  SELECT * FROM articles WHERE id > 500000 ORDER BY id       │
│                            LIMIT 20                         │
│                                                             │
│  优点：利用 B+Tree 索引，O(log N) 定位，不受偏移影响         │
│  缺点：无法直接跳转到第 N 页                                 │
└─────────────────────────────────────────────────────────────┘
```

### 9.3 游标分页实现

```python
import base64
from flask import request, url_for
from flask_restful import Resource
from typing import Any

class CursorPaginator:
    """基于游标的分页器"""

    def __init__(self, query, per_page: int = 20,
                 cursor_field: str = "id", order: str = "asc") -> None:
        self.query = query
        self.per_page = per_page
        self.cursor_field = cursor_field
        self.order = order

    def paginate(self, cursor: str | None = None) -> dict[str, Any]:
        """执行游标分页查询"""
        query = self.query

        if cursor:
            try:
                cursor_value = int(base64.b64decode(cursor).decode())
                if self.order == "asc":
                    query = query.filter(
                        getattr(self.query.column_descriptions[0]["entity"],
                                self.cursor_field) > cursor_value
                    )
                else:
                    query = query.filter(
                        getattr(self.query.column_descriptions[0]["entity"],
                                self.cursor_field) < cursor_value
                    )
            except (ValueError, UnicodeDecodeError):
                pass

        items = query.order_by(
            getattr(self.query.column_descriptions[0]["entity"],
                    self.cursor_field).asc()
            if self.order == "asc" else
            getattr(self.query.column_descriptions[0]["entity"],
                    self.cursor_field).desc()
        ).limit(self.per_page + 1).all()

        has_next = len(items) > self.per_page
        if has_next:
            items = items[:self.per_page]

        return {
            "items": items,
            "has_next": has_next,
            "next_cursor": self._encode_cursor(items[-1]) if has_next else None,
            "per_page": self.per_page,
        }

    def _encode_cursor(self, item) -> str:
        value = getattr(item, self.cursor_field)
        return base64.b64encode(str(value).encode()).decode()


class ArticleListResource(Resource):
    def get(self) -> dict[str, Any]:
        cursor = request.args.get("cursor")
        query = Article.query.filter_by(published=True)

        paginator = CursorPaginator(query, per_page=20)
        result = paginator.paginate(cursor)

        return {
            "data": [article.to_dict() for article in result["items"]],
            "pagination": {
                "has_next": result["has_next"],
                "next_cursor": result["next_cursor"],
                "next_url": (
                    url_for("api.article_list", cursor=result["next_cursor"],
                            _external=True)
                    if result["next_cursor"] else None
                ),
            }
        }
```

---

## 第十部分：Rate Limiting（速率限制）

### 10.1 实际场景

公开 API 需要防止滥用，不同用户/角色有不同的配额。

**问题：如何实现多级速率限制？**

### 10.2 基于用户/角色的分层次限流

```python
import time
from functools import wraps
from flask import request, jsonify, g
import redis

r = redis.from_url("redis://localhost:6379")

RATE_LIMITS = {
    "anonymous": {"requests": 10, "window": 60},    # 匿名 10次/分
    "user":      {"requests": 100, "window": 60},   # 用户 100次/分
    "premium":   {"requests": 1000, "window": 60},  # 高级 1000次/分
}

def tiered_rate_limit():
    """
    根据用户角色应用不同的速率限制
    使用 Redis Sorted Set 实现滑动窗口
    """
    def decorator(f: Callable) -> Callable:
        @wraps(f)
        def wrapper(*args, **kwargs):
            user_tier = getattr(g, "user_tier", "anonymous")
            limit_config = RATE_LIMITS.get(user_tier, RATE_LIMITS["anonymous"])

            key = f"rate:{user_tier}:{request.remote_addr}"
            now = int(time.time())
            window_start = now - limit_config["window"]

            # 滑动窗口：清理过期记录并计数
            pipe = r.pipeline()
            pipe.zremrangebyscore(key, 0, window_start)
            pipe.zadd(key, {str(now): now})
            pipe.zcard(key)
            pipe.expire(key, limit_config["window"] + 1)
            _, _, current_count, _ = pipe.execute()

            remaining = limit_config["requests"] - current_count

            response = f(*args, **kwargs)

            if isinstance(response, tuple):
                body, status = response[0], response[1]
                headers = response[2] if len(response) > 2 else {}
            else:
                body, status, headers = response, 200, {}

            # 标准限流响应头
            headers.update({
                "X-RateLimit-Limit": str(limit_config["requests"]),
                "X-RateLimit-Remaining": str(max(0, remaining)),
                "X-RateLimit-Reset": str(window_start + limit_config["window"]),
            })

            if current_count > limit_config["requests"]:
                return jsonify({
                    "error": "Rate limit exceeded",
                    "retry_after": limit_config["window"]
                }), 429, headers

            return body, status, headers
        return wrapper
    return decorator


class ArticleListResource(Resource):
    @tiered_rate_limit()
    def get(self):
        return {"articles": []}
```

---

## 第十一部分：API 文档与 OpenAPI

### 11.1 实际场景

API 需要有标准化的文档供前端开发者和第三方使用。

**问题：如何自动生成 OpenAPI 文档？**

### 11.2 Flask-RESTX 自动文档

```python
# pip install flask-restx
from flask_restx import Api, Resource, Namespace, fields as restx_fields

app: Flask = Flask(__name__)
api: Api = Api(
    app,
    version="1.0",
    title="Blog API",
    description="博客系统 RESTful API 文档",
    doc="/docs",  # Swagger UI 地址
)

ns = api.namespace("articles", description="文章操作")

article_model = api.model("Article", {
    "id": restx_fields.Integer(readonly=True, description="文章 ID"),
    "title": restx_fields.String(
        required=True,
        description="文章标题",
        min_length=1,
        max_length=200,
    ),
    "content": restx_fields.String(required=True, description="文章内容"),
    "category": restx_fields.String(
        enum=["tech", "life", "work"],
        description="分类",
    ),
    "tags": restx_fields.List(
        restx_fields.String,
        description="标签列表",
    ),
    "published": restx_fields.Boolean(
        default=False,
        description="是否发布",
    ),
    "created_at": restx_fields.DateTime(
        readonly=True,
        description="创建时间",
    ),
})

@ns.route("/")
class ArticleList(Resource):
    @ns.marshal_list_with(article_model)
    @ns.param("page", "页码", type=int, default=1)
    @ns.param("per_page", "每页数量", type=int, default=20)
    def get(self):
        """获取文章列表（分页）"""
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 20, type=int)
        return Article.query.paginate(page=page, per_page=per_page).items

    @ns.expect(article_model)
    @ns.marshal_with(article_model, code=201)
    @ns.response(400, "参数验证失败")
    def post(self):
        """创建新文章"""
        data = request.get_json()
        article = Article(**data)
        db.session.add(article)
        db.session.commit()
        return article, 201


@ns.route("/<int:article_id>")
@ns.param("article_id", "文章 ID")
class ArticleDetail(Resource):
    @ns.marshal_with(article_model)
    @ns.response(404, "文章不存在")
    def get(self, article_id: int):
        """获取文章详情"""
        return Article.query.get_or_404(article_id)
```

---

## 第十二部分：Content Negotiation（内容协商）

### 12.1 实际场景

同一个 API 需要支持 JSON、XML、YAML 多种格式。

**问题：如何根据客户端请求头返回不同格式的响应？**

### 12.2 多格式响应实现

```python
from flask import request, Response
import json
import xmltodict
import yaml

MIME_TYPES = {
    "application/json": "json",
    "application/xml": "xml",
    "text/xml": "xml",
    "application/x-yaml": "yaml",
    "text/yaml": "yaml",
}

def negotiate_response(data: dict, status_code: int = 200) -> Response:
    """根据 Accept 头返回对应格式的响应"""
    accept = request.headers.get("Accept", "application/json")

    best_mime = request.accept_mimetypes.best_match(MIME_TYPES.keys())
    fmt = MIME_TYPES.get(best_mime, "json")

    if fmt == "xml":
        body = xmltodict.unparse({"root": data}, pretty=True)
        mime = "application/xml"
    elif fmt == "yaml":
        body = yaml.dump(data, allow_unicode=True, default_flow_style=False)
        mime = "application/x-yaml"
    else:
        body = json.dumps(data, ensure_ascii=False, indent=2)
        mime = "application/json"

    return Response(body, status=status_code, mimetype=mime)


class FlexibleArticleResource(Resource):
    def get(self, article_id: int) -> Response:
        article = Article.query.get_or_404(article_id)
        return negotiate_response(article.to_dict())
```

### 12.3 全局内容协商装饰器

```python
def content_negotiation():
    """自动将 dict 返回值转换为请求头协商的格式"""
    def decorator(f: Callable) -> Callable:
        @wraps(f)
        def wrapper(*args, **kwargs):
            result = f(*args, **kwargs)

            if isinstance(result, Response):
                return result

            status_code = 200
            if isinstance(result, tuple):
                data, status_code = result[0], result[1]
            else:
                data = result

            if isinstance(data, dict):
                return negotiate_response(data, status_code)

            return result

        return wrapper
    return decorator
```

---

## 第十三部分：常见坑点排查

### 13.1 PUT vs PATCH 误用

**错误信息：**

```
（通常无错误，但语义不正确）
PUT 只更新了 title，期望 content 保持不变，但 content 被清空为 null。
```

**根因分析：**

PUT 语义是"完整替换"，应该将未提供的字段设为默认值或清空。如果只想更新部分字段，应使用 PATCH。

```python
# ❌ 误解：把 PUT 当 PATCH 用
class ArticleResource(Resource):
    def put(self, article_id: int):
        data = request.get_json()
        article = Article.query.get(article_id)
        article.title = data.get("title", article.title)  # 保留原值
        article.content = data.get("content", article.content)
        # 这其实是 PATCH 语义！

# ✅ 正确区分 PUT（完整替换）和 PATCH（部分更新）
class ArticleResource(Resource):
    def put(self, article_id: int):
        """完整替换：未提供的字段应重置为默认值"""
        data = request.get_json()
        article = Article.query.get(article_id)
        article.title = data.get("title", "")
        article.content = data.get("content", "")

    def patch(self, article_id: int):
        """部分更新：只更新提供的字段"""
        data = request.get_json()
        article = Article.query.get(article_id)
        if "title" in data:
            article.title = data["title"]
        if "content" in data:
            article.content = data["content"]
```

### 13.2 分页数据不一致

**错误信息：**

```
（随机出现）分页时，第 2 页出现了第 1 页已经出现过的数据。
```

**根因分析：**

OFFSET 分页在数据并发写入时，插入新数据会导致已有数据位置偏移。

```
修复方案：
1. 对静态数据（历史记录、日志）使用 OFFSET 分页
2. 对动态数据（新增频繁）使用游标分页
3. 添加一致性标记：请求带上 `after=<timestamp>` 参数
```

### 13.3 问题排查表

| 现象 | 可能原因 | 检查方法 | 解决方案 |
|------|---------|---------|---------|
| 200 OK 但没有数据 | GET 请求带了 body | 检查请求方式 | GET 不应带 body |
| 415 Unsupported Media Type | Content-Type 错误 | 检查请求头 | POST 时设置 `Content-Type: application/json` |
| 400 Bad Request | reqparse 参数不匹配 | 查看 `parser.errors` | 匹配参数名、类型、location |
| 500 Internal Error | 未捕获异常导致 500 | 添加错误日志 | 统一错误处理装饰器 |
| 分页数据重复/缺失 | OFFSET 并发修改 | 观察数据变化 | 改用游标分页 |
| API 文档不一致 | 文档手动维护 | 对比代码和文档 | 使用 Flask-RESTX 自动生成 |

---

## 第十四部分：调试与排错实战

### 14.1 调试会话：reqparse 参数验证静默失败

```
场景：POST /api/articles 带 JSON body，但 title 始终为 None。

调试步骤：

Step 1: 检查请求
import json
# 在视图函数中打印原始请求
@app.before_request
def debug_request():
    if request.path.startswith("/api"):
        print(f"[API DEBUG] {request.method} {request.path}")
        print(f"  Content-Type: {request.content_type}")
        print(f"  Body: {request.get_data(as_text=True)}")

Step 2: 输出
[API DEBUG] POST /api/articles
  Content-Type: application/json; charset=utf-8
  Body: {"title": "Hello", "content": "World"}

Step 3: 检查 reqparse 配置
parser = reqparse.RequestParser()
parser.add_argument("title", type=str, required=True,
                    location="json")  ← 明确指定 location

args = parser.parse_args()
print(f"Parsed args: {args}")

# 如果 Content-Type 不是 application/json 或含有 charset，
# location="json" 可能无法正确解析。

Step 4: 修复 — 同时接受多种 location
parser.add_argument("title", type=str, required=True,
                    location=["json", "form"])  # fallback
```

### 14.2 HTTP 状态码调试工具

```python
# 在应用启动时验证所有资源的状态码
def validate_api_status_codes(app: Flask) -> None:
    """检查 API 端点是否返回正确的状态码"""
    with app.test_client() as client:

        # 检查 GET 正常场景
        resp = client.get("/api/articles/1")
        assert resp.status_code in (200, 404), (
            f"Unexpected status: {resp.status_code}"
        )

        # 检查 POST 无 body
        resp = client.post("/api/articles",
                          content_type="application/json")
        assert resp.status_code in (400, 415, 422), (
            f"POST without body should return error: {resp.status_code}"
        )

        print("API status code validation: PASSED")
```

