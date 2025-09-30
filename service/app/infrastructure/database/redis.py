"""
Redis服务模块（已禁用）
此模块在Redis被禁用时提供空实现，避免引用错误
"""

import redis.asyncio as aioredis
from app.infrastructure.utils.logger import log_redis_error, get_business_logger
from typing import Optional, Any


class RedisService:
    """
    Redis服务类（已禁用）
    """
    
    def __init__(self):
        self.redis_client = None
        get_business_logger().info("Redis service is disabled")

    async def get_redis_client(self):
        """获取Redis客户端（禁用状态）"""
        log_redis_error("connection", "Redis is disabled")
        return None

    async def get(self, key: str) -> Optional[str]:
        """获取键值（禁用状态）"""
        try:
            log_redis_error("get", "Redis is disabled, returning None")
            return None
        except Exception as e:
            log_redis_error("get", str(e))
            return None

    async def set(self, key: str, value: Any, expire: Optional[int] = None) -> bool:
        """设置键值（禁用状态）"""
        try:
            log_redis_error("set", "Redis is disabled, operation ignored")
            return False
        except Exception as e:
            log_redis_error("set", str(e))
            return False

    async def delete(self, key: str) -> bool:
        """删除键（禁用状态）"""
        try:
            log_redis_error("delete", "Redis is disabled, operation ignored")
            return False
        except Exception as e:
            log_redis_error("delete", str(e))
            return False

    async def exists(self, key: str) -> bool:
        """检查键是否存在（禁用状态）"""
        try:
            log_redis_error("exists", "Redis is disabled, returning False")
            return False
        except Exception as e:
            log_redis_error("exists", str(e))
            return False


# 创建Redis服务实例
redis_service = RedisService()