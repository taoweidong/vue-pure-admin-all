#!/bin/bash

# Python虚拟环境设置脚本

# 切换到项目根目录
cd "$(dirname "$0")/../.."

VENV_DIR="venv"
PYTHON_VERSION="3.11"

echo "🐍 Python Virtual Environment Setup"
echo "===================================="

# 检查Python版本
check_python() {
    if command -v python3 &> /dev/null; then
        PYTHON_CMD="python3"
    elif command -v python &> /dev/null; then
        PYTHON_CMD="python"
    else
        echo "❌ Python not found. Please install Python 3.11+"
        exit 1
    fi
    
    # 检查Python版本
    PYTHON_VER=$($PYTHON_CMD --version 2>&1 | cut -d' ' -f2 | cut -d'.' -f1,2)
    echo "📋 Found Python $PYTHON_VER"
    
    # 检查版本是否满足要求
    if ! $PYTHON_CMD -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)"; then
        echo "❌ Python 3.8+ is required, found $PYTHON_VER"
        exit 1
    fi
}

# 创建虚拟环境
create_venv() {
    if [ -d "$VENV_DIR" ]; then
        echo "⚠️ Virtual environment already exists at $VENV_DIR"
        read -p "Do you want to recreate it? (y/N): " confirm
        if [[ $confirm =~ ^[Yy]$ ]]; then
            echo "🗑️ Removing existing virtual environment..."
            rm -rf "$VENV_DIR"
        else
            echo "✅ Using existing virtual environment"
            return
        fi
    fi
    
    echo "📦 Creating virtual environment..."
    $PYTHON_CMD -m venv "$VENV_DIR"
    
    if [ $? -eq 0 ]; then
        echo "✅ Virtual environment created successfully"
    else
        echo "❌ Failed to create virtual environment"
        exit 1
    fi
}

# 激活虚拟环境并安装依赖
setup_dependencies() {
    echo "🔧 Activating virtual environment..."
    source "$VENV_DIR/bin/activate"
    
    if [ $? -ne 0 ]; then
        echo "❌ Failed to activate virtual environment"
        exit 1
    fi
    
    echo "✅ Virtual environment activated"
    echo "📍 Python location: $(which python)"
    echo "📊 Python version: $(python --version)"
    
    # 升级pip
    echo "📦 Upgrading pip..."
    python -m pip install --upgrade pip
    
    # 安装依赖
    if [ -f "requirements.txt" ]; then
        echo "📦 Installing dependencies from requirements.txt..."
        pip install -r requirements.txt
        
        if [ $? -eq 0 ]; then
            echo "✅ Dependencies installed successfully"
        else
            echo "❌ Failed to install dependencies"
            exit 1
        fi
    else
        echo "⚠️ requirements.txt not found, skipping dependency installation"
    fi
}

# 显示使用说明
show_usage() {
    echo ""
    echo "🎉 Virtual environment setup completed!"
    echo ""
    echo "📋 Usage Instructions:"
    echo "   To activate the virtual environment:"
    echo "   $ source $VENV_DIR/bin/activate"
    echo ""
    echo "   To deactivate:"
    echo "   $ deactivate"
    echo ""
    echo "   To start the service:"
    echo "   $ ./start.sh"
    echo ""
    echo "💡 The start.sh script will automatically use this virtual environment"
}

# 主函数
main() {
    check_python
    create_venv
    setup_dependencies
    show_usage
}

# 执行主函数
main