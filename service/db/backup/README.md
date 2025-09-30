# 数据库备份说明

此目录用于存放SQLite数据库的备份文件。

## 备份文件命名规范

备份文件应按照以下格式命名：
```
vue_pure_admin_YYYYMMDD_HHMMSS.db
```

例如：
- `vue_pure_admin_20241201_143000.db`
- `vue_pure_admin_20241201_150000.db`

## 备份方法

### 手动备份
```bash
# 复制数据库文件
cp ../vue_pure_admin.db ./vue_pure_admin_$(date +%Y%m%d_%H%M%S).db
```

### 使用SQLite命令备份
```bash
# 使用sqlite3命令备份
sqlite3 ../vue_pure_admin.db ".backup ./vue_pure_admin_$(date +%Y%m%d_%H%M%S).db"
```

### 导出为SQL脚本
```bash
# 导出为SQL脚本
sqlite3 ../vue_pure_admin.db ".dump" > vue_pure_admin_$(date +%Y%m%d_%H%M%S).sql
```

## 恢复方法

### 从备份文件恢复
```bash
# 停止应用服务
# 替换数据库文件
cp ./vue_pure_admin_20241201_143000.db ../vue_pure_admin.db
# 重启应用服务
```

### 从SQL脚本恢复
```bash
# 停止应用服务
# 删除现有数据库
rm ../vue_pure_admin.db
# 从SQL脚本恢复
sqlite3 ../vue_pure_admin.db < vue_pure_admin_20241201_143000.sql
# 重启应用服务
```

## 自动备份脚本

可以创建定时任务进行自动备份：

```bash
#!/bin/bash
# backup_db.sh
BACKUP_DIR="/path/to/service/db/backup"
DB_FILE="/path/to/service/db/vue_pure_admin.db"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/vue_pure_admin_$TIMESTAMP.db"

# 创建备份
cp "$DB_FILE" "$BACKUP_FILE"

# 压缩备份文件（可选）
gzip "$BACKUP_FILE"

# 删除30天前的备份（可选）
find "$BACKUP_DIR" -name "vue_pure_admin_*.db.gz" -mtime +30 -delete

echo "Backup completed: $BACKUP_FILE.gz"
```

## 注意事项

1. 备份前确保应用没有正在写入数据库
2. 定期清理旧的备份文件以节省磁盘空间
3. 重要数据建议保存多个备份副本
4. 恢复前务必备份当前数据库