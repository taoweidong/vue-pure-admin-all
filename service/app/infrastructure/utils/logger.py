"""
日志配置模块
使用loguru进行统一的日志管理
"""
import sys
import os
from pathlib import Path
from loguru import logger
from app.config import settings


class LoggerConfig:
    """日志配置类"""
    
    def __init__(self):
        self.setup_logger()
    
    def setup_logger(self):
        """配置日志"""
        # 移除默认的处理器
        logger.remove()
        
        # 创建日志目录
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        # 日志格式
        log_format = (
            "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
            "<level>{message}</level>"
        )
        
        # 控制台输出
        if settings.DEBUG:
            logger.add(
                sys.stdout,
                format=log_format,
                level="DEBUG",
                colorize=True,
                backtrace=True,
                diagnose=True,
            )
        else:
            logger.add(
                sys.stdout,
                format=log_format,
                level="INFO",
                colorize=True,
            )
        
        # 文件输出 - 所有日志
        logger.add(
            log_dir / "app.log",
            format=log_format,
            level="DEBUG",
            rotation="10 MB",
            retention="30 days",
            compression="zip",
            encoding="utf-8",
            backtrace=True,
            diagnose=True,
        )
        
        # 文件输出 - 错误日志
        logger.add(
            log_dir / "error.log",
            format=log_format,
            level="ERROR",
            rotation="10 MB",
            retention="30 days",
            compression="zip",
            encoding="utf-8",
            backtrace=True,
            diagnose=True,
        )
        
        # 文件输出 - 访问日志
        logger.add(
            log_dir / "access.log",
            format=log_format,
            level="INFO",
            rotation="10 MB",
            retention="30 days",
            compression="zip",
            encoding="utf-8",
            filter=lambda record: "access" in record["extra"],
        )
        
        # 文件输出 - 业务日志
        logger.add(
            log_dir / "business.log",
            format=log_format,
            level="INFO",
            rotation="10 MB",
            retention="30 days",
            compression="zip",
            encoding="utf-8",
            filter=lambda record: "business" in record["extra"],
        )


# 初始化日志配置
logger_config = LoggerConfig()

# 创建不同用途的日志记录器
def get_logger(name: str = __name__):
    """获取日志记录器"""
    return logger.bind(name=name)

def get_access_logger():
    """获取访问日志记录器"""
    return logger.bind(access=True)

def get_business_logger():
    """获取业务日志记录器"""
    return logger.bind(business=True)

def log_startup(app_name: str, version: str, host: str, port: int):
    """记录应用启动日志"""
    logger.info(f"🚀 {app_name} v{version} started on http://{host}:{port}")
    logger.info(f"🚀 {app_name} v{version} docs address: http://{host}:{port}/docs")

def log_shutdown():
    """记录应用关闭日志"""
    logger.info("👋 Application shutdown")

def log_database_init():
    """记录数据库初始化日志"""
    get_business_logger().info("Database initialization started")

def log_database_success():
    """记录数据库初始化成功日志"""
    get_business_logger().info("Database initialized successfully!")
    get_business_logger().info("Admin user: admin / admin123")
    get_business_logger().info("Common user: common / common123")

def log_sql_execution(sql_file: str):
    """记录SQL文件执行日志"""
    get_business_logger().info(f"Executed SQL file: {sql_file}")

def log_sql_error(sql_file: str, error: str):
    """记录SQL执行错误日志"""
    logger.error(f"Error executing SQL file {sql_file}: {error}")

def log_redis_error(operation: str, error: str):
    """记录Redis操作错误日志"""
    logger.error(f"Redis {operation} error: {error}")

def log_password_update():
    """记录密码更新日志"""
    get_business_logger().info("Updated user passwords with proper hashes")

def log_password_update_error(error: str):
    """记录密码更新错误日志"""
    logger.error(f"Error updating passwords: {error}")

def log_file_not_found(file_path: str):
    """记录文件未找到警告"""
    logger.warning(f"File not found: {file_path}")

def log_database_exists():
    """记录数据库已存在日志"""
    get_business_logger().info("Database already initialized")

def log_database_with_data():
    """记录数据库已有数据日志"""
    get_business_logger().info("Database already initialized with data")