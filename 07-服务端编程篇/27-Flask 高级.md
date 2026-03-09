# 第 27 章 - Flask 高级（详细版）

本章讲解 Flask 的高级主题，包括 RESTful API 开发、认证授权、文件处理、缓存、异步任务和测试部署。

---

## 第一部分：RESTful API 开发

### 27.1 Flask-RESTful 简介

#### 概念说明

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

### 27.2 资源类（Resource）

#### 概念说明

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

### 27.3 请求解析（reqparse）

#### 概念说明

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

### 27.4 字段序列化

#### 概念说明

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

# 格式化字段
formatted_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'content': fields.String,
    'formatted_date': fields.DateTime(dt_format='rfc822'),
    'url': fields.Url('api.article_detail'),  # 生成 URL
}


class ArticleAPI(Resource):
    @marshal_with(article_fields)
    def get(self, article_id):
        article = Article.query.get_or_404(article_id)
        return article  # 自动序列化为指定格式
```

---

### 27.5 API 版本控制

#### 概念说明

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

---

## 第二部分：认证与授权

### 27.6 HTTP Basic Auth

#### 概念说明

HTTP Basic Auth 是最简单的认证方式，用户名和密码使用 Base64 编码后放在 Authorization 头中。

**实现代码：**

```python
from flask import Flask, request
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
auth = HTTPBasicAuth()

# 用户数据库
users = {
    'admin': generate_password_hash('admin123'),
    'user': generate_password_hash('user123')
}


@auth.verify_password
def verify_password(username, password):
    """验证用户名和密码"""
    if username in users and check_password_hash(users[username], password):
        return username
    return None


@auth.error_handler
def auth_error(status):
    """自定义认证错误响应"""
    return {'error': '认证失败'}, status


@app.route('/api/protected')
@auth.login_required
def protected():
    """需要认证的接口"""
    return {'message': f'欢迎，{auth.current_user()}!'}


# 公开接口
@app.route('/api/public')
def public():
    return {'message': '这是公开接口'}
```

**测试：**

```bash
# 使用 curl 测试
curl -u admin:admin123 http://localhost:5000/api/protected

# 无认证访问
curl http://localhost:5000/api/protected
# 返回 401
```

---

### 27.7 JWT Token 认证

#### 概念说明

JWT（JSON Web Token）是一种无状态认证方案，适合 API 和微服务。

**安装：**

```bash
uv add pyjwt python-dotenv
```

**完整实现：**

```python
# extensions.py
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta

jwt = JWTManager()


def init_jwt(app):
    app.config['JWT_SECRET_KEY'] = 'your-secret-key'
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)
    jwt.init_app(app)
```

```python
# routes/auth.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt
)

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')


@auth_bp.route('/register', methods=['POST'])
def register():
    """用户注册"""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # 检查用户是否已存在
    if User.query.filter_by(username=username).first():
        return {'error': '用户名已存在'}, 400

    # 创建用户
    user = User(username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    return {'message': '注册成功'}, 201


@auth_bp.route('/login', methods=['POST'])
def login():
    """用户登录"""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()

    if not user or not user.check_password(password):
        return {'error': '用户名或密码错误'}, 401

    # 创建 Token
    additional_claims = {'role': user.role}
    access_token = create_access_token(
        identity=user.id,
        additional_claims=additional_claims
    )
    refresh_token = create_refresh_token(identity=user.id)

    return {
        'access_token': access_token,
        'refresh_token': refresh_token,
        'user': {
            'id': user.id,
            'username': user.username
        }
    }, 200


@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """刷新 Access Token"""
    current_user = get_jwt_identity()
    new_token = create_access_token(identity=current_user)
    return {'access_token': new_token}, 200


@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """用户登出（客户端删除 Token）"""
    # 实际应用中可以将 Token 加入黑名单
    return {'message': '已登出'}, 200
```

**受保护的路由：**

```python
from flask_jwt_extended import jwt_required, get_jwt_identity


@app.route('/api/profile')
@jwt_required()
def get_profile():
    """获取当前用户资料"""
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    return {
        'id': user.id,
        'username': user.username,
        'email': user.email
    }


# 基于角色的权限控制
def admin_required(f):
    """管理员权限装饰器"""
    @wraps(f)
    @jwt_required()
    def decorated_function(*args, **kwargs):
        claims = get_jwt()
        if claims.get('role') != 'admin':
            return {'error': '需要管理员权限'}, 403
        return f(*args, **kwargs)
    return decorated_function


@app.route('/api/admin/users')
@admin_required
def list_users():
    """管理员接口：列出所有用户"""
    users = User.query.all()
    return {'users': [{'id': u.id, 'username': u.username} for u in users]}
```

---

### 27.8 权限控制（RBAC）

#### 概念说明

基于角色的访问控制（RBAC）根据用户角色限制资源访问。

**模型设计：**

```python
# 角色 - 权限关联表
role_permissions = db.Table('role_permissions',
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id')),
    db.Column('permission_id', db.Integer, db.ForeignKey('permissions.id'))
)

# 用户 - 角色关联表
user_roles = db.Table('user_roles',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id'))
)


class Permission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)  # 如 'read', 'write', 'admin'


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)  # 如 'user', 'admin'
    permissions = db.relationship('Permission', secondary=role_permissions)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    roles = db.relationship('Role', secondary=user_roles)

    def has_permission(self, permission_name):
        """检查用户是否有指定权限"""
        for role in self.roles:
            for perm in role.permissions:
                if perm.name == permission_name:
                    return True
        return False
