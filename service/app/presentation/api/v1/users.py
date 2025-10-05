from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from sqlalchemy.orm import Session
from datetime import datetime

from app.infrastructure.database.database import get_db
from app.domain.user.entities.user import User
from app.presentation.api.dependencies import get_current_user
from app.presentation.schemas.common import BaseResponse, PaginatedResponse, PaginationData

router = APIRouter(prefix="/api/v1/users", tags=["用户管理"])


@router.get("", response_model=PaginatedResponse)
async def list_users(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页记录数"),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """获取用户列表"""
    try:
        # 查询用户列表
        query = db.query(User)
        total = query.count()
        users = query.offset((page - 1) * page_size).limit(page_size).all()
        
        user_list = []
        for user in users:
            user_list.append({
                "id": user.id,
                "username": user.username,
                "nickname": user.nickname,
                "email": user.email,
                "phone": user.phone,
                "is_active": user.is_active,
                "created_time": user.created_time.isoformat() if user.created_time is not None else None,
                "updated_time": user.updated_time.isoformat() if user.updated_time is not None else None
            })
        
        pages = (total + page_size - 1) // page_size
        pagination_data = PaginationData(
            items=user_list,
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


@router.get("/{user_id}", response_model=BaseResponse)
async def get_user(
    user_id: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """获取用户详情"""
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="用户不存在"
            )
        
        user_detail = {
            "id": user.id,
            "username": user.username,
            "nickname": user.nickname,
            "email": user.email,
            "phone": user.phone,
            "is_active": user.is_active,
            "gender": user.gender,
            "avatar": user.avatar,
            "description": user.description,
            "created_time": user.created_time.isoformat() if user.created_time is not None else None,
            "updated_time": user.updated_time.isoformat() if user.updated_time is not None else None
        }
        
        return BaseResponse(
            success=True,
            data=user_detail
        )
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=str(e))


@router.post("", response_model=BaseResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: dict,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """创建用户"""
    try:
        # 检查用户名是否已存在
        existing_user = db.query(User).filter(User.username == user_data.get("username")).first()
        if existing_user:
            raise HTTPException(status_code=409, detail="用户名已存在")
        
        # 创建新用户
        new_user = User(
            username=user_data.get("username"),
            nickname=user_data.get("nickname", ""),
            email=user_data.get("email", ""),
            phone=user_data.get("phone", ""),
            gender=user_data.get("gender", 0),
            avatar=user_data.get("avatar", ""),
            description=user_data.get("description", ""),
            is_active=user_data.get("is_active", True),
            # 其他必要字段需要根据实际情况设置
        )
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        user_detail = {
            "id": new_user.id,
            "username": new_user.username,
            "nickname": new_user.nickname,
            "email": new_user.email,
            "phone": new_user.phone,
            "is_active": new_user.is_active,
            "gender": new_user.gender,
            "avatar": new_user.avatar,
            "description": new_user.description,
            "created_time": new_user.created_time.isoformat() if new_user.created_time is not None else None,
            "updated_time": new_user.updated_time.isoformat() if new_user.updated_time is not None else None
        }
        
        return BaseResponse(
            success=True,
            message="用户创建成功",
            data=user_detail
        )
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{user_id}", response_model=BaseResponse)
async def update_user(
    user_id: str,
    user_data: dict,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """更新用户"""
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="用户不存在"
            )
        
        # 更新用户信息
        for key, value in user_data.items():
            if hasattr(user, key) and key not in ["id", "created_time"]:
                setattr(user, key, value)
        
        db.commit()
        db.refresh(user)
        
        user_detail = {
            "id": user.id,
            "username": user.username,
            "nickname": user.nickname,
            "email": user.email,
            "phone": user.phone,
            "is_active": user.is_active,
            "gender": user.gender,
            "avatar": user.avatar,
            "description": user.description,
            "created_time": user.created_time.isoformat() if user.created_time is not None else None,
            "updated_time": user.updated_time.isoformat() if user.updated_time is not None else None
        }
        
        return BaseResponse(
            success=True,
            message="用户更新成功",
            data=user_detail
        )
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """删除用户"""
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="用户不存在"
            )
        
        db.delete(user)
        db.commit()
        
        return None
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))