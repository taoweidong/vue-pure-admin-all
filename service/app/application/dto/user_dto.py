from typing import Optional, List
from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserCreate(BaseModel):
    """创建用户DTO"""
    username: str
    nickname: str
    email: EmailStr
    phone: Optional[str] = None
    password: str
    dept_id: Optional[str] = None

class UserUpdate(BaseModel):
    """更新用户DTO"""
    nickname: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    dept_id: Optional[str] = None
    is_active: Optional[bool] = None

class UserResponse(BaseModel):
    """用户响应DTO"""
    id: str
    username: str
    nickname: str
    email: str
    phone: Optional[str]
    is_active: bool
    dept_id: Optional[str]
    role_names: List[str] = []
    created_time: datetime
    updated_time: datetime

    @classmethod
    def from_domain(cls, user) -> "UserResponse":
        """从领域模型转换"""
        return cls(
            id=user.id,
            username=user.username,
            nickname=user.nickname,
            email=user.email,
            phone=user.phone,
            is_active=user.is_active,
            dept_id=user.dept_id,
            role_names=user.get_role_names(),
            created_time=user.created_time,
            updated_time=user.updated_time
        )

class UserLogin(BaseModel):
    """用户登录DTO"""
    username: str
    password: str

class UserAssignRoles(BaseModel):
    """用户分配角色DTO"""
    role_ids: List[str]