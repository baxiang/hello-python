# Flask 路由详解

深入掌握 Flask 路由系统，包括路径参数、HTTP 方法、请求处理等。

---

## 1. 路由基础

### 1.1 什么是路由？

路由（Route）是 URL 路径与处理函数之间的映射关系。当用户访问某个 URL 时，Flask 会根据路由配置找到对应的处理函数来响应请求。

```python
from flask import Flask

app = Flask(__name__)

# 路由：/hello 路径映射到 hello 函数
@app.route('/hello')
def hello():
    return 'Hello, World!'
```

### 1.2 路由装饰器

`@app.route()` 是 Flask 的路由装饰器，用于注册路由。

```python
@app.route('/path')
def handler():
    return 'Response'
```

---

## 2. 路径参数

### 2.1 基本路径参数

```python
@app.route('/user/<username>')
def get_user(username):
    return f'User: {username}'

# 访问 /user/john 返回 "User: john"
```

### 2.2 类型转换器

Flask 支持多种路径参数类型：

| 转换器 | 说明 | 示例 |
|--------|------|------|
| `string` | 默认，匹配不含 `/` 的字符串 | `/user/<name>` |
| `int` | 匹配整数 | `/post/<int:post_id>` |
| `float` | 匹配浮点数 | `/price/<float:price>` |
| `path` | 匹配包含 `/` 的路径 | `/file/<path:filepath>` |
| `uuid` | 匹配 UUID 格式 | `/item/<uuid:item_id>` |

```python
# 整数参数
@app.route('/post/<int:post_id>')
def get_post(post_id):
    return f'Post ID: {post_id}, Type: {type(post_id).__name__}'
# 访问 /post/123 返回 "Post ID: 123, Type: int"

# 浮点数参数
@app.route('/price/<float:price>')
def get_price(price):
    return f'Price: {price}, Tax: {price * 0.1}'
# 访问 /price/99.9 返回 "Price: 99.9, Tax: 9.99"

# UUID 参数
@app.route('/item/<uuid:item_id>')
def get_item(item_id):
    return f'Item UUID: {item_id}'
# 访问 /item/550e8400-e29b-41d4-a716-446655440000

# 路径参数（包含斜杠）
@app.route('/file/<path:filepath>')
def get_file(filepath):
    return f'File path: {filepath}'
# 访问 /file/user/docs/readme.txt
```

### 2.3 路径参数验证

使用 `Path` 可以添加验证和元数据：

```python
from fastapi import FastAPI, Path

app = FastAPI()

# 路径参数验证
@app.get("/users/{user_id}")
async def read_user(
    user_id: int = Path(..., ge=1, le=100, description="用户ID")
):
    return {"user_id": user_id}
```

---

## 3. HTTP 方法

### 3.1 支持的方法

| 方法 | 说明 | 幂等性 |
|------|------|--------|
| GET | 获取资源 | ✓ |
| POST | 创建资源 | ✗ |
| PUT | 完整更新 | ✓ |
| PATCH | 部分更新 | ✗ |
| DELETE | 删除资源 | ✓ |
| HEAD | 获取头部 | ✓ |
| OPTIONS | 获取选项 | ✓ |

### 3.2 基本用法

```python
# 单个方法
@app.route('/resource', methods=['GET'])
def get_resource():
    return {'data': 'GET'}

# 多个方法
@app.route('/resource', methods=['GET', 'POST'])
def handle_resource():
    if request.method == 'GET':
        return {'data': 'GET'}
    return {'data': 'POST'}
```

### 3.3 简写方法

Flask 提供了常用方法的简写装饰器：

```python
@app.get('/items')
def get_items():
    return {'items': []}

@app.post('/items')
def create_item():
    return {'message': 'Created'}, 201

@app.put('/items/<int:item_id>')
def update_item(item_id):
    return {'message': f'Updated {item_id}'}

@app.delete('/items/<int:item_id>')
def delete_item(item_id):
    return {'message': f'Deleted {item_id}'}

# HEAD 和 OPTIONS 自动支持
```

---

## 4. URL 构建

### 4.1 url_for 函数

