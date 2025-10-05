"""
部门/组织架构领域实体"""
from sqlalchemy import Column, String, DateTime, Boolean, Text, ForeignKey, Integer, SmallInteger
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.infrastructure.database.database import Base
from sqlalchemy.dialects.mysql import JSON


class Department(Base):
    """部门实体"""
    __tablename__ = "system_deptinfo"

    mode_type = Column(SmallInteger, nullable=False, comment="模式类型")
    id = Column(String(32), primary_key=True, comment="部门ID")
    created_time = Column(DateTime(timezone=True), nullable=False, comment="创建时间")
    updated_time = Column(DateTime(timezone=True), nullable=False, comment="更新时间")
    description = Column(Text, nullable=True, comment="描述")
    name = Column(String(128), nullable=False, comment="部门名称")
    code = Column(String(128), unique=True, nullable=False, comment="部门编码")
    rank = Column(Integer, nullable=False, comment="排序")
    auto_bind = Column(Boolean, nullable=False, comment="自动绑定")
    is_active = Column(Boolean, nullable=False, comment="是否激活")
    creator_id = Column(String(32), ForeignKey("system_userinfo.id"), nullable=True, comment="创建者ID")
    dept_belong_id = Column(String(32), ForeignKey("system_deptinfo.id"), nullable=True, comment="所属部门ID")
    modifier_id = Column(String(32), ForeignKey("system_userinfo.id"), nullable=True, comment="修改者ID")
    parent_id = Column(String(32), ForeignKey("system_deptinfo.id"), nullable=True, comment="父部门ID")

    # 关系
    parent = relationship("Department", foreign_keys=[parent_id], remote_side=[id], back_populates="children")
    children = relationship("Department", foreign_keys=[parent_id], back_populates="parent")
    users = relationship("User", foreign_keys="User.dept_id", back_populates="dept")
    creator = relationship("User", foreign_keys=[creator_id], remote_side="User.id")
    modifier = relationship("User", foreign_keys=[modifier_id], remote_side="User.id")


class Position(Base):
    """职位实体"""
    __tablename__ = "positions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, comment="职位名称")
    code = Column(String(50), unique=True, nullable=False, comment="职位编码")
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=False, comment="所属部门ID")
    level = Column(Integer, default=1, comment="职位级别")
    category = Column(String(50), nullable=True, comment="职位类别")
    description = Column(Text, nullable=True, comment="职位描述")
    requirements = Column(Text, nullable=True, comment="任职要求")
    responsibilities = Column(Text, nullable=True, comment="工作职责")
    salary_range = Column(String(100), nullable=True, comment="薪资范围")
    is_leadership = Column(Boolean, default=False, comment="是否管理岗位")
    max_count = Column(Integer, default=1, comment="最大人数")
    current_count = Column(Integer, default=0, comment="当前人数")
    status = Column(Integer, default=1, comment="状态 1-启用 0-禁用")
    sort = Column(Integer, default=0, comment="排序")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新时间")

    # 关系
    department = relationship("Department", back_populates="positions")
    user_positions = relationship("UserPosition", back_populates="position")


class UserPosition(Base):
    """用户职位关联表"""
    __tablename__ = "user_positions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, comment="用户ID")
    position_id = Column(Integer, ForeignKey("positions.id"), nullable=False, comment="职位ID")
    is_primary = Column(Boolean, default=True, comment="是否主要职位")
    start_date = Column(DateTime, nullable=True, comment="开始日期")
    end_date = Column(DateTime, nullable=True, comment="结束日期")
    status = Column(Integer, default=1, comment="状态 1-在职 0-离职")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")

    # 关系
    user = relationship("User")
    position = relationship("Position", back_populates="user_positions")


class DepartmentHistory(Base):
    """部门变更历史"""
    __tablename__ = "department_histories"

    id = Column(Integer, primary_key=True, index=True)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=False, comment="部门ID")
    operation_type = Column(String(20), nullable=False, comment="操作类型 create|update|delete|move")
    old_value = Column(JSON, nullable=True, comment="变更前的值")
    new_value = Column(JSON, nullable=True, comment="变更后的值")
    operator_id = Column(Integer, ForeignKey("users.id"), nullable=False, comment="操作人ID")
    reason = Column(String(255), nullable=True, comment="变更原因")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")

    # 关系
    department = relationship("Department")
    operator = relationship("User")