# Task Manager API

FastAPI任务管理API示例项目，演示JWT认证、CRUD、WebSocket实时通知、后台任务等功能。

## 功能

- 用户注册/登录 (JWT认证)
- 任务CRUD (创建、读取、更新、删除)
- 任务过滤 (按状态/优先级)
- WebSocket实时通知
- 后台任务 (日志记录、完成通知)
- 请求日志中间件

## 安装

```bash
uv sync
```

## 运行

```bash
uv run uvicorn app.main:app --reload
```

## API文档

启动后访问:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 端点

### 认证

| 方法 | 端点 | 说明 |
|------|------|------|
| POST | `/api/auth/register` | 用户注册 |
| POST | `/api/auth/login` | 用户登录 |
| GET | `/api/auth/me` | 获取当前用户 |

### 任务

| 方法 | 端点 | 说明 |
|------|------|------|
| GET | `/api/tasks` | 任务列表 |
| POST | `/api/tasks` | 创建任务 |
| GET | `/api/tasks/{id}` | 获取任务 |
| PUT | `/api/tasks/{id}` | 更新任务 |
| DELETE | `/api/tasks/{id}` | 删除任务 |

### WebSocket

| 端点 | 说明 |
|------|------|
| WS `/api/ws/tasks` | 实时任务通知 |

## 测试

```bash
uv run pytest tests/ -v
```

## 知识点覆盖

| 章节 | 实现位置 |
|------|----------|
| 01-FastAPI入门 | `app/main.py`, `app/api/tasks.py` |
| 02-Pydantic模型 | `app/schemas/` |
| 03-依赖注入 | `app/api/deps.py` |
| 04-数据库集成 | `app/core/database.py`, `app/models/` |
| 05-认证授权 | `app/core/security.py`, `app/api/auth.py` |
| 06-中间件 | `app/middleware/logging.py`, `app/main.py` |
| 07-错误处理 | `app/api/` (HTTPException) |
| 08-WebSocket | `app/api/ws.py` |
| 09-后台任务 | `app/api/tasks.py` (BackgroundTasks) |
| 10-测试与部署 | `tests/` |