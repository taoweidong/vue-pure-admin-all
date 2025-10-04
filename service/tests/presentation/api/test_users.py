import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from tests.utils.test_utils import BaseTestCase, create_test_user, create_test_role, MockData


class TestUserAPI(BaseTestCase):
    """用户API测试类"""
    
    base_url = "/api/v1/users"
    
    def test_get_users_list(self, client: TestClient, admin_token: str, db_session: Session):
        """测试获取用户列表"""
        # 创建测试用户
        create_test_user(db_session, username="user1", nickname="用户1")
        create_test_user(db_session, username="user2", nickname="用户2")
        
        headers = self.create_test_headers(admin_token)
        response = client.get(self.base_url, headers=headers)
        
        data = self.assert_response_success(response)
        assert "data" in data
        assert "items" in data["data"]
        assert "total" in data["data"]
        assert data["data"]["total"] >= 2  # 至少包含创建的用户
    
    def test_get_users_list_with_pagination(self, client: TestClient, admin_token: str, db_session: Session):
        """测试分页获取用户列表"""
        # 创建多个测试用户
        for i in range(5):
            create_test_user(db_session, username=f"user{i}", nickname=f"用户{i}")
        
        headers = self.create_test_headers(admin_token)
        response = client.get(f"{self.base_url}?page=1&page_size=3", headers=headers)
        
        data = self.assert_response_success(response)
        assert data["data"]["page"] == 1
        assert data["data"]["page_size"] == 3
        assert len(data["data"]["items"]) <= 3
    
    def test_get_users_list_with_filters(self, client: TestClient, admin_token: str, db_session: Session):
        """测试带过滤条件的用户列表"""
        create_test_user(db_session, username="search_user", nickname="搜索用户")
        
        headers = self.create_test_headers(admin_token)
        response = client.get(f"{self.base_url}?username=search", headers=headers)
        
        data = self.assert_response_success(response)
        items = data["data"]["items"]
        assert len(items) >= 1
        assert any("search" in item["username"] for item in items)
    
    def test_create_user_success(self, client: TestClient, admin_token: str):
        """测试成功创建用户"""
        headers = self.create_test_headers(admin_token)
        user_data = MockData.user_create_data()
        
        response = client.post(self.base_url, json=user_data, headers=headers)
        
        data = self.assert_response_success(response, 201)
        assert "data" in data
        assert data["data"]["username"] == user_data["username"]
        assert data["data"]["nickname"] == user_data["nickname"]
        assert data["data"]["email"] == user_data["email"]
    
    def test_create_user_duplicate_username(self, client: TestClient, admin_token: str, db_session: Session):
        """测试创建重复用户名的用户"""
        # 先创建一个用户
        create_test_user(db_session, username="duplicate_user")
        
        headers = self.create_test_headers(admin_token)
        user_data = MockData.user_create_data(username="duplicate_user")
        
        response = client.post(self.base_url, json=user_data, headers=headers)
        
        self.assert_response_error(response, 409)
    
    def test_create_user_invalid_data(self, client: TestClient, admin_token: str):
        """测试创建用户时提供无效数据"""
        headers = self.create_test_headers(admin_token)
        invalid_data = {"username": ""}  # 缺少必要字段
        
        response = client.post(self.base_url, json=invalid_data, headers=headers)
        
        self.assert_response_error(response, 422)
    
    def test_get_user_detail(self, client: TestClient, admin_token: str, db_session: Session):
        """测试获取用户详情"""
        user = create_test_user(db_session, username="detail_user", nickname="详情用户")
        
        headers = self.create_test_headers(admin_token)
        response = client.get(f"{self.base_url}/{user.id}", headers=headers)
        
        data = self.assert_response_success(response)
        assert data["data"]["id"] == user.id
        assert data["data"]["username"] == user.username
        assert data["data"]["nickname"] == user.nickname
    
    def test_get_user_detail_not_found(self, client: TestClient, admin_token: str):
        """测试获取不存在的用户详情"""
        headers = self.create_test_headers(admin_token)
        response = client.get(f"{self.base_url}/99999", headers=headers)
        
        self.assert_response_error(response, 404)
    
    def test_update_user_success(self, client: TestClient, admin_token: str, db_session: Session):
        """测试成功更新用户"""
        user = create_test_user(db_session, username="update_user", nickname="更新用户")
        
        headers = self.create_test_headers(admin_token)
        update_data = MockData.user_update_data(nickname="新昵称")
        
        response = client.put(f"{self.base_url}/{user.id}", json=update_data, headers=headers)
        
        data = self.assert_response_success(response)
        assert data["data"]["nickname"] == "新昵称"
    
    def test_update_user_not_found(self, client: TestClient, admin_token: str):
        """测试更新不存在的用户"""
        headers = self.create_test_headers(admin_token)
        update_data = MockData.user_update_data()
        
        response = client.put(f"{self.base_url}/99999", json=update_data, headers=headers)
        
        self.assert_response_error(response, 404)
    
    def test_delete_user_success(self, client: TestClient, admin_token: str, db_session: Session):
        """测试成功删除用户"""
        user = create_test_user(db_session, username="delete_user", nickname="删除用户")
        
        headers = self.create_test_headers(admin_token)
        response = client.delete(f"{self.base_url}/{user.id}", headers=headers)
        
        assert response.status_code == 204
    
    def test_delete_user_not_found(self, client: TestClient, admin_token: str):
        """测试删除不存在的用户"""
        headers = self.create_test_headers(admin_token)
        response = client.delete(f"{self.base_url}/99999", headers=headers)
        
        self.assert_response_error(response, 404)
    
    def test_update_user_status(self, client: TestClient, admin_token: str, db_session: Session):
        """测试更新用户状态"""
        user = create_test_user(db_session, username="status_user", status=1)
        
        headers = self.create_test_headers(admin_token)
        response = client.put(f"{self.base_url}/{user.id}/status", 
                            json={"status": 0}, headers=headers)
        
        self.assert_response_success(response)
    
    def test_reset_user_password(self, client: TestClient, admin_token: str, db_session: Session):
        """测试重置用户密码"""
        user = create_test_user(db_session, username="password_user")
        
        headers = self.create_test_headers(admin_token)
        response = client.put(f"{self.base_url}/{user.id}/password", 
                            json={"password": "new_password123"}, headers=headers)
        
        self.assert_response_success(response)
    
    def test_get_user_roles(self, client: TestClient, admin_token: str, db_session: Session):
        """测试获取用户角色"""
        user = create_test_user(db_session, username="role_user")
        role = create_test_role(db_session, name="用户角色", code="user_role")
        
        # 分配角色给用户
        from app.domain.entities.models import UserRole
        user_role = UserRole(user_id=user.id, role_id=role.id)
        db_session.add(user_role)
        db_session.commit()
        
        headers = self.create_test_headers(admin_token)
        response = client.get(f"{self.base_url}/{user.id}/roles", headers=headers)
        
        data = self.assert_response_success(response)
        assert len(data["data"]) >= 1
        assert any(r["code"] == "user_role" for r in data["data"])
    
    def test_unauthorized_access(self, client: TestClient):
        """测试未授权访问"""
        response = client.get(self.base_url)
        assert response.status_code == 403
    
    def test_invalid_token_access(self, client: TestClient):
        """测试无效token访问"""
        headers = {"Authorization": "Bearer invalid_token"}
        response = client.get(self.base_url, headers=headers)
        assert response.status_code == 401


