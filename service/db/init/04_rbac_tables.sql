"""
RBAC权限系统数据库迁移脚本

创建完整的RBAC权限管理所需的数据库表
"""

-- 权限表
CREATE TABLE IF NOT EXISTS permissions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL UNIQUE COMMENT '权限名称',
    code VARCHAR(100) NOT NULL UNIQUE COMMENT '权限编码',
    resource VARCHAR(100) NOT NULL COMMENT '资源标识',
    action VARCHAR(50) NOT NULL COMMENT '操作类型',
    description TEXT COMMENT '权限描述',
    category VARCHAR(50) COMMENT '权限分类',
    status INTEGER DEFAULT 1 COMMENT '状态 1-启用 0-禁用',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间'
);

-- 资源表
CREATE TABLE IF NOT EXISTS resources (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL COMMENT '资源名称',
    code VARCHAR(100) NOT NULL UNIQUE COMMENT '资源编码',
    type VARCHAR(50) NOT NULL COMMENT '资源类型 menu|button|api|data',
    url VARCHAR(255) COMMENT '资源URL',
    method VARCHAR(20) COMMENT 'HTTP方法',
    parent_id INTEGER DEFAULT 0 COMMENT '父资源ID',
    description TEXT COMMENT '资源描述',
    status INTEGER DEFAULT 1 COMMENT '状态 1-启用 0-禁用',
    sort INTEGER DEFAULT 0 COMMENT '排序',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
    FOREIGN KEY (parent_id) REFERENCES resources(id)
);

-- 角色权限关联表
CREATE TABLE IF NOT EXISTS role_permissions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    role_id INTEGER NOT NULL COMMENT '角色ID',
    permission_id INTEGER NOT NULL COMMENT '权限ID',
    granted BOOLEAN DEFAULT TRUE COMMENT '是否授权',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE,
    FOREIGN KEY (permission_id) REFERENCES permissions(id) ON DELETE CASCADE,
    UNIQUE(role_id, permission_id)
);

-- 数据权限范围表
CREATE TABLE IF NOT EXISTS data_scopes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    role_id INTEGER NOT NULL COMMENT '角色ID',
    scope_type VARCHAR(50) NOT NULL COMMENT '数据范围类型 all|custom|dept|dept_and_child|self',
    scope_value TEXT COMMENT '范围值，JSON格式',
    resource_type VARCHAR(50) NOT NULL COMMENT '资源类型',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE
);

-- 用户会话表
CREATE TABLE IF NOT EXISTS user_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL COMMENT '用户ID',
    session_id VARCHAR(255) NOT NULL UNIQUE COMMENT '会话ID',
    access_token TEXT NOT NULL COMMENT '访问令牌',
    refresh_token TEXT COMMENT '刷新令牌',
    ip_address VARCHAR(45) COMMENT 'IP地址',
    user_agent TEXT COMMENT '用户代理',
    device_info TEXT COMMENT '设备信息',
    location VARCHAR(255) COMMENT '登录地点',
    is_active BOOLEAN DEFAULT TRUE COMMENT '是否激活',
    expires_at DATETIME NOT NULL COMMENT '过期时间',
    last_activity_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '最后活动时间',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 用户档案扩展表
CREATE TABLE IF NOT EXISTS user_profiles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL UNIQUE COMMENT '用户ID',
    real_name VARCHAR(50) COMMENT '真实姓名',
    id_card VARCHAR(20) COMMENT '身份证号',
    birthday DATETIME COMMENT '生日',
    address VARCHAR(255) COMMENT '地址',
    emergency_contact VARCHAR(50) COMMENT '紧急联系人',
    emergency_phone VARCHAR(20) COMMENT '紧急联系电话',
    job_title VARCHAR(100) COMMENT '职位',
    entry_date DATETIME COMMENT '入职日期',
    work_location VARCHAR(255) COMMENT '工作地点',
    supervisor_id INTEGER COMMENT '直属上级',
    preferences TEXT COMMENT '用户偏好设置，JSON格式',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (supervisor_id) REFERENCES users(id)
);

