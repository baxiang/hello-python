# 第 26 章 - Flask 进阶（详细版）

本章深入讲解 Flask 的高级特性，包括 Jinja2 模板引擎、蓝图模块化、数据库集成和用户认证。

---

## 第一部分：模板引擎（Jinja2）

### 26.1 模板渲染

#### 概念说明

Jinja2 是 Flask 内置的模板引擎，允许在 HTML 中嵌入 Python 表达式，实现动态页面渲染。

**目录结构：**

```
my-app/
├── app.py
└── templates/          # 模板文件夹（固定名称）
    ├── base.html       # 基础模板
    ├── index.html      # 首页模板
    └── user.html       # 用户模板
```

**基本用法：**

```python
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    # 渲染模板，传递变量
    return render_template('index.html', title='首页', user='张三')
```

**templates/index.html：**

```html
<!DOCTYPE html>
<html>
<head>
    <title>{{ title }}</title>
</head>
<body>
    <h1>欢迎，{{ user }}！</h1>
</body>
</html>
```

**render_template() 参数：**

```python
# 传递多个变量
render_template(
    'index.html',
    title='首页',
    user='张三',
    age=25,
    items=[1, 2, 3]
)

# 使用字典解包
context = {'title': '首页', 'user': '张三'}
render_template('index.html', **context)
```

---

### 26.2 变量与表达式

#### 概念说明

Jinja2 使用 `{{ }}` 语法输出变量，支持表达式和过滤器。

**变量输出：**

```html
<!-- 基础变量 -->
<h1>{{ username }}</h1>

<!-- 对象属性 -->
<p>{{ user.name }}</p>
<p>{{ user.email }}</p>

<!-- 字典访问 -->
<p>{{ config['SITE_NAME'] }}</p>
<p>{{ data.key }}</p>

<!-- 列表索引 -->
<p>{{ items.0 }}</p>
<p>{{ users.0.name }}</p>
```

**表达式运算：**

```html
<!-- 算术运算 -->
<p>{{ price * quantity }}</p>
<p>{{ (price - discount) | round(2) }}</p>

<!-- 逻辑运算 -->
{% if user and user.is_active %}
    <p>活跃用户</p>
{% endif %}

<!-- 比较运算 -->
{% if score >= 60 %}
    <p>及格</p>
{% else %}
    <p>不及格</p>
{% endif %}
```

**过滤器（Filters）：**

```html
<!-- 字符串处理 -->
<p>{{ name | upper }}</p>           <!-- 大写 -->
<p>{{ name | lower }}</p>           <!-- 小写 -->
<p>{{ name | title }}</p>           <!-- 首字母大写 -->
<p>{{ name | capitalize }}</p>      <!-- 句首大写 -->

<!-- 默认值 -->
<p>{{ nickname | default('匿名用户') }}</p>
<p>{{ nickname | default('匿名用户', true) }}</p>  <!-- 空字符串也使用默认值 -->

<!-- 列表处理 -->
<p>{{ items | first }}</p>          <!-- 第一个元素 -->
<p>{{ items | last }}</p>           <!-- 最后一个元素 -->
<p>{{ items | length }}</p>         <!-- 长度 -->
<p>{{ items | join(', ') }}</p>     <!-- 连接字符串 -->

<!-- 其他 -->
<p>{{ content | truncate(100) }}</p>  <!-- 截断 -->
<p>{{ html | safe }}</p>              <!-- 不转义 HTML -->
<p>{{ text | escape }}</p>            <!-- HTML 转义 -->
```

**自定义过滤器：**

```python
# app.py
@app.template_filter('reverse')
def reverse_filter(s):
    return s[::-1]


# 使用
<p>{{ name | reverse }}</p>  <!-- 输出反向字符串 -->
```

---

### 26.3 控制结构

#### 概念说明

Jinja2 支持 `{% %}` 语法用于控制结构，如条件判断和循环。

**条件判断：**

