"""
用户聚合根
"""
from typing import List, Optional, Set
from datetime import datetime

from app.domain.user.entities.user import User, UserRole, UserSession, UserProfile
from app.domain.role.value_objects.permission import UserPermissions


class UserAggregate:
    """用户聚合根"""
    
    def __init__(self, user: User):
        self._user = user
        self._roles: List[UserRole] = []
        self._sessions: List[UserSession] = []
        self._profile: Optional[UserProfile] = None
        self._permissions: Optional[UserPermissions] = None
        self._domain_events: List = []
    
    @property
    def user(self) -> User:
        return self._user
    
    @property
    def id(self) -> int:
        return self._user.id
    
    @property
    def username(self) -> str:
        return self._user.username
    
    @property
    def roles(self) -> List[UserRole]:
        return self._roles
    
    @property
    def sessions(self) -> List[UserSession]:
        return self._sessions
    
    @property
    def profile(self) -> Optional[UserProfile]:
        return self._profile
    
    @property
    def permissions(self) -> Optional[UserPermissions]:
        return self._permissions
    
    @property
    def domain_events(self) -> List:
        return self._domain_events
    
    def set_roles(self, roles: List[UserRole]):
        """设置用户角色"""
        self._roles = roles
        self._add_domain_event("user_roles_changed", {
            "user_id": self.id,
            "role_ids": [role.role_id for role in roles]
        })
    
    def set_sessions(self, sessions: List[UserSession]):
        """设置用户会话"""
        self._sessions = sessions
    
    def set_profile(self, profile: UserProfile):
        """设置用户档案"""
        self._profile = profile
    
    def set_permissions(self, permissions: UserPermissions):
        """设置用户权限"""
        self._permissions = permissions
    
    def is_active(self) -> bool:
        """检查用户是否激活"""
        return self._user.status == 1 and not self._user.is_locked
    
    def has_role(self, role_code: str) -> bool:
        """检查用户是否有指定角色"""
        for user_role in self._roles:
            if user_role.role.code == role_code and user_role.is_active:
                return True
        return False
    
    def has_any_role(self, role_codes: List[str]) -> bool:
        """检查用户是否有任一指定角色"""
        for user_role in self._roles:
            if user_role.role.code in role_codes and user_role.is_active:
                return True
        return False
    
    def has_permission(self, resource: str, action: str) -> bool:
        """检查用户是否有指定权限"""
        if not self._permissions:
            return False
        return self._permissions.has_resource_permission(resource, action)
    
    def get_active_sessions(self) -> List[UserSession]:
        """获取活跃会话"""
        now = datetime.now()
        return [
            session for session in self._sessions 
            if session.is_active and session.expires_at > now
        ]
    
    def add_session(self, session: UserSession):
        """添加会话"""
        self._sessions.append(session)
        self._add_domain_event("user_session_created", {
            "user_id": self.id,
            "session_id": session.session_id,
            "ip_address": session.ip_address
        })
    
    def remove_session(self, session_id: str):
        """移除会话"""
        for session in self._sessions:
            if session.session_id == session_id:
                session.is_active = False
                self._add_domain_event("user_session_removed", {
                    "user_id": self.id,
                    "session_id": session_id
                })
                break
    
    def lock(self, reason: str):
        """锁定用户"""
        self._user.is_locked = True
        self._user.lock_reason = reason
        
        # 清除所有会话
        for session in self._sessions:
            session.is_active = False
        
        self._add_domain_event("user_locked", {
            "user_id": self.id,
            "reason": reason
        })
    
    def unlock(self):
        """解锁用户"""
        self._user.is_locked = False
        self._user.lock_reason = None
        self._user.failed_login_attempts = 0
        
        self._add_domain_event("user_unlocked", {
            "user_id": self.id
        })
    
    def record_login_attempt(self, success: bool, ip: str):
        """记录登录尝试"""
        if success:
            self._user.failed_login_attempts = 0
            self._user.last_login_at = datetime.now()
            self._user.last_login_ip = ip
            
            self._add_domain_event("user_login_success", {
                "user_id": self.id,
                "ip": ip
            })
        else:
            self._user.failed_login_attempts += 1
            
            # 如果失败次数过多，自动锁定
            if self._user.failed_login_attempts >= 5:
                self.lock("登录失败次数过多")
            
            self._add_domain_event("user_login_failed", {
                "user_id": self.id,
                "ip": ip,
                "attempts": self._user.failed_login_attempts
            })
    
    def change_password(self, new_password_hash: str):
        """修改密码"""
        self._user.password_hash = new_password_hash
        self._user.password_changed_at = datetime.now()
        
        # 清除所有会话，强制重新登录
        for session in self._sessions:
            session.is_active = False
        
        self._add_domain_event("user_password_changed", {
            "user_id": self.id
        })
    
    def update_profile(self, profile_data: dict):
        """更新用户档案"""
        if self._profile:
            for key, value in profile_data.items():
                if hasattr(self._profile, key):
                    setattr(self._profile, key, value)
        
        self._add_domain_event("user_profile_updated", {
            "user_id": self.id,
            "changes": profile_data
        })
    
    def _add_domain_event(self, event_type: str, data: dict):
        """添加领域事件"""
        event = {
            "type": event_type,
            "data": data,
            "timestamp": datetime.now()
        }
        self._domain_events.append(event)
    
    def clear_domain_events(self):
        """清除领域事件"""
        self._domain_events.clear()
    
    @classmethod
    def create(cls, username: str, password_hash: str, nickname: str, **kwargs) -> "UserAggregate":
        """创建用户聚合"""
        user = User(
            username=username,
            password_hash=password_hash,
            nickname=nickname,
            **kwargs
        )
        
        aggregate = cls(user)
        aggregate._add_domain_event("user_created", {
            "user_id": user.id,
            "username": username
        })
        
        return aggregate