"""API v1版本"""

from fastapi import APIRouter
from app.presentation.api.v1 import auth, users, roles, menus, depts, operation_logs, login_logs, system_configs, test_users

# 创建v1版本的路由
router = APIRouter(prefix="/api/v1")

# 包含所有子路由
router.include_router(auth.router, prefix="/auth")
router.include_router(users.router, prefix="/users")
router.include_router(roles.router, prefix="/roles")
router.include_router(menus.router, prefix="/menus")
router.include_router(depts.router, prefix="/depts")
router.include_router(operation_logs.router, prefix="/operation-logs")
router.include_router(login_logs.router, prefix="/login-logs")
router.include_router(system_configs.router, prefix="/system-configs")
router.include_router(test_users.router, prefix="/test-users")