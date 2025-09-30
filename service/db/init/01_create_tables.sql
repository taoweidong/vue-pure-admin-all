-- 创建用户表
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    nickname VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE,
    phone VARCHAR(20) UNIQUE,
    avatar VARCHAR(255),
    password_hash VARCHAR(255) NOT NULL,
    description TEXT,
    sex INTEGER DEFAULT 0, -- 0-未知 1-男 2-女
    status INTEGER DEFAULT 1, -- 1-启用 0-禁用
    dept_id INTEGER,
    remark TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (dept_id) REFERENCES departments(id)
);

-- 创建角色表
CREATE TABLE IF NOT EXISTS roles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(50) UNIQUE NOT NULL,
    code VARCHAR(50) UNIQUE NOT NULL,
    status INTEGER DEFAULT 1, -- 1-启用 0-禁用
    remark TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 创建菜单表
CREATE TABLE IF NOT EXISTS menus (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    parent_id INTEGER DEFAULT 0,
    title VARCHAR(100) NOT NULL,
    name VARCHAR(100),
    path VARCHAR(255),
    component VARCHAR(255),
    menu_type INTEGER DEFAULT 0, -- 0-菜单 1-iframe 2-外链 3-按钮
    rank INTEGER,
    redirect VARCHAR(255),
    icon VARCHAR(100),
    extra_icon VARCHAR(100),
    enter_transition VARCHAR(100),
    leave_transition VARCHAR(100),
    active_path VARCHAR(255),
    auths VARCHAR(255),
    frame_src VARCHAR(255),
    frame_loading BOOLEAN DEFAULT 1,
    keep_alive BOOLEAN DEFAULT 0,
    hidden_tag BOOLEAN DEFAULT 0,
    fixed_tag BOOLEAN DEFAULT 0,
    show_link BOOLEAN DEFAULT 1,
    show_parent BOOLEAN DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (parent_id) REFERENCES menus(id)
);

-- 创建部门表
CREATE TABLE IF NOT EXISTS departments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    parent_id INTEGER DEFAULT 0,
    name VARCHAR(100) NOT NULL,
    code VARCHAR(50) UNIQUE NOT NULL,
    leader VARCHAR(50),
    phone VARCHAR(20),
    email VARCHAR(100),
    status INTEGER DEFAULT 1, -- 1-启用 0-禁用
    sort INTEGER DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (parent_id) REFERENCES departments(id)
);

-- 创建用户角色关联表
CREATE TABLE IF NOT EXISTS user_roles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    role_id INTEGER NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (role_id) REFERENCES roles(id)
);

-- 创建角色菜单关联表
CREATE TABLE IF NOT EXISTS role_menus (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    role_id INTEGER NOT NULL,
    menu_id INTEGER NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (role_id) REFERENCES roles(id),
    FOREIGN KEY (menu_id) REFERENCES menus(id)
);

-- 创建登录日志表
CREATE TABLE IF NOT EXISTS login_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    username VARCHAR(50) NOT NULL,
    ip VARCHAR(45),
    location VARCHAR(255),
    browser VARCHAR(100),
    os VARCHAR(100),
    status INTEGER DEFAULT 1, -- 1-成功 0-失败
    message VARCHAR(255),
    login_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- 创建操作日志表
CREATE TABLE IF NOT EXISTS operation_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    username VARCHAR(50),
    module VARCHAR(100),
    summary VARCHAR(255),
    method VARCHAR(10),
    request_url VARCHAR(255),
    request_params TEXT,
    ip VARCHAR(45),
    location VARCHAR(255),
    browser VARCHAR(100),
    os VARCHAR(100),
    status INTEGER DEFAULT 1, -- 1-成功 0-失败
    error_msg TEXT,
    operate_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- 创建系统日志表
CREATE TABLE IF NOT EXISTS system_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    level VARCHAR(20) NOT NULL,
    module VARCHAR(100),
    message TEXT NOT NULL,
    detail TEXT,
    ip VARCHAR(45),
    user_agent VARCHAR(255),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 创建在线用户表
CREATE TABLE IF NOT EXISTS online_users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    username VARCHAR(50) NOT NULL,
    nickname VARCHAR(50) NOT NULL,
    token VARCHAR(255) UNIQUE NOT NULL,
    ip VARCHAR(45),
    location VARCHAR(255),
    browser VARCHAR(100),
    os VARCHAR(100),
    login_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_access_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);