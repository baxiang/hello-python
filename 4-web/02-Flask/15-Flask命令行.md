# 15-Flask命令行

> Python 3.11+ | Flask 3.x

本章讲解 Flask 命令行工具（CLI）的完整体系：从基本用法到自定义命令，再到 Click 框架原理与 CLI 插件开发。

---

## 第一部分：命令行基础（L1）

### 1.1 实际场景

你开发了一个 Flask 应用，需要通过终端启动开发服务器、打开交互式 Shell、执行数据库迁移等操作。每次都写冗长的 Python 代码很不方便。

**问题：Flask 提供了哪些内置命令？如何使用？**

### 1.2 Flask CLI 是什么

Flask CLI 基于 [Click](https://click.palletsprojects.com/) 框架构建，提供了一组开箱即用的命令行工具。Flask 3.x 内置 CLI 支持，无需额外安装。

```
Flask CLI 架构：

  +─────────────────────────────────────────────────────+
  │                  用户输入的命令                       │
  │  $ flask --app myapp run --port 5000                │
  +──────────────────────┬──────────────────────────────+
                         │
  +──────────────────────▼──────────────────────────────+
  │                  Flask CLI 入口                      │
  │  ┌───────────────────────────────────────────────┐  │
  │  │  flask 命令组（Group）                          │  │
  │  │  ├── run        启动开发服务器                  │  │
  │  │  ├── shell      打开交互式 Shell                │  │
  │  │  ├── routes     查看所有路由                    │  │
  │  │  └── test       运行测试                        │  │
  │  └───────────────────────────────────────────────┘  │
  +──────────────────────┬──────────────────────────────+
                         │
  +──────────────────────▼──────────────────────────────+
  │              Click 参数解析引擎                      │
  │  - 解析 --option 和 argument                        │
  │  - 生成 --help 文档                                 │
  │  - 验证参数类型                                     │
  +─────────────────────────────────────────────────────+
```

### 1.3 基本用法：`flask run`

```bash
# 指定应用模块并启动
$ flask --app app run

# 指定主机和端口
$ flask --app app run --host 0.0.0.0 --port 5000

# 启用调试模式（代码变更自动重载）
$ flask --app app run --debug

# 等价写法：通过环境变量设置
$ export FLASK_APP=app
$ export FLASK_DEBUG=1
$ flask run
```

| 命令片段 | 含义 |
|----------|------|
| `--app app` | 指定应用入口模块（可省略 `.py`） |
| `--host 0.0.0.0` | 绑定地址，`0.0.0.0` 允许外部访问 |
| `--port 5000` | 监听端口（默认 5000） |
| `--debug` | 启用调试模式 + 自动重载 |
| `--reload` | 仅启用自动重载（不打开调试器） |

```python
# app/__init__.py
from flask import Flask


def create_app() -> Flask:
    """应用工厂函数"""
    app: Flask = Flask(__name__)
    app.config["SECRET_KEY"] = "dev-secret-key"

    @app.route("/")
    def index() -> str:
        return "Hello, Flask CLI!"

    return app
```

> **提示**：`--app` 的值可以是模块名（`app`）、应用对象路径（`app:create_app`）或文件路径（`app.py`）。

### 1.4 应用自动发现机制

Flask CLI 会按以下顺序自动寻找应用实例：

```
应用发现流程：

  flask run（未指定 --app）
      │
      ▼
  ┌─────────────────────────────────────┐
  │  1. 检查 FLASK_APP 环境变量          │
  │     export FLASK_APP=myapp:app      │
  └────────────────┬────────────────────┘
                   │ 未设置
                   ▼
  ┌─────────────────────────────────────┐
  │  2. 按文件名顺序查找：               │
  │     a. app.py                        │
  │     b. wsgi.py                       │
  │     c. app/__init__.py               │
  └────────────────┬────────────────────┘
                   │ 找到文件
                   ▼
  ┌─────────────────────────────────────┐
  │  3. 在文件中查找应用实例：           │
  │     a. 名为 "app" 或 "application"  │
  │        的 Flask 实例                 │
  │     b. 名为 "create_app" 或         │
  │        "make_app" 的工厂函数         │
  └────────────────┬────────────────────┘
                   │
                   ▼
  ┌─────────────────────────────────────┐
  │  4. 如果都找不到 → 报错              │
  │     Could not locate a Flask        │
  │     application.                    │
  └─────────────────────────────────────┘
```

```python
# wsgi.py —— CLI 自动发现的第二个候选文件
from app import create_app

app: Flask = create_app()

# flask run 会自动找到此文件中的 app 变量
```

```python
# app/__init__.py —— CLI 自动发现的第三个候选
from flask import Flask


def create_app() -> Flask:
    app: Flask = Flask(__name__)

    @app.route("/")
    def index() -> str:
        return "Auto-discovered!"

    return app

# CLI 会调用 create_app() 获取应用实例
```

### 1.5 `flask shell` 交互式 Shell

```bash
# 打开 Python 交互式 Shell（自动导入 app）
$ flask --app app shell

>>> app
<Flask 'app'>
>>> app.config["SECRET_KEY"]
'dev-secret-key'
```

```python
# app/__init__.py
from flask import Flask
from app.models import User, db


def create_app() -> Flask:
    app: Flask = Flask(__name__)
    # ... 其他配置
    return app


@app.shell_context_processor
def make_shell_context() -> dict[str, object]:
    """向 Shell 注入常用对象"""
    return {"db": db, "User": User}
```

```bash
# 使用 make_shell_context 后，Shell 中可直接使用 db 和 User
$ flask --app app shell

>>> db
<SQLAlchemy engine=sqlite:///app.db>
>>> User
<class 'app.models.User'>
```

> **注意**：`@app.shell_context_processor` 使用 `app` 装饰器而非 `app.cli`，因为它注册到 Flask 应用本身而非 CLI。

---

## 第二部分：dotenv 环境变量（L1）

### 2.1 .env 文件自动加载

Flask 3.x 原生支持 `.env` 和 `.flaskenv` 文件的自动加载（需要安装 `python-dotenv`）：

```bash
$ uv add python-dotenv
```

```
dotenv 加载顺序（优先级从高到低）：

  ┌──────────────────────────────────────────────────────┐
  │  1. 系统环境变量（终端 export 的变量）                  │
  │     ↓                                                 │
  │  2. .env 文件（应用配置，通常不提交到 Git）             │
  │     ↓                                                 │
  │  3. .flaskenv 文件（Flask CLI 配置，可提交到 Git）     │
  │     ↓                                                 │
  │  4. 代码中的默认值                                     │
  └──────────────────────────────────────────────────────┘

  注意：已存在的环境变量不会被 .env 文件覆盖
```

```ini
# .env —— 敏感配置（加入 .gitignore）
SECRET_KEY=your-super-secret-key-here
DATABASE_URL=postgresql://user:pass@localhost/dev_db
FLASK_DEBUG=1
```

```ini
# .flaskenv —— Flask CLI 相关配置（可提交到 Git）
FLASK_APP=app
FLASK_DEBUG=1
FLASK_RUN_PORT=5000
FLASK_RUN_HOST=0.0.0.0
```

```bash
# .gitignore
.env
.env.local
*.pyc
__pycache__/
```

> **关键区别**：`.flaskenv` 存 CLI 相关的环境变量（如 `FLASK_APP`），可以安全提交；`.env` 存应用敏感配置（如 `SECRET_KEY`），绝不能提交。

### 2.2 虚拟环境中的环境变量

```bash
# 方式一：通过 .env/.flaskenv（推荐）
# 在项目根目录创建文件，flask 命令自动加载

# 方式二：终端临时设置
$ export FLASK_APP=app
$ export FLASK_DEBUG=1
$ flask run

# 方式三：写入 shell 配置文件
# ~/.bashrc 或 ~/.zshrc
export FLASK_APP=app
export FLASK_DEBUG=1

# 方式四：使用 direnv（项目级环境变量）
# .envrc
export FLASK_APP=app
export FLASK_DEBUG=1
```

---

## 第三部分：自定义命令（L1）

### 3.1 使用 `@app.cli.command()` 注册命令

```python
# app/commands.py
import click
from flask import Flask
from flask.cli import with_appcontext


def register_cli_commands(app: Flask) -> None:
    """注册 CLI 命令到应用"""

    @app.cli.command("hello")
    @click.argument("name", default="World")
    def hello(name: str) -> None:
        """打印问候语"""
        click.echo(f"Hello, {name}!")

    @app.cli.command("greet")
    @click.option("--count", default=1, help="问候次数")
    @click.argument("name")
    def greet(name: str, count: int) -> None:
        """重复问候"""
        for _ in range(count):
            click.echo(f"Hi, {name}!")
```

```python
# app/__init__.py
from flask import Flask


def create_app() -> Flask:
    app: Flask = Flask(__name__)

    # ... 其他配置 ...

    # 注册自定义命令
    from app import commands  # noqa: F401

    return app
```

```bash
# 使用自定义命令
$ flask --app app hello
Hello, World!

$ flask --app app hello Flask
Hello, Flask!

$ flask --app app greet --count 3 Developer
Hi, Developer!
Hi, Developer!
Hi, Developer!

# 查看帮助
$ flask --app app hello --help
Usage: flask hello [OPTIONS] [NAME]

  打印问候语

Options:
  --help  Show this message and exit.
```

### 3.2 Click 参数：Argument vs Option

```python
# app/cli_args.py
import click
from flask import Flask
from typing import Any


def register_arg_commands(app: Flask) -> None:
    """演示 Click 参数类型"""

    # @click.argument：位置参数（必填）
    @app.cli.command("create-user")
    @click.argument("username")
    @click.argument("email")
    def create_user(username: str, email: str) -> None:
        """创建新用户"""
        click.echo(f"Creating user: {username} <{email}>")

    # @click.option：可选参数（带 -- 前缀）
    @app.cli.command("deploy")
    @click.option("--env", type=click.Choice(["dev", "staging", "prod"]), default="dev")
    @click.option("--verbose", "-v", is_flag=True, help="显示详细信息")
    @click.option("--workers", "-w", default=4, type=int, help="Worker 数量")
    def deploy(env: str, verbose: bool, workers: int) -> None:
        """部署应用"""
        click.echo(f"Deploying to {env} with {workers} workers")
        if verbose:
            click.echo("Verbose mode enabled")

    # 组合使用
    @app.cli.command("migrate-db")
    @click.argument("migration_name")
    @click.option("--dry-run", is_flag=True, help="预览而不执行")
    @click.option("--auto", is_flag=True, help="自动生成迁移脚本")
    def migrate_db(migration_name: str, dry_run: bool, auto: bool) -> None:
        """数据库迁移"""
        if dry_run:
            click.echo(f"[DRY RUN] Would create migration: {migration_name}")
        elif auto:
            click.echo(f"Auto-generating migration: {migration_name}")
        else:
            click.echo(f"Creating migration: {migration_name}")
```

| 装饰器 | 用途 | 示例 | 必填 |
|--------|------|------|------|
| `@click.argument("name")` | 位置参数 | `flask cmd value` | 是 |
| `@click.option("--name")` | 可选参数 | `flask cmd --name value` | 否 |
| `@click.option("--flag", is_flag=True)` | 布尔标志 | `flask cmd --flag` | 否 |
| `@click.option("--n", type=int)` | 类型约束 | `flask cmd --n 10` | 否 |
| `@click.option("--env", type=click.Choice([...]))` | 枚举选择 | `flask cmd --env prod` | 否 |

### 3.3 实战：`flask init-db` 数据库初始化

```python
# app/cli_db.py
import click
from flask import Flask, current_app
from flask.cli import with_appcontext
import sqlite3


def register_db_commands(app: Flask) -> None:
    """注册数据库相关 CLI 命令"""

    def get_db() -> sqlite3.Connection:
        """获取数据库连接"""
        db_path: str = current_app.config.get("DATABASE", "app.db")
        conn: sqlite3.Connection = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        return conn

    @app.cli.command("init-db")
    @click.option("--drop/--no-drop", default=False, help="删除已有表")
    def init_db(drop: bool) -> None:
        """初始化数据库"""
        conn: sqlite3.Connection = get_db()

        if drop:
            click.echo("Dropping existing tables...")
            conn.executescript("""
                DROP TABLE IF EXISTS users;
                DROP TABLE IF EXISTS posts;
            """)

        click.echo("Creating tables...")
        conn.executescript("""
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                body TEXT NOT NULL,
                user_id INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            );
        """)

        conn.commit()
        conn.close()
        click.echo("Database initialized successfully.")

    @app.cli.command("seed-db")
    @click.option("--count", default=10, help="生成测试数据条数")
    def seed_db(count: int) -> None:
        """填充测试数据"""
        conn: sqlite3.Connection = get_db()

        click.echo(f"Inserting {count} test users...")
        for i in range(count):
            conn.execute(
                "INSERT INTO users (username, email) VALUES (?, ?)",
                (f"user_{i}", f"user_{i}@example.com"),
            )

        conn.commit()
        conn.close()
        click.echo(f"Seeded {count} users.")

    @app.cli.command("drop-db")
    @click.confirmation_option(prompt="Are you sure you want to drop the database?")
    def drop_db() -> None:
        """删除数据库文件"""
        import os

        db_path: str = current_app.config.get("DATABASE", "app.db")
        if os.path.exists(db_path):
            os.remove(db_path)
            click.echo(f"Database file '{db_path}' deleted.")
        else:
            click.echo("Database file not found.")
```

```bash
# 使用数据库命令
$ flask --app app init-db
Creating tables...
Database initialized successfully.

$ flask --app app init-db --drop
Dropping existing tables...
Creating tables...
Database initialized successfully.

$ flask --app app seed-db --count 5
Inserting 5 test users...
Seeded 5 users.

$ flask --app app drop-db
Are you sure you want to drop the database? [y/N]: y
Database file 'app.db' deleted.
```

### 3.4 `@with_appcontext` 装饰器

当自定义命令需要访问 Flask 应用上下文（如数据库、配置）时，使用 `@with_appcontext`：

```python
# app/cli_context.py
import click
from flask import Flask, current_app
from flask.cli import with_appcontext


def register_context_commands(app: Flask) -> None:
    """演示应用上下文命令"""

    @app.cli.command("show-config")
    @with_appcontext
    def show_config() -> None:
        """显示当前应用配置"""
        # current_app 需要应用上下文
        for key in sorted(current_app.config.keys()):
            if not key.startswith("_"):
                click.echo(f"  {key}: {current_app.config[key]}")

    @app.cli.command("db-info")
    @with_appcontext
    def db_info() -> None:
        """显示数据库连接信息"""
        db_uri: str = current_app.config.get("SQLALCHEMY_DATABASE_URI", "N/A")
        click.echo(f"Database URI: {db_uri}")
```

---

## 第四部分：L2 实践层

### 4.1 常用命令清单

```
Flask 内置命令一览：

  $ flask --help
  Usage: flask [OPTIONS] COMMAND [ARGS]...

  Commands:
    routes    显示应用的所有路由规则
    run       启动开发服务器
    shell     打开交互式 Shell（自动加载应用上下文）
    test      运行测试（Flask 3.x 新增）

  常用选项：
    --app TEXT       指定应用（模块名或 import 路径）
    --debug / --no-debug  启用/禁用调试模式
    --version        显示 Flask 版本
    --help           显示帮助信息
```

### 4.2 `flask routes` 查看所有路由

```bash
# 列出所有路由
$ flask --app app routes

  Endpoint            Methods  Rule
  ------------------  -------  ---------------------------
  static              GET      /static/<path:filename>
  index               GET      /
  users.list          GET      /users/
  users.detail        GET      /users/<int:user_id>
  posts.list          GET,POST /posts/
  posts.detail        GET      /posts/<int:post_id>

# 过滤特定端点
$ flask --app app routes | grep users

  users.list          GET      /users/
  users.detail        GET      /users/<int:user_id>
```

```python
# app/routes_demo.py
from flask import Flask, Blueprint


def create_app() -> Flask:
    app: Flask = Flask(__name__)

    # 应用级路由
    @app.route("/")
    def index() -> str:
        return "Home"

    # 蓝图路由
    users_bp: Blueprint = Blueprint("users", __name__, url_prefix="/users")

    @users_bp.route("/")
    def list_users() -> str:
        return "Users List"

    @users_bp.route("/<int:user_id>")
    def user_detail(user_id: int) -> str:
        return f"User {user_id}"

    app.register_blueprint(users_bp)

    return app
```

### 4.3 `flask test` 运行测试

Flask 3.x 内置 `test` 命令，自动发现并运行 pytest：

```bash
# 运行所有测试
$ flask --app app test

# 运行特定测试文件
$ flask --app app test tests/test_users.py

# 显示详细输出
$ flask --app app test -v

# 运行匹配名称的测试
$ flask --app app test -k "test_login"
```

```python
# tests/test_cli.py
from flask import Flask
from flask.testing import FlaskCliRunner
import pytest


@pytest.fixture
def app() -> Flask:
    app: Flask = create_app()
    app.config["TESTING"] = True
    return app


@pytest.fixture
def cli_runner(app: Flask) -> FlaskCliRunner:
    return app.test_cli_runner()


def test_hello_command(cli_runner: FlaskCliRunner) -> None:
    """测试 hello 命令"""
    result = cli_runner.invoke(args=["hello", "World"])
    assert result.exit_code == 0
    assert "Hello, World!" in result.output


def test_init_db_command(cli_runner: FlaskCliRunner) -> None:
    """测试 init-db 命令"""
    result = cli_runner.invoke(args=["init-db"])
    assert result.exit_code == 0
    assert "Database initialized" in result.output
```

### 4.4 自定义命令的最佳实践

```
命令组织最佳实践：

  ┌──────────────────────────────────────────────────────────┐
  │  项目结构                                                │
  │                                                          │
  │  app/                                                    │
  │  ├── __init__.py          # create_app + 命令注册        │
  │  ├── cli/               # CLI 命令模块                    │
  │  │   ├── __init__.py      # 注册入口                     │
  │  │   ├── db.py            # 数据库命令                    │
  │  │   ├── user.py          # 用户管理命令                  │
  │  │   └── admin.py         # 管理员命令                    │
  │  ├── models/              # 数据模型                      │
  │  └── blueprints/          # 蓝图模块                      │
  │                                                          │
  │  原则：                                                   │
  │  1. 命令按功能分组，不堆在一个文件里                       │
  │  2. 每个命令都有 docstring（自动生成 --help）              │
  │  3. 使用 click.echo 而非 print（支持颜色/样式）            │
  │  4. 耗时操作添加进度提示（click.progressbar）              │
  │  5. 错误使用 ctx.fail() 而非 raise                        │
  └──────────────────────────────────────────────────────────┘
```

```python
# app/cli/__init__.py
from flask import Flask


def register_cli(app: Flask) -> None:
    """注册所有 CLI 命令组"""
    from app.cli import db, user, admin  # noqa: F401

    # 各模块的 register_commands() 会在 import 时执行
    db.register_commands(app)
    user.register_commands(app)
    admin.register_commands(app)
```

```python
# app/cli/db.py
import click
from flask import Flask
from flask.cli import with_appcontext
from typing import Any


def register_commands(app: Flask) -> None:
    """注册数据库命令组"""

    @app.cli.group("db")
    def db_group() -> None:
        """数据库管理命令"""
        pass

    @db_group.command("create")
    @with_appcontext
    def db_create() -> None:
        """创建数据库表"""
        from app.extensions import db

        db.create_all()
        click.echo("Database tables created.")

    @db_group.command("drop")
    @click.confirmation_option(prompt="Drop all tables?")
    @with_appcontext
    def db_drop() -> None:
        """删除所有数据库表"""
        from app.extensions import db

        db.drop_all()
        click.echo("Database tables dropped.")

    @db_group.command("reset")
    @with_appcontext
    def db_reset() -> None:
        """重置数据库（删除 + 重建）"""
        from app.extensions import db

        db.drop_all()
        click.echo("Tables dropped.")
        db.create_all()
        click.echo("Tables recreated.")


# 使用：flask db create / flask db drop / flask db reset
```

### 4.5 命令分组：Blueprint.cli

Flask 2.x+ 支持蓝图级别的 CLI 命令，让每个蓝图管理自己的命令：

```python
# app/blueprints/users.py
import click
from flask import Blueprint
from flask.cli import with_appcontext


users_bp: Blueprint = Blueprint("users", __name__, url_prefix="/users")


@users_bp.cli.command("list")
@with_appcontext
@click.option("--limit", default=20, type=int, help="显示数量")
def list_users(limit: int) -> None:
    """列出所有用户"""
    from app.models import User

    users: list[User] = User.query.limit(limit).all()
    for user in users:
        click.echo(f"  {user.id}: {user.username} ({user.email})")
    click.echo(f"\nTotal: {len(users)} users shown (limit: {limit})")


@users_bp.cli.command("delete")
@with_appcontext
@click.argument("user_id", type=int)
@click.confirmation_option(prompt="Delete this user?")
def delete_user(user_id: int) -> None:
    """删除指定用户"""
    from app.models import User, db

    user: User | None = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        click.echo(f"User '{user.username}' deleted.")
    else:
        click.echo(f"User with ID {user_id} not found.")
```

```python
# app/__init__.py
from flask import Flask


def create_app() -> Flask:
    app: Flask = Flask(__name__)

    # 注册蓝图（蓝图中的 CLI 命令自动注册）
    from app.blueprints.users import users_bp
    from app.blueprints.posts import posts_bp

    app.register_blueprint(users_bp)
    app.register_blueprint(posts_bp)

    return app
```

```bash
# 蓝图命令通过蓝图名调用
$ flask --app app users list --limit 5
  1: admin (admin@example.com)
  2: alice (alice@example.com)

Total: 2 users shown (limit: 5)

$ flask --app app users delete 2
Delete this user? [y/N]: y
User 'alice' deleted.
```

### 4.6 Click 高级功能

```python
# app/cli_advanced.py
import click
from flask import Flask
from flask.cli import with_appcontext
from pathlib import Path
from typing import Any


def register_advanced_commands(app: Flask) -> None:
    """演示 Click 高级功能"""

    # 文件路径参数
    @app.cli.command("import-data")
    @click.argument("file", type=click.Path(exists=True, readable=True, path_type=Path))
    @with_appcontext
    def import_data(file: Path) -> None:
        """从 JSON 文件导入数据"""
        import json

        data: list[dict[str, Any]] = json.loads(file.read_text())
        click.echo(f"Importing {len(data)} records from {file.name}")
        for record in data:
            click.echo(f"  → {record}")

    # 进度条
    @app.cli.command("process-tasks")
    @click.option("--total", default=100, type=int)
    def process_tasks(total: int) -> None:
        """模拟批量任务处理"""
        with click.progressbar(range(total), label="Processing") as bar:
            for _ in bar:
                # 模拟处理
                pass
        click.echo(f"\nDone! Processed {total} tasks.")

    # 交互式输入
    @app.cli.command("create-admin")
    @with_appcontext
    def create_admin() -> None:
        """交互式创建管理员"""
        username: str = click.prompt("Username", type=str)
        email: str = click.prompt("Email", type=str)
        password: str = click.prompt("Password", hide_input=True, confirmation_prompt=True)

        click.echo(f"\nCreating admin: {username} ({email})")
        click.echo("Admin created successfully.")

    # 命令链（通过 group 组织）
    @app.cli.group("cache")
    def cache_group() -> None:
        """缓存管理命令"""
        pass

    @cache_group.command("clear")
    @with_appcontext
    def cache_clear() -> None:
        """清空所有缓存"""
        click.echo("Cache cleared.")

    @cache_group.command("stats")
    @with_appcontext
    def cache_stats() -> None:
        """显示缓存统计"""
        click.echo("Cache stats:")
        click.echo("  Hits:   1234")
        click.echo("  Misses: 56")
        click.echo("  Size:   2.3 MB")
```

---

## 第五部分：L3 专家层

### 5.1 Click 框架原理

Click 是 Flask 团队开发的命令行工具包，核心理念是**可组合的命令树 + 自动帮助生成**。

```
Click 命令树结构：

                    flask (Group)
                   /      |      \
              run       shell    routes  (Command)
              (Command) (Command) (Command)
                            |
                     hello (Command)   ← 自定义命令
                     /    \
                name     ...
              (Argument)

  Group：命令组，可以包含多个 Command 或子 Group
  Command：具体可执行的命令
  Option：可选参数（--option value）
  Argument：位置参数（必填）

  核心流程：
  1. 解析命令行字符串 → 拆分为 token 列表
  2. 匹配命令树找到对应 Command
  3. 解析 Option 和 Argument
  4. 类型转换与验证
  5. 调用 Command 的 callback 函数
```

```python
# click_internals_demo.py
"""Click 内部机制的简化演示"""
from __future__ import annotations

import sys
from typing import Any, Callable


class SimpleCommand:
    """简化版 Click Command"""

    def __init__(
        self,
        name: str,
        callback: Callable[..., None],
        params: list[Parameter] | None = None,
        help_text: str | None = None,
    ) -> None:
        self.name: str = name
        self.callback: Callable[..., None] = callback
        self.params: list[Parameter] = params or []
        self.help_text: str = help_text or ""

    def get_help(self) -> str:
        """自动生成帮助文档"""
        lines: list[str] = [
            f"Usage: flask {self.name} [OPTIONS]",
            "",
            f"  {self.help_text}",
            "",
            "Options:",
        ]
        for param in self.params:
            lines.append(f"  {param.get_help_line()}")
        lines.append("  --help  Show this message and exit.")
        return "\n".join(lines)

    def invoke(self, parsed_args: dict[str, Any]) -> None:
        """执行命令"""
        self.callback(**parsed_args)


class Parameter:
    """简化版 Click 参数"""

    def __init__(
        self,
        name: str,
        param_type: type = str,
        default: Any = None,
        is_flag: bool = False,
        help_text: str = "",
    ) -> None:
        self.name: str = name
        self.param_type: type = param_type
        self.default: Any = default
        self.is_flag: bool = is_flag
        self.help_text: str = help_text

    def get_help_line(self) -> str:
        if self.is_flag:
            return f"  --{self.replace('_', '-')}  {self.help_text}"
        return f"  --{self.replace('_', '-')} TEXT  {self.help_text}"

    def replace(self, old: str, new: str) -> str:
        return self.name.replace(old, new)

    def parse(self, value: str) -> Any:
        """类型转换"""
        if self.is_flag:
            return True
        return self.param_type(value)


class SimpleGroup:
    """简化版 Click Group"""

    def __init__(self, name: str = "cli") -> None:
        self.name: str = name
        self.commands: dict[str, SimpleCommand] = {}

    def command(
        self, name: str, help_text: str = ""
    ) -> Callable[[Callable[..., None]], SimpleCommand]:
        """装饰器：注册命令"""

        def decorator(callback: Callable[..., None]) -> SimpleCommand:
            cmd: SimpleCommand = SimpleCommand(name, callback, help_text=help_text)
            self.commands[name] = cmd
            return cmd

        return decorator

    def group(
        self, name: str, help_text: str = ""
    ) -> "SimpleGroup":
        """创建子命令组"""
        sub_group: SimpleGroup = SimpleGroup(name)
        self.commands[name] = sub_group  # type: ignore[assignment]
        return sub_group

    def dispatch(self, args: list[str]) -> None:
        """解析并分发命令"""
        if not args or args[0] == "--help":
            self.print_help()
            return

        cmd_name: str = args[0]
        cmd: SimpleCommand | SimpleGroup | None = self.commands.get(cmd_name)

        if cmd is None:
            print(f"Error: No such command '{cmd_name}'")
            sys.exit(1)

        if isinstance(cmd, SimpleGroup):
            cmd.dispatch(args[1:])
        else:
            parsed: dict[str, Any] = self._parse_params(cmd, args[1:])
            cmd.invoke(parsed)

    def _parse_params(
        self, cmd: SimpleCommand, args: list[str]
    ) -> dict[str, Any]:
        """简化版参数解析"""
        result: dict[str, Any] = {}
        for param in cmd.params:
            if param.default is not None:
                result[param.name] = param.default
        return result

    def print_help(self) -> None:
        """打印帮助"""
        print(f"Usage: flask [OPTIONS] COMMAND [ARGS]...")
        print(f"\nCommands:")
        for name, cmd in self.commands.items():
            help_text: str = getattr(cmd, "help_text", "")
            print(f"  {name:<20} {help_text}")


# 使用演示
demo_cli: SimpleGroup = SimpleGroup("flask")


@demo_cli.command("hello", help_text="Print a greeting")
def demo_hello(name: str = "World") -> None:
    print(f"Hello, {name}!")


demo_cli.dispatch(["hello"])
# Output: Hello, World!

demo_cli.dispatch(["--help"])
# Output:
# Usage: flask [OPTIONS] COMMAND [ARGS]...
#
# Commands:
#   hello                Print a greeting
```

### 5.2 Flask CLI 的应用发现流程

```
Flask CLI 应用发现源码级流程：

  flask run
    │
    ▼
  load_dotenv()                     # 加载 .env / .flaskenv
    │
    ▼
  locate_app()                      # flask.cli.locate_app()
    │
    ├── 检查 FLASK_APP 环境变量
    │     └── 解析为 import_string（如 "app:create_app"）
    │
    ├── 遍历候选文件：app.py → wsgi.py → app/__init__.py
    │     └── 找到第一个存在的文件
    │
    └── 在模块中查找应用：
          ├── 名为 "app" 或 "application" 的 Flask 实例
          └── 名为 "create_app" 或 "make_app" 的工厂函数

    ▼
  ScriptInfo 对象                    # 缓存应用信息
    │
    ├── .app_import_path            # 导入路径
    ├── .create_app                 # 工厂函数引用
    └── .load_app()                 # 延迟加载应用实例

    ▼
  FlaskGroup.invoke()               # 执行命令
    │
    └── 确保应用上下文已创建
        └── 调用具体 Command.callback()
```

```python
# flask_cli_discovery.py
"""Flask CLI 应用发现流程的简化演示"""
from __future__ import annotations

import importlib
import os
from typing import Any, Callable
from pathlib import Path


class ScriptInfo:
    """简化版 Flask ScriptInfo"""

    def __init__(self, app_import_path: str | None = None) -> None:
        self.app_import_path: str | None = app_import_path
        self._loaded_app: Any = None

    def load_app(self) -> Any:
        """延迟加载应用实例"""
        if self._loaded_app is not None:
            return self._loaded_app

        if self.app_import_path:
            self._loaded_app = self._import_app(self.app_import_path)
        else:
            self._loaded_app = self._auto_discover_app()

        return self._loaded_app

    def _import_app(self, import_path: str) -> Any:
        """从 import 路径加载应用"""
        # 解析 "module:attr" 格式
        if ":" in import_path:
            module_name, attr_name = import_path.split(":", 1)
        else:
            module_name, attr_name = import_path, "app"

        module = importlib.import_module(module_name)
        app = getattr(module, attr_name)

        # 如果是工厂函数，调用它
        if callable(app) and app.__name__ in ("create_app", "make_app"):
            app = app()

        return app

    def _auto_discover_app(self) -> Any:
        """自动发现应用"""
        candidates: list[str] = ["app", "wsgi"]

        for candidate in candidates:
            module_path: Path = Path(f"{candidate}.py")
            if module_path.exists():
                return self._import_app(candidate)

            pkg_path: Path = Path(candidate) / "__init__.py"
            if pkg_path.exists():
                return self._import_app(candidate)

        raise RuntimeError(
            "Could not locate a Flask application. "
            "Use --app or set FLASK_APP environment variable."
        )


# 使用演示
def demo_discovery() -> None:
    # 方式一：显式指定
    info: ScriptInfo = ScriptInfo("myapp:create_app")
    app = info.load_app()

    # 方式二：自动发现
    info2: ScriptInfo = ScriptInfo()
    app2 = info2.load_app()  # 自动查找 app.py / wsgi.py
```

### 5.3 自定义 CLI 插件开发

可以通过 Flask 的 entry points 机制注册 CLI 插件，让第三方扩展提供命令：

```
CLI 插件架构：

  +─────────────────────────────────────────────────────────+
  │                    Flask 应用                            │
  │                                                         │
  │  flask CLI (FlaskGroup)                                 │
  │  ├── 内置命令：run, shell, routes, test                 │
  │  ├── 应用自定义命令：@app.cli.command()                  │
  │  ├── 蓝图命令：@blueprint.cli.command()                 │
  │  └── 插件命令（通过 entry_points 注册）                  │
  │      ├── flask-migrate → flask db upgrade               │
  │      ├── flask-login → 无 CLI                           │
  │      └── flask-mail → flask mail send                   │
  +─────────────────────────────────────────────────────────+
```

```python
# flask_myplugin/__init__.py
"""Flask CLI 插件示例"""
from __future__ import annotations

import click
from flask import Flask, current_app
from flask.cli import with_appcontext


class MyPlugin:
    """Flask 扩展 + CLI 插件"""

    def __init__(self, app: Flask | None = None) -> None:
        if app is not None:
            self.init_app(app)

    def init_app(self, app: Flask) -> None:
        """初始化扩展"""
        app.config.setdefault("MYPLUGIN_ENABLED", True)

        # 注册 CLI 命令
        self._register_cli(app)

    def _register_cli(self, app: Flask) -> None:
        """注册 CLI 命令到应用"""

        @app.cli.group("myplugin")
        def myplugin_group() -> None:
            """MyPlugin 管理命令"""
            pass

        @myplugin_group.command("status")
        @with_appcontext
        def status() -> None:
            """显示插件状态"""
            enabled: bool = current_app.config.get("MYPLUGIN_ENABLED", False)
            click.echo(f"MyPlugin enabled: {enabled}")

        @myplugin_group.command("enable")
        @with_appcontext
        def enable() -> None:
            """启用插件"""
            current_app.config["MYPLUGIN_ENABLED"] = True
            click.echo("MyPlugin enabled.")

        @myplugin_group.command("disable")
        @with_appcontext
        def disable() -> None:
            """禁用插件"""
            current_app.config["MYPLUGIN_ENABLED"] = False
            click.echo("MyPlugin disabled.")
```

```toml
# pyproject.toml —— 通过 entry points 注册为 Flask 插件
[project]
name = "flask-myplugin"
version = "1.0.0"

[project.entry-points."flask.commands"]
myplugin = "flask_myplugin.cli:myplugin_cli"
```

```python
# flask_myplugin/cli.py
"""独立 CLI 命令（通过 entry_points 注册）"""
import click


@click.group("myplugin")
def myplugin_cli() -> None:
    """MyPlugin CLI commands"""
    pass


@myplugin_cli.command("version")
def version() -> None:
    """显示插件版本"""
    click.echo("flask-myplugin v1.0.0")
```

```bash
# 安装插件后，命令自动出现在 flask CLI 中
$ pip install flask-myplugin

$ flask --help
Commands:
  ...
  myplugin    MyPlugin CLI commands    ← 自动注册

$ flask myplugin version
flask-myplugin v1.0.0

$ flask myplugin status
MyPlugin enabled: True
```

### 5.4 知识关联图

```
                    Flask CLI 知识体系
                          │
         ┌────────────────┼────────────────┐
         │                │                │
      内置命令         自定义命令        插件机制
         │                │                │
    ┌────┴────┐      ┌────┴────┐     ┌────┴────┐
    │ run     │      │@app.cli  │     │entry_   │
    │ shell   │      │.command()│     │points   │
    │ routes  │      │          │     │         │
    │ test    │      │@click.   │     │Flask    │
    └────┬────┘      │option()  │     │扩展规范 │
         │           │          │     └────┬────┘
         │           │@click.   │          │
    ┌────┴────┐      │argument()│     ┌────┴────┐
    │应用发现  │      │          │     │第三方   │
    │流程     │      │@with_    │     │包命令   │
    │.env加载 │      │appcontext│     │集成     │
    └─────────┘      └────┬─────┘     └─────────┘
                          │
                    ┌─────┴─────┐
                    │ Click 框架│
                    │ 原理      │
                    │           │
                    │ Group/    │
                    │ Command/  │
                    │ Parameter │
                    └───────────┘
```

| 知识点 | 说明 | 前置知识 |
|--------|------|----------|
| `flask run` | 启动开发服务器 | 无 |
| `flask shell` | 交互式 Shell | `shell_context_processor` |
| `flask routes` | 查看路由列表 | 蓝图与 endpoint |
| `@app.cli.command()` | 注册自定义命令 | Click 基础 |
| `@click.option()` | 可选参数 | 无 |
| `@click.argument()` | 位置参数 | 无 |
| `@with_appcontext` | 注入应用上下文 | Flask 应用上下文 |
| `blueprint.cli` | 蓝图级 CLI | 蓝图机制 |
| Entry Points | 插件注册 | Python 包分发 |

---

## 本章总结

```
Flask CLI 全景：

  ┌─────────────────────────────────────────────────────────────┐
  │                                                             │
  │  L1 基础：                                                   │
  │  ├── Flask CLI 基于 Click 框架构建                           │
  │  ├── flask --app myapp run [OPTIONS] 启动服务器             │
  │  ├── 应用自动发现：app.py → wsgi.py → app/__init__.py       │
  │  ├── flask shell 打开交互式 Shell                           │
  │  ├── .env / .flaskenv 自动加载环境变量                       │
  │  ├── @app.cli.command() 注册自定义命令                       │
  │  └── @click.option() / @click.argument() 定义参数           │
  │                                                             │
  │  L2 实践：                                                   │
  │  ├── flask routes 查看所有路由                               │
  │  ├── flask test 运行测试                                     │
  │  ├── @app.cli.group() 命令分组（如 flask db create）        │
  │  ├── blueprint.cli 蓝图级命令（如 flask users list）        │
  │  ├── click.progressbar / click.prompt 高级交互              │
  │  └── 最佳实践：按功能分组、使用 click.echo、添加 docstring  │
  │                                                             │
  │  L3 专家：                                                   │
  │  ├── Click 核心：Group → Command → Parameter 命令树         │
  │  ├── 应用发现流程：locate_app() → ScriptInfo → load_app()   │
  │  ├── Entry Points 注册插件命令（flask.commands 组）         │
  │  └── with_appcontext 确保命令有应用上下文                   │
  │                                                             │
  │  核心原则：                                                  │
  │  内置命令开箱即用，自定义命令用 Click 装饰器，                │
  │  插件通过 entry_points 注册                                  │
  │                                                             │
  └─────────────────────────────────────────────────────────────┘
```

| 知识点 | 说明 |
|--------|------|
| Flask CLI | 基于 Click 的命令行工具 |
| flask run | 启动开发服务器 |
| flask shell | 交互式 Shell |
| flask routes | 查看路由 |
| dotenv | .env / .flaskenv 环境变量 |
| @app.cli.command() | 自定义命令 |
| @click.option / argument | 参数定义 |
| @app.cli.group() | 命令分组 |
| blueprint.cli | 蓝图级 CLI |
| entry_points | 插件注册 |
