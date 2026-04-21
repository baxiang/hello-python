"""认证服务"""

from datetime import timedelta

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.core.security import create_access_token, get_password_hash, verify_password
from app.models.user import User
from app.schemas.user import UserCreate

settings = get_settings()


class AuthService:
    """认证服务类"""

    async def get_by_username(self, db: AsyncSession, username: str) -> User | None:
        """根据用户名获取用户"""
        result = await db.execute(select(User).where(User.username == username))
        return result.scalar_one_or_none()

    async def get_by_email(self, db: AsyncSession, email: str) -> User | None:
        """根据邮箱获取用户"""
        result = await db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def get_by_id(self, db: AsyncSession, user_id: int) -> User | None:
        """根据ID获取用户"""
        result = await db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def register(self, db: AsyncSession, user_data: UserCreate) -> User:
        """注册用户"""
        user = User(
            username=user_data.username,
            email=user_data.email,
            hashed_password=get_password_hash(user_data.password),
            is_active=True,
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user

    async def authenticate(
        self, db: AsyncSession, username: str, password: str
    ) -> User | None:
        """验证用户凭证"""
        user = await self.get_by_username(db, username)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def create_token(self, user_id: int) -> str:
        """创建访问令牌"""
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        return create_access_token(
            data={"sub": str(user_id)},
            expires_delta=access_token_expires,
        )


auth_service = AuthService()
