# Vue Pure Admin Service

基于 **FastAPI + SQLAlchemy + SQLite/MySQL** 的现代化后端API服务，采用 **DDD（领域驱动设计）** 架构模式，为 Vue Pure Admin 前端项目提供完整的RESTful API支持。

## 🚀 最新特性

- ✅ **现代化架构**: 基于FastAPI + SQLAlchemy + DDD架构
- ✅ **完整的RBAC权限**: 用户、角色、菜单、部门管理
- ✅ **JWT认证授权**: 基于JWT的安全认证和权限控制
- ✅ **数据库管理**: 完整的数据库初始化、备份、恢复工具
- ✅ **日志审计**: 登录日志、操作日志、系统日志、安全审计
- ✅ **单元测试**: 覆盖率超过65%的完整测试体系
- ✅ **自动化脚本**: 一键启动、数据库管理、环境配置
- ✅ **容器化部署**: Docker + docker-compose 支持
- ✅ **API文档**: 自动生成的Swagger/OpenAPI文档

## 📁 项目结构

```
service/
├── app/                     # 应用核心代码（DDD架构）
│   ├── application/         # 应用层
│   │   ├── dto/            # 数据传输对象
│   │   ├── interfaces/     # 应用接口
│   │   ├── services/       # 应用服务
│   │   └── __init__.py
│   ├── domain/             # 领域层
│   │   ├── audit/          # 审计日志领域
│   │   ├── entities/       # 实体模型
│   │   ├── menu/           # 菜单领域
│   │   ├── models/         # 领域模型
│   │   ├── organization/   # 组织领域
│   │   ├── repositories/   # 仓储接口
│   │   ├── role/           # 角色领域
│   │   ├── services/       # 领域服务
│   │   ├── user/           # 用户领域
│   │   └── __init__.py
│   ├── infrastructure/     # 基础设施层
│   │   ├── auth/           # 认证服务
│   │   ├── database/       # 数据库配置
│   │   ├── persistence/    # 数据持久化
│   │   ├── utils/          # 工具类
│   │   └── __init__.py
│   ├── presentation/       # 表示层（接口层）
│   │   ├── api/            # API路由
│   │   ├── dto/            # 接口数据对象
│   │   ├── middleware/     # 中间件
│   │   ├── schemas/        # 请求/响应模式
│   │   └── __init__.py
│   ├── config.py           # 应用配置
│   └── __init__.py
├── db/                      # 数据库文件和初始化脚本
│   ├── init/               # SQL初始化脚本
│   │   ├── 01_create_tables.sql      # 创建表结构（MySQL）
│   │   ├── 01_create_tables_sqlite.sql # 创建表结构（SQLite）
│   │   ├── 02_insert_data.sql        # 插入初始数据
│   │   ├── 03_create_indexes.sql     # 创建索引
│   │   └── 04_rbac_tables.sql        # RBAC权限表
│   ├── backup/             # 数据库备份文件
│   ├── migrations/         # 数据库迁移文件
│   └── vue_pure_admin.db   # SQLite数据库文件
├── docs/                    # 项目文档
│   ├── API_DOCUMENTATION.md        # API文档
│   ├── DATABASE.md                 # 数据库配置说明
│   ├── DDD_RBAC_ARCHITECTURE.md    # DDD架构设计
│   ├── DOCKER.md                   # Docker使用说明
│   ├── PROJECT_STRUCTURE.md        # 项目结构详解
│   ├── REST_API_SPECIFICATION.md   # REST API规范
│   └── refactor.md                 # 重构文档
├── scripts/                 # 各类管理脚本
│   ├── database/           # 数据库管理脚本
│   │   ├── db_manager.bat/.sh      # 数据库管理工具
│   │   ├── setup_database.bat/.sh  # 数据库初始化脚本
│   │   └── update_passwords.py     # 密码更新工具
│   ├── docker/             # Docker配置文件
│   │   ├── Dockerfile              # Docker镜像配置
│   │   └── docker-compose.yml      # Docker编排配置
│   └── environment/        # 环境管理脚本
│       ├── check_venv.bat/.sh      # 虚拟环境检查
│       └── setup_venv.bat/.sh      # 虚拟环境设置
├── shared/                  # 共享核心组件
│   ├── kernel/             # 核心配置和工具
│   │   ├── config.py       # 共享配置
│   │   ├── dependencies.py # 依赖注入
│   │   ├── exceptions.py   # 异常处理
│   │   └── __init__.py
│   └── utils/              # 通用工具类
├── tests/                   # 完整测试套件
│   ├── application/        # 应用层测试
│   ├── domain/             # 领域层测试
│   ├── fixtures/           # 测试固件
│   ├── infrastructure/     # 基础设施层测试
│   ├── presentation/       # 表示层测试
│   ├── reports/            # 测试报告
│   ├── utils/              # 测试工具
│   ├── conftest.py         # pytest配置
│   ├── requirements.txt    # 测试依赖
│   ├── run_tests.py        # 测试运行脚本
│   └── __init__.py
├── logs/                    # 日志文件目录
├── main.py                  # 应用入口文件
├── start.bat/.sh           # 一键启动脚本
├── requirements.txt         # Python依赖包
├── pyproject.toml          # 项目配置文件
└── pytest.ini              # pytest配置文件
```

