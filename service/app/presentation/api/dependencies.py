from functools import lru_cache
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.persistence.sqlalchemy.database import get_db
from infrastructure.persistence.sqlalchemy.repositories.user_repo_impl import SQLAlchemyUserRepository
from infrastructure.persistence.sqlalchemy.repositories.role_repo_impl import SQLAlchemyRoleRepository
from application.services.user_service import UserService
from application.services.role_service import RoleService
from infrastructure.auth.jwt_handler import JWTHandler
from infrastructure.auth.password_handler import PasswordHandler

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