```html
<!-- if / elif / else -->
{% if user.role == 'admin' %}
    <a href="/admin">管理后台</a>
{% elif user.role == 'editor' %}
    <a href="/editor">编辑后台</a>
{% else %}
    <a href="/user">用户中心</a>
{% endif %}

<!-- 逻辑运算 -->
{% if user and user.is_active %}
    <p>活跃用户</p>
{% endif %}

<!-- 比较运算 -->
{% if score >= 90 %}
    <p>优秀</p>
{% elif score >= 60 %}
    <p>及格</p>
{% else %}
    <p>不及格</p>
{% endif %}
```

**循环：**

```html
<!-- 遍历列表 -->
<ul>
{% for item in items %}
    <li>{{ item }}</li>
{% endfor %}
</ul>

<!-- 遍历对象列表 -->
<ul>
{% for user in users %}
    <li>
        <span class="loop-index">{{ loop.index }}</span>  <!-- 从 1 开始 -->
        <span class="loop-index0">{{ loop.index0 }}</span> <!-- 从 0 开始 -->
        <span>{{ user.name }}</span>
        {% if loop.first %}<span class="first">首个</span>{% endif %}
        {% if loop.last %}<span class="last">末尾</span>{% endif %}
    </li>
{% else %}
    <li>暂无数据</li>  <!-- 列表为空时执行 -->
{% endfor %}
</ul>

<!-- 嵌套循环 -->
{% for category in categories %}
    <h3>{{ category.name }}</h3>
    <ul>
    {% for article in category.articles %}
        <li>{{ article.title }}</li>
    {% endfor %}
    </ul>
{% endfor %}
```

---

### 26.4 模板继承

#### 概念说明

模板继承允许创建基础模板，子模板继承并覆盖特定部分，避免代码重复。

**基础模板 base.html：**

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>{% block title %}默认标题{% endblock %}</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
    {% block extra_css %}{% endblock %}
</head>
<body>
    <header>
        <nav>
            <a href="{{ url_for('index') }}">首页</a>
            <a href="{{ url_for('about') }}">关于</a>
            <a href="{{ url_for('contact') }}">联系</a>
        </nav>
    </header>

    <main>
        {% block content %}{% endblock %}
    </main>

    <footer>
        <p>&copy; 2027 我的网站</p>
    </footer>

    {% block extra_js %}{% endblock %}
</body>
</html>
```

**子模板 index.html：**

```html
{% extends "base.html" %}

{% block title %}首页 - {{ super() }}{% endblock %}

{% block content %}
<h1>欢迎来到首页</h1>
<p>这里是首页内容...</p>

{% for article in articles %}
    <article>
        <h2>{{ article.title }}</h2>
        <p>{{ article.summary }}</p>
    </article>
{% endfor %}
{% endblock %}

{% block extra_js %}
<script src="{{ url_for('static', filename='js/index.js') }}"></script>
{% endblock %}
```

**关键点：**
- `{% extends "base.html" %}` 必须在模板第一行
- `{% block name %}{% endblock %}` 定义可覆盖的区域
- `{{ super() }}` 调用父模板的内容

---

### 26.5 宏（Macro）

#### 概念说明

宏类似于函数，可以重复使用，用于封装常用的 HTML 片段。

**定义宏：**

```html
<!-- macros/form.html -->
{% macro input_field(name, type='text', label='', placeholder='') %}
<div class="form-group">
    {% if label %}
    <label for="{{ name }}">{{ label }}</label>
    {% endif %}
    <input type="{{ type }}" name="{{ name }}" id="{{ name }}" placeholder="{{ placeholder }}">
</div>
{% endmacro %}


{% macro button(text, type='submit', class='') %}
<button type="{{ type }}" class="{{ class }}">{{ text }}</button>
{% endmacro %}
```

**使用宏：**

```html
<!-- 方式 1：在同一文件中定义并使用 -->
{% from 'macros/form.html' import input_field, button %}

<form>
    {{ input_field('username', label='用户名', placeholder='请输入用户名') }}
    {{ input_field('password', type='password', label='密码') }}
    {{ button('登录', class='btn-primary') }}
</form>


<!-- 方式 2：导入整个宏文件 -->
{% import 'macros/form.html' as form %}

<form>
    {{ form.input_field('email', type='email', label='邮箱') }}
    {{ form.button('提交') }}
