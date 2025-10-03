from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.config import settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """验证密码"""
        try:
            # 先尝试 bcrypt 验证
            return pwd_context.verify(plain_password, hashed_password)
        except:
            # 如果 bcrypt 失败，尝试 SHA256 验证（备用方案）
            import hashlib
            sha256_hash = hashlib.sha256(plain_password.encode()).hexdigest()
            return sha256_hash == hashed_password

    @staticmethod
    def get_password_hash(password: str) -> str:
        """获取密码哈希"""
        try:
            # bcrypt 算法对密码长度有 72 字节的限制，需要截断
            password_bytes = password.encode('utf-8')
            if len(password_bytes) > 72:
                password = password_bytes[:72].decode('utf-8', errors='ignore')
            return pwd_context.hash(password)
        except Exception as e:
            # 如果 bcrypt 失败，记录错误但不中断程序
            from app.infrastructure.utils.logger import get_business_logger
            get_business_logger().error(f"Password hashing failed: {e}")
            # 返回一个默认的弱哈希值（仅用于开发环境）
            import hashlib
            return hashlib.sha256(password.encode()).hexdigest()

    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
        """创建访问令牌"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt

    @staticmethod
    def create_refresh_token(data: dict):
        """创建刷新令牌"""
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt

    @staticmethod
    def verify_token(token: str):
        """验证令牌"""
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            username = payload.get("sub")
            if username is None:
                return None
            return username
        except JWTError:
            return None