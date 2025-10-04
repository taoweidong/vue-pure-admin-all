"""
认证相关fixtures
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


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