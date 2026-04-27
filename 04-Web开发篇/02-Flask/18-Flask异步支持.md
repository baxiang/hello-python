# Flask 异步支持（详细版）

> Python 3.11+

本章讲解 Flask 3.x 原生异步支持、性能考量、后台任务及底层原理。

---

## 第一部分：Flask 3.x 原生异步（L1）

### 1.1 实际场景

Flask 3.0 开始原生支持 `async def` 视图函数，可以直接使用 `await` 进行异步 I/O 操作，无需借助 Quart 等第三方框架。

**问题：如何在 Flask 中编写异步视图？**

### 1.2 async def 视图函数

Flask 3.x 允许视图函数定义为 `async def`，在 ASGI 服务器（如 Hypercorn、Daphne）或 WSGI 服务器（如 Gunicorn + gevent）下均可运行。

```python
# async_views.py
from flask import Flask, jsonify
import asyncio
from typing import Any

app: Flask = Flask(__name__)


@app.route("/async-hello")
async def async_hello() -> dict[str, str]:
    """异步视图函数 — Flask 3.0+"""
    await asyncio.sleep(0.1)  # 模拟异步 I/O
    return {"message": "Hello from async Flask!"}


@app.route("/async-fetch/<int:item_id>")
async def async_fetch(item_id: int) -> dict[str, Any]:
    """模拟异步数据获取"""
    data: dict[str, Any] = await fetch_data_async(item_id)
    return {"id": item_id, "data": data}


async def fetch_data_async(item_id: int) -> dict[str, Any]:
    """模拟异步 I/O 操作"""
    await asyncio.sleep(0.5)
    return {"name": f"Item {item_id}", "status": "active"}
```

### 1.3 async with app.app_context() 异步上下文管理

在异步代码中访问 Flask 应用上下文（如数据库会话、配置、g 对象），需要使用异步上下文管理器。

```python
# async_context.py
from flask import Flask, g, current_app
from typing import Any

app: Flask = Flask(__name__)


async def get_user_from_db(user_id: int) -> dict[str, Any] | None:
    """在异步上下文中访问 Flask 应用上下文"""
    async with app.app_context():
        # current_app 和 g 在异步上下文中可用
        db_uri: str = current_app.config.get("DATABASE_URI", "sqlite:///app.db")
        # 模拟异步数据库查询
        result: dict[str, Any] = await async_db_query(db_uri, user_id)
        return result


async def async_db_query(db_uri: str, user_id: int) -> dict[str, Any]:
    """模拟异步数据库查询"""
    import asyncio
    await asyncio.sleep(0.2)
    return {"id": user_id, "name": "test_user", "uri": db_uri}


@app.route("/async-user/<int:user_id>")
async def get_user(user_id: int) -> dict[str, Any] | tuple[dict[str, str], int]:
    """异步视图中使用异步上下文"""
    user: dict[str, Any] | None = await get_user_from_db(user_id)
    if user is None:
        return {"error": "User not found"}, 404
    return user
```

### 1.4 async 模板渲染

Flask 的 `render_template` 和 `render_template_string` 在 Flask 3.x 中支持异步调用。

```python
# async_render.py
from flask import Flask, render_template_string
from typing import Any

app: Flask = Flask(__name__)

TEMPLATE: str = """
<!DOCTYPE html>
<html>
<head><title>{{ title }}</title></head>
<body>
    <h1>{{ title }}</h1>
    <ul>
    {% for item in items %}
        <li>{{ item.name }} — {{ item.status }}</li>
    {% endfor %}
    </ul>
</body>
</html>
"""


@app.route("/async-page")
async def async_page() -> str:
    """异步渲染模板"""
    items: list[dict[str, str]] = await fetch_items_async()
    return render_template_string(TEMPLATE, title="Async Page", items=items)


async def fetch_items_async() -> list[dict[str, str]]:
    """模拟异步获取数据"""
    import asyncio
    await asyncio.sleep(0.3)
    return [
        {"name": "Item A", "status": "active"},
        {"name": "Item B", "status": "inactive"},
    ]
```

---

## 第二部分：性能考量（L1）

### 2.1 Flask async vs sync 性能对比

异步视图的优势在于 **并发 I/O**，而非 **单次请求速度**。

