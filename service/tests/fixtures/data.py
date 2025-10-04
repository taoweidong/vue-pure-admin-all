"""
测试数据fixtures
"""
import pytest


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