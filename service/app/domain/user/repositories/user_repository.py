"""
用户仓储接口
"""
from abc import ABC, abstractmethod
from typing import List, Optional

from app.domain.user.aggregates.user_aggregate import UserAggregate
from app.domain.user.entities.user import User


class IUserRepository(ABC):
    """用户仓储接口"""
    
    @abstractmethod
    def get_by_id(self, user_id: int) -> Optional[UserAggregate]:
        """根据ID获取用户聚合"""
        pass
    
    @abstractmethod
    def get_by_username(self, username: str) -> Optional[UserAggregate]:
        """根据用户名获取用户聚合"""
        pass
    
    @abstractmethod
    def get_by_email(self, email: str) -> Optional[UserAggregate]:
        """根据邮箱获取用户聚合"""
        pass
    
    @abstractmethod
    def get_by_phone(self, phone: str) -> Optional[UserAggregate]:
        """根据手机号获取用户聚合"""
        pass
    
    @abstractmethod
    def find_all(
        self, 
        page: int = 1, 
        page_size: int = 10,
        filters: Optional[dict] = None
    ) -> tuple[List[UserAggregate], int]:
        """分页查询用户"""
        pass
    
    @abstractmethod
    def save(self, user_aggregate: UserAggregate) -> UserAggregate:
        """保存用户聚合"""
        pass
    
    @abstractmethod
    def delete(self, user_id: int) -> bool:
        """删除用户"""
        pass
    
    @abstractmethod
    def exists_by_username(self, username: str) -> bool:
        """检查用户名是否存在"""
        pass
    
    @abstractmethod
    def exists_by_email(self, email: str) -> bool:
        """检查邮箱是否存在"""
        pass
    
    @abstractmethod
    def exists_by_phone(self, phone: str) -> bool:
        """检查手机号是否存在"""
        pass