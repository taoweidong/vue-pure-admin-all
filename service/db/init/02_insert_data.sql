-- 插入部门数据
INSERT OR IGNORE INTO system_deptinfo (id, parent_id, name, code, rank, is_active, auto_bind, mode_type, created_time, updated_time) VALUES
('103', '0', '研发部门', 'dev', 1, 1, 1, 1, datetime('now'), datetime('now')),
('105', '0', '测试部门', 'test', 2, 1, 1, 1, datetime('now'), datetime('now'));

-- 插入角色数据
INSERT OR IGNORE INTO system_userrole (id, name, code, is_active, description, created_time, updated_time) VALUES
('1', '超级管理员', 'admin', 1, '超级管理员拥有最高权限', datetime('now'), datetime('now')),
('2', '普通角色', 'common', 1, '普通角色拥有部分权限', datetime('now'), datetime('now'));

-- 插入用户数据（密码：admin123 和 common123 的bcrypt哈希）
INSERT OR IGNORE INTO system_userinfo (id, username, password, nickname, email, phone, avatar, description, gender, is_active, is_staff, is_superuser, date_joined, mode_type, created_time, updated_time, dept_id) VALUES
('1', 'admin', 'temp_hash_admin', '小铭', 'admin@example.com', '15888886789', 'https://avatars.githubusercontent.com/u/44761321', '系统管理员', 1, 1, 1, 1, datetime('now'), 1, datetime('now'), datetime('now'), '103'),
('2', 'common', 'temp_hash_common', '小林', 'common@example.com', '18288882345', 'https://avatars.githubusercontent.com/u/52823142', '普通用户', 2, 1, 1, 0, datetime('now'), 1, datetime('now'), datetime('now'), '105');

-- 插入用户角色关联
INSERT OR IGNORE INTO system_userinfo_roles (userinfo_id, userrole_id) VALUES
('1', '1'), -- admin -> 超级管理员
('2', '2'); -- common -> 普通角色

-- 插入菜单元数据
INSERT OR IGNORE INTO system_menumeta (id, title, icon, is_show_menu, is_show_parent, is_keepalive, frame_loading, is_hidden_tag, fixed_tag, dynamic_level, created_time, updated_time) VALUES
('1', '系统管理', 'ri:settings-3-line', 1, 1, 1, 1, 0, 0, 1, datetime('now'), datetime('now'));

-- 插入菜单数据
INSERT OR IGNORE INTO system_menu (id, name, path, menu_type, rank, is_active, meta_id, created_time, updated_time) VALUES
-- 系统管理
('100', 'PureSystem', '/system', 0, 10, 1, '1', datetime('now'), datetime('now')),

-- 用户管理
('101', 'SystemUser', '/system/user/index', 1, 1, 1, '1', datetime('now'), datetime('now')),

-- 角色管理
('102', 'SystemRole', '/system/role/index', 1, 2, 1, '1', datetime('now'), datetime('now')),

-- 部门管理
('103', 'SystemDept', '/system/dept/index', 1, 3, 1, '1', datetime('now'), datetime('now')),

-- 菜单管理
('104', 'SystemMenu', '/system/menu/index', 1, 4, 1, '1', datetime('now'), datetime('now')),

-- 系统监控
('105', 'PureMonitor', '/monitor', 0, 11, 1, '1', datetime('now'), datetime('now')),

-- 登录日志
('106', 'LoginLog', '/monitor/login-logs', 1, 1, 1, '1', datetime('now'), datetime('now')),

-- 操作日志
('107', 'OperationLog', '/monitor/operation-logs', 1, 2, 1, '1', datetime('now'), datetime('now')),

-- 系统日志
('108', 'SystemLog', '/monitor/system-logs', 1, 3, 1, '1', datetime('now'), datetime('now'));

-- 插入角色菜单关联（管理员拥有所有权限）
INSERT OR IGNORE INTO system_userrole_menu (userrole_id, menu_id) VALUES
-- 管理员权限
('1', '100'), ('1', '101'), ('1', '102'), ('1', '103'), ('1', '104'),
('1', '105'), ('1', '106'), ('1', '107'), ('1', '108'),

-- 普通用户权限
('2', '100'), ('2', '101'), ('2', '105'), ('2', '108');