```
+-------------------------------------------------------------------+
|                    请求响应时间对比                                  |
+-------------------------------------------------------------------+
|                                                                   |
|  同步视图（单个请求）                                                |
|  ┌─────────────────────────────────────────────┐                  |
|  │ 请求 → 处理 → [阻塞 I/O 2s] → 响应           │  总耗时: 2s      |
|  └─────────────────────────────────────────────┘                  |
|                                                                   |
|  异步视图（单个请求）                                                |
|  ┌─────────────────────────────────────────────┐                  |
|  │ 请求 → 处理 → [await I/O 2s] → 响应          │  总耗时: 2s      |
|  └─────────────────────────────────────────────┘                  |
|  (单个请求: async 不比 sync 快)                                    |
|                                                                   |
|  同步视图（100 个并发请求）                                          |
|  ┌──────┐ ┌──────┐ ┌──────┐ ... ┌──────┐                         |
|  │线程 1 │ │线程 2 │ │线程 3 │     │线程 N │  需要大量线程         |
|  │阻塞中 │ │阻塞中 │ │阻塞中 │     │阻塞中 │  内存开销大           |
|  └──────┘ └──────┘ └──────┘     └──────┘                         |
|                                                                   |
|  异步视图（100 个并发请求）                                          |
|  ┌───────────────────────────────────────────────────┐            |
|  │ 单个事件循环管理所有请求                            │            |
|  │ 请求1 await → 让出 → 请求2 await → 让出 → ...     │            |
|  │ I/O 完成时自动恢复对应的协程                        │            |
|  └───────────────────────────────────────────────────┘            |
|  内存开销小，可处理数千并发                                         |
|                                                                   |
+-------------------------------------------------------------------+
```

```python
# performance_comparison.py
"""同步与异步视图性能对比示例"""
import time
import asyncio
from flask import Flask
from typing import Any

app: Flask = Flask(__name__)


# ============ 同步视图 ============
@app.route("/sync-fetch")
def sync_fetch() -> dict[str, float]:
    """同步阻塞 — 每次请求阻塞整个线程"""
    start: float = time.monotonic()
    _blocking_io_operation()
    elapsed: float = time.monotonic() - start
    return {"elapsed": elapsed, "type": "sync"}


def _blocking_io_operation() -> None:
    """模拟阻塞 I/O（如 HTTP 请求、数据库查询）"""
    time.sleep(1)  # 阻塞当前线程 1 秒


# ============ 异步视图 ============
@app.route("/async-fetch")
async def async_fetch() -> dict[str, float]:
    """异步非阻塞 — 等待 I/O 时可处理其他请求"""
    start: float = time.monotonic()
    await _nonblocking_io_operation()
    elapsed: float = time.monotonic() - start
    return {"elapsed": elapsed, "type": "async"}


async def _nonblocking_io_operation() -> None:
    """模拟非阻塞 I/O"""
    await asyncio.sleep(1)  # 让出事件循环，不阻塞


# ============ 错误用法：async 中同步阻塞 ============
@app.route("/bad-async")
async def bad_async() -> dict[str, str]:
    """反模式 — 在 async 视图中使用同步阻塞调用"""
    # 这会阻塞整个事件循环！
    time.sleep(1)  # ❌ 阻塞事件循环
    return {"status": "bad practice"}
```

### 2.2 何时用 async（I/O 密集型）

| 场景 | 原因 |
|------|------|
| 外部 HTTP API 调用 | `aiohttp`/`httpx` 异步客户端 |
| 数据库查询（异步驱动） | `asyncpg`、`aiosqlite`、`motor` |
| 文件读写 | `aiofiles` |
| Redis/Memcached 操作 | `redis.asyncio` |
| 邮件发送 | `aiosmtplib` |
| WebSocket 连接 | 长时间保持连接 |

