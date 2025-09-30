-- 插入部门数据
INSERT OR IGNORE INTO departments (id, parent_id, name, code, leader, phone, email, status, sort) VALUES
(103, 0, '研发部门', 'dev', '张三', '13800138000', 'dev@example.com', 1, 1),
(105, 0, '测试部门', 'test', '李四', '13800138001', 'test@example.com', 1, 2);

-- 插入角色数据
INSERT OR IGNORE INTO roles (id, name, code, status, remark) VALUES
(1, '超级管理员', 'admin', 1, '超级管理员拥有最高权限'),
(2, '普通角色', 'common', 1, '普通角色拥有部分权限');

-- 插入用户数据（密码：admin123 和 common123 的bcrypt哈希）
INSERT OR IGNORE INTO users (id, username, nickname, email, phone, avatar, password_hash, description, sex, status, dept_id, remark) VALUES
(1, 'admin', '小铭', 'admin@example.com', '15888886789', 'https://avatars.githubusercontent.com/u/44761321', '$2b$12$9jKr.Vk5XJ5I5J5J5J5J5OqCJ5J5J5J5J5J5J5J5J5J5J5J5J5J5J', '系统管理员', 1, 1, 103, '管理员账户'),
(2, 'common', '小林', 'common@example.com', '18288882345', 'https://avatars.githubusercontent.com/u/52823142', '$2b$12$9jKr.Vk5XJ5I5J5J5J5J5OqCJ5J5J5J5J5J5J5J5J5J5J5J5J5J5J', '普通用户', 2, 1, 105, '普通用户账户');

-- 插入用户角色关联
INSERT OR IGNORE INTO user_roles (user_id, role_id) VALUES
(1, 1), -- admin -> 超级管理员
(2, 2); -- common -> 普通角色

-- 插入菜单数据
INSERT OR IGNORE INTO menus (id, parent_id, title, name, path, component, menu_type, rank, redirect, icon, extra_icon, enter_transition, leave_transition, active_path, auths, frame_src, frame_loading, keep_alive, hidden_tag, fixed_tag, show_link, show_parent) VALUES
-- 外部页面
(100, 0, 'menus.pureExternalPage', 'PureIframe', '/iframe', '', 0, 7, '', 'ri:links-fill', '', '', '', '', '', '', 1, 0, 0, 0, 1, 0),
(101, 100, 'menus.pureExternalDoc', 'PureIframeExternal', '/iframe/external', '', 0, NULL, '', '', '', '', '', '', '', '', 1, 0, 0, 0, 1, 0),
(102, 101, 'menus.pureExternalLink', 'https://pure-admin.cn/', '/external', '', 2, NULL, '', '', '', '', '', '', '', '', 1, 0, 0, 0, 1, 0),
(103, 101, 'menus.pureUtilsLink', 'https://pure-admin-utils.netlify.app/', '/pureUtilsLink', '', 2, NULL, '', '', '', '', '', '', '', '', 1, 0, 0, 0, 1, 0),
(104, 100, 'menus.pureEmbeddedDoc', 'PureIframeEmbedded', '/iframe/embedded', '', 1, NULL, '', '', '', '', '', '', '', '', 1, 0, 0, 0, 1, 0),
(105, 104, 'menus.pureEpDoc', 'FrameEp', '/iframe/ep', '', 1, NULL, '', '', '', '', '', '', '', 'https://element-plus.org/zh-CN/', 1, 1, 0, 0, 1, 0),

