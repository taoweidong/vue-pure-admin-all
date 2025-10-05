import os
import sqlite3
from sqlalchemy.orm import Session
from app.infrastructure.database.database import SessionLocal, engine, Base
from app.domain.user.entities.user import User, UserRole, UserSession, UserProfile
from app.domain.role.entities.role import Role, RoleMenu
from app.domain.menu.entities.menu import Menu, MenuMeta
from app.domain.organization.entities.department import Department
from app.domain.audit.entities.log import LoginLog, OperationLog, SystemLog
from app.infrastructure.utils.auth import AuthService
from app.infrastructure.utils.logger import (
    log_file_not_found, log_sql_execution, log_sql_error, log_database_init,
    log_database_success, log_password_update, log_password_update_error,
    log_database_exists, log_database_with_data, get_business_logger
)
from datetime import datetime
import uuid


def execute_sql_file(db_path: str, sql_file_path: str):
    """执行SQL文件"""
    if not os.path.exists(sql_file_path):
        log_file_not_found(sql_file_path)
        return
    
    try:
        with sqlite3.connect(db_path) as conn:
            with open(sql_file_path, 'r', encoding='utf-8') as file:
                sql_content = file.read()
                # 执行多条SQL语句
                conn.executescript(sql_content)
                conn.commit()
        log_sql_execution(sql_file_path)
    except Exception as e:
        log_sql_error(sql_file_path, str(e))
        raise


def ensure_db_directory():
    """确保数据库目录存在"""
    db_dir = os.path.join(os.getcwd(), 'db')
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)
        get_business_logger().info(f"Created database directory: {db_dir}")
    return db_dir


def init_database_with_sql():
    """使用SQL文件初始化数据库"""
    # 确保数据库目录存在
    db_dir = ensure_db_directory()
    db_path = os.path.join(db_dir, 'vue_pure_admin.db')
    
    # 检查是否已经初始化
    if os.path.exists(db_path):
        # 检查数据库是否有数据
        try:
            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM system_userinfo")
                user_count = cursor.fetchone()[0]
                if user_count > 0:
                    log_database_with_data()
                    return
        except sqlite3.OperationalError:
            # 表不存在，需要初始化
            pass
    
    log_database_init()
    
    # SQL文件路径 - 使用适合SQLite的SQL文件
    sql_dir = os.path.join(db_dir, 'init')
    sql_files = [
        '01_create_tables_sqlite.sql',  # 使用适合SQLite的SQL文件
        '02_insert_data.sql', 
        '03_create_indexes.sql'
    ]
    
    # 按顺序执行SQL文件
    for sql_file in sql_files:
        sql_file_path = os.path.join(sql_dir, sql_file)
        execute_sql_file(db_path, sql_file_path)
    
    # 更新用户密码为实际的哈希值
    try:
        auth_service = AuthService()
        
        # 验证密码长度在 bcrypt 限制内
        admin_password = "admin123"
        common_password = "common123"
        
        # 检查密码长度
        if len(admin_password.encode('utf-8')) > 72:
            admin_password = admin_password.encode('utf-8')[:72].decode('utf-8', errors='ignore')
        if len(common_password.encode('utf-8')) > 72:
            common_password = common_password.encode('utf-8')[:72].decode('utf-8', errors='ignore')
            
        admin_hash = auth_service.get_password_hash(admin_password)
        common_hash = auth_service.get_password_hash(common_password)
        
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE system_userinfo SET password = ? WHERE username = 'admin'", (admin_hash,))
            cursor.execute("UPDATE system_userinfo SET password = ? WHERE username = 'common'", (common_hash,))
            conn.commit()
        
        log_password_update()
    except Exception as e:
        log_password_update_error(str(e))
        # 不再抛出异常，让系统继续运行
        get_business_logger().warning(f"Password update failed, but database initialization continues: {e}")
    
    log_database_success()