```python
# async_io_examples.py
"""I/O 密集型场景的异步实现"""
import asyncio
from flask import Flask
from typing import Any

app: Flask = Flask(__name__)


@app.route("/async-multi-fetch")
async def async_multi_fetch() -> dict[str, Any]:
    """并发获取多个外部数据源"""
    # 三个 I/O 操作并发执行，总耗时 ≈ 最慢的那个
    user_data, posts, comments = await asyncio.gather(
        fetch_users_async(),
        fetch_posts_async(),
        fetch_comments_async(),
    )
    return {
        "users": user_data,
        "posts": posts,
        "comments": comments,
    }


async def fetch_users_async() -> list[dict[str, Any]]:
    await asyncio.sleep(0.5)  # 模拟 HTTP 请求
    return [{"id": 1, "name": "Alice"}]


async def fetch_posts_async() -> list[dict[str, Any]]:
    await asyncio.sleep(0.3)  # 模拟数据库查询
    return [{"id": 1, "title": "Hello"}]


async def fetch_comments_async() -> list[dict[str, Any]]:
    await asyncio.sleep(0.4)  # 模拟 Redis 查询
    return [{"id": 1, "text": "Nice!"}]


# 同步串行执行: 0.5 + 0.3 + 0.4 = 1.2s
# 异步并发执行: max(0.5, 0.3, 0.4) = 0.5s
```

### 2.3 何时不用 async（CPU 密集型）

| 场景 | 原因 |
|------|------|
| 图像处理 | 阻塞事件循环，应用 `concurrent.futures` |
| 数据计算 | CPU 密集不释放事件循环 |
| 机器学习推理 | 同步阻塞，应使用后台任务 |
| 文件压缩/解压 | CPU 密集，应放到线程/进程池 |

```python
# cpu_bound_async.py
"""CPU 密集型任务不应使用 async — 正确做法"""
import asyncio
from concurrent.futures import ProcessPoolExecutor
from flask import Flask
from typing import Any

app: Flask = Flask(__name__)


# ❌ 错误: CPU 密集阻塞事件循环
@app.route("/bad-cpu-async")
async def bad_cpu_async() -> dict[str, Any]:
    result: int = _heavy_computation()  # 阻塞事件循环
    return {"result": result}


# ✅ 正确: 使用线程池/进程池执行 CPU 密集任务
@app.route("/good-cpu-async")
async def good_cpu_async() -> dict[str, Any]:
    loop: asyncio.AbstractEventLoop = asyncio.get_event_loop()
    # 在线程池中执行，不阻塞事件循环
    result: int = await loop.run_in_executor(None, _heavy_computation)
    return {"result": result}


def _heavy_computation() -> int:
    """模拟 CPU 密集型计算"""
    total: int = 0
    for i in range(10_000_000):
        total += i
    return total
```

---

## 第三部分：后台任务（L1）

### 3.1 async def 中的后台任务

在异步视图中启动后台任务，可以使用 `asyncio.create_task()`。

```python
# async_background.py
"""Flask 异步视图中的后台任务"""
import asyncio
from flask import Flask, jsonify
from typing import Any

app: Flask = Flask(__name__)

# 存储运行中的后台任务
background_tasks: set[asyncio.Task[Any]] = set()


@app.route("/async-send-email", methods=["POST"])
async def async_send_email() -> tuple[dict[str, str], int]:
    """启动异步后台任务 — 立即响应"""
    # 创建后台任务
    task: asyncio.Task[bool] = asyncio.create_task(
        _send_email_background("user@example.com", "Welcome", "Hello!")
    )
    # 保存任务引用，防止被垃圾回收
    background_tasks.add(task)
    task.add_done_callback(background_tasks.discard)

    return jsonify({"message": "Email queued"}), 202


async def _send_email_background(to: str, subject: str, body: str) -> bool:
    """后台发送邮件 — 不阻塞响应"""
    try:
        await asyncio.sleep(2)  # 模拟发送邮件
        print(f"Email sent to {to}: {subject}")
        return True
    except Exception as e:
        print(f"Email failed: {e}")
        return False
```

### 3.2 与 Celery 集成

对于生产级后台任务，Celery 仍然是首选。

