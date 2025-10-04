from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime

class RoleCreate(BaseModel):
    """创建角色DTO"""
    name: str
    description: Optional[str] = None

class RoleUpdate(BaseModel):
    """更新角色DTO"""
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None

class RoleResponse(BaseModel):
    """角色响应DTO"""
    id: str
    name: str
    description: Optional[str]
    is_active: bool
    menu_count: int = 0
    user_count: int = 0
    created_time: datetime
    updated_time: datetime

    @classmethod
    def from_domain(cls, role) -> "RoleResponse":
        """从领域模型转换"""
        return cls(
            id=role.id,
            name=role.name,
            description=role.description,
            is_active=role.is_active,
            menu_count=len(role.menus),
            created_time=role.created_time if hasattr(role, 'created_time') else datetime.now(),
            updated_time=role.updated_time if hasattr(role, 'updated_time') else datetime.now()
        )

class RoleAssignMenus(BaseModel):
    """角色分配菜单DTO"""
    menu_ids: List[str]