import pytest
from typing import Dict, Any, Optional
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


class BaseTestCase:
    """基础测试类"""
    
    def setup_method(self):
        """每个测试方法执行前的设置"""
        pass
    
    def teardown_method(self):
        """每个测试方法执行后的清理"""
        pass
    
    def assert_response_success(self, response, expected_status=200):
        """断言响应成功"""
        assert response.status_code == expected_status
        data = response.json()
        assert data.get("success") is True
        return data
    
    def assert_response_error(self, response, expected_status=400):
        """断言响应错误"""
        assert response.status_code == expected_status
        return response.json()
    
    def create_test_headers(self, token: str) -> Dict[str, str]:
        """创建测试请求头"""
        return {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }


class APITestMixin:
    """API测试混入类"""
    
    def test_create_item(self, client: TestClient, token: str, create_data: Dict[str, Any]):
        """通用创建测试"""
        headers = self.create_test_headers(token)
        response = client.post(self.base_url, json=create_data, headers=headers)
        return self.assert_response_success(response, 201)
    
    def test_get_item_list(self, client: TestClient, token: str):
        """通用获取列表测试"""
        headers = self.create_test_headers(token)
        response = client.get(self.base_url, headers=headers)
        return self.assert_response_success(response)
    
    def test_get_item_detail(self, client: TestClient, token: str, item_id: int):
        """通用获取详情测试"""
        headers = self.create_test_headers(token)
        response = client.get(f"{self.base_url}/{item_id}", headers=headers)
        return self.assert_response_success(response)
    
    def test_update_item(self, client: TestClient, token: str, item_id: int, update_data: Dict[str, Any]):
        """通用更新测试"""
        headers = self.create_test_headers(token)
        response = client.put(f"{self.base_url}/{item_id}", json=update_data, headers=headers)
        return self.assert_response_success(response)
    
    def test_delete_item(self, client: TestClient, token: str, item_id: int):
        """通用删除测试"""
        headers = self.create_test_headers(token)
        response = client.delete(f"{self.base_url}/{item_id}", headers=headers)
        assert response.status_code == 204


def create_test_user(db_session: Session, **kwargs) -> Any:
    """创建测试用户"""
    from app.domain.entities.models import User
    from app.infrastructure.utils.auth import AuthService
    
    auth_service = AuthService()
    default_data = {
        "username": "test_user",
        "nickname": "测试用户",
        "email": "test@example.com",
        "password_hash": auth_service.get_password_hash("test123"),
        "status": 1
    }
    default_data.update(kwargs)
    
    user = User(**default_data)
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


def create_test_role(db_session: Session, **kwargs) -> Any:
    """创建测试角色"""
    from app.domain.entities.models import Role
    
    default_data = {
        "name": "测试角色",
        "code": "test_role",
        "status": 1
    }
    default_data.update(kwargs)
    
    role = Role(**default_data)
    db_session.add(role)
    db_session.commit()
    db_session.refresh(role)
    return role


def create_test_menu(db_session: Session, **kwargs) -> Any:
    """创建测试菜单"""
    from app.domain.entities.models import Menu
    
    default_data = {
        "parent_id": 0,
        "title": "测试菜单",
        "name": "test_menu",
        "path": "/test",
        "component": "TestComponent",
        "menu_type": 0,
        "rank": 1,
        "show_link": True,
        "frame_loading": True,
        "keep_alive": False,
        "hidden_tag": False,
        "fixed_tag": False,
        "show_parent": False
    }
    default_data.update(kwargs)
    
    menu = Menu(**default_data)
    db_session.add(menu)
    db_session.commit()
    db_session.refresh(menu)
    return menu


def create_test_department(db_session: Session, **kwargs) -> Any:
    """创建测试部门"""
    from app.domain.entities.models import Department
    
    default_data = {
        "parent_id": 0,
        "name": "测试部门",
        "code": "test_dept",
        "status": 1,
        "sort": 1
    }
    default_data.update(kwargs)
    
    dept = Department(**default_data)
    db_session.add(dept)
    db_session.commit()
    db_session.refresh(dept)
    return dept


class MockData:
    """模拟数据类"""
    
    @staticmethod
    def user_create_data(**kwargs):
        """用户创建数据"""
        data = {
            "username": "new_user",
            "password": "password123",
            "nickname": "新用户",
            "email": "new@example.com",
            "phone": "13900139000",
            "sex": 1,
            "status": 1,
            "remark": "新用户备注"
        }
        data.update(kwargs)
        return data
    
    @staticmethod
    def user_update_data(**kwargs):
        """用户更新数据"""
        data = {
            "nickname": "更新用户",
            "email": "updated@example.com",
            "phone": "13900139001",
            "remark": "更新备注"
        }
        data.update(kwargs)
        return data
    
    @staticmethod
    def role_create_data(**kwargs):
        """角色创建数据"""
        data = {
            "name": "新角色",
            "code": "new_role",
            "status": 1,
            "remark": "新角色备注"
        }
        data.update(kwargs)
        return data
    
    @staticmethod
    def menu_create_data(**kwargs):
        """菜单创建数据"""
        data = {
            "parent_id": 0,
            "title": "新菜单",
            "name": "new_menu",
            "path": "/new",
            "component": "NewComponent",
            "menu_type": 0,
            "rank": 1,
            "icon": "new-icon",
            "show_link": True
        }
        data.update(kwargs)
        return data


class TestUtils:
    """测试工具类"""
    
    @staticmethod
    def compare_datetime_fields(actual, expected, tolerance_seconds=2):
        """比较日期时间字段，允许一定误差"""
        from datetime import datetime, timedelta
        
        if isinstance(actual, int):
            actual = datetime.fromtimestamp(actual / 1000)
        if isinstance(expected, int):
            expected = datetime.fromtimestamp(expected / 1000)
        
        if isinstance(actual, datetime) and isinstance(expected, datetime):
            diff = abs((actual - expected).total_seconds())
            return diff <= tolerance_seconds
        
        return actual == expected
    
    @staticmethod
    def extract_pagination_info(response_data):
        """提取分页信息"""
        data = response_data.get("data", {})
        return {
            "total": data.get("total", 0),
            "page": data.get("page", 1),
            "page_size": data.get("page_size", 10),
            "pages": data.get("pages", 0),
            "items_count": len(data.get("items", []))
        }