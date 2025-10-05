from sqlalchemy import Column, String, Integer, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.infrastructure.persistence.sqlalchemy.models.base import BaseModel

class MenuModel(BaseModel):
    """菜单数据库模型"""
    __tablename__ = 'menus'
    
    name = Column(String(100), nullable=False)
    path = Column(String(200), nullable=False)
    component = Column(String(200), nullable=True)
    menu_type = Column(Integer, default=1, nullable=False)  # 0: 目录, 1: 菜单, 2: 按钮
    parent_id = Column(String(36), ForeignKey('menus.id'), nullable=True)
    rank = Column(Integer, default=0, nullable=False)
    meta = Column(JSON, default=dict, nullable=False)
    
    # 关系
    parent = relationship("MenuModel", remote_side="MenuModel.id", back_populates="children")
    children = relationship("MenuModel", back_populates="parent")
    roles = relationship("RoleModel", secondary="role_menu_association", back_populates="menus")
    
    def __repr__(self):
        return f"<Menu(id='{self.id}', name='{self.name}', path='{self.path}')>"