## 🛠 技术栈

- **Web框架**: FastAPI 0.104+
- **数据库**: SQLite（默认）/ MySQL（可选）+ SQLAlchemy 2.0+
- **缓存**: Redis（可选）
- **身份认证**: JWT + bcrypt 密码加密
- **容器化**: Docker + docker-compose
- **架构模式**: DDD (领域驱动设计)
- **日志系统**: loguru + 结构化日志
- **测试框架**: pytest + 覆盖率测试
- **代码质量**: 类型注解 + 依赖注入

## ⭐ 功能特性

### 核心功能
- ✅ **用户认证与授权** - JWT + bcrypt 安全认证
- ✅ **RBAC权限管理** - 用户/角色/权限精细化控制
- ✅ **用户管理** - 用户CRUD、状态管理、密码策略
- ✅ **角色管理** - 角色分配、权限继承
- ✅ **菜单管理** - 动态菜单、权限控制
- ✅ **部门管理** - 组织架构、职位管理

### 监控审计
- ✅ **在线用户监控** - 实时在线用户状态
- ✅ **登录日志** - 登录记录、IP地理位置
- ✅ **操作日志** - 用户操作审计跟踪
- ✅ **系统日志** - 系统运行日志
- ✅ **安全审计** - 安全事件监控

### 开发运维
- ✅ **数据库管理工具** - 初始化、备份、恢复
- ✅ **自动化脚本** - 一键启动、环境检查
- ✅ **API文档** - 自动生成Swagger文档
- ✅ **单元测试** - 完整测试覆盖
- ✅ **Docker部署** - 容器化一键部署
- ✅ **虚拟环境管理** - 自动化虚拟环境设置

## 🚀 快速开始

### 方式一：一键启动（推荐）

#### 前置要求
- **Python 3.8+**（推荐 3.11+）
- **SQLite**（内置）或 **MySQL 8.0+**（可选）
- **Redis**（可选，用于缓存）

#### 🎯 一键启动
使用自动化脚本，自动处理环境配置、依赖安装、数据库初始化：

```bash
# Windows 用户
start.bat

# Linux/Mac 用户  
chmod +x start.sh
./start.sh
```

启动脚本会自动完成：
- ✅ 检查 Python 环境
- ✅ 创建虚拟环境
- ✅ 安装项目依赖
- ✅ 创建环境配置文件
- ✅ 初始化数据库
- ✅ 启动 FastAPI 服务

### 方式二：手动安装（开发者模式）

```bash
# 1. 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

# 2. 安装依赖
pip install -r requirements.txt

# 3. 配置环境
cp .env.example .env

# 4. 初始化数据库
scripts/database/db_manager.sh init  # Linux/Mac
# scripts\database\db_manager.bat init  # Windows

# 5. 启动服务
python main.py
```

### 方式三：Docker 容器化部署

```bash
# 1. 切换到 Docker 目录
cd scripts/docker

# 2. 启动所有服务
docker-compose up -d

# 3. 查看服务状态
docker-compose ps

# 4. 查看日志
docker-compose logs -f app
```

## 🔐 默认账户

数据库初始化完成后，系统会自动创建以下测试账户：

| 用户名 | 密码 | 角色 | 权限说明 |
|--------|------|------|----------|
| **admin** | **admin123** | 超级管理员 | 拥有所有系统权限 |
| **common** | **common123** | 普通用户 | 基础功能权限 |

> ⚠️ **安全提醒**: 生产环境部署时请务必修改默认密码！

