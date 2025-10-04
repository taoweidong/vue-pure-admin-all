"""RBAC接口定义"""

from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any

class RBACInterface(ABC):
    """RBAC系统对外接口"""
    
    @abstractmethod
    async def authenticate_user(self, username: str, password: str) -> Optional[Dict[str, Any]]:
        """用户认证"""
        pass
    
    @abstractmethod
    async def get_user_permissions(self, user_id: str) -> List[str]:
        """获取用户权限列表"""
        pass
    
    @abstractmethod
    async def check_user_permission(self, user_id: str, permission: str) -> bool:
        """检查用户权限"""
        pass
    
    @abstractmethod
    async def get_user_menus(self, user_id: str) -> List[Dict[str, Any]]:
        """获取用户菜单"""
        pass
    
    @abstractmethod
    async def assign_role_to_user(self, user_id: str, role_ids: List[str]) -> bool:
        """为用户分配角色"""
        pass
    
    @abstractmethod
    async def remove_role_from_user(self, user_id: str, role_id: str) -> bool:
        """从用户移除角色"""
        pass