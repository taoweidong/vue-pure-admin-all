# 项目结构说明

## 目录结构

```
service/
├── app/                    # 应用核心代码（DDD架构）
│   ├── application/        # 应用层
│   ├── domain/            # 领域层
│   ├── infrastructure/    # 基础设施层
│   ├── interfaces/        # 接口层（API路由）
│   ├── main.py           # FastAPI应用入口
│   └── config.py         # 应用配置
│
├── db/                    # 数据库文件和初始化脚本
│   ├── init/             # 数据库初始化SQL脚本
│   └── vue_pure_admin.db # SQLite数据库文件（运行后生成）
│
├── docs/                  # 项目文档
│   ├── DATABASE.md       # 数据库配置说明
│   └── PROJECT_STRUCTURE.md # 项目结构说明（本文件）
│
├── scripts/               # 各类脚本文件
│   ├── database/         # 数据库相关脚本
│   │   ├── setup_database.sh    # Linux数据库设置脚本
│   │   ├── setup_database.bat   # Windows数据库设置脚本
│   │   ├── db_manager.sh        # Linux数据库管理脚本
│   │   └── db_manager.bat       # Windows数据库管理脚本
│   │
│   ├── docker/           # Docker相关文件
│   │   ├── docker-compose.yml   # Docker Compose配置
│   │   └── Dockerfile           # Docker镜像构建文件
│   │
│   └── environment/      # 虚拟环境管理脚本
│       ├── setup_venv.sh        # Linux虚拟环境设置脚本
│       ├── setup_venv.bat       # Windows虚拟环境设置脚本
│       ├── check_venv.sh        # Linux虚拟环境检查脚本
│       └── check_venv.bat       # Windows虚拟环境检查脚本
│
├── tests/                 # 测试文件
│
├── .env                   # 环境配置文件
├── .env.example          # 环境配置模板
├── .gitignore           # Git忽略文件配置
├── README.md            # 项目说明文档
├── requirements.txt     # Python依赖包列表
├── start.sh            # Linux/Mac启动脚本
└── start.bat           # Windows启动脚本
```

## 快速开始

### 方式一：直接启动（推荐）

**Linux/Mac:**
```bash
./start.sh
```

**Windows:**
```batch
start.bat
```

启动脚本会自动：
1. 检查Python环境
2. 创建和激活虚拟环境
3. 安装依赖包
4. 初始化数据库
5. 启动FastAPI服务

### 方式二：手动步骤

1. **创建虚拟环境**
```bash
# Linux/Mac
./scripts/environment/setup_venv.sh

# Windows
scripts\environment\setup_venv.bat
```

2. **激活虚拟环境**
```bash
# Linux/Mac
source venv/bin/activate

# Windows
venv\Scripts\activate
```

3. **安装依赖**
```bash
pip install -r requirements.txt
```

4. **配置环境变量**
```bash
cp .env.example .env
# 编辑 .env 文件根据需要修改配置
```

5. **初始化数据库**
```bash
python -m app.infrastructure.database.init_db
```

6. **启动服务**
```bash
python -m app.main
```

### 方式三：Docker部署

```bash
# 使用Docker Compose
cd scripts/docker
docker-compose up -d
```

## 脚本工具

### 虚拟环境管理

- `scripts/environment/setup_venv.*` - 创建虚拟环境并安装依赖
- `scripts/environment/check_venv.*` - 检查虚拟环境状态

### 数据库管理

- `scripts/database/setup_database.*` - 数据库初始化设置
- `scripts/database/db_manager.*` - 数据库管理工具

### Docker部署

- `scripts/docker/docker-compose.yml` - 容器编排配置
- `scripts/docker/Dockerfile` - 镜像构建配置

## 开发指南

### 代码架构

本项目采用DDD（领域驱动设计）架构模式：

- **Domain Layer (领域层)**: 业务逻辑和规则
- **Application Layer (应用层)**: 用例和业务流程
- **Infrastructure Layer (基础设施层)**: 数据库、缓存等外部依赖
- **Interface Layer (接口层)**: API路由和数据传输

### 数据库配置

默认使用SQLite数据库，支持切换到MySQL。详细配置请参考 `docs/DATABASE.md`。

### 环境变量

主要配置项：
- `DATABASE_URL`: 数据库连接字符串
- `REDIS_URL`: Redis连接字符串
- `SECRET_KEY`: JWT密钥
- `DEBUG`: 调试模式开关

## 注意事项

1. **Python版本**: 需要Python 3.8+，推荐3.11+
2. **依赖管理**: 使用虚拟环境隔离依赖
3. **数据库**: 首次运行需要初始化数据库
4. **端口占用**: 默认使用8000端口，确保端口未被占用