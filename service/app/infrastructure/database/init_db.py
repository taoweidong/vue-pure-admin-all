import os
import sqlite3
from sqlalchemy.orm import Session
from app.infrastructure.database.database import SessionLocal, engine
from app.domain.entities.models import *
from app.domain.entities.logs import *
from app.infrastructure.utils.auth import AuthService
from app.infrastructure.utils.logger import (
    log_file_not_found, log_sql_execution, log_sql_error, log_database_init,
    log_database_success, log_password_update, log_password_update_error,
    log_database_exists, log_database_with_data, get_business_logger
)
from datetime import datetime


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
                cursor.execute("SELECT COUNT(*) FROM users")
                user_count = cursor.fetchone()[0]
                if user_count > 0:
                    log_database_with_data()
                    return
        except sqlite3.OperationalError:
            # 表不存在，需要初始化
            pass
    
    log_database_init()
    
    # SQL文件路径
    sql_dir = os.path.join(db_dir, 'init')
    sql_files = [
        '01_create_tables.sql',
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
            cursor.execute("UPDATE users SET password_hash = ? WHERE username = 'admin'", (admin_hash,))
            cursor.execute("UPDATE users SET password_hash = ? WHERE username = 'common'", (common_hash,))
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
            id=103,
            name="研发部门",
            code="dev",
            leader="张三",
            phone="13800138000",
            email="dev@example.com",
            status=1,
            sort=1
        )
        
        test_dept = Department(
            id=105,
            name="测试部门",
            code="test",
            leader="李四",
            phone="13800138001",
            email="test@example.com",
            status=1,
            sort=2
        )
        
        db.add(dev_dept)
        db.add(test_dept)
        db.flush()
        
        # 创建角色
        admin_role = Role(
            id=1,
            name="超级管理员",
            code="admin",
            status=1,
            remark="超级管理员拥有最高权限"
        )
        
        common_role = Role(
            id=2,
            name="普通角色",
            code="common",
            status=1,
            remark="普通角色拥有部分权限"
        )
        
        db.add(admin_role)
        db.add(common_role)
        db.flush()
        
        # 创建用户
        admin_user = User(
            id=1,
            username="admin",
            nickname="小铭",
            email="admin@example.com",
            phone="15888886789",
            avatar="https://avatars.githubusercontent.com/u/44761321",
            password_hash=auth_service.get_password_hash("admin123"),
            description="系统管理员",
            sex=1,
            status=1,
            dept_id=103,
            remark="管理员账户"
        )
        
        common_user = User(
            id=2,
            username="common",
            nickname="小林",
            email="common@example.com",
            phone="18288882345",
            avatar="https://avatars.githubusercontent.com/u/52823142",
            password_hash=auth_service.get_password_hash("common123"),
            description="普通用户",
            sex=2,
            status=1,
            dept_id=105,
            remark="普通用户账户"
        )
        
        db.add(admin_user)
        db.add(common_user)
        db.flush()
        
        # 创建用户角色关联
        admin_user_role = UserRole(user_id=1, role_id=1)
        common_user_role = UserRole(user_id=2, role_id=2)
        
        db.add(admin_user_role)
        db.add(common_user_role)
        
        # 创建菜单（保持与之前相同的菜单结构）
        menus = [
            # 外部页面
            Menu(id=100, parent_id=0, title="menus.pureExternalPage", name="PureIframe", path="/iframe", menu_type=0, rank=7, icon="ri:links-fill", show_link=True),
            Menu(id=101, parent_id=100, title="menus.pureExternalDoc", name="PureIframeExternal", path="/iframe/external", menu_type=0, show_link=True),
            Menu(id=102, parent_id=101, title="menus.pureExternalLink", name="https://pure-admin.cn/", path="/external", menu_type=2, show_link=True),
            Menu(id=103, parent_id=101, title="menus.pureUtilsLink", name="https://pure-admin-utils.netlify.app/", path="/pureUtilsLink", menu_type=2, show_link=True),
            Menu(id=104, parent_id=100, title="menus.pureEmbeddedDoc", name="PureIframeEmbedded", path="/iframe/embedded", menu_type=1, show_link=True),
            Menu(id=105, parent_id=104, title="menus.pureEpDoc", name="FrameEp", path="/iframe/ep", menu_type=1, frame_src="https://element-plus.org/zh-CN/", keep_alive=True, show_link=True),
            
            # 权限管理
            Menu(id=200, parent_id=0, title="menus.purePermission", name="PurePermission", path="/permission", menu_type=0, rank=9, icon="ep:lollipop", show_link=True),
            Menu(id=201, parent_id=200, title="menus.purePermissionPage", name="PermissionPage", path="/permission/page/index", menu_type=0, show_link=True),
            Menu(id=202, parent_id=200, title="menus.purePermissionButton", name="PermissionButton", path="/permission/button", menu_type=0, show_link=True),
            Menu(id=203, parent_id=202, title="添加", name="", path="", menu_type=3, auths="permission:btn:add", show_link=True),
            Menu(id=204, parent_id=202, title="修改", name="", path="", menu_type=3, auths="permission:btn:edit", show_link=True),
            Menu(id=205, parent_id=202, title="删除", name="", path="", menu_type=3, auths="permission:btn:delete", show_link=True),
            
            # 系统管理
            Menu(id=300, parent_id=0, title="menus.pureSysManagement", name="PureSystem", path="/system", menu_type=0, rank=10, icon="ri:settings-3-line", show_link=True),
            Menu(id=301, parent_id=300, title="menus.pureUser", name="SystemUser", path="/system/user/index", menu_type=0, icon="ri:admin-line", show_link=True),
            Menu(id=302, parent_id=300, title="menus.pureRole", name="SystemRole", path="/system/role/index", menu_type=0, icon="ri:admin-fill", show_link=True),
            Menu(id=303, parent_id=300, title="menus.pureSystemMenu", name="SystemMenu", path="/system/menu/index", menu_type=0, icon="ep:menu", show_link=True),
            Menu(id=304, parent_id=300, title="menus.pureDept", name="SystemDept", path="/system/dept/index", menu_type=0, icon="ri:git-branch-line", show_link=True),
            
            # 系统监控
            Menu(id=400, parent_id=0, title="menus.pureSysMonitor", name="PureMonitor", path="/monitor", menu_type=0, rank=11, icon="ep:monitor", show_link=True),
            Menu(id=401, parent_id=400, title="menus.pureOnlineUser", name="OnlineUser", path="/monitor/online-user", menu_type=0, icon="ri:user-voice-line", show_link=True),
            Menu(id=402, parent_id=400, title="menus.pureLoginLog", name="LoginLog", path="/monitor/login-logs", menu_type=0, icon="ri:window-line", show_link=True),
            Menu(id=403, parent_id=400, title="menus.pureOperationLog", name="OperationLog", path="/monitor/operation-logs", menu_type=0, icon="ri:history-fill", show_link=True),
            Menu(id=404, parent_id=400, title="menus.pureSystemLog", name="SystemLog", path="/monitor/system-logs", menu_type=0, icon="ri:file-search-line", show_link=True),
            
            # 标签页操作
            Menu(id=500, parent_id=0, title="menus.pureTabs", name="PureTabs", path="/tabs", menu_type=0, rank=12, icon="ri:bookmark-2-line", show_link=True),
            Menu(id=501, parent_id=500, title="menus.pureTabs", name="Tabs", path="/tabs/index", menu_type=0, show_link=True),
        ]
        
        for menu in menus:
            db.add(menu)
        
        db.flush()
        
        # 创建角色菜单关联 - 管理员拥有所有权限
        admin_menu_ids = [100, 101, 102, 103, 104, 105, 200, 201, 202, 203, 204, 205, 300, 301, 302, 303, 304, 400, 401, 402, 403, 404, 500, 501]
        for menu_id in admin_menu_ids:
            role_menu = RoleMenu(role_id=1, menu_id=menu_id)
            db.add(role_menu)
        
        # 普通用户权限
        common_menu_ids = [100, 101, 102, 103, 104, 105, 200, 201, 404, 500, 501]
        for menu_id in common_menu_ids:
            role_menu = RoleMenu(role_id=2, menu_id=menu_id)
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