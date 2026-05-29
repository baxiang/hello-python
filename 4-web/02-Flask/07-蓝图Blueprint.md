# 07-蓝图Blueprint

> Python 3.11+

本章讲解 Flask 蓝图实现模块化应用组织。

---

## 概念铺垫

蓝图（Blueprint）是 Flask 中组织大型应用的模块化机制，采用延迟注册（Deferred Registration）模式。蓝图创建时不立即注册路由，而是在 `app.register_blueprint()` 时才将所有路由、错误处理器、请求钩子注入到应用的 `url_map` 中。endpoint 使用命名空间隔离（`蓝图名.函数名`）避免路由名称冲突。

---

### L1 理解层：会用

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

### L2 实践层：用好

| 做法 | 原因 | 示例 |
|------|------|------|
| 蓝图按业务模块拆分 | 代码可维护 | `users_bp`、`posts_bp`、`admin_bp` |
| `url_prefix` 统一 URL 前缀 | 避免路由冲突 | `Blueprint("users", url_prefix="/users")` |
| 蓝图级错误处理器 | 不同模块不同错误页面 | `@api_bp.errorhandler(404)` |
| 使用 `url_for("蓝图.视图")` 跨蓝图引用 | endpoint 命名空间隔离 | `url_for("admin.dashboard")` |
| 蓝图内用 `.视图` 简写 | 省略蓝图前缀 | `url_for(".index")` |

#### 反模式

```python
# ❌ 错误：所有路由放在一个文件
@app.route("/users/...")
@app.route("/posts/...")
@app.route("/admin/...")

# ✅ 正确：用蓝图拆分
# users_bp = Blueprint("users", __name__, url_prefix="/users")
# posts_bp = Blueprint("posts", __name__, url_prefix="/posts")
# app.register_blueprint(users_bp)
# app.register_blueprint(posts_bp)
```

#### 蓝图 vs 应用级路由

| 场景 | 推荐方式 |
|------|---------|
| 简单应用（<5 路由） | 应用级路由足够 |
| 中型应用（5-20 路由） | 开始考虑蓝图 |
| 大型应用（>20 路由） | 必须使用蓝图 |

---

### L3 专家层：深入

## 第六部分：L3 专家层

### 6.1 Blueprint 的注册流程（延迟注册模式）

Flask Blueprint 采用延迟注册（Deferred Registration）模式：蓝图创建时不立即注册路由，而是在 `app.register_blueprint()` 时才将所有路由、错误处理器、请求钩子"注入"到应用。

**注册流程：**

```
  创建 Blueprint                注册 Blueprint
  +-----------------+          +------------------+
  | Blueprint()     |          | register_bp()    |
  |                 |          |                  |
  | - 记录路由装饰器 |          | 1. 合并 url_prefix|
  | - 记录 error_handler|       | 2. 注册所有路由   |
  | - 记录 before/after|       | 3. 注册错误处理器  |
  | - 记录静态文件配置|         | 4. 注册请求钩子   |
  +--------+--------+          +--------+---------+
           |                            |
           |  路由/处理器暂存            |  规则映射到 app.url_map
           v                            v
  +-----------------+          +------------------+
  | deferred_functions|         | app.view_functions|
  | (延迟函数列表)   |------->  | app.url_map      |
  +-----------------+          | app.before_request|
                               +------------------+
```

