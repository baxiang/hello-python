# 第 25 章 - Flask 快速上手（详细版）

本章带你快速入门 Flask 框架，从安装配置到路由、请求处理、响应构建，掌握 Flask 开发的核心基础。

---

## 第一部分：Flask 简介与安装

### 25.1 什么是 Flask

#### 概念说明

Flask 是一个轻量级的 Python Web 框架，被称为"微框架"（Microframework）。

**Flask 的核心理念：**

```
┌─────────────────────────────────────────────────────────────┐
│                    Flask 设计理念                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   核心特点：                                                │
│   • 轻量级：核心代码仅几千行                               │
│   • 灵活：不强制项目结构，按需选择扩展                     │
│   • 易上手：API 简洁直观，文档完善                          │
│   • 生态丰富：大量官方和第三方扩展                         │
│                                                             │
│   Flask vs 全栈框架（如 Django）：                          │
│   ┌───────────────────────────────────────────────────┐     │
│   │  Flask (微框架)          │  Django (全栈框架)     │     │
│   │  ├─ 核心：路由、视图     │  ├─ 自带 ORM            │     │
│   │  ├─ 扩展：按需添加       │  ├─ 自带 Admin          │     │
│   │  ├─ 数据库：Flask-SQLA   │  ├─ 自带表单系统        │     │
│   │  └─ 灵活：自由组织       │  └─ 约定：约定优于配置  │     │
│   └───────────────────────────────────────────────────┘     │
│                                                             │
│   适用场景：                                                │
│   • 小型到中型 Web 应用                                      │
│   • RESTful API 服务                                         │
│   • 快速原型开发                                             │
│   • 微服务架构                                               │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

### 25.2 安装 Flask

#### 概念说明

使用 uv 包管理器安装 Flask 及其常用扩展。

**安装步骤：**

```bash
# 1. 创建新项目
uv init my-flask-app
cd my-flask-app

# 2. 安装 Flask
uv add flask

# 3. 安装常用扩展（可选）
uv add flask-sqlalchemy    # 数据库 ORM
uv add flask-login         # 用户认证
uv add flask-wtf           # 表单处理
uv add flask-migrate       # 数据库迁移
uv add python-dotenv       # 环境变量

# 4. 运行应用
uv run python app.py
```

**项目结构建议：**

```
my-flask-app/
├── app.py              # 应用入口
├── requirements.txt    # 依赖列表
├── .env                # 环境变量
├── templates/          # HTML 模板
│   └── index.html
└── static/             # 静态文件
    ├── css/
    ├── js/
    └── images/
```

---

### 25.3 第一个 Flask 应用

#### 概念说明

一个最小的 Flask 应用只需要几行代码。

**示例代码：Hello World**

```python
# app.py
from flask import Flask

# 创建 Flask 应用实例
app = Flask(__name__)


# 定义路由和视图函数
@app.route('/')
def hello():
    return 'Hello, World!'


# 运行开发服务器
if __name__ == '__main__':
    app.run(debug=True)
```

**运行应用：**

```bash
# 方式一：直接运行 Python 文件
uv run python app.py

# 方式二：使用 flask 命令
# 设置环境变量
export FLASK_APP=app.py
export FLASK_DEBUG=1
uv run flask run
```

**输出：**

```
 * Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
```

**访问：** http://127.0.0.1:5000

---

### 25.4 Flask(__name__) 参数详解

#### 概念说明

`Flask(__name__)` 中的 `__name__` 参数用于确定应用的根目录。

```python
# __name__ 的值取决于运行方式

# 方式 1：直接运行 python app.py
print(__name__)  # 输出：__main__

# 方式 2：作为模块导入 from app import app
print(__name__)  # 输出：app
```

**为什么需要 `__name__`？**

```
┌─────────────────────────────────────────────────────────────┐
│              __name__ 的作用                                │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   Flask 需要知道：                                          │
│   • 模板文件夹在哪里 (templates/)                           │
│   • 静态文件夹在哪里 (static/)                              │
│   • 相对路径如何解析                                        │
│                                                             │
│   使用 __name__，Flask 可以：                               │
│   • 自动定位到 app.py 所在目录                              │
│   • 正确加载 templates 和 static 文件夹                     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 第二部分：开发服务器与调试模式

