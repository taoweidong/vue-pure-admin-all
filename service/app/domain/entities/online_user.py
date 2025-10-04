"""
在线用户实体
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.infrastructure.database.database import Base


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

    # 关系
    user = relationship("User", foreign_keys=[user_id])