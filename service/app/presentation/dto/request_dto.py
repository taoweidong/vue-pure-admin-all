from typing import Optional, List
from pydantic import BaseModel

class PaginationRequest(BaseModel):
    """分页请求模型"""
    skip: int = 0
    limit: int = 100
    
class SearchRequest(BaseModel):
    """搜索请求模型"""
    keyword: Optional[str] = None
    filters: dict = {}

class BatchRequest(BaseModel):
    """批量操作请求模型"""
    ids: List[str]
    
class SortRequest(BaseModel):
    """排序请求模型"""
    field: str
    order: str = "asc"  # asc, desc