```python
# celery_async_flask.py
"""Flask 异步视图与 Celery 集成"""
from flask import Flask, request
from celery import Celery
from typing import Any

app: Flask = Flask(__name__)
app.config["CELERY_BROKER_URL"] = "redis://localhost:6379/0"
app.config["CELERY_RESULT_BACKEND"] = "redis://localhost:6379/1"


def make_celery(flask_app: Flask) -> Celery:
    celery_app: Celery = Celery(
        flask_app.import_name,
        broker=flask_app.config["CELERY_BROKER_URL"],
        backend=flask_app.config["CELERY_RESULT_BACKEND"],
    )

    class ContextTask(celery_app.Task):
        def __call__(self, *args: Any, **kwargs: Any) -> Any:
            with flask_app.app_context():
                return self.run(*args, **kwargs)

    celery_app.Task = ContextTask
    return celery_app


celery: Celery = make_celery(app)


@celery.task
def process_report_async(report_id: int) -> dict[str, Any]:
    """Celery 异步任务 — 独立进程执行"""
    import time
    time.sleep(5)  # 模拟耗时的报表生成
    return {"report_id": report_id, "status": "completed"}


@app.route("/async-generate-report/<int:report_id>")
async def generate_report(report_id: int) -> tuple[dict[str, Any], int]:
    """异步视图 + Celery 后台任务"""
    task = process_report_async.delay(report_id)
    return {"task_id": task.id, "status": "queued"}, 202


@app.route("/report-status/<task_id>")
def report_status(task_id: str) -> dict[str, Any]:
    from celery.result import AsyncResult
    task_result: AsyncResult = AsyncResult(task_id)
    return {
        "task_id": task_id,
        "state": task_result.state,
        "result": task_result.result if task_result.ready() else None,
    }
```

### 3.3 异步数据库查询（aiosqlite, asyncpg）

```python
# async_database.py
"""Flask 异步视图中的异步数据库操作"""
import asyncio
import aiosqlite
from flask import Flask
from typing import Any

app: Flask = Flask(__name__)

# 全局连接池（生产环境应使用连接池管理）
_db_path: str = "app.db"


async def get_db() -> aiosqlite.Connection:
    """获取异步数据库连接"""
    conn: aiosqlite.Connection = await aiosqlite.connect(_db_path)
    conn.row_factory = aiosqlite.Row
    return conn


@app.route("/async-users")
async def get_users() -> dict[str, Any]:
    """异步数据库查询"""
    conn: aiosqlite.Connection = await get_db()
    try:
        async with conn.execute("SELECT id, name, email FROM users") as cursor:
            rows: list[aiosqlite.Row] = await cursor.fetchall()
            return {
                "users": [{"id": r[0], "name": r[1], "email": r[2]} for r in rows]
            }
    finally:
        await conn.close()


@app.route("/async-user/<int:user_id>")
async def get_user(user_id: int) -> dict[str, Any] | tuple[dict[str, str], int]:
    """异步单条查询"""
    conn: aiosqlite.Connection = await get_db()
    try:
        async with conn.execute(
            "SELECT id, name, email FROM users WHERE id = ?", (user_id,)
        ) as cursor:
            row: aiosqlite.Row | None = await cursor.fetchone()
            if row is None:
                return {"error": "User not found"}, 404
            return {"id": row[0], "name": row[1], "email": row[2]}
    finally:
        await conn.close()


# ============ PostgreSQL + asyncpg ============
# uv add asyncpg
"""
import asyncpg

async def get_pg_pool() -> asyncpg.Pool:
    pool = await asyncpg.create_pool(
        host="localhost",
        database="mydb",
        user="postgres",
        password="secret",
        min_size=5,
        max_size=20,
    )
    return pool

@app.route("/async-pg-users")
async def get_pg_users() -> dict[str, Any]:
    pool = await get_pg_pool()
    async with pool.acquire() as conn:
        rows = await conn.fetch("SELECT id, name, email FROM users")
        return {"users": [dict(r) for r in rows]}
"""
```

---

## 第四部分：L2 实践层

### 4.1 最佳实践

| 实践 | 说明 | 示例 |
|------|------|------|
| 使用异步 HTTP 客户端 | `httpx.AsyncClient` 替代 `requests` | `async with httpx.AsyncClient() as client` |
| 使用异步数据库驱动 | `asyncpg`/`aiosqlite` 替代同步 ORM | `await conn.execute(...)` |
| 使用 `asyncio.gather` 并发 | 多个独立 I/O 操作并发执行 | `await asyncio.gather(a, b, c)` |
| 设置超时 | 防止无限等待 | `asyncio.wait_for(coro, timeout=10)` |
| 错误处理 | async 视图中捕获异常 | `try/except` 包裹 await |
| 连接池 | 复用数据库连接 | `asyncpg.create_pool()` |