-- 职位表
CREATE TABLE IF NOT EXISTS positions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL COMMENT '职位名称',
    code VARCHAR(50) NOT NULL UNIQUE COMMENT '职位编码',
    department_id INTEGER NOT NULL COMMENT '所属部门ID',
    level INTEGER DEFAULT 1 COMMENT '职位级别',
    category VARCHAR(50) COMMENT '职位类别',
    description TEXT COMMENT '职位描述',
    requirements TEXT COMMENT '任职要求',
    responsibilities TEXT COMMENT '工作职责',
    salary_range VARCHAR(100) COMMENT '薪资范围',
    is_leadership BOOLEAN DEFAULT FALSE COMMENT '是否管理岗位',
    max_count INTEGER DEFAULT 1 COMMENT '最大人数',
    current_count INTEGER DEFAULT 0 COMMENT '当前人数',
    status INTEGER DEFAULT 1 COMMENT '状态 1-启用 0-禁用',
    sort INTEGER DEFAULT 0 COMMENT '排序',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
    FOREIGN KEY (department_id) REFERENCES departments(id)
);

-- 用户职位关联表
CREATE TABLE IF NOT EXISTS user_positions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL COMMENT '用户ID',
    position_id INTEGER NOT NULL COMMENT '职位ID',
    is_primary BOOLEAN DEFAULT TRUE COMMENT '是否主要职位',
    start_date DATETIME COMMENT '开始日期',
    end_date DATETIME COMMENT '结束日期',
    status INTEGER DEFAULT 1 COMMENT '状态 1-在职 0-离职',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (position_id) REFERENCES positions(id)
);

-- 菜单权限关联表
CREATE TABLE IF NOT EXISTS menu_permissions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    menu_id INTEGER NOT NULL COMMENT '菜单ID',
    permission_id INTEGER NOT NULL COMMENT '权限ID',
    required BOOLEAN DEFAULT TRUE COMMENT '是否必需',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    FOREIGN KEY (menu_id) REFERENCES menus(id) ON DELETE CASCADE,
    FOREIGN KEY (permission_id) REFERENCES permissions(id) ON DELETE CASCADE,
    UNIQUE(menu_id, permission_id)
);

-- 菜单操作记录表
CREATE TABLE IF NOT EXISTS menu_operations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    menu_id INTEGER NOT NULL COMMENT '菜单ID',
    operator_id INTEGER NOT NULL COMMENT '操作人ID',
    operation_type VARCHAR(20) NOT NULL COMMENT '操作类型 create|update|delete|sort',
    old_value TEXT COMMENT '操作前的值',
    new_value TEXT COMMENT '操作后的值',
    remark VARCHAR(255) COMMENT '备注',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    FOREIGN KEY (menu_id) REFERENCES menus(id),
    FOREIGN KEY (operator_id) REFERENCES users(id)
);

-- 角色继承关系表
CREATE TABLE IF NOT EXISTS role_inheritances (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    parent_role_id INTEGER NOT NULL COMMENT '父角色ID',
    child_role_id INTEGER NOT NULL COMMENT '子角色ID',
    inherit_type VARCHAR(20) DEFAULT 'full' COMMENT '继承类型 full|partial',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    FOREIGN KEY (parent_role_id) REFERENCES roles(id) ON DELETE CASCADE,
    FOREIGN KEY (child_role_id) REFERENCES roles(id) ON DELETE CASCADE,
    UNIQUE(parent_role_id, child_role_id)
);

-- 部门变更历史表
CREATE TABLE IF NOT EXISTS department_histories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    department_id INTEGER NOT NULL COMMENT '部门ID',
    operation_type VARCHAR(20) NOT NULL COMMENT '操作类型 create|update|delete|move',
    old_value TEXT COMMENT '变更前的值',
    new_value TEXT COMMENT '变更后的值',
    operator_id INTEGER NOT NULL COMMENT '操作人ID',
    reason VARCHAR(255) COMMENT '变更原因',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    FOREIGN KEY (department_id) REFERENCES departments(id),
    FOREIGN KEY (operator_id) REFERENCES users(id)
);

-- 审计日志表
CREATE TABLE IF NOT EXISTS audit_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER COMMENT '用户ID',
    username VARCHAR(50) COMMENT '用户名',
    event_type VARCHAR(50) NOT NULL COMMENT '事件类型',
    resource_type VARCHAR(50) NOT NULL COMMENT '资源类型',
    resource_id VARCHAR(100) COMMENT '资源ID',
    resource_name VARCHAR(255) COMMENT '资源名称',
    action VARCHAR(50) NOT NULL COMMENT '操作动作',
    old_values TEXT COMMENT '操作前的值',
    new_values TEXT COMMENT '操作后的值',
    result VARCHAR(20) DEFAULT 'success' COMMENT '操作结果 success|failure',
    risk_level VARCHAR(20) DEFAULT 'low' COMMENT '风险级别 low|medium|high|critical',
    session_id VARCHAR(255) COMMENT '会话ID',
    ip VARCHAR(45) COMMENT 'IP地址',
    user_agent TEXT COMMENT '用户代理',
    remark VARCHAR(500) COMMENT '备注',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- 安全事件表
