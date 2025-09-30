from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from app.domain.entities.models import User, UserRole, Role
from app.domain.entities.logs import LoginLog
from app.infrastructure.utils.auth import AuthService
from typing import Optional, Tuple, List


class UserService:
    def __init__(self, db: Session):
        self.db = db
        self.auth_service = AuthService()

    def get_user_by_username(self, username: str) -> Optional[User]:
        """根据用户名获取用户"""
        return self.db.query(User).filter(User.username == username).first()

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """根据用户ID获取用户"""
        return self.db.query(User).filter(User.id == user_id).first()

    def verify_user_password(self, user: User, password: str) -> bool:
        """验证用户密码"""
        return self.auth_service.verify_password(password, user.password_hash)

    def get_user_roles(self, user_id: int) -> List[str]:
        """获取用户角色列表"""
        user_roles = self.db.query(UserRole).filter(UserRole.user_id == user_id).all()
        roles = []
        for user_role in user_roles:
            role = self.db.query(Role).filter(Role.id == user_role.role_id).first()
            if role:
                roles.append(role.code)
        return roles

    def get_user_permissions(self, user_id: int) -> List[str]:
        """获取用户权限列表"""
        # 这里可以根据角色获取权限，暂时返回基础权限
        roles = self.get_user_roles(user_id)
        if "admin" in roles:
            return ["*:*:*"]
        else:
            return ["permission:btn:add", "permission:btn:edit"]

    def get_user_list(
        self,
        username: Optional[str] = None,
        status: Optional[int] = None,
        phone: Optional[str] = None,
        dept_id: Optional[int] = None,
        page: int = 1,
        page_size: int = 10
    ) -> Tuple[List[User], int]:
        """获取用户列表"""
        query = self.db.query(User)
        
        # 添加过滤条件
        if username:
            query = query.filter(User.username.contains(username))
        if status is not None:
            query = query.filter(User.status == status)
        if phone:
            query = query.filter(User.phone == phone)
        if dept_id:
            query = query.filter(User.dept_id == dept_id)
        
        # 获取总数
        total = query.count()
        
        # 分页
        offset = (page - 1) * page_size
        users = query.offset(offset).limit(page_size).all()
        
        return users, total

    def get_user_logs(self, user_id: int) -> List[LoginLog]:
        """获取用户登录日志"""
        return self.db.query(LoginLog).filter(LoginLog.user_id == user_id).order_by(LoginLog.login_time.desc()).limit(10).all()

    def create_user(self, user_data: dict) -> User:
        """创建用户"""
        # 检查用户名是否存在
        existing_user = self.get_user_by_username(user_data['username'])
        if existing_user:
            raise ValueError("Username already exists")
        
        # 加密密码
        password_hash = self.auth_service.get_password_hash(user_data['password'])
        
        # 创建用户
        user = User(
            username=user_data['username'],
            nickname=user_data['nickname'],
            email=user_data.get('email'),
            phone=user_data.get('phone'),
            avatar=user_data.get('avatar'),
            password_hash=password_hash,
            description=user_data.get('description'),
            sex=user_data.get('sex', 0),
            dept_id=user_data.get('dept_id'),
            remark=user_data.get('remark')
        )
        
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update_user(self, user_id: int, user_data: dict) -> User:
        """更新用户"""
        user = self.get_user_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        
        # 更新用户信息
        for key, value in user_data.items():
            if hasattr(user, key) and value is not None:
                setattr(user, key, value)
        
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete_user(self, user_id: int) -> bool:
        """删除用户"""
        user = self.get_user_by_id(user_id)
        if not user:
            return False
        
        self.db.delete(user)
        self.db.commit()
        return True