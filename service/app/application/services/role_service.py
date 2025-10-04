from typing import List, Optional
import uuid
from datetime import datetime

from domain.models.role import Role
from domain.repositories.role_repository import RoleRepository
from domain.repositories.menu_repository import MenuRepository
from application.dto.role_dto import RoleCreate, RoleUpdate
from shared.kernel.exceptions import BusinessException

class RoleService:
    """角色应用服务"""
    
    def __init__(self, role_repo: RoleRepository, menu_repo: Optional[MenuRepository] = None):
        self.role_repo = role_repo
        self.menu_repo = menu_repo

    async def list_roles(self, skip: int = 0, limit: int = 100) -> List[Role]:
        """获取角色列表"""
        return await self.role_repo.get_all(skip=skip, limit=limit)

    async def get_role(self, role_id: str) -> Optional[Role]:
        """获取角色详情"""
        return await self.role_repo.get_by_id(role_id)

    async def create_role(self, role_in: RoleCreate) -> Role:
        """创建角色"""
        # 检查角色名唯一性
        existing_role = await self.role_repo.find_by_name(role_in.name)
        if existing_role:
            raise BusinessException("角色名已存在")
        
        # 创建角色领域对象
        role = Role(
            id=str(uuid.uuid4()),
            name=role_in.name,
            description=role_in.description or "",
            is_active=True,
            menus=[],
            data_permissions=[],
            field_permissions=[]
        )
        
        # 这里需要转换为数据库模型并保存
        # 简化实现，实际需要在仓储层处理
        return role

    async def update_role(self, role_id: str, role_update: RoleUpdate) -> Optional[Role]:
        """更新角色信息"""
        role = await self.role_repo.get_by_id(role_id)
        if not role:
            return None
            
        updates = role_update.dict(exclude_unset=True)
        
        # 如果更新名称，检查唯一性
        if 'name' in updates:
            existing_role = await self.role_repo.find_by_name(updates['name'])
            if existing_role and existing_role.id != role_id:
                raise BusinessException("角色名已存在")
        
        return await self.role_repo.update(role_id, **updates)

    async def delete_role(self, role_id: str) -> bool:
        """删除角色"""
        return await self.role_repo.delete(role_id)

    async def assign_menus_to_role(self, role_id: str, menu_ids: List[str]) -> Optional[Role]:
        """为角色分配菜单权限"""
        role = await self.role_repo.get_by_id(role_id)
        if not role:
            return None
            
        if not self.menu_repo:
            # 如果没有菜单仓储，返回原角色
            return role
            
        # 验证菜单存在性
        menus = []
        for menu_id in menu_ids:
            menu = await self.menu_repo.get_by_id(menu_id)
            if menu:
                menus.append(menu)
                
        # 分配菜单
        success = await self.role_repo.assign_menus(role_id, menu_ids)
        if success:
            role.menus = menus
            return role
        return None

    async def get_role_menus(self, role_id: str) -> List:
        """获取角色的菜单列表"""
        if not self.menu_repo:
            return []
        return await self.menu_repo.find_by_role_id(role_id)

    async def count_roles(self) -> int:
        """统计角色数量"""
        return await self.role_repo.count()