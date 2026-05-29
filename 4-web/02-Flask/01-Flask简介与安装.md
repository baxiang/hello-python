# 01-Flask简介与安装

> Python 3.11+

本章介绍 Flask Web 框架的基本概念、安装方法和第一个应用的创建。

---

## 概念铺垫

### 什么是 Flask

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

### Flask(**name**) 参数详解

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

### 开发服务器与调试模式

Flask 内置了一个轻量级的开发服务器，适合开发环境使用。

**app.run() 参数详解：**

```python
from flask import Flask

app: Flask = Flask(__name__)

app.run(
    host="127.0.0.1",   # 监听地址，0.0.0.0 表示所有网卡
    port=5000,          # 端口号
    debug=None,         # 调试模式
    load_dotenv=True,   # 加载.env 文件
)
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

### L1 理解层：会用

#### 安装 Flask

使用 uv 包管理器安装 Flask 及其常用扩展。

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

#### Hello World 示例

一个最小的 Flask 应用只需要几行代码。

```python
# app.py
from flask import Flask

app: Flask = Flask(__name__)


@app.route("/")
def hello() -> str:
    return "Hello, World!"


if __name__ == "__main__":
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

#### 开发服务器配置

```python
# 开发环境
app.run(debug=True)  # 启用调试模式

# 允许外部访问
app.run(host="0.0.0.0", port=5000)

# 指定端口
app.run(port=8080)
```

**启用调试模式的方式：**

```python
# 方式 1：在代码中设置
from flask import Flask

app: Flask = Flask(__name__)
app.run(debug=True)

# 方式 2：使用环境变量
# export FLASK_DEBUG=1
# uv run flask run

# 方式 3：使用 flask 命令
# uv run flask --debug run
```

---

### L2 实践层：用好

#### 最佳实践

| 做法 | 原因 | 示例 |
|------|------|------|
| 使用应用工厂模式 | 测试隔离、多实例、延迟初始化 | `def create_app(config_name): ...` |
| 生产环境使用 Gunicorn | 开发服务器仅用于开发 | `gunicorn -w 4 app:app` |
| `debug=True` 仅用于开发 | 避免暴露代码和交互式调试器 | 生产 `DEBUG = False` |
| 使用 uv 管理依赖 | 更快、更现代的包管理 | `uv add flask` |
| `.env` 存敏感配置 | 避免密钥泄露到版本控制 | `SECRET_KEY=...` 放入 `.env` |

#### 反模式

```python
# ❌ 错误：生产环境开启 debug
app.run(debug=True, host="0.0.0.0")  # 暴露调试器！

# ✅ 正确：用环境变量控制
import os
debug_mode: bool = os.environ.get("FLASK_DEBUG", "0") == "1"
app.run(debug=debug_mode)

# ❌ 错误：使用弱 SECRET_KEY
app.config["SECRET_KEY"] = "123456"

# ✅ 正确：使用密码学安全随机密钥
import secrets
app.config["SECRET_KEY"] = secrets.token_hex(32)
```

#### 何时使用 Flask vs Django

| 场景 | 推荐 |
|------|------|
| 小型 API、微服务、快速原型 | Flask |
| CMS、企业应用、内置管理后台 | Django |
| 中大型复杂应用 | Pyramid |
| 异步 WebSocket 应用 | Quart |

---

### L3 专家层：深入

#### WSGI 协议原理

WSGI（Web Server Gateway Interface）是 Python Web 应用与 Web 服务器之间的标准接口规范（PEP 3333）。

