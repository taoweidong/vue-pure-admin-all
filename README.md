# Vue Pure Admin 全栈管理系统

<p align="center">
  <img src="https://img.shields.io/github/license/taoweidong/vue-pure-admin-all?style=flat" alt="GitHub">
  <img src="https://img.shields.io/github/stars/taoweidong/vue-pure-admin-all?color=fa6470&style=flat" alt="GitHub stars">
  <img src="https://img.shields.io/github/forks/taoweidong/vue-pure-admin-all?style=flat" alt="GitHub forks">
</p>

## 📖 项目简介

Vue Pure Admin All 是一个基于现代前端和后端技术栈构建的全栈管理系统，包含完整的前后端代码。前端基于 [vue-pure-admin](https://github.com/pure-admin/vue-pure-admin) 构建，后端采用 FastAPI + SQLAlchemy + DDD 架构模式实现，提供完整的 RBAC 权限管理系统。

### 🌟 项目特色

- ✅ **前后端分离架构** - 前端 Vue3 + Vite，后端 FastAPI + SQLAlchemy
- ✅ **DDD领域驱动设计** - 清晰的分层架构，易于维护和扩展
- ✅ **完整的RBAC权限管理** - 用户、角色、菜单、部门管理
- ✅ **现代化技术栈** - Vue3、Vite、Element-Plus、FastAPI、TypeScript等
- ✅ **容器化部署** - Docker + docker-compose 一键部署
- ✅ **完善的文档** - 详细的开发文档和部署指南

## 📁 项目结构

```
vue-pure-admin-all/
├── web/                     # 前端项目（基于 vue-pure-admin）
│   ├── src/                # 源代码目录
│   ├── public/             # 静态资源目录
│   ├── package.json        # 项目依赖配置
│   └── vite.config.ts      # 构建配置
└── service/                 # 后端服务（FastAPI + DDD）
    ├── app/                # 应用核心代码（DDD架构）
    │   ├── application/    # 应用层
    │   ├── domain/         # 领域层
    │   ├── infrastructure/ # 基础设施层
    │   └── presentation/   # 表示层
    ├── db/                 # 数据库文件和脚本
    ├── scripts/            # 各类管理脚本
    ├── tests/              # 测试套件
    ├── docs/               # 项目文档
    ├── main.py             # 应用入口文件
    └── requirements.txt    # Python依赖包
```

## 🚀 技术栈

### 前端技术栈
- **框架**: Vue 3.5+
- **构建工具**: Vite 7+
- **UI库**: Element Plus 2.11+
- **状态管理**: Pinia 3+
- **路由**: Vue Router 4+
- **语言**: TypeScript 5+
- **样式**: TailwindCSS 4+
- **HTTP库**: Axios 1.12+

### 后端技术栈
- **框架**: FastAPI 0.104+
- **数据库**: SQLite/MySQL + SQLAlchemy 2.0+
- **认证**: JWT + bcrypt 密码加密
- **架构模式**: DDD (领域驱动设计)
- **日志系统**: loguru
- **测试框架**: pytest
- **容器化**: Docker + docker-compose

## 🎯 功能特性

### 前端功能
- ✅ **响应式布局** - 适配不同屏幕尺寸
- ✅ **国际化支持** - 多语言切换
- ✅ **主题定制** - 暗色/亮色主题切换
- ✅ **权限控制** - 基于角色的页面和按钮权限
- ✅ **丰富的组件** - 表格、表单、图表等通用组件
- ✅ **路由管理** - 动态路由、路由守卫
- ✅ **状态管理** - 全局状态、主题配置、标签页等

### 后端功能
- ✅ **用户认证与授权** - JWT + bcrypt 安全认证
- ✅ **RBAC权限管理** - 用户/角色/权限精细化控制
- ✅ **用户管理** - 用户CRUD、状态管理、密码策略
- ✅ **角色管理** - 角色分配、权限继承
- ✅ **菜单管理** - 动态菜单、权限控制
- ✅ **部门管理** - 组织架构、职位管理
- ✅ **系统监控** - 在线用户、登录日志、操作日志
- ✅ **数据库管理工具** - 初始化、备份、恢复
- ✅ **API文档** - 自动生成Swagger文档
- ✅ **单元测试** - 完整测试覆盖

## 🚀 快速开始

### 前端启动

```bash
# 进入前端目录
cd web

# 安装依赖
pnpm install

# 启动开发服务器
pnpm dev
```

### 后端启动

#### 方式一：一键启动（推荐）

```bash
# 进入后端目录
cd service

# Windows 用户
start.bat

# Linux/Mac 用户  
chmod +x start.sh
./start.sh
```

#### 方式二：Docker 容器化部署

```bash
# 进入后端Docker目录
cd service/scripts/docker

# 启动所有服务
docker-compose up -d
```

## 🔐 默认账户

数据库初始化完成后，系统会自动创建以下测试账户：

| 用户名 | 密码 | 角色 | 权限说明 |
|--------|------|------|----------|
| **admin** | **admin123** | 超级管理员 | 拥有所有系统权限 |
| **common** | **common123** | 普通用户 | 基础功能权限 |

> ⚠️ **安全提醒**: 生产环境部署时请务必修改默认密码！

## 📚 文档指南

### 前端文档
- [vue-pure-admin官方文档](https://pure-admin.cn/)

### 后端文档
- **[service/README.md](service/README.md)** - 后端项目说明
- **[service/docs/PROJECT_STRUCTURE.md](service/docs/PROJECT_STRUCTURE.md)** - 项目结构详解
- **[service/docs/DDD_RBAC_ARCHITECTURE.md](service/docs/DDD_RBAC_ARCHITECTURE.md)** - DDD架构设计
- **[service/docs/DATABASE.md](service/docs/DATABASE.md)** - 数据库配置指南
- **[service/docs/DOCKER.md](service/docs/DOCKER.md)** - Docker部署说明

## 📦 部署方案

### 前端部署

```bash
# 构建生产版本
pnpm build

# 构建完成后，将 dist 目录部署到Web服务器
```

### 后端部署

```bash
# 使用Docker部署（推荐）
cd service/scripts/docker
docker-compose up -d
```

## 🤝 贡献指南

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 📜 许可证

本项目基于 MIT License 开源，详细信息请查看 [LICENSE](LICENSE) 文件。

## 🌟 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=taoweidong/vue-pure-admin-all&type=Date)](https://star-history.com/#taoweidong/vue-pure-admin-all&Date)