### 25.5 开发服务器

#### 概念说明

Flask 内置了一个轻量级的开发服务器，适合开发环境使用。

**app.run() 参数详解：**

```python
app.run(
    host='127.0.0.1',   # 监听地址，0.0.0.0 表示所有网卡
    port=5000,          # 端口号
    debug=None,         # 调试模式
    load_dotenv=True,   # 加载.env 文件
    **options
)
```

**常用配置：**

```python
# 开发环境
app.run(debug=True)  # 启用调试模式

# 允许外部访问
app.run(host='0.0.0.0', port=5000)

# 指定端口
app.run(port=8080)
```

---

### 25.6 调试模式

#### 概念说明

调试模式启用后，代码变更会自动重载，并且提供交互式调试器。

**启用调试模式的方式：**

```python
# 方式 1：在代码中设置
app.run(debug=True)

# 方式 2：使用环境变量
export FLASK_DEBUG=1
uv run flask run

# 方式 3：使用 flask 命令
uv run flask --debug run
```

**调试模式的特性：**

```
┌─────────────────────────────────────────────────────────────┐
│                  调试模式特性                                │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   1. 自动重载 (Auto Reload)                                 │
│      代码修改后，服务器自动重启，无需手动停止               │
│                                                             │
│   2. 交互式调试器 (Interactive Debugger)                    │
│      出错时显示详细的堆栈信息                               │
│      可在浏览器中执行 Python 代码调试                        │
│                                                             │
│   3. 详细的错误页面                                         │
│      显示完整的 traceback                                   │
│      显示源代码和局部变量                                   │
│                                                             │
│   ⚠️ 警告：调试模式有安全风险，不要在生产环境使用！          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 第三部分：路由与视图函数

### 25.7 @app.route 装饰器

#### 概念说明

路由（Route）将 URL 映射到视图函数，`@app.route()` 装饰器用于注册路由。

**基本用法：**

```python
from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    return '首页'


@app.route('/about')
def about():
    return '关于我们'


@app.route('/contact')
def contact():
    return '联系方式'
```

**访问 URL：**
- http://localhost:5000/ → 首页
- http://localhost:5000/about → 关于我们
- http://localhost:5000/contact → 联系方式

---

### 25.8 动态路由规则

#### 概念说明

使用尖括号 `<variable_name>` 可以在 URL 中捕获动态值并传递给视图函数。

**URL 变量类型转换器：**

```python
@app.route('/user/<username>')
def show_user(username):
    """字符串类型（默认）"""
    return f'用户：{username}'


@app.route('/post/<int:post_id>')
def show_post(post_id):
    """整数类型"""
    return f'文章 ID: {post_id}'


@app.route('/price/<float:price>')
def show_price(price):
    """浮点数类型"""
    return f'价格：{price}'


@app.route('/path/<path:subpath>')
def show_path(subpath):
    """路径类型（可包含斜杠）"""
    return f'子路径：{subpath}'


@app.route('/uuid/<uuid:user_id>')
def show_uuid(user_id):
    """UUID 类型"""
    return f'UUID: {user_id}'
```

**示例：博客文章 URL**

```python
# /article/2027/03/09/my-first-post
@app.route('/article/<int:year>/<int:month>/<int:day>/<slug:title>')
def article(year, month, day, title):
    return f'{year}年{month}月{day}日 - {title}'
```

---

### 25.9 URL 构建：url_for()

#### 概念说明

`url_for()` 函数根据视图函数名生成 URL，避免硬编码 URL。

**基本用法：**

```python
from flask import Flask, url_for

app = Flask(__name__)


@app.route('/')
def index():
    return '首页'


@app.route('/user/<username>')
def user_profile(username):
    return f'{username}的主页'


