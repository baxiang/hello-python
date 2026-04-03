"""REST API 路由"""

from fastapi import APIRouter, Query
from ..services import manager, store

router = APIRouter(prefix="/api", tags=["api"])


@router.get("/users")
async def get_users():
    """获取在线用户"""
    return {
        "users": manager.get_users(),
        "count": len(manager.get_users())
    }


@router.get("/messages")
async def get_messages(limit: int = Query(50, le=200)):
    """获取历史消息"""
    return {
        "messages": store.get_recent(limit)
    }


@router.get("/messages/search")
async def search_messages(
    keyword: str, 
    limit: int = Query(50, le=100)
):
    """搜索消息"""
    return {
        "messages": store.search(keyword, limit)
    }