CREATE TABLE IF NOT EXISTS security_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_id VARCHAR(100) NOT NULL UNIQUE COMMENT '事件ID',
    event_type VARCHAR(50) NOT NULL COMMENT '事件类型',
    severity VARCHAR(20) NOT NULL COMMENT '严重级别 low|medium|high|critical',
    title VARCHAR(255) NOT NULL COMMENT '事件标题',
    description TEXT COMMENT '事件描述',
    source_ip VARCHAR(45) COMMENT '来源IP',
    target_ip VARCHAR(45) COMMENT '目标IP',
    user_id INTEGER COMMENT '相关用户ID',
    username VARCHAR(50) COMMENT '用户名',
    affected_resource VARCHAR(255) COMMENT '受影响资源',
    attack_vector VARCHAR(100) COMMENT '攻击向量',
    detection_method VARCHAR(100) COMMENT '检测方法',
    status VARCHAR(20) DEFAULT 'new' COMMENT '处理状态 new|investigating|resolved|false_positive',
    handled_by INTEGER COMMENT '处理人',
    handled_at DATETIME COMMENT '处理时间',
    resolution TEXT COMMENT '处理结果',
    raw_data TEXT COMMENT '原始数据',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (handled_by) REFERENCES users(id)
);

-- 更新现有表结构

-- 更新用户表
ALTER TABLE users ADD COLUMN last_login_at DATETIME COMMENT '最后登录时间';
ALTER TABLE users ADD COLUMN last_login_ip VARCHAR(45) COMMENT '最后登录IP';  
ALTER TABLE users ADD COLUMN password_changed_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '密码修改时间';
ALTER TABLE users ADD COLUMN is_locked BOOLEAN DEFAULT FALSE COMMENT '是否锁定';
ALTER TABLE users ADD COLUMN lock_reason VARCHAR(255) COMMENT '锁定原因';
ALTER TABLE users ADD COLUMN failed_login_attempts INTEGER DEFAULT 0 COMMENT '失败登录尝试次数';

-- 更新角色表
ALTER TABLE roles ADD COLUMN type VARCHAR(20) DEFAULT 'custom' COMMENT '角色类型 system|custom';
ALTER TABLE roles ADD COLUMN level INTEGER DEFAULT 0 COMMENT '角色级别，数字越大级别越高';
ALTER TABLE roles ADD COLUMN parent_id INTEGER DEFAULT 0 COMMENT '父角色ID';
ALTER TABLE roles ADD COLUMN description TEXT COMMENT '角色描述';
ALTER TABLE roles ADD COLUMN is_default BOOLEAN DEFAULT FALSE COMMENT '是否默认角色';
ALTER TABLE roles ADD COLUMN max_users INTEGER COMMENT '最大用户数限制';

-- 更新用户角色关联表
ALTER TABLE user_roles ADD COLUMN granted_by INTEGER COMMENT '授权人';
ALTER TABLE user_roles ADD COLUMN granted_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '授权时间';
ALTER TABLE user_roles ADD COLUMN expires_at DATETIME COMMENT '过期时间';
ALTER TABLE user_roles ADD COLUMN is_active BOOLEAN DEFAULT TRUE COMMENT '是否激活';

-- 更新角色菜单关联表
ALTER TABLE role_menus ADD COLUMN granted BOOLEAN DEFAULT TRUE COMMENT '是否授权';

-- 更新菜单表
ALTER TABLE menus ADD COLUMN is_external BOOLEAN DEFAULT FALSE COMMENT '是否外部链接';
ALTER TABLE menus ADD COLUMN external_url VARCHAR(500) COMMENT '外部链接地址';
ALTER TABLE menus ADD COLUMN meta TEXT COMMENT '菜单元数据';
ALTER TABLE menus ADD COLUMN status INTEGER DEFAULT 1 COMMENT '状态 1-启用 0-禁用';

