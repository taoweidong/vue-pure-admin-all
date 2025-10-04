from passlib.context import CryptContext

class PasswordHandler:
    """密码处理器"""
    
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def hash_password(self, password: str) -> str:
        """加密密码"""
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """验证密码"""
        return self.pwd_context.verify(plain_password, hashed_password)

    def generate_password_reset_token(self, email: str) -> str:
        """生成密码重置令牌"""
        # 简化实现，实际应该使用安全的令牌生成
        import hashlib
        import time
        return hashlib.sha256(f"{email}{time.time()}".encode()).hexdigest()[:32]