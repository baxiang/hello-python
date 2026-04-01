# Flask 蓝图 Blueprint

掌握 Flask 蓝图实现模块化应用。

---

## 1. 蓝图基础

### 1.1 什么是蓝图？

蓝图（Blueprint）是 Flask 中用于组织大型应用的结构，将路由、视图、模板等分组管理。

### 1.2 创建蓝图

```python
# app/blueprints/users.py
from flask import Blueprint

# 创建蓝图
users_bp = Blueprint('users', __name__, url_prefix='/users')

# 定义路由
@users_bp.route('/')
def index():
    return '用户列表'

@users_bp.route('/<int:user_id>')
def profile(user_id):
    return f'用户 {user_id} 的资料'
```

### 1.3 注册蓝图

```python
# app/main.py
from flask import Flask
from app.blueprints.users import users_bp
from app.blueprints.posts import posts_bp

app = Flask(__name__)
app.register_blueprint(users_bp)
app.register_blueprint(posts_bp)
```

---

## 2. 蓝图结构

### 2.1 目录结构

```
app/
├── __init__.py
├── main.py
├── blueprints/
│   ├── __init__.py
│   ├── users.py
│   ├── posts.py
│   └── admin.py
├── templates/
│   ├── users/
│   │   └── index.html
│   └── posts/
│       └── index.html
└── static/
```

### 2.2 完整蓝图示例

```python
# app/blueprints/posts.py
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from app.models import Post, db

# 创建蓝图
posts_bp = Blueprint('posts', __name__, 
                   url_prefix='/posts',
                   template_folder='../templates/posts')

# 路由
@posts_bp.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.created_at.desc()).paginate(
        page=page, per_page=20
    )
    return render_template('posts/index.html', posts=posts)

@posts_bp.route('/<int:post_id>')
def view(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('posts/view.html', post=post)

@posts_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        
        post = Post(
            title=title,
            content=content,
            author_id=current_user.id
        )
        db.session.add(post)
        db.session.commit()
        
        return redirect(url_for('posts.view', post_id=post.id))
    
    return render_template('posts/create.html')
```

---

## 3. 蓝图资源

### 3.1 静态文件

```python
# 创建蓝图时指定静态文件夹
admin_bp = Blueprint('admin', __name__, 
                   url_prefix='/admin',
                   static_folder='static',
                   static_url_path='/admin/static')
```

### 3.2 模板

```python
# 在蓝图中渲染模板
@posts_bp.route('/')
def index():
    # 相对于蓝图的 template_folder 查找
    return render_template('posts/index.html')
```

---

## 4. 蓝图钩子

### 4.1 错误处理

```python
@posts_bp.errorhandler(404)
def post_not_found(e):
    return render_template('posts/404.html'), 404

@posts_bp.errorhandler(500)
def server_error(e):
    return render_template('posts/500.html'), 500
```

### 4.2 请求处理

```python
@posts_bp.before_request
def check_user_status():
    # 每个请求前检查
    pass

@posts_bp.after_request
def add_header(response):
    response.headers['X-Posts-Blueprint'] = 'true'
    return response
```

---

## 5. 完整示例

### 5.1 用户模块

```python
# app/blueprints/users.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import User, db
from app.utils.decorators import admin_required

users_bp = Blueprint('users', __name__, url_prefix='/users')

@users_bp.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    users = User.query.paginate(page=page, per_page=20)
    return render_template('users/index.html', users=users)

@users_bp.route('/<int:user_id>')
def profile(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('users/profile.html', user=user)

@users_bp.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        current_user.bio = request.form.get('bio')
        current_user.location = request.form.get('location')
        db.session.commit()
        flash('设置已保存', 'success')
        return redirect(url_for('users.settings'))
    
    return render_template('users/settings.html')

@users_bp.route('/admin')
@admin_required
def admin_panel():
    return render_template('users/admin.html')
```

### 5.2 注册多个蓝图

```python
# app/__init__.py
from flask import Flask

def create_app():
    app = Flask(__name__)
    
    # 注册蓝图
    from app.blueprints.users import users_bp
    from app.blueprints.posts import posts_bp
    from app.blueprints.admin import admin_bp
    
    app.register_blueprint(users_bp)
    app.register_blueprint(posts_bp)
    app.register_blueprint(admin_bp)
    
    return app
```

---

## 总结

| 知识点 | 说明 |
|---------|------|
| Blueprint | 创建蓝图 |
| url_prefix | URL 前缀 |
| template_folder | 模板文件夹 |
| 错误处理 | 蓝图级别错误处理 |
| 请求钩子 | before/after request |

---

[← 上一章](./Flask/05-Flask文件上传下载.md) | [下一章](./Flask/07-Flask认证授权.md)