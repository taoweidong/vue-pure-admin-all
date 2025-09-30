# 数据库迁移说明

此目录用于存放数据库结构变更的迁移脚本。

## 迁移脚本命名规范

迁移脚本应按照以下格式命名：
```
YYYYMMDD_HHMMSS_description.sql
```

例如：
- `20241201_143000_add_user_avatar_column.sql`
- `20241201_150000_create_notification_table.sql`

## 迁移脚本内容

每个迁移脚本应包含：
1. 注释说明变更内容
2. 向上迁移（应用变更）
3. 向下迁移（回滚变更，如需要）

示例：
```sql
-- 迁移：添加用户头像字段
-- 日期：2024-12-01
-- 作者：开发者姓名

-- 向上迁移
ALTER TABLE users ADD COLUMN avatar VARCHAR(255);

-- 向下迁移（回滚时使用）
-- ALTER TABLE users DROP COLUMN avatar;
```

## 使用说明

1. 创建新的迁移脚本时，确保文件名唯一且按时间顺序
2. 测试迁移脚本确保没有语法错误
3. 在生产环境应用前先在开发环境测试
4. 保持迁移脚本的原子性（一个脚本完成一个完整的变更）