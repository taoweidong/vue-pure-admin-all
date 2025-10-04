from sqlalchemy.orm import Session
from app.domain.entities.models import User, Role, Menu, Department, UserRole, RoleMenu
from app.domain.audit.entities.log import LoginLog, OperationLog, SystemLog
from app.domain.entities.online_user import OnlineUser
from app.infrastructure.utils.auth import AuthService
from typing import Optional, Tuple, List
import datetime


class SystemService:
    def __init__(self, db: Session):
        self.db = db

    def get_all_roles(self) -> List[Role]:
        """获取所有角色"""
        return self.db.query(Role).filter(Role.status == 1).all()

    def get_user_role_ids(self, user_id: int) -> List[int]:
        """获取用户的角色ID列表"""
        user_roles = self.db.query(UserRole).filter(UserRole.user_id == user_id).all()
        role_ids = []
        for ur in user_roles:
            role_ids.append(ur.role_id)
        return role_ids

    def get_role_list(
        self,
        name: Optional[str] = None,
        code: Optional[str] = None,
        status: Optional[int] = None,
        page: int = 1,
        page_size: int = 10
    ) -> Tuple[List[Role], int]:
        """获取角色列表"""
        query = self.db.query(Role)
        
        # 添加过滤条件
        if name:
            query = query.filter(Role.name.contains(name))
        if code:
            query = query.filter(Role.code == code)
        if status is not None:
            query = query.filter(Role.status == status)
        
        # 获取总数
        total = query.count()
        
        # 分页
        offset = (page - 1) * page_size
        roles = query.offset(offset).limit(page_size).all()
        
        return roles, total

    def get_menu_list(self) -> List[Menu]:
        """获取菜单列表"""
        return self.db.query(Menu).order_by(Menu.rank.asc()).all()

    def get_dept_list(self) -> List[Department]:
        """获取部门列表"""
        return self.db.query(Department).order_by(Department.sort.asc()).all()

    def get_role_menu_ids(self, role_id: int) -> List[int]:
        """获取角色的菜单ID列表"""
        role_menus = self.db.query(RoleMenu).filter(RoleMenu.role_id == role_id).all()
        menu_ids = []
        for rm in role_menus:
            menu_ids.append(rm.menu_id)
        return menu_ids

    def get_online_logs(self, page: int = 1, page_size: int = 10) -> Tuple[List[OnlineUser], int]:
        """获取在线用户列表"""
        query = self.db.query(OnlineUser)
        total = query.count()
        
        offset = (page - 1) * page_size
        online_users = query.offset(offset).limit(page_size).all()
        
        return online_users, total

    def get_login_logs(self, page: int = 1, page_size: int = 10) -> Tuple[List[LoginLog], int]:
        """获取登录日志列表"""
        query = self.db.query(LoginLog).order_by(LoginLog.login_time.desc())
        total = query.count()
        
        offset = (page - 1) * page_size
        logs = query.offset(offset).limit(page_size).all()
        
        return logs, total

    def get_operation_logs(self, page: int = 1, page_size: int = 10) -> Tuple[List[OperationLog], int]:
        """获取操作日志列表"""
        query = self.db.query(OperationLog).order_by(OperationLog.operate_time.desc())
        total = query.count()
        
        offset = (page - 1) * page_size
        logs = query.offset(offset).limit(page_size).all()
        
        return logs, total

    def get_system_logs(self, page: int = 1, page_size: int = 10) -> Tuple[List[SystemLog], int]:
        """获取系统日志列表"""
        query = self.db.query(SystemLog).order_by(SystemLog.created_at.desc())
        total = query.count()
        
        offset = (page - 1) * page_size
        logs = query.offset(offset).limit(page_size).all()
        
        return logs, total

    def get_system_log_detail(self, log_id: int) -> Optional[SystemLog]:
        """获取系统日志详情"""
        return self.db.query(SystemLog).filter(SystemLog.id == log_id).first()

    def create_role(self, role_data: dict) -> Role:
        """创建角色"""
        # 检查角色编码是否存在
        existing_role = self.db.query(Role).filter(Role.code == role_data['code']).first()
        if existing_role:
            raise ValueError("Role code already exists")
        
        role = Role(
            name=role_data['name'],
            code=role_data['code'],
            status=role_data.get('status', 1),
            remark=role_data.get('remark')
        )
        
        self.db.add(role)
        self.db.commit()
        self.db.refresh(role)
        return role

    def update_role(self, role_id: int, role_data: dict) -> Role:
        """更新角色"""
        role = self.db.query(Role).filter(Role.id == role_id).first()
        if not role:
            raise ValueError("Role not found")
        
        # 更新角色信息
        for key, value in role_data.items():
            if hasattr(role, key) and value is not None:
                setattr(role, key, value)
        
        self.db.commit()
        self.db.refresh(role)
        return role

    def delete_role(self, role_id: int) -> bool:
        """删除角色"""
        role = self.db.query(Role).filter(Role.id == role_id).first()
        if not role:
            return False
        
        # 检查是否有用户使用该角色
        user_roles = self.db.query(UserRole).filter(UserRole.role_id == role_id).first()
        if user_roles:
            raise ValueError("Cannot delete role: users are assigned to this role")
        
        self.db.delete(role)
        self.db.commit()
        return True

    def create_menu(self, menu_data: dict) -> Menu:
        """创建菜单"""
        menu = Menu(**menu_data)
        self.db.add(menu)
        self.db.commit()
        self.db.refresh(menu)
        return menu

    def update_menu(self, menu_id: int, menu_data: dict) -> Menu:
        """更新菜单"""
        menu = self.db.query(Menu).filter(Menu.id == menu_id).first()
        if not menu:
            raise ValueError("Menu not found")
        
        for key, value in menu_data.items():
            if hasattr(menu, key) and value is not None:
                setattr(menu, key, value)
        
        self.db.commit()
        self.db.refresh(menu)
        return menu

    def delete_menu(self, menu_id: int) -> bool:
        """删除菜单"""
        menu = self.db.query(Menu).filter(Menu.id == menu_id).first()
        if not menu:
            return False
        
        # 检查是否有子菜单
        children = self.db.query(Menu).filter(Menu.parent_id == menu_id).first()
        if children:
            raise ValueError("Cannot delete menu: has child menus")
        
        self.db.delete(menu)
        self.db.commit()
        return True