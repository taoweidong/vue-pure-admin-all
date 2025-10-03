from pydantic import BaseModel, EmailStr
from typing import Optional, List, Any
from datetime import datetime


class BaseResponse(BaseModel):
    """基础响应模型"""
    success: bool
    message: Optional[str] = None


class LoginRequest(BaseModel):
    """登录请求"""
    username: str
    password: str


class LoginResponse(BaseResponse):
    """登录响应"""
    data: Optional[dict] = None


class RefreshTokenRequest(BaseModel):
    """刷新令牌请求"""
    refreshToken: str


class RefreshTokenResponse(BaseResponse):
    """刷新令牌响应"""
    data: Optional[dict] = None


class UserInfo(BaseModel):
    """用户信息"""
    avatar: Optional[str] = None
    username: str
    nickname: str
    email: Optional[str] = None
    phone: Optional[str] = None
    description: Optional[str] = None

    class Config:
        from_attributes = True


class UserInfoResponse(BaseResponse):
    """用户信息响应"""
    data: Optional[UserInfo] = None


class UserCreate(BaseModel):
    """创建用户"""
    username: str
    password: str
    nickname: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    avatar: Optional[str] = None
    description: Optional[str] = None
    sex: Optional[int] = 0
    dept_id: Optional[int] = None
    remark: Optional[str] = None


class UserUpdate(BaseModel):
    """更新用户"""
    nickname: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    avatar: Optional[str] = None
    description: Optional[str] = None
    sex: Optional[int] = None
    status: Optional[int] = None
    dept_id: Optional[int] = None
    remark: Optional[str] = None


class UserList(BaseModel):
    """用户列表项"""
    id: int
    username: str
    nickname: str
    email: Optional[str] = None
    phone: Optional[str] = None
    avatar: Optional[str] = None
    sex: int
    status: int
    dept: Optional[dict] = None
    remark: Optional[str] = None
    createTime: Optional[int] = None

    class Config:
        from_attributes = True


class UserListRequest(BaseModel):
    """用户列表请求"""
    username: Optional[str] = None
    status: Optional[int] = None
    phone: Optional[str] = None
    deptId: Optional[int] = None
    pageSize: Optional[int] = 10
    currentPage: Optional[int] = 1


class UserListResponse(BaseResponse):
    """用户列表响应"""
    data: Optional[dict] = None


class PageResponse(BaseModel):
    """分页响应"""
    list: List[Any]
    total: int
    pageSize: int
    currentPage: int


class TableResponse(BaseResponse):
    """表格响应"""
    data: Optional[PageResponse] = None


class UserInList(BaseModel):
    """用户列表项"""
    id: int
    username: str
    nickname: str
    email: Optional[str] = None
    phone: Optional[str] = None
    avatar: Optional[str] = None
    sex: int
    status: int
    dept: Optional[dict] = None
    remark: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class UserDetail(BaseModel):
    """用户详情"""
    id: int
    username: str
    nickname: str
    email: Optional[str] = None
    phone: Optional[str] = None
    avatar: Optional[str] = None
    description: Optional[str] = None
    sex: int
    status: int
    dept: Optional[dict] = None
    roles: List[dict] = []
    remark: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class UserStatusUpdate(BaseModel):
    """用户状态更新"""
    status: int


class PasswordResetRequest(BaseModel):
    """密码重置请求"""
    password: str