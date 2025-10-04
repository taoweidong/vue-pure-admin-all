"""应用异常定义"""

class BaseException(Exception):
    """基础异常类"""
    def __init__(self, message: str, code: str = "ERROR"):
        self.message = message
        self.code = code
        super().__init__(message)

class BusinessException(BaseException):
    """业务异常"""
    def __init__(self, message: str):
        super().__init__(message, "BUSINESS_ERROR")

class ValidationException(BaseException):
    """验证异常"""
    def __init__(self, message: str):
        super().__init__(message, "VALIDATION_ERROR")

class NotFoundError(BaseException):
    """资源未找到异常"""
    def __init__(self, message: str = "资源未找到"):
        super().__init__(message, "NOT_FOUND")

class UnauthorizedError(BaseException):
    """未授权异常"""
    def __init__(self, message: str = "未授权访问"):
        super().__init__(message, "UNAUTHORIZED")

class ForbiddenError(BaseException):
    """禁止访问异常"""
    def __init__(self, message: str = "禁止访问"):
        super().__init__(message, "FORBIDDEN")