"""
RBAC领域实体初始化
"""
from .permission import Permission, RolePermission, Resource, DataScope

__all__ = [
    "Permission",
    "RolePermission", 
    "Resource",
    "DataScope"
]