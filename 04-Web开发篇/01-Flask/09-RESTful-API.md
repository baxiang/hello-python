# RESTful API 开发（详细版）

> Python 3.11+

本章讲解 Flask-RESTful 扩展构建 REST API。

---

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

## 总结

| 知识点 | 说明 |
|---------|------|
| Resource | 资源类 |
| HTTP 方法 | GET, POST, PUT, DELETE |
| reqparse | 请求参数解析 |
| fields | 响应字段序列化 |
| 版本控制 | Blueprint 实现 |