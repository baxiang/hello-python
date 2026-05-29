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

---

## 第七部分：蓝图模板与静态文件独立配置

### 7.1 实际场景

后台管理蓝图需要自己专属的 CSS/JS 样式和模板，不应该和其他蓝图混在一起。

**问题：如何为蓝图配置独立的模板目录和静态文件目录？**

### 7.2 逐蓝图配置模板和静态文件

```python
# app/blueprints/admin.py
from flask import Blueprint, render_template, url_for

admin_bp: Blueprint = Blueprint(
    "admin",
    __name__,
    url_prefix="/admin",
    template_folder="templates",        # 相对路径，相对于 admin.py 所在目录
    static_folder="static",             # 静态文件目录
    static_url_path="/admin/static"     # URL 访问路径
)

@admin_bp.route("/")
def dashboard() -> str:
    # 优先查找 admin 蓝图的 template_folder
    return render_template("admin/dashboard.html")

@admin_bp.route("/login")
def login() -> str:
    return render_template("admin/login.html")
```

```
目录结构：
app/
├── blueprints/
│   ├── admin/
│   │   ├── __init__.py
│   │   ├── views.py         ← admin_bp 定义在此
│   │   ├── templates/       ← 蓝图专属模板目录
│   │   │   └── admin/
│   │   │       ├── dashboard.html
│   │   │       └── login.html
│   │   └── static/           ← 蓝图专属静态文件
│   │       ├── css/
│   │       │   └── admin.css
│   │       └── js/
│   │           └── admin.js
│   └── users/
│       ├── views.py
│       └── templates/
│           └── users/
│               └── profile.html
```

### 7.3 模板查找优先级

Flask 渲染模板时的查找顺序：

```
模板查找优先级（render_template("admin/dashboard.html")）：
┌─────────────────────────────────────────────────────────────┐
│  1. 蓝图专属 template_folder（高优先级）                      │
│     app/blueprints/admin/templates/admin/dashboard.html      │
│       ↓ 未找到                                              │
│  2. 应用全局 templates 目录                                   │
│     app/templates/admin/dashboard.html                       │
│       ↓ 未找到                                              │
│  3. 其他已注册蓝图的 template_folder（不可靠，不推荐依赖）     │
│       ↓ 未找到                                              │
│  4. 抛出 TemplateNotFound 异常                               │
└─────────────────────────────────────────────────────────────┘
```

### 7.4 静态文件 URL 冲突解决

```python
# 场景：两个蓝图都提供 static/style.css，如何区分？

# 蓝图 A（用户模块）
users_bp = Blueprint(
    "users", __name__,
    url_prefix="/users",
    static_folder="static",
    static_url_path="/users/static"   # 自定义 URL 路径，避免冲突
)

# 蓝图 B（后台管理模块）
admin_bp = Blueprint(
    "admin", __name__,
    url_prefix="/admin",
    static_folder="static",
    static_url_path="/admin/static"   # 不同的 URL 路径
)

# 模板中引用：
# <link href="{{ url_for('users.static', filename='css/style.css') }}" rel="stylesheet">
# <link href="{{ url_for('admin.static', filename='css/style.css') }}" rel="stylesheet">
```

---

## 第八部分：应用工厂模式与蓝图

### 8.1 实际场景

测试时需要创建不同配置的 Flask 应用实例，把应用创建封装成工厂函数。

**问题：如何用工厂模式组织蓝图注册？**

### 8.2 渐进式工厂模式

#### 最简工厂（入门）

```python
# app/__init__.py
from flask import Flask

def create_app() -> Flask:
    app: Flask = Flask(__name__)
    app.config["SECRET_KEY"] = "dev"

    from app.blueprints.users import users_bp
    from app.blueprints.posts import posts_bp

    app.register_blueprint(users_bp)
    app.register_blueprint(posts_bp)

    return app
```

#### 进阶工厂（环境区分）

