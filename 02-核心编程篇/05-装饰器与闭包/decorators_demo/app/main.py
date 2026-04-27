"""装饰器与闭包示例项目 — FastAPI 应用入口

每章的装饰器通过对应的 API 路由进行演示：
- ch03: /api/v1/demo          — 日志 + 计时装饰器
- ch04: /api/v1/auth/...      — 权限验证装饰器
- ch04: /api/v1/retry         — 重试装饰器
- ch05: /api/v1/cache         — 缓存装饰器
- ch06: /api/v1/async         — 异步装饰器
"""

from fastapi import FastAPI

from app.routers import demo

app = FastAPI(
    title="Python 装饰器与闭包示例",
    description="每章的装饰器通过 API 路由进行演示",
    version="0.2.0",
)

app.include_router(demo.router)
