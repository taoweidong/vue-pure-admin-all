"""
角色领域实体
"""
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.infrastructure.database.database import Base


class Role(Base):
    """角色实体"""
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False, comment="角色名称")
    code = Column(String(50), unique=True, nullable=False, comment="角色编码")
    type = Column(String(20), default="custom", comment="角色类型 system|custom")
    level = Column(Integer, default=0, comment="角色级别，数字越大级别越高")
    parent_id = Column(Integer, ForeignKey("roles.id"), default=0, comment="父角色ID")
    description = Column(Text, nullable=True, comment="角色描述")
    is_default = Column(Boolean, default=False, comment="是否默认角色")
    max_users = Column(Integer, nullable=True, comment="最大用户数限制")
    status = Column(Integer, default=1, comment="状态 1-启用 0-禁用")
    remark = Column(Text, nullable=True, comment="备注")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新时间")

    # 关系
    children = relationship("Role", backref="parent", remote_side=[id])
    user_roles = relationship("UserRole", back_populates="role")
    role_menus = relationship("RoleMenu", back_populates="role", cascade="all, delete-orphan")
    role_permissions = relationship("RolePermission", back_populates="role", cascade="all, delete-orphan")
    data_scopes = relationship("DataScope", back_populates="role", cascade="all, delete-orphan")


class RoleMenu(Base):
    """角色菜单关联表"""
    __tablename__ = "role_menus"

    id = Column(Integer, primary_key=True, index=True)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False, comment="角色ID")
    menu_id = Column(Integer, ForeignKey("menus.id"), nullable=False, comment="菜单ID")
    granted = Column(Boolean, default=True, comment="是否授权")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")

    # 关系
    role = relationship("Role", back_populates="role_menus")
    menu = relationship("Menu", back_populates="role_menus")


class RoleInheritance(Base):
    """角色继承关系表"""
    __tablename__ = "role_inheritances"

    id = Column(Integer, primary_key=True, index=True)
    parent_role_id = Column(Integer, ForeignKey("roles.id"), nullable=False, comment="父角色ID")
    child_role_id = Column(Integer, ForeignKey("roles.id"), nullable=False, comment="子角色ID")
    inherit_type = Column(String(20), default="full", comment="继承类型 full|partial")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")

    # 关系
    parent_role = relationship("Role", foreign_keys=[parent_role_id])
    child_role = relationship("Role", foreign_keys=[child_role_id])