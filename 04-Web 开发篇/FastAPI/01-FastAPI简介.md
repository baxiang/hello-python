# FastAPI 简介

## 为什么选择 FastAPI

FastAPI 是一个现代、高性能的 Python Web 框架，基于 Starlette 和 Pydantic，专为构建 API 而设计。

**核心特性：**

```
┌─────────────────────────────────────────────────────────────┐
│                  FastAPI 核心特性                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   🚀 高性能                                                  │
│   • 基于 Starlette 和 uvicorn，性能媲美 NodeJS 和 Go         │
│   • 异步支持，高并发场景表现优异                            │
│                                                             │
│   📝 自动文档                                                │
│   • 自动生成 OpenAPI 规范                                    │
│   • 内置 Swagger UI (/docs) 和 ReDoc (/redoc)               │
│                                                             │
│   ✅ 类型检查                                                │
│   • 基于 Python 类型提示                                     │
│   • 自动数据验证和转换                                       │
│   • IDE 智能提示和错误检查                                   │
│                                                             │
│   🔧 依赖注入                                                │
│   • 强大的依赖注入系统                                       │
│   • 可组合、可测试、可复用                                   │
│                                                             │
│   🛡️ 生产就绪                                                │
│   • Docker 支持                                              │
│   • 完善的认证方案                                           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**FastAPI vs Flask 对比：**

| 特性 | Flask | FastAPI |
|------|-------|---------|
| 类型 | 同步 | 异步 (async/await) |
| 数据验证 | 手动 | Pydantic 自动 |
| API 文档 | 需手动配置 | 自动生成 |
| 类型提示 | 可选 | 核心特性 |
| 学习曲线 | 低 | 中等 |
| 性能 | 中等 | 高 |
| WebSocket | 需扩展 | 原生支持 |

---

## 安装与运行

FastAPI 需要配合 ASGI 服务器（如 uvicorn）运行。

**安装：**

```bash
# 创建项目
uv init my-fastapi-app
cd my-fastapi-app

# 安装 FastAPI 和 uvicorn
uv add fastapi uvicorn[standard]

# 开发环境运行
uv run uvicorn main:app --reload

# 生产环境运行
uv run uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

**第一个 FastAPI 应用：**

```python
# main.py
from fastapi import FastAPI

app = FastAPI(
    title="我的 API",
    description="一个示例 API",
    version="1.0.0"
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}
```

**访问：**
- API 根地址：http://localhost:8000
- Swagger 文档：http://localhost:8000/docs
- ReDoc 文档：http://localhost:8000/redoc

---

## 路径操作

### 路径装饰器

FastAPI 使用装饰器定义 HTTP 方法和路径的对应关系。

**HTTP 方法装饰器：**

```python
from fastapi import FastAPI

app = FastAPI()


@app.get("/items")
async def list_items():
    """获取物品列表"""
    return {"items": []}


@app.post("/items")
async def create_item():
    """创建新物品"""
    return {"message": "创建成功"}


@app.put("/items/{item_id}")
async def update_item(item_id: int):
    """更新物品"""
    return {"item_id": item_id}


@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    """删除物品"""
    return {"message": "删除成功"}
```

### 路径参数

路径参数使用花括号 `{}` 包裹，函数参数名需与路径参数名一致。

```python
@app.get("/users/{user_id}")
async def get_user(user_id: int):
    """获取用户 - user_id 自动转换为 int"""
    return {"user_id": user_id}


@app.get("/users/{user_id}/posts/{post_id}")
async def get_user_post(user_id: int, post_id: int):
    """多层路径参数"""
    return {"user_id": user_id, "post_id": post_id}
```

**路径参数验证：**

```python
from fastapi import Path

@app.get("/items/{item_id}")
async def read_item(
    item_id: int = Path(..., title="物品 ID", gt=0, le=1000)
):
    """
    gt=0: 必须大于 0
    le=1000: 必须小于等于 1000
    """
    return {"item_id": item_id}
```

### 查询参数

查询参数是 URL 中 `?` 后面的参数，作为函数的可选参数。

```python
from fastapi import Query
from typing import Optional

@app.get("/items")
async def list_items(
    q: Optional[str] = Query(None, min_length=1, max_length=50),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    tags: list[str] = Query([])  # 多个值：?tags=python&tags=fastapi
):
    return {
        "q": q,
        "page": page,
        "limit": limit,
        "tags": tags
    }
```