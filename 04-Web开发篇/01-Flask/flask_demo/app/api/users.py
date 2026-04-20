"""用户API"""

from flask import Blueprint, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.services.auth_service import AuthService

users_bp = Blueprint("users", __name__)


@users_bp.route("", methods=["GET"])
@jwt_required()
def list_users():
    """用户列表"""
    users = AuthService.get_all_users()
    return jsonify({"users": [u.to_dict() for u in users]})


@users_bp.route("/<int:user_id>", methods=["GET"])
@jwt_required()
def get_user(user_id: int):
    """用户详情"""
    user = AuthService.get_user_by_id(user_id)
    if not user:
        return jsonify({"error": "用户不存在"}), 404
    return jsonify(user.to_dict())


@users_bp.route("/me", methods=["GET"])
@jwt_required()
def get_current_user():
    """当前用户"""
    user_id = get_jwt_identity()
    user = AuthService.get_user_by_id(user_id)
    return jsonify(user.to_dict())