```python
# best_practices.py
"""Flask 异步最佳实践"""
import asyncio
import httpx
from flask import Flask
from typing import Any

app: Flask = Flask(__name__)


@app.route("/async-best-practice")
async def async_best_practice() -> dict[str, Any]:
    """综合最佳实践示例"""
    try:
        # 1. 使用超时控制
        async with asyncio.timeout(10):
            # 2. 并发获取多个数据源
            async with httpx.AsyncClient() as client:
                response_a, response_b = await asyncio.gather(
                    client.get("https://api.example.com/a"),
                    client.get("https://api.example.com/b"),
                    return_exceptions=True,
                )

            # 3. 错误处理
            data_a: dict[str, Any] = (
                response_a.json()
                if isinstance(response_a, httpx.Response)
                else {"error": str(response_a)}
            )
            data_b: dict[str, Any] = (
                response_b.json()
                if isinstance(response_b, httpx.Response)
                else {"error": str(response_b)}
            )

            return {"data_a": data_a, "data_b": data_b}

    except asyncio.TimeoutError:
        return {"error": "Request timed out"}, 504
    except Exception as e:
        return {"error": str(e)}, 500
```

### 4.2 反模式

| 反模式 | 问题 | 修正 |
|--------|------|------|
| `async def` 中使用 `time.sleep()` | 阻塞事件循环 | 使用 `await asyncio.sleep()` |
| `async def` 中使用 `requests.get()` | 阻塞事件循环 | 使用 `httpx.AsyncClient` |
| `async def` 中使用同步 SQLite | 阻塞事件循环 | 使用 `aiosqlite` |
| CPU 密集计算放在 async 视图 | 阻塞事件循环 | 使用 `run_in_executor` |
| 忘记 `await` | 协程不执行，返回 Coroutine 对象 | 检查所有异步调用 |

```python
# anti_patterns.py
"""Flask 异步反模式与正确写法"""
import time
import asyncio
import requests
from flask import Flask
from typing import Any

app: Flask = Flask(__name__)


# ============ 反模式 1: async 中 time.sleep ============
@app.route("/anti-pattern-sleep")
async def anti_pattern_sleep() -> dict[str, str]:
    # ❌ 阻塞整个事件循环
    time.sleep(1)
    return {"status": "bad"}


@app.route("/correct-sleep")
async def correct_sleep() -> dict[str, str]:
    # ✅ 让出事件循环
    await asyncio.sleep(1)
    return {"status": "good"}


# ============ 反模式 2: async 中 requests ============
@app.route("/anti-pattern-requests")
async def anti_pattern_requests() -> dict[str, Any]:
    # ❌ 同步阻塞
    resp = requests.get("https://api.example.com/data")
    return resp.json()


@app.route("/correct-requests")
async def correct_requests() -> dict[str, Any]:
    # ✅ 异步 HTTP
    import httpx
    async with httpx.AsyncClient() as client:
        resp = await client.get("https://api.example.com/data")
        return resp.json()


# ============ 反模式 3: 忘记 await ============
@app.route("/anti-pattern-no-await")
async def anti_pattern_no_awit() -> dict[str, Any]:
    # ❌ 返回 Coroutine 对象，不会执行
    result = fetch_data()  # 缺少 await
    return {"data": result}  # TypeError: Object of type coroutine is not JSON serializable


@app.route("/correct-await")
async def correct_await() -> dict[str, Any]:
    # ✅ 正确 await
    result: dict[str, Any] = await fetch_data()
    return {"data": result}


async def fetch_data() -> dict[str, Any]:
    await asyncio.sleep(0.1)
    return {"name": "test"}
```

### 4.3 混合使用 async/sync 的注意事项

```
+-------------------------------------------------------------------+
|              混合 async/sync 调用矩阵                               |
+-------------------------------------------------------------------+
|                                                                   |
|  调用方 \ 被调用方    |  sync 函数     |  async 协程                |
|  ──────────────────── ┼ ───────────── ┼ ─────────────────         |
|  sync 视图             |  直接调用      |  asyncio.run(coro())      |
|                       |  (推荐)        |  (不推荐, 创建新循环)      |
|  ──────────────────── ┼ ───────────── ┼ ─────────────────         |
|  async 视图            |  await loop    |  直接 await                |
|                       |  .run_in_exec  |  (推荐)                   |
|                       |  utor(...)     |                            |
|                       |  (推荐)        |                            |
|                                                                   |
+-------------------------------------------------------------------+
```

