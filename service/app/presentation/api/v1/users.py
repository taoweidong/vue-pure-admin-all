from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.infrastructure.database.database import get_db
from app.presentation.api.v1.auth import get_current_user
from app.presentation.schemas.user import *
from app.presentation.schemas.common import *
from app.application.services.user_service import UserService

router = APIRouter()


@router.get("", response_model=PaginatedResponse[UserInList])
async def get_users(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页记录数"),
    username: Optional[str] = Query(None, description="用户名"),
    nickname: Optional[str] = Query(None, description="昵称"),
    email: Optional[str] = Query(None, description="邮箱"),
    phone: Optional[str] = Query(None, description="手机号"),
    status: Optional[int] = Query(None, description="状态"),
    dept_id: Optional[int] = Query(None, description="部门ID"),
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取用户列表"""
    try:
        user_service = UserService(db)
        users, total = user_service.get_users_paginated(
            page=page,
            page_size=page_size,
            username=username,
            nickname=nickname,
            email=email,
            phone=phone,
            status=status,
            dept_id=dept_id
        )
        
        user_list = []
        for user in users:
            dept_info = None
            if user.dept:
                dept_info = {
                    "id": user.dept.id,
                    "name": user.dept.name,
                    "code": user.dept.code
                }
            
            user_list.append(UserInList(
                id=user.id,
                username=user.username,
                nickname=user.nickname,
                email=user.email,
                phone=user.phone,
                avatar=user.avatar,
                sex=user.sex,
                status=user.status,
                dept=dept_info,
                remark=user.remark,
                created_at=user.created_at,
                updated_at=user.updated_at
            ))
        
        pages = (total + page_size - 1) // page_size
        
        return PaginatedResponse(
            success=True,
            data=PaginationData(
                items=user_list,
                total=total,
                page=page,
                page_size=page_size,
                pages=pages
            )
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{user_id}", response_model=BaseResponse[UserDetail])
async def get_user(
    user_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取用户详情"""
    try:
        user_service = UserService(db)
        user = user_service.get_user_by_id(user_id)
        
        if not user:
            raise HTTPException(status_code=404, detail="用户不存在")
        
        # 获取用户角色
        roles = user_service.get_user_roles(user_id)
        role_list = [{"id": role.id, "name": role.name, "code": role.code} for role in roles]
        
        dept_info = None
        if user.dept:
            dept_info = {
                "id": user.dept.id,
                "name": user.dept.name,
                "code": user.dept.code
            }
        
        user_detail = UserDetail(
            id=user.id,
            username=user.username,
            nickname=user.nickname,
            email=user.email,
            phone=user.phone,
            avatar=user.avatar,
            description=user.description,
            sex=user.sex,
            status=user.status,
            dept=dept_info,
            roles=role_list,
            remark=user.remark,
            created_at=user.created_at,
            updated_at=user.updated_at
        )
        
        return BaseResponse(
            success=True,
            data=user_detail
        )
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=str(e))


@router.post("", response_model=BaseResponse[UserDetail], status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """创建用户"""
    try:
        user_service = UserService(db)
        
        # 检查用户名是否已存在
        if user_service.get_user_by_username(user_data.username):
            raise HTTPException(status_code=409, detail="用户名已存在")
        
        # 检查邮箱是否已存在
        if user_data.email and user_service.get_user_by_email(user_data.email):
            raise HTTPException(status_code=409, detail="邮箱已存在")
        
        # 检查手机号是否已存在
        if user_data.phone and user_service.get_user_by_phone(user_data.phone):
            raise HTTPException(status_code=409, detail="手机号已存在")
        
        user = user_service.create_user(user_data)
        
        dept_info = None
        if user.dept:
            dept_info = {
                "id": user.dept.id,
                "name": user.dept.name,
                "code": user.dept.code
            }
        
        user_detail = UserDetail(
            id=user.id,
            username=user.username,
            nickname=user.nickname,
            email=user.email,
            phone=user.phone,
            avatar=user.avatar,
            description=user.description,
            sex=user.sex,
            status=user.status,
            dept=dept_info,
            roles=[],
            remark=user.remark,
            created_at=user.created_at,
            updated_at=user.updated_at
        )
        
        return BaseResponse(
            success=True,
            message="用户创建成功",
            data=user_detail
        )
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{user_id}", response_model=BaseResponse[UserDetail])
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """更新用户"""
    try:
        user_service = UserService(db)
        
        user = user_service.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="用户不存在")
        
        # 检查邮箱是否已被其他用户使用
        if user_data.email and user_data.email != user.email:
            existing_user = user_service.get_user_by_email(user_data.email)
            if existing_user and existing_user.id != user_id:
                raise HTTPException(status_code=409, detail="邮箱已被其他用户使用")
        
        # 检查手机号是否已被其他用户使用
        if user_data.phone and user_data.phone != user.phone:
            existing_user = user_service.get_user_by_phone(user_data.phone)
            if existing_user and existing_user.id != user_id:
                raise HTTPException(status_code=409, detail="手机号已被其他用户使用")
        
        updated_user = user_service.update_user(user_id, user_data)
        
        # 获取用户角色
        roles = user_service.get_user_roles(user_id)
        role_list = [{"id": role.id, "name": role.name, "code": role.code} for role in roles]
        
        dept_info = None
        if updated_user.dept:
            dept_info = {
                "id": updated_user.dept.id,
                "name": updated_user.dept.name,
                "code": updated_user.dept.code
            }
        
        user_detail = UserDetail(
            id=updated_user.id,
            username=updated_user.username,
            nickname=updated_user.nickname,
            email=updated_user.email,
            phone=updated_user.phone,
            avatar=updated_user.avatar,
            description=updated_user.description,
            sex=updated_user.sex,
            status=updated_user.status,
            dept=dept_info,
            roles=role_list,
            remark=updated_user.remark,
            created_at=updated_user.created_at,
            updated_at=updated_user.updated_at
        )
        
        return BaseResponse(
            success=True,
            message="用户更新成功",
            data=user_detail
        )
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """删除用户"""
    try:
        user_service = UserService(db)
        
        user = user_service.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="用户不存在")
        
        # 不能删除当前登录用户
        if user_id == current_user.id:
            raise HTTPException(status_code=400, detail="不能删除当前登录用户")
        
        user_service.delete_user(user_id)
        
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{user_id}/status")
async def update_user_status(
    user_id: int,
    request: UserStatusUpdate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """更新用户状态"""
    try:
        user_service = UserService(db)
        
        user = user_service.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="用户不存在")
        
        # 不能禁用当前登录用户
        if user_id == current_user.id and request.status == 0:
            raise HTTPException(status_code=400, detail="不能禁用当前登录用户")
        
        user_service.update_user_status(user_id, request.status)
        
        return {
            "success": True,
            "message": "用户状态更新成功"
        }
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{user_id}/password")
async def reset_user_password(
    user_id: int,
    request: PasswordResetRequest,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """重置用户密码"""
    try:
        user_service = UserService(db)
        
        user = user_service.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="用户不存在")
        
        user_service.reset_password(user_id, request.password)
        
        return {
            "success": True,
            "message": "密码重置成功"
        }
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{user_id}/roles")
async def get_user_roles(
    user_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取用户角色列表"""
    try:
        user_service = UserService(db)
        
        user = user_service.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="用户不存在")
        
        roles = user_service.get_user_roles(user_id)
        role_list = [{"id": role.id, "name": role.name, "code": role.code} for role in roles]
        
        return {
            "success": True,
            "data": role_list
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))