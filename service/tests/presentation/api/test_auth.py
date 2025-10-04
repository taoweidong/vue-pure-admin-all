import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from tests.utils.test_utils import BaseTestCase, create_test_user


class TestAuthAPI(BaseTestCase):
    """认证API测试类"""
    
    base_url = "/api/v1/auth"
    
    def test_login_success(self, client: TestClient, db_session: Session):
        """测试成功登录"""
        # 创建测试用户
        user = create_test_user(db_session, username="auth_user", 
                               password_hash="$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p02e4JMMC1NPDWQr5w3Pz2dC")  # secret
        
        response = client.post(f"{self.base_url}/login", json={
            "username": "auth_user",
            "password": "secret"
        })
        
        data = self.assert_response_success(response)
        assert "data" in data
        assert "accessToken" in data["data"]
        assert "refreshToken" in data["data"]
    
    def test_login_invalid_credentials(self, client: TestClient, db_session: Session):
        """测试无效凭据登录"""
        create_test_user(db_session, username="auth_user")
        
        response = client.post(f"{self.base_url}/login", json={
            "username": "auth_user",
            "password": "wrong_password"
        })
        
        self.assert_response_error(response, 400)
    
    def test_login_nonexistent_user(self, client: TestClient):
        """测试不存在的用户登录"""
        response = client.post(f"{self.base_url}/login", json={
            "username": "nonexistent",
            "password": "password"
        })
        
        self.assert_response_error(response, 400)
    
    def test_get_current_user_info(self, client: TestClient, admin_token: str):
        """测试获取当前用户信息"""
        headers = self.create_test_headers(admin_token)
        response = client.get(f"{self.base_url}/me", headers=headers)
        
        data = self.assert_response_success(response)
        assert "data" in data
        assert "username" in data["data"]
        assert "nickname" in data["data"]
    
    def test_get_current_user_info_unauthorized(self, client: TestClient):
        """测试未授权获取用户信息"""
        response = client.get(f"{self.base_url}/me")
        assert response.status_code == 403
    
    def test_logout(self, client: TestClient, admin_token: str):
        """测试用户登出"""
        headers = self.create_test_headers(admin_token)
        response = client.post(f"{self.base_url}/logout", headers=headers)
        
        self.assert_response_success(response)