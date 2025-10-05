"""
日志审计领域实体
"""
from sqlalchemy import Column, String, DateTime, Boolean, Text, ForeignKey, Integer, BigInteger, SmallInteger
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.infrastructure.database.database import Base
from sqlalchemy.dialects.mysql import JSON


class LoginLog(Base):
    """登录日志实体"""
    __tablename__ = "system_userloginlog"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    created_time = Column(DateTime(timezone=True), nullable=False, comment="创建时间")
    updated_time = Column(DateTime(timezone=True), nullable=False, comment="更新时间")
    description = Column(Text, nullable=True, comment="描述")
    status = Column(Boolean, nullable=False, comment="状态")
    ipaddress = Column(String(39), nullable=True, comment="IP地址")
    browser = Column(String(64), nullable=True, comment="浏览器")
    system = Column(String(64), nullable=True, comment="系统")
    agent = Column(String(128), nullable=True, comment="代理")
    login_type = Column(SmallInteger, nullable=False, comment="登录类型")
    creator_id = Column(String(32), ForeignKey("system_userinfo.id"), nullable=True, comment="创建者ID")
    dept_belong_id = Column(String(32), ForeignKey("system_deptinfo.id"), nullable=True, comment="所属部门ID")
    modifier_id = Column(String(32), ForeignKey("system_userinfo.id"), nullable=True, comment="修改者ID")

    # 关系
    user = relationship("User", back_populates="login_logs")
    creator = relationship("User", foreign_keys=[creator_id], remote_side="User.id")
    modifier = relationship("User", foreign_keys=[modifier_id], remote_side="User.id")


class OperationLog(Base):
    """操作日志实体"""
    __tablename__ = "system_operationlog"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    created_time = Column(DateTime(timezone=True), nullable=False, comment="创建时间")
    updated_time = Column(DateTime(timezone=True), nullable=False, comment="更新时间")
    description = Column(Text, nullable=True, comment="描述")
    module = Column(String(64), nullable=True, comment="模块")
    path = Column(String(400), nullable=True, comment="路径")
    body = Column(Text, nullable=True, comment="请求体")
    method = Column(String(8), nullable=True, comment="方法")
    ipaddress = Column(String(39), nullable=True, comment="IP地址")
    browser = Column(String(64), nullable=True, comment="浏览器")
    system = Column(String(64), nullable=True, comment="系统")
    response_code = Column(Integer, nullable=True, comment="响应码")
    response_result = Column(Text, nullable=True, comment="响应结果")
    status_code = Column(Integer, nullable=True, comment="状态码")
    creator_id = Column(String(32), ForeignKey("system_userinfo.id"), nullable=True, comment="创建者ID")
    dept_belong_id = Column(String(32), ForeignKey("system_deptinfo.id"), nullable=True, comment="所属部门ID")
    modifier_id = Column(String(32), ForeignKey("system_userinfo.id"), nullable=True, comment="修改者ID")

    # 关系
    user = relationship("User", back_populates="operation_logs")
    creator = relationship("User", foreign_keys=[creator_id], remote_side="User.id")
    modifier = relationship("User", foreign_keys=[modifier_id], remote_side="User.id")


class SystemLog(Base):
    """系统日志实体"""
    __tablename__ = "system_systemconfig"

    id = Column(String(32), primary_key=True, comment="系统配置ID")
    created_time = Column(DateTime(timezone=True), nullable=False, comment="创建时间")
    updated_time = Column(DateTime(timezone=True), nullable=False, comment="更新时间")
    description = Column(Text, nullable=True, comment="描述")
    value = Column(Text, nullable=False, comment="值")
    is_active = Column(Boolean, nullable=False, comment="是否激活")
    access = Column(Boolean, nullable=False, comment="访问权限")
    key = Column(String(255), unique=True, nullable=False, comment="键")
    inherit = Column(Boolean, nullable=False, comment="继承")
    creator_id = Column(String(32), ForeignKey("system_userinfo.id"), nullable=True, comment="创建者ID")
    dept_belong_id = Column(String(32), ForeignKey("system_deptinfo.id"), nullable=True, comment="所属部门ID")
    modifier_id = Column(String(32), ForeignKey("system_userinfo.id"), nullable=True, comment="修改者ID")

    # 关系
    creator = relationship("User", foreign_keys=[creator_id], remote_side="User.id")
    modifier = relationship("User", foreign_keys=[modifier_id], remote_side="User.id")


class AuditLog(Base):
    """审计日志实体"""
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True, comment="用户ID")
    username = Column(String(50), nullable=True, comment="用户名")
    event_type = Column(String(50), nullable=False, comment="事件类型")
    resource_type = Column(String(50), nullable=False, comment="资源类型")
    resource_id = Column(String(100), nullable=True, comment="资源ID")
    resource_name = Column(String(255), nullable=True, comment="资源名称")
    action = Column(String(50), nullable=False, comment="操作动作")
    old_values = Column(JSON, nullable=True, comment="操作前的值")
    new_values = Column(JSON, nullable=True, comment="操作后的值")
    result = Column(String(20), default="success", comment="操作结果 success|failure")
    risk_level = Column(String(20), default="low", comment="风险级别 low|medium|high|critical")
    session_id = Column(String(255), nullable=True, comment="会话ID")
    ip = Column(String(45), nullable=True, comment="IP地址")
    user_agent = Column(Text, nullable=True, comment="用户代理")
    remark = Column(String(500), nullable=True, comment="备注")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")

    # 关系
    user = relationship("User")


class SecurityEvent(Base):
    """安全事件实体"""
    __tablename__ = "security_events"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(String(100), unique=True, nullable=False, comment="事件ID")
    event_type = Column(String(50), nullable=False, comment="事件类型")
    severity = Column(String(20), nullable=False, comment="严重级别 low|medium|high|critical")
    title = Column(String(255), nullable=False, comment="事件标题")
    description = Column(Text, nullable=True, comment="事件描述")
    source_ip = Column(String(45), nullable=True, comment="来源IP")
    target_ip = Column(String(45), nullable=True, comment="目标IP")
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True, comment="相关用户ID")
    username = Column(String(50), nullable=True, comment="用户名")
    affected_resource = Column(String(255), nullable=True, comment="受影响资源")
    attack_vector = Column(String(100), nullable=True, comment="攻击向量")
    detection_method = Column(String(100), nullable=True, comment="检测方法")
    status = Column(String(20), default="new", comment="处理状态 new|investigating|resolved|false_positive")
    handled_by = Column(Integer, ForeignKey("users.id"), nullable=True, comment="处理人")
    handled_at = Column(DateTime(timezone=True), nullable=True, comment="处理时间")
    resolution = Column(Text, nullable=True, comment="处理结果")
    raw_data = Column(JSON, nullable=True, comment="原始数据")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新时间")

    # 关系
    user = relationship("User", foreign_keys=[user_id])
    handler = relationship("User", foreign_keys=[handled_by])