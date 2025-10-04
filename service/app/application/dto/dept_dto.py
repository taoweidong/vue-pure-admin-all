from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime

class DeptCreate(BaseModel):
    """创建部门DTO"""
    name: str
    code: str
    parent_id: Optional[str] = None
    rank: int = 0
    auto_bind: bool = False

class DeptUpdate(BaseModel):
    """更新部门DTO"""
    name: Optional[str] = None
    code: Optional[str] = None
    parent_id: Optional[str] = None
    rank: Optional[int] = None
    auto_bind: Optional[bool] = None
    is_active: Optional[bool] = None

class DeptResponse(BaseModel):
    """部门响应DTO"""
    id: str
    name: str
    code: str
    parent_id: Optional[str]
    rank: int
    auto_bind: bool
    is_active: bool
    children: List['DeptResponse'] = []
    user_count: int = 0
    created_time: datetime
    updated_time: datetime

    @classmethod
    def from_domain(cls, dept) -> "DeptResponse":
        """从领域模型转换"""
        return cls(
            id=dept.id,
            name=dept.name,
            code=dept.code,
            parent_id=dept.parent_id,
            rank=dept.rank,
            auto_bind=dept.auto_bind,
            is_active=dept.is_active,
            children=[],
            created_time=dept.created_time if hasattr(dept, 'created_time') else datetime.now(),
            updated_time=dept.updated_time if hasattr(dept, 'updated_time') else datetime.now()
        )

DeptResponse.model_rebuild()