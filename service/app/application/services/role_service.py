from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from app.domain.entities.models import Role, RoleMenu, Menu, UserRole
from app.presentation.schemas.role import RoleCreate, RoleUpdate
from typing import Optional, Tuple, List


class RoleService:
    def __init__(self, db: Session):
        self.db = db

    def get_role_by_id(self, role_id: int) -> Optional[Role]:
        """根据角色ID获取角色"""
        return self.db.query(Role).filter(Role.id == role_id).first()

    def get_role_by_name(self, name: str) -> Optional[Role]:
        """根据角色名称获取角色"""
        return self.db.query(Role).filter(Role.name == name).first()

    def get_role_by_code(self, code: str) -> Optional[Role]:
        """根据角色编码获取角色"""
        return self.db.query(Role).filter(Role.code == code).first()

    def get_roles_paginated(
        self,
        page: int = 1,
        page_size: int = 10,
        name: Optional[str] = None,
        code: Optional[str] = None,
        status: Optional[int] = None
    ) -> Tuple[List[Role], int]:
        """获取分页角色列表"""
        query = self.db.query(Role)
        
        # 添加过滤条件
        if name:
            query = query.filter(Role.name.contains(name))
        if code:
            query = query.filter(Role.code.contains(code))
        if status is not None:
            query = query.filter(Role.status == status)
        
        # 获取总数
        total = query.count()
        
        # 分页
        offset = (page - 1) * page_size
        roles = query.offset(offset).limit(page_size).all()
        
        return roles, total

    def get_all_roles(self) -> List[Role]:
        """获取所有角色"""
        return self.db.query(Role).filter(Role.status == 1).all()

    def create_role(self, role_data: RoleCreate) -> Role:
        """创建角色"""
        role = Role(
            name=role_data.name,
            code=role_data.code,
            status=role_data.status,
            remark=role_data.remark
        )
        
        self.db.add(role)
        self.db.commit()
        self.db.refresh(role)
        return role

    def update_role(self, role_id: int, role_data: RoleUpdate) -> Role:
        """更新角色"""
        role = self.get_role_by_id(role_id)
        if not role:
            raise ValueError("Role not found")
        
        # 更新角色信息
        update_data = role_data.dict(exclude_unset=True)
        for key, value in update_data.items():
            if hasattr(role, key):
                setattr(role, key, value)
        
        self.db.commit()
        self.db.refresh(role)
        return role

    def update_role_status(self, role_id: int, status: int) -> bool:
        """更新角色状态"""
        role = self.get_role_by_id(role_id)
        if not role:
            raise ValueError("Role not found")
        
        role.status = status
        self.db.commit()
        return True

    def delete_role(self, role_id: int) -> bool:
        """删除角色"""
        role = self.get_role_by_id(role_id)
        if not role:
            return False
        
        # 删除角色菜单关联
        self.db.query(RoleMenu).filter(RoleMenu.role_id == role_id).delete()
        
        # 删除用户角色关联
        self.db.query(UserRole).filter(UserRole.role_id == role_id).delete()
        
        # 删除角色
        self.db.delete(role)
        self.db.commit()
        return True

    def check_role_in_use(self, role_id: int) -> bool:
        """检查角色是否被用户使用"""
        count = self.db.query(UserRole).filter(UserRole.role_id == role_id).count()
        return count > 0

    def get_role_menus(self, role_id: int) -> List[Menu]:
        """获取角色菜单权限"""
        role_menus = self.db.query(RoleMenu).filter(RoleMenu.role_id == role_id).all()
        menus = []
        for role_menu in role_menus:
            menu = self.db.query(Menu).filter(Menu.id == role_menu.menu_id).first()
            if menu:
                menus.append(menu)
        return menus

    def get_role_menu_ids(self, role_id: int) -> List[int]:
        """获取角色菜单ID列表"""
        role_menus = self.db.query(RoleMenu).filter(RoleMenu.role_id == role_id).all()
        return [role_menu.menu_id for role_menu in role_menus]

    def update_role_menus(self, role_id: int, menu_ids: List[int]) -> bool:
        """更新角色菜单权限"""
        # 删除原有的角色菜单关联
        self.db.query(RoleMenu).filter(RoleMenu.role_id == role_id).delete()
        
        # 添加新的角色菜单关联
        for menu_id in menu_ids:
            role_menu = RoleMenu(role_id=role_id, menu_id=menu_id)
            self.db.add(role_menu)
        
        self.db.commit()
        return True