```python
# app/__init__.py
import os
from flask import Flask
from typing import Any

def create_app(config_name: str | None = None) -> Flask:
    if config_name is None:
        config_name = os.environ.get("FLASK_ENV", "development")

    app: Flask = Flask(__name__)

    from app.config import config_map
    config_cls: Any = config_map.get(config_name, config_map["default"])
    app.config.from_object(config_cls)

    from app.extensions import db, migrate, login_manager
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    register_blueprints(app)
    register_commands(app)

    return app

def register_blueprints(app: Flask) -> None:
    """集中管理所有蓝图注册"""
    from app.blueprints.users import users_bp
    from app.blueprints.posts import posts_bp
    from app.blueprints.admin import admin_bp
    from app.api.v1 import api_v1_bp
    from app.api.v2 import api_v2_bp

    app.register_blueprint(users_bp)
    app.register_blueprint(posts_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(api_v1_bp)
    app.register_blueprint(api_v2_bp)

def register_commands(app: Flask) -> None:
    """注册自定义 CLI 命令"""
    from app.commands import seed_db_cmd, init_admin_cmd
    app.cli.add_command(seed_db_cmd)
    app.cli.add_command(init_admin_cmd)
```

#### 生产级工厂（延迟导入、条件注册）

```python
# app/__init__.py
from flask import Flask
import importlib

_BLUEPRINT_MODULES: list[str] = [
    "app.blueprints.users",
    "app.blueprints.posts",
    "app.blueprints.admin",
    "app.api.v1",
    "app.api.v2",
]

def create_app(config_name: str = "production") -> Flask:
    app: Flask = Flask(__name__, instance_relative_config=True)

    app.config.from_object("app.config.default")
    app.config.from_object(f"app.config.{config_name}")
    app.config.from_pyfile("config.py", silent=True)

    for module_path in _BLUEPRINT_MODULES:
        _register_module_blueprint(app, module_path)

    return app

def _register_module_blueprint(app: Flask, module_path: str) -> None:
    """动态导入并注册蓝图模块"""
    try:
        module = importlib.import_module(module_path)
        if hasattr(module, "bp"):
            app.register_blueprint(module.bp)
    except ImportError as e:
        app.logger.warning(f"跳过蓝图模块 {module_path}: {e}")
```

### 8.3 蓝图延迟注册的陷阱

```python
# 场景：在蓝图定义时访问数据库（错误！）
# ❌ 错误：蓝图定义时 app 尚未创建，无法获取配置
from app.models import User  # 可能导入失败（循环引用）

users_bp = Blueprint("users", __name__, url_prefix="/users")

# ❌ 蓝图定义时从配置读取值
admin_email = os.environ.get("ADMIN_EMAIL")  # 静态值，修改环境变量无效
# ✅ 正确：在视图函数或 before_request 中获取
@users_bp.before_request
def set_admin_email() -> None:
    g.admin_email = current_app.config.get("ADMIN_EMAIL")
```

---

## 第九部分：蓝图嵌套与子蓝图

### 9.1 实际场景

后台管理模块包含多个子模块：用户管理、内容管理、系统设置。需要将它们组织成级联蓝图。

**问题：如何实现蓝图的嵌套注册？**

### 9.2 子蓝图实现

```python
# app/blueprints/admin/__init__.py
from flask import Blueprint

# 父蓝图
admin_bp: Blueprint = Blueprint(
    "admin", __name__,
    url_prefix="/admin",
    template_folder="templates"
)

# 子蓝图
from app.blueprints.admin.users import admin_users_bp
from app.blueprints.admin.content import admin_content_bp
from app.blueprints.admin.settings import admin_settings_bp

# 注册子蓝图到父蓝图（注意：不设置 url_prefix，父蓝图已有）
admin_bp.register_blueprint(admin_users_bp)
admin_bp.register_blueprint(admin_content_bp)
admin_bp.register_blueprint(admin_settings_bp)


# app/blueprints/admin/users.py
from flask import Blueprint, render_template

admin_users_bp: Blueprint = Blueprint(
    "admin_users", __name__,
    url_prefix="/users"   # 最终 URL: /admin/users
)

@admin_users_bp.route("/")
def user_list() -> str:
    return render_template("admin/users/list.html")

# endpoint 链：admin.admin_users.user_list
# URL 链：/admin/users/
```

