# RESTful API 开发

## Flask-RESTful 简介

Flask-RESTful 是一个用于构建 REST API 的 Flask 扩展，提供了资源类、请求解析等工具。

**安装：**

```bash
uv add flask-restful
```

**基本用法：**

```python
from flask import Flask
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)


class HelloWorld(Resource):
    def get(self):
        return {'message': 'Hello World'}

    def post(self):
        data = request.get_json()
        return {'received': data}, 201


# 注册资源
api.add_resource(HelloWorld, '/hello')
```

---

## 资源类（Resource）

资源类将 HTTP 方法映射到类方法，每个方法对应一种 HTTP 操作。

**完整示例：文章 API**

```python
from flask_restful import Resource, request, abort

articles_db = {}  # 模拟数据库
next_id = 1


class ArticleList(Resource):
    """文章列表资源"""

    def get(self):
        """获取所有文章"""
        return {'articles': list(articles_db.values())}, 200

    def post(self):
        """创建新文章"""
        data = request.get_json()

        if not data or 'title' not in data:
            abort(400, message='标题是必需的')

        global next_id
        article = {
            'id': next_id,
            'title': data['title'],
            'content': data.get('content', '')
        }
        articles_db[next_id] = article
        next_id += 1

        return article, 201


class ArticleResource(Resource):
    """单篇文章资源"""

    def get(self, article_id):
        """获取单篇文章"""
        article = articles_db.get(article_id)
        if not article:
            abort(404, message='文章不存在')
        return article, 200

    def put(self, article_id):
        """更新文章（完整更新）"""
        article = articles_db.get(article_id)
        if not article:
            abort(404, message='文章不存在')

        data = request.get_json()
        article['title'] = data.get('title', article['title'])
        article['content'] = data.get('content', article['content'])

        return article, 200

    def delete(self, article_id):
        """删除文章"""
        if article_id not in articles_db:
            abort(404, message='文章不存在')

        del articles_db[article_id]
        return '', 204


# 注册资源
api.add_resource(ArticleList, '/api/articles')
api.add_resource(ArticleResource, '/api/articles/<int:article_id>')
```

---

## 请求解析（reqparse）

`reqparse` 用于解析和验证请求数据，类似于 argparse 但用于 HTTP 请求。

**示例代码：**

```python
from flask_restful import reqparse

# 创建解析器
parser = reqparse.RequestParser()
parser.add_argument(
    'title',
    type=str,
    required=True,
    help='标题是必需的',
    location='json'
)
parser.add_argument(
    'content',
    type=str,
    required=False,
    default='',
    help='文章内容',
    location='json'
)
parser.add_argument(
    'category',
    type=str,
    choices=['tech', 'life', 'work'],  # 限制选项
    required=False,
    location='json'
)
parser.add_argument(
    'tags',
    type=list,
    action='append',  # 允许多个值
    location='json'
)


class ArticleCreate(Resource):
    def post(self):
        args = parser.parse_args()

        article = {
            'title': args['title'],
            'content': args['content'],
            'category': args.get('category'),
            'tags': args.get('tags', [])
        }

        return article, 201
```

**location 参数选项：**

```python
# 从不同位置获取参数
parser.add_argument('name', location='args')      # 查询参数 ?name=xxx
parser.add_argument('data', location='json')      # JSON 请求体
parser.add_argument('file', location='files')     # 上传文件
parser.add_argument('token', location='headers')  # 请求头
parser.add_argument('id', location='form')        # 表单数据
```

---

## 字段序列化

使用 `fields` 模块可以控制响应数据的格式和结构。

**示例代码：**

```python
from flask_restful import fields, marshal_with

# 定义字段
article_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'content': fields.String,
    'created_at': fields.DateTime,
}

# 嵌套字段
author_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'email': fields.String,
}

article_with_author = {
    'id': fields.Integer,
    'title': fields.String,
    'author': fields.Nested(author_fields),
}


class ArticleAPI(Resource):
    @marshal_with(article_fields)
    def get(self, article_id):
        article = Article.query.get_or_404(article_id)
        return article  # 自动序列化为指定格式
```

---

## API 版本控制

使用蓝图实现 API 版本隔离，支持多版本并存。

**项目结构：**

```
app/
├── api_v1/
│   ├── __init__.py
│   └── routes.py
├── api_v2/
│   ├── __init__.py
│   └── routes.py
└── app.py
```

**实现代码：**

```python
# app.py
from flask import Flask, Blueprint
from flask_restful import Api

app = Flask(__name__)

# 创建版本蓝图
api_v1 = Blueprint('api_v1', __name__, url_prefix='/api/v1')
api_v2 = Blueprint('api_v2', __name__, url_prefix='/api/v2')

api_v1_api = Api(api_v1)
api_v2_api = Api(api_v2)


# v1 API 路由
class ArticleListV1(Resource):
    def get(self):
        return {'version': 'v1', 'articles': []}


api_v1_api.add_resource(ArticleListV1, '/articles')


# v2 API 路由（新功能）
class ArticleListV2(Resource):
    def get(self):
        # v2 支持更多过滤选项
        return {
            'version': 'v2',
            'articles': [],
            'filters': ['author', 'category', 'tag']
        }


api_v2_api.add_resource(ArticleListV2, '/articles')

# 注册蓝图
app.register_blueprint(api_v1)
app.register_blueprint(api_v2)
```