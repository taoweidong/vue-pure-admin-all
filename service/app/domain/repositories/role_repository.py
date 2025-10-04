from abc import ABC, abstractmethod
from typing import Optional, List
from domain.repositories.base_repository import BaseRepository
from domain.models.role import Role

class RoleRepository(BaseRepository[Role], ABC):
    """角色仓储接口"""
    
    @abstractmethod
    async def find_by_name(self, name: str) -> Optional[Role]:
        """根据角色名查找角色"""
        pass
    
    @abstractmethod
    async def find_active_roles(self) -> List[Role]:
        """查找活跃角色"""
        pass
    
    @abstractmethod
    async def find_by_user_id(self, user_id: str) -> List[Role]:
        """根据用户ID查找角色"""
        pass
    
    @abstractmethod
    async def assign_menus(self, role_id: str, menu_ids: List[str]) -> bool:
        """为角色分配菜单"""
        pass