# Service目录结构整理

## 新的目录结构

```
service/
├── app/                      # 应用源码（保持不变）
├── db/                       # 数据库文件和SQL脚本（保持不变）
├── scripts/                  # 各种管理脚本
│   ├── database/            # 数据库相关脚本
│   │   ├── setup_database.sh
│   │   ├── setup_database.bat
│   │   ├── db_manager.sh
│   │   └── db_manager.bat
│   ├── environment/         # 环境管理脚本
│   │   ├── setup_venv.sh
│   │   ├── setup_venv.bat
│   │   ├── check_venv.sh
│   │   └── check_venv.bat
│   └── docker/             # Docker相关脚本
│       ├── docker-compose.yml
│       └── Dockerfile
├── docs/                    # 文档目录
│   ├── DATABASE.md
│   └── API.md
├── tests/                   # 测试文件（保持不变）
├── requirements.txt         # Python依赖（保持不变）
├── start.sh                # 主启动脚本（Linux/Mac）
├── start.bat               # 主启动脚本（Windows）
├── .env.example            # 环境配置示例（保持不变）
├── .gitignore              # Git忽略文件（保持不变）
└── README.md               # 项目说明（保持不变）
```

## 整理说明

1. 所有脚本文件移动到 `scripts/` 目录下按功能分类
2. 文档文件移动到 `docs/` 目录
3. Docker相关文件移动到 `scripts/docker/`
4. 根目录只保留必要的启动脚本和配置文件