# 生成 URL
print(url_for('index'))           # 输出：/
print(url_for('user_profile', username='张三'))  # 输出：/user/张三
```

**url_for() 的优势：**

```
┌─────────────────────────────────────────────────────────────┐
│              使用 url_for() 的优势                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   1. 易于重构                                               │
│      修改路由规则后，不需要修改所有引用该 URL 的地方         │
│                                                             │
│   2. 自动处理特殊字符                                        │
│      url_for('/user/张三') → /user/%E5%BC%A0%E4%B8%89       │
│                                                             │
│   3. 支持测试环境                                           │
│      测试时可以重定向到测试服务器                           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

### 25.10 重定向与 abort

#### 概念说明

`redirect()` 用于跳转到其他 URL，`abort()` 用于立即返回错误状态码。

**示例代码：**

```python
from flask import Flask, redirect, abort, url_for

app = Flask(__name__)


# 永久重定向
@app.route('/old-page')
def old_page():
    return redirect(url_for('new_page'), code=301)


# 临时重定向
@app.route('/new-page')
def new_page():
    return '这是新页面'


# 根据条件重定向
@app.route('/admin')
def admin():
    user = get_current_user()  # 假设有这个函数
    if not user:
        return redirect(url_for('login'))
    if not user.is_admin:
        abort(403)  # 返回 403 Forbidden
    return '管理员页面'


# 自定义错误页面
@app.errorhandler(403)
def forbidden(error):
    return '您没有权限访问此页面', 403


@app.errorhandler(404)
def not_found(error):
    return '页面未找到', 404
```

---

## 第四部分：请求处理

### 25.11 request 对象

#### 概念说明

Flask 的 `request` 对象封装了 HTTP 请求的所有信息。

**导入 request：**

```python
from flask import request
```

**request 对象常用属性：**

```python
from flask import Flask, request

app = Flask(__name__)


@app.route('/request-info')
def request_info():
    """展示 request 对象的常用属性"""

    # 请求方法
    method = request.method  # GET, POST, PUT, DELETE, etc.

    # URL 信息
    url = request.url                # 完整 URL
    path = request.path              # 路径部分
    args = request.args              # 查询参数 (ImmutableMultiDict)

    # 请求头
    user_agent = request.user_agent  # 浏览器信息
    content_type = request.content_type  # Content-Type

    # 客户端信息
    remote_addr = request.remote_addr  # IP 地址

    return f'''
    <h3>请求信息</h3>
    <p>方法：{method}</p>
    <p>URL: {url}</p>
    <p>路径：{path}</p>
    <p>用户代理：{user_agent}</p>
    <p>IP 地址：{remote_addr}</p>
    '''
```

---

### 25.12 获取请求数据

#### 概念说明

不同 Content-Type 的请求使用不同的方式获取数据。

**获取查询参数（Query Parameters）：**

```python
from flask import Flask, request

app = Flask(__name__)


@app.route('/search')
def search():
    # URL: /search?q=python&page=2
    keyword = request.args.get('q')      # 获取单个参数
    page = request.args.get('page', 1)   # 带默认值

    # 获取所有参数
    all_args = request.args.to_dict()

    return f'搜索：{keyword}, 页码：{page}'
```

**获取表单数据（Form Data）：**

```python
@app.route('/login', methods=['POST'])
def login():
    # Content-Type: application/x-www-form-urlencoded
    username = request.form.get('username')
    password = request.form.get('password')

    # 获取所有表单字段
    all_form_data = request.form.to_dict()

    return f'登录用户：{username}'
```

**获取 JSON 数据：**

```python
@app.route('/api/users', methods=['POST'])
def create_user():
    # Content-Type: application/json
    data = request.get_json()

    # 获取单个字段
    username = data.get('username')
    email = data.get('email')

    # 如果 JSON 格式无效，返回 400
    if not data:
        abort(400, description='无效的 JSON 数据')

    return {'message': f'创建用户：{username}'}
```

**获取上传的文件：**

