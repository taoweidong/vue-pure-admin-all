from sqlalchemy.orm import Session
from app.application.services.user_service import UserService
from app.infrastructure.utils.auth import AuthService
# from app.infrastructure.database.redis import redis_service  # 暂时禁用Redis
from app.domain.audit.entities.log import LoginLog
from app.domain.entities.online_user import OnlineUser
from datetime import datetime, timedelta
from typing import Dict, Any


class AuthApplicationService:
    def __init__(self, db: Session):
        self.db = db
        self.user_service = UserService(db)
        self.auth_service = AuthService()

    async def login(self, username: str, password: str) -> Dict[str, Any]:
        """用户登录"""
        # 验证用户
        user = self.user_service.get_user_by_username(username)
        if not user:
            raise ValueError("用户名或密码错误")
        
        if not self.user_service.verify_user_password(user, password):
            raise ValueError("用户名或密码错误")
        
        if getattr(user, 'status') == 0:
            raise ValueError("账户已被禁用")
        
        # 获取用户角色和权限
        user_id = getattr(user, 'id')
        roles = self.user_service.get_user_roles(user_id)
        permissions = self.user_service.get_user_permissions(user_id)
        
        # 生成令牌
        token_data = {"sub": getattr(user, 'username'), "user_id": user_id}
        access_token = self.auth_service.create_access_token(token_data)
        refresh_token = self.auth_service.create_refresh_token(token_data)
        
        # 记录登录日志
        login_log = LoginLog(
            user_id=user_id,
            username=getattr(user, 'username'),
            ip="127.0.0.1",  # 这里应该从请求中获取真实IP
            location="本地",
            browser="Chrome",  # 这里应该从请求头中解析
            os="Windows",  # 这里应该从请求头中解析
            status=1,
            message="登录成功"
        )
        self.db.add(login_log)
        
        # 记录在线用户
        online_user = OnlineUser(
            user_id=user_id,
            username=getattr(user, 'username'),
            nickname=getattr(user, 'nickname'),
            token=access_token,
            ip="127.0.0.1",
            location="本地",
            browser="Chrome",
            os="Windows"
        )
        
        # 删除之前的在线记录
        self.db.query(OnlineUser).filter(OnlineUser.user_id == user_id).delete()
        self.db.add(online_user)
        self.db.commit()
        
        # 存储到Redis缓存（暂时禁用）
        # user_cache_key = f"user:{user_id}"
        # await redis_service.set(user_cache_key, {
        #     "id": user_id,
        #     "username": getattr(user, 'username'),
        #     "nickname": getattr(user, 'nickname'),
        #     "roles": roles,
        #     "permissions": permissions
        # }, expire=3600)
        
        return {
            "avatar": getattr(user, 'avatar') or "https://avatars.githubusercontent.com/u/44761321",
            "username": getattr(user, 'username'),
            "nickname": getattr(user, 'nickname'),
            "roles": roles,
            "permissions": permissions,
            "accessToken": access_token,
            "refreshToken": refresh_token,
            "expires": (datetime.now() + timedelta(minutes=30)).strftime("%Y/%m/%d %H:%M:%S")
        }

    async def refresh_token(self, refresh_token: str) -> Dict[str, Any]:
        """刷新访问令牌"""
        username = self.auth_service.verify_token(refresh_token)
        if not username:
            raise ValueError("无效的刷新令牌")
        
        user = self.user_service.get_user_by_username(username)
        if not user or getattr(user, 'status') == 0:
            raise ValueError("用户不存在或已被禁用")
        
        # 生成新的令牌
        user_id = getattr(user, 'id')
        token_data = {"sub": getattr(user, 'username'), "user_id": user_id}
        new_access_token = self.auth_service.create_access_token(token_data)
        new_refresh_token = self.auth_service.create_refresh_token(token_data)
        
        return {
            "accessToken": new_access_token,
            "refreshToken": new_refresh_token,
            "expires": (datetime.now() + timedelta(minutes=30)).strftime("%Y/%m/%d %H:%M:%S")
        }

    async def logout(self, user_id: int, token: str):
        """用户登出"""
        # 删除在线用户记录
        self.db.query(OnlineUser).filter(OnlineUser.user_id == user_id).delete()
        self.db.commit()
        
        # 删除Redis缓存（暂时禁用）
        # user_cache_key = f"user:{user_id}"
        # await redis_service.delete(user_cache_key)
        
        # 将令牌加入黑名单（暂时禁用）
        # blacklist_key = f"blacklist:{token}"
        # await redis_service.set(blacklist_key, "1", expire=1800)  # 30分钟过期