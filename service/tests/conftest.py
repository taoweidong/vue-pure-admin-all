import pytest
import os
from typing import Generator
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.main import app
from app.infrastructure.database.database import get_db, Base
from app.config import settings

# 导入fixtures
from tests.fixtures.database import *
from tests.fixtures.client import *
from tests.fixtures.data import *
from tests.fixtures.auth import *


def pytest_configure(config):
    """pytest配置"""
    # 设置测试环境变量
    os.environ["TESTING"] = "true"


def pytest_unconfigure(config):
    """pytest清理"""
    # 清理测试数据库文件
    if os.path.exists("test.db"):
        os.remove("test.db")