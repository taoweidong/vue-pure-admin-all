from sqlalchemy import Column, String, DateTime, Boolean, Integer, Text
from infrastructure.persistence.sqlalchemy.database import Base
from datetime import datetime
import uuid

class BaseModel(Base):
    """数据库基础模型"""
    __abstract__ = True
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_time = Column(DateTime, default=datetime.now, nullable=False)
    updated_time = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    
    def to_dict(self):
        """转换为字典"""
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }