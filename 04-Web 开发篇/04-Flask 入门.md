# 第 4 章：Flask 入门

掌握 Flask 框架基础，创建第一个 Web 应用。

---

## 本章目标

- 理解 Flask 框架
- 掌握路由定义
- 学会使用模板引擎 Jinja2
- 处理请求和响应
- 理解应用结构

---

## 4.1 Flask 简介

### 什么是 Flask？

Flask 是一个轻量级的 Python Web 框架，灵活、简单、易于扩展。

### 安装 Flask

```bash
pip install flask
```

### 第一个 Flask 应用

```python
# app.py
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=True)
```

运行：

```bash
python app.py
```

访问 http://127.0.0.1:5000 即可看到 "Hello, World!"

---

## 4.2 路由定义

### 基本路由

```python
from flask import Flask

app = Flask(__name__)

# 根路径
@app.route('/')
def index():
    return '首页'

# 简单路径
@app.route('/about')
def about():
    return '关于页面'

# 多个路径映射同一视图
@app.route('/home')
@app.route('/index')
def home():
    return '主页'
```

### 动态路由

```python
# 路径参数
@app.route('/user/<username>')
def user_profile(username):
    return f'用户: {username}'

# 带类型的路径参数
@app.route('/post/<int:post_id>')
def get_post(post_id):
    return f'文章 ID: {post_id}'

@app.route('/date/<int:year>/<int:month>/<int:day>')
def get_date(year, month, day):
    return f'日期: {year}-{month:02d}-{day:02d}'

# 浮点型
@app.route('/price/<float:price>')
def show_price(price):
    return f'价格: {price}元'

# 字符串型（默认）
@app.route('/name/<name>')
def show_name(name):
    return f'名字: {name}'

# 路径（包含斜杠）
@app.route('/path/<path:filepath>')
def show_path(filepath):
    return f'路径: {filepath}'
```

### HTTP 方法

```python
from flask import request, render_template_string

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        # 处理 POST 请求
        name = request.form.get('name')
        return f'收到 POST 请求: {name}'
    else:
        # 返回表单页面
        return '''
            <form method="post">
                <input type="text" name="name">
                <button type="submit">提交</button>
            </form>
        '''

# 简化的方法特定视图
@app.get('/data')
def get_data():
    return 'GET 请求'

@app.post('/data')
def create_data():
    return 'POST 请求'

@app.put('/data')
def update_data():
    return 'PUT 请求'

@app.delete('/data')
def delete_data():
    return 'DELETE 请求'
```

### URL 反向生成

```python
from flask import url_for

@app.route('/')
def index():
    # 生成 URL
    about_url = url_for('about')
    user_url = url_for('user_profile', username='john')
    return f'''
        <a href="{about_url}">关于</a>
        <a href="{user_url}">用户</a>
    '''

@app.route('/user/<username>')
def user_profile(username):
    return f'用户: {username}'
```

---

## 4.3 请求对象

### 获取请求数据

```python
from flask import request

@app.route('/analyze')
def analyze_request():
    # URL 参数
    page = request.args.get('page', '1')
    limit = request.args.get('limit', '10')
    
    # 表单数据
    username = request.form.get('username')
    password = request.form.get('password')
    
    # JSON 数据
    json_data = request.get_json()
    
    # 请求头
    user_agent = request.headers.get('User-Agent')
    auth_token = request.headers.get('Authorization')
    
    # 请求方法
    method = request.method
    
    # 请求路径
    path = request.path
    full_url = request.url
    
    # IP 地址
    ip = request.remote_addr
    
    return f'''
        <h2>请求分析</h2>
        <p>方法: {method}</p>
        <p>路径: {path}</p>
        <p>URL: {full_url}</p>
        <p>User-Agent: {user_agent}</p>
        <p>IP: {ip}</p>
        <p>Page: {page}</p>
    '''
```

### 文件上传

```python
from flask import request, send_from_directory
import os

# 配置上传文件夹
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # 检查文件
        if 'file' not in request.files:
            return '没有选择文件'
        
        file = request.files['file']
        
        if file.filename == '':
            return '没有选择文件'
        
        # 保存文件
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        
        return f'文件上传成功: {file.filename}'
    
    # 上传表单
    return '''
        <form method="post" enctype="multipart/form-data">
            <input type="file" name="file">
            <button type="submit">上传</button>
        </form>
    '''
```

