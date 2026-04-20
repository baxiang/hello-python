"""文件上传API"""

from pathlib import Path

from flask import Blueprint, jsonify, request, send_from_directory
from flask_jwt_extended import jwt_required

from app.services.file_service import FileService

files_bp = Blueprint("files", __name__)


@files_bp.route("/upload", methods=["POST"])
@jwt_required()
def upload_file():
    """上传文件"""
    if "file" not in request.files:
        return jsonify({"error": "未提供文件"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "未选择文件"}), 400

    if not FileService.allowed_file(file.filename):
        return jsonify({"error": "不允许的文件类型"}), 400

    filename = FileService.save_upload_file(file)
    return jsonify({"message": "上传成功", "filename": filename}), 201


@files_bp.route("/<filename>", methods=["GET"])
def download_file(filename: str):
    """下载文件"""
    filepath = FileService.get_file_path(filename)
    if not filepath:
        return jsonify({"error": "文件不存在"}), 404

    upload_folder = Path(filepath).parent
    return send_from_directory(str(upload_folder), filename)
