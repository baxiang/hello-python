"""JWT认证API"""

from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from marshmallow import Schema, ValidationError, fields

from app.services.auth_service import AuthService

auth_bp = Blueprint("auth", __name__)


class RegisterSchema(Schema):
    username = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)


class LoginSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)


@auth_bp.route("/register", methods=["POST"])
def register():
    """用户注册"""
    schema = RegisterSchema()
    try:
        data = schema.load(request.get_json())
    except ValidationError as e:
        return jsonify({"error": e.messages}), 400

    if AuthService.get_user_by_username(data["username"]):
        return jsonify({"error": "用户名已存在"}), 400

    if AuthService.get_user_by_email(data["email"]):
        return jsonify({"error": "邮箱已存在"}), 400

    user = AuthService.register(
        username=data["username"],
        email=data["email"],
        password=data["password"],
    )

    return jsonify({"message": "注册成功", "user": user.to_dict()}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    """用户登录"""
    schema = LoginSchema()
    try:
        data = schema.load(request.get_json())
    except ValidationError as e:
        return jsonify({"error": e.messages}), 400

    result = AuthService.login(data["username"], data["password"])
    if not result:
        return jsonify({"error": "用户名或密码错误"}), 401

    return jsonify(result), 200


@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    """刷新Token"""
    user_id = get_jwt_identity()
    access_token = create_access_token(identity=user_id)
    return jsonify({"access_token": access_token}), 200