def init_database():
    """初始化数据库数据（兼容SQLAlchemy方式）"""
    # 优先使用SQL文件初始化（适用于SQLite）
    try:
        from app.config import settings
        if "sqlite" in settings.DATABASE_URL.lower():
            init_database_with_sql()
            return
    except Exception as e:
        get_business_logger().warning(f"SQL file initialization failed, falling back to SQLAlchemy: {e}")
    
    # 如果不是SQLite或SQL文件初始化失败，使用SQLAlchemy方式
    init_database_with_sqlalchemy()


def init_database_with_sqlalchemy():
    """使用SQLAlchemy初始化数据库（适用于MySQL等）"""
    # 创建所有表
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    auth_service = AuthService()
    
    try:
        # 检查是否已经初始化
        if db.query(User).first():
            log_database_with_data()
            return
        
        get_business_logger().info("Initializing database...")
        
        # 创建部门
        dev_dept = Department(
            id=str(uuid.uuid4()).replace('-', ''),
            mode_type=1,
            created_time=datetime.now(),
            updated_time=datetime.now(),
            name="研发部门",
            code="dev",
            rank=1,
            auto_bind=True,
            is_active=True
        )
        
        test_dept = Department(
            id=str(uuid.uuid4()).replace('-', ''),
            mode_type=1,
            created_time=datetime.now(),
            updated_time=datetime.now(),
            name="测试部门",
            code="test",
            rank=2,
            auto_bind=True,
            is_active=True
        )
        
        db.add(dev_dept)
        db.add(test_dept)
        db.flush()
        
        # 创建角色
        admin_role = Role(
            id=str(uuid.uuid4()).replace('-', ''),
            created_time=datetime.now(),
            updated_time=datetime.now(),
            name="超级管理员",
            code="admin",
            is_active=True,
            description="超级管理员拥有最高权限"
        )
        
        common_role = Role(
            id=str(uuid.uuid4()).replace('-', ''),
            created_time=datetime.now(),
            updated_time=datetime.now(),
            name="普通角色",
            code="common",
            is_active=True,
            description="普通角色拥有部分权限"
        )
        
        db.add(admin_role)
        db.add(common_role)
        db.flush()
        
        # 创建用户
        admin_user = User(
            id=str(uuid.uuid4()).replace('-', ''),
            password=auth_service.get_password_hash("admin123"),
            last_login=None,
            is_superuser=True,
            username="admin",
            first_name="",
            last_name="",
            is_staff=True,
            is_active=True,
            date_joined=datetime.now(),
            mode_type=1,
            created_time=datetime.now(),
            updated_time=datetime.now(),
            nickname="小铭",
            gender=1,
            phone="15888886789",
            email="admin@example.com",
            avatar="https://avatars.githubusercontent.com/u/44761321",
            description="系统管理员"
        )
        
        common_user = User(
            id=str(uuid.uuid4()).replace('-', ''),
            password=auth_service.get_password_hash("common123"),
            last_login=None,
            is_superuser=False,
            username="common",
            first_name="",
            last_name="",
            is_staff=True,
            is_active=True,
            date_joined=datetime.now(),
            mode_type=1,
            created_time=datetime.now(),
            updated_time=datetime.now(),
            nickname="小林",
            gender=2,
            phone="18288882345",
            email="common@example.com",
            avatar="https://avatars.githubusercontent.com/u/52823142",
            description="普通用户"
        )
        
        db.add(admin_user)
        db.add(common_user)
        db.flush()
        
        # 创建用户角色关联
        admin_user_role = UserRole(
            userinfo_id=admin_user.id,
            userrole_id=admin_role.id
        )
        
        common_user_role = UserRole(
            userinfo_id=common_user.id,
            userrole_id=common_role.id
        )
        
        db.add(admin_user_role)
        db.add(common_user_role)
        
        # 创建菜单元数据
        menu_meta = MenuMeta(
            id=str(uuid.uuid4()).replace('-', ''),
            created_time=datetime.now(),
            updated_time=datetime.now(),
            title="系统管理",
            icon="ri:settings-3-line",
            is_show_menu=True,
            is_show_parent=True,
            is_keepalive=True,
            frame_loading=True,
            is_hidden_tag=False,
            fixed_tag=False,
            dynamic_level=1
        )
        
        db.add(menu_meta)
        db.flush()
        
        # 创建菜单
        menus_data = [
            # 系统管理
            {
                "id": str(uuid.uuid4()).replace('-', ''),
                "name": "PureSystem",
                "path": "/system",
                "menu_type": 0,  # 目录
                "rank": 10,
                "is_active": True,
                "meta_id": menu_meta.id
            },
            
            # 用户管理
            {
                "id": str(uuid.uuid4()).replace('-', ''),
                "name": "SystemUser",
                "path": "/system/user/index",
                "menu_type": 1,  # 菜单
                "rank": 1,
                "is_active": True,
                "parent_id": None,
                "meta_id": menu_meta.id
            },
            
            # 角色管理
            {
                "id": str(uuid.uuid4()).replace('-', ''),
                "name": "SystemRole",
                "path": "/system/role/index",
                "menu_type": 1,  # 菜单
                "rank": 2,
                "is_active": True,
                "parent_id": None,
                "meta_id": menu_meta.id
            },
            
            # 部门管理
            {
                "id": str(uuid.uuid4()).replace('-', ''),
                "name": "SystemDept",
                "path": "/system/dept/index",
                "menu_type": 1,  # 菜单
                "rank": 3,
                "is_active": True,
                "parent_id": None,
                "meta_id": menu_meta.id
            },
            
            # 菜单管理
            {
                "id": str(uuid.uuid4()).replace('-', ''),
                "name": "SystemMenu",
                "path": "/system/menu/index",
                "menu_type": 1,  # 菜单
                "rank": 4,
                "is_active": True,
                "parent_id": None,
                "meta_id": menu_meta.id
            },
            
            # 系统监控
            {
                "id": str(uuid.uuid4()).replace('-', ''),
                "name": "PureMonitor",
                "path": "/monitor",
                "menu_type": 0,  # 目录
                "rank": 11,
                "is_active": True,
                "meta_id": menu_meta.id
            },
            
            # 登录日志
            {
                "id": str(uuid.uuid4()).replace('-', ''),
                "name": "LoginLog",
                "path": "/monitor/login-logs",
                "menu_type": 1,  # 菜单
                "rank": 1,
                "is_active": True,
                "parent_id": None,
                "meta_id": menu_meta.id
            },
            
            # 操作日志
            {
                "id": str(uuid.uuid4()).replace('-', ''),
                "name": "OperationLog",
                "path": "/monitor/operation-logs",
                "menu_type": 1,  # 菜单
                "rank": 2,
                "is_active": True,
                "parent_id": None,
                "meta_id": menu_meta.id
            },
            
            # 系统日志
            {
                "id": str(uuid.uuid4()).replace('-', ''),
                "name": "SystemLog",
                "path": "/monitor/system-logs",
                "menu_type": 1,  # 菜单
                "rank": 3,
                "is_active": True,
                "parent_id": None,
                "meta_id": menu_meta.id
            }
        ]
        
        menu_objects = []
        for menu_data in menus_data:
            menu = Menu(**menu_data)
            menu_objects.append(menu)
            db.add(menu)
        
        db.flush()
        
        # 创建角色菜单关联 - 管理员拥有所有权限
        for menu in menu_objects:
            role_menu = RoleMenu(
                userrole_id=admin_role.id,
                menu_id=menu.id
            )
            db.add(role_menu)
        
        db.commit()
        log_database_success()
        
    except Exception as e:
        get_business_logger().error(f"Error initializing database: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    init_database()