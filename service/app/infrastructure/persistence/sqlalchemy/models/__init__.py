"""数据库模型"""

from infrastructure.persistence.sqlalchemy.models.base import BaseModel
from infrastructure.persistence.sqlalchemy.models.user import UserModel, user_role_association
from infrastructure.persistence.sqlalchemy.models.role import RoleModel, DataPermissionModel, FieldPermissionModel, role_menu_association
from infrastructure.persistence.sqlalchemy.models.dept import DepartmentModel
from infrastructure.persistence.sqlalchemy.models.menu import MenuModel

__all__ = [
    "BaseModel",
    "UserModel",
    "RoleModel", 
    "DataPermissionModel",
    "FieldPermissionModel",
    "DepartmentModel",
    "MenuModel",
    "user_role_association",
    "role_menu_association"
]