from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from app.application.services.system_service import SystemService
from app.application.services.user_service import UserService
from app.infrastructure.database.database import get_db
from app.presentation.api.dependencies import get_current_user, get_user_service, get_role_service
from app.presentation.schemas.system import *
from app.presentation.schemas.user import *

router = APIRouter()


@router.post("/user", response_model=TableResponse)
async def get_user_list(
        request: UserListRequest,
        current_user=Depends(get_current_user),
        user_service: UserService = Depends(get_user_service)
):
    """获取用户列表"""
    try:
        # 注意：这个实现需要根据新的UserService进行调整
        # 目前使用旧的同步实现作为示例
        users = await user_service.list_users(
            skip=(request.currentPage or 1 - 1) * (request.pageSize or 10),
            limit=request.pageSize or 10
        )
        total = await user_service.count_users()

        # 转换为前端需要的格式
        user_list = []
        for user in users:
            created_time = getattr(user, 'created_time', None)
            
            user_list.append({
                "id": getattr(user, 'id', ''),
                "username": getattr(user, 'username', ''),
                "nickname": getattr(user, 'nickname', ''),
                "phone": getattr(user, 'phone', ''),
                "email": getattr(user, 'email', ''),
                "avatar": getattr(user, 'avatar', ''),
                "sex": 0,  # 需要根据实际模型调整
                "status": 1 if getattr(user, 'is_active', True) else 0,
                "dept": None,  # 需要根据实际模型调整
                "remark": "",  # 需要根据实际模型调整
                "createTime": int(created_time.timestamp() * 1000) if created_time and isinstance(created_time, datetime) else None
            })

        return TableResponse(
            success=True,
            data=PageResponse(
                list=user_list,
                total=total,
                pageSize=request.pageSize or 10,
                currentPage=request.currentPage or 1
            )
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/list-all-role")
async def get_all_roles(
        current_user=Depends(get_current_user),
        role_service = Depends(get_role_service)
):
    """获取所有角色列表"""
    try:
        roles = await role_service.list_roles()
        
        role_list = []
        for role in roles:
            role_list.append({
                "id": getattr(role, 'id', ''),
                "name": getattr(role, 'name', '')
            })

        return {
            "success": True,
            "data": role_list
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/list-role-ids")
async def get_user_role_ids(
        request: dict,
        current_user=Depends(get_current_user),
        role_service = Depends(get_role_service)
):
    """根据用户ID获取角色ID列表"""
    try:
        user_id = request.get("userId")
        if not user_id:
            raise HTTPException(status_code=400, detail="userId is required")

        # 这里需要实现根据用户ID获取角色ID的逻辑
        # 示例实现
        role_ids = []  # 需要根据实际逻辑实现

        return {
            "success": True,
            "data": role_ids
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/role", response_model=TableResponse)
async def get_role_list(
        request: RoleListRequest,
        current_user=Depends(get_current_user),
        role_service = Depends(get_role_service)
):
    """获取角色列表"""
    try:
        roles = await role_service.list_roles(
            skip=(request.currentPage or 1 - 1) * (request.pageSize or 10),
            limit=request.pageSize or 10
        )
        total = await role_service.count_roles()

        role_list = []
        for role in roles:
            role_list.append({
                "id": getattr(role, 'id', ''),
                "name": getattr(role, 'name', ''),
                "code": "",  # 需要根据实际模型调整
                "status": 1 if getattr(role, 'is_active', True) else 0,
                "remark": "",  # 需要根据实际模型调整
                "createTime": None,  # 需要根据实际模型调整
                "updateTime": None  # 需要根据实际模型调整
            })

        return TableResponse(
            success=True,
            data=PageResponse(
                list=role_list,
                total=total,
                pageSize=request.pageSize or 10,
                currentPage=request.currentPage or 1
            )
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/menu")
async def get_menu_list(
        request: dict,
        current_user=Depends(get_current_user)
):
    """获取菜单列表"""
    try:
        # 这里需要实现获取菜单列表的逻辑
        # 示例实现
        menu_list = []  # 需要根据实际逻辑实现

        return {
            "success": True,
            "data": menu_list
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))