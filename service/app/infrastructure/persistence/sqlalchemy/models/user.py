from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, BigInteger, SmallInteger, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .base import BaseModel

# 用户角色关联表
user_role_association = Table(
    'system_userinfo_roles',
    BaseModel.metadata,
    Column('id', BigInteger, primary_key=True, autoincrement=True),
    Column('userinfo_id', BigInteger, ForeignKey('system_userinfo.id')),
    Column('userrole_id', String(32), ForeignKey('system_userrole.id'))
)

# 用户数据权限关联表
user_rule_association = Table(
    'system_userinfo_rules',
    BaseModel.metadata,
    Column('id', BigInteger, primary_key=True, autoincrement=True),
    Column('userinfo_id', BigInteger, ForeignKey('system_userinfo.id')),
    Column('datapermission_id', String(32), ForeignKey('system_datapermission.id'))
)


class UserInfo(BaseModel):
    """用户信息表"""
    __tablename__ = "system_userinfo"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    password = Column(String(128), nullable=False)
    last_login = Column(DateTime, nullable=True)
    is_superuser = Column(Boolean, nullable=False, default=False)
    username = Column(String(150), nullable=False, unique=True, index=True)
    first_name = Column(String(150), nullable=False, default="")
    last_name = Column(String(150), nullable=False, default="")
    is_staff = Column(Boolean, nullable=False, default=False)
    is_active = Column(Boolean, nullable=False, default=True)
    date_joined = Column(DateTime, nullable=False, default=func.now())
    mode_type = Column(SmallInteger, nullable=False, default=0)
    avatar = Column(String(100), nullable=True)
    nickname = Column(String(150), nullable=False, default="")
    gender = Column(Integer, nullable=False, default=0)
    phone = Column(String(16), nullable=False, default="", index=True)
    email = Column(String(254), nullable=False, default="", index=True)
    
    # 外键关系
    creator_id = Column(BigInteger, ForeignKey('system_userinfo.id'), nullable=True)
    modifier_id = Column(BigInteger, ForeignKey('system_userinfo.id'), nullable=True)
    dept_id = Column(String(32), ForeignKey('system_deptinfo.id'), nullable=True)
    dept_belong_id = Column(String(32), ForeignKey('system_deptinfo.id'), nullable=True)
    
    # 关系
    creator = relationship("UserInfo", foreign_keys=[creator_id], remote_side=[id])
    modifier = relationship("UserInfo", foreign_keys=[modifier_id], remote_side=[id])
    dept = relationship("DeptInfo", foreign_keys=[dept_id], back_populates="users")
    dept_belong = relationship("DeptInfo", foreign_keys=[dept_belong_id])
    
    # 多对多关系
    roles = relationship("UserRole", secondary=user_role_association, back_populates="users")
    rules = relationship("DataPermission", secondary=user_rule_association, back_populates="users")
    
    def __repr__(self):
        return f"<UserInfo(id={self.id}, username={self.username})>"


class UserLoginLog(BaseModel):
    """用户登录日志表"""
    __tablename__ = "system_userloginlog"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    status = Column(Boolean, nullable=False)
    ipaddress = Column(String(39), nullable=True)
    browser = Column(String(64), nullable=True)
    system = Column(String(64), nullable=True)
    agent = Column(String(128), nullable=True)
    login_type = Column(SmallInteger, nullable=False, default=0)
    
    # 外键关系
    creator_id = Column(BigInteger, ForeignKey('system_userinfo.id'), nullable=True)
    modifier_id = Column(BigInteger, ForeignKey('system_userinfo.id'), nullable=True)
    dept_belong_id = Column(String(32), ForeignKey('system_deptinfo.id'), nullable=True)
    
    # 关系
    creator = relationship("UserInfo", foreign_keys=[creator_id])
    modifier = relationship("UserInfo", foreign_keys=[modifier_id])
    dept_belong = relationship("DeptInfo", foreign_keys=[dept_belong_id])


class UserPersonalConfig(BaseModel):
    """用户个人配置表"""
    __tablename__ = "system_userpersonalconfig"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    value = Column(Text, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    access = Column(Boolean, nullable=False, default=True)
    key = Column(String(255), nullable=False)
    
    # 外键关系
    creator_id = Column(BigInteger, ForeignKey('system_userinfo.id'), nullable=True)
    modifier_id = Column(BigInteger, ForeignKey('system_userinfo.id'), nullable=True)
    dept_belong_id = Column(String(32), ForeignKey('system_deptinfo.id'), nullable=True)
    owner_id = Column(BigInteger, ForeignKey('system_userinfo.id'), nullable=False)
    
    # 关系
    creator = relationship("UserInfo", foreign_keys=[creator_id])
    modifier = relationship("UserInfo", foreign_keys=[modifier_id])
    dept_belong = relationship("DeptInfo", foreign_keys=[dept_belong_id])
    owner = relationship("UserInfo", foreign_keys=[owner_id])