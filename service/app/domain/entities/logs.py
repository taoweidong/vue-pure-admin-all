from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.infrastructure.database.database import Base


class LoginLog(Base):
    """登录日志实体"""
    __tablename__ = "login_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, comment="用户ID")
    username = Column(String(50), nullable=False, comment="用户名")
    ip = Column(String(45), nullable=True, comment="IP地址")
    location = Column(String(255), nullable=True, comment="登录地点")
    browser = Column(String(100), nullable=True, comment="浏览器")
    os = Column(String(100), nullable=True, comment="操作系统")
    status = Column(Integer, default=1, comment="登录状态 1-成功 0-失败")
    message = Column(String(255), nullable=True, comment="登录消息")
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
    summary = Column(String(255), nullable=True, comment="操作摘要")
    method = Column(String(10), nullable=True, comment="请求方法")
    request_url = Column(String(255), nullable=True, comment="请求URL")
    request_params = Column(Text, nullable=True, comment="请求参数")
    ip = Column(String(45), nullable=True, comment="IP地址")
    location = Column(String(255), nullable=True, comment="操作地点")
    browser = Column(String(100), nullable=True, comment="浏览器")
    os = Column(String(100), nullable=True, comment="操作系统")
    status = Column(Integer, default=1, comment="操作状态 1-成功 0-失败")
    error_msg = Column(Text, nullable=True, comment="错误消息")
    operate_time = Column(DateTime(timezone=True), server_default=func.now(), comment="操作时间")

    # 关系
    user = relationship("User", back_populates="operation_logs")


class SystemLog(Base):
    """系统日志实体"""
    __tablename__ = "system_logs"

    id = Column(Integer, primary_key=True, index=True)
    level = Column(String(20), nullable=False, comment="日志级别")
    module = Column(String(100), nullable=True, comment="模块名称")
    message = Column(Text, nullable=False, comment="日志消息")
    detail = Column(Text, nullable=True, comment="详细信息")
    ip = Column(String(45), nullable=True, comment="IP地址")
    user_agent = Column(String(255), nullable=True, comment="用户代理")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")


class OnlineUser(Base):
    """在线用户实体"""
    __tablename__ = "online_users"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, comment="用户ID")
    username = Column(String(50), nullable=False, comment="用户名")
    nickname = Column(String(50), nullable=False, comment="昵称")
    token = Column(String(255), nullable=False, unique=True, comment="访问令牌")
    ip = Column(String(45), nullable=True, comment="IP地址")
    location = Column(String(255), nullable=True, comment="登录地点")
    browser = Column(String(100), nullable=True, comment="浏览器")
    os = Column(String(100), nullable=True, comment="操作系统")
    login_time = Column(DateTime(timezone=True), server_default=func.now(), comment="登录时间")
    last_access_time = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="最后访问时间")