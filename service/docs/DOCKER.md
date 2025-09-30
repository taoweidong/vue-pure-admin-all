# Docker使用说明

## 快速开始

### 使用Docker Compose（推荐）

1. **切换到Docker目录**
```bash
cd scripts/docker
```

2. **启动所有服务**
```bash
# 后台运行
docker-compose up -d

# 前台运行（查看日志）
docker-compose up
```

3. **访问服务**
- FastAPI后端: http://localhost:8000
- API文档: http://localhost:8000/docs
- Redis: localhost:6379
- MySQL: localhost:3306（如果启用）

### 单独构建镜像

```bash
# 在service根目录下
docker build -f scripts/docker/Dockerfile -t vue-pure-admin-backend .
```

## 服务配置

### 默认配置（SQLite）

默认使用SQLite数据库，无需额外数据库服务：

```yaml
services:
  backend:
    environment:
      DATABASE_URL: sqlite:///./db/vue_pure_admin.db
    depends_on:
      - redis
```

### 切换到MySQL

1. **编辑docker-compose.yml**，取消MySQL相关注释：

```yaml
services:
  backend:
    environment:
      # 注释SQLite配置
      # DATABASE_URL: sqlite:///./db/vue_pure_admin.db
      # 启用MySQL配置
      DATABASE_URL: mysql+pymysql://root:123456@mysql:3306/vue_pure_admin
    depends_on:
      - mysql  # 取消注释
      - redis
```

2. **重启服务**
```bash
docker-compose down
docker-compose up -d
```

## 常用命令

### 服务管理

```bash
# 启动服务
docker-compose up -d

# 停止服务
docker-compose down

# 重启服务
docker-compose restart

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs

# 查看特定服务日志
docker-compose logs backend
docker-compose logs mysql
docker-compose logs redis
```

### 数据管理

```bash
# 进入后端容器
docker-compose exec backend bash

# 进入MySQL容器
docker-compose exec mysql mysql -u root -p

# 进入Redis容器
docker-compose exec redis redis-cli

# 备份MySQL数据
docker-compose exec mysql mysqldump -u root -p123456 vue_pure_admin > backup.sql

# 恢复MySQL数据
docker-compose exec -T mysql mysql -u root -p123456 vue_pure_admin < backup.sql
```

### 开发调试

```bash
# 重新构建镜像
docker-compose build

# 强制重新构建
docker-compose build --no-cache

# 删除所有容器和网络
docker-compose down --remove-orphans

# 删除所有容器、网络和卷
docker-compose down -v
```

## 环境变量

### 后端服务环境变量

- `DATABASE_URL`: 数据库连接字符串
- `REDIS_URL`: Redis连接字符串  
- `SECRET_KEY`: JWT密钥
- `DEBUG`: 调试模式

### MySQL环境变量

- `MYSQL_ROOT_PASSWORD`: root用户密码
- `MYSQL_DATABASE`: 默认数据库名
- `MYSQL_USER`: 普通用户名
- `MYSQL_PASSWORD`: 普通用户密码

## 持久化存储

### 数据卷

- `mysql_data`: MySQL数据存储
- `redis_data`: Redis数据存储
- SQLite数据库文件通过目录挂载持久化

### 备份策略

**MySQL备份:**
```bash
# 创建备份
docker-compose exec mysql mysqldump -u root -p123456 --all-databases > mysql_backup.sql

# 恢复备份
docker-compose exec -T mysql mysql -u root -p123456 < mysql_backup.sql
```

**SQLite备份:**
```bash
# SQLite文件位于 ./db/vue_pure_admin.db，直接复制即可
cp db/vue_pure_admin.db db/vue_pure_admin_backup.db
```

## 网络配置

服务通过自定义网络 `vue-pure-admin` 通信：

- 后端可通过 `mysql:3306` 访问MySQL
- 后端可通过 `redis:6379` 访问Redis
- 外部可通过 `localhost:端口` 访问服务

## 故障排除

### 常见问题

1. **端口冲突**
```bash
# 查看端口占用
netstat -tulpn | grep :8000

# 修改docker-compose.yml中的端口映射
ports:
  - "8001:8000"  # 将本地端口改为8001
```

2. **权限问题**
```bash
# Linux/Mac下给脚本执行权限
chmod +x scripts/docker/*.sh
```

3. **网络问题**
```bash
# 重建网络
docker-compose down
docker network prune
docker-compose up -d
```

4. **数据库连接问题**
```bash
# 检查MySQL是否启动
docker-compose logs mysql

# 检查网络连通性
docker-compose exec backend ping mysql
```

### 日志查看

```bash
# 查看所有服务日志
docker-compose logs

# 实时查看日志
docker-compose logs -f

# 查看特定服务日志
docker-compose logs backend
docker-compose logs mysql
docker-compose logs redis
```

## 生产部署建议

1. **安全配置**
   - 修改默认密码
   - 使用强密钥
   - 限制网络访问

2. **性能优化**
   - 调整资源限制
   - 配置日志轮转
   - 使用外部数据库

3. **监控告警**
   - 添加健康检查
   - 配置监控指标
   - 设置告警规则