class TestUserService:
    """用户服务测试类"""
    
    def test_user_service_create_user(self, db_session: Session):
        """测试用户服务创建用户"""
        from app.application.services.user_service import UserService
        from app.presentation.schemas.user import UserCreate
        
        user_service = UserService(db_session)
        user_data = UserCreate(
            username="service_user",
            password="password123",
            nickname="服务用户",
            email="service@example.com"
        )
        
        user = user_service.create_user(user_data)
        
        assert user.id is not None
        assert user.username == "service_user"
        assert user.nickname == "服务用户"
        assert user.email == "service@example.com"
    
    def test_user_service_get_user_by_username(self, db_session: Session):
        """测试通过用户名获取用户"""
        from app.application.services.user_service import UserService
        
        user = create_test_user(db_session, username="find_user")
        user_service = UserService(db_session)
        
        found_user = user_service.get_user_by_username("find_user")
        
        assert found_user is not None
        assert found_user.id == user.id
        assert found_user.username == "find_user"
    
    def test_user_service_get_users_paginated(self, db_session: Session):
        """测试分页获取用户"""
        from app.application.services.user_service import UserService
        
        # 创建多个用户
        for i in range(5):
            create_test_user(db_session, username=f"page_user{i}")
        
        user_service = UserService(db_session)
        users, total = user_service.get_users_paginated(page=1, page_size=3)
        
        assert len(users) <= 3
        assert total >= 5
    
    def test_user_service_verify_password(self, db_session: Session):
        """测试验证用户密码"""
        from app.application.services.user_service import UserService
        from app.infrastructure.utils.auth import AuthService
        
        auth_service = AuthService()
        password_hash = auth_service.get_password_hash("test123")
        user = create_test_user(db_session, username="pwd_user", password_hash=password_hash)
        
        user_service = UserService(db_session)
        
        # 正确密码
        assert user_service.verify_user_password(user, "test123") is True
        
        # 错误密码
        assert user_service.verify_user_password(user, "wrong") is False