```python
# mixed_async_sync.py
"""Flask 中混合使用 async/sync 的正确方式"""
import asyncio
from flask import Flask
from typing import Any

app: Flask = Flask(__name__)


# ============ sync 视图调用 async 函数 ============
def sync_view() -> dict[str, Any]:
    """同步视图中调用异步函数 — 不推荐但可行"""
    # 创建新的事件循环（每次请求都有开销）
    return asyncio.run(_async_helper())


async def _async_helper() -> dict[str, Any]:
    await asyncio.sleep(0.1)
    return {"from": "async"}


# ============ async 视图调用 sync 函数 ============
@app.route("/async-call-sync")
async def async_call_sync() -> dict[str, Any]:
    """异步视图中调用同步函数 — 使用线程池"""
    loop: asyncio.AbstractEventLoop = asyncio.get_event_loop()
    # 在线程池中执行，不阻塞事件循环
    result: dict[str, Any] = await loop.run_in_executor(
        None,  # 使用默认线程池
        _sync_helper,
    )
    return result


def _sync_helper() -> dict[str, Any]:
    """同步函数 — 可能在内部做阻塞操作"""
    time.sleep(0.5)  # 模拟阻塞操作
    import time
    return {"from": "sync"}


import time

# ============ async 视图调用 async 函数 ============
@app.route("/async-call-async")
async def async_call_async() -> dict[str, Any]:
    """异步视图中调用异步函数 — 直接 await"""
    result: dict[str, Any] = await _async_helper()
    return result
```

---

## 第五部分：L3 专家层

### 5.1 Flask 异步实现原理（ASGI vs WSGI）

Flask 本质上是一个 **WSGI** 框架，但 3.0 版本通过适配器实现了 async 视图支持。

```
+-------------------------------------------------------------------+
|                    WSGI vs ASGI 架构对比                            |
+-------------------------------------------------------------------+
|                                                                   |
|  WSGI (Web Server Gateway Interface) — Flask 传统模式              |
|                                                                   |
|  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐    |
|  │ Client   │───>│ Web      │───>│ WSGI     │───>│ Flask    │    |
|  │ Browser  │<───│ Server   │<───│ Server   │<───│ App      │    |
|  │          │    │(Nginx)   │    │(Gunicorn)│    │(sync)    │    |
|  └──────────┘    └──────────┘    └──────────┘    └──────────┘    |
|                                                                   |
|  特点: 同步调用, 一个请求 = 一个线程/进程                           |
|  限制: 不支持 WebSocket, 不支持原生 async                         |
|                                                                   |
|  ─────────────────────────────────────────────────────────────    |
|                                                                   |
|  ASGI (Asynchronous Server Gateway Interface) — Flask 3.x async    |
|                                                                   |
|  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐    |
|  │ Client   │───>│ Web      │───>│ ASGI     │───>│ Flask    │    |
|  │ Browser  │<───│ Server   │<───│ Server   │<───│ App      │    |
|  │          │    │(Nginx)   │    │(Hypercorn│    │(async    │    |
|  │ WebSocket│<──>│          │<──>│/Daphne)  │<──>│ views)    │    |
|  └──────────┘    └──────────┘    └──────────┘    └──────────┘    |
|                                                                   |
|  特点: 异步调用, 一个事件循环管理数千并发                           |
|  优势: 支持 WebSocket, 支持原生 async, 长连接                      |
|                                                                   |
+-------------------------------------------------------------------+
```

```python
# asgi_wsgi_explained.py
"""WSGI 与 ASGI 接口对比 — 原理示意"""
from typing import Any, Callable, Iterable

# ============ WSGI 接口 ============
def wsgi_app(
    environ: dict[str, Any],
    start_response: Callable[[str, list[tuple[str, str]]], Any],
) -> Iterable[bytes]:
    """WSGI 接口 — 同步、基于 callable"""
    status: str = "200 OK"
    response_headers: list[tuple[str, str]] = [("Content-Type", "text/plain")]
    start_response(status, response_headers)
    return [b"Hello from WSGI!"]


# ============ ASGI 接口 ============
async def asgi_app(
    scope: dict[str, Any],
    receive: Callable[[], Any],
    send: Callable[[dict[str, Any]], Any],
) -> None:
    """ASGI 接口 — 异步、基于 coroutine"""
    if scope["type"] == "http":
        await send({
            "type": "http.response.start",
            "status": 200,
            "headers": [[b"content-type", b"text/plain"]],
        })
        await send({
            "type": "http.response.body",
            "body": b"Hello from ASGI!",
        })
    elif scope["type"] == "websocket":
        # WebSocket 仅 ASGI 支持
        await send({"type": "websocket.accept"})
        message: dict[str, Any] = await receive()
        await send({
            "type": "websocket.send",
            "text": f"Echo: {message.get('text')}",
        })
        await send({"type": "websocket.close"})


# Flask 3.x 内部实现原理:
# 当检测到 ASGI 服务器时, Flask 通过 asgi_app 适配器运行
# sync 视图通过 run_sync 包装到线程池执行
# async 视图直接 await 执行
```

