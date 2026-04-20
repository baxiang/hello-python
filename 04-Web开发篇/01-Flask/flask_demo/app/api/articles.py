"""文章RESTful API"""

from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from marshmallow import Schema, ValidationError, fields

from app.services.article_service import ArticleService

articles_bp = Blueprint("articles", __name__)


class ArticleCreateSchema(Schema):
    title = fields.Str(required=True)
    content = fields.Str()
    status = fields.Str(load_default="draft")


class ArticleUpdateSchema(Schema):
    title = fields.Str()
    content = fields.Str()
    status = fields.Str()


@articles_bp.route("", methods=["GET"])
def list_articles():
    """获取文章列表"""
    status = request.args.get("status")
    articles = ArticleService.get_all(status=status)
    return jsonify({"articles": [a.to_dict() for a in articles]}), 200


@articles_bp.route("/<int:article_id>", methods=["GET"])
def get_article(article_id: int):
    """获取单篇文章"""
    article = ArticleService.get_by_id(article_id)
    if not article:
        return jsonify({"error": "文章不存在"}), 404
    return jsonify(article.to_dict()), 200


@articles_bp.route("", methods=["POST"])
@jwt_required()
def create_article():
    """创建文章"""
    schema = ArticleCreateSchema()
    try:
        data = schema.load(request.get_json())
    except ValidationError as e:
        return jsonify({"error": e.messages}), 400

    user_id = get_jwt_identity()
    article = ArticleService.create(
        title=data["title"],
        content=data.get("content", ""),
        author_id=user_id,
        status=data.get("status", "draft"),
    )
    return jsonify(article.to_dict()), 201


@articles_bp.route("/<int:article_id>", methods=["PUT"])
@jwt_required()
def update_article(article_id: int):
    """更新文章"""
    schema = ArticleUpdateSchema()
    try:
        data = schema.load(request.get_json())
    except ValidationError as e:
        return jsonify({"error": e.messages}), 400

    article = ArticleService.update(article_id, **data)
    if not article:
        return jsonify({"error": "文章不存在"}), 404
    return jsonify(article.to_dict()), 200


@articles_bp.route("/<int:article_id>", methods=["DELETE"])
@jwt_required()
def delete_article(article_id: int):
    """删除文章"""
    success = ArticleService.delete(article_id)
    if not success:
        return jsonify({"error": "文章不存在"}), 404
    return jsonify({"message": "删除成功"}), 204
