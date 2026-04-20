"""路由"""

from flask import Blueprint, jsonify, request

api_bp = Blueprint("api", __name__, url_prefix="/api")


@api_bp.route("/hello", methods=["GET"])
def hello():
    """问候接口"""
    return jsonify({"message": "Hello, Flask!"})


@api_bp.route("/users", methods=["GET", "POST"])
def users():
    """用户接口"""
    if request.method == "GET":
        return jsonify({"users": [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]})
    else:
        data = request.get_json()
        return jsonify({"message": "用户创建成功", "user": data}), 201


@api_bp.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    """获取用户"""
    return jsonify({"id": user_id, "name": f"User {user_id}"})