from abc import ABC, abstractmethod
from typing import Optional, List
from app.domain.repositories.base_repository import BaseRepository
from app.domain.models.user import User

class UserRepository(BaseRepository[User], ABC):
    """用户仓储接口"""
    
    @abstractmethod
    async def find_by_username(self, username: str) -> Optional[User]:
        """根据用户名查找用户"""
        pass
    
    @abstractmethod
    async def find_by_email(self, email: str) -> Optional[User]:
        """根据邮箱查找用户"""
        pass
    
    @abstractmethod
    async def find_by_dept(self, dept_id: str) -> List[User]:
        """根据部门ID查找用户"""
        pass
    
    @abstractmethod
    async def find_active_users(self) -> List[User]:
        """查找活跃用户"""
        pass
    
    @abstractmethod
    async def update_last_login(self, user_id: str) -> bool:
        """更新最后登录时间"""
        pass