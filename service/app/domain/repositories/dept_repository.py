from abc import ABC, abstractmethod
from typing import Optional, List
from app.domain.repositories.base_repository import BaseRepository
from app.domain.models.dept import Department

class DeptRepository(BaseRepository[Department], ABC):
    """部门仓储接口"""
    
    @abstractmethod
    async def find_by_code(self, code: str) -> Optional[Department]:
        """根据部门代码查找部门"""
        pass
    
    @abstractmethod
    async def find_children(self, parent_id: str) -> List[Department]:
        """查找子部门"""
        pass
    
    @abstractmethod
    async def find_root_depts(self) -> List[Department]:
        """查找根部门"""
        pass
    
    @abstractmethod
    async def build_tree(self) -> List[Department]:
        """构建部门树"""
        pass