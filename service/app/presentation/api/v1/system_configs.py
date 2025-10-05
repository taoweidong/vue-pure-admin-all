from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from sqlalchemy.orm import Session
from datetime import datetime

from app.infrastructure.database.database import get_db
from app.domain.audit.entities.log import SystemLog
from app.presentation.api.dependencies import get_current_user
from app.presentation.schemas.common import BaseResponse, PaginatedResponse, PaginationData

router = APIRouter(prefix="/api/v1/system-configs", tags=["系统配置管理"])


@router.get("", response_model=PaginatedResponse)
async def list_system_configs(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页记录数"),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """获取系统配置列表"""
    try:
        # 查询系统配置列表
        query = db.query(SystemLog)
        total = query.count()
        configs = query.offset((page - 1) * page_size).limit(page_size).all()
        
        config_list = []
        for config in configs:
            config_list.append({
                "id": config.id,
                "key": config.key,
                "value": config.value,
                "is_active": config.is_active,
                "access": config.access,
                "inherit": config.inherit,
                "created_time": config.created_time.isoformat() if config.created_time is not None else None,
                "updated_time": config.updated_time.isoformat() if config.updated_time is not None else None
            })
        
        pages = (total + page_size - 1) // page_size
        pagination_data = PaginationData(
            items=config_list,
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


@router.get("/{config_id}", response_model=BaseResponse)
async def get_system_config(
    config_id: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """获取系统配置详情"""
    try:
        config = db.query(SystemLog).filter(SystemLog.id == config_id).first()
        if not config:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="系统配置不存在"
            )
        
        config_detail = {
            "id": config.id,
            "key": config.key,
            "value": config.value,
            "description": config.description,
            "is_active": config.is_active,
            "access": config.access,
            "inherit": config.inherit,
            "created_time": config.created_time.isoformat() if config.created_time is not None else None,
            "updated_time": config.updated_time.isoformat() if config.updated_time is not None else None
        }
        
        return BaseResponse(
            success=True,
            data=config_detail
        )
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=str(e))


@router.post("", response_model=BaseResponse, status_code=status.HTTP_201_CREATED)
async def create_system_config(
    config_data: dict,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """创建系统配置"""
    try:
        # 检查配置键是否已存在
        existing_config = db.query(SystemLog).filter(SystemLog.key == config_data.get("key")).first()
        if existing_config:
            raise HTTPException(status_code=409, detail="配置键已存在")
        
        # 创建新配置
        new_config = SystemLog(
            key=config_data.get("key"),
            value=config_data.get("value"),
            description=config_data.get("description", ""),
            is_active=config_data.get("is_active", True),
            access=config_data.get("access", False),
            inherit=config_data.get("inherit", False),
            # 其他必要字段需要根据实际情况设置
        )
        
        db.add(new_config)
        db.commit()
        db.refresh(new_config)
        
        config_detail = {
            "id": new_config.id,
            "key": new_config.key,
            "value": new_config.value,
            "description": new_config.description,
            "is_active": new_config.is_active,
            "access": new_config.access,
            "inherit": new_config.inherit,
            "created_time": new_config.created_time.isoformat() if new_config.created_time is not None else None,
            "updated_time": new_config.updated_time.isoformat() if new_config.updated_time is not None else None
        }
        
        return BaseResponse(
            success=True,
            message="系统配置创建成功",
            data=config_detail
        )
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{config_id}", response_model=BaseResponse)
async def update_system_config(
    config_id: str,
    config_data: dict,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """更新系统配置"""
    try:
        config = db.query(SystemLog).filter(SystemLog.id == config_id).first()
        if not config:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="系统配置不存在"
            )
        
        # 更新配置信息
        for key, value in config_data.items():
            if hasattr(config, key) and key not in ["id", "created_time"]:
                setattr(config, key, value)
        
        db.commit()
        db.refresh(config)
        
        config_detail = {
            "id": config.id,
            "key": config.key,
            "value": config.value,
            "description": config.description,
            "is_active": config.is_active,
            "access": config.access,
            "inherit": config.inherit,
            "created_time": config.created_time.isoformat() if config.created_time is not None else None,
            "updated_time": config.updated_time.isoformat() if config.updated_time is not None else None
        }
        
        return BaseResponse(
            success=True,
            message="系统配置更新成功",
            data=config_detail
        )
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{config_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_system_config(
    config_id: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """删除系统配置"""
    try:
        config = db.query(SystemLog).filter(SystemLog.id == config_id).first()
        if not config:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="系统配置不存在"
            )
        
        db.delete(config)
        db.commit()
        
        return None
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))