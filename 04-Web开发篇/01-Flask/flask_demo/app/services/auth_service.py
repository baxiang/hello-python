"""JWT认证服务"""

from flask_jwt_extended import create_access_token, create_refresh_token

from app.extensions import db
from app.models.user import User


class AuthService:
    """认证服务"""

    @staticmethod
    def register(username: str, email: str, password: str) -> User:
        """用户注册"""
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def login(username: str, password: str) -> dict | None:
        """用户登录"""
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            access_token = create_access_token(identity=str(user.id))
            refresh_token = create_refresh_token(identity=str(user.id))
            return {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "user": user.to_dict(),
            }
        return None

    @staticmethod
    def get_user_by_id(user_id: int | str) -> User | None:
        """获取用户"""
        return User.query.get(int(user_id))

    @staticmethod
    def get_user_by_username(username: str) -> User | None:
        """通过用户名获取"""
        return User.query.filter_by(username=username).first()

    @staticmethod
    def get_user_by_email(email: str) -> User | None:
        """通过邮箱获取"""
        return User.query.filter_by(email=email).first()

    @staticmethod
    def get_all_users() -> list[User]:
        """获取所有用户"""
        return User.query.all()
