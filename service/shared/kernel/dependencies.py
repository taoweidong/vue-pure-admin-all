"""依赖注入容器配置"""

from functools import lru_cache
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.persistence.sqlalchemy.database import get_db
from infrastructure.persistence.sqlalchemy.repositories.user_repo_impl import SQLAlchemyUserRepository
from infrastructure.persistence.sqlalchemy.repositories.role_repo_impl import SQLAlchemyRoleRepository
from application.services.user_service import UserService
from application.services.role_service import RoleService
from infrastructure.auth.jwt_handler import JWTHandler
from infrastructure.auth.password_handler import PasswordHandler
from domain.models.user import User
from shared.kernel.config import get_settings

# 安全依赖
security = HTTPBearer()
settings = get_settings()

# 基础设施依赖
@lru_cache()
def get_jwt_handler() -> JWTHandler:
    """获取JWT处理器"""
    return JWTHandler()

@lru_cache()
def get_password_handler() -> PasswordHandler:
    """获取密码处理器"""
    return PasswordHandler()

# 仓储依赖
def get_user_repository(db: AsyncSession = Depends(get_db)) -> SQLAlchemyUserRepository:
    """获取用户仓储"""
    return SQLAlchemyUserRepository(db)

def get_role_repository(db: AsyncSession = Depends(get_db)) -> SQLAlchemyRoleRepository:
    """获取角色仓储"""
    return SQLAlchemyRoleRepository(db)

# 应用服务依赖
def get_user_service(
    user_repo: SQLAlchemyUserRepository = Depends(get_user_repository)
) -> UserService:
    """获取用户服务"""
    return UserService(user_repo)

def get_role_service(
    role_repo: SQLAlchemyRoleRepository = Depends(get_role_repository)
) -> RoleService:
    """获取角色服务"""
    # 临时解决方案，menu_repo设为None
    return RoleService(role_repo, None)

# 认证依赖
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    jwt_handler: JWTHandler = Depends(get_jwt_handler),
    user_service: UserService = Depends(get_user_service)
) -> User:
    """获取当前登录用户"""
    # 验证令牌
    payload = jwt_handler.verify_token(credentials.credentials)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="令牌无效",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 获取用户信息
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="令牌格式错误",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = await user_service.get_user(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户不存在",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户已被禁用",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user

async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """获取当前活跃用户"""
    return current_user