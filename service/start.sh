#!/bin/bash

# Vue Pure Admin Service 启动脚本

echo "🚀 Starting Vue Pure Admin Service..."

# 检查Python环境
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found. Please install Python 3.11+"
    exit 1
fi

# 虚拟环境目录
VENV_DIR="venv"

# 创建虚拟环境（如果不存在）
if [ ! -d "$VENV_DIR" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv $VENV_DIR
    if [ $? -ne 0 ]; then
        echo "❌ Failed to create virtual environment"
        exit 1
    fi
    echo "✅ Virtual environment created successfully"
fi

# 激活虚拟环境
echo "🔧 Activating virtual environment..."
source $VENV_DIR/bin/activate

if [ $? -ne 0 ]; then
    echo "❌ Failed to activate virtual environment"
    exit 1
fi

echo "✅ Virtual environment activated: $VIRTUAL_ENV"

# 升级pip
echo "📦 Upgrading pip..."
pip install --upgrade pip

# 安装依赖
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# 复制环境配置文件
if [ ! -f .env ]; then
    echo "📋 Creating .env file from .env.example..."
    cp .env.example .env
    echo "✏️ Please edit .env file with your configuration"
fi

# 初始化数据库
echo "🗄️ Initializing Vue Pure Admin database..."
python -c "from app.infrastructure.database.init_vue_pure_admin import init_vue_pure_admin_database; init_vue_pure_admin_database()"

# 启动服务
echo "🎯 Starting the service..."
python main.py