```
URL 映射规则：
┌─────────────────────────────────────────────────────────────┐
│  父蓝图: admin_bp       (url_prefix="/admin")               │
│  ├── 子蓝图: admin_users_bp    (url_prefix="/users")         │
│  │   ├── / (list)         → /admin/users/                   │
│  │   └── /<int:id> (edit) → /admin/users/<id>               │
│  ├── 子蓝图: admin_content_bp  (url_prefix="/content")       │
│  │   └── / (dashboard)    → /admin/content/                 │
│  └── 子蓝图: admin_settings_bp (url_prefix="/settings")      │
│      └── / (config)       → /admin/settings/                │
│                                                              │
│  Endpoint 命名：父蓝图.子蓝图.视图函数名                       │
│  url_for("admin.admin_users.user_list")                     │
│  在 admin_users_bp 内部可用简写：url_for(".user_list")       │
└─────────────────────────────────────────────────────────────┘
```

### 9.3 嵌套蓝图的钩子行为

```python
# 每个蓝图都可以有自己的 before_request / after_request
# 当请求 /admin/users/ 时，钩子执行顺序为：

# 1. app.before_request（应用级）
# 2. admin_bp.before_request（父蓝图）
# 3. admin_users_bp.before_request（子蓝图）
# 4. user_list() 视图函数
# 5. admin_users_bp.after_request（子蓝图）
# 6. admin_bp.after_request（父蓝图）
# 7. app.after_request（应用级）

# 如果任何 before_request 返回 Response，后续钩子和视图都不会执行
```

---

## 第十部分：蓝图注册顺序与 URL 冲突

### 10.1 注册顺序对路由匹配的影响

Flask 的路由匹配按 `app.url_map` 中规则的顺序进行。蓝图的注册顺序影响 URL 匹配优先级。

```python
# 场景：两个蓝图都注册了 "/profile" 路由
users_bp = Blueprint("users", __name__, url_prefix="/users")
vip_bp = Blueprint("vip", __name__, url_prefix="/users")  # 相同前缀！

# 如果都定义了 @xxx_bp.route("/profile")
# 先注册的蓝图匹配 "/users/profile"

# 解决方案：
# 方案一：不同的 url_prefix
# users_bp → /users
# vip_bp   → /vip/users

# 方案二：使用不同的子路径
# @users_bp.route("/profile")
# @vip_bp.route("/profile-vip")

# 方案三：合并到一个蓝图，通过视图逻辑区分
```

### 10.2 运行时检查 URL 冲突

```python
# app/utils.py
from flask import Flask
from werkzeug.routing import Rule
from collections import defaultdict

def detect_url_conflicts(app: Flask) -> None:
    """检测应用中重叠的 URL 路由"""
    rules_by_url: dict[str, list[Rule]] = defaultdict(list)

    for rule in app.url_map.iter_rules():
        rules_by_url[rule.rule].append(rule)

    for url, rules in rules_by_url.items():
        if len(rules) > 1:
            endpoint_names: str = ", ".join(r.endpoint for r in rules)
            app.logger.warning(
                f"URL 冲突: {url} → endpoints: [{endpoint_names}]"
            )

# 在应用启动时调用
# with app.app_context():
#     detect_url_conflicts(app)
```

### 10.3 url_prefix 的陷阱

