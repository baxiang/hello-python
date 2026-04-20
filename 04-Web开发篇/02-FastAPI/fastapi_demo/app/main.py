"""
FastAPI 应用入口

创建并配置 FastAPI 应用实例。

Example:
    运行开发服务器::

        $ uvicorn app.main:app --reload

    运行生产服务器::

        $ uvicorn app.main:app --host 0.0.0.0 --port 8000
"""

from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import __version__
from app.api.routes import api_router, health_router
from app.core.config import get_settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    应用生命周期管理

    在应用启动和关闭时执行操作。

    Args:
        app: FastAPI 应用实例
    """
    # 启动时
    settings = get_settings()
    print(f"启动 {settings.APP_NAME} v{__version__}")
    print(f"环境: {settings.APP_ENV}")

    yield

    # 关闭时
    print("关闭应用")


def create_app() -> FastAPI:
    """
    创建 FastAPI 应用实例

    Returns:
        配置好的 FastAPI 应用

    Example:
        >>> app = create_app()
        >>> app.title
        'FastAPI Demo API'
    """
    settings = get_settings()

    app = FastAPI(
        title=settings.API_TITLE,
        description=settings.APP_DESCRIPTION,
        version=__version__,
        lifespan=lifespan,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )

    # CORS 中间件
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # 生产环境应限制
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # 注册路由
    app.include_router(health_router)
    app.include_router(api_router)

    return app


# 创建应用实例
app = create_app()