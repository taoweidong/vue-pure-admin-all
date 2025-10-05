from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from sqlalchemy.orm import Session
from datetime import datetime

from app.infrastructure.database.database import get_db
from app.domain.audit.entities.log import LoginLog
from app.presentation.api.dependencies import get_current_user
from app.presentation.schemas.common import BaseResponse, PaginatedResponse, PaginationData

router = APIRouter(prefix="/api/v1/login-logs", tags=["登录日志管理"])


@router.get("", response_model=PaginatedResponse)
async def list_login_logs(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页记录数"),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """获取登录日志列表"""
    try:
        # 查询登录日志列表
        query = db.query(LoginLog)
        total = query.count()
        logs = query.offset((page - 1) * page_size).limit(page_size).all()
        
        log_list = []
        for log in logs:
            log_list.append({
                "id": log.id,
                "username": log.username,
                "ip": log.ipaddress,
                "browser": log.browser,
                "system": log.system,
                "status": log.status,
                "login_type": log.login_type,
                "created_time": log.created_time.isoformat() if log.created_time is not None else None,
                "updated_time": log.updated_time.isoformat() if log.updated_time is not None else None
            })
        
        pages = (total + page_size - 1) // page_size
        pagination_data = PaginationData(
            items=log_list,
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


@router.get("/{log_id}", response_model=BaseResponse)
async def get_login_log(
    log_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """获取登录日志详情"""
    try:
        log = db.query(LoginLog).filter(LoginLog.id == log_id).first()
        if not log:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="登录日志不存在"
            )
        
        log_detail = {
            "id": log.id,
            "username": log.username,
            "ip": log.ipaddress,
            "browser": log.browser,
            "system": log.system,
            "agent": log.agent,
            "status": log.status,
            "login_type": log.login_type,
            "failure_reason": log.description,
            "created_time": log.created_time.isoformat() if log.created_time is not None else None,
            "updated_time": log.updated_time.isoformat() if log.updated_time is not None else None
        }
        
        return BaseResponse(
            success=True,
            data=log_detail
        )
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{log_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_login_log(
    log_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """删除登录日志"""
    try:
        log = db.query(LoginLog).filter(LoginLog.id == log_id).first()
        if not log:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="登录日志不存在"
            )
        
        db.delete(log)
        db.commit()
        
        return None
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))