from abc import ABC, abstractmethod
from typing import Optional, List
from app.domain.repositories.base_repository import BaseRepository
from app.domain.models.menu import Menu

class MenuRepository(BaseRepository[Menu], ABC):
    """菜单仓储接口"""
    
    @abstractmethod
    async def find_by_path(self, path: str) -> Optional[Menu]:
        """根据路径查找菜单"""
        pass
    
    @abstractmethod
    async def find_by_type(self, menu_type: int) -> List[Menu]:
        """根据类型查找菜单"""
        pass
    
    @abstractmethod
    async def find_children(self, parent_id: str) -> List[Menu]:
        """查找子菜单"""
        pass
    
    @abstractmethod
    async def find_root_menus(self) -> List[Menu]:
        """查找根菜单"""
        pass
    
    @abstractmethod
    async def build_tree(self) -> List[Menu]:
        """构建菜单树"""
        pass
    
    @abstractmethod
    async def find_by_role_id(self, role_id: str) -> List[Menu]:
        """根据角色ID查找菜单"""
        pass