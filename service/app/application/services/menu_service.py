from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from app.domain.entities.models import Menu, RoleMenu
from app.presentation.schemas.menu import MenuCreate, MenuUpdate
from typing import Optional, Tuple, List, Dict, Any


class MenuService:
    def __init__(self, db: Session):
        self.db = db

    def get_menu_by_id(self, menu_id: int) -> Optional[Menu]:
        """根据菜单ID获取菜单"""
        return self.db.query(Menu).filter(Menu.id == menu_id).first()

    def get_menu_by_name(self, name: str) -> Optional[Menu]:
        """根据菜单名称获取菜单"""
        return self.db.query(Menu).filter(Menu.name == name).first()

    def get_menus_paginated(
        self,
        page: int = 1,
        page_size: int = 10,
        title: Optional[str] = None,
        name: Optional[str] = None,
        menu_type: Optional[int] = None
    ) -> Tuple[List[Menu], int]:
        """获取分页菜单列表"""
        query = self.db.query(Menu)
        
        # 添加过滤条件
        if title:
            query = query.filter(Menu.title.contains(title))
        if name:
            query = query.filter(Menu.name.contains(name))
        if menu_type is not None:
            query = query.filter(Menu.menu_type == menu_type)
        
        # 获取总数
        total = query.count()
        
        # 分页
        offset = (page - 1) * page_size
        menus = query.order_by(Menu.rank.asc(), Menu.id.asc()).offset(offset).limit(page_size).all()
        
        return menus, total

    def get_all_menus(self) -> List[Menu]:
        """获取所有菜单"""
        return self.db.query(Menu).order_by(Menu.rank.asc(), Menu.id.asc()).all()

    def get_menu_tree(self) -> List[Dict[str, Any]]:
        """获取菜单树"""
        menus = self.get_all_menus()
        return self._build_tree(menus)

    def _build_tree(self, menus: List[Menu], parent_id: int = 0) -> List[Dict[str, Any]]:
        """构建菜单树"""
        tree = []
        for menu in menus:
            if menu.parent_id == parent_id:
                menu_dict = {
                    "id": menu.id,
                    "parent_id": menu.parent_id,
                    "title": menu.title,
                    "name": menu.name,
                    "path": menu.path,
                    "component": menu.component,
                    "menu_type": menu.menu_type,
                    "rank": menu.rank,
                    "redirect": menu.redirect,
                    "icon": menu.icon,
                    "extra_icon": menu.extra_icon,
                    "enter_transition": menu.enter_transition,
                    "leave_transition": menu.leave_transition,
                    "active_path": menu.active_path,
                    "auths": menu.auths,
                    "frame_src": menu.frame_src,
                    "frame_loading": menu.frame_loading,
                    "keep_alive": menu.keep_alive,
                    "hidden_tag": menu.hidden_tag,
                    "fixed_tag": menu.fixed_tag,
                    "show_link": menu.show_link,
                    "show_parent": menu.show_parent,
                    "children": self._build_tree(menus, menu.id)
                }
                tree.append(menu_dict)
        return tree

    def create_menu(self, menu_data: MenuCreate) -> Menu:
        """创建菜单"""
        menu = Menu(
            parent_id=menu_data.parent_id,
            title=menu_data.title,
            name=menu_data.name,
            path=menu_data.path,
            component=menu_data.component,
            menu_type=menu_data.menu_type,
            rank=menu_data.rank,
            redirect=menu_data.redirect,
            icon=menu_data.icon,
            extra_icon=menu_data.extra_icon,
            enter_transition=menu_data.enter_transition,
            leave_transition=menu_data.leave_transition,
            active_path=menu_data.active_path,
            auths=menu_data.auths,
            frame_src=menu_data.frame_src,
            frame_loading=menu_data.frame_loading,
            keep_alive=menu_data.keep_alive,
            hidden_tag=menu_data.hidden_tag,
            fixed_tag=menu_data.fixed_tag,
            show_link=menu_data.show_link,
            show_parent=menu_data.show_parent
        )
        
        self.db.add(menu)
        self.db.commit()
        self.db.refresh(menu)
        return menu

    def update_menu(self, menu_id: int, menu_data: MenuUpdate) -> Menu:
        """更新菜单"""
        menu = self.get_menu_by_id(menu_id)
        if not menu:
            raise ValueError("Menu not found")
        
        # 更新菜单信息
        update_data = menu_data.dict(exclude_unset=True)
        for key, value in update_data.items():
            if hasattr(menu, key):
                setattr(menu, key, value)
        
        self.db.commit()
        self.db.refresh(menu)
        return menu

    def delete_menu(self, menu_id: int) -> bool:
        """删除菜单"""
        menu = self.get_menu_by_id(menu_id)
        if not menu:
            return False
        
        # 删除角色菜单关联
        self.db.query(RoleMenu).filter(RoleMenu.menu_id == menu_id).delete()
        
        # 删除菜单
        self.db.delete(menu)
        self.db.commit()
        return True

    def has_children(self, menu_id: int) -> bool:
        """检查菜单是否有子菜单"""
        count = self.db.query(Menu).filter(Menu.parent_id == menu_id).count()
        return count > 0

    def check_menu_in_use(self, menu_id: int) -> bool:
        """检查菜单是否被角色使用"""
        count = self.db.query(RoleMenu).filter(RoleMenu.menu_id == menu_id).count()
        return count > 0