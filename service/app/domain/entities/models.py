from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.infrastructure.database.database import Base


class User(Base):
    """用户实体"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False, comment="用户名")
    nickname = Column(String(50), nullable=False, comment="昵称")
    email = Column(String(100), unique=True, index=True, nullable=True, comment="邮箱")
    phone = Column(String(20), unique=True, index=True, nullable=True, comment="手机号")
    avatar = Column(String(255), nullable=True, comment="头像")
    password_hash = Column(String(255), nullable=False, comment="密码哈希")
    description = Column(Text, nullable=True, comment="简介")
    sex = Column(Integer, default=0, comment="性别 0-未知 1-男 2-女")
    status = Column(Integer, default=1, comment="状态 1-启用 0-禁用")
    dept_id = Column(Integer, ForeignKey("departments.id"), nullable=True, comment="部门ID")
    remark = Column(Text, nullable=True, comment="备注")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新时间")

    # 关系
    dept = relationship("Department", back_populates="users")
    user_roles = relationship("UserRole", back_populates="user")
    login_logs = relationship("LoginLog", back_populates="user")
    operation_logs = relationship("OperationLog", back_populates="user")


class Role(Base):
    """角色实体"""
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False, comment="角色名称")
    code = Column(String(50), unique=True, nullable=False, comment="角色编码")
    status = Column(Integer, default=1, comment="状态 1-启用 0-禁用")
    remark = Column(Text, nullable=True, comment="备注")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新时间")

    # 关系
    user_roles = relationship("UserRole", back_populates="role")
    role_menus = relationship("RoleMenu", back_populates="role")


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
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新时间")

    # 关系
    children = relationship("Menu", backref="parent", remote_side=[id])
    role_menus = relationship("RoleMenu", back_populates="menu")


class Department(Base):
    """部门实体"""
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True)
    parent_id = Column(Integer, ForeignKey("departments.id"), default=0, comment="父部门ID")
    name = Column(String(100), nullable=False, comment="部门名称")
    code = Column(String(50), unique=True, nullable=False, comment="部门编码")
    leader = Column(String(50), nullable=True, comment="负责人")
    phone = Column(String(20), nullable=True, comment="联系电话")
    email = Column(String(100), nullable=True, comment="邮箱")
    status = Column(Integer, default=1, comment="状态 1-启用 0-禁用")
    sort = Column(Integer, default=0, comment="排序")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新时间")

    # 关系
    children = relationship("Department", backref="parent", remote_side=[id])
    users = relationship("User", back_populates="dept")


class UserRole(Base):
    """用户角色关联表"""
    __tablename__ = "user_roles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, comment="用户ID")
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False, comment="角色ID")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")

    # 关系
    user = relationship("User", back_populates="user_roles")
    role = relationship("Role", back_populates="user_roles")


class RoleMenu(Base):
    """角色菜单关联表"""
    __tablename__ = "role_menus"

    id = Column(Integer, primary_key=True, index=True)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False, comment="角色ID")
    menu_id = Column(Integer, ForeignKey("menus.id"), nullable=False, comment="菜单ID")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")

    # 关系
    role = relationship("Role", back_populates="role_menus")
    menu = relationship("Menu", back_populates="role_menus")