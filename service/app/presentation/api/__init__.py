"""API路由"""

from fastapi import APIRouter
from app.presentation.api import v1

# 创建主路由
router = APIRouter()

# 包含所有版本的路由
router.include_router(v1.router)