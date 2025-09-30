import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root():
    """测试根路径"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Welcome to Vue Pure Admin Service"


def test_health_check():
    """测试健康检查"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


def test_login_success():
    """测试登录成功"""
    response = client.post("/login", json={
        "username": "admin",
        "password": "admin123"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "accessToken" in data["data"]
    assert "refreshToken" in data["data"]


def test_login_failure():
    """测试登录失败"""
    response = client.post("/login", json={
        "username": "admin",
        "password": "wrongpassword"
    })
    assert response.status_code == 400


def test_get_user_info_without_token():
    """测试未携带token获取用户信息"""
    response = client.get("/mine")
    assert response.status_code == 403


def test_get_async_routes_without_token():
    """测试未携带token获取路由"""
    response = client.get("/get-async-routes")
    assert response.status_code == 403


if __name__ == "__main__":
    pytest.main([__file__])