-- 权限管理
(200, 0, 'menus.purePermission', 'PurePermission', '/permission', '', 0, 9, '', 'ep:lollipop', '', '', '', '', '', '', 1, 0, 0, 0, 1, 0),
(201, 200, 'menus.purePermissionPage', 'PermissionPage', '/permission/page/index', '', 0, NULL, '', '', '', '', '', '', '', '', 1, 0, 0, 0, 1, 0),
(202, 200, 'menus.purePermissionButton', 'PermissionButton', '/permission/button', '', 0, NULL, '', '', '', '', '', '', '', '', 1, 0, 0, 0, 1, 0),
(203, 202, '添加', '', '', '', 3, NULL, '', '', '', '', '', '', 'permission:btn:add', '', 1, 0, 0, 0, 1, 0),
(204, 202, '修改', '', '', '', 3, NULL, '', '', '', '', '', '', 'permission:btn:edit', '', 1, 0, 0, 0, 1, 0),
(205, 202, '删除', '', '', '', 3, NULL, '', '', '', '', '', '', 'permission:btn:delete', '', 1, 0, 0, 0, 1, 0),

-- 系统管理
(300, 0, 'menus.pureSysManagement', 'PureSystem', '/system', '', 0, 10, '', 'ri:settings-3-line', '', '', '', '', '', '', 1, 0, 0, 0, 1, 0),
(301, 300, 'menus.pureUser', 'SystemUser', '/system/user/index', '', 0, NULL, '', 'ri:admin-line', '', '', '', '', '', '', 1, 0, 0, 0, 1, 0),
(302, 300, 'menus.pureRole', 'SystemRole', '/system/role/index', '', 0, NULL, '', 'ri:admin-fill', '', '', '', '', '', '', 1, 0, 0, 0, 1, 0),
(303, 300, 'menus.pureSystemMenu', 'SystemMenu', '/system/menu/index', '', 0, NULL, '', 'ep:menu', '', '', '', '', '', '', 1, 0, 0, 0, 1, 0),
(304, 300, 'menus.pureDept', 'SystemDept', '/system/dept/index', '', 0, NULL, '', 'ri:git-branch-line', '', '', '', '', '', '', 1, 0, 0, 0, 1, 0),

-- 系统监控
(400, 0, 'menus.pureSysMonitor', 'PureMonitor', '/monitor', '', 0, 11, '', 'ep:monitor', '', '', '', '', '', '', 1, 0, 0, 0, 1, 0),
(401, 400, 'menus.pureOnlineUser', 'OnlineUser', '/monitor/online-user', '', 0, NULL, '', 'ri:user-voice-line', '', '', '', '', '', '', 1, 0, 0, 0, 1, 0),
(402, 400, 'menus.pureLoginLog', 'LoginLog', '/monitor/login-logs', '', 0, NULL, '', 'ri:window-line', '', '', '', '', '', '', 1, 0, 0, 0, 1, 0),
(403, 400, 'menus.pureOperationLog', 'OperationLog', '/monitor/operation-logs', '', 0, NULL, '', 'ri:history-fill', '', '', '', '', '', '', 1, 0, 0, 0, 1, 0),
(404, 400, 'menus.pureSystemLog', 'SystemLog', '/monitor/system-logs', '', 0, NULL, '', 'ri:file-search-line', '', '', '', '', '', '', 1, 0, 0, 0, 1, 0),

-- 标签页操作
(500, 0, 'menus.pureTabs', 'PureTabs', '/tabs', '', 0, 12, '', 'ri:bookmark-2-line', '', '', '', '', '', '', 1, 0, 0, 0, 1, 0),
(501, 500, 'menus.pureTabs', 'Tabs', '/tabs/index', '', 0, NULL, '', '', '', '', '', '', '', '', 1, 0, 0, 0, 1, 0);

-- 插入角色菜单关联（管理员拥有所有权限）
INSERT OR IGNORE INTO role_menus (role_id, menu_id) VALUES
-- 管理员权限
(1, 100), (1, 101), (1, 102), (1, 103), (1, 104), (1, 105),
(1, 200), (1, 201), (1, 202), (1, 203), (1, 204), (1, 205),
(1, 300), (1, 301), (1, 302), (1, 303), (1, 304),
(1, 400), (1, 401), (1, 402), (1, 403), (1, 404),
(1, 500), (1, 501),

-- 普通用户权限
(2, 100), (2, 101), (2, 102), (2, 103), (2, 104), (2, 105),
(2, 200), (2, 201), (2, 404), (2, 500), (2, 501);