from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List

from app.application.services.role_service import RoleService
from application.dto.role_dto import RoleCreate, RoleUpdate, RoleResponse, RoleAssignMenus
from presentation.dto.response_dto import SuccessResponse, PageResponse
from presentation.api.dependencies import get_role_service
from shared.kernel.exceptions import BusinessException

router = APIRouter(prefix="/api/v1/roles", tags=["角色管理"])

@router.get("", response_model=PageResponse[RoleResponse])
async def list_roles(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    role_service: RoleService = Depends(get_role_service),
):
    """获取角色列表"""
    roles = await role_service.list_roles(skip=skip, limit=limit)
    total = await role_service.count_roles()
    
    # 转换为响应DTO
    role_responses = [RoleResponse.from_domain(role) for role in roles]
    
    return PageResponse(
        data=role_responses,
        total=total,
        skip=skip,
        limit=limit
    )

@router.get("/{role_id}", response_model=SuccessResponse[RoleResponse])
async def get_role(
    role_id: str,
    role_service: RoleService = Depends(get_role_service),
):
    """获取角色详情"""
    role = await role_service.get_role(role_id)
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="角色不存在"
        )
    return SuccessResponse(data=RoleResponse.from_domain(role))

@router.post("", response_model=SuccessResponse[RoleResponse])
async def create_role(
    role_in: RoleCreate,
    role_service: RoleService = Depends(get_role_service),
):
    """创建角色"""
    try:
        role = await role_service.create_role(role_in)
        return SuccessResponse(
            data=RoleResponse.from_domain(role),
            message="角色创建成功"
        )
    except BusinessException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.put("/{role_id}", response_model=SuccessResponse[RoleResponse])
async def update_role(
    role_id: str,
    role_update: RoleUpdate,
    role_service: RoleService = Depends(get_role_service),
):
    """更新角色"""
    try:
        role = await role_service.update_role(role_id, role_update)
        if not role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="角色不存在"
            )
        return SuccessResponse(
            data=RoleResponse.from_domain(role),
            message="角色更新成功"
        )
    except BusinessException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.delete("/{role_id}", response_model=SuccessResponse[None])
async def delete_role(
    role_id: str,
    role_service: RoleService = Depends(get_role_service),
):
    """删除角色"""
    success = await role_service.delete_role(role_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="角色不存在"
        )
    return SuccessResponse(message="角色删除成功")

@router.put("/{role_id}/menus", response_model=SuccessResponse[None])
async def assign_role_menus(
    role_id: str,
    menu_data: RoleAssignMenus,
    role_service: RoleService = Depends(get_role_service),
):
    """分配角色菜单"""
    role = await role_service.assign_menus_to_role(role_id, menu_data.menu_ids)
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="角色不存在"
        )
    return SuccessResponse(message="菜单分配成功")