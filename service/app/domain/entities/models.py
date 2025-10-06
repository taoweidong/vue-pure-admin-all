"""
测试用户实体模型
"""
from sqlalchemy import Column, String, DateTime, Boolean, Text, Integer
from sqlalchemy.sql import func
from app.infrastructure.database.database import Base


class TestUser(Base):
    """测试用户实体"""
    __tablename__ = "test_user"

    id = Column(String(32), primary_key=True, comment="用户ID")
    username = Column(String(150), unique=True, index=True, nullable=False, comment="用户名")
    nickname = Column(String(150), nullable=False, comment="昵称")
    email = Column(String(254), index=True, nullable=False, comment="邮箱")
    phone = Column(String(16), index=True, nullable=False, comment="电话")
    gender = Column(Integer, nullable=False, comment="性别")
    avatar = Column(String(100), nullable=True, comment="头像")
    description = Column(Text, nullable=True, comment="描述")
    is_active = Column(Boolean, default=True, comment="是否激活")
    created_time = Column(DateTime(timezone=True), nullable=False, comment="创建时间")
    updated_time = Column(DateTime(timezone=True), nullable=False, comment="更新时间")
    creator_id = Column(String(32), nullable=True, comment="创建者ID")
    modifier_id = Column(String(32), nullable=True, comment="修改者ID")