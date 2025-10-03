from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.infrastructure.database.database import get_db
from app.infrastructure.utils.auth import AuthService
from app.presentation.schemas.auth import *
from app.application.services.auth_service import AuthApplicationService
from app.application.services.user_service import UserService

router = APIRouter()
security = HTTPBearer()
auth_service = AuthService()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security), 
    db: Session = Depends(get_db)
):
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


@router.post("/logout")
async def logout(current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    """用户登出"""
    try:
        auth_app_service = AuthApplicationService(db)
        await auth_app_service.logout(current_user.username)
        
        return {
            "success": True,
            "message": "登出成功"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/refresh", response_model=RefreshTokenResponse)
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


@router.get("/me", response_model=UserInfoResponse)
async def get_current_user_info(current_user=Depends(get_current_user)):
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


@router.put("/password")
async def change_password(
    request: ChangePasswordRequest,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """修改密码"""
    try:
        auth_app_service = AuthApplicationService(db)
        await auth_app_service.change_password(
            current_user.username, 
            request.old_password, 
            request.new_password
        )
        
        return {
            "success": True,
            "message": "密码修改成功"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/permissions")
async def get_user_permissions(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取用户权限"""
    try:
        auth_app_service = AuthApplicationService(db)
        permissions = await auth_app_service.get_user_permissions(current_user.id)
        
        return {
            "success": True,
            "data": permissions
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/routes")
async def get_user_routes(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取用户路由"""
    try:
        auth_app_service = AuthApplicationService(db)
        routes = await auth_app_service.get_user_routes(current_user.id)
        
        return {
            "success": True,
            "data": routes
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))