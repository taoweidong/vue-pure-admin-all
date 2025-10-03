from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.infrastructure.database.database import get_db
from app.presentation.api.v1.auth import get_current_user
from app.presentation.schemas.role import *
from app.presentation.schemas.common import *
from app.application.services.role_service import RoleService

router = APIRouter()


@router.get("", response_model=PaginatedResponse[RoleInList])
async def get_roles(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页记录数"),
    name: Optional[str] = Query(None, description="角色名称"),
    code: Optional[str] = Query(None, description="角色编码"),
    status: Optional[int] = Query(None, description="状态"),
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取角色列表"""
    try:
        role_service = RoleService(db)
        roles, total = role_service.get_roles_paginated(
            page=page,
            page_size=page_size,
            name=name,
            code=code,
            status=status
        )
        
        role_list = []
        for role in roles:
            role_list.append(RoleInList(
                id=role.id,
                name=role.name,
                code=role.code,
                status=role.status,
                remark=role.remark,
                created_at=role.created_at,
                updated_at=role.updated_at
            ))
        
        pages = (total + page_size - 1) // page_size
        
        return PaginatedResponse(
            success=True,
            data=PaginationData(
                items=role_list,
                total=total,
                page=page,
                page_size=page_size,
                pages=pages
            )
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{role_id}", response_model=BaseResponse[RoleDetail])
async def get_role(
    role_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取角色详情"""
    try:
        role_service = RoleService(db)
        role = role_service.get_role_by_id(role_id)
        
        if not role:
            raise HTTPException(status_code=404, detail="角色不存在")
        
        # 获取角色菜单权限
        menus = role_service.get_role_menus(role_id)
        menu_list = [{"id": menu.id, "title": menu.title, "name": menu.name} for menu in menus]
        
        role_detail = RoleDetail(
            id=role.id,
            name=role.name,
            code=role.code,
            status=role.status,
            remark=role.remark,
            menus=menu_list,
            created_at=role.created_at,
            updated_at=role.updated_at
        )
        
        return BaseResponse(
            success=True,
            data=role_detail
        )
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=str(e))


@router.post("", response_model=BaseResponse[RoleDetail], status_code=status.HTTP_201_CREATED)
async def create_role(
    role_data: RoleCreate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """创建角色"""
    try:
        role_service = RoleService(db)
        
        # 检查角色名称是否已存在
        if role_service.get_role_by_name(role_data.name):
            raise HTTPException(status_code=409, detail="角色名称已存在")
        
        # 检查角色编码是否已存在
        if role_service.get_role_by_code(role_data.code):
            raise HTTPException(status_code=409, detail="角色编码已存在")
        
        role = role_service.create_role(role_data)
        
        role_detail = RoleDetail(
            id=role.id,
            name=role.name,
            code=role.code,
            status=role.status,
            remark=role.remark,
            menus=[],
            created_at=role.created_at,
            updated_at=role.updated_at
        )
        
        return BaseResponse(
            success=True,
            message="角色创建成功",
            data=role_detail
        )
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{role_id}", response_model=BaseResponse[RoleDetail])
async def update_role(
    role_id: int,
    role_data: RoleUpdate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """更新角色"""
    try:
        role_service = RoleService(db)
        
        role = role_service.get_role_by_id(role_id)
        if not role:
            raise HTTPException(status_code=404, detail="角色不存在")
        
        # 检查角色名称是否已被其他角色使用
        if role_data.name and role_data.name != role.name:
            existing_role = role_service.get_role_by_name(role_data.name)
            if existing_role and existing_role.id != role_id:
                raise HTTPException(status_code=409, detail="角色名称已被其他角色使用")
        
        # 检查角色编码是否已被其他角色使用
        if role_data.code and role_data.code != role.code:
            existing_role = role_service.get_role_by_code(role_data.code)
            if existing_role and existing_role.id != role_id:
                raise HTTPException(status_code=409, detail="角色编码已被其他角色使用")
        
        updated_role = role_service.update_role(role_id, role_data)
        
        # 获取角色菜单权限
        menus = role_service.get_role_menus(role_id)
        menu_list = [{"id": menu.id, "title": menu.title, "name": menu.name} for menu in menus]
        
        role_detail = RoleDetail(
            id=updated_role.id,
            name=updated_role.name,
            code=updated_role.code,
            status=updated_role.status,
            remark=updated_role.remark,
            menus=menu_list,
            created_at=updated_role.created_at,
            updated_at=updated_role.updated_at
        )
        
        return BaseResponse(
            success=True,
            message="角色更新成功",
            data=role_detail
        )
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_role(
    role_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """删除角色"""
    try:
        role_service = RoleService(db)
        
        role = role_service.get_role_by_id(role_id)
        if not role:
            raise HTTPException(status_code=404, detail="角色不存在")
        
        # 检查角色是否被用户使用
        if role_service.check_role_in_use(role_id):
            raise HTTPException(status_code=400, detail="角色正在被用户使用，无法删除")
        
        role_service.delete_role(role_id)
        
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{role_id}/status")
async def update_role_status(
    role_id: int,
    request: RoleStatusUpdate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """更新角色状态"""
    try:
        role_service = RoleService(db)
        
        role = role_service.get_role_by_id(role_id)
        if not role:
            raise HTTPException(status_code=404, detail="角色不存在")
        
        role_service.update_role_status(role_id, request.status)
        
        return {
            "success": True,
            "message": "角色状态更新成功"
        }
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{role_id}/menus")
async def get_role_menus(
    role_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取角色菜单权限"""
    try:
        role_service = RoleService(db)
        
        role = role_service.get_role_by_id(role_id)
        if not role:
            raise HTTPException(status_code=404, detail="角色不存在")
        
        menus = role_service.get_role_menus(role_id)
        menu_list = [{"id": menu.id, "title": menu.title, "name": menu.name} for menu in menus]
        
        return {
            "success": True,
            "data": menu_list
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{role_id}/menus")
async def update_role_menus(
    role_id: int,
    request: RoleMenusUpdate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """更新角色菜单权限"""
    try:
        role_service = RoleService(db)
        
        role = role_service.get_role_by_id(role_id)
        if not role:
            raise HTTPException(status_code=404, detail="角色不存在")
        
        role_service.update_role_menus(role_id, request.menu_ids)
        
        return {
            "success": True,
            "message": "角色菜单权限更新成功"
        }
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=str(e))