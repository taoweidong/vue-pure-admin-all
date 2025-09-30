# 数据库配置说明

## 数据库支持

本项目支持两种数据库配置：

### 1. SQLite（默认推荐）

**优点：**
- 无需安装额外数据库服务
- 开发测试方便
- 文件式存储，便于备份
- 零配置启动

**配置：**
```env
DATABASE_URL=sqlite:///./vue_pure_admin.db
```

### 2. MySQL（生产环境推荐）

**优点：**
- 更好的并发性能
- 支持大数据量
- 企业级特性
- 分布式部署

**配置：**
```env
DATABASE_URL=mysql+pymysql://用户名:密码@主机:端口/数据库名
```

## 切换数据库

### 方法一：修改 .env 文件

1. 复制环境配置文件：
```bash
cp .env.example .env
```

2. 编辑 .env 文件：

**使用 SQLite（默认）：**
```env
DATABASE_URL=sqlite:///./vue_pure_admin.db
```

**使用 MySQL：**
```env
DATABASE_URL=mysql+pymysql://root:123456@localhost:3306/vue_pure_admin
```

### 方法二：Docker Compose 切换

**使用 SQLite（默认）：**
```yaml
environment:
  DATABASE_URL: sqlite:///./vue_pure_admin.db
```

**使用 MySQL：**
```yaml
environment:
  DATABASE_URL: mysql+pymysql://root:123456@mysql:3306/vue_pure_admin
depends_on:
  - mysql  # 取消注释
  - redis
```

## MySQL 设置步骤

如果选择使用 MySQL，请按以下步骤设置：

### 1. 安装 MySQL

**Ubuntu/Debian：**
```bash
sudo apt update
sudo apt install mysql-server
```

**CentOS/RHEL：**
```bash
sudo yum install mysql-server
```

**Windows/macOS：**
下载并安装 MySQL 官方安装包

### 2. 创建数据库

```sql
CREATE DATABASE vue_pure_admin CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'vue_admin'@'localhost' IDENTIFIED BY 'vue_admin_password';
GRANT ALL PRIVILEGES ON vue_pure_admin.* TO 'vue_admin'@'localhost';
FLUSH PRIVILEGES;
```

### 3. 更新配置

修改 `.env` 文件：
```env
DATABASE_URL=mysql+pymysql://vue_admin:vue_admin_password@localhost:3306/vue_pure_admin
```

### 4. Docker MySQL 启动

如果使用 Docker Compose：

1. 取消注释 docker-compose.yml 中的 MySQL 配置
2. 启动所有服务：
```bash
docker-compose up -d
```

## 数据迁移

切换数据库后，需要重新初始化：

```bash
python -m app.infrastructure.database.init_db
```

## 性能对比

| 特性 | SQLite | MySQL |
|------|--------|-------|
| 启动速度 | 极快 | 较慢 |
| 并发支持 | 有限 | 优秀 |
| 数据量 | < 1GB | 无限制 |
| 维护成本 | 极低 | 中等 |
| 适用场景 | 开发/小型应用 | 生产/大型应用 |

## 建议

- **开发环境**: 使用 SQLite，简单快速
- **测试环境**: 使用 SQLite 或 MySQL
- **生产环境**: 使用 MySQL，更好的性能和可靠性