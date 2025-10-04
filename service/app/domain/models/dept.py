from typing import List, Optional
from pydantic import BaseModel

class Department(BaseModel):
    """部门领域模型"""
    id: str
    name: str
    code: str
    parent_id: Optional[str] = None
    rank: int
    is_active: bool
    auto_bind: bool
    children: List['Department'] = []
    
    def get_all_children_ids(self) -> List[str]:
        """获取所有子部门ID"""
        ids = [self.id]
        for child in self.children:
            ids.extend(child.get_all_children_ids())
        return ids
    
    def is_root(self) -> bool:
        """判断是否为根部门"""
        return self.parent_id is None
    
    def get_level(self) -> int:
        """获取部门层级"""
        if self.is_root():
            return 1
        # 这里需要递归计算，简化处理
        return 1
    
    def get_full_path(self) -> str:
        """获取完整路径"""
        # 简化实现，实际需要递归获取父部门路径
        return self.name

Department.model_rebuild()