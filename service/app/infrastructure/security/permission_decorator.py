"""
权限装饰器和中间件
"""
from functools import wraps
from typing import List, Optional, Callable, Any
from fastapi import HTTPException, Depends, status
from sqlalchemy.orm import Session

from app.infrastructure.database.database import get_db
from app.domain.rbac.services.permission_service import PermissionDomainService
from app.presentation.api.v1.auth import get_current_user


def require_permission(resource: str, action: str):
    """权限检查装饰器"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # 从kwargs中获取当前用户和数据库会话
            current_user = kwargs.get('current_user')
            db = kwargs.get('db')
            
            if not current_user or not db:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Authentication required"
                )
            
            # 检查权限
            permission_service = PermissionDomainService(db)
            if not permission_service.check_permission(current_user.id, resource, action):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Permission denied: {resource}:{action}"
                )
            
            return await func(*args, **kwargs)
        return wrapper
    return decorator


def require_any_permission(permissions: List[tuple]):
    """要求任一权限的装饰器"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            current_user = kwargs.get('current_user')
            db = kwargs.get('db')
            
            if not current_user or not db:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Authentication required"
                )
            
            permission_service = PermissionDomainService(db)
            
            # 检查是否有任一权限
            has_permission = False
            for resource, action in permissions:
                if permission_service.check_permission(current_user.id, resource, action):
                    has_permission = True
                    break
            
            if not has_permission:
                permission_strs = [f"{r}:{a}" for r, a in permissions]
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Permission denied. Required any of: {', '.join(permission_strs)}"
                )
            
            return await func(*args, **kwargs)
        return wrapper
    return decorator


def require_all_permissions(permissions: List[tuple]):
    """要求所有权限的装饰器"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            current_user = kwargs.get('current_user')
            db = kwargs.get('db')
            
            if not current_user or not db:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Authentication required"
                )
            
            permission_service = PermissionDomainService(db)
            
            # 检查是否有所有权限
            missing_permissions = []
            for resource, action in permissions:
                if not permission_service.check_permission(current_user.id, resource, action):
                    missing_permissions.append(f"{resource}:{action}")
            
            if missing_permissions:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Permission denied. Missing: {', '.join(missing_permissions)}"
                )
            
            return await func(*args, **kwargs)
        return wrapper
    return decorator


def require_role(role_code: str):
    """角色检查装饰器"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            current_user = kwargs.get('current_user')
            db = kwargs.get('db')
            
            if not current_user or not db:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Authentication required"
                )
            
            # 检查用户是否有指定角色
            from app.domain.user.entities.user import UserRole
            from app.domain.role.entities.role import Role
            
            has_role = db.query(UserRole).join(Role).filter(
                UserRole.user_id == current_user.id,
                UserRole.is_active == True,
                Role.code == role_code,
                Role.status == 1
            ).first() is not None
            
            if not has_role:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Role required: {role_code}"
                )
            
            return await func(*args, **kwargs)
        return wrapper
    return decorator


def require_any_role(role_codes: List[str]):
    """要求任一角色的装饰器"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            current_user = kwargs.get('current_user')
            db = kwargs.get('db')
            
            if not current_user or not db:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Authentication required"
                )
            
            from app.domain.user.entities.user import UserRole
            from app.domain.role.entities.role import Role
            
            has_role = db.query(UserRole).join(Role).filter(
                UserRole.user_id == current_user.id,
                UserRole.is_active == True,
                Role.code.in_(role_codes),
                Role.status == 1
            ).first() is not None
            
            if not has_role:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Role required. Any of: {', '.join(role_codes)}"
                )
            
            return await func(*args, **kwargs)
        return wrapper
    return decorator


def data_permission_filter(resource_type: str):
    """数据权限过滤装饰器"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            current_user = kwargs.get('current_user')
            db = kwargs.get('db')
            
            if not current_user or not db:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Authentication required"
                )
            
            # 获取用户可访问的部门ID列表
            permission_service = PermissionDomainService(db)
            accessible_dept_ids = permission_service.get_user_accessible_dept_ids(current_user.id)
            
            # 将可访问的部门ID列表添加到kwargs中，供业务逻辑使用
            kwargs['accessible_dept_ids'] = accessible_dept_ids
            
            return await func(*args, **kwargs)
        return wrapper
    return decorator


class PermissionChecker:
    """权限检查器"""
    
    def __init__(self, db: Session):
        self.db = db
        self.permission_service = PermissionDomainService(db)
    
    def check_permission(self, user_id: int, resource: str, action: str) -> bool:
        """检查权限"""
        return self.permission_service.check_permission(user_id, resource, action)
    
    def check_data_permission(self, user_id: int, resource_type: str, data_owner: str) -> bool:
        """检查数据权限"""
        return self.permission_service.check_data_permission(user_id, resource_type, data_owner)
    
    def get_accessible_dept_ids(self, user_id: int) -> set:
        """获取可访问的部门ID"""
        return self.permission_service.get_user_accessible_dept_ids(user_id)


def get_permission_checker(db: Session = Depends(get_db)) -> PermissionChecker:
    """获取权限检查器依赖"""
    return PermissionChecker(db)