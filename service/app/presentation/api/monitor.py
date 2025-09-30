from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.infrastructure.database.database import get_db
from app.presentation.api.auth import get_current_user
from app.presentation.schemas.user import TableResponse, PageResponse
from app.application.services.system_service import SystemService

router = APIRouter()


@router.post("/online-logs", response_model=TableResponse)
async def get_online_logs(
    request: dict,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取在线用户列表"""
    try:
        system_service = SystemService(db)
        page = request.get("currentPage", 1)
        page_size = request.get("pageSize", 10)
        
        online_users, total = system_service.get_online_logs(page, page_size)
        
        user_list = []
        for online_user in online_users:
            user_list.append({
                "id": online_user.id,
                "username": online_user.username,
                "nickname": online_user.nickname,
                "ip": online_user.ip,
                "location": online_user.location or "未知",
                "browser": online_user.browser or "未知",
                "os": online_user.os or "未知",
                "loginTime": int(online_user.login_time.timestamp() * 1000) if online_user.login_time else None,
                "lastAccessTime": int(online_user.last_access_time.timestamp() * 1000) if online_user.last_access_time else None
            })
        
        return TableResponse(
            success=True,
            data=PageResponse(
                list=user_list,
                total=total,
                pageSize=page_size,
                currentPage=page
            )
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/login-logs", response_model=TableResponse)
async def get_login_logs(
    request: dict,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取登录日志列表"""
    try:
        system_service = SystemService(db)
        page = request.get("currentPage", 1)
        page_size = request.get("pageSize", 10)
        
        logs, total = system_service.get_login_logs(page, page_size)
        
        log_list = []
        for log in logs:
            log_list.append({
                "id": log.id,
                "username": log.username,
                "ip": log.ip,
                "location": log.location or "未知",
                "browser": log.browser or "未知",
                "os": log.os or "未知",
                "status": log.status,
                "message": log.message or "",
                "loginTime": int(log.login_time.timestamp() * 1000) if log.login_time else None
            })
        
        return TableResponse(
            success=True,
            data=PageResponse(
                list=log_list,
                total=total,
                pageSize=page_size,
                currentPage=page
            )
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/operation-logs", response_model=TableResponse)
async def get_operation_logs(
    request: dict,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取操作日志列表"""
    try:
        system_service = SystemService(db)
        page = request.get("currentPage", 1)
        page_size = request.get("pageSize", 10)
        
        logs, total = system_service.get_operation_logs(page, page_size)
        
        log_list = []
        for log in logs:
            log_list.append({
                "id": log.id,
                "username": log.username or "系统",
                "module": log.module or "",
                "summary": log.summary or "",
                "method": log.method or "",
                "requestUrl": log.request_url or "",
                "ip": log.ip or "",
                "location": log.location or "未知",
                "browser": log.browser or "未知",
                "os": log.os or "未知",
                "status": log.status,
                "operateTime": int(log.operate_time.timestamp() * 1000) if log.operate_time else None
            })
        
        return TableResponse(
            success=True,
            data=PageResponse(
                list=log_list,
                total=total,
                pageSize=page_size,
                currentPage=page
            )
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/system-logs", response_model=TableResponse)
async def get_system_logs(
    request: dict,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取系统日志列表"""
    try:
        system_service = SystemService(db)
        page = request.get("currentPage", 1)
        page_size = request.get("pageSize", 10)
        
        logs, total = system_service.get_system_logs(page, page_size)
        
        log_list = []
        for log in logs:
            log_list.append({
                "id": log.id,
                "level": log.level,
                "module": log.module or "",
                "message": log.message,
                "ip": log.ip or "",
                "userAgent": log.user_agent or "",
                "createTime": int(log.created_at.timestamp() * 1000) if log.created_at else None
            })
        
        return TableResponse(
            success=True,
            data=PageResponse(
                list=log_list,
                total=total,
                pageSize=page_size,
                currentPage=page
            )
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/system-logs-detail")
async def get_system_log_detail(
    request: dict,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取系统日志详情"""
    try:
        log_id = request.get("id")
        if not log_id:
            raise HTTPException(status_code=400, detail="id is required")
        
        system_service = SystemService(db)
        log = system_service.get_system_log_detail(log_id)
        
        if not log:
            raise HTTPException(status_code=404, detail="Log not found")
        
        return {
            "success": True,
            "data": {
                "id": log.id,
                "level": log.level,
                "module": log.module or "",
                "message": log.message,
                "detail": log.detail or "",
                "ip": log.ip or "",
                "userAgent": log.user_agent or "",
                "createTime": int(log.created_at.timestamp() * 1000) if log.created_at else None
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))