# API文档

## 概述

本文档描述了系统提供的所有REST API接口。系统基于FastAPI框架构建，提供了完整的RBAC权限管理功能。

## 认证

大部分API需要认证才能访问。系统使用JWT Token进行认证。

### 获取Token

```
POST /api/v1/auth/login
Content-Type: application/json

{
  "username": "admin",
  "password": "admin123"
}
```

响应:
```json
{
  "success": true,
  "message": "登录成功",
  "data": {
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "token_type": "bearer"
  }
}
```

### 使用Token

在需要认证的API请求中，在请求头中添加Authorization字段：

```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

## API列表

### 1. 用户管理 (/api/v1/users)

#### 获取用户列表
```
GET /api/v1/users?page=1&page_size=10
```

#### 获取用户详情
```
GET /api/v1/users/{user_id}
```

#### 创建用户
```
POST /api/v1/users
Content-Type: application/json

{
  "username": "newuser",
  "nickname": "新用户",
  "email": "newuser@example.com",
  "phone": "13800138000",
  "gender": 1,
  "is_active": true
}
```

#### 更新用户
```
PUT /api/v1/users/{user_id}
Content-Type: application/json

{
  "nickname": "更新用户",
  "email": "updated@example.com"
}
```

#### 删除用户
```
DELETE /api/v1/users/{user_id}
```

### 2. 角色管理 (/api/v1/roles)

#### 获取角色列表
```
GET /api/v1/roles?skip=0&limit=100
```

#### 获取角色详情
```
GET /api/v1/roles/{role_id}
```

#### 创建角色
```
POST /api/v1/roles
Content-Type: application/json

{
  "name": "新角色",
  "code": "new_role",
  "description": "新角色描述"
}
```

#### 更新角色
```
PUT /api/v1/roles/{role_id}
Content-Type: application/json

{
  "name": "更新角色",
  "description": "更新角色描述"
}
```

#### 删除角色
```
DELETE /api/v1/roles/{role_id}
```

#### 分配角色菜单
```
PUT /api/v1/roles/{role_id}/menus
Content-Type: application/json

{
  "menu_ids": ["menu_id1", "menu_id2"]
}
```

### 3. 菜单管理 (/api/v1/menus)

#### 获取菜单列表
```
GET /api/v1/menus?page=1&page_size=10
```

#### 获取菜单树
```
GET /api/v1/menus/tree
```

#### 获取菜单详情
```
GET /api/v1/menus/{menu_id}
```

#### 创建菜单
```
POST /api/v1/menus
Content-Type: application/json

{
  "title": "新菜单",
  "name": "NewMenu",
  "path": "/new-menu",
  "menu_type": 1,
  "rank": 1
}
```

#### 更新菜单
```
PUT /api/v1/menus/{menu_id}
Content-Type: application/json

{
  "title": "更新菜单",
  "path": "/updated-menu"
}
```

#### 删除菜单
```
DELETE /api/v1/menus/{menu_id}
```

### 4. 部门管理 (/api/v1/depts)

#### 获取部门列表
```
GET /api/v1/depts?page=1&page_size=10
```

#### 获取部门详情
```
GET /api/v1/depts/{dept_id}
```

#### 创建部门
```
POST /api/v1/depts
Content-Type: application/json

{
  "name": "新部门",
  "code": "new_dept",
  "description": "新部门描述",
  "rank": 1,
  "is_active": true
}
```

#### 更新部门
```
PUT /api/v1/depts/{dept_id}
Content-Type: application/json

{
  "name": "更新部门",
  "description": "更新部门描述"
}
```

#### 删除部门
```
DELETE /api/v1/depts/{dept_id}
```

### 5. 操作日志管理 (/api/v1/operation-logs)

#### 获取操作日志列表
```
GET /api/v1/operation-logs?page=1&page_size=10
```

#### 获取操作日志详情
```
GET /api/v1/operation-logs/{log_id}
```

#### 删除操作日志
```
DELETE /api/v1/operation-logs/{log_id}
```

### 6. 登录日志管理 (/api/v1/login-logs)

#### 获取登录日志列表
```
GET /api/v1/login-logs?page=1&page_size=10
```

#### 获取登录日志详情
```
GET /api/v1/login-logs/{log_id}
```

#### 删除登录日志
```
DELETE /api/v1/login-logs/{log_id}
```

### 7. 系统配置管理 (/api/v1/system-configs)

#### 获取系统配置列表
```
GET /api/v1/system-configs?page=1&page_size=10
```

#### 获取系统配置详情
```
GET /api/v1/system-configs/{config_id}
```

#### 创建系统配置
```
POST /api/v1/system-configs
Content-Type: application/json

{
  "key": "config_key",
  "value": "config_value",
  "description": "配置描述",
  "is_active": true
}
```

#### 更新系统配置
```
PUT /api/v1/system-configs/{config_id}
Content-Type: application/json

{
  "value": "updated_value",
  "description": "更新配置描述"
}
```

#### 删除系统配置
```
DELETE /api/v1/system-configs/{config_id}
```

## 错误处理

API使用标准HTTP状态码表示请求结果：

- 200: 请求成功
- 201: 创建成功
- 204: 删除成功
- 400: 请求参数错误
- 401: 未认证
- 403: 权限不足
- 404: 资源不存在
- 500: 服务器内部错误

错误响应格式:
```json
{
  "detail": "错误信息"
}
```

## 分页

列表接口支持分页参数：

- `page`: 页码，默认为1
- `page_size`: 每页记录数，默认为10，最大100

响应格式:
```json
{
  "success": true,
  "data": {
    "items": [...],
    "total": 100,
    "page": 1,
    "page_size": 10,
    "pages": 10
  }
}
```