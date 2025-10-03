"""
组织架构实体模块
"""
from .department import Department, Position, UserPosition, DepartmentHistory

__all__ = [
    "Department",
    "Position",
    "UserPosition",
    "DepartmentHistory"
]