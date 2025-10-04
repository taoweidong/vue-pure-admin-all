from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Optional, List, Dict, Any
from uuid import UUID

T = TypeVar('T')

class BaseRepository(Generic[T], ABC):
    """通用仓储接口"""
    
    @abstractmethod
    async def create(self, entity: T) -> T:
        """创建实体"""
        pass
    
    @abstractmethod
    async def get_by_id(self, id: str) -> Optional[T]:
        """根据ID获取实体"""
        pass
    
    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[T]:
        """获取所有实体"""
        pass
    
    @abstractmethod
    async def filter_by(self, **kwargs) -> List[T]:
        """根据条件过滤实体"""
        pass
    
    @abstractmethod
    async def update(self, id: str, **updates) -> Optional[T]:
        """更新实体"""
        pass
    
    @abstractmethod
    async def delete(self, id: str) -> bool:
        """删除实体"""
        pass
    
    @abstractmethod
    async def count(self) -> int:
        """统计数量"""
        pass