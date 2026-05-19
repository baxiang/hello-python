"""第 4 章权限验证路由 — @require_role 装饰器演示"""

from dataclasses import dataclass

from fastapi import APIRouter, Header

from app.decorators.ch04_parameterized import require_role

router = APIRouter(prefix="/api/v1/auth", tags=["ch04: 权限验证"])


@dataclass
class RequestContext:
    """模拟请求上下文"""

    role: str


@require_role("admin")
def _delete_user(user_id: int, request: RequestContext) -> dict:
    return {"status": 200, "deleted": user_id}


@require_role("user")
def _view_profile(request: RequestContext) -> dict:
    return {"status": 200, "profile": {"role": request.role}}


@router.delete("/users/{user_id}")
def api_delete_user(
    user_id: int,
    x_role: str = Header(default="guest"),
) -> dict:
    """删除用户 — 仅 admin 可访问"""
    return _delete_user(user_id, request=RequestContext(role=x_role))


@router.get("/profile")
def api_view_profile(x_role: str = Header(default="guest")) -> dict:
    """查看资料 — user 及以上可访问"""
    return _view_profile(request=RequestContext(role=x_role))
