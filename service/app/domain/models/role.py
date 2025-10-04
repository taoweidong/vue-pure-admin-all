from typing import List, Optional, TYPE_CHECKING
from pydantic import BaseModel

if TYPE_CHECKING:
    from domain.models.menu import Menu

class Role(BaseModel):
    """角色领域模型"""
    id: str
    name: str
    description: str
    is_active: bool
    menus: List['Menu'] = []
    data_permissions: List['DataPermission'] = []
    field_permissions: List['FieldPermission'] = []
    
    def has_permission(self, permission: str) -> bool:
        """检查角色是否有指定权限"""
        return any(menu.path == permission for menu in self.menus)
    
    def get_menu_ids(self) -> List[str]:
        """获取菜单ID列表"""
        return [menu.id for menu in self.menus]
    
    def can_access_menu(self, menu_id: str) -> bool:
        """检查是否可以访问指定菜单"""
        return menu_id in self.get_menu_ids()
    
    def is_super_admin(self) -> bool:
        """检查是否为超级管理员"""
        return self.name == "super_admin"

class DataPermission(BaseModel):
    """数据权限模型"""
    id: str
    name: str
    description: str
    rule_type: str  # all, dept, custom
    rule_value: Optional[str] = None

class FieldPermission(BaseModel):
    """字段权限模型"""
    model_config = {"protected_namespaces": ()}
    
    id: str
    name: str
    description: str
    model_name: str
    field_name: str
    permission_type: str  # read, write, hide

# 模型重建将在模块导入完成后进行
# 避免循环导入问题