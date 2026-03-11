# 第 5 章：Flask 进阶

深入学习 Flask 数据库集成、ORM 和蓝图。

---

## 本章目标

- 掌握 SQLAlchemy ORM
- 理解数据库模型设计
- 学会使用 Flask-SQLAlchemy
- 掌握蓝图（Blueprint）实现模块化
- 理解 Flask 上下文

---

## 5.1 数据库集成

### 安装依赖

```bash
pip install flask-sqlalchemy pymysql
```

### 配置数据库

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# 配置 SQLite 数据库
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'

# 配置 MySQL 数据库
# app.config['SQLALCHEMY_DATABASE_URI'] = \
#     'mysql+pymysql://username:password@localhost/dbname'

# 其他配置
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭修改追踪
app.config['SQLALCHEMY_ECHO'] = True  # 打印 SQL 语句

db = SQLAlchemy(app)
```

---

## 5.2 数据模型

### 定义模型

```python
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)

class User(db.Model):
    """用户表"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    # 关系
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat()
        }


class Post(db.Model):
    """文章表"""
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    slug = db.Column(db.String(200), unique=True)
    published = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 外键
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # 关系
    comments = db.relationship('Comment', backref='post', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Post {self.title}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'author': self.author.username,
            'created_at': self.created_at.isoformat()
        }


class Comment(db.Model):
    """评论表"""
    __tablename__ = 'comments'
    
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 外键
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    def __repr__(self):
        return f'<Comment {self.id}>'
```

### 创建表

```python
# 在 Flask 应用上下文中执行
with app.app_context():
    db.create_all()
    print("数据库表创建成功")
```

---

## 5.3 CRUD 操作

### 创建数据

```python
# 创建用户
new_user = User(
    username='john',
    email='john@example.com',
    password_hash='hashed_password'
)
db.session.add(new_user)
db.session.commit()

# 批量创建
users = [
    User(username='alice', email='alice@example.com', password_hash='hash1'),
    User(username='bob', email='bob@example.com', password_hash='hash2'),
]
db.session.add_all(users)
db.session.commit()
```

### 读取数据

```python
# 根据 ID 查询
user = User.query.get(1)

# 根据条件查询
user = User.query.filter_by(username='john').first()
users = User.query.filter(User.email.like('%@example.com')).all()

# 排序
users = User.query.order_by(User.created_at.desc()).all()

# 分页
page = User.query.paginate(page=1, per_page=20)
items = page.items
total = page.total

# 计数
count = User.query.count()

# 链式调用
active_users = User.query.filter_by(is_active=True).order_by(User.created_at.desc()).limit(10).all()
```

### 更新数据

```python
user = User.query.get(1)
user.email = 'newemail@example.com'
db.session.commit()

# 批量更新
User.query.filter_by(is_active=False).update({'is_active': True})
db.session.commit()
```

### 删除数据

```python
user = User.query.get(1)
db.session.delete(user)
db.session.commit()

# 批量删除
User.query.filter_by(is_active=False).delete()
db.session.commit()
```

---

## 5.4 蓝图（Blueprint）

### 什么是蓝图？

蓝图用于将应用分割成模块，实现代码组织和复用。

### 创建蓝图

```python
# admin/__init__.py
from flask import Blueprint

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

from . import routes
```

```python
# admin/routes.py
from . import admin_bp

@admin_bp.route('/')
def index():
    return 'Admin Dashboard'

@admin_bp.route('/users')
def users():
    return 'User Management'

@admin_bp.route('/settings')
def settings():
    return 'Settings'
```

```python
# blog/__init__.py
from flask import Blueprint

blog_bp = Blueprint('blog', __name__, url_prefix='/blog')

from . import routes
```

```python
# blog/routes.py
from . import blog_bp
from flask import render_template

@blog_bp.route('/')
def index():
    return 'Blog Index'

@blog_bp.route('/post/<int:post_id>')
def post(post_id):
    return f'Blog Post {post_id}'
```

### 注册蓝图

```python
from flask import Flask
from admin import admin_bp
from blog import blog_bp

app = Flask(__name__)
app.register_blueprint(admin_bp)
app.register_blueprint(blog_bp)

# 访问路径:
# /admin/
# /admin/users
# /blog/
# /blog/post/1
```

---

## 5.5 Flask 上下文

### 应用上下文

```python
# 手动推送上下文
with app.app_context():
    user = User.query.first()
    print(user.username)

# 获取当前应用
from flask import current_app
@app.route('/app-name')
def app_name():
    return current_app.name
```

### 请求上下文

```python
# 手动推送请求上下文
with app.test_request_context('/hello', method='GET'):
    from flask import request
    print(request.path)

# 测试客户端
with app.test_client() as client:
    response = client.get('/')
    print(response.status_code)
    print(response.data)
```

---

## 5.6 实战：博客系统后端

```python
# app.py
from flask import Flask, render_template, request, redirect, url_for, flash, abort
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ==================== 模型定义 ====================
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    posts = db.relationship('Post', backref='author', lazy='dynamic')

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    slug = db.Column(db.String(200), unique=True)
    published = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# ==================== 路由 ====================
@app.route('/')
def index():
    posts = Post.query.filter_by(published=True).order_by(Post.created_at.desc()).all()
    return render_template('index.html', posts=posts)

@app.route('/post/<slug>')
def post(slug):
    post = Post.query.filter_by(slug=slug).first_or_404()
    return render_template('post.html', post=post)

@app.route('/post/new', methods=['GET', 'POST'])
def new_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        slug = request.form.get('slug') or title.lower().replace(' ', '-')
        
        # 简单的作者（实际应从登录获取）
        author = User.query.first()
        if not author:
            author = User(username='admin', email='admin@example.com', password_hash='x')
            db.session.add(author)
            db.session.commit()
        
        post = Post(title=title, content=content, slug=slug, author_id=author.id)
        db.session.add(post)
        db.session.commit()
        
        flash('文章创建成功！')
        return redirect(url_for('index'))
    
    return render_template('edit_post.html', post=None)

@app.route('/post/<int:post_id>/edit', methods=['GET', 'POST'])
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    
    if request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['content']
        post.updated_at = datetime.utcnow()
        db.session.commit()
        
        flash('文章更新成功！')
        return redirect(url_for('post', slug=post.slug))
    
    return render_template('edit_post.html', post=post)

@app.route('/post/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('文章已删除！')
    return redirect(url_for('index'))

# ==================== 初始化 ====================
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
```

---

## 本章总结

### 学到的技能

| 技能 | 说明 |
|------|------|
| SQLAlchemy | ORM 框架 |
| 数据模型 | 表关系设计 |
| CRUD 操作 | 增删改查 |
| 蓝图 | 模块化组织 |
| 上下文 | 应用和请求上下文 |

### 下一步

在 [第 6 章](./06-Flask 高级.md) 中，我们将学习 Flask 高级内容，包括认证、缓存和异步任务。

---

[← 上一章](./04-Flask 入门.md) | [下一章 →](./06-Flask 高级.md)