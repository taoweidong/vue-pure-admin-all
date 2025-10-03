"""
菜单领域实体
"""
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.infrastructure.database.database import Base


class Menu(Base):
    """菜单实体"""
    __tablename__ = "menus"

    id = Column(Integer, primary_key=True, index=True)
    parent_id = Column(Integer, ForeignKey("menus.id"), default=0, comment="父菜单ID")
    title = Column(String(100), nullable=False, comment="菜单标题")
    name = Column(String(100), nullable=True, comment="菜单名称")
    path = Column(String(255), nullable=True, comment="路由路径")
    component = Column(String(255), nullable=True, comment="组件路径")
    menu_type = Column(Integer, default=0, comment="菜单类型 0-菜单 1-iframe 2-外链 3-按钮")
    rank = Column(Integer, nullable=True, comment="排序")
    redirect = Column(String(255), nullable=True, comment="重定向")
    icon = Column(String(100), nullable=True, comment="图标")
    extra_icon = Column(String(100), nullable=True, comment="额外图标")
    enter_transition = Column(String(100), nullable=True, comment="进入动画")
    leave_transition = Column(String(100), nullable=True, comment="离开动画")
    active_path = Column(String(255), nullable=True, comment="激活路径")
    auths = Column(String(255), nullable=True, comment="权限标识")
    frame_src = Column(String(255), nullable=True, comment="iframe地址")
    frame_loading = Column(Boolean, default=True, comment="iframe加载状态")
    keep_alive = Column(Boolean, default=False, comment="缓存页面")
    hidden_tag = Column(Boolean, default=False, comment="隐藏标签")
    fixed_tag = Column(Boolean, default=False, comment="固定标签")
    show_link = Column(Boolean, default=True, comment="显示链接")
    show_parent = Column(Boolean, default=False, comment="显示父级")
    is_external = Column(Boolean, default=False, comment="是否外部链接")
    external_url = Column(String(500), nullable=True, comment="外部链接地址")
    meta = Column(JSON, nullable=True, comment="菜单元数据")
    status = Column(Integer, default=1, comment="状态 1-启用 0-禁用")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新时间")

    # 关系
    children = relationship("Menu", backref="parent", remote_side=[id])
    role_menus = relationship("RoleMenu", back_populates="menu")
    menu_permissions = relationship("MenuPermission", back_populates="menu", cascade="all, delete-orphan")


class MenuPermission(Base):
    """菜单权限关联表"""
    __tablename__ = "menu_permissions"

    id = Column(Integer, primary_key=True, index=True)
    menu_id = Column(Integer, ForeignKey("menus.id"), nullable=False, comment="菜单ID")
    permission_id = Column(Integer, ForeignKey("permissions.id"), nullable=False, comment="权限ID")
    required = Column(Boolean, default=True, comment="是否必需")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")

    # 关系
    menu = relationship("Menu", back_populates="menu_permissions")
    permission = relationship("Permission")


class MenuOperation(Base):
    """菜单操作记录"""
    __tablename__ = "menu_operations"

    id = Column(Integer, primary_key=True, index=True)
    menu_id = Column(Integer, ForeignKey("menus.id"), nullable=False, comment="菜单ID")
    operator_id = Column(Integer, ForeignKey("users.id"), nullable=False, comment="操作人ID")
    operation_type = Column(String(20), nullable=False, comment="操作类型 create|update|delete|sort")
    old_value = Column(JSON, nullable=True, comment="操作前的值")
    new_value = Column(JSON, nullable=True, comment="操作后的值")
    remark = Column(String(255), nullable=True, comment="备注")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")

    # 关系
    menu = relationship("Menu")
    operator = relationship("User")