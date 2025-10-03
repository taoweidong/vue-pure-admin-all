"""
日志审计领域实体
"""
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.infrastructure.database.database import Base


class LoginLog(Base):
    """登录日志实体"""
    __tablename__ = "login_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True, comment="用户ID")
    username = Column(String(50), nullable=False, comment="用户名")
    login_type = Column(String(20), default="web", comment="登录类型 web|mobile|api")
    client_type = Column(String(20), nullable=True, comment="客户端类型")
    ip = Column(String(45), nullable=True, comment="IP地址")
    location = Column(String(255), nullable=True, comment="登录地点")
    browser = Column(String(100), nullable=True, comment="浏览器")
    os = Column(String(100), nullable=True, comment="操作系统")
    device = Column(String(100), nullable=True, comment="设备信息")
    user_agent = Column(Text, nullable=True, comment="用户代理")
    status = Column(Integer, default=1, comment="登录状态 1-成功 0-失败")
    failure_reason = Column(String(255), nullable=True, comment="失败原因")
    session_id = Column(String(255), nullable=True, comment="会话ID")
    logout_time = Column(DateTime(timezone=True), nullable=True, comment="登出时间")
    duration = Column(Integer, nullable=True, comment="会话持续时间(秒)")
    login_time = Column(DateTime(timezone=True), server_default=func.now(), comment="登录时间")

    # 关系
    user = relationship("User", back_populates="login_logs")


class OperationLog(Base):
    """操作日志实体"""
    __tablename__ = "operation_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True, comment="用户ID")
    username = Column(String(50), nullable=True, comment="用户名")
    module = Column(String(100), nullable=True, comment="操作模块")
    operation = Column(String(100), nullable=True, comment="操作名称")
    method = Column(String(10), nullable=True, comment="请求方法")
    request_url = Column(String(500), nullable=True, comment="请求URL")
    request_params = Column(Text, nullable=True, comment="请求参数")
    response_data = Column(Text, nullable=True, comment="响应数据")
    business_id = Column(String(100), nullable=True, comment="业务ID")
    business_type = Column(String(50), nullable=True, comment="业务类型")
    ip = Column(String(45), nullable=True, comment="IP地址")
    location = Column(String(255), nullable=True, comment="操作地点")
    browser = Column(String(100), nullable=True, comment="浏览器")
    os = Column(String(100), nullable=True, comment="操作系统")
    user_agent = Column(Text, nullable=True, comment="用户代理")
    status = Column(Integer, default=1, comment="操作状态 1-成功 0-失败")
    error_msg = Column(Text, nullable=True, comment="错误消息")
    execute_time = Column(Integer, nullable=True, comment="执行时间(毫秒)")
    remark = Column(String(500), nullable=True, comment="备注")
    operate_time = Column(DateTime(timezone=True), server_default=func.now(), comment="操作时间")

    # 关系
    user = relationship("User", back_populates="operation_logs")


class SystemLog(Base):
    """系统日志实体"""
    __tablename__ = "system_logs"

    id = Column(Integer, primary_key=True, index=True)
    level = Column(String(20), nullable=False, comment="日志级别 DEBUG|INFO|WARN|ERROR|FATAL")
    category = Column(String(50), nullable=True, comment="日志分类")
    module = Column(String(100), nullable=True, comment="模块名称")
    function = Column(String(100), nullable=True, comment="函数名称")
    message = Column(Text, nullable=False, comment="日志消息")
    detail = Column(Text, nullable=True, comment="详细信息")
    exception = Column(Text, nullable=True, comment="异常信息")
    trace_id = Column(String(100), nullable=True, comment="追踪ID")
    span_id = Column(String(100), nullable=True, comment="跨度ID")
    ip = Column(String(45), nullable=True, comment="IP地址")
    user_agent = Column(String(255), nullable=True, comment="用户代理")
    extra_data = Column(JSON, nullable=True, comment="额外数据")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")


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