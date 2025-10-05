-- 禁用外键检查（SQLite中用于避免创建表时的约束问题）
PRAGMA foreign_keys = OFF;

-- 删除并创建部门表
DROP TABLE IF EXISTS system_deptinfo;
CREATE TABLE system_deptinfo (
  mode_type INTEGER NOT NULL,
  id TEXT NOT NULL PRIMARY KEY,
  created_time TEXT NOT NULL,
  updated_time TEXT NOT NULL,
  description TEXT,
  name TEXT NOT NULL,
  code TEXT NOT NULL UNIQUE,
  rank INTEGER NOT NULL,
  auto_bind INTEGER NOT NULL,
  is_active INTEGER NOT NULL,
  creator_id TEXT,
  dept_belong_id TEXT,
  modifier_id TEXT,
  parent_id TEXT,
  FOREIGN KEY (creator_id) REFERENCES system_userinfo (id),
  FOREIGN KEY (dept_belong_id) REFERENCES system_deptinfo (id),
  FOREIGN KEY (modifier_id) REFERENCES system_userinfo (id),
  FOREIGN KEY (parent_id) REFERENCES system_deptinfo (id)
);

-- 删除并创建用户表
DROP TABLE IF EXISTS system_userinfo;
CREATE TABLE system_userinfo (
  id TEXT NOT NULL PRIMARY KEY,
  password TEXT NOT NULL,
  last_login TEXT,
  is_superuser INTEGER NOT NULL,
  username TEXT NOT NULL UNIQUE,
  first_name TEXT NOT NULL,
  last_name TEXT NOT NULL,
  is_staff INTEGER NOT NULL,
  is_active INTEGER NOT NULL,
  date_joined TEXT NOT NULL,
  mode_type INTEGER NOT NULL,
  created_time TEXT NOT NULL,
  updated_time TEXT NOT NULL,
  description TEXT,
  avatar TEXT,
  nickname TEXT NOT NULL,
  gender INTEGER NOT NULL,
  phone TEXT NOT NULL,
  email TEXT NOT NULL,
  creator_id TEXT,
  modifier_id TEXT,
  dept_id TEXT,
  dept_belong_id TEXT,
  FOREIGN KEY (creator_id) REFERENCES system_userinfo (id),
  FOREIGN KEY (modifier_id) REFERENCES system_userinfo (id),
  FOREIGN KEY (dept_id) REFERENCES system_deptinfo (id),
  FOREIGN KEY (dept_belong_id) REFERENCES system_deptinfo (id)
);

-- 删除并创建角色表
DROP TABLE IF EXISTS system_userrole;
CREATE TABLE system_userrole (
  id TEXT NOT NULL PRIMARY KEY,
  created_time TEXT NOT NULL,
  updated_time TEXT NOT NULL,
  description TEXT,
  name TEXT NOT NULL UNIQUE,
  code TEXT NOT NULL UNIQUE,
  is_active INTEGER NOT NULL,
  creator_id TEXT,
  dept_belong_id TEXT,
  modifier_id TEXT,
  FOREIGN KEY (creator_id) REFERENCES system_userinfo (id),
  FOREIGN KEY (dept_belong_id) REFERENCES system_deptinfo (id),
  FOREIGN KEY (modifier_id) REFERENCES system_userinfo (id)
);

-- 删除并创建用户角色关联表
DROP TABLE IF EXISTS system_userinfo_roles;
CREATE TABLE system_userinfo_roles (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  userinfo_id TEXT NOT NULL,
  userrole_id TEXT NOT NULL,
  FOREIGN KEY (userinfo_id) REFERENCES system_userinfo (id),
  FOREIGN KEY (userrole_id) REFERENCES system_userrole (id)
);

-- 删除并创建菜单元数据表
DROP TABLE IF EXISTS system_menumeta;
CREATE TABLE system_menumeta (
  id TEXT NOT NULL PRIMARY KEY,
  created_time TEXT NOT NULL,
  updated_time TEXT NOT NULL,
  description TEXT,
  title TEXT,
  icon TEXT,
  r_svg_name TEXT,
  is_show_menu INTEGER NOT NULL,
  is_show_parent INTEGER NOT NULL,
  is_keepalive INTEGER NOT NULL,
  frame_url TEXT,
  frame_loading INTEGER NOT NULL,
  transition_enter TEXT,
  transition_leave TEXT,
  is_hidden_tag INTEGER NOT NULL,
  fixed_tag INTEGER NOT NULL,
  dynamic_level INTEGER NOT NULL,
  creator_id TEXT,
  dept_belong_id TEXT,
  modifier_id TEXT,
  FOREIGN KEY (creator_id) REFERENCES system_userinfo (id),
  FOREIGN KEY (dept_belong_id) REFERENCES system_deptinfo (id),
  FOREIGN KEY (modifier_id) REFERENCES system_userinfo (id)
);

