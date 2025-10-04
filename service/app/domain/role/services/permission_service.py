"""
权限领域服务
"""
from typing import List, Set, Dict, Optional
from sqlalchemy.orm import Session

from app.domain.role.entities.role import Permission, RolePermission, DataScope as DataScopeEntity, Role
from app.domain.role.value_objects.permission import (
    PermissionCode, DataScope, DataScopeType, UserPermissions
)
from app.domain.user.entities.user import User, UserRole


class PermissionDomainService:
    """权限领域服务"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_user_permissions(self, user_id: int) -> UserPermissions:
        """获取用户的完整权限"""
        # 获取用户所有角色
        user_roles = self.db.query(UserRole).filter(
            UserRole.user_id == user_id,
            UserRole.is_active == True
        ).all()
        
        if not user_roles:
            return UserPermissions(permissions=set(), data_scopes={})
        
        role_ids = [ur.role_id for ur in user_roles]
        
        # 获取角色权限
        permissions = self._get_roles_permissions(role_ids)
        
        # 获取数据权限范围
        data_scopes = self._get_roles_data_scopes(role_ids)
        
        return UserPermissions(permissions=permissions, data_scopes=data_scopes)
    
    def _get_roles_permissions(self, role_ids: List[int]) -> Set[PermissionCode]:
        """获取角色的权限集合"""
        role_permissions = self.db.query(RolePermission).join(Permission).filter(
            RolePermission.role_id.in_(role_ids),
            RolePermission.granted == True,
            Permission.status == 1
        ).all()
        
        permissions = set()
        for rp in role_permissions:
            permission_code = PermissionCode(
                resource=rp.permission.resource,
                action=rp.permission.action
            )
            permissions.add(permission_code)
        
        return permissions
    
    def _get_roles_data_scopes(self, role_ids: List[int]) -> Dict[str, DataScope]:
        """获取角色的数据权限范围"""
        data_scope_entities = self.db.query(DataScopeEntity).filter(
            DataScopeEntity.role_id.in_(role_ids)
        ).all()
        
        data_scopes = {}
        for ds in data_scope_entities:
            scope_type = DataScopeType(ds.scope_type)
            scope_values = None
            
            if ds.scope_value and scope_type == DataScopeType.CUSTOM:
                import json
                try:
                    scope_values = set(json.loads(ds.scope_value))
                except (json.JSONDecodeError, TypeError):
                    scope_values = set()
            
            data_scope = DataScope(scope_type=scope_type, scope_values=scope_values)
            
            # 如果同一资源类型有多个范围，取最宽松的
            if ds.resource_type in data_scopes:
                existing_scope = data_scopes[ds.resource_type]
                if self._is_wider_scope(data_scope, existing_scope):
                    data_scopes[ds.resource_type] = data_scope
            else:
                data_scopes[ds.resource_type] = data_scope
        
        return data_scopes
    
    def _is_wider_scope(self, scope1: DataScope, scope2: DataScope) -> bool:
        """判断scope1是否比scope2权限更宽"""
        scope_order = {
            DataScopeType.ALL: 4,
            DataScopeType.DEPT_AND_CHILD: 3,
            DataScopeType.DEPT: 2,
            DataScopeType.CUSTOM: 1,
            DataScopeType.SELF: 0
        }
        return scope_order[scope1.scope_type] > scope_order[scope2.scope_type]
    
    def check_permission(self, user_id: int, resource: str, action: str) -> bool:
        """检查用户是否有指定权限"""
        user_permissions = self.get_user_permissions(user_id)
        return user_permissions.has_resource_permission(resource, action)
    
    def check_data_permission(self, user_id: int, resource_type: str, data_owner: str) -> bool:
        """检查用户是否有数据权限"""
        user_permissions = self.get_user_permissions(user_id)
        return user_permissions.can_access_data(resource_type, data_owner)
    
    def get_user_accessible_dept_ids(self, user_id: int) -> Set[int]:
        """获取用户可访问的部门ID列表"""
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            return set()
        
        user_permissions = self.get_user_permissions(user_id)
        dept_scope = user_permissions.get_data_scope("department")
        
        if not dept_scope:
            return set()
        
        if dept_scope.scope_type == DataScopeType.ALL:
            # 返回所有部门ID
            from app.domain.organization.entities.department import Department
            all_depts = self.db.query(Department.id).filter(Department.status == 1).all()
            return {dept.id for dept in all_depts}
        
        elif dept_scope.scope_type == DataScopeType.DEPT:
            # 返回用户所在部门
            return {user.dept_id} if user.dept_id else set()
        
        elif dept_scope.scope_type == DataScopeType.DEPT_AND_CHILD:
            # 返回用户所在部门及子部门
            if not user.dept_id:
                return set()
            return self._get_dept_and_children_ids(user.dept_id)
        
        elif dept_scope.scope_type == DataScopeType.CUSTOM:
            # 返回自定义部门列表
            if dept_scope.scope_values:
                return {int(dept_id) for dept_id in dept_scope.scope_values if dept_id.isdigit()}
            return set()
        
        elif dept_scope.scope_type == DataScopeType.SELF:
            # 仅返回用户所在部门
            return {user.dept_id} if user.dept_id else set()
        
        return set()
    
    def _get_dept_and_children_ids(self, dept_id: int) -> Set[int]:
        """获取部门及其所有子部门ID"""
        from app.domain.organization.entities.department import Department
        
        result = {dept_id}
        
        # 递归获取子部门
        children = self.db.query(Department).filter(
            Department.parent_id == dept_id,
            Department.status == 1
        ).all()
        
        for child in children:
            result.update(self._get_dept_and_children_ids(child.id))
        
        return result


class RoleHierarchyService:
    """角色层级服务"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_role_hierarchy(self, role_id: int) -> List[int]:
        """获取角色层级链（从根到当前角色）"""
        role = self.db.query(Role).filter(Role.id == role_id).first()
        if not role:
            return []
        
        hierarchy = []
        current_role = role
        
        while current_role and current_role.parent_id != 0:
            hierarchy.insert(0, current_role.parent_id)
            current_role = self.db.query(Role).filter(Role.id == current_role.parent_id).first()
        
        hierarchy.append(role_id)
        return hierarchy
    
    def can_assign_role(self, assigner_user_id: int, target_role_id: int) -> bool:
        """检查是否可以分配角色"""
        # 获取分配者的最高级别角色
        assigner_roles = self.db.query(UserRole).join(Role).filter(
            UserRole.user_id == assigner_user_id,
            UserRole.is_active == True,
            Role.status == 1
        ).all()
        
        if not assigner_roles:
            return False
        
        max_level = max(ur.role.level for ur in assigner_roles)
        
        # 获取目标角色级别
        target_role = self.db.query(Role).filter(Role.id == target_role_id).first()
        if not target_role:
            return False
        
        # 只能分配级别不高于自己的角色
        return target_role.level <= max_level