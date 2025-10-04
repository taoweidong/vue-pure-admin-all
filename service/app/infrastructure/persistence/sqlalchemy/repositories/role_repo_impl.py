from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from domain.repositories.role_repository import RoleRepository
from domain.models.role import Role
from infrastructure.persistence.sqlalchemy.repositories.base_repo_impl import SQLAlchemyBaseRepository
from infrastructure.persistence.sqlalchemy.models.role import RoleModel

class SQLAlchemyRoleRepository(SQLAlchemyBaseRepository[RoleModel], RoleRepository):
    """SQLAlchemy 角色仓储实现"""

    def __init__(self, session: AsyncSession):
        super().__init__(session, RoleModel)

    async def find_by_name(self, name: str) -> Optional[Role]:
        """根据角色名查找角色"""
        result = await self.session.execute(
            select(RoleModel)
            .options(selectinload(RoleModel.menus))
            .where(RoleModel.name == name)
        )
        role_model = result.scalar_one_or_none()
        return self._to_domain(role_model) if role_model else None

    async def find_active_roles(self) -> List[Role]:
        """查找活跃角色"""
        result = await self.session.execute(
            select(RoleModel)
            .options(selectinload(RoleModel.menus))
            .where(RoleModel.is_active == True)
        )
        role_models = result.scalars().all()
        return [self._to_domain(model) for model in role_models]

    async def find_by_user_id(self, user_id: str) -> List[Role]:
        """根据用户ID查找角色"""
        result = await self.session.execute(
            select(RoleModel)
            .options(selectinload(RoleModel.menus))
            .join(RoleModel.users)
            .where(RoleModel.users.any(id=user_id))
        )
        role_models = result.scalars().all()
        return [self._to_domain(model) for model in role_models]

    async def assign_menus(self, role_id: str, menu_ids: List[str]) -> bool:
        """为角色分配菜单"""
        # 这里需要实现菜单分配逻辑
        # 简化实现
        return True

    def _to_domain(self, role_model: RoleModel) -> Role:
        """转换为领域模型"""
        return Role(
            id=role_model.id,
            name=role_model.name,
            description=role_model.description or "",
            is_active=role_model.is_active,
            menus=[],  # TODO: 转换菜单
            data_permissions=[],  # TODO: 转换数据权限
            field_permissions=[]  # TODO: 转换字段权限
        )