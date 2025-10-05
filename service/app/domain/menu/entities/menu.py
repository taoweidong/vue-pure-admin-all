"""菜单领域实体"""
from sqlalchemy import Column, String, DateTime, Boolean, Text, ForeignKey, Integer, SmallInteger
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.infrastructure.database.database import Base
from sqlalchemy.dialects.mysql import JSON


class Menu(Base):
    """菜单实体"""
    __tablename__ = "system_menu"

    id = Column(String(32), primary_key=True, comment="菜单ID")
    created_time = Column(DateTime(timezone=True), nullable=False, comment="创建时间")
    updated_time = Column(DateTime(timezone=True), nullable=False, comment="更新时间")
    description = Column(Text, nullable=True, comment="描述")
    menu_type = Column(SmallInteger, nullable=False, comment="菜单类型")
    name = Column(String(128), unique=True, nullable=False, comment="菜单名称")
    rank = Column(Integer, nullable=False, comment="排序")
    path = Column(String(255), nullable=False, comment="路径")
    component = Column(String(255), nullable=True, comment="组件")
    is_active = Column(Boolean, nullable=False, comment="是否激活")
    method = Column(String(10), nullable=True, comment="方法")
    creator_id = Column(String(32), ForeignKey("system_userinfo.id"), nullable=True, comment="创建者ID")
    dept_belong_id = Column(String(32), ForeignKey("system_deptinfo.id"), nullable=True, comment="所属部门ID")
    modifier_id = Column(String(32), ForeignKey("system_userinfo.id"), nullable=True, comment="修改者ID")
    parent_id = Column(String(32), ForeignKey("system_menu.id"), nullable=True, comment="父菜单ID")
    meta_id = Column(String(32), ForeignKey("system_menumeta.id"), nullable=False, comment="菜单元数据ID")

    # 关系
    parent = relationship("Menu", foreign_keys=[parent_id], remote_side=[id], back_populates="children")
    children = relationship("Menu", foreign_keys=[parent_id], back_populates="parent")
    roles = relationship("RoleMenu", back_populates="menu")
    meta = relationship("MenuMeta", back_populates="menu")
    creator = relationship("User", foreign_keys=[creator_id], remote_side="User.id")
    modifier = relationship("User", foreign_keys=[modifier_id], remote_side="User.id")


class MenuMeta(Base):
    """菜单元数据实体"""
    __tablename__ = "system_menumeta"

    id = Column(String(32), primary_key=True, comment="菜单元数据ID")
    created_time = Column(DateTime(timezone=True), nullable=False, comment="创建时间")
    updated_time = Column(DateTime(timezone=True), nullable=False, comment="更新时间")
    description = Column(Text, nullable=True, comment="描述")
    title = Column(String(255), nullable=True, comment="标题")
    icon = Column(String(255), nullable=True, comment="图标")
    r_svg_name = Column(String(255), nullable=True, comment="SVG名称")
    is_show_menu = Column(Boolean, nullable=False, comment="是否显示菜单")
    is_show_parent = Column(Boolean, nullable=False, comment="是否显示父级")
    is_keepalive = Column(Boolean, nullable=False, comment="是否保持活跃")
    frame_url = Column(String(255), nullable=True, comment="框架URL")
    frame_loading = Column(Boolean, nullable=False, comment="框架加载")
    transition_enter = Column(String(255), nullable=True, comment="进入过渡")
    transition_leave = Column(String(255), nullable=True, comment="离开过渡")
    is_hidden_tag = Column(Boolean, nullable=False, comment="是否隐藏标签")
    fixed_tag = Column(Boolean, nullable=False, comment="固定标签")
    dynamic_level = Column(Integer, nullable=False, comment="动态级别")
    creator_id = Column(String(32), ForeignKey("system_userinfo.id"), nullable=True, comment="创建者ID")
    dept_belong_id = Column(String(32), ForeignKey("system_deptinfo.id"), nullable=True, comment="所属部门ID")
    modifier_id = Column(String(32), ForeignKey("system_userinfo.id"), nullable=True, comment="修改者ID")

    # 关系
    menu = relationship("Menu", back_populates="meta", uselist=False)
    creator = relationship("User", foreign_keys=[creator_id], remote_side="User.id")
    modifier = relationship("User", foreign_keys=[modifier_id], remote_side="User.id")