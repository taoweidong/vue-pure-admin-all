from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from sqlalchemy.orm import Session
from datetime import datetime

from app.infrastructure.database.database import get_db
from app.domain.organization.entities.department import Department
from app.presentation.api.dependencies import get_current_user
from app.presentation.schemas.common import BaseResponse, PaginatedResponse, PaginationData

router = APIRouter(prefix="/api/v1/depts", tags=["部门管理"])


@router.get("", response_model=PaginatedResponse)
async def list_depts(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页记录数"),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """获取部门列表"""
    try:
        # 查询部门列表
        query = db.query(Department)
        total = query.count()
        depts = query.offset((page - 1) * page_size).limit(page_size).all()
        
        dept_list = []
        for dept in depts:
            dept_list.append({
                "id": dept.id,
                "name": dept.name,
                "code": dept.code,
                "rank": dept.rank,
                "is_active": dept.is_active,
                "auto_bind": dept.auto_bind,
                "created_time": dept.created_time.isoformat() if dept.created_time is not None else None,
                "updated_time": dept.updated_time.isoformat() if dept.updated_time is not None else None
            })
        
        pages = (total + page_size - 1) // page_size
        pagination_data = PaginationData(
            items=dept_list,
            total=total,
            page=page,
            page_size=page_size,
            pages=pages
        )
        
        return PaginatedResponse(
            success=True,
            data=pagination_data
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{dept_id}", response_model=BaseResponse)
async def get_dept(
    dept_id: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """获取部门详情"""
    try:
        dept = db.query(Department).filter(Department.id == dept_id).first()
        if not dept:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="部门不存在"
            )
        
        dept_detail = {
            "id": dept.id,
            "name": dept.name,
            "code": dept.code,
            "description": dept.description,
            "rank": dept.rank,
            "is_active": dept.is_active,
            "auto_bind": dept.auto_bind,
            "parent_id": dept.parent_id,
            "created_time": dept.created_time.isoformat() if dept.created_time is not None else None,
            "updated_time": dept.updated_time.isoformat() if dept.updated_time is not None else None
        }
        
        return BaseResponse(
            success=True,
            data=dept_detail
        )
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=str(e))


@router.post("", response_model=BaseResponse, status_code=status.HTTP_201_CREATED)
async def create_dept(
    dept_data: dict,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """创建部门"""
    try:
        # 检查部门编码是否已存在
        existing_dept = db.query(Department).filter(Department.code == dept_data.get("code")).first()
        if existing_dept:
            raise HTTPException(status_code=409, detail="部门编码已存在")
        
        # 创建新部门
        new_dept = Department(
            name=dept_data.get("name"),
            code=dept_data.get("code"),
            description=dept_data.get("description", ""),
            rank=dept_data.get("rank", 0),
            is_active=dept_data.get("is_active", True),
            auto_bind=dept_data.get("auto_bind", False),
            parent_id=dept_data.get("parent_id"),
            # 其他必要字段需要根据实际情况设置
        )
        
        db.add(new_dept)
        db.commit()
        db.refresh(new_dept)
        
        dept_detail = {
            "id": new_dept.id,
            "name": new_dept.name,
            "code": new_dept.code,
            "description": new_dept.description,
            "rank": new_dept.rank,
            "is_active": new_dept.is_active,
            "auto_bind": new_dept.auto_bind,
            "parent_id": new_dept.parent_id,
            "created_time": new_dept.created_time.isoformat() if new_dept.created_time is not None else None,
            "updated_time": new_dept.updated_time.isoformat() if new_dept.updated_time is not None else None
        }
        
        return BaseResponse(
            success=True,
            message="部门创建成功",
            data=dept_detail
        )
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{dept_id}", response_model=BaseResponse)
async def update_dept(
    dept_id: str,
    dept_data: dict,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """更新部门"""
    try:
        dept = db.query(Department).filter(Department.id == dept_id).first()
        if not dept:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="部门不存在"
            )
        
        # 更新部门信息
        for key, value in dept_data.items():
            if hasattr(dept, key) and key not in ["id", "created_time"]:
                setattr(dept, key, value)
        
        db.commit()
        db.refresh(dept)
        
        dept_detail = {
            "id": dept.id,
            "name": dept.name,
            "code": dept.code,
            "description": dept.description,
            "rank": dept.rank,
            "is_active": dept.is_active,
            "auto_bind": dept.auto_bind,
            "parent_id": dept.parent_id,
            "created_time": dept.created_time.isoformat() if dept.created_time is not None else None,
            "updated_time": dept.updated_time.isoformat() if dept.updated_time is not None else None
        }
        
        return BaseResponse(
            success=True,
            message="部门更新成功",
            data=dept_detail
        )
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{dept_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_dept(
    dept_id: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """删除部门"""
    try:
        dept = db.query(Department).filter(Department.id == dept_id).first()
        if not dept:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="部门不存在"
            )
        
        db.delete(dept)
        db.commit()
        
        return None
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))