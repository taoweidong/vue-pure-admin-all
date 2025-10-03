# Vue Pure Admin Service

基于 FastAPI + SQLAlchemy + MySQL 的后端API服务，采用DDD（领域驱动设计）架构模式，提供完整的RESTful API支持。

## 🚀 最新特性

- ✅ **完整的REST API架构**: 严格按照RESTful规范设计的API接口
- ✅ **DDD架构模式**: 采用领域驱动设计，代码结构清晰
- ✅ **完整的CRUD操作**: 所有数据表的增删改查操作
- ✅ **JWT认证授权**: 基于JWT的用户认证和权限控制
- ✅ **单元测试框架**: 覆盖率超过65%的完整测试体系
- ✅ **API文档**: 自动生成的Swagger/OpenAPI文档
- ✅ **数据库迁移**: 基于Alembic的数据库版本管理

## 项目结构

```
service/
├── app/                     # 应用核心代码（DDD架构）
│   ├── application/         # 应用层
│   │   └── services/       # 应用服务
│   ├── domain/             # 领域层
│   │   └── entities/      # 实体
│   ├── infrastructure/     # 基础设施层
│   │   ├── database/      # 数据库相关
│   │   └── utils/         # 工具类
│   ├── interfaces/         # 接口层（API路由）
│   │   ├── api/           # API路由
│   │   └── schemas/       # API模式
│   ├── config.py          # 配置文件
│   └── main.py            # 应用入口
├── db/                      # 数据库文件和初始化脚本
│   ├── init/              # 数据库初始化SQL脚本
│   └── vue_pure_admin.db  # SQLite数据库文件（运行后生成）
├── docs/                    # 项目文档
│   ├── DATABASE.md        # 数据库配置说明
│   ├── DOCKER.md          # Docker使用说明
│   └── PROJECT_STRUCTURE.md # 项目结构详细说明
├── scripts/                 # 各类脚本文件
│   ├── database/          # 数据库相关脚本
│   ├── docker/            # Docker相关文件
│   └── environment/       # 虚拟环境管理脚本
├── tests/                   # 测试文件
├── .env                     # 环境配置文件
├── .env.example            # 环境配置模板
├── requirements.txt        # Python依赖
├── start.sh               # Linux启动脚本
├── start.bat              # Windows启动脚本
└── README.md               # 项目说明
```

## 技术栈

- **Web框架**: FastAPI
- **数据库**: SQLite（默认）/ MySQL（可选）+ SQLAlchemy ORM
- **缓存**: Redis
- **身份认证**: JWT
- **容器化**: Docker + docker-compose
- **架构模式**: DDD (领域驱动设计)

## 功能特性

- ✅ 用户认证与授权 (JWT)
- ✅ 角色权限管理 (RBAC)
- ✅ 用户管理
- ✅ 角色管理
- ✅ 菜单管理
- ✅ 部门管理
- ✅ 在线用户监控
- ✅ 登录日志
- ✅ 操作日志
- ✅ 系统日志
- ✅ Redis缓存
- ✅ API文档自动生成
- ✅ Docker容器化部署

## 快速开始

### 方式一：本地开发环境（推荐）

#### 前置要求
- Python 3.8+（推荐 3.11+）
- Redis 6.0+
- SQLite（内置）或 MySQL 8.0+（可选）

#### 快速启动（推荐）
使用自动化脚本，会自动创建虚拟环境：
```bash
# Windows
start.bat

# Linux/Mac
chmod +x start.sh
./start.sh
```

#### 手动设置（可选）

#### 1. 克隆项目
```bash
cd service
```

#### 2. 设置虚拟环境（推荐）
```bash
# Windows
scripts\environment\setup_venv.bat

# Linux/Mac
chmod +x scripts/environment/setup_venv.sh
./scripts/environment/setup_venv.sh
```

#### 3. 或手动创建虚拟环境

#### 4. 创建虚拟环境（推荐）
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

#### 5. 安装依赖
```bash
pip install -r requirements.txt
```

#### 6. 配置环境变量
```bash
# 复制环境配置文件
cp .env.example .env

# 编辑 .env 文件，配置Redis连接和数据库（可选）
# 默认使用SQLite，无需额外配置
# 如需使用MySQL，请参考 DATABASE.md 文档
```

#### 7. 初始化数据库
```bash
python -m app.infrastructure.database.init_db
```

#### 8. 启动服务
```bash
python -m app.main
```

#### 9. 或者使用启动脚本
```bash
# Windows
start.bat

# Linux/Mac
chmod +x start.sh
./start.sh
```

