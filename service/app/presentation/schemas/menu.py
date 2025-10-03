from pydantic import BaseModel
from typing import Optional
from datetime import datetime


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


class MenuInList(BaseModel):
    """菜单列表项"""
    id: int
    parent_id: int
    title: str
    name: Optional[str] = None
    path: Optional[str] = None
    component: Optional[str] = None
    menu_type: int
    rank: Optional[int] = None
    redirect: Optional[str] = None
    icon: Optional[str] = None
    extra_icon: Optional[str] = None
    enter_transition: Optional[str] = None
    leave_transition: Optional[str] = None
    active_path: Optional[str] = None
    auths: Optional[str] = None
    frame_src: Optional[str] = None
    frame_loading: bool
    keep_alive: bool
    hidden_tag: bool
    fixed_tag: bool
    show_link: bool
    show_parent: bool
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class MenuDetail(MenuInList):
    """菜单详情"""
    pass