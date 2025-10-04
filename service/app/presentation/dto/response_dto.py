from typing import Generic, TypeVar, Optional, List, Any
from pydantic import BaseModel

T = TypeVar('T')

class BaseResponse(BaseModel, Generic[T]):
    """基础响应模型"""
    code: int = 200
    message: str = "success"
    data: Optional[T] = None

class SuccessResponse(BaseResponse[T]):
    """成功响应"""
    def __init__(self, data: T = None, message: str = "操作成功", **kwargs):
        super().__init__(code=200, message=message, data=data, **kwargs)

class ErrorResponse(BaseResponse[None]):
    """错误响应"""
    def __init__(self, message: str = "操作失败", code: int = 400, **kwargs):
        super().__init__(code=code, message=message, data=None, **kwargs)

class PageResponse(BaseModel, Generic[T]):
    """分页响应模型"""
    code: int = 200
    message: str = "success"
    data: List[T]
    total: int
    skip: int
    limit: int
    
    def __init__(self, data: List[T], total: int, skip: int = 0, limit: int = 100, **kwargs):
        super().__init__(
            code=200,
            message="success",
            data=data,
            total=total,
            skip=skip,
            limit=limit,
            **kwargs
        )

class TokenResponse(BaseModel):
    """令牌响应"""
    access_token: str
    token_type: str = "bearer"
    expires_in: int