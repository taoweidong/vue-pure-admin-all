from fastapi import APIRouter
from app.presentation.api.v1 import users, roles, menus, departments, user_roles, role_menus, logs, auth

# 创建API v1路由器
api_v1 = APIRouter(prefix="/api/v1")

# 注册各模块路由
api_v1.include_router(auth.router, prefix="/auth", tags=["认证授权"])
api_v1.include_router(users.router, prefix="/users", tags=["用户管理"])
api_v1.include_router(roles.router, prefix="/roles", tags=["角色管理"])
api_v1.include_router(menus.router, prefix="/menus", tags=["菜单管理"])
api_v1.include_router(departments.router, prefix="/departments", tags=["部门管理"])
api_v1.include_router(user_roles.router, prefix="/user-roles", tags=["用户角色"])
api_v1.include_router(role_menus.router, prefix="/role-menus", tags=["角色菜单"])
api_v1.include_router(logs.router, prefix="/logs", tags=["日志管理"])