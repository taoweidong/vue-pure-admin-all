"""仓储接口定义"""

from app.domain.repositories.base_repository import BaseRepository
from app.domain.repositories.user_repository import UserRepository
from app.domain.repositories.role_repository import RoleRepository
from app.domain.repositories.dept_repository import DeptRepository
from app.domain.repositories.menu_repository import MenuRepository

__all__ = [
    "BaseRepository",
    "UserRepository",
    "RoleRepository", 
    "DeptRepository",
    "MenuRepository"
]