</form>
```

---

## 第二部分：蓝图（Blueprint）

### 26.6 为什么需要蓝图

#### 概念说明

当应用变大时，将所有路由放在一个文件中会变得难以维护。蓝图允许将应用拆分为多个模块。

**问题：单一文件的局限**

```python
# app.py - 当路由很多时会变得混乱
@app.route('/')
def index(): ...

@app.route('/user/login')
def user_login(): ...

@app.route('/user/register')
def user_register(): ...

@app.route('/admin/dashboard')
def admin_dashboard(): ...
# ... 几十上百个路由
```

**解决方案：蓝图模块化**

```
my-app/
├── app.py
├── blueprints/
│   ├── __init__.py
│   ├── auth.py      # 认证相关路由
│   ├── admin.py     # 管理后台路由
│   └── api.py       # API 路由
└── templates/
    ├── auth/
    ├── admin/
    └── ...
```

---

### 26.7 创建与注册蓝图

#### 概念说明

蓝图是路由的集合，可以独立定义，然后注册到主应用。

**创建蓝图：**

```python
# blueprints/auth.py
from flask import Blueprint, render_template, request, redirect, url_for

# 创建蓝图
auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login')
def login():
    return render_template('auth/login.html')


@auth_bp.route('/register')
def register():
    return render_template('auth/register.html')


@auth_bp.route('/logout')
def logout():
    return redirect(url_for('auth.login'))
```

**注册蓝图：**

```python
# app.py
from flask import Flask
from blueprints.auth import auth_bp
from blueprints.admin import admin_bp
from blueprints.api import api_bp

app = Flask(__name__)

# 注册蓝图
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(api_bp, url_prefix='/api')


# 主应用路由
@app.route('/')
def index():
    return render_template('index.html')
```

**URL 映射：**

| 蓝图 | 路由 | 完整 URL |
|------|------|---------|
| auth_bp | `/login` | `/auth/login` |
| auth_bp | `/register` | `/auth/register` |
| admin_bp | `/dashboard` | `/admin/dashboard` |
| api_bp | `/users` | `/api/users` |

---

### 26.8 蓝图 URL 前缀与端点

#### 概念说明

蓝图可以设置 URL 前缀和端点前缀，方便组织和管理。

**蓝图配置选项：**

```python
# 完整参数
Blueprint(
    'auth',              # 蓝图名称
    __name__,            # 导入名
    url_prefix='/auth',  # URL 前缀
    subdomain='auth',    # 子域名（可选）
    template_folder='templates',  # 模板文件夹
    static_folder='static',       # 静态文件夹
    static_url_path='/static/auth'
)
```

**端点命名：**

```python
# 蓝图中的路由端点格式：蓝图名。函数名
# auth_bp.login
# auth_bp.register

# 在模板中使用
<a href="{{ url_for('auth.login') }}">登录</a>
<a href="{{ url_for('auth.register') }}">注册</a>
```

---

### 26.9 应用工厂模式

#### 概念说明

应用工厂模式使用函数创建 Flask 应用，而不是在模块级别直接创建，更适合测试和多种配置。

**为什么需要工厂模式：**

```
┌─────────────────────────────────────────────────────────────┐
│              应用工厂模式的优势                              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   1. 多环境配置                                             │
│      可以创建开发、测试、生产等不同环境的应用实例           │
│                                                             │
│   2. 应用实例隔离                                           │
│      每次测试都创建新的应用实例，避免状态污染               │
│                                                             │
│   3. 循环导入问题                                           │
│      蓝图可以导入 create_app 函数，避免循环依赖              │
│                                                             │
│   4. 扩展初始化灵活                                         │
│      可以在创建应用后初始化扩展                             │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**工厂模式实现：**

```python
# app/__init__.py
from flask import Flask


def create_app(config_name='default'):
    """应用工厂函数"""
    app = Flask(__name__)

    # 加载配置
    app.config.from_object(f'config.{config_name}')

    # 注册蓝图
    from .blueprints.auth import auth_bp
    from .blueprints.admin import admin_bp
    from .blueprints.api import api_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(api_bp, url_prefix='/api')

    # 注册扩展
    from .extensions import db, login_manager
    db.init_app(app)
    login_manager.init_app(app)

    return app
```

