# 蓝图 Blueprint（详细版）

> Python 3.11+

本章讲解 Flask 蓝图实现模块化应用组织。

---

## 第一部分：蓝图基础

### 1.1 实际场景

你的 Flask 应用变得越来越大，有用户模块、文章模块、评论模块、后台管理模块等。所有路由都写在一个文件里，维护困难。

**问题：如何将大型应用拆分成多个模块？**

### 1.2 什么是蓝图？

蓝图（Blueprint）是 Flask 中用于组织大型应用的结构，将路由、视图、模板等分组管理。

### 1.3 创建蓝图

```python
# app/blueprints/users.py
from flask import Blueprint

# 创建蓝图
users_bp: Blueprint = Blueprint("users", __name__, url_prefix="/users")

# 定义路由
@users_bp.route("/")
def index() -> str:
    return "用户列表"

@users_bp.route("/<int:user_id>")
def profile(user_id: int) -> str:
    return f"用户 {user_id} 的资料"
```

### 1.4 注册蓝图

```python
# app/main.py
from flask import Flask
from app.blueprints.users import users_bp
from app.blueprints.posts import posts_bp

app: Flask = Flask(__name__)
app.register_blueprint(users_bp)
app.register_blueprint(posts_bp)
```

---

## 第二部分：蓝图结构

### 2.1 实际场景

每个蓝图模块有自己的模板和静态文件，需要合理的目录组织。

**问题：如何组织蓝图的项目结构？**

### 2.2 目录结构

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

### 2.3 完整蓝图示例

```python
# app/blueprints/posts.py
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from app.models import Post, db

# 创建蓝图
posts_bp: Blueprint = Blueprint(
    "posts", __name__,
    url_prefix="/posts",
    template_folder="../templates/posts"
)

# 路由
@posts_bp.route("/")
def index() -> str:
    page: int = request.args.get("page", 1, type=int)
    posts = Post.query.order_by(Post.created_at.desc()).paginate(
        page=page, per_page=20
    )
    return render_template("posts/index.html", posts=posts)

@posts_bp.route("/<int:post_id>")
def view(post_id: int) -> str:
    post: Post = Post.query.get_or_404(post_id)
    return render_template("posts/view.html", post=post)

@posts_bp.route("/create", methods=["GET", "POST"])
@login_required
def create() -> str:
    if request.method == "POST":
        title: str = request.form.get("title", "")
        content: str = request.form.get("content", "")
        
        post: Post = Post(
            title=title,
            content=content,
            author_id=current_user.id
        )
        db.session.add(post)
        db.session.commit()
        
        return redirect(url_for("posts.view", post_id=post.id))
    
    return render_template("posts/create.html")
```

---

## 第三部分：蓝图资源

### 3.1 实际场景

后台管理模块有自己专属的 CSS 样式和 JavaScript 文件，不应该和其他模块混在一起。

**问题：如何为蓝图配置独立的静态文件和模板？**

### 3.2 静态文件

```python
# 创建蓝图时指定静态文件夹
admin_bp: Blueprint = Blueprint(
    "admin", __name__,
    url_prefix="/admin",
    static_folder="static",
    static_url_path="/admin/static"
)
```

### 3.3 模板

```python
# 在蓝图中渲染模板
@posts_bp.route("/")
def index() -> str:
    # 相对于蓝图的 template_folder 查找
    return render_template("posts/index.html")
```

---

## 第四部分：蓝图钩子

### 4.1 实际场景

文章模块的所有请求都需要检查权限，所有响应都需要添加特定的响应头。

**问题：如何在蓝图级别添加请求处理钩子？**

### 4.2 错误处理

```python
@posts_bp.errorhandler(404)
def post_not_found(e: Exception) -> tuple[str, int]:
    return render_template("posts/404.html"), 404

@posts_bp.errorhandler(500)
def server_error(e: Exception) -> tuple[str, int]:
    return render_template("posts/500.html"), 500
```

### 4.3 请求处理

```python
from flask import Response

@posts_bp.before_request
def check_user_status() -> None:
    # 每个请求前检查
    pass

@posts_bp.after_request
def add_header(response: Response) -> Response:
    response.headers["X-Posts-Blueprint"] = "true"
    return response
```

---

## 第五部分：完整示例

### 5.1 用户模块

```python
# app/blueprints/users.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import User, db

users_bp: Blueprint = Blueprint("users", __name__, url_prefix="/users")

@users_bp.route("/")
def index() -> str:
    page: int = request.args.get("page", 1, type=int)
    users = User.query.paginate(page=page, per_page=20)
    return render_template("users/index.html", users=users)

@users_bp.route("/<int:user_id>")
def profile(user_id: int) -> str:
    user: User = User.query.get_or_404(user_id)
    return render_template("users/profile.html", user=user)

@users_bp.route("/settings", methods=["GET", "POST"])
@login_required
def settings() -> str:
    if request.method == "POST":
        current_user.bio = request.form.get("bio", "")
        current_user.location = request.form.get("location", "")
        db.session.commit()
        flash("设置已保存", "success")
        return redirect(url_for("users.settings"))
    
    return render_template("users/settings.html")
```

### 5.2 注册多个蓝图

```python
# app/__init__.py
from flask import Flask

def create_app() -> Flask:
    app: Flask = Flask(__name__)
    
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