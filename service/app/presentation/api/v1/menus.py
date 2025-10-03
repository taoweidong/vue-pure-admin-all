from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.infrastructure.database.database import get_db
from app.presentation.api.v1.auth import get_current_user
from app.presentation.schemas.menu import *
from app.presentation.schemas.common import *
from app.application.services.menu_service import MenuService

router = APIRouter()


@router.get("", response_model=PaginatedResponse[MenuInList])
async def get_menus(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页记录数"),
    title: Optional[str] = Query(None, description="菜单标题"),
    name: Optional[str] = Query(None, description="菜单名称"),
    menu_type: Optional[int] = Query(None, description="菜单类型"),
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取菜单列表"""
    try:
        menu_service = MenuService(db)
        menus, total = menu_service.get_menus_paginated(
            page=page,
            page_size=page_size,
            title=title,
            name=name,
            menu_type=menu_type
        )
        
        menu_list = []
        for menu in menus:
            menu_list.append(MenuInList(
                id=menu.id,
                parent_id=menu.parent_id,
                title=menu.title,
                name=menu.name,
                path=menu.path,
                component=menu.component,
                menu_type=menu.menu_type,
                rank=menu.rank,
                redirect=menu.redirect,
                icon=menu.icon,
                extra_icon=menu.extra_icon,
                enter_transition=menu.enter_transition,
                leave_transition=menu.leave_transition,
                active_path=menu.active_path,
                auths=menu.auths,
                frame_src=menu.frame_src,
                frame_loading=menu.frame_loading,
                keep_alive=menu.keep_alive,
                hidden_tag=menu.hidden_tag,
                fixed_tag=menu.fixed_tag,
                show_link=menu.show_link,
                show_parent=menu.show_parent,
                created_at=menu.created_at,
                updated_at=menu.updated_at
            ))
        
        pages = (total + page_size - 1) // page_size
        
        return PaginatedResponse(
            success=True,
            data=PaginationData(
                items=menu_list,
                total=total,
                page=page,
                page_size=page_size,
                pages=pages
            )
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/tree")
async def get_menu_tree(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取菜单树"""
    try:
        menu_service = MenuService(db)
        menu_tree = menu_service.get_menu_tree()
        
        return {
            "success": True,
            "data": menu_tree
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{menu_id}", response_model=BaseResponse[MenuDetail])
async def get_menu(
    menu_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取菜单详情"""
    try:
        menu_service = MenuService(db)
        menu = menu_service.get_menu_by_id(menu_id)
        
        if not menu:
            raise HTTPException(status_code=404, detail="菜单不存在")
        
        menu_detail = MenuDetail(
            id=menu.id,
            parent_id=menu.parent_id,
            title=menu.title,
            name=menu.name,
            path=menu.path,
            component=menu.component,
            menu_type=menu.menu_type,
            rank=menu.rank,
            redirect=menu.redirect,
            icon=menu.icon,
            extra_icon=menu.extra_icon,
            enter_transition=menu.enter_transition,
            leave_transition=menu.leave_transition,
            active_path=menu.active_path,
            auths=menu.auths,
            frame_src=menu.frame_src,
            frame_loading=menu.frame_loading,
            keep_alive=menu.keep_alive,
            hidden_tag=menu.hidden_tag,
            fixed_tag=menu.fixed_tag,
            show_link=menu.show_link,
            show_parent=menu.show_parent,
            created_at=menu.created_at,
            updated_at=menu.updated_at
        )
        
        return BaseResponse(
            success=True,
            data=menu_detail
        )
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=str(e))


@router.post("", response_model=BaseResponse[MenuDetail], status_code=status.HTTP_201_CREATED)
async def create_menu(
    menu_data: MenuCreate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """创建菜单"""
    try:
        menu_service = MenuService(db)
        
        # 检查菜单名称是否已存在
        if menu_data.name and menu_service.get_menu_by_name(menu_data.name):
            raise HTTPException(status_code=409, detail="菜单名称已存在")
        
        menu = menu_service.create_menu(menu_data)
        
        menu_detail = MenuDetail(
            id=menu.id,
            parent_id=menu.parent_id,
            title=menu.title,
            name=menu.name,
            path=menu.path,
            component=menu.component,
            menu_type=menu.menu_type,
            rank=menu.rank,
            redirect=menu.redirect,
            icon=menu.icon,
            extra_icon=menu.extra_icon,
            enter_transition=menu.enter_transition,
            leave_transition=menu.leave_transition,
            active_path=menu.active_path,
            auths=menu.auths,
            frame_src=menu.frame_src,
            frame_loading=menu.frame_loading,
            keep_alive=menu.keep_alive,
            hidden_tag=menu.hidden_tag,
            fixed_tag=menu.fixed_tag,
            show_link=menu.show_link,
            show_parent=menu.show_parent,
            created_at=menu.created_at,
            updated_at=menu.updated_at
        )
        
        return BaseResponse(
            success=True,
            message="菜单创建成功",
            data=menu_detail
        )
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{menu_id}", response_model=BaseResponse[MenuDetail])
async def update_menu(
    menu_id: int,
    menu_data: MenuUpdate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """更新菜单"""
    try:
        menu_service = MenuService(db)
        
        menu = menu_service.get_menu_by_id(menu_id)
        if not menu:
            raise HTTPException(status_code=404, detail="菜单不存在")
        
        # 检查菜单名称是否已被其他菜单使用
        if menu_data.name and menu_data.name != menu.name:
            existing_menu = menu_service.get_menu_by_name(menu_data.name)
            if existing_menu and existing_menu.id != menu_id:
                raise HTTPException(status_code=409, detail="菜单名称已被其他菜单使用")
        
        updated_menu = menu_service.update_menu(menu_id, menu_data)
        
        menu_detail = MenuDetail(
            id=updated_menu.id,
            parent_id=updated_menu.parent_id,
            title=updated_menu.title,
            name=updated_menu.name,
            path=updated_menu.path,
            component=updated_menu.component,
            menu_type=updated_menu.menu_type,
            rank=updated_menu.rank,
            redirect=updated_menu.redirect,
            icon=updated_menu.icon,
            extra_icon=updated_menu.extra_icon,
            enter_transition=updated_menu.enter_transition,
            leave_transition=updated_menu.leave_transition,
            active_path=updated_menu.active_path,
            auths=updated_menu.auths,
            frame_src=updated_menu.frame_src,
            frame_loading=updated_menu.frame_loading,
            keep_alive=updated_menu.keep_alive,
            hidden_tag=updated_menu.hidden_tag,
            fixed_tag=updated_menu.fixed_tag,
            show_link=updated_menu.show_link,
            show_parent=updated_menu.show_parent,
            created_at=updated_menu.created_at,
            updated_at=updated_menu.updated_at
        )
        
        return BaseResponse(
            success=True,
            message="菜单更新成功",
            data=menu_detail
        )
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{menu_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_menu(
    menu_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """删除菜单"""
    try:
        menu_service = MenuService(db)
        
        menu = menu_service.get_menu_by_id(menu_id)
        if not menu:
            raise HTTPException(status_code=404, detail="菜单不存在")
        
        # 检查是否有子菜单
        if menu_service.has_children(menu_id):
            raise HTTPException(status_code=400, detail="存在子菜单，无法删除")
        
        # 检查菜单是否被角色使用
        if menu_service.check_menu_in_use(menu_id):
            raise HTTPException(status_code=400, detail="菜单正在被角色使用，无法删除")
        
        menu_service.delete_menu(menu_id)
        
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=str(e))