from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.infrastructure.database.database import get_db
from app.presentation.api.dependencies import get_current_user
from app.presentation.schemas.menu import *
from app.presentation.schemas.common import *
from app.application.services.menu_service import MenuService

router = APIRouter(prefix="/api/v1/menus", tags=["菜单管理"])


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
                id=getattr(menu, 'id', 0),
                parent_id=getattr(menu, 'parent_id', 0) or 0,
                title=getattr(menu, 'title', ''),
                name=getattr(menu, 'name', None),
                path=getattr(menu, 'path', None),
                component=getattr(menu, 'component', None),
                menu_type=getattr(menu, 'menu_type', 1),
                rank=getattr(menu, 'rank', 0) or 0,
                redirect=getattr(menu, 'redirect', None),
                icon=getattr(menu, 'icon', None),
                extra_icon=getattr(menu, 'extra_icon', None),
                enter_transition=getattr(menu, 'enter_transition', None),
                leave_transition=getattr(menu, 'leave_transition', None),
                active_path=getattr(menu, 'active_path', None),
                auths=getattr(menu, 'auths', None),
                frame_src=getattr(menu, 'frame_src', None),
                frame_loading=bool(getattr(menu, 'frame_loading', False)),
                keep_alive=bool(getattr(menu, 'keep_alive', False)),
                hidden_tag=bool(getattr(menu, 'hidden_tag', False)),
                fixed_tag=bool(getattr(menu, 'fixed_tag', False)),
                show_link=bool(getattr(menu, 'show_link', True)),
                show_parent=bool(getattr(menu, 'show_parent', True)),
                created_at=getattr(menu, 'created_at', None),
                updated_at=getattr(menu, 'updated_at', None)
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
            id=getattr(menu, 'id', 0),
            parent_id=getattr(menu, 'parent_id', 0) or 0,
            title=getattr(menu, 'title', ''),
            name=getattr(menu, 'name', None),
            path=getattr(menu, 'path', None),
            component=getattr(menu, 'component', None),
            menu_type=getattr(menu, 'menu_type', 1),
            rank=getattr(menu, 'rank', 0) or 0,
            redirect=getattr(menu, 'redirect', None),
            icon=getattr(menu, 'icon', None),
            extra_icon=getattr(menu, 'extra_icon', None),
            enter_transition=getattr(menu, 'enter_transition', None),
            leave_transition=getattr(menu, 'leave_transition', None),
            active_path=getattr(menu, 'active_path', None),
            auths=getattr(menu, 'auths', None),
            frame_src=getattr(menu, 'frame_src', None),
            frame_loading=bool(getattr(menu, 'frame_loading', False)),
            keep_alive=bool(getattr(menu, 'keep_alive', False)),
            hidden_tag=bool(getattr(menu, 'hidden_tag', False)),
            fixed_tag=bool(getattr(menu, 'fixed_tag', False)),
            show_link=bool(getattr(menu, 'show_link', True)),
            show_parent=bool(getattr(menu, 'show_parent', True)),
            created_at=getattr(menu, 'created_at', None),
            updated_at=getattr(menu, 'updated_at', None)
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
            id=getattr(menu, 'id', 0),
            parent_id=getattr(menu, 'parent_id', 0) or 0,
            title=getattr(menu, 'title', ''),
            name=getattr(menu, 'name', None),
            path=getattr(menu, 'path', None),
            component=getattr(menu, 'component', None),
            menu_type=getattr(menu, 'menu_type', 1),
            rank=getattr(menu, 'rank', 0) or 0,
            redirect=getattr(menu, 'redirect', None),
            icon=getattr(menu, 'icon', None),
            extra_icon=getattr(menu, 'extra_icon', None),
            enter_transition=getattr(menu, 'enter_transition', None),
            leave_transition=getattr(menu, 'leave_transition', None),
            active_path=getattr(menu, 'active_path', None),
            auths=getattr(menu, 'auths', None),
            frame_src=getattr(menu, 'frame_src', None),
            frame_loading=bool(getattr(menu, 'frame_loading', False)),
            keep_alive=bool(getattr(menu, 'keep_alive', False)),
            hidden_tag=bool(getattr(menu, 'hidden_tag', False)),
            fixed_tag=bool(getattr(menu, 'fixed_tag', False)),
            show_link=bool(getattr(menu, 'show_link', True)),
            show_parent=bool(getattr(menu, 'show_parent', True)),
            created_at=getattr(menu, 'created_at', None),
            updated_at=getattr(menu, 'updated_at', None)
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
            if existing_menu is not None and str(existing_menu.id) != str(menu_id):
                raise HTTPException(status_code=409, detail="菜单名称已被其他菜单使用")
        
        updated_menu = menu_service.update_menu(menu_id, menu_data)
        
        menu_detail = MenuDetail(
            id=getattr(updated_menu, 'id', 0),
            parent_id=getattr(updated_menu, 'parent_id', 0) or 0,
            title=getattr(updated_menu, 'title', ''),
            name=getattr(updated_menu, 'name', None),
            path=getattr(updated_menu, 'path', None),
            component=getattr(updated_menu, 'component', None),
            menu_type=getattr(updated_menu, 'menu_type', 1),
            rank=getattr(updated_menu, 'rank', 0) or 0,
            redirect=getattr(updated_menu, 'redirect', None),
            icon=getattr(updated_menu, 'icon', None),
            extra_icon=getattr(updated_menu, 'extra_icon', None),
            enter_transition=getattr(updated_menu, 'enter_transition', None),
            leave_transition=getattr(updated_menu, 'leave_transition', None),
            active_path=getattr(updated_menu, 'active_path', None),
            auths=getattr(updated_menu, 'auths', None),
            frame_src=getattr(updated_menu, 'frame_src', None),
            frame_loading=bool(getattr(updated_menu, 'frame_loading', False)),
            keep_alive=bool(getattr(updated_menu, 'keep_alive', False)),
            hidden_tag=bool(getattr(updated_menu, 'hidden_tag', False)),
            fixed_tag=bool(getattr(updated_menu, 'fixed_tag', False)),
            show_link=bool(getattr(updated_menu, 'show_link', True)),
            show_parent=bool(getattr(updated_menu, 'show_parent', True)),
            created_at=getattr(updated_menu, 'created_at', None),
            updated_at=getattr(updated_menu, 'updated_at', None)
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