### 5.2 为什么 Flask 不全面转向 ASGI（与 Quart 的关系）

```
+-------------------------------------------------------------------+
|                  Flask 与 Quart 的关系                               |
+-------------------------------------------------------------------+
|                                                                   |
|  Quart (由 Flask 同一作者 pgjones 开发)                              |
|  ┌──────────────────────────────────────────────────┐             |
|  │  - 原生 ASGI 框架                                  │             |
|  │  - API 与 Flask 几乎完全兼容                        │             |
|  │  - 全面支持 async/await                           │             |
|  │  - 支持 WebSocket                                  │             |
|  │  - 如果你的项目全面异步 → 选择 Quart                │             |
|  └──────────────────────────────────────────────────┘             |
|                                                                   |
|  Flask 3.x (逐步加入 async 支持)                                     |
|  ┌──────────────────────────────────────────────────┐             |
|  │  - WSGI 为主, ASGI 为辅                           │             |
|  │  - 视图函数支持 async def                         │             |
|  │  - 模板渲染支持异步                                │             |
|  │  - 不全面转向 ASGI 的原因:                         │             |
|  │    1. 大量现有 WSGI 生态依赖                       │             |
|  │    2. 同步代码仍是主流                             │             |
|  │    3. Quart 已满足全面异步需求                     │             |
|  │    4. 渐进式迁移路径更平滑                         │             |
|  └──────────────────────────────────────────────────┘             |
|                                                                   |
|  选型建议:                                                         |
|  ┌──────────────────────────────────────────────────┐             |
|  │  新项目 + 全面异步 + WebSocket → Quart             │             |
|  │  已有 Flask 项目 + 局部异步 → Flask 3.x            │             |
|  │  简单 API / 传统 Web → Flask (sync)               │             |
|  └──────────────────────────────────────────────────┘             |
|                                                                   |
+-------------------------------------------------------------------+
```

### 5.3 gevent 方案（greenlet 协程）

在 Flask 全面转向 async 之前，gevent 是主流的异步方案。

```
+-------------------------------------------------------------------+
|                    gevent 协程模型                                   |
+-------------------------------------------------------------------+
|                                                                   |
|  传统多线程模型:                                                     |
|  ┌────────┐  ┌────────┐  ┌────────┐                               |
|  │ Thread │  │ Thread │  │ Thread │  OS 级别调度, 上下文切换开销大   |
|  │ (1MB)  │  │ (1MB)  │  │ (1MB)  │  内存占用大                    |
|  └────────┘  └────────┘  └────────┘                               |
|                                                                   |
|  gevent greenlet 模型:                                             |
|  ┌─────────────────────────────────────────────────┐              |
|  │                OS Thread (1 个)                  │              |
|  │  ┌─────────┐  ┌─────────┐  ┌─────────┐         │              |
|  │  │greenlet │  │greenlet │  │greenlet │  用户态调度│              |
|  │  │(几 KB)  │  │(几 KB)  │  │(几 KB)  │  内存占用小 │              |
|  │  └─────────┘  └─────────┘  └─────────┘         │              |
|  │                                                   │              |
|  │  自动 patch: time.sleep → gevent.sleep            │              |
|  │           socket → 非阻塞 socket                  │              |
|  │           requests → gevent-http                  │              |
|  └─────────────────────────────────────────────────┘              |
|                                                                   |
+-------------------------------------------------------------------+
```

