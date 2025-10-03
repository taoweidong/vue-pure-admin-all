"""
RBAC领域值对象
"""
from typing import List, Optional, Set, Dict
from dataclasses import dataclass
from enum import Enum


class PermissionAction(Enum):
    """权限操作枚举"""
    CREATE = "create"
    READ = "read"
    UPDATE = "update"
    DELETE = "delete"
    EXECUTE = "execute"
    APPROVE = "approve"
    EXPORT = "export"
    IMPORT = "import"


class ResourceType(Enum):
    """资源类型枚举"""
    MENU = "menu"
    BUTTON = "button"
    API = "api"
    DATA = "data"
    FILE = "file"


class DataScopeType(Enum):
    """数据权限范围类型"""
    ALL = "all"                 # 全部数据
    CUSTOM = "custom"           # 自定义数据
    DEPT = "dept"              # 本部门数据
    DEPT_AND_CHILD = "dept_and_child"  # 本部门及子部门数据
    SELF = "self"              # 仅本人数据


@dataclass(frozen=True)
class PermissionCode:
    """权限编码值对象"""
    resource: str
    action: str
    
    def __post_init__(self):
        if not self.resource or not self.action:
            raise ValueError("资源和操作不能为空")
    
    def to_string(self) -> str:
        return f"{self.resource}:{self.action}"
    
    @classmethod
    def from_string(cls, permission_str: str) -> "PermissionCode":
        if ":" not in permission_str:
            raise ValueError("权限编码格式错误，应为 resource:action")
        resource, action = permission_str.split(":", 1)
        return cls(resource=resource, action=action)


@dataclass(frozen=True)
class DataScope:
    """数据权限范围值对象"""
    scope_type: DataScopeType
    scope_values: Optional[Set[str]] = None
    
    def __post_init__(self):
        if self.scope_type == DataScopeType.CUSTOM and not self.scope_values:
            raise ValueError("自定义数据范围必须指定具体值")
    
    def includes(self, value: str) -> bool:
        """检查是否包含指定值"""
        if self.scope_type == DataScopeType.ALL:
            return True
        elif self.scope_type == DataScopeType.CUSTOM:
            return value in (self.scope_values or set())
        return False


@dataclass
class UserPermissions:
    """用户权限集合值对象"""
    permissions: Set[PermissionCode]
    data_scopes: Dict[str, DataScope]
    
    def has_permission(self, permission: PermissionCode) -> bool:
        """检查是否有指定权限"""
        return permission in self.permissions
    
    def has_resource_permission(self, resource: str, action: str) -> bool:
        """检查是否有资源权限"""
        permission = PermissionCode(resource=resource, action=action)
        return self.has_permission(permission)
    
    def get_data_scope(self, resource_type: str) -> Optional[DataScope]:
        """获取数据权限范围"""
        return self.data_scopes.get(resource_type)
    
    def can_access_data(self, resource_type: str, data_owner: str) -> bool:
        """检查是否可以访问数据"""
        scope = self.get_data_scope(resource_type)
        if not scope:
            return False
        return scope.includes(data_owner)