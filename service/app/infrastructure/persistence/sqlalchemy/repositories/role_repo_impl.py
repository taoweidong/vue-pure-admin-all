from typing import Optional, List
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.domain.repositories.role_repository import RoleRepository
from app.domain.models.role import Role
from app.infrastructure.persistence.sqlalchemy.models.role import UserRole

class SQLAlchemyRoleRepository(RoleRepository):
    """SQLAlchemy 角色仓储实现"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, entity: Role) -> Role:
        """创建实体"""
        role_model = self._to_model(entity)
        self.session.add(role_model)
        await self.session.commit()
        await self.session.refresh(role_model)
        role = self._to_domain(role_model)
        if role is None:
            raise ValueError("无法创建角色")
        return role

    async def get_by_id(self, id: str) -> Optional[Role]:
        """根据ID获取实体"""
        result = await self.session.execute(
            select(UserRole).where(UserRole.id == id)
        )
        role_model = result.scalar_one_or_none()
        return self._to_domain(role_model) if role_model else None

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Role]:
        """获取所有实体"""
        result = await self.session.execute(
            select(UserRole).offset(skip).limit(limit)
        )
        role_models = result.scalars().all()
        roles = []
        for model in role_models:
            role = self._to_domain(model)
            if role is not None:
                roles.append(role)
        return roles

    async def filter_by(self, **kwargs) -> List[Role]:
        """根据条件过滤实体"""
        # 简化实现
        result = await self.session.execute(select(UserRole))
        role_models = result.scalars().all()
        roles = []
        for model in role_models:
            role = self._to_domain(model)
            if role is not None:
                roles.append(role)
        return roles

    async def update(self, id: str, **updates) -> Optional[Role]:
        """更新实体"""
        # 简化实现
        role = await self.get_by_id(id)
        return role

    async def delete(self, id: str) -> bool:
        """删除实体"""
        role_model = await self.get_by_id(id)
        if role_model:
            await self.session.delete(role_model)
            await self.session.commit()
            return True
        return False

    async def count(self) -> int:
        """统计数量"""
        result = await self.session.execute(select(func.count()).select_from(UserRole))
        return result.scalar_one()

    async def find_by_name(self, name: str) -> Optional[Role]:
        """根据角色名查找角色"""
        result = await self.session.execute(
            select(UserRole)
            .options(selectinload(UserRole.menus))
            .where(UserRole.name == name)
        )
        role_model = result.scalar_one_or_none()
        return self._to_domain(role_model) if role_model else None

    async def find_active_roles(self) -> List[Role]:
        """查找活跃角色"""
        result = await self.session.execute(
            select(UserRole)
            .options(selectinload(UserRole.menus))
            .where(UserRole.is_active == True)
        )
        role_models = result.scalars().all()
        roles = []
        for model in role_models:
            role = self._to_domain(model)
            if role is not None:
                roles.append(role)
        return roles

    async def find_by_user_id(self, user_id: str) -> List[Role]:
        """根据用户ID查找角色"""
        result = await self.session.execute(
            select(UserRole)
            .options(selectinload(UserRole.menus))
            .join(UserRole.users)
            .where(UserRole.users.any(id=user_id))
        )
        role_models = result.scalars().all()
        roles = []
        for model in role_models:
            role = self._to_domain(model)
            if role is not None:
                roles.append(role)
        return roles

    async def assign_menus(self, role_id: str, menu_ids: List[str]) -> bool:
        """为角色分配菜单"""
        # 这里需要实现菜单分配逻辑
        # 简化实现
        return True

    def _to_domain(self, role_model: UserRole) -> Optional[Role]:
        """转换为领域模型"""
        if not role_model:
            return None
            
        return Role(
            id=getattr(role_model, 'id', ''),
            name=getattr(role_model, 'name', ''),
            description=getattr(role_model, 'description', '') or "",
            is_active=bool(getattr(role_model, 'is_active', False)),
            menus=[],  # TODO: 转换菜单
            data_permissions=[],  # TODO: 转换数据权限
            field_permissions=[]  # TODO: 转换字段权限
        )

    def _to_model(self, role: Role) -> UserRole:
        """转换为数据库模型"""
        return UserRole(
            id=role.id,
            name=role.name,
            description=role.description,
            is_active=role.is_active
        )