from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from domain.repositories.user_repository import UserRepository
from domain.models.user import User
from infrastructure.persistence.sqlalchemy.repositories.base_repo_impl import SQLAlchemyBaseRepository
from infrastructure.persistence.sqlalchemy.models.user import UserModel

class SQLAlchemyUserRepository(SQLAlchemyBaseRepository[UserModel], UserRepository):
    """SQLAlchemy 用户仓储实现"""

    def __init__(self, session: AsyncSession):
        super().__init__(session, UserModel)

    async def find_by_username(self, username: str) -> Optional[User]:
        """根据用户名查找用户"""
        result = await self.session.execute(
            select(UserModel)
            .options(selectinload(UserModel.roles))
            .where(UserModel.username == username)
        )
        user_model = result.scalar_one_or_none()
        return self._to_domain(user_model) if user_model else None

    async def find_by_email(self, email: str) -> Optional[User]:
        """根据邮箱查找用户"""
        result = await self.session.execute(
            select(UserModel)
            .options(selectinload(UserModel.roles))
            .where(UserModel.email == email)
        )
        user_model = result.scalar_one_or_none()
        return self._to_domain(user_model) if user_model else None

    async def find_by_dept(self, dept_id: str) -> List[User]:
        """根据部门ID查找用户"""
        result = await self.session.execute(
            select(UserModel)
            .options(selectinload(UserModel.roles))
            .where(UserModel.dept_id == dept_id)
        )
        user_models = result.scalars().all()
        return [self._to_domain(model) for model in user_models]

    async def find_active_users(self) -> List[User]:
        """查找活跃用户"""
        result = await self.session.execute(
            select(UserModel)
            .options(selectinload(UserModel.roles))
            .where(UserModel.is_active == True)
        )
        user_models = result.scalars().all()
        return [self._to_domain(model) for model in user_models]

    async def update_last_login(self, user_id: str) -> bool:
        """更新最后登录时间"""
        # 简化实现，实际需要添加last_login字段
        return True

    def _to_domain(self, user_model: UserModel) -> User:
        """转换为领域模型"""
        return User(
            id=user_model.id,
            username=user_model.username,
            nickname=user_model.nickname,
            email=user_model.email,
            phone=user_model.phone or "",
            is_active=user_model.is_active,
            dept_id=user_model.dept_id,
            roles=[],  # TODO: 转换角色
            created_time=user_model.created_time,
            updated_time=user_model.updated_time
        )

    def _to_model(self, user: User) -> UserModel:
        """转换为数据库模型"""
        return UserModel(
            id=user.id,
            username=user.username,
            nickname=user.nickname,
            email=user.email,
            phone=user.phone,
            is_active=user.is_active,
            dept_id=user.dept_id,
            created_time=user.created_time,
            updated_time=user.updated_time
        )