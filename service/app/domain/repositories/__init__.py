"""仓储接口定义"""

from domain.repositories.base_repository import BaseRepository
from domain.repositories.user_repository import UserRepository
from domain.repositories.role_repository import RoleRepository
from domain.repositories.dept_repository import DeptRepository
from domain.repositories.menu_repository import MenuRepository

__all__ = [
    "BaseRepository",
    "UserRepository",
    "RoleRepository", 
    "DeptRepository",
    "MenuRepository"
]