-- 更新部门表
ALTER TABLE departments ADD COLUMN full_name VARCHAR(255) COMMENT '部门全称';
ALTER TABLE departments ADD COLUMN type VARCHAR(20) DEFAULT 'department' COMMENT '类型 company|department|team|group';
ALTER TABLE departments ADD COLUMN level INTEGER DEFAULT 1 COMMENT '层级';
ALTER TABLE departments ADD COLUMN path VARCHAR(500) COMMENT '路径，用/分隔';
ALTER TABLE departments ADD COLUMN leader_id INTEGER COMMENT '负责人ID';
ALTER TABLE departments ADD COLUMN address VARCHAR(255) COMMENT '办公地址';
ALTER TABLE departments ADD COLUMN description TEXT COMMENT '部门描述';
ALTER TABLE departments ADD COLUMN function_desc TEXT COMMENT '职能描述';
ALTER TABLE departments ADD COLUMN cost_center VARCHAR(50) COMMENT '成本中心';
ALTER TABLE departments ADD COLUMN budget_limit INTEGER COMMENT '预算限额';
ALTER TABLE departments ADD COLUMN employee_limit INTEGER COMMENT '人员限制';
ALTER TABLE departments ADD COLUMN extra_info TEXT COMMENT '扩展信息';

-- 更新登录日志表
ALTER TABLE login_logs ADD COLUMN login_type VARCHAR(20) DEFAULT 'web' COMMENT '登录类型 web|mobile|api';
ALTER TABLE login_logs ADD COLUMN client_type VARCHAR(20) COMMENT '客户端类型';
ALTER TABLE login_logs ADD COLUMN device VARCHAR(100) COMMENT '设备信息';
ALTER TABLE login_logs ADD COLUMN user_agent TEXT COMMENT '用户代理';
ALTER TABLE login_logs ADD COLUMN failure_reason VARCHAR(255) COMMENT '失败原因';
ALTER TABLE login_logs ADD COLUMN session_id VARCHAR(255) COMMENT '会话ID';
ALTER TABLE login_logs ADD COLUMN logout_time DATETIME COMMENT '登出时间';
ALTER TABLE login_logs ADD COLUMN duration INTEGER COMMENT '会话持续时间(秒)';

-- 更新操作日志表
ALTER TABLE operation_logs ADD COLUMN operation VARCHAR(100) COMMENT '操作名称';
ALTER TABLE operation_logs ADD COLUMN response_data TEXT COMMENT '响应数据';
ALTER TABLE operation_logs ADD COLUMN business_id VARCHAR(100) COMMENT '业务ID';
ALTER TABLE operation_logs ADD COLUMN business_type VARCHAR(50) COMMENT '业务类型';
ALTER TABLE operation_logs ADD COLUMN user_agent TEXT COMMENT '用户代理';
ALTER TABLE operation_logs ADD COLUMN execute_time INTEGER COMMENT '执行时间(毫秒)';
ALTER TABLE operation_logs ADD COLUMN remark VARCHAR(500) COMMENT '备注';

-- 更新系统日志表
ALTER TABLE system_logs ADD COLUMN category VARCHAR(50) COMMENT '日志分类';
ALTER TABLE system_logs ADD COLUMN function VARCHAR(100) COMMENT '函数名称';
ALTER TABLE system_logs ADD COLUMN exception TEXT COMMENT '异常信息';
ALTER TABLE system_logs ADD COLUMN trace_id VARCHAR(100) COMMENT '追踪ID';
ALTER TABLE system_logs ADD COLUMN span_id VARCHAR(100) COMMENT '跨度ID';
ALTER TABLE system_logs ADD COLUMN extra_data TEXT COMMENT '额外数据';

-- 创建索引
CREATE INDEX IF NOT EXISTS idx_permissions_resource ON permissions(resource);
CREATE INDEX IF NOT EXISTS idx_permissions_action ON permissions(action);
CREATE INDEX IF NOT EXISTS idx_permissions_status ON permissions(status);

CREATE INDEX IF NOT EXISTS idx_resources_type ON resources(type);
CREATE INDEX IF NOT EXISTS idx_resources_status ON resources(status);
CREATE INDEX IF NOT EXISTS idx_resources_parent_id ON resources(parent_id);

CREATE INDEX IF NOT EXISTS idx_role_permissions_role_id ON role_permissions(role_id);
CREATE INDEX IF NOT EXISTS idx_role_permissions_permission_id ON role_permissions(permission_id);

