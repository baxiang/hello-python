"""API 模块"""

from fastapi import APIRouter
from .websocket import router as websocket_router
from .rest import router as rest_router

api_router = APIRouter()
api_router.include_router(websocket_router)
api_router.include_router(rest_router)