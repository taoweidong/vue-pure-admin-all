from typing import List, Optional
import uuid
from datetime import datetime

from domain.models.user import User
from domain.repositories.user_repository import UserRepository
from application.dto.user_dto import UserCreate, UserUpdate
from shared.kernel.exceptions import BusinessException
from infrastructure.auth.password_handler import PasswordHandler

class UserService:
    """用户应用服务"""
    
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo
        self.password_handler = PasswordHandler()

    async def list_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        """获取用户列表"""
        return await self.user_repo.get_all(skip=skip, limit=limit)

    async def get_user(self, user_id: str) -> Optional[User]:
        """获取用户详情"""
        return await self.user_repo.get_by_id(user_id)

    async def create_user(self, user_in: UserCreate) -> User:
        """创建用户"""
        # 检查用户名唯一性
        existing_user = await self.user_repo.find_by_username(user_in.username)
        if existing_user:
            raise BusinessException("用户名已存在")
        
        # 检查邮箱唯一性
        existing_email = await self.user_repo.find_by_email(user_in.email)
        if existing_email:
            raise BusinessException("邮箱已存在")
        
        # 创建用户领域对象
        user = User(
            id=str(uuid.uuid4()),
            username=user_in.username,
            nickname=user_in.nickname,
            email=user_in.email,
            phone=user_in.phone or "",
            dept_id=user_in.dept_id,
            is_active=True,
            roles=[],
            created_time=datetime.now(),
            updated_time=datetime.now()
        )
        
        # 这里需要转换为数据库模型并保存
        # 简化实现，实际需要在仓储层处理
        return user

    async def update_user(self, user_id: str, user_update: UserUpdate) -> Optional[User]:
        """更新用户信息"""
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            return None
            
        updates = user_update.dict(exclude_unset=True)
        updates['updated_time'] = datetime.now()
        
        return await self.user_repo.update(user_id, **updates)

    async def delete_user(self, user_id: str) -> bool:
        """删除用户"""
        return await self.user_repo.delete(user_id)

    async def count_users(self) -> int:
        """统计用户数量"""
        return await self.user_repo.count()

    async def find_by_username(self, username: str) -> Optional[User]:
        """根据用户名查找用户"""
        return await self.user_repo.find_by_username(username)

    async def authenticate_user(self, username: str, password: str) -> Optional[User]:
        """用户认证"""
        user = await self.user_repo.find_by_username(username)
        if not user or not user.is_active:
            return None
        
        # 密码验证逻辑需要在这里实现
        # if not self.password_handler.verify_password(password, user.hashed_password):
        #     return None
        
        return user