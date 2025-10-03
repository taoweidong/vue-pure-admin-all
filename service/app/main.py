import os
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from contextlib import asynccontextmanager

from loguru import logger
from app.config import settings
from app.presentation.api import auth, system, monitor, list
from app.presentation.api.v1 import api_v1
from app.infrastructure.database.database import engine, Base
from app.infrastructure.utils.logger import log_startup, log_shutdown
import uvicorn


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

    # 启动事件
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("数据库表初始化成功")
    except Exception as e:
        logger.error(f"数据库初始化失败: {e}")

    log_startup(settings.APP_NAME, settings.APP_VERSION, settings.HOST, settings.PORT)

    yield  # 应用运行期间

    # 关闭事件
    log_shutdown()


def create_app() -> FastAPI:
    """创建FastAPI应用"""
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        debug=settings.DEBUG,
        docs_url="/docs" if settings.DEBUG else None,
        redoc_url="/redoc" if settings.DEBUG else None,
        lifespan=lifespan,  # 使用新的lifespan事件处理器
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

    # 注册路由
    app.include_router(api_v1, tags=["API v1"])
    app.include_router(auth.router, tags=["认证"])
    app.include_router(system.router, tags=["系统管理"])
    app.include_router(monitor.router, tags=["系统监控"])
    app.include_router(list.router, tags=["列表数据"])

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
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info"
    )
