"""数据库模型"""

from app.infrastructure.persistence.sqlalchemy.models.base import BaseModel
from app.infrastructure.persistence.sqlalchemy.models.user import UserInfo as UserModel, user_role_association
from app.infrastructure.persistence.sqlalchemy.models.role import UserRole as RoleModel, DataPermission as DataPermissionModel, FieldPermission as FieldPermissionModel, role_menu_association
from app.infrastructure.persistence.sqlalchemy.models.dept import DeptInfo as DepartmentModel
from app.infrastructure.persistence.sqlalchemy.models.menu import MenuModel

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