```python
from typing import Callable, Any
from flask import Flask, Blueprint

class BlueprintInternals:
    """蓝图内部机制的简化演示"""
    
    def __init__(self, name: str, url_prefix: str | None = None) -> None:
        self.name: str = name
        self.url_prefix: str | None = url_prefix
        self.deferred_functions: list[Callable] = []
        self._view_functions: dict[str, Callable] = {}
    
    def record(self, func: Callable) -> None:
        """记录延迟函数（路由装饰器调用时触发）"""
        self.deferred_functions.append(func)
    
    def register(self, app: Flask, options: dict[str, Any]) -> None:
        """注册蓝图到应用"""
        # 合并 url_prefix
        url_prefix: str | None = options.get("url_prefix", self.url_prefix)
        
        # 执行所有延迟函数（将路由规则注册到 app）
        for deferred_func in self.deferred_functions:
            deferred_func(app, url_prefix, options)

# 使用演示
def demo_registration() -> None:
    bp: BlueprintInternals = BlueprintInternals("users", "/users")
    
    # @bp.route("/") 底层调用的是 bp.record()
    def register_index(app: Flask, prefix: str | None, opts: dict) -> None:
        rule: str = (prefix or "") + "/"
        # app.add_url_rule(rule, view_func=index_view)
    
    bp.record(register_index)
    
    # 此时路由还未注册，直到调用 bp.register(app)
    # bp.register(app_instance)
```

**关键机制：**
- `@blueprint.route()` 不是直接调用 `app.add_url_rule()`，而是将注册逻辑包装为函数存入 `deferred_functions`
- 注册时可覆盖蓝图默认配置：`app.register_blueprint(bp, url_prefix="/v2/users")`
- 蓝图可以嵌套注册：蓝图 A 可以注册蓝图 B

### 6.2 url_for 的 endpoint 解析机制

`url_for()` 通过 endpoint 名称反向生成 URL，其解析涉及蓝图的命名空间（namespace）机制。

**Endpoint 命名规则：**

```
  蓝图内定义:
    @users_bp.route("/profile")          → endpoint = "users.profile"
    @users_bp.route("/<int:id>")         → endpoint = "users.profile_detail"
  
  蓝图外（应用级）:
    @app.route("/")                       → endpoint = "index"
  
  url_for 解析:
    url_for("users.profile")             → "/users/profile"
    url_for("users.profile_detail", id=5)→ "/users/5"
    url_for("index")                     → "/"
```

```python
from typing import Callable
from werkzeug.routing import Map, Rule

class EndpointResolver:
    """简化版 url_for 解析器"""
    
    def __init__(self) -> None:
        self.url_map: Map = Map()
        self.view_functions: dict[str, Callable] = {}
    
    def add_rule(self, rule: str, endpoint: str, view_func: Callable) -> None:
        self.url_map.add(Rule(rule, endpoint=endpoint))
        self.view_functions[endpoint] = view_func
    
    def url_for(self, endpoint: str, **values: Any) -> str:
        """反向解析 endpoint 到 URL"""
        # 1. 精确匹配
        if endpoint in self.view_functions:
            rule = self._find_rule(endpoint)
            return self._build_url(rule, values)
        
        # 2. 带蓝图前缀的匹配（当前蓝图内可省略前缀）
        # 假设当前在 users 蓝图中
        blueprint_name: str = endpoint.split(".")[0] if "." in endpoint else ""
        qualified: str = f"{blueprint_name}.{endpoint}" if "." not in endpoint else endpoint
        
        if qualified in self.view_functions:
            rule = self._find_rule(qualified)
            return self._build_url(rule, values)
        
        raise ValueError(f"No endpoint found: {endpoint}")
    
    def _find_rule(self, endpoint: str) -> Rule:
        for rule in self.url_map.iter_rules():
            if rule.endpoint == endpoint:
                return rule
        raise ValueError(f"No rule for endpoint: {endpoint}")
    
    def _build_url(self, rule: Rule, values: dict[str, Any]) -> str:
        # 简化实现：实际使用 Werkzeug 的 URL 构建逻辑
        url: str = rule.rule
        for key, val in values.items():
            url = url.replace(f"<{key}>", str(val))
        return url
```

**设计要点：**

| 特性 | 说明 | 示例 |
|------|------|------|
| 命名空间隔离 | 蓝图自动添加 `blueprint_name.` 前缀 | `users.profile` |
| 跨蓝图引用 | 必须使用完整 endpoint | `url_for("admin.dashboard")` |
| 蓝图内引用 | 可省略蓝图前缀（同蓝图内） | `url_for(".profile")`（`. ` 表示当前蓝图） |
| 应用级路由 | 无前缀 | `url_for("index")` |