CREATE INDEX IF NOT EXISTS idx_data_scopes_role_id ON data_scopes(role_id);
CREATE INDEX IF NOT EXISTS idx_data_scopes_resource_type ON data_scopes(resource_type);

CREATE INDEX IF NOT EXISTS idx_user_sessions_user_id ON user_sessions(user_id);
CREATE INDEX IF NOT EXISTS idx_user_sessions_session_id ON user_sessions(session_id);
CREATE INDEX IF NOT EXISTS idx_user_sessions_is_active ON user_sessions(is_active);

CREATE INDEX IF NOT EXISTS idx_user_profiles_user_id ON user_profiles(user_id);

CREATE INDEX IF NOT EXISTS idx_positions_department_id ON positions(department_id);
CREATE INDEX IF NOT EXISTS idx_positions_status ON positions(status);

CREATE INDEX IF NOT EXISTS idx_user_positions_user_id ON user_positions(user_id);
CREATE INDEX IF NOT EXISTS idx_user_positions_position_id ON user_positions(position_id);

CREATE INDEX IF NOT EXISTS idx_menu_permissions_menu_id ON menu_permissions(menu_id);
CREATE INDEX IF NOT EXISTS idx_menu_permissions_permission_id ON menu_permissions(permission_id);

CREATE INDEX IF NOT EXISTS idx_audit_logs_user_id ON audit_logs(user_id);
CREATE INDEX IF NOT EXISTS idx_audit_logs_event_type ON audit_logs(event_type);
CREATE INDEX IF NOT EXISTS idx_audit_logs_resource_type ON audit_logs(resource_type);
CREATE INDEX IF NOT EXISTS idx_audit_logs_created_at ON audit_logs(created_at);

CREATE INDEX IF NOT EXISTS idx_security_events_event_type ON security_events(event_type);
CREATE INDEX IF NOT EXISTS idx_security_events_severity ON security_events(severity);
CREATE INDEX IF NOT EXISTS idx_security_events_status ON security_events(status);
CREATE INDEX IF NOT EXISTS idx_security_events_created_at ON security_events(created_at);

-- 用户表索引
CREATE INDEX IF NOT EXISTS idx_users_status ON users(status);
CREATE INDEX IF NOT EXISTS idx_users_is_locked ON users(is_locked);
CREATE INDEX IF NOT EXISTS idx_users_last_login_at ON users(last_login_at);

-- 角色表索引
CREATE INDEX IF NOT EXISTS idx_roles_type ON roles(type);
CREATE INDEX IF NOT EXISTS idx_roles_level ON roles(level);
CREATE INDEX IF NOT EXISTS idx_roles_parent_id ON roles(parent_id);

-- 用户角色关联表索引
CREATE INDEX IF NOT EXISTS idx_user_roles_is_active ON user_roles(is_active);
CREATE INDEX IF NOT EXISTS idx_user_roles_granted_by ON user_roles(granted_by);

-- 菜单表索引
CREATE INDEX IF NOT EXISTS idx_menus_status ON menus(status);
CREATE INDEX IF NOT EXISTS idx_menus_menu_type ON menus(menu_type);

-- 部门表索引
CREATE INDEX IF NOT EXISTS idx_departments_type ON departments(type);
CREATE INDEX IF NOT EXISTS idx_departments_level ON departments(level);
CREATE INDEX IF NOT EXISTS idx_departments_leader_id ON departments(leader_id);

-- 日志表索引
CREATE INDEX IF NOT EXISTS idx_login_logs_login_type ON login_logs(login_type);
CREATE INDEX IF NOT EXISTS idx_login_logs_status ON login_logs(status);
CREATE INDEX IF NOT EXISTS idx_login_logs_login_time ON login_logs(login_time);

CREATE INDEX IF NOT EXISTS idx_operation_logs_module ON operation_logs(module);
CREATE INDEX IF NOT EXISTS idx_operation_logs_operation ON operation_logs(operation);
CREATE INDEX IF NOT EXISTS idx_operation_logs_business_type ON operation_logs(business_type);
CREATE INDEX IF NOT EXISTS idx_operation_logs_operate_time ON operation_logs(operate_time);

CREATE INDEX IF NOT EXISTS idx_system_logs_level ON system_logs(level);
CREATE INDEX IF NOT EXISTS idx_system_logs_category ON system_logs(category);
CREATE INDEX IF NOT EXISTS idx_system_logs_created_at ON system_logs(created_at);