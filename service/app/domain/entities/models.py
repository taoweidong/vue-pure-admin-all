# 导入新的领域实体
from app.domain.user.entities.user import User, UserRole, UserSession, UserProfile
from app.domain.role.entities.role import Role, RoleMenu, RoleInheritance, Permission, RolePermission, Resource, DataScope
from app.domain.menu.entities.menu import Menu, MenuPermission, MenuOperation
from app.domain.organization.entities.department import Department, Position, UserPosition, DepartmentHistory
from app.domain.audit.entities.log import LoginLog, OperationLog, SystemLog, AuditLog, SecurityEvent
from app.domain.entities.online_user import OnlineUser

# 重新导出所有实体，保持向后兼容
__all__ = [
    "User", "UserRole", "UserSession", "UserProfile",
    "Role", "RoleMenu", "RoleInheritance", 
    "Menu", "MenuPermission", "MenuOperation",
    "Department", "Position", "UserPosition", "DepartmentHistory",
    "Permission", "RolePermission", "Resource", "DataScope",
    "LoginLog", "OperationLog", "SystemLog", "AuditLog", "SecurityEvent",
    "OnlineUser"
]