```python
# gevent_flask.py
"""使用 gevent 使 Flask 支持高并发 — 无需改代码"""
# 安装: uv add gevent gunicorn

# 启动命令:
# gunicorn --worker-class gevent --workers 4 app:app

from flask import Flask
from typing import Any

app: Flask = Flask(__name__)


# 代码不需要任何修改 — gevent 自动 patch 标准库
@app.route("/gevent-fetch")
def gevent_fetch() -> dict[str, Any]:
    """在 gevent 下, 这个同步函数可以处理数千并发"""
    import time

    # gevent 会自动将此转换为非阻塞调用
    time.sleep(1)
    return {"status": "handled by gevent"}


# ============ gevent monkey patch ============
# 在应用入口最顶部添加 (必须在所有 import 之前):
"""
from gevent import monkey
monkey.patch_all()
"""

# ============ gevent 手动使用 greenlet ============
"""
from gevent import spawn, sleep
from gevent.pool import Pool

def worker(task_id: int) -> str:
    sleep(1)  # gevent 的非阻塞 sleep
    return f"Task {task_id} done"

# 创建协程池
pool = Pool(100)
results = [pool.spawn(worker, i) for i in range(1000)]
# 等待所有完成
for r in results:
    r.get()
"""
```

### 5.4 知识关联图

```
+---------------------+          +------------------------+          +--------------------+
| Flask 异步视图       |          | ASGI/WSGI 架构         |          | 并发模型            |
+---------------------+          +------------------------+          +--------------------+
|  async def 视图     |          |  WSGI: 同步, 单请求/线程 |         |  asyncio: 原生协程  |
|  async app_context  |--------->|  ASGI: 异步, 事件循环    |<--------|  gevent: greenlet  |
|  async render       |          |  Flask: WSGI + 适配器   |         |  Celery: 进程池    |
|  反模式避免         |          |  Quart: 原生 ASGI       |         |  ThreadPool: 线程  |
+---------------------+          +------------------------+          +--------------------+
          |                                 |                                 |
          v                                 v                                 v
+---------------------------------------------------------------------------+
|                          设计目标                                          |
|  高并发 I/O · 非阻塞 · 资源高效 · 渐进迁移 · 生态兼容                       |
+---------------------------------------------------------------------------+
```

---

## 总结

```
+-------------------------------------------------------------------+
|                    Flask 异步支持全景图                              |
+-------------------------------------------------------------------+
|                                                                   |
|  Flask 3.x                                                         |
|  ┌───────────────────────────────────────────────────────────┐    |
|  │  async def 视图  ──────────────┐                           │    |
|  │  async with app_context        │   L1 理解层                │    |
|  │  async render_template         │   原生异步支持              │    |
|  │                                │                           │    |
|  │  ── I/O 密集 ──> ✅ async      │   L1 性能                   │    |
|  │  ── CPU 密集 ──> ❌ executor   │   async 用于 I/O, 不用于 CPU │    |
|  │                                │                           │    |
|  │  asyncio.create_task() ────┐   │   L1 后台任务              │    |
|  │  Celery ──────────────> 进程│   │   轻量任务 vs 生产级队列    │    |
|  │  aiosqlite/asyncpg ──> 异步DB│   │   异步数据库驱动            │    |
|  └──────────────────────────┼───┘                           │    |
|                             │                               │    |
|  ┌──────────────────────────┼───────────────────────────┐   │    |
|  │  最佳实践 │ 反模式 │ 混合调用 │                      │   │    |
|  │  L2 实践层                                            │   │    |
|  └───────────────────────────────────────────────────────┘   │    |
|  ┌───────────────────────────────────────────────────────┐   │    |
|  │  WSGI vs ASGI │ Flask vs Quart │ gevent greenlet     │   │    |
|  │  L3 专家层                                              │   │    |
|  └───────────────────────────────────────────────────────┘   │    |
+-------------------------------------------------------------------+
```

| 知识点 | 说明 |
|---------|------|
| `async def` 视图 | Flask 3.x 原生支持异步视图函数 |
| `async with app.app_context()` | 异步上下文中访问 Flask 应用上下文 |
| `asyncio.gather` | 并发执行多个异步 I/O 操作 |
| `run_in_executor` | 在异步视图中执行同步阻塞函数 |
| `aiosqlite` / `asyncpg` | 异步数据库驱动 |
| Celery | 生产级异步任务队列 |
| gevent | 基于 greenlet 的协程方案 |
| ASGI vs WSGI | 异步 vs 同步服务器网关接口 |
| Flask vs Quart | 渐进异步 vs 原生异步 |
