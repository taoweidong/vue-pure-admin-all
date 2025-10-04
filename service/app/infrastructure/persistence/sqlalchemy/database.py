from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from typing import AsyncGenerator
from pathlib import Path
from shared.kernel.config import get_settings
from loguru import logger

# 获取配置
settings = get_settings()

# 数据库基类
Base = declarative_base()

# 确保数据库文件所在目录存在
if settings.DATABASE_URL.startswith('sqlite'):
    db_path = settings.DATABASE_URL.replace('sqlite:///', '')
    if '/' in db_path or '\\' in db_path:
        db_dir = os.path.dirname(db_path)
        if db_dir:
            Path(db_dir).mkdir(parents=True, exist_ok=True)

# 同步引擎（用于创建表）
engine = create_engine(settings.DATABASE_URL, echo=settings.DATABASE_ECHO)

# 异步引擎
if settings.DATABASE_URL.startswith("sqlite"):
    async_database_url = settings.DATABASE_URL.replace("sqlite://", "sqlite+aiosqlite://")
else:
    async_database_url = settings.DATABASE_URL.replace("mysql+pymysql://", "mysql+aiomysql://")

async_engine = create_async_engine(async_database_url, echo=settings.DATABASE_ECHO)

# 会话工厂
AsyncSessionLocal = async_sessionmaker(
    async_engine, class_=AsyncSession, expire_on_commit=False
)

# 同步会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """获取异步数据库会话"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

def get_sync_db():
    """获取同步数据库会话"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def create_tables():
    """创建数据库表（使用SQLAlchemy模型）"""
    try:
        # 导入所有模型以确保它们被注册到Base.metadata中
        from .models import user, role, dept, menu  # 导入所有模型模块
        
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("数据库表创建成功")
    except Exception as e:
        logger.error(f"创建数据库表失败: {e}")
        raise

async def create_tables_from_sql():
    """使用Vue Pure Admin的SQL文件创建表"""
    try:
        from app.infrastructure.database.init_vue_pure_admin import init_vue_pure_admin_database
        init_vue_pure_admin_database()
        logger.info("使用SQL文件创建数据库表成功")
    except Exception as e:
        logger.error(f"使用SQL文件创建数据库表失败: {e}")
        raise