## 📚 API文档

服务启动后，可通过以下地址访问自动生成的API文档：

- **🎯 Swagger UI**: http://localhost:8000/docs
- **📖 ReDoc**: http://localhost:8000/redoc
- **🏠 服务首页**: http://localhost:8000/
- **💚 健康检查**: http://localhost:8000/health

## 主要API端点

### 认证相关
- `POST /auth/login` - 用户登录
- `POST /auth/refresh` - 刷新令牌
- `GET /auth/me` - 获取当前用户信息
- `GET /auth/logs` - 获取用户安全日志

### 系统管理
- `GET /users` - 获取用户列表
- `POST /users` - 创建用户
- `PUT /users/{id}` - 更新用户
- `DELETE /users/{id}` - 删除用户
- `GET /roles` - 获取角色列表
- `POST /roles` - 创建角色
- `GET /menus` - 获取菜单列表
- `POST /menus` - 创建菜单
- `GET /depts` - 获取部门列表
- `POST /depts` - 创建部门

### 系统监控
- `GET /monitor/online` - 获取在线用户
- `GET /monitor/login-logs` - 获取登录日志
- `GET /monitor/operation-logs` - 获取操作日志
- `GET /monitor/system-logs` - 获取系统日志

### 其他
- `GET /routes` - 获取动态路由
- `POST /dashboard/card-list` - 获取卡片列表
- `GET /health` - 健康检查

## 📊 数据库管理工具

项目提供了完整的数据库管理脚本：

```bash
# Windows
scripts\database\db_manager.bat [command]

# Linux/Mac
./scripts/database/db_manager.sh [command]
```

**可用命令：**
- `init` - 初始化数据库（创建表和默认数据）
- `backup` - 备份数据库到压缩文件
- `restore` - 从备份文件恢复数据库
- `reset` - 重置数据库（危险操作）
- `info` - 显示数据库状态信息
- `password` - 更新用户密码

## ⚙️ 环境配置

主要配置项（`.env` 文件）：

```env
# 🚀 应用配置
APP_NAME=XAdmin FastAPI RBAC System
DEBUG=True
PORT=8000

# 🗄️ 数据库
DATABASE_URL=sqlite:///./db/vue_pure_admin.db
# DATABASE_URL=mysql+pymysql://user:pass@localhost:3306/db

# 🔒 JWT 安全
JWT_SECRET_KEY=your-super-secret-key
JWT_EXPIRE_MINUTES=30

# 🌐 CORS
ALLOWED_ORIGINS=["http://localhost:3000","http://localhost:5173"]

# 📦 Redis（可选）
REDIS_URL=redis://localhost:6379/0
```

## 📖 文档指南

- **[docs/PROJECT_STRUCTURE.md](docs/PROJECT_STRUCTURE.md)** - 📁 项目结构详解
- **[docs/DDD_RBAC_ARCHITECTURE.md](docs/DDD_RBAC_ARCHITECTURE.md)** - 🏗️ DDD架构设计
- **[docs/DATABASE.md](docs/DATABASE.md)** - 🗄️ 数据库配置指南
- **[docs/DOCKER.md](docs/DOCKER.md)** - 🐳 Docker部署说明
- **[docs/API_DOCUMENTATION.md](docs/API_DOCUMENTATION.md)** - 📘 API文档
- **[docs/REST_API_SPECIFICATION.md](docs/REST_API_SPECIFICATION.md)** - 📗 REST API规范

## 📝 开发指南

### 测试运行
```bash
# 运行所有测试
python -m pytest tests/

# 覆盖率报告
python tests/run_tests.py
```

### 环境管理脚本
```bash
# 检查虚拟环境（Windows）
scripts\environment\check_venv.bat

# 设置虚拟环境（Windows）
scripts\environment\setup_venv.bat

# 检查虚拟环境（Linux/Mac）
./scripts/environment/check_venv.sh

# 设置虚拟环境（Linux/Mac）
./scripts/environment/setup_venv.sh
```

### 生产部署建议
1. **安全配置** - 修改默认密码、使用强密码的JWT密钥
2. **数据库** - 使用MySQL或PostgreSQL
3. **监控日志** - 配置日志收集和监控
4. **性能优化** - 使用Nginx反向代理、配置Redis缓存

## 🤝 贡献指南

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 📜 许可证

MIT License - 查看 [LICENSE](LICENSE) 文件了解详情