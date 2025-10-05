from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.application.services.user_service import UserService
from app.application.dto.user_dto import UserLogin
from app.presentation.dto.response_dto import SuccessResponse, TokenResponse
from app.presentation.api.dependencies import get_user_service, get_jwt_handler, get_password_handler
from app.infrastructure.auth.jwt_handler import JWTHandler
from app.infrastructure.auth.password_handler import PasswordHandler
from shared.kernel.exceptions import BusinessException

router = APIRouter(prefix="/api/v1/auth", tags=["认证"])
security = HTTPBearer()

@router.post("/login", response_model=SuccessResponse[TokenResponse])
async def login(
    login_data: UserLogin,
    user_service: UserService = Depends(get_user_service),
    jwt_handler: JWTHandler = Depends(get_jwt_handler),
    password_handler: PasswordHandler = Depends(get_password_handler)
):
    """用户登录"""
    try:
        # 用户认证
        user = await user_service.authenticate_user(login_data.username, login_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="用户名或密码错误"
            )
        
        # 生成令牌
        token_data = {"sub": user.id, "username": user.username}
        access_token = jwt_handler.create_access_token(token_data)
        
        token_response = TokenResponse(
            access_token=access_token,
            token_type="bearer",
            expires_in=jwt_handler.expire_minutes * 60
        )
        
        return SuccessResponse(data=token_response, message="登录成功")
        
    except BusinessException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/logout", response_model=SuccessResponse[None])
async def logout(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """用户登出"""
    # 简化实现，实际应该将令牌加入黑名单
    return SuccessResponse(message="登出成功")

@router.post("/refresh", response_model=SuccessResponse[TokenResponse])
async def refresh_token(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    jwt_handler: JWTHandler = Depends(get_jwt_handler)
):
    """刷新令牌"""
    try:
        # 验证当前令牌
        payload = jwt_handler.verify_token(credentials.credentials)
        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="令牌无效"
            )
        
        # 生成新令牌
        token_data = {"sub": payload["sub"], "username": payload.get("username")}
        access_token = jwt_handler.create_access_token(token_data)
        
        token_response = TokenResponse(
            access_token=access_token,
            token_type="bearer",
            expires_in=jwt_handler.expire_minutes * 60
        )
        
        return SuccessResponse(data=token_response, message="令牌刷新成功")
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="令牌刷新失败"
        )