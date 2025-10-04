from typing import List
from domain.models.user import User
from domain.models.role import Role
from domain.models.menu import Menu
from domain.repositories.user_repository import UserRepository
from domain.repositories.role_repository import RoleRepository
from domain.repositories.menu_repository import MenuRepository

class PermissionService:
    """权限领域服务"""
    
    def __init__(
        self, 
        user_repo: UserRepository, 
        role_repo: RoleRepository,
        menu_repo: MenuRepository
    ):
        self.user_repo = user_repo
        self.role_repo = role_repo
        self.menu_repo = menu_repo
    
    async def get_user_menus(self, user_id: str) -> List[Menu]:
        """获取用户可访问的菜单"""
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            return []
        
        all_menus = []
        for role in user.roles:
            role_menus = await self.menu_repo.find_by_role_id(role.id)
            all_menus.extend(role_menus)
        
        # 去重
        unique_menus = {}
        for menu in all_menus:
            unique_menus[menu.id] = menu
        
        return list(unique_menus.values())
    
    async def check_menu_access(self, user_id: str, menu_path: str) -> bool:
        """检查用户是否可以访问指定菜单"""
        user_menus = await self.get_user_menus(user_id)
        return any(menu.path == menu_path for menu in user_menus)
    
    async def assign_role_to_user(self, user_id: str, role_ids: List[str]) -> bool:
        """为用户分配角色"""
        # 这里需要在仓储层实现具体的角色分配逻辑
        return True
    
    async def remove_role_from_user(self, user_id: str, role_id: str) -> bool:
        """从用户移除角色"""
        # 这里需要在仓储层实现具体的角色移除逻辑
        return True