#!/bin/bash

# 数据库配置切换工具

# 切换到项目根目录
cd "$(dirname "$0")/../.."

VENV_DIR="venv"

echo "[INFO] Vue Pure Admin Service - 数据库配置切换工具"
echo "[INFO] 当前工作目录："
pwd
echo "[INFO] 脚本目录: $(dirname "$0")"
echo

# 激活虚拟环境（如果存在）
activate_venv() {
    if [ -d "$VENV_DIR" ]; then
        echo "[INFO] 激活虚拟环境..."
        source "$VENV_DIR/bin/activate"
    else
        echo "[WARNING] 虚拟环境不存在，使用系统 Python 环境"
    fi
}

# 检查 Python 是否可用
echo "[INFO] 检查 Python 环境..."
if ! command -v python &> /dev/null; then
    echo "[ERROR] Python 未找到或未正确安装"
    echo "[ERROR] 请确保 Python 已安装并添加到 PATH 环境变量"
    exit 1
fi

# 检查必要的模块
echo "[INFO] 检查项目依赖..."
if ! python -c "import app" &> /dev/null; then
    echo "[ERROR] 项目模块无法导入"
    echo "[ERROR] 请确保在正确的项目目录下执行脚本"
    echo "[ERROR] 当前目录："
    pwd
    exit 1
fi

# 检查 .env 文件是否存在
if [ ! -f .env ]; then
    echo "[INFO] .env 文件不存在，从 .env.example 创建..."
    cp .env.example .env
fi

echo "请选择数据库类型："
echo "1) SQLite (推荐，无需额外配置)"
echo "2) MySQL (需要预先安装和配置MySQL)"
echo
read -p "请输入选择 (1 或 2): " choice

case $choice in
    1)
        echo "[INFO] 配置 SQLite 数据库..."
        # 更新 .env 文件
        sed -i 's/^DATABASE_URL=.*/DATABASE_URL=sqlite:\/\/\/.\/db\/vue_pure_admin.db/' .env
        echo "[SUCCESS] SQLite 配置完成！"
        echo
        echo "[INFO] 配置信息："
        echo "   数据库类型: SQLite"
        echo "   数据库文件: ./db/vue_pure_admin.db"
        echo "   优点: 零配置、开箱即用"
        ;;
    2)
        echo "[INFO] 配置 MySQL 数据库..."
        echo
        read -p "MySQL 主机地址 (默认: localhost): " host
        host=${host:-localhost}
        
        read -p "MySQL 端口 (默认: 3306): " port
        port=${port:-3306}
        
        read -p "数据库名称 (默认: vue_pure_admin): " dbname
        dbname=${dbname:-vue_pure_admin}
        
        read -p "用户名 (默认: root): " username
        username=${username:-root}
        
        read -sp "密码: " password
        echo
        
        # 构建连接字符串
        db_url="mysql+pymysql://${username}:${password}@${host}:${port}/${dbname}"
        
        # 更新 .env 文件
        echo "[INFO] 更新数据库配置: $db_url"
        sed -i "s|^DATABASE_URL=.*|DATABASE_URL=${db_url}|" .env
        
        echo "[SUCCESS] MySQL 配置完成！"
        echo
        echo "[INFO] 配置信息："
        echo "   数据库类型: MySQL"
        echo "   主机: ${host}:${port}"
        echo "   数据库: ${dbname}"
        echo "   用户: ${username}"
        echo
        echo "[WARNING] 注意：请确保："
        echo "   1. MySQL 服务已启动"
        echo "   2. 数据库 '${dbname}' 已创建"
        echo "   3. 用户 '${username}' 有足够权限"
        ;;
    *)
        echo "[ERROR] 无效选择，退出。"
        exit 1
        ;;
esac

echo
echo "[INFO] 初始化数据库..."
echo "[INFO] 当前工作目录："
pwd
echo "[INFO] 执行命令: python -m app.infrastructure.database.init_db"
echo

activate_venv
python -m app.infrastructure.database.init_db
db_init_result=$?

echo
echo "[INFO] 数据库初始化命令执行完成，返回代码: $db_init_result"

if [ $db_init_result -eq 0 ]; then
    echo "[SUCCESS] 数据库初始化成功！"
    echo
    echo "[INFO] 现在可以启动服务："
    echo "   python -m app.main"
else
    echo "[ERROR] 数据库初始化失败，返回代码: $db_init_result"
    echo "[ERROR] 请检查以下内容："
    echo "   1. Python 环境是否正确"
    echo "   2. 依赖包是否已安装"
    echo "   3. 数据库配置是否正确"
    echo "   4. 文件权限是否充足"
    exit $db_init_result
fi

read -p "Press Enter to continue..."