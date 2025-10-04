from typing import List, Optional
from pydantic import BaseModel

class Menu(BaseModel):
    """菜单/权限领域模型"""
    id: str
    name: str
    path: str
    component: Optional[str] = None
    menu_type: int  # 0: 目录, 1: 菜单, 2: 按钮
    parent_id: Optional[str] = None
    rank: int
    is_active: bool
    meta: dict = {}
    children: List['Menu'] = []
    
    def is_directory(self) -> bool:
        """判断是否为目录"""
        return self.menu_type == 0
    
    def is_menu(self) -> bool:
        """判断是否为菜单"""
        return self.menu_type == 1
    
    def is_button(self) -> bool:
        """判断是否为按钮"""
        return self.menu_type == 2
    
    def get_all_children_ids(self) -> List[str]:
        """获取所有子菜单ID"""
        ids = [self.id]
        for child in self.children:
            ids.extend(child.get_all_children_ids())
        return ids
    
    def get_breadcrumb(self) -> List[str]:
        """获取面包屑路径"""
        # 简化实现，实际需要递归获取父菜单
        return [self.name]

Menu.model_rebuild()