```python
# 陷阱一：忘记末尾斜杠
@users_bp.route("/profile")  # 蓝图 url_prefix="/users"
# 实际 URL: /users/profile   ← 正确

@users_bp.route("profile")   # 没有前导斜杠
# 实际 URL: /usersprofile    ← 连在一起，不符合预期！

# 陷阱二：url_prefix 重复设置
bp = Blueprint("api", __name__, url_prefix="/api")
app.register_blueprint(bp, url_prefix="/v1")  # 会覆盖蓝图默认的 /api
# 最终 URL: /v1/...  (不是 /api/v1/...)

# 陷阱三：url_prefix 未以 / 开头
bp = Blueprint("api", __name__, url_prefix="api")  # 缺少前导 /
# Flask 会自动补全为 /api，但不要依赖此行为，显式写 / 开头
```

---

## 第十一部分：测试蓝图

### 11.1 实际场景

需要独立测试某个蓝图的路由和逻辑，不依赖完整的应用。

**问题：如何独立测试单个蓝图？**

### 11.2 隔离测试蓝图

```python
# tests/test_users_blueprint.py
import pytest
from flask import Flask
from flask.testing import FlaskClient
from app.blueprints.users import users_bp

@pytest.fixture
def app() -> Flask:
    """创建只包含待测蓝图的轻量应用"""
    app: Flask = Flask(__name__)
    app.config["TESTING"] = True
    app.config["SECRET_KEY"] = "test"
    app.register_blueprint(users_bp)
    return app

@pytest.fixture
def client(app: Flask) -> FlaskClient:
    return app.test_client()

def test_users_index(client: FlaskClient) -> None:
    response = client.get("/users/")
    assert response.status_code == 200

def test_users_profile_not_found(client: FlaskClient) -> None:
    response = client.get("/users/99999")
    assert response.status_code == 404

def test_users_blueprint_endpoints(client: FlaskClient) -> None:
    """测试蓝图中的 endpoint 是否存在"""
    with client.application.app_context():
        from flask import url_for
        assert url_for("users.index") == "/users/"
```

### 11.3 测试带钩子的蓝图

```python
# tests/test_auth_blueprint.py
from unittest.mock import MagicMock, patch
from flask import Flask, g, session
from flask.testing import FlaskClient

@patch("app.blueprints.auth.load_user")
def test_before_request_hook(mock_load_user: MagicMock, client: FlaskClient) -> None:
    """测试蓝图 before_request 钩子的行为"""
    mock_user = MagicMock()
    mock_user.is_authenticated = True
    mock_load_user.return_value = mock_user

    response = client.get("/auth/protected")
    assert response.status_code == 200
    mock_load_user.assert_called_once()
```

---

## 第十二部分：常见坑点排查

### 12.1 蓝图未注册导致 404

**错误信息：**

```
werkzeug.routing.exceptions.BuildError: Could not build url for endpoint 'users.profile'.
Did you mean 'posts.view' instead?
```

**根因分析：**

蓝图已定义但忘记调用 `app.register_blueprint()`，导致路由未注入 `app.url_map`。

**修复步骤：**

1. 检查 `create_app()` 中是否调用了 `app.register_blueprint(users_bp)`
2. 确认 import 语句不会触发循环引用导致 import 失败（静默跳过）
3. 在应用中打印 `app.url_map` 查看已注册的路由

**预防措施：**

```python
# conftest.py 或测试启动脚本
def assert_blueprint_registered(app: Flask, blueprint_name: str) -> None:
    """断言蓝图已注册"""
    blueprints: set[str] = {bp for bp in app.blueprints}
    assert blueprint_name in blueprints, (
        f"蓝图 {blueprint_name} 未注册！已注册的蓝图: {blueprints}"
    )
```

### 12.2 循环引用导致蓝图导入失败

**错误信息：**

```
ImportError: cannot import name 'users_bp' from partially initialized module
'app.blueprints.users' (most likely due to a circular import)
```

**根因分析：**

`app/__init__.py` 导入蓝图 → 蓝图文件导入模型 → 模型文件导入 `app/__init__.py` 中的 `db` 对象 → 形成循环。