#### 10. 数据库配置工具（可选）
如需切换数据库类型，可使用配置工具：
```bash
# Windows
scripts\database\setup_database.bat

# Linux/Mac
chmod +x scripts/database/setup_database.sh
./scripts/database/setup_database.sh
```

### 方式二：Docker部署

#### 1. 确保已安装Docker和docker-compose

#### 2. 启动所有服务
```bash
# 切换到Docker目录
cd scripts/docker

# 启动服务
docker-compose up -d
```

#### 3. 查看服务状态
```bash
docker-compose ps
```

#### 4. 查看日志
```bash
docker-compose logs -f backend
```

## 默认账户

初始化数据库后，系统会创建以下测试账户：

| 用户名 | 密码 | 角色 | 说明 |
|--------|------|------|------|
| admin  | admin123 | 超级管理员 | 拥有所有权限 |
| common | common123 | 普通用户 | 部分权限 |

## API文档

服务启动后，可以通过以下地址访问API文档：

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 主要API端点

### 认证相关
- `POST /login` - 用户登录
- `POST /refresh-token` - 刷新令牌
- `GET /mine` - 获取当前用户信息
- `GET /mine-logs` - 获取用户安全日志

### 系统管理
- `POST /user` - 获取用户列表
- `GET /list-all-role` - 获取所有角色
- `POST /role` - 获取角色列表
- `POST /menu` - 获取菜单列表
- `POST /dept` - 获取部门列表

### 系统监控
- `POST /online-logs` - 获取在线用户
- `POST /login-logs` - 获取登录日志
- `POST /operation-logs` - 获取操作日志
- `POST /system-logs` - 获取系统日志

### 其他
- `GET /get-async-routes` - 获取动态路由
- `POST /get-card-list` - 获取卡片列表
- `GET /health` - 健康检查

## 环境配置

主要环境变量说明：

```env
# 应用配置
APP_NAME=Vue Pure Admin Service
DEBUG=True
HOST=127.0.0.1
PORT=8000

# 数据库配置
# SQLite（默认）
DATABASE_URL=sqlite:///./db/vue_pure_admin.db
# MySQL（可选）
# DATABASE_URL=mysql+pymysql://root:123456@localhost:3306/vue_pure_admin

# Redis配置
REDIS_URL=redis://localhost:6379/0

# JWT配置
SECRET_KEY=your-super-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_MINUTES=10080

# CORS配置
ALLOWED_ORIGINS=["http://localhost:3000","http://localhost:5173"]
```

## 数据库配置

本项目支持两种数据库：

- **SQLite**（默认）：无需安装，开箱即用
- **MySQL**（可选）：更好的性能和并发支持

详细的数据库配置和切换方法，请参考 [docs/DATABASE.md](docs/DATABASE.md) 文档。

## 文档说明

- **[docs/PROJECT_STRUCTURE.md](docs/PROJECT_STRUCTURE.md)** - 详细的项目结构说明
- **[docs/DATABASE.md](docs/DATABASE.md)** - 数据库配置和切换指南  
- **[docs/DOCKER.md](docs/DOCKER.md)** - Docker部署和使用说明

## 开发指南

### 添加新的API端点

1. 在 `app/presentation/api/` 下创建或修改路由文件
2. 在 `app/presentation/schemas/` 下定义请求/响应模型
3. 在 `app/application/services/` 下实现业务逻辑
4. 在 `app/domain/entities/` 下定义实体模型（如需要）

### 数据库迁移

```bash
# 如果修改了模型，重新初始化数据库
python -m app.infrastructure.database.init_db
```

### 运行测试

```bash
python -m pytest tests/
```

## 生产部署建议

1. **安全配置**
   - 修改默认密码
   - 使用强密码的SECRET_KEY
   - 配置HTTPS
   - 限制CORS域名

2. **性能优化**
   - 使用生产级数据库
   - 配置Redis持久化
   - 启用数据库连接池
   - 使用Nginx反向代理

3. **监控日志**
   - 配置日志收集
   - 设置健康检查
   - 监控数据库性能

## 故障排除

### 常见问题

1. **数据库连接失败**
   - 检查数据库服务是否启动
   - 验证连接字符串配置
   - 确认数据库用户权限

2. **Redis连接失败**
   - 检查Redis服务状态
   - 验证Redis连接配置

3. **依赖安装失败**
   - 确保Python版本正确
   - 检查网络连接
   - 尝试使用镜像源

### 查看日志

```bash
# Docker环境
docker-compose logs -f backend

# 本地环境
# 查看应用输出日志
```

## 贡献指南

1. Fork 项目
2. 创建特性分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 许可证

MIT License