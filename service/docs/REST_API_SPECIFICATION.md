# REST API 接口规范

## 概述

本文档定义了Vue Pure Admin后端服务的REST API接口规范，严格按照RESTful架构风格设计，为所有数据表提供标准的CRUD操作。

## 设计原则

1. **资源导向**: 每个API端点代表一个资源
2. **统一接口**: 使用标准HTTP方法(GET, POST, PUT, DELETE)
3. **状态无关**: 每个请求包含完整的处理信息
4. **分层系统**: 清晰的分层架构
5. **缓存性**: 响应可缓存以提高性能

## HTTP状态码规范

- `200 OK`: 请求成功
- `201 Created`: 资源创建成功
- `204 No Content`: 请求成功但无返回内容
- `400 Bad Request`: 请求参数错误
- `401 Unauthorized`: 未授权
- `403 Forbidden`: 禁止访问
- `404 Not Found`: 资源不存在
- `409 Conflict`: 资源冲突
- `422 Unprocessable Entity`: 验证失败
- `500 Internal Server Error`: 服务器内部错误

## 响应格式规范

所有API响应统一使用以下格式：

```json
{
  "success": boolean,
  "message": string,
  "data": object|array,
  "errors": array
}
```

## 分页规范

列表查询接口统一使用以下分页格式：

**请求参数:**
- `page`: 页码，从1开始
- `page_size`: 每页记录数，默认10

**响应格式:**
```json
{
  "success": true,
  "data": {
    "items": [],
    "total": 100,
    "page": 1,
    "page_size": 10,
    "pages": 10
  }
}
```

## API端点设计

### 1. 用户管理 (Users)

| 方法 | 端点 | 描述 | 参数 |
|------|------|------|------|
| GET | `/api/users` | 获取用户列表 | page, page_size, username, status, dept_id |
| GET | `/api/users/{id}` | 获取用户详情 | - |
| POST | `/api/users` | 创建用户 | UserCreate |
| PUT | `/api/users/{id}` | 更新用户 | UserUpdate |
| DELETE | `/api/users/{id}` | 删除用户 | - |
| PUT | `/api/users/{id}/status` | 更新用户状态 | status |
| PUT | `/api/users/{id}/password` | 重置用户密码 | password |

### 2. 角色管理 (Roles)

| 方法 | 端点 | 描述 | 参数 |
|------|------|------|------|
| GET | `/api/roles` | 获取角色列表 | page, page_size, name, code, status |
| GET | `/api/roles/{id}` | 获取角色详情 | - |
| POST | `/api/roles` | 创建角色 | RoleCreate |
| PUT | `/api/roles/{id}` | 更新角色 | RoleUpdate |
| DELETE | `/api/roles/{id}` | 删除角色 | - |
| PUT | `/api/roles/{id}/status` | 更新角色状态 | status |

### 3. 菜单管理 (Menus)

| 方法 | 端点 | 描述 | 参数 |
|------|------|------|------|
| GET | `/api/menus` | 获取菜单列表 | page, page_size, title, menu_type |
| GET | `/api/menus/{id}` | 获取菜单详情 | - |
| POST | `/api/menus` | 创建菜单 | MenuCreate |
| PUT | `/api/menus/{id}` | 更新菜单 | MenuUpdate |
| DELETE | `/api/menus/{id}` | 删除菜单 | - |
| GET | `/api/menus/tree` | 获取菜单树 | - |

### 4. 部门管理 (Departments)

| 方法 | 端点 | 描述 | 参数 |
|------|------|------|------|
| GET | `/api/departments` | 获取部门列表 | page, page_size, name, status |
| GET | `/api/departments/{id}` | 获取部门详情 | - |
| POST | `/api/departments` | 创建部门 | DepartmentCreate |
| PUT | `/api/departments/{id}` | 更新部门 | DepartmentUpdate |
| DELETE | `/api/departments/{id}` | 删除部门 | - |
| GET | `/api/departments/tree` | 获取部门树 | - |
| PUT | `/api/departments/{id}/status` | 更新部门状态 | status |

### 5. 用户角色关联 (UserRoles)