**修复方案：**

```python
# 方案一：延迟导入（在 create_app 内部导入蓝图）
def create_app() -> Flask:
    app: Flask = Flask(__name__)
    # 先初始化扩展
    db.init_app(app)
    # 再导入蓝图（此时 app 和 db 都已就绪）
    from app.blueprints.users import users_bp  # 放在函数内部
    app.register_blueprint(users_bp)
    return app

# 方案二：使用独立的 extensions.py 文件
# app/extensions.py
from flask_sqlalchemy import SQLAlchemy
db: SQLAlchemy = SQLAlchemy()

# 方案三：使用蓝图层延迟访问
# 不在蓝图文件中顶层导入 db，而是在视图函数中访问
from flask import current_app
@users_bp.route("/")
def index():
    from app.extensions import db  # 延迟导入
    users = db.session.execute(...)
```

### 12.3 url_for 使用了错误的 endpoint 前缀

**错误信息：**

```
werkzeug.routing.exceptions.BuildError: Could not build url for endpoint 'profile'.
Did you forget to specify the blueprint name?
```

**根因分析：**

在蓝图 A 中使用 `url_for("profile")` 试图引用蓝图 B 的路由。应使用 `url_for("blueprint_b.profile")`。

**常见误用：**

```python
# ❌ 错误：省略蓝图前缀（但当需要跨蓝图引用时）
@posts_bp.route("/user-posts")
def user_posts():
    return redirect(url_for("profile"))  # 找不到 'profile'

# ✅ 正确：指定完整 endpoint
@posts_bp.route("/user-posts")
def user_posts():
    return redirect(url_for("users.profile"))

# ✅ 正确：蓝图内引用可用点号简写
@users_bp.route("/settings")
def settings():
    return redirect(url_for(".profile"))  # .profile = users.profile
```

### 12.4 问题排查表

| 现象 | 可能原因 | 检查方法 | 解决方案 |
|------|---------|---------|---------|
| 404 Not Found | 蓝图未注册 | 打印 `app.blueprints` | 确认 `register_blueprint()` 已调用 |
| BuildError | endpoint 前缀错误 | 检查 `url_for()` 参数 | 使用 `蓝图名.视图名` 格式 |
| 蓝图钩子不执行 | url_prefix 不匹配 | 确认请求 URL 匹配蓝图前缀 | 打印 `request.url_rule.endpoint` |
| 静态文件 404 | static_url_path 冲突 | 检查多个蓝图的 static_url_path | 为每个蓝图设置不同路径 |
| 模板覆盖 | template_folder 同名模板 | 检查模板查找顺序 | 使用前缀子目录隔离 |
| ImportError | 循环引用 | 检查 import 链 | 使用延迟导入或 extensions 模式 |

---

## 第十三部分：调试与排错实战

### 13.1 调试会话：蓝图路由不生效

```
场景：定义了一个蓝图 posts_bp，注册后访问 /posts/ 返回 404。

调试步骤：

Step 1: 确认蓝图已注册
$ python -c "from app import create_app; app=create_app(); print(list(app.blueprints))"
['posts', 'users', 'admin']  ← posts 在列表中，说明已注册

Step 2: 检查 URL 映射
$ python -c "
from app import create_app
app = create_app()
for rule in app.url_map.iter_rules():
    print(f'{rule.endpoint:30s} {rule.rule}')
"
posts.index                    /posts/
posts.view                     /posts/<int:post_id>
users.index                    /users/
...
← 路由规则存在

Step 3: 检查实际请求路径
在 before_request 钩子中打印：
@posts_bp.before_request
def debug_route() -> None:
    from flask import request
    print(f"[DEBUG] PATH: {request.path}, URL_RULE: {request.url_rule}")

访问 http://localhost:5000/Posts/ （注意大写 P）
输出：[DEBUG] PATH: /Posts/, URL_RULE: None
结论：Flask 路由匹配区分大小写！

Step 4: 修复
$ curl http://localhost:5000/posts/  ← 小写路径正常返回 200
```

