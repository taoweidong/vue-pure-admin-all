from typing import Optional, List
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from datetime import datetime

from app.domain.repositories.user_repository import UserRepository
from app.domain.models.user import User
from app.infrastructure.persistence.sqlalchemy.models.user import UserInfo

class SQLAlchemyUserRepository(UserRepository):
    """SQLAlchemy 用户仓储实现"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, entity: User) -> User:
        """创建实体"""
        user_model = self._to_model(entity)
        self.session.add(user_model)
        await self.session.commit()
        await self.session.refresh(user_model)
        user = self._to_domain(user_model)
        if user is None:
            raise ValueError("无法创建用户")
        return user

    async def get_by_id(self, id: str) -> Optional[User]:
        """根据ID获取实体"""
        result = await self.session.execute(
            select(UserInfo).where(UserInfo.id == id)
        )
        user_model = result.scalar_one_or_none()
        return self._to_domain(user_model) if user_model else None

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[User]:
        """获取所有实体"""
        result = await self.session.execute(
            select(UserInfo).offset(skip).limit(limit)
        )
        user_models = result.scalars().all()
        users = []
        for model in user_models:
            user = self._to_domain(model)
            if user is not None:
                users.append(user)
        return users

    async def filter_by(self, **kwargs) -> List[User]:
        """根据条件过滤实体"""
        # 简化实现
        result = await self.session.execute(select(UserInfo))
        user_models = result.scalars().all()
        users = []
        for model in user_models:
            user = self._to_domain(model)
            if user is not None:
                users.append(user)
        return users

    async def update(self, id: str, **updates) -> Optional[User]:
        """更新实体"""
        # 简化实现
        user = await self.get_by_id(id)
        return user

    async def delete(self, id: str) -> bool:
        """删除实体"""
        user_model = await self.get_by_id(id)
        if user_model:
            await self.session.delete(user_model)
            await self.session.commit()
            return True
        return False

    async def count(self) -> int:
        """统计数量"""
        result = await self.session.execute(select(func.count()).select_from(UserInfo))
        return result.scalar_one()

    async def find_by_username(self, username: str) -> Optional[User]:
        """根据用户名查找用户"""
        result = await self.session.execute(
            select(UserInfo)
            .options(selectinload(UserInfo.roles))
            .where(UserInfo.username == username)
        )
        user_model = result.scalar_one_or_none()
        return self._to_domain(user_model) if user_model else None

    async def find_by_email(self, email: str) -> Optional[User]:
        """根据邮箱查找用户"""
        result = await self.session.execute(
            select(UserInfo)
            .options(selectinload(UserInfo.roles))
            .where(UserInfo.email == email)
        )
        user_model = result.scalar_one_or_none()
        return self._to_domain(user_model) if user_model else None

    async def find_by_dept(self, dept_id: str) -> List[User]:
        """根据部门ID查找用户"""
        result = await self.session.execute(
            select(UserInfo)
            .options(selectinload(UserInfo.roles))
            .where(UserInfo.dept_id == dept_id)
        )
        user_models = result.scalars().all()
        users = []
        for model in user_models:
            user = self._to_domain(model)
            if user is not None:
                users.append(user)
        return users

    async def find_active_users(self) -> List[User]:
        """查找活跃用户"""
        result = await self.session.execute(
            select(UserInfo)
            .options(selectinload(UserInfo.roles))
            .where(UserInfo.is_active == True)
        )
        user_models = result.scalars().all()
        users = []
        for model in user_models:
            user = self._to_domain(model)
            if user is not None:
                users.append(user)
        return users

    async def update_last_login(self, user_id: str) -> bool:
        """更新最后登录时间"""
        # 简化实现，实际需要添加last_login字段
        return True

    def _to_domain(self, user_model: UserInfo) -> Optional[User]:
        """转换为领域模型"""
        if not user_model:
            return None
            
        return User(
            id=str(getattr(user_model, 'id', '')),
            username=getattr(user_model, 'username', ''),
            nickname=getattr(user_model, 'nickname', ''),
            email=getattr(user_model, 'email', ''),
            phone=getattr(user_model, 'phone', '') or "",
            is_active=bool(getattr(user_model, 'is_active', False)),
            dept_id=getattr(user_model, 'dept_id', None),
            roles=[],  # TODO: 转换角色
            created_time=getattr(user_model, 'created_time', datetime.now()),
            updated_time=getattr(user_model, 'updated_time', datetime.now())
        )

    def _to_model(self, user: User) -> UserInfo:
        """转换为数据库模型"""
        return UserInfo(
            id=int(user.id) if user.id.isdigit() else 0,
            username=user.username,
            nickname=user.nickname,
            email=user.email,
            phone=user.phone,
            is_active=user.is_active,
            dept_id=user.dept_id,
            created_time=user.created_time,
            updated_time=user.updated_time
        )