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
from logging import INFO, basicConfig

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

from app import __version__
from app.api.routes import api_router, health_router
from app.api.ws import task_websocket_endpoint
from app.core.config import get_settings
from app.core.database import init_db
from app.middleware.logging import LoggingMiddleware

basicConfig(level=INFO)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    settings = get_settings()
    print(f"启动 {settings.APP_NAME} v{__version__}")
    print(f"环境: {settings.APP_ENV}")

    await init_db()

    yield

    print("关闭应用")


def create_app() -> FastAPI:
    """创建 FastAPI 应用实例"""
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

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_middleware(GZipMiddleware, minimum_size=1000)

    app.add_middleware(LoggingMiddleware)

    app.include_router(health_router)
    app.include_router(api_router, prefix="/api")

    app.add_api_websocket_route("/api/ws/tasks", task_websocket_endpoint)

    return app


app = create_app()
