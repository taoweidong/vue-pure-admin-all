from pydantic import BaseModel, EmailStr
from typing import Optional
from app.presentation.schemas.common import BaseResponse


class LoginRequest(BaseModel):
    """登录请求"""
    username: str
    password: str


class LoginResponse(BaseResponse):
    """登录响应"""
    pass


class RefreshTokenRequest(BaseModel):
    """刷新令牌请求"""
    refreshToken: str


class RefreshTokenResponse(BaseResponse):
    """刷新令牌响应"""
    pass


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


class UserInfoResponse(BaseResponse[UserInfo]):
    """用户信息响应"""
    pass


class ChangePasswordRequest(BaseModel):
    """修改密码请求"""
    old_password: str
    new_password: str