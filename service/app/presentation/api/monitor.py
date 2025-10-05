from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.infrastructure.database.database import get_db
from app.presentation.api.dependencies import get_current_user
from app.presentation.schemas.user import TableResponse, PageResponse
from app.application.services.system_service import SystemService
from datetime import datetime

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
            login_time = getattr(online_user, 'login_time', None)
            last_access_time = getattr(online_user, 'last_access_time', None)
            
            user_list.append({
                "id": getattr(online_user, 'id', ''),
                "username": getattr(online_user, 'username', ''),
                "nickname": getattr(online_user, 'nickname', ''),
                "ip": getattr(online_user, 'ip', ''),
                "location": getattr(online_user, 'location', None) or "未知",
                "browser": getattr(online_user, 'browser', None) or "未知",
                "os": getattr(online_user, 'os', None) or "未知",
                "loginTime": int(login_time.timestamp() * 1000) if login_time and isinstance(login_time, datetime) else None,
                "lastAccessTime": int(last_access_time.timestamp() * 1000) if last_access_time and isinstance(last_access_time, datetime) else None
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
            login_time = getattr(log, 'login_time', None)
            
            log_list.append({
                "id": getattr(log, 'id', ''),
                "username": getattr(log, 'username', ''),
                "ip": getattr(log, 'ip', ''),
                "location": getattr(log, 'location', None) or "未知",
                "browser": getattr(log, 'browser', None) or "未知",
                "os": getattr(log, 'os', None) or "未知",
                "status": getattr(log, 'status', 0),
                "message": getattr(log, 'message', None) or "",
                "loginTime": int(login_time.timestamp() * 1000) if login_time and isinstance(login_time, datetime) else None
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
            operate_time = getattr(log, 'operate_time', None)
            
            log_list.append({
                "id": getattr(log, 'id', ''),
                "username": getattr(log, 'username', None) or "系统",
                "module": getattr(log, 'module', None) or "",
                "summary": getattr(log, 'summary', None) or "",
                "method": getattr(log, 'method', None) or "",
                "requestUrl": getattr(log, 'request_url', None) or "",
                "ip": getattr(log, 'ip', None) or "",
                "location": getattr(log, 'location', None) or "未知",
                "browser": getattr(log, 'browser', None) or "未知",
                "os": getattr(log, 'os', None) or "未知",
                "status": getattr(log, 'status', 0),
                "operateTime": int(operate_time.timestamp() * 1000) if operate_time and isinstance(operate_time, datetime) else None
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
            created_at = getattr(log, 'created_at', None)
            
            log_list.append({
                "id": getattr(log, 'id', ''),
                "level": getattr(log, 'level', ''),
                "module": getattr(log, 'module', None) or "",
                "message": getattr(log, 'message', ''),
                "ip": getattr(log, 'ip', None) or "",
                "userAgent": getattr(log, 'user_agent', None) or "",
                "createTime": int(created_at.timestamp() * 1000) if created_at and isinstance(created_at, datetime) else None
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
        
        created_at = getattr(log, 'created_at', None)
        
        return {
            "success": True,
            "data": {
                "id": getattr(log, 'id', ''),
                "level": getattr(log, 'level', ''),
                "module": getattr(log, 'module', None) or "",
                "message": getattr(log, 'message', ''),
                "ip": getattr(log, 'ip', None) or "",
                "userAgent": getattr(log, 'user_agent', None) or "",
                "createTime": int(created_at.timestamp() * 1000) if created_at and isinstance(created_at, datetime) else None,
                "details": getattr(log, 'details', None) or ""
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))