"""路由聚合"""

from fastapi import WebSocket

from app.api.auth import router as auth_router
from app.api.tasks import router as tasks_router
from app.api.ws import task_websocket_endpoint

api_router = APIRouter()
api_router.include_router(auth_router)
api_router.include_router(tasks_router)

health_router = APIRouter(tags=["健康检查"])


@health_router.get("/health")
async def health_check() -> dict[str, str]:
    """健康检查"""
    return {"status": "healthy", "service": "Task Manager API"}


@health_router.get("/")
async def root() -> dict[str, str]:
    """根路径"""
    return {
        "message": "Task Manager API",
        "docs": "/docs",
        "redoc": "/redoc",
    }