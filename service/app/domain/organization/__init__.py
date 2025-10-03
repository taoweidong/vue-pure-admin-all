"""
组织架构领域模块
"""
from .entities.department import Department, Position, UserPosition, DepartmentHistory

__all__ = [
    "Department",
    "Position",
    "UserPosition", 
    "DepartmentHistory"
]