### 13.2 调试工具函数

```python
# app/debug_utils.py
from flask import Flask

def print_all_routes(app: Flask) -> None:
    """打印所有注册的路由（按 URL 排序）"""
    rules = sorted(app.url_map.iter_rules(), key=lambda r: r.rule)
    for rule in rules:
        methods: str = ",".join(sorted(rule.methods - {"HEAD", "OPTIONS"}))
        print(f"{methods:10s} {rule.rule:40s} → {rule.endpoint}")

def print_blueprint_tree(app: Flask) -> None:
    """打印蓝图注册树"""
    for name in app.blueprints:
        bp = app.blueprints.get(name)
        if bp:
            prefix = bp.url_prefix if hasattr(bp, "url_prefix") else "N/A"
            print(f"  ├── {name} (url_prefix={prefix})")

# 使用
# from app.debug_utils import print_all_routes, print_blueprint_tree
# print_all_routes(app)
# print_blueprint_tree(app)
```

---

## 第十四部分：进阶用法与性能考量

### 14.1 条件蓝图注册

```python
def create_app(config_name: str) -> Flask:
    app: Flask = Flask(__name__)

    # 核心蓝图始终注册
    app.register_blueprint(users_bp)
    app.register_blueprint(posts_bp)

    # 根据环境选择性注册
    if app.config.get("ENABLE_ADMIN", False):
        app.register_blueprint(admin_bp)

    if app.config.get("ENABLE_API", True):
        from app.api import get_api_blueprints
        for bp in get_api_blueprints(app.config):
            app.register_blueprint(bp)

    # 调试蓝图仅在开发环境注册
    if app.debug:
        from app.debug_toolbar import debug_bp
        app.register_blueprint(debug_bp)

    return app
```

### 14.2 蓝图中间件模式

```python
# 使用蓝图实现可复用的请求日志中间件
import time
from flask import Blueprint, request, g

def create_logging_blueprint(name: str, prefix: str = "") -> Blueprint:
    """创建带请求日志的蓝图工厂"""
    bp = Blueprint(name, __name__, url_prefix=prefix)

    @bp.before_request
    def log_request() -> None:
        g.start_time = time.time()

    @bp.after_request
    def log_response(response):
        duration = time.time() - g.get("start_time", 0)
        response.headers["X-Process-Time"] = f"{duration:.4f}s"
        return response

    return bp

# 使用
audit_bp = create_logging_blueprint("audit", "/audit")
```

### 14.3 蓝图与路由性能

```python
# 性能测试：直接路由 vs 蓝图路由
import time

def benchmark_routing(app: Flask, num_iterations: int = 10000) -> None:
    """对比不同路由方式的性能"""
    client = app.test_client()

    start = time.perf_counter()
    for _ in range(num_iterations):
        client.get("/api/v1/items/42")
    elapsed = time.perf_counter() - start
    print(f"蓝图路由: {elapsed:.4f}s ({num_iterations/elapsed:.0f} req/s)")

# 结论：蓝图路由与应用级路由性能无显著差异（<1%），
# 因为注册后统一存储在 app.url_map 中，查找逻辑相同。
```

| 进阶知识点 | 说明 |
|-------------|------|
| 嵌套蓝图 | 父蓝图内 register_blueprint 注册子蓝图 |
| 工厂模式 | create_app() 集中管理蓝图注册 |
| 条件注册 | 根据配置选择性加载蓝图 |
| 双向钩子链 | 父蓝图钩子包裹子蓝图钩子 |
| 隔离测试 | 创建独立 Flask 实例仅注册被测蓝图 |
| URL 冲突检测 | 遍历 url_map 发现重复路由 |
| 延迟导入 | 解决循环引用，提高启动速度 |