```python
@app.route('/upload', methods=['POST'])
def upload_file():
    # Content-Type: multipart/form-data
    file = request.files.get('file')

    if file:
        # 保存文件
        file.save(f'./uploads/{file.filename}')
        return f'文件已上传：{file.filename}'

    return '未选择文件', 400
```

---

### 25.13 请求钩子

#### 概念说明

请求钩子允许在请求处理的不同阶段执行代码。

**四种请求钩子：**

```python
from flask import Flask, request, g

app = Flask(__name__)


@app.before_request
def before_request():
    """在每个请求处理之前执行"""
    # 可用于：用户认证、日志记录、数据库连接
    print(f"处理请求：{request.method} {request.path}")
    g.start_time = time.time()  # g 对象用于存储请求级别的数据


@app.after_request
def after_request(response):
    """在每个请求处理之后执行（无异常时）"""
    # 可用于：添加响应头、记录日志
    response.headers['X-Custom-Header'] = 'MyApp'
    return response  # 必须返回 response


@app.teardown_request
def teardown_request(exception=None):
    """在请求结束时执行（无论是否有异常）"""
    # 可用于：关闭数据库连接、清理资源
    if exception:
        print(f'请求处理异常：{exception}')


@app.errorhandler(404)
def handle_404(error):
    """错误处理器"""
    return '页面未找到', 404
```

**使用场景示例：用户认证**

```python
from flask import Flask, request, redirect, url_for, g
from functools import wraps

app = Flask(__name__)


def login_required(f):
    """登录检查装饰器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.current_user is None:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


@app.before_request
def load_current_user():
    """在每次请求前加载当前用户"""
    session_id = request.cookies.get('session_id')
    g.current_user = get_user_from_session(session_id)  # 假设有这个函数
```

---

## 第五部分：响应构建

### 25.14 Response 对象

#### 概念说明

视图函数返回的内容会被 Flask 包装成 Response 对象返回给客户端。

**返回值的多种形式：**

```python
from flask import Flask, Response, make_response

app = Flask(__name__)


# 1. 返回字符串（最常见）
@app.route('/hello')
def hello():
    return 'Hello, World!'


# 2. 返回元组 (响应体，状态码)
@app.route('/not-found')
def not_found():
    return '页面不存在', 404


# 3. 返回元组 (响应体，状态码，响应头)
@app.route('/custom')
def custom():
    return '自定义响应', 201, {'X-Custom': 'Value'}


# 4. 使用 make_response 创建 Response 对象
@app.route('/make-response')
def make_resp():
    response = make_response('响应内容', 200)
    response.headers['X-Header'] = 'Value'
    response.set_cookie('my_cookie', 'value')
    return response


# 5. 直接返回 Response 对象
@app.route('/api/data')
def api_data():
    return Response(
        response='{"data": "value"}',
        status=200,
        content_type='application/json'
    )
```

---

### 25.15 JSON 响应

#### 概念说明

API 开发中，常用 `jsonify()` 返回 JSON 格式的响应。

**示例代码：**

```python
from flask import Flask, jsonify

app = Flask(__name__)


# 返回单个对象
@app.route('/api/user/<int:user_id>')
def get_user(user_id):
    user = {
        'id': user_id,
        'name': '张三',
        'email': 'zhangsan@example.com'
    }
    return jsonify(user)


# 返回数组
@app.route('/api/users')
def get_users():
    users = [
        {'id': 1, 'name': '张三'},
        {'id': 2, 'name': '李四'},
        {'id': 3, 'name': '王五'}
    ]
    return jsonify(users)


# 返回嵌套结构
@app.route('/api/article/<int:article_id>')
def get_article(article_id):
    article = {
        'id': article_id,
        'title': '我的文章',
        'content': '...',
        'author': {
            'id': 1,
            'name': '张三'
        },
        'comments': [
            {'id': 1, 'text': '好文章！'},
            {'id': 2, 'text': '学习了'}
        ]
    }
    return jsonify(article)


# 返回错误响应
@app.route('/api/error')
def api_error():
    return jsonify({
        'error': 'NOT_FOUND',
        'message': '资源不存在'
    }), 404
```

