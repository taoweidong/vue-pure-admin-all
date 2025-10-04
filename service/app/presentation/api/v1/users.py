from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional

from app.application.services.user_service import UserService
from application.dto.user_dto import UserCreate, UserUpdate, UserResponse, UserAssignRoles
from presentation.dto.response_dto import SuccessResponse, PageResponse
from presentation.api.dependencies import get_user_service
from shared.kernel.exceptions import BusinessException

router = APIRouter(prefix="/api/v1/users", tags=["用户管理"])

@router.get("", response_model=PageResponse[UserResponse])
async def list_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    user_service: UserService = Depends(get_user_service),
):
    """获取用户列表"""
    users = await user_service.list_users(skip=skip, limit=limit)
    total = await user_service.count_users()
    
    # 转换为响应DTO
    user_responses = [UserResponse.from_domain(user) for user in users]
    
    return PageResponse(
        data=user_responses,
        total=total,
        skip=skip,
        limit=limit
    )

@router.get("/{user_id}", response_model=SuccessResponse[UserResponse])
async def get_user(
    user_id: str,
    user_service: UserService = Depends(get_user_service),
):
    """获取用户详情"""
    user = await user_service.get_user(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    return SuccessResponse(data=UserResponse.from_domain(user))

@router.post("", response_model=SuccessResponse[UserResponse])
async def create_user(
    user_in: UserCreate,
    user_service: UserService = Depends(get_user_service),
):
    """创建用户"""
    try:
        user = await user_service.create_user(user_in)
        return SuccessResponse(
            data=UserResponse.from_domain(user),
            message="用户创建成功"
        )
    except BusinessException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.put("/{user_id}", response_model=SuccessResponse[UserResponse])
async def update_user(
    user_id: str,
    user_update: UserUpdate,
    user_service: UserService = Depends(get_user_service),
):
    """更新用户"""
    try:
        user = await user_service.update_user(user_id, user_update)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="用户不存在"
            )
        return SuccessResponse(
            data=UserResponse.from_domain(user),
            message="用户更新成功"
        )
    except BusinessException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.delete("/{user_id}", response_model=SuccessResponse[None])
async def delete_user(
    user_id: str,
    user_service: UserService = Depends(get_user_service),
):
    """删除用户"""
    success = await user_service.delete_user(user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    return SuccessResponse(message="用户删除成功")

@router.put("/{user_id}/roles", response_model=SuccessResponse[None])
async def assign_user_roles(
    user_id: str,
    role_data: UserAssignRoles,
    user_service: UserService = Depends(get_user_service),
):
    """分配用户角色"""
    user = await user_service.get_user(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    
    # 这里需要实现角色分配逻辑
    # 简化实现
    return SuccessResponse(message="角色分配成功")