`url_for()` 用于根据视图函数名生成 URL：

```python
from flask import url_for, Flask

app = Flask(__name__)

@app.route('/')
def index():
    return 'Index'

@app.route('/user/<int:user_id>')
def user_profile(user_id):
    return f'User {user_id}'

@app.route('/about')
def about():
    # 生成 URL
    index_url = url_for('index')
    user_url = url_for('user_profile', user_id=123)
    return f'Index: {index_url}, User: {user_url}'
# 输出: Index: /, User: /user/123
```

### 4.2 动态 URL 构建

```python
@app.route('/post/<slug>')
def post(slug):
    return f'Post: {slug}'

# 构建带参数的 URL
with app.test_request_context():
    url = url_for('post', slug='hello-world')
    print(url)  # /post/hello-world

# 构建带查询参数的 URL
with app.test_request_context():
    url = url_for('post', slug='hello', page=2)
    print(url)  # /post/hello?page=2
```

### 4.3 锚点和外部 URL

```python
@app.route('/docs')
def docs():
    # 带锚点
    url = url_for('docs', _anchor='authentication')
    return url  # /docs#authentication

# 外部 URL 需要配置 SERVER_NAME
app.config['SERVER_NAME'] = 'example.com'
with app.test_request_context():
    url = url_for('index', _external=True)
    print(url)  # http://example.com/
```

---

## 5. 请求对象

### 5.1 获取请求数据

```python
from flask import request

@app.route('/analyze-request')
def analyze_request():
    # 方法和路径
    method = request.method
    path = request.path
    url = request.url
    
    # 查询参数
    page = request.args.get('page', '1')
    limit = request.args.get('limit', '10')
    
    # 表单数据
    username = request.form.get('username')
    password = request.form.get('password')
    
    # JSON 数据
    json_data = request.get_json()
    
    # 请求头
    user_agent = request.headers.get('User-Agent')
    auth = request.headers.get('Authorization')
    
    # Cookie
    session_id = request.cookies.get('session_id')
    
    # 客户端信息
    ip = request.remote_addr
    host = request.host
    
    return {
        'method': method,
        'path': path,
        'page': page,
        'ip': ip
    }
```

### 5.2 请求钩子

请求钩子允许在请求处理的不同阶段执行代码：

```python
@app.before_request
def before_request():
    """每个请求之前执行"""
    print(f"Before: {request.path}")

@app.after_request
def after_request(response):
    """每个请求之后执行"""
    response.headers['X-Custom'] = 'Value'
    return response

@app.teardown_request
def teardown_request(exception):
    """请求结束时执行（即使有异常）"""
    print(f"Teardown: {exception}")

@app.teardown_appcontext
def teardown_appcontext(exception):
    """应用上下文结束时执行"""
    print("App context teardown")
```

---

## 6. 响应处理

### 6.1 返回响应

```python
from flask import Response, jsonify, make_response

# 字符串响应
@app.route('/text')
def text_response():
    return 'Plain text'

# JSON 响应
@app.route('/json')
def json_response():
    return jsonify({'message': 'Hello'})

# 自定义响应
@app.route('/custom')
def custom_response():
    response = make_response('Custom response')
    response.headers['X-Custom'] = 'Value'
    response.status_code = 201
    return response

# 元组形式
@app.route('/tuple')
def tuple_response():
    return {'data': 'tuple'}, 201, {'X-Custom': 'Value'}
```

### 6.2 特殊响应

```python
from flask import redirect, abort

# 重定向
@app.route('/old')
def old_url():
    return redirect('/new', code=302)

# 错误响应
@app.route('/error')
def error():
    abort(404)  # 抛出 404 错误
    # 或返回错误响应
    return 'Not Found', 404

# 文件响应
from flask import send_file, send_from_directory

@app.route('/download')
def download():
    return send_file('file.txt', as_attachment=True)

@app.route('/files/<path:filename>')
def serve_file(filename):
    return send_from_directory('files', filename)
```

---

## 7. 路由分组

### 7.1 蓝图基础

蓝图（Blueprint）用于组织大型应用的路由：

