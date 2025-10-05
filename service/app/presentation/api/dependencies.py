from functools import lru_cache
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.persistence.sqlalchemy.database import get_db
from app.infrastructure.persistence.sqlalchemy.repositories.user_repo_impl import SQLAlchemyUserRepository
from app.infrastructure.persistence.sqlalchemy.repositories.role_repo_impl import SQLAlchemyRoleRepository
from app.application.services.user_service import UserService
from app.application.services.role_service import RoleService
from app.infrastructure.auth.jwt_handler import JWTHandler
from app.infrastructure.auth.password_handler import PasswordHandler

# JWT安全方案
security = HTTPBearer()

# 仓储依赖
def get_user_repository(db: AsyncSession = Depends(get_db)) -> SQLAlchemyUserRepository:
    """获取用户仓储实例"""
    return SQLAlchemyUserRepository(db)

def get_role_repository(db: AsyncSession = Depends(get_db)) -> SQLAlchemyRoleRepository:
    """获取角色仓储实例"""
    return SQLAlchemyRoleRepository(db)

# 服务依赖
def get_user_service(
    user_repo: SQLAlchemyUserRepository = Depends(get_user_repository)
) -> UserService:
    """获取用户服务实例"""
    return UserService(user_repo)

def get_role_service(
    role_repo: SQLAlchemyRoleRepository = Depends(get_role_repository),
    # menu_repo: SQLAlchemyMenuRepository = Depends(get_menu_repository)
) -> RoleService:
    """获取角色服务实例"""
    # 临时解决方案，实际需要菜单仓储
    return RoleService(role_repo, None)

# 认证相关依赖
@lru_cache()
def get_jwt_handler() -> JWTHandler:
    """获取JWT处理器"""
    return JWTHandler()

@lru_cache()
def get_password_handler() -> PasswordHandler:
    """获取密码处理器"""
    return PasswordHandler()

# 获取当前用户依赖
async def get_current_user(
    credentials = Depends(security),
    user_service: UserService = Depends(get_user_service),
    jwt_handler: JWTHandler = Depends(get_jwt_handler)
):
    """获取当前认证用户"""
    try:
        payload = jwt_handler.verify_token(credentials.credentials)
        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="令牌无效"
            )
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="令牌无效"
            )
        user = await user_service.get_user(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="用户不存在"
            )
        return user
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="认证失败"
        )