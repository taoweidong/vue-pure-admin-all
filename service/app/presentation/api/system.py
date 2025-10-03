from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.application.services.system_service import SystemService
from app.application.services.user_service import UserService
from app.infrastructure.database.database import get_db
from app.presentation.api.auth import get_current_user
from app.presentation.schemas.system import *
from app.presentation.schemas.user import *

router = APIRouter()


@router.post("/user", response_model=TableResponse)
async def get_user_list(
        request: UserListRequest,
        current_user=Depends(get_current_user),
        db: Session = Depends(get_db)
):
    """获取用户列表"""
    try:
        user_service = UserService(db)
        users, total = user_service.get_user_list(
            username=request.username,
            status=request.status,
            phone=request.phone,
            dept_id=request.deptId,
            page=request.currentPage or 1,
            page_size=request.pageSize or 10
        )

        # 转换为前端需要的格式
        user_list = []
        for user in users:
            dept_info = None
            if user.dept:
                dept_info = {
                    "id": user.dept.id,
                    "name": user.dept.name
                }

            user_list.append({
                "id": user.id,
                "username": user.username,
                "nickname": user.nickname,
                "phone": user.phone,
                "email": user.email,
                "avatar": user.avatar,
                "sex": user.sex,
                "status": user.status,
                "dept": dept_info,
                "remark": user.remark,
                "createTime": int(user.created_at.timestamp() * 1000) if user.created_at else None
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
        db: Session = Depends(get_db)
):
    """获取所有角色列表"""
    try:
        system_service = SystemService(db)
        roles = system_service.get_all_roles()

        role_list = []
        for role in roles:
            role_list.append({
                "id": role.id,
                "name": role.name
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
        db: Session = Depends(get_db)
):
    """根据用户ID获取角色ID列表"""
    try:
        user_id = request.get("userId")
        if not user_id:
            raise HTTPException(status_code=400, detail="userId is required")

        system_service = SystemService(db)
        role_ids = system_service.get_user_role_ids(user_id)

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
        db: Session = Depends(get_db)
):
    """获取角色列表"""
    try:
        system_service = SystemService(db)
        roles, total = system_service.get_role_list(
            name=request.name,
            code=request.code,
            status=request.status,
            page=request.currentPage or 1,
            page_size=request.pageSize or 10
        )

        role_list = []
        for role in roles:
            role_list.append({
                "id": role.id,
                "name": role.name,
                "code": role.code,
                "status": role.status,
                "remark": role.remark,
                "createTime": int(role.created_at.timestamp() * 1000) if role.created_at else None,
                "updateTime": int(role.updated_at.timestamp() * 1000) if role.updated_at else None
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
        current_user=Depends(get_current_user),
        db: Session = Depends(get_db)
):
    """获取菜单列表"""
    try:
        system_service = SystemService(db)
        menus = system_service.get_menu_list()

        menu_list = []
        for menu in menus:
            menu_list.append({
                "id": menu.id,
                "parentId": menu.parent_id,
                "title": menu.title,
                "name": menu.name,
                "path": menu.path,
                "component": menu.component,
                "menuType": menu.menu_type,
                "rank": menu.rank,
                "redirect": menu.redirect,
                "icon": menu.icon,
                "extraIcon": menu.extra_icon,
                "enterTransition": menu.enter_transition,
                "leaveTransition": menu.leave_transition,
                "activePath": menu.active_path,
                "auths": menu.auths,
                "frameSrc": menu.frame_src,
                "frameLoading": menu.frame_loading,
                "keepAlive": menu.keep_alive,
                "hiddenTag": menu.hidden_tag,
                "fixedTag": menu.fixed_tag,
                "showLink": menu.show_link,
                "showParent": menu.show_parent
            })

        return {
            "success": True,
            "data": menu_list
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/dept")
async def get_dept_list(
        request: dict,
        current_user=Depends(get_current_user),
        db: Session = Depends(get_db)
):
    """获取部门列表"""
    try:
        system_service = SystemService(db)
        depts = system_service.get_dept_list()

        dept_list = []
        for dept in depts:
            dept_list.append({
                "id": dept.id,
                "parentId": dept.parent_id,
                "name": dept.name,
                "code": dept.code,
                "leader": dept.leader,
                "phone": dept.phone,
                "email": dept.email,
                "status": dept.status,
                "sort": dept.sort
            })

        return {
            "success": True,
            "data": dept_list
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/role-menu")
async def get_role_menu(
        request: dict,
        current_user=Depends(get_current_user),
        db: Session = Depends(get_db)
):
    """获取角色菜单权限"""
    try:
        system_service = SystemService(db)
        menus = system_service.get_menu_list()

        menu_list = []
        for menu in menus:
            menu_list.append({
                "id": menu.id,
                "parentId": menu.parent_id,
                "menuType": menu.menu_type,
                "title": menu.title
            })

        return {
            "success": True,
            "data": menu_list
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/role-menu-ids")
async def get_role_menu_ids(
        request: dict,
        current_user=Depends(get_current_user),
        db: Session = Depends(get_db)
):
    """根据角色ID获取菜单ID列表"""
    try:
        role_id = request.get("id")
        if not role_id:
            raise HTTPException(status_code=400, detail="id is required")

        system_service = SystemService(db)
        menu_ids = system_service.get_role_menu_ids(role_id)

        return {
            "success": True,
            "data": menu_ids
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