```python
from flask import Blueprint

# 创建蓝图
api = Blueprint('api', __name__, url_prefix='/api')

# 在蓝图中定义路由
@api.route('/users')
def get_users():
    return {'users': []}

@api.route('/posts')
def get_posts():
    return {'posts': []}

# 注册蓝图
app.register_blueprint(api)
# 访问: /api/users, /api/posts
```

### 7.2 路由前缀

```python
# 动态前缀
@v1_bp.route('/users')
def get_users():
    return {'version': 'v1', 'users': []}

app.register_blueprint(v1_bp, url_prefix='/v1')
app.register_blueprint(v2_bp, url_prefix='/v2')
```

---

## 8. 路由装饰器

### 8.1 自定义装饰器

```python
from functools import wraps
from flask import request

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return {'error': 'Unauthorized'}, 401
        return f(*args, **kwargs)
    return decorated_function

@app.route('/dashboard')
@login_required
def dashboard():
    return {'message': 'Dashboard'}
```

### 8.2 速率限制装饰器

```python
from flask_limiter import Limiter

limiter = Limiter(app, key_func=get_remote_address)

@app.route('/api/data')
@limiter.limit("10 per minute")
def get_data():
    return {'data': 'limited'}
```

---

## 9. 路由优先级

### 9.1 静态优先于动态

```python
# 静态路由优先匹配
@app.route('/user')
def get_user():
    return 'Static: user'

@app.route('/user/<username>')
def get_user_by_name(username):
    return f'Dynamic: {username}'

# 访问 /user 返回 "Static: user"
# 访问 /user/john 返回 "Dynamic: john"
```

### 9.2 规则排序

Flask 按照规则长度降序匹配，长度相同时按定义顺序：

```python
# 匹配顺序
@app.route('/user')           # 3
@app.route('/user/<id>')      # 4
@app.route('/user/profile')    # 4
@app.route('/user/<name>/posts')  # 5
```

---

## 10. 完整示例

```python
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# ============ 基础路由 ============
@app.route('/')
def index():
    return {'message': 'Welcome to Flask API'}

# ============ 路径参数 ============
@app.route('/users/<int:user_id>')
def get_user(user_id):
    return {'id': user_id, 'name': f'User {user_id}'}

@app.route('/posts/<int:year>/<int:month>')
def get_posts_by_date(year, month):
    return {'year': year, 'month': month, 'posts': []}

# ============ HTTP 方法 ============
@app.route('/items', methods=['GET', 'POST'])
def handle_items():
    if request.method == 'GET':
        return {'items': ['item1', 'item2']}
    else:
        data = request.get_json()
        return {'message': 'Created', 'item': data}, 201

# ============ 查询参数 ============
@app.route('/search')
def search():
    q = request.args.get('q', '')
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 10))
    return {
        'query': q,
        'page': page,
        'limit': limit,
        'results': []
    }

# ============ URL 构建 ============
@app.route('/url-examples')
def url_examples():
    return {
        'index': url_for('index'),
        'user': url_for('get_user', user_id=123),
        'search': url_for('search', q='flask', page=1)
    }

# ============ 请求钩子 ============
@app.before_request
def log_request():
    print(f"Request: {request.method} {request.path}")

@app.after_request
def add_headers(response):
    response.headers['X-API-Version'] = '1.0'
    return response

# ============ 错误处理 ============
@app.errorhandler(404)
def not_found(e):
    return {'error': 'Not Found'}, 404

@app.errorhandler(500)
def server_error(e):
    return {'error': 'Internal Server Error'}, 500

if __name__ == '__main__':
    app.run(debug=True)
```

---

## 总结

| 知识点 | 说明 |
|---------|------|
| 路径参数 | `<type:name>` 格式 |
| HTTP 方法 | GET、POST、PUT、DELETE |
| URL 构建 | `url_for()` 函数 |
| 请求对象 | `request` 获取数据 |
| 响应处理 | 字符串、JSON、文件 |
| 路由分组 | 蓝图 Blueprint |
| 装饰器 | 自定义和第三方 |

---

[← 返回目录](../README.md) | [下一篇 →](./Flask/02-Jinja2模板引擎.md)