---

## 4.4 响应对象

### 返回不同类型响应

```python
from flask import Response, jsonify, make_response

# 字符串响应
@app.route('/text')
def text_response():
    return '纯文本响应'

# HTML 响应
@app.route('/html')
def html_response():
    return '<h1>HTML 响应</h1>'

# JSON 响应
@app.route('/json')
def json_response():
    return jsonify({
        'status': 'success',
        'data': {'name': '张三', 'age': 25}
    })

# 自定义响应
@app.route('/custom')
def custom_response():
    response = make_response('自定义响应')
    response.headers['X-Custom-Header'] = 'Custom Value'
    response.status_code = 200
    return response

# 设置 Cookie
@app.route('/set-cookie')
def set_cookie():
    response = make_response('Cookie 已设置')
    response.set_cookie('user_id', '123', max_age=3600)
    return response

# 读取 Cookie
@app.route('/get-cookie')
def get_cookie():
    user_id = request.cookies.get('user_id', '未设置')
    return f'Cookie: {user_id}'

# 重定向
@app.route('/redirect')
def redirect_example():
    from flask import redirect, url_for
    return redirect(url_for('index'))

# 错误响应
@app.route('/error')
def error_example():
    from flask import abort
    # abort(404)  # 抛出 404 错误
    
    # 或返回错误响应
    return make_response('页面未找到', 404)
```

---

## 4.5 模板引擎 Jinja2

### 模板基础

```python
from flask import render_template, render_template_string

# 使用模板文件
@app.route('/')
def index():
    title = '首页'
    items = ['苹果', '香蕉', '橙子']
    return render_template('index.html', title=title, items=items)

# 使用内联模板（开发测试用）
@app.route('/hello')
def hello():
    return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head>
            <title>{{ title }}</title>
        </head>
        <body>
            <h1>Hello, {{ name }}!</h1>
            <ul>
            {% for item in items %}
                <li>{{ item }}</li>
            {% endfor %}
            </ul>
        </body>
        </html>
    ''', title='问候', name='World', items=['苹果', '香蕉'])
```

### 模板语法

```html
<!-- 变量 -->
<p>名字: {{ user.name }}</p>
<p>年龄: {{ user.age }}</p>

<!-- 条件判断 -->
{% if user.is_active %}
    <p>用户已激活</p>
{% else %}
    <p>用户未激活</p>
{% endif %}

<!-- 循环 -->
{% for item in items %}
    <li>{{ loop.index }}. {{ item }}</li>
{% endfor %}

<!-- 循环索引 -->
<ul>
{% for item in items %}
    <li class="{% if loop.first %}first{% endif %}">
        {{ item }}
    </li>
{% endfor %}
</ul>

<!-- 过滤器 -->
<p>{{ name|upper }}</p>           <!-- 大写 -->
<p>{{ text|truncate(20) }}</p>   <!-- 截断 -->
<p>{{ items|length }}</p>        <!-- 长度 -->
<p>{{ date|date('%Y-%m-%d') }}</p> <!-- 日期格式化 -->

<!-- 自定义过滤器 -->
<!-- app.py 中: -->
<!-- from flask import Flask -->
<!-- app = Flask(__name__) -->
<!-- @app.template_filter('reverse') -->
<!-- def reverse_filter(s): return s[::-1] -->
<p>{{ text|reverse }}</p>
```

### 模板继承

```html
<!-- base.html -->
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{% block title %}默认标题{% endblock %}</title>
    {% block extra_head %}{% endblock %}
</head>
<body>
    <header>
        <nav>
            <a href="/">首页</a>
            <a href="/about">关于</a>
        </nav>
    </header>
    
    <main>
        {% block content %}{% endblock %}
    </main>
    
    <footer>
        {% block footer %}
            <p>&copy; 2024 我的网站</p>
        {% endblock %}
    </footer>
</body>
</html>

<!-- index.html -->
{% extends "base.html" %}

{% block title %}首页{% endblock %}

{% block content %}
    <h1>欢迎来到首页</h1>
    <p>这是首页内容</p>
{% endblock %}
```

---

## 4.6 实战：个人博客首页

### 项目结构

