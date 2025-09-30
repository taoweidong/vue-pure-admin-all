# 数据库文件目录

此目录用于存放SQLite数据库文件和相关的SQL脚本。

## 目录结构

```
db/
├── vue_pure_admin.db      # SQLite数据库文件（运行时生成）
├── init/                  # 初始化SQL脚本
│   ├── 01_create_tables.sql    # 创建表结构
│   ├── 02_insert_data.sql      # 插入初始数据
│   └── 03_create_indexes.sql   # 创建索引
├── migrations/            # 数据库迁移脚本
│   └── README.md         # 迁移说明
└── backup/               # 数据库备份文件
    └── README.md         # 备份说明
```

## 说明

- `vue_pure_admin.db`: SQLite数据库文件，程序启动时自动创建
- `init/`: 存放数据库初始化SQL脚本
- `migrations/`: 存放数据库结构变更的迁移脚本
- `backup/`: 存放数据库备份文件

## 注意事项

1. SQLite数据库文件会在程序首次运行时自动创建
2. 请不要直接编辑数据库文件
3. 如需备份，建议复制整个`vue_pure_admin.db`文件
4. 开发环境下可以删除数据库文件重新初始化