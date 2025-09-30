#!/bin/bash

# 数据库配置切换脚本

# 切换到项目根目录
cd "$(dirname "$0")/../.."

VENV_DIR="venv"

echo "🔧 Vue Pure Admin Service - 数据库配置切换工具"
echo ""

# 激活虚拟环境（如果存在）
if [ -d "$VENV_DIR" ]; then
    echo "🔧 Activating virtual environment..."
    source "$VENV_DIR/bin/activate"
fi

# 检查 .env 文件是否存在
if [ ! -f .env ]; then
    echo "📋 .env 文件不存在，从 .env.example 创建..."
    cp .env.example .env
fi

echo "请选择数据库类型："
echo "1) SQLite（推荐，无需额外配置）"
echo "2) MySQL（需要预先安装和配置MySQL）"
echo ""
read -p "请输入选择 (1 或 2): " choice

case $choice in
    1)
        echo "✅ 配置 SQLite 数据库..."
        # 更新 .env 文件
        sed -i 's|^DATABASE_URL=.*|DATABASE_URL=sqlite:///./db/vue_pure_admin.db|' .env
        echo "✅ SQLite 配置完成！"
        echo ""
        echo "📝 配置信息："
        echo "   数据库类型: SQLite"
        echo "   数据库文件: ./db/vue_pure_admin.db"
        echo "   优点: 零配置、开箱即用"
        ;;
    2)
        echo "⚙️ 配置 MySQL 数据库..."
        echo ""
        read -p "MySQL 主机地址 (默认: localhost): " host
        host=${host:-localhost}
        
        read -p "MySQL 端口 (默认: 3306): " port
        port=${port:-3306}
        
        read -p "数据库名称 (默认: vue_pure_admin): " dbname
        dbname=${dbname:-vue_pure_admin}
        
        read -p "用户名 (默认: root): " username
        username=${username:-root}
        
        read -s -p "密码: " password
        echo ""
        
        # 构建连接字符串
        db_url="mysql+pymysql://${username}:${password}@${host}:${port}/${dbname}"
        
        # 更新 .env 文件
        sed -i "s|^DATABASE_URL=.*|DATABASE_URL=${db_url}|" .env
        
        echo "✅ MySQL 配置完成！"
        echo ""
        echo "📝 配置信息："
        echo "   数据库类型: MySQL"
        echo "   主机: ${host}:${port}"
        echo "   数据库: ${dbname}"
        echo "   用户: ${username}"
        echo ""
        echo "⚠️ 注意：请确保："
        echo "   1. MySQL 服务已启动"
        echo "   2. 数据库 '${dbname}' 已创建"
        echo "   3. 用户 '${username}' 有足够权限"
        ;;
    *)
        echo "❌ 无效选择，退出。"
        exit 1
        ;;
esac

echo ""
echo "🔄 初始化数据库..."
python -m app.infrastructure.database.init_db

if [ $? -eq 0 ]; then
    echo "✅ 数据库初始化成功！"
    echo ""
    echo "🚀 现在可以启动服务："
    echo "   python -m app.main"
else
    echo "❌ 数据库初始化失败，请检查配置。"
    exit 1
fi