### 6.3 Blueprint 的 before_request 执行顺序

当应用有多个蓝图且每个蓝图有自己的 `before_request` 钩子时，执行顺序是一个关键概念。

**执行顺序：**

```
  请求到达
     |
     v
  +--------------------------------+
  | app.before_request (应用级)     |  ← 所有请求都会执行
  +--------------------------------+
     |
     v
  +--------------------------------+
  | Blueprint A.before_request     |  ← 按注册顺序执行
  +--------------------------------+
     |
     v
  +--------------------------------+
  | Blueprint B.before_request     |  ← 仅匹配当前请求的蓝图
  +--------------------------------+
     |
     v
  +--------------------------------+
  | 视图函数 (View Function)        |
  +--------------------------------+
     |
     v
  +--------------------------------+
  | Blueprint B.after_request      |  ← 逆序执行
  +--------------------------------+
     |
     v
  +--------------------------------+
  | Blueprint A.after_request      |
  +--------------------------------+
     |
     v
  +--------------------------------+
  | app.after_request (应用级)      |
  +--------------------------------+
```

```python
from flask import Flask, Blueprint, request, g
from typing import Any

def demonstrate_hook_order() -> None:
    app: Flask = Flask(__name__)
    
    auth_bp: Blueprint = Blueprint("auth", __name__, url_prefix="/auth")
    api_bp: Blueprint = Blueprint("api", __name__, url_prefix="/api")
    
    execution_log: list[str] = []
    
    @app.before_request
    def app_before() -> None:
        execution_log.append("app.before_request")
        g.start_time: Any = request.environ.get("werkzeug.request.start_time")
    
    @auth_bp.before_request
    def auth_before() -> None:
        execution_log.append("auth_bp.before_request")
    
    @api_bp.before_request
    def api_before() -> None:
        execution_log.append("api_bp.before_request")
    
    # 请求 /api/data 时:
    # execution_log = ["app.before_request", "api_bp.before_request"]
    # 注意：auth_bp.before_request 不会执行，因为请求不属于 auth 蓝图
```

**关键规则：**

| 规则 | 说明 |
|------|------|
| 应用级钩子 | 对所有请求执行，无论路由属于哪个蓝图 |
| 蓝图钩子 | 仅当请求匹配该蓝图的路由时执行 |
| 执行顺序 | app.before → 蓝图.before → 视图 → 蓝图.after → app.after |
| 多蓝图注册顺序 | 按 `app.register_blueprint()` 的调用顺序 |
| 短路行为 | `before_request` 返回 Response 则跳过后续钩子和视图 |

### 6.4 知识关联

```
                    Blueprint 知识体系
                         |
        +----------------+----------------+
        |                |                |
     创建层          注册层          运行时
        |                |                |
   +----+----+      +----+----+      +----+----+
   | 蓝图定义 |      | 延迟注册 |      | 请求钩子 |
   | 路由装饰 |      | url_prefix|     | endpoint |
   +----+----+      +----+----+      +----+----+
        |                |                |
        v                v                v
   +---------+      +---------+      +---------+
   | 静态文件 |      | 路由注入 |      | url_for |
   | 模板目录 |      | url_map  |      | 解析    |
   +---------+      +---------+      +---------+
                         |
                         v
                   +-----+-----+
                   | 执行顺序   |
                   | before_req|
                   +-----+-----+
                         |
                   +-----+-----+      +---------+
                   | 应用级   |<---->| 蓝图级   |
                   | 全局钩子 |      | 局部钩子 |
                   +---------+      +---------+
```

| 知识点 | 说明 |
|---------|------|
| Blueprint | 创建蓝图 |
| url_prefix | URL 前缀 |
| template_folder | 模板文件夹 |
| 错误处理 | 蓝图级别错误处理 |
| 请求钩子 | before/after request |