```
┌─────────────────────────────────────────────────────────────────┐
│                    WSGI 调用流程                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   Web Server (Gunicorn/uWSWSGI/nginx)                           │
│       │                                                         │
│       │ environ = {                                             │
│       │   'REQUEST_METHOD': 'GET',                              │
│       │   'PATH_INFO': '/hello',                                │
│       │   'QUERY_STRING': 'name=abc',                           │
│       │   'wsgi.input': <socket>,                               │
│       │   ...                                                   │
│       │ }                                                       │
│       │                                                         │
│       ▼                                                         │
│   WSGI Callable (Flask 应用)                                    │
│       │                                                         │
│       │ def application(environ, start_response):               │
│       │     status = '200 OK'                                   │
│       │     headers = [('Content-Type', 'text/html')]           │
│       │     start_response(status, headers)                     │
│       │     return [b'Hello, World!']                           │
│       │                                                         │
│       ▼                                                         │
│   Web Server → 返回 HTTP 响应给客户端                           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

Flask 的 `Flask` 类实现了 `__call__` 方法，使其成为 WSGI callable：

```python
# Flask 源码简化版
class Flask:
    def __call__(
        self,
        environ: dict[str, Any],
        start_response: Callable[[str, list[tuple[str, str]]], None],
    ) -> Iterable[bytes]:
        """WSGI 入口点"""
        return self.wsgi_app(environ, start_response)

    def wsgi_app(
        self,
        environ: dict[str, Any],
        start_response: Callable[[str, list[tuple[str, str]]], None],
    ) -> Iterable[bytes]:
        # 1. 创建请求上下文
        ctx = self.request_context(environ)
        ctx.push()
        error: BaseException | None = None
        try:
            try:
                # 2. 路由匹配 + 视图函数调用
                response = self.full_dispatch_request()
            except Exception as e:
                error = e
                response = self.handle_exception(e)
            # 3. 返回响应
            return response(environ, start_response)
        finally:
            # 4. 清理上下文
            ctx.pop(error)
```

#### 性能考量

| 操作 | 耗时 | 内存 | 说明 |
|------|------|------|------|
| Flask 应用初始化 | ~5ms | ~15MB | 首次导入所有扩展 |
| 单次请求处理（简单路由） | ~0.5ms | ~2KB/req | 仅路由匹配 + 字符串返回 |
| 上下文创建/销毁 | ~0.1ms | ~1KB | RequestContext 推送/弹出 |
| Jinja2 模板渲染（小模板） | ~1ms | ~50KB | 含缓存命中 |
| Werkzeug 路由匹配（100 条规则） | ~0.05ms | — | 线性扫描，O(n) |

**扩展性：** Flask 内置开发服务器单进程单线程，QPS 约 1000-3000。生产环境需使用 Gunicorn/uWSGI + 多 worker 进程，可达 10000+ QPS。

#### Flask vs Django vs Pyramid 架构对比

| 维度 | Flask | Django | Pyramid |
|------|-------|--------|---------|
| 设计理念 | 微框架，核心极简 | 全栈框架，约定优于配置 | 组件化，按需组装 |
| 路由系统 | Werkzeug URLMap | 自研 URLconf | 自研 Routes/Traversal |
| ORM | 无（用 Flask-SQLAlchemy） | 自带 Django ORM | 无（用 SQLAlchemy） |
| 模板引擎 | Jinja2（独立项目） | Django Templates | Chameleon/Mako/Jinja2 |
| 应用工厂 | 推荐模式 | 不适用（项目结构固定） | 原生支持 |
| 学习曲线 | 低 | 中高 | 高 |
| 适合场景 | 小型项目、API、微服务 | 大型内容管理、企业应用 | 中大型复杂应用 |

#### 应用工厂模式的设计动机

```
┌─────────────────────────────────────────────────────────────────┐
│              应用工厂模式 (Application Factory)                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   传统方式：                                                     │
│       app = Flask(__name__)     ← 全局单例，难以测试             │
│                                                                 │
│   工厂模式：                                                     │
│       def create_app(config_name: str) -> Flask:                 │
│           app = Flask(__name__)  ← 每次创建新实例                │
│           app.config.from_object(config_name)                    │
│           register_extensions(app)                               │
│           register_blueprints(app)                               │
│           return app                                             │
│                                                                 │
│   设计动机：                                                     │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │ • 测试隔离：每个测试函数获得独立的 app 实例              │   │
│   │ • 多实例：同一进程运行多个配置不同的应用                 │   │
│   │ • 延迟初始化：扩展可在 app 创建后再绑定                  │   │
│   │ • 配置灵活：通过参数切换 dev/test/prod 配置              │   │
│   └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

#### 知识关联

```
                    WSGI 协议
                        │
            ┌───────────┼───────────┐
            ▼           ▼           ▼
        Werkzeug    Flask Core   Gunicorn
        (路由/请求)  (上下文/扩展)  (WSGI Server)
            │           │           │
            └───────────┼───────────┘
                        ▼
                  应用工厂模式
                        │
            ┌───────────┼───────────┐
            ▼           ▼           ▼
        Blueprints   Extensions   Config
        (模块化)    (SQLAlchemy等) (环境变量)
```

---

## 总结

| 知识点 | 说明 |
|---------|------|
| Flask | 轻量级 Web 框架 |
| uv 安装 | 使用 uv add flask |
| app.run() | 启动开发服务器 |
| debug=True | 启用调试模式 |
| __name__ | 应用根目录定位 |