```

**权限装饰器：**

```python
from functools import wraps
from flask_jwt_extended import get_jwt_identity


def permission_required(permission_name):
    """权限检查装饰器"""
    def decorator(f):
        @wraps(f)
        @jwt_required()
        def wrapped(*args, **kwargs):
            user_id = get_jwt_identity()
            user = User.query.get(user_id)

            if not user or not user.has_permission(permission_name):
                return {'error': f'需要 {permission_name} 权限'}, 403

            return f(*args, **kwargs)
        return wrapped
    return decorator


# 使用示例
@app.route('/api/articles', methods=['POST'])
@permission_required('write')
def create_article():
    """需要 write 权限"""
    ...


@app.route('/api/admin', methods=['GET'])
@permission_required('admin')
def admin_panel():
    """需要 admin 权限"""
    ...
```

---

## 第三部分：文件处理

### 27.9 文件上传

#### 概念说明

Flask 处理文件上传需要使用 `request.files` 和 `SecureFilename`。

**示例代码：**

```python
import os
from werkzeug.utils import secure_filename
from flask import Flask, request, jsonify

app = Flask(__name__)

# 配置
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH


def allowed_file(filename):
    """检查文件扩展名是否允许"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/api/upload', methods=['POST'])
def upload_file():
    """单文件上传"""
    if 'file' not in request.files:
        return {'error': '没有文件'}, 400

    file = request.files['file']

    if file.filename == '':
        return {'error': '未选择文件'}, 400

    if not allowed_file(file.filename):
        return {'error': '不支持的文件类型'}, 400

    # 安全文件名
    filename = secure_filename(file.filename)

    # 保存文件
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    return {
        'message': '上传成功',
        'filename': filename,
        'path': filepath
    }, 201
```

**多文件上传：**

```python
@app.route('/api/upload/multiple', methods=['POST'])
def upload_multiple():
    """多文件上传"""
    files = request.files.getlist('files')

    uploaded = []
    errors = []

    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            uploaded.append(filename)
        else:
            errors.append(file.filename)

    return {
        'uploaded': uploaded,
        'errors': errors
    }
```

---

### 27.10 文件下载

#### 概念说明

使用 `send_file()` 和 `send_from_directory()` 提供文件下载。

```python
from flask import send_file, send_from_directory
import os


@app.route('/api/files/<filename>')
def download_file(filename):
    """文件下载"""
    # 安全文件名
    safe_filename = secure_filename(filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], safe_filename)

    if not os.path.exists(filepath):
        return {'error': '文件不存在'}, 404

    return send_file(
        filepath,
        as_attachment=True,  # 作为附件下载
        download_name=safe_filename  # 下载文件名
    )


@app.route('/api/static/<path:filename>')
def serve_static(filename):
    """从目录提供文件"""
    directory = app.config['UPLOAD_FOLDER']
    return send_from_directory(directory, filename)
```

---

## 第四部分：缓存

### 27.11 Flask-Caching

#### 概念说明

Flask-Caching 提供了多种缓存后端，可以缓存视图结果或任意数据。

**安装与配置：**

```bash
uv add flask-caching redis
```

```python
from flask import Flask
from flask_caching import Cache

app = Flask(__name__)

# 配置缓存后端
app.config['CACHE_TYPE'] = 'redis'
app.config['CACHE_REDIS_HOST'] = 'localhost'
app.config['CACHE_REDIS_PORT'] = 6379
app.config['CACHE_REDIS_DB'] = 0

cache = Cache(app)
```

**缓存后端选项：**

| 类型 | 配置 | 说明 |
|------|------|------|
| `simple` | 默认 | 内存缓存，单进程 |
| `redis` | `CACHE_REDIS_HOST` | Redis，生产推荐 |
| `memcached` | `CACHE_MEMCACHED_SERVERS` | Memcached |
| `filesystem` | `CACHE_DIR` | 文件系统 |
| `null` | - | 无缓存（用于禁用） |

---

### 27.12 视图缓存

#### 概念说明

使用 `@cache.cached` 装饰器缓存整个视图的响应。

```python
from flask_caching import cached


# 缓存视图 5 分钟
@app.route('/api/articles')
@cached(timeout=300)
def get_articles():
    # 模拟耗时操作
    articles = Article.query.all()
    return {'articles': [a.to_dict() for a in articles]}


# 带参数的缓存
@app.route('/api/articles/<int:article_id>')
@cached(timeout=600)
def get_article(article_id):
    article = Article.query.get_or_404(article_id)
    return article.to_dict()


# 自定义缓存键
@app.route('/api/user/<int:user_id>')
@cached(timeout=300, key_prefix='user_data')
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return user.to_dict()
```

---

### 27.13 数据缓存

#### 概念说明

使用 `cache.get()` 和 `cache.set()` 手动缓存任意数据。

```python
from flask_caching import Cache

cache = Cache()


def get_expensive_data():
    """缓存计算结果"""
    # 尝试从缓存获取
    data = cache.get('expensive_data')

    if data is None:
        # 缓存未命中，执行耗时操作
        data = compute_expensive_data()
        # 存入缓存，10 分钟过期
        cache.set('expensive_data', data, timeout=600)

    return data


# 缓存删除
@app.route('/api/cache/clear', methods=['POST'])
def clear_cache():
    cache.clear()
    return {'message': '缓存已清除'}
```

---

## 第五部分：异步任务

### 27.14 Celery 集成

#### 概念说明

Celery 是一个分布式任务队列，用于处理耗时任务，如发送邮件、处理图片等。

**安装：**

```bash
uv add celery redis
```

**项目结构：**

```
app/
├── celery_app.py      # Celery 配置
├── tasks.py           # 任务定义
└── routes.py          # 视图路由
```

**Celery 配置：**

```python
# celery_app.py
from celery import Celery
from flask import Flask


def make_celery(app):
    celery = Celery(
        app.import_name,
        broker=app.config['CELERY_BROKER_URL'],
        backend=app.config['CELERY_RESULT_BACKEND']
    )

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery
```

**任务定义：**

```python
# tasks.py
from celery import current_task
from celery.signals import after_task_publish
import time


@celery.task
def send_email(to, subject, body):
    """发送邮件任务"""
    time.sleep(2)  # 模拟发送延迟
    # 实际使用 smtplib 或邮件服务 API
    print(f"发送邮件到 {to}: {subject}")
    return True


@celery.task
def process_image(image_path):
    """处理图片任务"""
    # 调整大小、添加水印等
    time.sleep(5)
    return f"处理完成：{image_path}"


@celery.task(bind=True)
def long_running_task(self, data):
    """带进度追踪的长任务"""
    for i in range(10):
        time.sleep(1)
        # 更新任务状态
        self.update_state(state='PROGRESS', meta={'current': i + 1, 'total': 10})
    return '完成'
```

---

### 27.15 任务队列使用

#### 概念说明

在视图中异步执行任务，立即返回响应。

```python
from flask import Blueprint, request, jsonify
from .tasks import send_email, process_image

api_bp = Blueprint('api', __name__)


@api_bp.route('/api/send-email', methods=['POST'])
def queue_email():
    """异步发送邮件"""
    data = request.get_json()

    # 异步执行，立即返回
    task = send_email.delay(
        to=data['to'],
        subject=data['subject'],
        body=data['body']
    )

    return {
        'message': '邮件已加入队列',
        'task_id': task.id
    }, 202


@api_bp.route('/api/task-status/<task_id>')
def task_status(task_id):
    """查询任务状态"""
    from celery.result import AsyncResult

    task = AsyncResult(task_id)

    if task.state == 'PENDING':
        response = {'state': task.state, 'status': '任务等待执行'}
    elif task.state == 'PROGRESS':
        response = {
            'state': task.state,
            'progress': task.info.get('current', 0),
            'total': task.info.get('total', 0)
        }
    elif task.state == 'SUCCESS':
        response = {'state': task.state, 'result': task.result}
    else:
        response = {'state': task.state, 'status': str(task.info)}

    status_code = 200 if task.state == 'SUCCESS' else 202
    return jsonify(response), status_code
```

---

## 第六部分：测试与部署

### 27.16 Flask 测试客户端

#### 概念说明

Flask 提供了测试客户端，可以在不启动服务器的情况下测试应用。

**基本测试：**

```python
# tests/test_app.py
import pytest
from app import create_app


@pytest.fixture
def app():
    """创建测试应用"""
    app = create_app('testing')
    app.config['TESTING'] = True
    with app.app_context():
        yield app


@pytest.fixture
def client(app):
    """创建测试客户端"""
    return app.test_client()


def test_hello_world(client):
    """测试首页"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Hello' in response.data


