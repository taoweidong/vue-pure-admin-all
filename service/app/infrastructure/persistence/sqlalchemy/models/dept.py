from sqlalchemy import Column, String, Boolean, Integer, SmallInteger, ForeignKey, BigInteger
from sqlalchemy.orm import relationship
from .base import BaseModel
from .role import dept_role_association, dept_rule_association


class DeptInfo(BaseModel):
    """部门信息表"""
    __tablename__ = "system_deptinfo"
    
    id = Column(String(32), primary_key=True)
    mode_type = Column(SmallInteger, nullable=False, default=0)
    name = Column(String(128), nullable=False)
    code = Column(String(128), nullable=False, unique=True)
    rank = Column(Integer, nullable=False, default=0)
    auto_bind = Column(Boolean, nullable=False, default=False)
    is_active = Column(Boolean, nullable=False, default=True)
    
    # 外键关系
    creator_id = Column(BigInteger, ForeignKey('system_userinfo.id'), nullable=True)
    modifier_id = Column(BigInteger, ForeignKey('system_userinfo.id'), nullable=True)
    dept_belong_id = Column(String(32), ForeignKey('system_deptinfo.id'), nullable=True)
    parent_id = Column(String(32), ForeignKey('system_deptinfo.id'), nullable=True)
    
    # 关系
    creator = relationship("UserInfo", foreign_keys=[creator_id])
    modifier = relationship("UserInfo", foreign_keys=[modifier_id])
    dept_belong = relationship("DeptInfo", foreign_keys=[dept_belong_id], remote_side=[id])
    parent = relationship("DeptInfo", foreign_keys=[parent_id], remote_side=[id])
    
    # 一对多关系
    users = relationship("UserInfo", foreign_keys="UserInfo.dept_id", back_populates="dept")
    children = relationship("DeptInfo", foreign_keys=[parent_id])
    
    # 多对多关系
    roles = relationship("UserRole", secondary=dept_role_association, back_populates="departments")
    rules = relationship("DataPermission", secondary=dept_rule_association, back_populates="departments")
    
    def __repr__(self):
        return f"<DeptInfo(id={self.id}, name={self.name}, code={self.code})>"