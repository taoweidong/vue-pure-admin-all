import os
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from contextlib import asynccontextmanager

from loguru import logger
from shared.kernel.config import get_settings
from app.presentation.api import router as api_router
from app.infrastructure.persistence.sqlalchemy.database import create_tables
import uvicorn

settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 确保数据库文件所在目录存在
    try:
        db_path = settings.DATABASE_URL.replace('sqlite:///', '')
        if '/' in db_path:
            db_dir = os.path.dirname(db_path)
            if db_dir:
                Path(str(db_dir)).mkdir(parents=True, exist_ok=True)
    except Exception as e:
        logger.warning(f"数据库目录检查失败: {e}")

    # 启动时创建数据库表
    try:
        await create_tables()
        logger.info("数据库表初始化成功")
    except Exception as e:
        logger.error(f"数据库初始化失败: {e}")

    logger.info(f"🚀 {settings.APP_NAME} v{settings.APP_VERSION} started")
    logger.info(f"📍 Server running on http://{settings.HOST}:{settings.PORT}")
    logger.info(f"📚 API Documentation: http://{settings.HOST}:{settings.PORT}/docs")

    yield  # 应用运行期间

    # 关闭时清理资源
    logger.info("🛑 Application shutting down...")

def create_app() -> FastAPI:
    """创建FastAPI应用"""
    app = FastAPI(
        title=settings.APP_NAME,
        description="基于 FastAPI 的 RBAC 权限管理系统",
        version=settings.APP_VERSION,
        lifespan=lifespan
    )

    # 添加CORS中间件
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # 添加可信主机中间件
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["*"]  # 生产环境应该配置具体的域名
    )

    # 注册 API 路由
    app.include_router(api_router)

    @app.get("/", tags=["根路径"])
    async def root():
        """根路径"""
        return {
            "message": f"Welcome to {settings.APP_NAME}",
            "version": settings.APP_VERSION,
            "docs": "/docs"
        }

    @app.get("/health", tags=["健康检查"])
    async def health_check():
        """健康检查"""
        return {"status": "healthy", "version": settings.APP_VERSION}

    return app

app = create_app()

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info"
    )