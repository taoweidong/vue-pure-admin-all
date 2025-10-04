from typing import Optional
from domain.models.user import User
from domain.repositories.user_repository import UserRepository
from domain.repositories.role_repository import RoleRepository

class AuthService:
    """认证领域服务"""
    
    def __init__(self, user_repo: UserRepository, role_repo: RoleRepository):
        self.user_repo = user_repo
        self.role_repo = role_repo
    
    async def authenticate_user(self, username: str, password: str) -> Optional[User]:
        """用户认证"""
        user = await self.user_repo.find_by_username(username)
        if not user or not user.is_active:
            return None
        
        # 验证密码逻辑（简化，实际需要密码加密验证）
        # if not verify_password(password, user.hashed_password):
        #     return None
        
        # 加载用户角色
        roles = await self.role_repo.find_by_user_id(user.id)
        user.roles = roles
        
        return user
    
    async def check_user_permission(self, user: User, permission: str) -> bool:
        """检查用户权限"""
        return user.has_permission(permission)
    
    async def is_user_admin(self, user: User) -> bool:
        """检查用户是否为管理员"""
        return user.is_admin()