```
blog/
├── app.py
├── templates/
│   ├── base.html
│   ├── index.html
│   └── post.html
└── static/
    └── style.css
```

### 代码实现

```python
# app.py
from flask import Flask, render_template

app = Flask(__name__)

# 模拟数据
posts = [
    {
        'id': 1,
        'title': 'Python Web 开发入门',
        'content': 'Flask 是一个轻量级的 Web 框架...',
        'author': '张三',
        'date': '2024-01-15',
        'views': 120
    },
    {
        'id': 2,
        'title': '理解 HTTP 协议',
        'content': 'HTTP 是 Web 通信的基础协议...',
        'author': '李四',
        'date': '2024-01-10',
        'views': 85
    },
    {
        'id': 3,
        'title': '前端基础 HTML 与 CSS',
        'content': 'HTML 用于构建网页结构...',
        'author': '王五',
        'date': '2024-01-05',
        'views': 200
    }
]

@app.route('/')
def index():
    return render_template('index.html', posts=posts)

@app.route('/post/<int:post_id>')
def post(post_id):
    post = next((p for p in posts if p['id'] == post_id), None)
    if post:
        return render_template('post.html', post=post)
    return '文章不存在', 404

if __name__ == '__main__':
    app.run(debug=True)
```

```html
<!-- templates/base.html -->
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}我的博客{% endblock %}</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>
    <header>
        <div class="container">
            <h1><a href="/">我的博客</a></h1>
            <nav>
                <a href="/">首页</a>
                <a href="/about">关于</a>
            </nav>
        </div>
    </header>
    
    <main class="container">
        {% block content %}{% endblock %}
    </main>
    
    <footer>
        <div class="container">
            <p>&copy; 2024 我的博客. All rights reserved.</p>
        </div>
    </footer>
</body>
</html>
```

```html
<!-- templates/index.html -->
{% extends "base.html" %}

{% block content %}
    <div class="posts">
        {% for post in posts %}
        <article class="post-card">
            <h2><a href="/post/{{ post.id }}">{{ post.title }}</a></h2>
            <div class="post-meta">
                <span>作者: {{ post.author }}</span>
                <span>日期: {{ post.date }}</span>
                <span>浏览: {{ post.views }}</span>
            </div>
            <p class="post-excerpt">{{ post.content[:100] }}...</p>
            <a href="/post/{{ post.id }}" class="read-more">阅读全文 →</a>
        </article>
        {% endfor %}
    </div>
{% endblock %}
```

```css
/* static/style.css */
* { margin: 0; padding: 0; box-sizing: border-box; }

body {
    font-family: -apple-system, BlinkMacSystemFont, sans-serif;
    line-height: 1.6;
    color: #333;
    background: #f5f5f5;
}

.container {
    max-width: 800px;
    margin: 0 auto;
    padding: 0 20px;
}

header {
    background: #fff;
    padding: 20px 0;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

header h1 a {
    text-decoration: none;
    color: #333;
}

nav { margin-top: 10px; }
nav a {
    margin-right: 20px;
    text-decoration: none;
    color: #666;
}
nav a:hover { color: #007bff; }

main { padding: 40px 0; }

.post-card {
    background: #fff;
    padding: 30px;
    margin-bottom: 20px;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.post-card h2 a {
    text-decoration: none;
    color: #333;
}

.post-meta {
    color: #999;
    font-size: 0.9em;
    margin: 10px 0;
}

.post-meta span { margin-right: 15px; }

.read-more {
    display: inline-block;
    margin-top: 15px;
    color: #007bff;
    text-decoration: none;
}

footer {
    text-align: center;
    padding: 20px;
    color: #999;
}
```

---

## 本章总结

### 学到的技能

| 技能 | 说明 |
|------|------|
| Flask 基础 | 框架安装、第一个应用 |
| 路由定义 | 路径参数、HTTP 方法 |
| 请求对象 | 获取表单、JSON、文件 |
| 响应对象 | JSON、Cookie、重定向 |
| Jinja2 模板 | 变量、循环、条件、继承 |

### 下一步

在 [第 5 章](./05-Flask 进阶.md) 中，我们将学习 Flask 进阶内容，包括数据库集成和蓝图。

---

[← 上一章](./03-JavaScript 基础.md) | [下一章 →](./05-Flask 进阶.md)