-- 删除并创建菜单表
DROP TABLE IF EXISTS system_menu;
CREATE TABLE system_menu (
  id TEXT NOT NULL PRIMARY KEY,
  created_time TEXT NOT NULL,
  updated_time TEXT NOT NULL,
  description TEXT,
  menu_type INTEGER NOT NULL,
  name TEXT NOT NULL UNIQUE,
  rank INTEGER NOT NULL,
  path TEXT NOT NULL,
  component TEXT,
  is_active INTEGER NOT NULL,
  method TEXT,
  creator_id TEXT,
  dept_belong_id TEXT,
  modifier_id TEXT,
  parent_id TEXT,
  meta_id TEXT NOT NULL,
  FOREIGN KEY (creator_id) REFERENCES system_userinfo (id),
  FOREIGN KEY (dept_belong_id) REFERENCES system_deptinfo (id),
  FOREIGN KEY (modifier_id) REFERENCES system_userinfo (id),
  FOREIGN KEY (parent_id) REFERENCES system_menu (id),
  FOREIGN KEY (meta_id) REFERENCES system_menumeta (id)
);

-- 删除并创建角色菜单关联表
DROP TABLE IF EXISTS system_userrole_menu;
CREATE TABLE system_userrole_menu (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  userrole_id TEXT NOT NULL,
  menu_id TEXT NOT NULL,
  FOREIGN KEY (userrole_id) REFERENCES system_userrole (id),
  FOREIGN KEY (menu_id) REFERENCES system_menu (id)
);

-- 删除并创建用户会话表
DROP TABLE IF EXISTS user_sessions;
CREATE TABLE user_sessions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id TEXT NOT NULL,
  session_id TEXT NOT NULL UNIQUE,
  access_token TEXT NOT NULL,
  refresh_token TEXT,
  ip_address TEXT,
  user_agent TEXT,
  device_info TEXT,
  location TEXT,
  is_active INTEGER,
  expires_at TEXT NOT NULL,
  last_activity_at TEXT,
  created_at TEXT,
  FOREIGN KEY (user_id) REFERENCES system_userinfo (id)
);

-- 删除并创建用户资料表
DROP TABLE IF EXISTS user_profiles;
CREATE TABLE user_profiles (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id TEXT NOT NULL UNIQUE,
  real_name TEXT,
  id_card TEXT,
  birthday TEXT,
  address TEXT,
  emergency_contact TEXT,
  emergency_phone TEXT,
  job_title TEXT,
  entry_date TEXT,
  work_location TEXT,
  supervisor_id TEXT,
  preferences TEXT,
  created_at TEXT,
  updated_at TEXT,
  FOREIGN KEY (user_id) REFERENCES system_userinfo (id),
  FOREIGN KEY (supervisor_id) REFERENCES system_userinfo (id)
);

-- 删除并创建登录日志表
DROP TABLE IF EXISTS system_userloginlog;
CREATE TABLE system_userloginlog (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  created_time TEXT NOT NULL,
  updated_time TEXT NOT NULL,
  description TEXT,
  status INTEGER NOT NULL,
  ipaddress TEXT,
  browser TEXT,
  system TEXT,
  agent TEXT,
  login_type INTEGER NOT NULL,
  creator_id TEXT,
  dept_belong_id TEXT,
  modifier_id TEXT,
  FOREIGN KEY (creator_id) REFERENCES system_userinfo (id),
  FOREIGN KEY (dept_belong_id) REFERENCES system_deptinfo (id),
  FOREIGN KEY (modifier_id) REFERENCES system_userinfo (id)
);

-- 删除并创建操作日志表
DROP TABLE IF EXISTS system_operationlog;
CREATE TABLE system_operationlog (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  created_time TEXT NOT NULL,
  updated_time TEXT NOT NULL,
  description TEXT,
  module TEXT,
  path TEXT,
  body TEXT,
  method TEXT,
  ipaddress TEXT,
  browser TEXT,
  system TEXT,
  response_code INTEGER,
  response_result TEXT,
  status_code INTEGER,
  creator_id TEXT,
  dept_belong_id TEXT,
  modifier_id TEXT,
  FOREIGN KEY (creator_id) REFERENCES system_userinfo (id),
  FOREIGN KEY (dept_belong_id) REFERENCES system_deptinfo (id),
  FOREIGN KEY (modifier_id) REFERENCES system_userinfo (id)
);

-- 删除并创建系统配置表
DROP TABLE IF EXISTS system_systemconfig;
CREATE TABLE system_systemconfig (
  id TEXT NOT NULL PRIMARY KEY,
  created_time TEXT NOT NULL,
  updated_time TEXT NOT NULL,
  description TEXT,
  value TEXT NOT NULL,
  is_active INTEGER NOT NULL,
  access INTEGER NOT NULL,
  key TEXT NOT NULL UNIQUE,
  inherit INTEGER NOT NULL,
  creator_id TEXT,
  dept_belong_id TEXT,
  modifier_id TEXT,
  FOREIGN KEY (creator_id) REFERENCES system_userinfo (id),
  FOREIGN KEY (dept_belong_id) REFERENCES system_deptinfo (id),
  FOREIGN KEY (modifier_id) REFERENCES system_userinfo (id)
);