"""
部门/组织架构领域实体
"""
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.infrastructure.database.database import Base


class Department(Base):
    """部门实体"""
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True)
    parent_id = Column(Integer, ForeignKey("departments.id"), default=0, comment="父部门ID")
    name = Column(String(100), nullable=False, comment="部门名称")
    code = Column(String(50), unique=True, nullable=False, comment="部门编码")
    full_name = Column(String(255), nullable=True, comment="部门全称")
    type = Column(String(20), default="department", comment="类型 company|department|team|group")
    level = Column(Integer, default=1, comment="层级")
    path = Column(String(500), nullable=True, comment="路径，用/分隔")
    leader_id = Column(Integer, ForeignKey("users.id"), nullable=True, comment="负责人ID")
    leader = Column(String(50), nullable=True, comment="负责人姓名")
    phone = Column(String(20), nullable=True, comment="联系电话")
    email = Column(String(100), nullable=True, comment="邮箱")
    address = Column(String(255), nullable=True, comment="办公地址")
    description = Column(Text, nullable=True, comment="部门描述")
    function_desc = Column(Text, nullable=True, comment="职能描述")
    cost_center = Column(String(50), nullable=True, comment="成本中心")
    budget_limit = Column(Integer, nullable=True, comment="预算限额")
    employee_limit = Column(Integer, nullable=True, comment="人员限制")
    status = Column(Integer, default=1, comment="状态 1-启用 0-禁用")
    sort = Column(Integer, default=0, comment="排序")
    extra_info = Column(JSON, nullable=True, comment="扩展信息")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新时间")

    # 关系
    children = relationship("Department", backref="parent", remote_side=[id])
    users = relationship("User", back_populates="dept", foreign_keys="User.dept_id")
    leader_user = relationship("User", foreign_keys=[leader_id])
    positions = relationship("Position", back_populates="department")


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