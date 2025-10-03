"""
用户领域应用服务
"""
from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

from app.domain.user.entities.user import User, UserRole, UserSession, UserProfile
from app.domain.role.entities.role import Role
from app.domain.organization.entities.department import Department
from app.domain.rbac.services.permission_service import PermissionDomainService
from app.presentation.schemas.user import UserCreate, UserUpdate
from app.infrastructure.utils.auth import AuthService


class UserApplicationService:
    """用户应用服务"""
    
    def __init__(self, db: Session):
        self.db = db
        self.auth_service = AuthService()
        self.permission_service = PermissionDomainService(db)
    
    def create_user(self, user_data: UserCreate, creator_id: int) -> User:
        """创建用户"""
        # 检查用户名是否已存在
        if self.get_user_by_username(user_data.username):
            raise ValueError("用户名已存在")
        
        # 检查邮箱是否已存在
        if user_data.email and self.get_user_by_email(user_data.email):
            raise ValueError("邮箱已存在")
        
        # 检查手机号是否已存在
        if user_data.phone and self.get_user_by_phone(user_data.phone):
            raise ValueError("手机号已存在")
        
        # 创建用户
        password_hash = self.auth_service.get_password_hash(user_data.password)
        
        user = User(
            username=user_data.username,
            nickname=user_data.nickname,
            email=user_data.email,
            phone=user_data.phone,
            avatar=user_data.avatar,
            password_hash=password_hash,
            description=user_data.description,
            sex=user_data.sex,
            dept_id=user_data.dept_id,
            remark=user_data.remark
        )
        
        self.db.add(user)
        self.db.flush()
        
        # 创建用户档案
        if hasattr(user_data, 'profile') and user_data.profile:
            profile = UserProfile(
                user_id=user.id,
                **user_data.profile.dict(exclude_unset=True)
            )
            self.db.add(profile)
        
        self.db.commit()
        self.db.refresh(user)
        
        # 记录操作日志
        self._log_user_operation(creator_id, "create", user.id, f"创建用户: {user.username}")
        
        return user
    
    def update_user(self, user_id: int, user_data: UserUpdate, updater_id: int) -> User:
        """更新用户"""
        user = self.get_user_by_id(user_id)
        if not user:
            raise ValueError("用户不存在")
        
        # 检查邮箱是否已被其他用户使用
        if user_data.email and user_data.email != user.email:
            existing_user = self.get_user_by_email(user_data.email)
            if existing_user and existing_user.id != user_id:
                raise ValueError("邮箱已被其他用户使用")
        
        # 检查手机号是否已被其他用户使用
        if user_data.phone and user_data.phone != user.phone:
            existing_user = self.get_user_by_phone(user_data.phone)
            if existing_user and existing_user.id != user_id:
                raise ValueError("手机号已被其他用户使用")
        
        # 更新用户信息
        old_values = {}
        update_data = user_data.dict(exclude_unset=True, exclude={'profile'})
        
        for key, value in update_data.items():
            if hasattr(user, key):
                old_values[key] = getattr(user, key)
                setattr(user, key, value)
        
        # 更新用户档案
        if hasattr(user_data, 'profile') and user_data.profile:
            profile = self.db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
            if profile:
                profile_data = user_data.profile.dict(exclude_unset=True)
                for key, value in profile_data.items():
                    if hasattr(profile, key):
                        setattr(profile, key, value)
            else:
                profile = UserProfile(user_id=user_id, **user_data.profile.dict(exclude_unset=True))
                self.db.add(profile)
        
        self.db.commit()
        self.db.refresh(user)
        
        # 记录操作日志
        self._log_user_operation(updater_id, "update", user.id, f"更新用户: {user.username}")
        
        return user
    
    def delete_user(self, user_id: int, deleter_id: int) -> bool:
        """删除用户"""
        user = self.get_user_by_id(user_id)
        if not user:
            return False
        
        # 检查是否可以删除（不能删除超级管理员等）
        if not self._can_delete_user(user_id, deleter_id):
            raise ValueError("无权限删除该用户")
        
        # 软删除：设置状态为禁用
        user.status = 0
        user.is_locked = True
        user.lock_reason = "用户已被删除"
        
        # 禁用用户的所有角色
        self.db.query(UserRole).filter(UserRole.user_id == user_id).update({"is_active": False})
        
        # 清除用户会话
        self.db.query(UserSession).filter(UserSession.user_id == user_id).update({"is_active": False})
        
        self.db.commit()
        
        # 记录操作日志
        self._log_user_operation(deleter_id, "delete", user.id, f"删除用户: {user.username}")
        
        return True
    
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """根据ID获取用户"""
        return self.db.query(User).filter(User.id == user_id).first()
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        """根据用户名获取用户"""
        return self.db.query(User).filter(User.username == username).first()
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """根据邮箱获取用户"""
        return self.db.query(User).filter(User.email == email).first()
    
    def get_user_by_phone(self, phone: str) -> Optional[User]:
        """根据手机号获取用户"""
        return self.db.query(User).filter(User.phone == phone).first()
    
    def get_users_paginated(
        self,
        page: int = 1,
        page_size: int = 10,
        username: Optional[str] = None,
        nickname: Optional[str] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        status: Optional[int] = None,
        dept_id: Optional[int] = None,
        accessible_dept_ids: Optional[set] = None
    ) -> Tuple[List[User], int]:
        """获取分页用户列表"""
        query = self.db.query(User)
        
        # 数据权限过滤
        if accessible_dept_ids is not None:
            if accessible_dept_ids:
                query = query.filter(User.dept_id.in_(accessible_dept_ids))
            else:
                # 如果没有可访问的部门，返回空结果
                return [], 0
        
        # 添加过滤条件
        if username:
            query = query.filter(User.username.contains(username))
        if nickname:
            query = query.filter(User.nickname.contains(nickname))
        if email:
            query = query.filter(User.email.contains(email))
        if phone:
            query = query.filter(User.phone == phone)
        if status is not None:
            query = query.filter(User.status == status)
        if dept_id:
            query = query.filter(User.dept_id == dept_id)
        
        # 获取总数
        total = query.count()
        
        # 分页
        offset = (page - 1) * page_size
        users = query.offset(offset).limit(page_size).all()
        
        return users, total
    
    def assign_roles(self, user_id: int, role_ids: List[int], assigner_id: int) -> bool:
        """分配角色给用户"""
        user = self.get_user_by_id(user_id)
        if not user:
            raise ValueError("用户不存在")
        
        # 检查权限
        for role_id in role_ids:
            if not self._can_assign_role(assigner_id, role_id):
                raise ValueError(f"无权限分配角色ID: {role_id}")
        
        # 删除现有角色
        self.db.query(UserRole).filter(UserRole.user_id == user_id).delete()
        
        # 添加新角色
        for role_id in role_ids:
            user_role = UserRole(
                user_id=user_id,
                role_id=role_id,
                granted_by=assigner_id
            )
            self.db.add(user_role)
        
        self.db.commit()
        
        # 记录操作日志
        role_names = [str(rid) for rid in role_ids]
        self._log_user_operation(
            assigner_id, "assign_roles", user_id, 
            f"为用户 {user.username} 分配角色: {', '.join(role_names)}"
        )
        
        return True
    
    def lock_user(self, user_id: int, reason: str, locker_id: int) -> bool:
        """锁定用户"""
        user = self.get_user_by_id(user_id)
        if not user:
            raise ValueError("用户不存在")
        
        user.is_locked = True
        user.lock_reason = reason
        
        # 清除用户会话
        self.db.query(UserSession).filter(UserSession.user_id == user_id).update({"is_active": False})
        
        self.db.commit()
        
        # 记录操作日志
        self._log_user_operation(locker_id, "lock", user_id, f"锁定用户: {user.username}, 原因: {reason}")
        
        return True
    
    def unlock_user(self, user_id: int, unlocker_id: int) -> bool:
        """解锁用户"""
        user = self.get_user_by_id(user_id)
        if not user:
            raise ValueError("用户不存在")
        
        user.is_locked = False
        user.lock_reason = None
        user.failed_login_attempts = 0
        
        self.db.commit()
        
        # 记录操作日志
        self._log_user_operation(unlocker_id, "unlock", user_id, f"解锁用户: {user.username}")
        
        return True
    
    def reset_password(self, user_id: int, new_password: str, resetter_id: int) -> bool:
        """重置密码"""
        user = self.get_user_by_id(user_id)
        if not user:
            raise ValueError("用户不存在")
        
        password_hash = self.auth_service.get_password_hash(new_password)
        user.password_hash = password_hash
        user.password_changed_at = func.now()
        user.failed_login_attempts = 0
        
        # 清除用户会话，强制重新登录
        self.db.query(UserSession).filter(UserSession.user_id == user_id).update({"is_active": False})
        
        self.db.commit()
        
        # 记录操作日志
        self._log_user_operation(resetter_id, "reset_password", user_id, f"重置用户密码: {user.username}")
        
        return True
    
    def _can_delete_user(self, user_id: int, deleter_id: int) -> bool:
        """检查是否可以删除用户"""
        # 不能删除自己
        if user_id == deleter_id:
            return False
        
        # 检查目标用户是否是超级管理员
        target_user_roles = self.db.query(UserRole).join(Role).filter(
            UserRole.user_id == user_id,
            UserRole.is_active == True,
            Role.code == "super_admin",
            Role.status == 1
        ).first()
        
        if target_user_roles:
            # 只有超级管理员才能删除超级管理员
            deleter_roles = self.db.query(UserRole).join(Role).filter(
                UserRole.user_id == deleter_id,
                UserRole.is_active == True,
                Role.code == "super_admin",
                Role.status == 1
            ).first()
            return deleter_roles is not None
        
        return True
    
    def _can_assign_role(self, assigner_id: int, role_id: int) -> bool:
        """检查是否可以分配角色"""
        from app.domain.rbac.services.permission_service import RoleHierarchyService
        hierarchy_service = RoleHierarchyService(self.db)
        return hierarchy_service.can_assign_role(assigner_id, role_id)
    
    def _log_user_operation(self, operator_id: int, operation: str, target_user_id: int, description: str):
        """记录用户操作日志"""
        from app.domain.audit.entities.log import OperationLog
        
        log = OperationLog(
            user_id=operator_id,
            module="user_management",
            operation=operation,
            business_id=str(target_user_id),
            business_type="user",
            remark=description
        )
        self.db.add(log)
        self.db.flush()