def test_create_article(client):
    """测试创建文章"""
    response = client.post(
        '/api/articles',
        json={'title': '测试文章', 'content': '内容'},
        content_type='application/json'
    )
    assert response.status_code == 201
    data = response.get_json()
    assert data['title'] == '测试文章'
```

---

### 27.17 Gunicorn + Nginx 部署

#### 概念说明

生产环境使用 Gunicorn 作为 WSGI 服务器，Nginx 作为反向代理。

**Gunicorn 安装与配置：**

```bash
uv add gunicorn
```

**启动命令：**

```bash
# 基本启动
gunicorn -w 4 -b 0.0.0.0:8000 app:app

# 生产配置
gunicorn \
    --workers 4 \
    --bind 0.0.0.0:8000 \
    --worker-class sync \
    --timeout 120 \
    --access-logfile /var/log/gunicorn/access.log \
    --error-logfile /var/log/gunicorn/error.log \
    app:app
```

**Nginx 配置：**

```nginx
server {
    listen 80;
    server_name example.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /path/to/static;
        expires 30d;
    }
}
```

---

## 本章小结

```
┌─────────────────────────────────────────────────────────────┐
│                      第 27 章 知识要点                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   RESTful API:                                               │
│   ✓ Flask-RESTful：Resource 类、reqparse 解析器               │
│   ✓ 字段序列化：fields、marshal_with                        │
│   ✓ 版本控制：蓝图隔离 v1/v2                                │
│                                                             │
│   认证授权：                                                 │
│   ✓ HTTP Basic Auth：flask-httpauth                         │
│   ✓ JWT Token：flask-jwt-extended、access/refresh token     │
│   ✓ RBAC：角色 - 权限模型、权限装饰器                        │
│                                                             │
│   文件处理：                                                 │
│   ✓ 上传：request.files、secure_filename                    │
│   ✓ 下载：send_file()、send_from_directory()                │
│   ✓ 验证：扩展名检查、大小限制                              │
│                                                             │
│   缓存：                                                     │
│   ✓ Flask-Caching：Redis 后端、视图缓存、数据缓存            │
│   ✓ @cached 装饰器、cache.get/set/clear                      │
│                                                             │
│   异步任务：                                                 │
│   ✓ Celery：任务定义、Broker(Redis)                          │
│   ✓ 任务队列：delay()、AsyncResult、任务状态                 │
│                                                             │
│   测试部署：                                                 │
│   ✓ 测试客户端：test_client()、fixture                      │
│   ✓ Gunicorn：WSGI 服务器、生产配置                          │
│   ✓ Nginx：反向代理、静态文件                               │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

[上一章](./26-Flask 进阶.md) | [下一章](./28-FastAPI.md)
