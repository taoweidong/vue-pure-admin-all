from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.infrastructure.database.database import get_db
from app.infrastructure.utils.auth import AuthService
from app.presentation.schemas.user import *
from app.application.services.user_service import UserService
from app.application.services.auth_service import AuthApplicationService
from datetime import datetime, timedelta

router = APIRouter()
security = HTTPBearer()
auth_service = AuthService()


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    """获取当前用户"""
    token = credentials.credentials
    username = auth_service.verify_token(token)
    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user_service = UserService(db)
    user = user_service.get_user_by_username(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    """用户登录"""
    try:
        auth_app_service = AuthApplicationService(db)
        result = await auth_app_service.login(request.username, request.password)
        
        return LoginResponse(
            success=True,
            data=result
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/refresh-token", response_model=RefreshTokenResponse)
async def refresh_token(request: RefreshTokenRequest, db: Session = Depends(get_db)):
    """刷新访问令牌"""
    try:
        auth_app_service = AuthApplicationService(db)
        result = await auth_app_service.refresh_token(request.refreshToken)
        
        return RefreshTokenResponse(
            success=True,
            data=result
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/mine", response_model=UserInfoResponse)
async def get_user_info(current_user = Depends(get_current_user)):
    """获取当前用户信息"""
    user_info = UserInfo(
        avatar=current_user.avatar,
        username=current_user.username,
        nickname=current_user.nickname,
        email=current_user.email,
        phone=current_user.phone,
        description=current_user.description
    )
    
    return UserInfoResponse(
        success=True,
        data=user_info
    )


@router.get("/mine-logs", response_model=TableResponse)
async def get_user_logs(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取当前用户安全日志"""
    try:
        user_service = UserService(db)
        logs = user_service.get_user_logs(current_user.id)
        
        # 转换为前端需要的格式
        log_list = []
        for log in logs:
            log_list.append({
                "id": log.id,
                "ip": log.ip,
                "address": log.location or "未知",
                "system": log.os or "未知",
                "browser": log.browser or "未知",
                "summary": "账户登录" if log.status == 1 else "登录失败",
                "operatingTime": int(log.login_time.timestamp() * 1000) if log.login_time else None
            })
        
        return TableResponse(
            success=True,
            data=PageResponse(
                list=log_list,
                total=len(log_list),
                pageSize=10,
                currentPage=1
            )
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))