**浏览器输出：**

```json
{
  "id": 1,
  "name": "张三",
  "email": "zhangsan@example.com"
}
```

---

### 25.16 设置响应头

#### 概念说明

可以通过多种方式设置响应头。

**示例代码：**

```python
from flask import Flask, make_response, jsonify

app = Flask(__name__)


# 方式 1：使用 make_response
@app.route('/with-headers')
def with_headers():
    response = make_response('内容')
    response.headers['X-Custom-Header'] = 'Value'
    response.headers['Content-Type'] = 'text/plain; charset=utf-8'
    return response


# 方式 2：返回元组
@app.route('/tuple-headers')
def tuple_headers():
    return '内容', 200, {'X-Custom': 'Value'}


# 方式 3：常用响应头设置
@app.route('/download')
def download():
    response = make_response('文件内容')
    response.headers['Content-Disposition'] = 'attachment; filename=file.txt'
    return response


# 方式 4：CORS 跨域设置
@app.route('/api/cors')
def cors():
    response = jsonify({'data': 'value'})
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response
```

---

## 第六部分：会话管理

### 25.17 session 对象

#### 概念说明

Flask 的 `session` 对象用于在请求之间保存用户状态。

**基本用法：**

```python
from flask import Flask, session, redirect, url_for, request

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # 必须设置密钥


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        # 存储到 session
        session['username'] = username
        session['user_id'] = get_user_id(username)  # 假设有这个函数
        return redirect(url_for('index'))

    return '''
    <form method="post">
        <input name="username" placeholder="用户名">
        <button type="submit">登录</button>
    </form>
    '''


@app.route('/')
def index():
    # 读取 session
    if 'username' in session:
        return f'欢迎回来，{session["username"]}！'
    return '您还未登录'


@app.route('/logout')
def logout():
    # 清除 session
    session.clear()  # 或 session.pop('username', None)
    return redirect(url_for('index'))
```

**设置 session 过期时间：**

```python
from datetime import timedelta

# 配置 session 永久有效
app.permanent_session_lifetime = timedelta(days=7)


@app.route('/login', methods=['POST'])
def login():
    session.permanent = True  # 标记为永久 session
    session['username'] = request.form.get('username')
    return '登录成功'
```

---

## 本章小结

```
┌─────────────────────────────────────────────────────────────┐
│                      第 25 章 知识要点                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   Flask 基础：                                               │
│   ✓ 安装：uv add flask                                      │
│   ✓ 最小应用：Flask(__name__)、@app.route()、app.run()     │
│   ✓ 调试模式：debug=True 或 FLASK_DEBUG=1                   │
│                                                             │
│   路由：                                                     │
│   ✓ 动态路由：<int:id>、<string:name>、<path:subpath>       │
│   ✓ url_for()：根据函数名生成 URL                           │
│   ✓ redirect()：重定向到其他 URL                            │
│   ✓ abort()：立即返回错误状态码                            │
│                                                             │
│   请求处理：                                                 │
│   ✓ request.method：请求方法                                │
│   ✓ request.args：查询参数                                  │
│   ✓ request.form：表单数据                                  │
│   ✓ request.get_json()：JSON 数据                            │
│   ✓ request.files：上传文件                                 │
│   ✓ before_request/after_request：请求钩子                  │
│                                                             │
│   响应构建：                                                 │
│   ✓ 返回值：字符串、元组、Response 对象                       │
│   ✓ jsonify()：返回 JSON 响应                                │
│   ✓ make_response()：创建 Response 对象                      │
│   ✓ 设置响应头：headers、set_cookie()                        │
│                                                             │
│   会话管理：                                                 │
│   ✓ session 对象：存储用户状态                               │
│   ✓ secret_key：签名密钥                                    │
│   ✓ session.permanent：永久 session                          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```
---

[← 上一篇](./01-Web基础.md) | [下一篇 →](./03-Flask进阶.md)
