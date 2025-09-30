from pydantic import BaseModel
from typing import Optional, List, Any
from datetime import datetime


class RoleBase(BaseModel):
    """角色基础模型"""
    name: str
    code: str
    status: Optional[int] = 1
    remark: Optional[str] = None


class RoleCreate(RoleBase):
    """创建角色"""
    pass


class RoleUpdate(BaseModel):
    """更新角色"""
    name: Optional[str] = None
    code: Optional[str] = None
    status: Optional[int] = None
    remark: Optional[str] = None


class RoleList(BaseModel):
    """角色列表项"""
    id: int
    name: str
    code: str
    status: int
    remark: Optional[str] = None
    createTime: Optional[int] = None
    updateTime: Optional[int] = None

    class Config:
        from_attributes = True


class RoleListRequest(BaseModel):
    """角色列表请求"""
    name: Optional[str] = None
    code: Optional[str] = None
    status: Optional[int] = None
    pageSize: Optional[int] = 10
    currentPage: Optional[int] = 1


class MenuBase(BaseModel):
    """菜单基础模型"""
    parent_id: Optional[int] = 0
    title: str
    name: Optional[str] = None
    path: Optional[str] = None
    component: Optional[str] = None
    menu_type: Optional[int] = 0
    rank: Optional[int] = None
    redirect: Optional[str] = None
    icon: Optional[str] = None
    extra_icon: Optional[str] = None
    enter_transition: Optional[str] = None
    leave_transition: Optional[str] = None
    active_path: Optional[str] = None
    auths: Optional[str] = None
    frame_src: Optional[str] = None
    frame_loading: Optional[bool] = True
    keep_alive: Optional[bool] = False
    hidden_tag: Optional[bool] = False
    fixed_tag: Optional[bool] = False
    show_link: Optional[bool] = True
    show_parent: Optional[bool] = False


class MenuCreate(MenuBase):
    """创建菜单"""
    pass


class MenuUpdate(BaseModel):
    """更新菜单"""
    parent_id: Optional[int] = None
    title: Optional[str] = None
    name: Optional[str] = None
    path: Optional[str] = None
    component: Optional[str] = None
    menu_type: Optional[int] = None
    rank: Optional[int] = None
    redirect: Optional[str] = None
    icon: Optional[str] = None
    extra_icon: Optional[str] = None
    enter_transition: Optional[str] = None
    leave_transition: Optional[str] = None
    active_path: Optional[str] = None
    auths: Optional[str] = None
    frame_src: Optional[str] = None
    frame_loading: Optional[bool] = None
    keep_alive: Optional[bool] = None
    hidden_tag: Optional[bool] = None
    fixed_tag: Optional[bool] = None
    show_link: Optional[bool] = None
    show_parent: Optional[bool] = None


class MenuList(BaseModel):
    """菜单列表项"""
    id: int
    parentId: int
    title: str
    name: Optional[str] = None
    path: Optional[str] = None
    component: Optional[str] = None
    menuType: int
    rank: Optional[int] = None
    redirect: Optional[str] = None
    icon: Optional[str] = None
    extraIcon: Optional[str] = None
    enterTransition: Optional[str] = None
    leaveTransition: Optional[str] = None
    activePath: Optional[str] = None
    auths: Optional[str] = None
    frameSrc: Optional[str] = None
    frameLoading: bool
    keepAlive: bool
    hiddenTag: bool
    fixedTag: bool
    showLink: bool
    showParent: bool

    class Config:
        from_attributes = True


class DepartmentBase(BaseModel):
    """部门基础模型"""
    parent_id: Optional[int] = 0
    name: str
    code: str
    leader: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    status: Optional[int] = 1
    sort: Optional[int] = 0


class DepartmentCreate(DepartmentBase):
    """创建部门"""
    pass


class DepartmentUpdate(BaseModel):
    """更新部门"""
    parent_id: Optional[int] = None
    name: Optional[str] = None
    code: Optional[str] = None
    leader: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    status: Optional[int] = None
    sort: Optional[int] = None


class DepartmentList(BaseModel):
    """部门列表项"""
    id: int
    parentId: int
    name: str
    code: str
    leader: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    status: int
    sort: int

    class Config:
        from_attributes = True