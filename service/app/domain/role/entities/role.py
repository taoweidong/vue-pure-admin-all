"""
角色领域实体
"""
from sqlalchemy import Column, String, DateTime, Boolean, Text, ForeignKey, Integer, SmallInteger
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.infrastructure.database.database import Base


class Role(Base):
    """角色实体"""
    __tablename__ = "system_userrole"

    id = Column(String(32), primary_key=True, comment="角色ID")
    created_time = Column(DateTime(timezone=True), nullable=False, comment="创建时间")
    updated_time = Column(DateTime(timezone=True), nullable=False, comment="更新时间")
    description = Column(Text, nullable=True, comment="描述")
    name = Column(String(128), unique=True, nullable=False, comment="角色名称")
    code = Column(String(128), unique=True, nullable=False, comment="角色编码")
    is_active = Column(Boolean, nullable=False, comment="是否激活")
    creator_id = Column(String(32), ForeignKey("system_userinfo.id"), nullable=True, comment="创建者ID")
    dept_belong_id = Column(String(32), ForeignKey("system_deptinfo.id"), nullable=True, comment="所属部门ID")
    modifier_id = Column(String(32), ForeignKey("system_userinfo.id"), nullable=True, comment="修改者ID")

    # 关系
    users = relationship("UserRole", back_populates="role")
    menus = relationship("RoleMenu", back_populates="role")
    creator = relationship("User", foreign_keys=[creator_id], remote_side="User.id")
    modifier = relationship("User", foreign_keys=[modifier_id], remote_side="User.id")


class RoleMenu(Base):
    """角色菜单关联表"""
    __tablename__ = "system_userrole_menu"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    userrole_id = Column(String(32), ForeignKey("system_userrole.id"), nullable=False, comment="角色ID")
    menu_id = Column(String(32), ForeignKey("system_menu.id"), nullable=False, comment="菜单ID")

    # 关系
    role = relationship("Role", back_populates="menus")
    menu = relationship("Menu", back_populates="roles")


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


class Permission(Base):
    """权限实体"""
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False, comment="权限名称")
    code = Column(String(100), unique=True, nullable=False, comment="权限编码")
    resource = Column(String(100), nullable=False, comment="资源标识")
    action = Column(String(50), nullable=False, comment="操作类型")
    description = Column(Text, nullable=True, comment="权限描述")
    category = Column(String(50), nullable=True, comment="权限分类")
    status = Column(Integer, default=1, comment="状态 1-启用 0-禁用")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新时间")

    # 关系
    role_permissions = relationship("RolePermission", back_populates="permission")


class RolePermission(Base):
    """角色权限关联表"""
    __tablename__ = "role_permissions"

    id = Column(Integer, primary_key=True, index=True)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False, comment="角色ID")
    permission_id = Column(Integer, ForeignKey("permissions.id"), nullable=False, comment="权限ID")
    granted = Column(Boolean, default=True, comment="是否授权")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")

    # 关系
    role = relationship("Role", back_populates="role_permissions")
    permission = relationship("Permission", back_populates="role_permissions")


class Resource(Base):
    """资源实体"""
    __tablename__ = "resources"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, comment="资源名称")
    code = Column(String(100), unique=True, nullable=False, comment="资源编码")
    type = Column(String(50), nullable=False, comment="资源类型 menu|button|api|data")
    url = Column(String(255), nullable=True, comment="资源URL")
    method = Column(String(20), nullable=True, comment="HTTP方法")
    parent_id = Column(Integer, ForeignKey("resources.id"), default=0, comment="父资源ID")
    description = Column(Text, nullable=True, comment="资源描述")
    status = Column(Integer, default=1, comment="状态 1-启用 0-禁用")
    sort = Column(Integer, default=0, comment="排序")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新时间")

    # 关系
    children = relationship("Resource", backref="parent", remote_side=[id])


class DataScope(Base):
    """数据权限范围"""
    __tablename__ = "data_scopes"

    id = Column(Integer, primary_key=True, index=True)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False, comment="角色ID")
    scope_type = Column(String(50), nullable=False, comment="数据范围类型 all|custom|dept|dept_and_child|self")
    scope_value = Column(Text, nullable=True, comment="范围值，JSON格式")
    resource_type = Column(String(50), nullable=False, comment="资源类型")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")

    # 关系
    role = relationship("Role", back_populates="data_scopes")