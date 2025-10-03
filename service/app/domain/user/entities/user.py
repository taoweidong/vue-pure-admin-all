"""
用户领域实体
"""
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
    last_login_at = Column(DateTime(timezone=True), nullable=True, comment="最后登录时间")
    last_login_ip = Column(String(45), nullable=True, comment="最后登录IP")
    password_changed_at = Column(DateTime(timezone=True), server_default=func.now(), comment="密码修改时间")
    is_locked = Column(Boolean, default=False, comment="是否锁定")
    lock_reason = Column(String(255), nullable=True, comment="锁定原因")
    failed_login_attempts = Column(Integer, default=0, comment="失败登录尝试次数")
    remark = Column(Text, nullable=True, comment="备注")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新时间")

    # 关系
    dept = relationship("Department", back_populates="users")
    user_roles = relationship("UserRole", back_populates="user", cascade="all, delete-orphan")
    login_logs = relationship("LoginLog", back_populates="user")
    operation_logs = relationship("OperationLog", back_populates="user")
    sessions = relationship("UserSession", back_populates="user", cascade="all, delete-orphan")


class UserRole(Base):
    """用户角色关联表"""
    __tablename__ = "user_roles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, comment="用户ID")
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False, comment="角色ID")
    granted_by = Column(Integer, ForeignKey("users.id"), nullable=True, comment="授权人")
    granted_at = Column(DateTime(timezone=True), server_default=func.now(), comment="授权时间")
    expires_at = Column(DateTime(timezone=True), nullable=True, comment="过期时间")
    is_active = Column(Boolean, default=True, comment="是否激活")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")

    # 关系
    user = relationship("User", back_populates="user_roles", foreign_keys=[user_id])
    role = relationship("Role", back_populates="user_roles")
    granter = relationship("User", foreign_keys=[granted_by])


class UserSession(Base):
    """用户会话表"""
    __tablename__ = "user_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, comment="用户ID")
    session_id = Column(String(255), unique=True, nullable=False, comment="会话ID")
    access_token = Column(Text, nullable=False, comment="访问令牌")
    refresh_token = Column(Text, nullable=True, comment="刷新令牌")
    ip_address = Column(String(45), nullable=True, comment="IP地址")
    user_agent = Column(Text, nullable=True, comment="用户代理")
    device_info = Column(Text, nullable=True, comment="设备信息")
    location = Column(String(255), nullable=True, comment="登录地点")
    is_active = Column(Boolean, default=True, comment="是否激活")
    expires_at = Column(DateTime(timezone=True), nullable=False, comment="过期时间")
    last_activity_at = Column(DateTime(timezone=True), server_default=func.now(), comment="最后活动时间")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")

    # 关系
    user = relationship("User", back_populates="sessions")


class UserProfile(Base):
    """用户个人资料扩展表"""
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False, comment="用户ID")
    real_name = Column(String(50), nullable=True, comment="真实姓名")
    id_card = Column(String(20), nullable=True, comment="身份证号")
    birthday = Column(DateTime, nullable=True, comment="生日")
    address = Column(String(255), nullable=True, comment="地址")
    emergency_contact = Column(String(50), nullable=True, comment="紧急联系人")
    emergency_phone = Column(String(20), nullable=True, comment="紧急联系电话")
    job_title = Column(String(100), nullable=True, comment="职位")
    entry_date = Column(DateTime, nullable=True, comment="入职日期")
    work_location = Column(String(255), nullable=True, comment="工作地点")
    supervisor_id = Column(Integer, ForeignKey("users.id"), nullable=True, comment="直属上级")
    preferences = Column(Text, nullable=True, comment="用户偏好设置，JSON格式")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新时间")

    # 关系
    user = relationship("User", foreign_keys=[user_id])
    supervisor = relationship("User", foreign_keys=[supervisor_id])