**使用工厂：**

```python
# run.py
from app import create_app

app = create_app('development')

if __name__ == '__main__':
    app.run()
```

**测试中使用：**

```python
# tests/test_auth.py
from app import create_app
import pytest


@pytest.fixture
def app():
    app = create_app('testing')
    with app.app_context():
        yield app


@pytest.fixture
def client(app):
    return app.test_client()


def test_login(client):
    response = client.get('/auth/login')
    assert response.status_code == 200
```

---

## 第三部分：数据库集成

### 26.10 Flask-SQLAlchemy 简介

#### 概念说明

Flask-SQLAlchemy 是 Flask 的数据库 ORM 扩展，简化了 SQLAlchemy 的使用。

**安装与配置：**

```bash
uv add flask-sqlalchemy
```

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# 配置数据库 URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://user:pass@localhost/blog'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:pass@localhost/blog'

# 关闭追踪修改（节省内存）
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 初始化扩展
db = SQLAlchemy(app)
```

---

### 26.11 模型定义

#### 概念说明

模型类继承自 `db.Model`，每个类对应一张表，每个属性对应一列。

**基本模型：**

```python
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class User(db.Model):
    """用户模型"""
    __tablename__ = 'users'

    # 主键
    id = db.Column(db.Integer, primary_key=True)

    # 普通列
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # 关系（一对多：一个用户可以有多篇文章）
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return f'<User {self.username}>'


class Post(db.Model):
    """文章模型"""
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # 外键（多对一：多篇文章属于一个用户）
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f'<Post {self.title}>'
```

**创建数据库表：**

```python
# 在应用上下文中创建表
with app.app_context():
    db.create_all()  # 创建所有表
    # db.drop_all()  # 删除所有表
```

---

### 26.12 CRUD 操作

#### 概念说明

数据库的四种基本操作：Create（创建）、Read（读取）、Update（更新）、Delete（删除）。

**Create 创建：**

```python
# 创建单个对象
user = User(username='张三', email='zhangsan@example.com', password_hash='hashed_pwd')
db.session.add(user)
db.session.commit()

# 创建多个对象
users = [
    User(username='李四', email='lisi@example.com', password_hash='hash1'),
    User(username='王五', email='wangwu@example.com', password_hash='hash2')
]
db.session.add_all(users)
db.session.commit()
```

**Read 读取：**

```python
# 根据主键查询
user = User.query.get(1)           # 返回单个对象或 None
user = User.query.get_or_404(1)    # 不存在则返回 404

# 根据条件查询
users = User.query.filter_by(username='张三').all()
users = User.query.filter(User.email.like('%@gmail.com')).all()

# 链式查询
users = User.query.filter_by(role='admin').order_by(User.created_at.desc()).limit(10).all()

# 计数
count = User.query.count()

# 分页
page = User.query.paginate(page=1, per_page=20, error_out=False)
for user in page.items:
    print(user.username)
print(f'总页数：{page.pages}')
```

**Update 更新：**

```python
# 修改单个对象
user = User.query.get(1)
user.email = 'new_email@example.com'
db.session.commit()

# 批量更新
User.query.filter_by(role='guest').update({'role': 'user'})
db.session.commit()
```

**Delete 删除：**

```python
# 删除单个对象
user = User.query.get(1)
db.session.delete(user)
db.session.commit()

# 批量删除
User.query.filter_by(role='banned').delete()
db.session.commit()
```

---

### 26.13 关系定义

#### 概念说明

SQLAlchemy 支持三种关系：一对多、多对一、多对多。

**一对多（One to Many）：**

```python
class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    # 一个作者可以有多篇文章
    posts = db.relationship('Post', backref='author', lazy='dynamic')


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'))


# 使用
author = Author.query.get(1)
posts = author.posts.all()  # 获取作者所有文章

post = Post.query.get(1)
author = post.author  # 获取文章作者
```

**多对多（Many to Many）：**

```python
# 关联表
post_tags = db.Table('post_tags',
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'))
)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    # 一篇文章可以有多个标签
    tags = db.relationship('Tag', secondary=post_tags, backref='posts')


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))


