import pytest
import os
import tempfile
from typing import Generator
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.main import app
from app.infrastructure.database.database import get_db, Base
from app.config import settings


# 创建测试数据库
TEST_DATABASE_URL = "sqlite:///./test.db"
test_engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


def override_get_db() -> Generator[Session, None, None]:
    """覆盖数据库依赖以使用测试数据库"""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture(scope="session")
def db_engine():
    """数据库引擎fixture"""
    Base.metadata.create_all(bind=test_engine)
    yield test_engine
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture(scope="function")
def db_session(db_engine) -> Generator[Session, None, None]:
    """数据库会话fixture"""
    connection = db_engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(db_session: Session) -> Generator[TestClient, None, None]:
    """测试客户端fixture"""
    app.dependency_overrides[get_db] = lambda: db_session
    
    with TestClient(app) as test_client:
        yield test_client
    
    app.dependency_overrides.clear()


@pytest.fixture
def test_user_data():
    """测试用户数据"""
    return {
        "username": "test_user",
        "password": "test_password123",
        "nickname": "测试用户",
        "email": "test@example.com",
        "phone": "13800138000",
        "sex": 1,
        "status": 1,
        "dept_id": None,
        "remark": "测试用户"
    }


@pytest.fixture
def test_role_data():
    """测试角色数据"""
    return {
        "name": "测试角色",
        "code": "test_role",
        "status": 1,
        "remark": "测试角色备注"
    }


@pytest.fixture
def test_menu_data():
    """测试菜单数据"""
    return {
        "parent_id": 0,
        "title": "测试菜单",
        "name": "test_menu",
        "path": "/test",
        "component": "TestComponent",
        "menu_type": 0,
        "rank": 1,
        "icon": "test-icon",
        "show_link": True
    }


@pytest.fixture
def test_dept_data():
    """测试部门数据"""
    return {
        "parent_id": 0,
        "name": "测试部门",
        "code": "test_dept",
        "leader": "测试负责人",
        "phone": "021-12345678",
        "email": "dept@example.com",
        "status": 1,
        "sort": 1
    }


@pytest.fixture
def admin_token(client: TestClient, db_session: Session):
    """获取管理员token"""
    from app.application.services.user_service import UserService
    from app.domain.entities.models import User, Role, UserRole
    from app.infrastructure.utils.auth import AuthService
    
    auth_service = AuthService()
    
    # 创建管理员用户
    admin_user = User(
        username="admin",
        nickname="管理员",
        email="admin@example.com",
        password_hash=auth_service.get_password_hash("admin123"),
        status=1
    )
    db_session.add(admin_user)
    db_session.commit()
    db_session.refresh(admin_user)
    
    # 创建管理员角色
    admin_role = Role(
        name="管理员",
        code="admin",
        status=1
    )
    db_session.add(admin_role)
    db_session.commit()
    db_session.refresh(admin_role)
    
    # 分配角色给用户
    user_role = UserRole(user_id=admin_user.id, role_id=admin_role.id)
    db_session.add(user_role)
    db_session.commit()
    
    # 登录获取token
    response = client.post("/api/v1/auth/login", json={
        "username": "admin",
        "password": "admin123"
    })
    
    assert response.status_code == 200
    data = response.json()
    return data["data"]["accessToken"]


def pytest_configure(config):
    """pytest配置"""
    # 设置测试环境变量
    os.environ["TESTING"] = "true"


def pytest_unconfigure(config):
    """pytest清理"""
    # 清理测试数据库文件
    if os.path.exists("test.db"):
        os.remove("test.db")