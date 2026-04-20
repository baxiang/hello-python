"""文件服务"""

from pathlib import Path

from flask import current_app
from werkzeug.utils import secure_filename


class FileService:
    """文件服务"""

    @staticmethod
    def allowed_file(filename: str) -> bool:
        """检查文件扩展名"""
        allowed = current_app.config.get("ALLOWED_EXTENSIONS", set())
        return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed

    @staticmethod
    def save_upload_file(file) -> str:
        """保存上传文件"""
        filename = secure_filename(file.filename)
        upload_folder = Path(current_app.config["UPLOAD_FOLDER"])
        upload_folder.mkdir(parents=True, exist_ok=True)
        filepath = upload_folder / filename
        file.save(str(filepath))
        return filename

    @staticmethod
    def get_file_path(filename: str) -> Path | None:
        """获取文件路径"""
        upload_folder = Path(current_app.config["UPLOAD_FOLDER"])
        filepath = upload_folder / secure_filename(filename)
        if filepath.exists():
            return filepath
        return None
