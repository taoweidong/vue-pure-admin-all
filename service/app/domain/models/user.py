from typing import List, Optional, TYPE_CHECKING
from pydantic import BaseModel, EmailStr
from datetime import datetime

if TYPE_CHECKING:
    from app.domain.models.role import Role

class User(BaseModel):
    """用户领域模型"""
    id: str
    username: str
    nickname: str
    email: EmailStr
    phone: str
    is_active: bool
    dept_id: Optional[str] = None
    roles: List['Role'] = []
    created_time: datetime
    updated_time: datetime
    
    def has_permission(self, permission: str) -> bool:
        """检查用户是否有指定权限"""
        for role in self.roles:
            if role.has_permission(permission):
                return True
        return False
    
    def is_admin(self) -> bool:
        """检查是否为管理员"""
        return any(role.name == "admin" for role in self.roles)
    
    def get_role_names(self) -> List[str]:
        """获取角色名称列表"""
        return [role.name for role in self.roles]

# 模型重建将在模块导入完成后进行