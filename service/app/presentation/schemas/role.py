from pydantic import BaseModel
from typing import Optional, List
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


class RoleInList(BaseModel):
    """角色列表项"""
    id: int
    name: str
    code: str
    status: int
    remark: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class RoleDetail(BaseModel):
    """角色详情"""
    id: int
    name: str
    code: str
    status: int
    remark: Optional[str] = None
    menus: List[dict] = []
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class RoleStatusUpdate(BaseModel):
    """角色状态更新"""
    status: int


class RoleMenusUpdate(BaseModel):
    """角色菜单权限更新"""
    menu_ids: List[int]