from pydantic import BaseModel
from typing import Optional, List, Any, Generic, TypeVar
from datetime import datetime

T = TypeVar('T')


class BaseResponse(BaseModel, Generic[T]):
    """基础响应模型"""
    success: bool
    message: Optional[str] = None
    data: Optional[T] = None
    errors: Optional[List[dict]] = None


class PaginationData(BaseModel, Generic[T]):
    """分页数据模型"""
    items: List[T]
    total: int
    page: int
    page_size: int
    pages: int


class PaginatedResponse(BaseModel, Generic[T]):
    """分页响应模型"""
    success: bool
    message: Optional[str] = None
    data: Optional[PaginationData[T]] = None
    errors: Optional[List[dict]] = None


class StatusUpdate(BaseModel):
    """状态更新模型"""
    status: int


class IDsRequest(BaseModel):
    """ID列表请求模型"""
    ids: List[int]


class SimpleItem(BaseModel):
    """简单项模型"""
    id: int
    name: str
    code: Optional[str] = None