"""
用户领域实体
"""
from sqlalchemy import Column, String, DateTime, Boolean, Text, ForeignKey, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.infrastructure.database.database import Base
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from app.domain.organization.entities.department import Department
    from app.domain.role.entities.role import Role

class User(Base):
    """用户实体"""
    __tablename__ = "system_userinfo"

    id = Column(String(32), primary_key=True, comment="用户ID")
    password = Column(String(128), nullable=False, comment="密码")
    last_login = Column(DateTime(timezone=True), nullable=True, comment="最后登录时间")
    is_superuser = Column(Boolean, default=False, comment="是否超级用户")
    username = Column(String(150), unique=True, index=True, nullable=False, comment="用户名")
    first_name = Column(String(150), nullable=False, comment="名")
    last_name = Column(String(150), nullable=False, comment="姓")
    is_staff = Column(Boolean, default=False, comment="是否员工")
    is_active = Column(Boolean, default=True, comment="是否激活")
    date_joined = Column(DateTime(timezone=True), nullable=False, comment="加入日期")
    mode_type = Column(Integer, nullable=False, comment="模式类型")
    created_time = Column(DateTime(timezone=True), nullable=False, comment="创建时间")
    updated_time = Column(DateTime(timezone=True), nullable=False, comment="更新时间")
    description = Column(Text, nullable=True, comment="描述")
    avatar = Column(String(100), nullable=True, comment="头像")
    nickname = Column(String(150), nullable=False, comment="昵称")
    gender = Column(Integer, nullable=False, comment="性别")
    phone = Column(String(16), index=True, nullable=False, comment="电话")
    email = Column(String(254), index=True, nullable=False, comment="邮箱")
    creator_id = Column(String(32), ForeignKey("system_userinfo.id"), nullable=True, comment="创建者ID")
    modifier_id = Column(String(32), ForeignKey("system_userinfo.id"), nullable=True, comment="修改者ID")
    dept_id = Column(String(32), ForeignKey("system_deptinfo.id"), nullable=True, comment="部门ID")
    dept_belong_id = Column(String(32), ForeignKey("system_deptinfo.id"), nullable=True, comment="所属部门ID")

    # 关系
    dept = relationship("Department", foreign_keys=[dept_id], back_populates="users")
    roles = relationship("UserRole", back_populates="user")
    creator = relationship("User", foreign_keys=[creator_id], remote_side=[id])
    modifier = relationship("User", foreign_keys=[modifier_id], remote_side=[id])
    login_logs = relationship("LoginLog", back_populates="user")
    operation_logs = relationship("OperationLog", back_populates="user")


class UserRole(Base):
    """用户角色关联表"""
    __tablename__ = "system_userinfo_roles"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    userinfo_id = Column(String(32), ForeignKey("system_userinfo.id"), nullable=False, comment="用户ID")
    userrole_id = Column(String(32), ForeignKey("system_userrole.id"), nullable=False, comment="角色ID")

    # 关系
    user = relationship("User", back_populates="roles")
    role = relationship("Role", back_populates="users")


class UserSession(Base):
    """用户会话表"""
    __tablename__ = "user_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(32), ForeignKey("system_userinfo.id"), nullable=False, comment="用户ID")
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
    user_id = Column(String(32), ForeignKey("system_userinfo.id"), unique=True, nullable=False, comment="用户ID")
    real_name = Column(String(50), nullable=True, comment="真实姓名")
    id_card = Column(String(20), nullable=True, comment="身份证号")
    birthday = Column(DateTime, nullable=True, comment="生日")
    address = Column(String(255), nullable=True, comment="地址")
    emergency_contact = Column(String(50), nullable=True, comment="紧急联系人")
    emergency_phone = Column(String(20), nullable=True, comment="紧急联系电话")
    job_title = Column(String(100), nullable=True, comment="职位")
    entry_date = Column(DateTime, nullable=True, comment="入职日期")
    work_location = Column(String(255), nullable=True, comment="工作地点")
    supervisor_id = Column(String(32), ForeignKey("system_userinfo.id"), nullable=True, comment="直属上级")
    preferences = Column(Text, nullable=True, comment="用户偏好设置，JSON格式")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新时间")

    # 关系
    user = relationship("User", foreign_keys=[user_id])
    supervisor = relationship("User", foreign_keys=[supervisor_id])