# 使用
post = Post.query.get(1)
post.tags.append(Tag.query.filter_by(name='Python').first())
db.session.commit()

tag_names = [tag.name for tag in post.tags]
```

---

### 26.14 数据库迁移（Flask-Migrate）

#### 概念说明

当模型变更时，Flask-Migrate 可以自动跟踪并应用数据库结构变更。

**安装与配置：**

```bash
uv add flask-migrate
```

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# 定义模型...
class User(db.Model):
    ...
```

**迁移命令：**

```bash
# 初始化迁移仓库（只需执行一次）
uv run flask db init

# 创建迁移脚本（每次模型变更后执行）
uv run flask db migrate -m "添加用户模型"

# 应用迁移
uv run flask db upgrade

# 回滚迁移
uv run flask db downgrade
```

---

## 第四部分：用户认证

### 26.15 Flask-Login 简介

#### 概念说明

Flask-Login 提供了用户会话管理功能，处理用户登录、登出、记住我等功能。

**安装与配置：**

```bash
uv add flask-login
```

```python
from flask import Flask
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'  # 登录页面端点
login_manager.login_message = '请先登录'
```

---

### 26.16 UserMixin 与用户加载

#### 概念说明

UserMixin 提供了 Flask-Login 所需的四个属性和方法。

**用户模型：**

```python
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String(256))

    def set_password(self, password):
        """设置密码哈希"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """验证密码"""
        return check_password_hash(self.password_hash, password)


# 用户加载回调
@login_manager.user_loader
def load_user(user_id):
    """根据用户 ID 加载用户"""
    return User.query.get(int(user_id))
```

---

### 26.17 登录/登出

#### 概念说明

使用 `login_user()` 和 `logout_user()` 管理用户会话。

**登录视图：**

```python
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = request.form.get('remember', False)

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user, remember=remember)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('index'))
        else:
            flash('用户名或密码错误', 'error')

    return render_template('auth/login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
```

**登录保护：**

```python
# 使用装饰器保护路由
@auth_bp.route('/profile')
@login_required
def profile():
    return render_template('auth/profile.html')


# 在模板中检查登录状态
{% if current_user.is_authenticated %}
    <p>欢迎，{{ current_user.username }}！</p>
    <a href="{{ url_for('auth.logout') }}">退出</a>
{% else %}
    <a href="{{ url_for('auth.login') }}">登录</a>
{% endif %}
```

---

## 本章小结

```
┌─────────────────────────────────────────────────────────────┐
│                      第 26 章 知识要点                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   Jinja2 模板：                                              │
│   ✓ 变量：{{ variable }}、{{ obj.attr }}                    │
│   ✓ 过滤器：upper、lower、default、join、truncate           │
│   ✓ 控制：if/elif/else、for/else、loop 变量                 │
│   ✓ 继承：{% extends %}、{% block %}、{{ super() }}          │
│   ✓ 宏：{% macro %}、{% import %}、{% from ... import %}     │
│                                                             │
│   蓝图：                                                     │
│   ✓ 创建：Blueprint('name', __name__)                       │
│   ✓ 注册：app.register_blueprint(bp, url_prefix='/xxx')     │
│   ✓ 端点：蓝图名。函数名（如 auth.login）                    │
│   ✓ 工厂模式：create_app() 函数、多环境支持                  │
│                                                             │
│   Flask-SQLAlchemy：                                         │
│   ✓ 模型：db.Model、db.Column、主键、外键                   │
│   ✓ 关系：一对多、多对多、backref、secondary                │
│   ✓ CRUD：add()、commit()、query、delete()                  │
│   ✓ 迁移：flask db init/migrate/upgrade                     │
│                                                             │
│   Flask-Login：                                              │
│   ✓ 配置：LoginManager、user_loader 回调                    │
│   ✓ UserMixin：提供 is_authenticated 等属性                  │
│   ✓ 登录：login_user()、logout_user()                       │
│   ✓ 保护：@login_required 装饰器                            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```
---

[← 上一篇](./02-Flask快速上手.md) | [下一篇 →](./04-Flask高级.md)