| 方法 | 端点 | 描述 | 参数 |
|------|------|------|------|
| GET | `/api/users/{user_id}/roles` | 获取用户角色列表 | - |
| POST | `/api/users/{user_id}/roles` | 分配角色给用户 | role_ids |
| DELETE | `/api/users/{user_id}/roles/{role_id}` | 移除用户角色 | - |
| PUT | `/api/users/{user_id}/roles` | 更新用户角色 | role_ids |

### 6. 角色菜单关联 (RoleMenus)

| 方法 | 端点 | 描述 | 参数 |
|------|------|------|------|
| GET | `/api/roles/{role_id}/menus` | 获取角色菜单列表 | - |
| POST | `/api/roles/{role_id}/menus` | 分配菜单给角色 | menu_ids |
| DELETE | `/api/roles/{role_id}/menus/{menu_id}` | 移除角色菜单 | - |
| PUT | `/api/roles/{role_id}/menus` | 更新角色菜单 | menu_ids |

### 7. 登录日志 (LoginLogs)

| 方法 | 端点 | 描述 | 参数 |
|------|------|------|------|
| GET | `/api/login-logs` | 获取登录日志列表 | page, page_size, username, status, start_time, end_time |
| GET | `/api/login-logs/{id}` | 获取登录日志详情 | - |
| DELETE | `/api/login-logs/{id}` | 删除登录日志 | - |
| POST | `/api/login-logs/clean` | 清理登录日志 | days |

### 8. 操作日志 (OperationLogs)

| 方法 | 端点 | 描述 | 参数 |
|------|------|------|------|
| GET | `/api/operation-logs` | 获取操作日志列表 | page, page_size, username, module, start_time, end_time |
| GET | `/api/operation-logs/{id}` | 获取操作日志详情 | - |
| DELETE | `/api/operation-logs/{id}` | 删除操作日志 | - |
| POST | `/api/operation-logs/clean` | 清理操作日志 | days |

### 9. 系统日志 (SystemLogs)

| 方法 | 端点 | 描述 | 参数 |
|------|------|------|------|
| GET | `/api/system-logs` | 获取系统日志列表 | page, page_size, level, module, start_time, end_time |
| GET | `/api/system-logs/{id}` | 获取系统日志详情 | - |
| DELETE | `/api/system-logs/{id}` | 删除系统日志 | - |
| POST | `/api/system-logs/clean` | 清理系统日志 | days |

### 10. 在线用户 (OnlineUsers)

| 方法 | 端点 | 描述 | 参数 |
|------|------|------|------|
| GET | `/api/online-users` | 获取在线用户列表 | page, page_size |
| DELETE | `/api/online-users/{id}` | 强制下线用户 | - |

## 认证与授权

### 认证接口

| 方法 | 端点 | 描述 | 参数 |
|------|------|------|------|
| POST | `/api/auth/login` | 用户登录 | username, password |
| POST | `/api/auth/logout` | 用户登出 | - |
| POST | `/api/auth/refresh` | 刷新令牌 | refresh_token |
| GET | `/api/auth/me` | 获取当前用户信息 | - |
| PUT | `/api/auth/password` | 修改密码 | old_password, new_password |

### 权限验证

所有需要认证的接口都需要在请求头中携带访问令牌：

```
Authorization: Bearer <access_token>
```

## 错误处理

错误响应格式：

```json
{
  "success": false,
  "message": "错误描述",
  "errors": [
    {
      "field": "字段名",
      "message": "字段错误信息"
    }
  ]
}
```

## 数据验证

- 所有输入数据必须经过验证
- 使用Pydantic模型进行数据验证
- 返回详细的验证错误信息

## 性能考虑

- 实现响应缓存
- 使用数据库索引优化查询
- 实现分页避免大量数据传输
- 使用异步处理提高并发性能

## 安全考虑

- 使用HTTPS传输
- 实现JWT令牌认证
- 输入数据防XSS处理
- 实现API访问频率限制
- 敏感数据加密存储

## 版本控制

- API版本通过URL路径标识: `/api/v1/`
- 保持向后兼容性
- 新版本不删除旧版本功能