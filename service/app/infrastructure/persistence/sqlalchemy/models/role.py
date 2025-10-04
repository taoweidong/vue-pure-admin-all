from sqlalchemy import Column, String, Boolean, Text, ForeignKey, Table, BigInteger, SmallInteger, JSON
from sqlalchemy.orm import relationship
from .base import BaseModel
from .user import user_role_association

# 角色菜单关联表
role_menu_association = Table(
    'system_userrole_menu',
    BaseModel.metadata,
    Column('id', BigInteger, primary_key=True, autoincrement=True),
    Column('userrole_id', String(32), ForeignKey('system_userrole.id')),
    Column('menu_id', String(32), ForeignKey('system_menu.id'))
)

# 部门角色关联表
dept_role_association = Table(
    'system_deptinfo_roles',
    BaseModel.metadata,
    Column('id', BigInteger, primary_key=True, autoincrement=True),
    Column('deptinfo_id', String(32), ForeignKey('system_deptinfo.id')),
    Column('userrole_id', String(32), ForeignKey('system_userrole.id'))
)

# 数据权限菜单关联表
datapermission_menu_association = Table(
    'system_datapermission_menu',
    BaseModel.metadata,
    Column('id', BigInteger, primary_key=True, autoincrement=True),
    Column('datapermission_id', String(32), ForeignKey('system_datapermission.id')),
    Column('menu_id', String(32), ForeignKey('system_menu.id'))
)

# 部门数据权限关联表
dept_rule_association = Table(
    'system_deptinfo_rules',
    BaseModel.metadata,
    Column('id', BigInteger, primary_key=True, autoincrement=True),
    Column('deptinfo_id', String(32), ForeignKey('system_deptinfo.id')),
    Column('datapermission_id', String(32), ForeignKey('system_datapermission.id'))
)


class UserRole(BaseModel):
    """用户角色表"""
    __tablename__ = "system_userrole"
    
    id = Column(String(32), primary_key=True)
    name = Column(String(128), nullable=False, unique=True)
    code = Column(String(128), nullable=False, unique=True)
    is_active = Column(Boolean, nullable=False, default=True)
    
    # 外键关系
    creator_id = Column(BigInteger, ForeignKey('system_userinfo.id'), nullable=True)
    modifier_id = Column(BigInteger, ForeignKey('system_userinfo.id'), nullable=True)
    dept_belong_id = Column(String(32), ForeignKey('system_deptinfo.id'), nullable=True)
    
    # 关系
    creator = relationship("UserInfo", foreign_keys=[creator_id])
    modifier = relationship("UserInfo", foreign_keys=[modifier_id])
    dept_belong = relationship("DeptInfo", foreign_keys=[dept_belong_id])
    
    # 多对多关系
    users = relationship("UserInfo", secondary=user_role_association, back_populates="roles")
    menus = relationship("Menu", secondary=role_menu_association, back_populates="roles")
    departments = relationship("DeptInfo", secondary=dept_role_association, back_populates="roles")
    
    def __repr__(self):
        return f"<UserRole(id={self.id}, name={self.name}, code={self.code})>"


class DataPermission(BaseModel):
    """数据权限表"""
    __tablename__ = "system_datapermission"
    
    id = Column(String(32), primary_key=True)
    mode_type = Column(SmallInteger, nullable=False)
    name = Column(String(255), nullable=False, unique=True)
    rules = Column(JSON, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    
    # 外键关系
    creator_id = Column(BigInteger, ForeignKey('system_userinfo.id'), nullable=True)
    modifier_id = Column(BigInteger, ForeignKey('system_userinfo.id'), nullable=True)
    dept_belong_id = Column(String(32), ForeignKey('system_deptinfo.id'), nullable=True)
    
    # 关系
    creator = relationship("UserInfo", foreign_keys=[creator_id])
    modifier = relationship("UserInfo", foreign_keys=[modifier_id])
    dept_belong = relationship("DeptInfo", foreign_keys=[dept_belong_id])
    
    # 多对多关系
    users = relationship("UserInfo", secondary="system_userinfo_rules", back_populates="rules")
    menus = relationship("Menu", secondary=datapermission_menu_association, back_populates="data_permissions")
    departments = relationship("DeptInfo", secondary=dept_rule_association, back_populates="rules")
    
    def __repr__(self):
        return f"<DataPermission(id={self.id}, name={self.name})>"


class FieldPermission(BaseModel):
    """字段权限表"""
    __tablename__ = "system_fieldpermission"
    
    id = Column(String(128), primary_key=True)
    
    # 外键关系
    creator_id = Column(BigInteger, ForeignKey('system_userinfo.id'), nullable=True)
    modifier_id = Column(BigInteger, ForeignKey('system_userinfo.id'), nullable=True)
    dept_belong_id = Column(String(32), ForeignKey('system_deptinfo.id'), nullable=True)
    menu_id = Column(String(32), ForeignKey('system_menu.id'), nullable=False)
    role_id = Column(String(32), ForeignKey('system_userrole.id'), nullable=False)
    
    # 关系
    creator = relationship("UserInfo", foreign_keys=[creator_id])
    modifier = relationship("UserInfo", foreign_keys=[modifier_id])
    dept_belong = relationship("DeptInfo", foreign_keys=[dept_belong_id])
    menu = relationship("Menu", foreign_keys=[menu_id])
    role = relationship("UserRole", foreign_keys=[role_id])
    
    def __repr__(self):
        return f"<FieldPermission(id={self.id})>"