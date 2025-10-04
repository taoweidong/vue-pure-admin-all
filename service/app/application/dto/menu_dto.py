from typing import Optional, List, Dict, Any
from pydantic import BaseModel
from datetime import datetime

class MenuCreate(BaseModel):
    """创建菜单DTO"""
    name: str
    path: str
    component: Optional[str] = None
    menu_type: int = 1  # 0: 目录, 1: 菜单, 2: 按钮
    parent_id: Optional[str] = None
    rank: int = 0
    meta: Dict[str, Any] = {}

class MenuUpdate(BaseModel):
    """更新菜单DTO"""
    name: Optional[str] = None
    path: Optional[str] = None
    component: Optional[str] = None
    menu_type: Optional[int] = None
    parent_id: Optional[str] = None
    rank: Optional[int] = None
    meta: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None

class MenuResponse(BaseModel):
    """菜单响应DTO"""
    id: str
    name: str
    path: str
    component: Optional[str]
    menu_type: int
    parent_id: Optional[str]
    rank: int
    is_active: bool
    meta: Dict[str, Any]
    children: List['MenuResponse'] = []
    created_time: datetime
    updated_time: datetime

    @classmethod
    def from_domain(cls, menu) -> "MenuResponse":
        """从领域模型转换"""
        return cls(
            id=menu.id,
            name=menu.name,
            path=menu.path,
            component=menu.component,
            menu_type=menu.menu_type,
            parent_id=menu.parent_id,
            rank=menu.rank,
            is_active=menu.is_active,
            meta=menu.meta,
            children=[],
            created_time=menu.created_time if hasattr(menu, 'created_time') else datetime.now(),
            updated_time=menu.updated_time if hasattr(menu, 'updated_time') else datetime.now()
        )

MenuResponse.model_rebuild()