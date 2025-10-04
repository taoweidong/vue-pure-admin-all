#!/bin/bash

VENV_DIR="../../venv"

echo "[INFO] Python Virtual Environment Setup"
echo "===================================="

# 检查Python版本
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python not found. Please install Python 3.11+"
    exit 1
fi

PYTHON_VER=$(python3 --version | awk '{print $2}')
echo "[INFO] Found Python $PYTHON_VER"

# 检查版本是否满足要求
if ! python3 -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)" &> /dev/null; then
    echo "[ERROR] Python 3.8+ is required, found $PYTHON_VER"
    exit 1
fi

# 创建虚拟环境
if [ -d "$VENV_DIR" ]; then
    echo "[WARNING] Virtual environment already exists at $VENV_DIR"
    read -p "Do you want to recreate it? (y/N): " confirm
    if [[ $confirm =~ ^[Yy]$ ]]; then
        echo "[INFO] Removing existing virtual environment..."
        rm -rf "$VENV_DIR"
    else
        echo "[SUCCESS] Using existing virtual environment"
        cd ../..
        goto setup_dependencies
    fi
fi

echo "[INFO] Creating virtual environment..."
python3 -m venv "$VENV_DIR"

if [ $? -eq 0 ]; then
    echo "[SUCCESS] Virtual environment created successfully"
else
    echo "[ERROR] Failed to create virtual environment"
    exit 1
fi

# 激活虚拟环境并安装依赖
setup_dependencies() {
    echo "[INFO] Activating virtual environment..."
    source "$VENV_DIR/bin/activate"

    if [ $? -ne 0 ]; then
        echo "[ERROR] Failed to activate virtual environment"
        exit 1
    fi

    echo "[SUCCESS] Virtual environment activated"
    which python
    python --version

    # 升级pip
    echo "[INFO] Upgrading pip..."
    python -m pip install --upgrade pip

    # 安装依赖
    if [ -f "../../requirements.txt" ]; then
        echo "[INFO] Installing dependencies from requirements.txt..."
        pip install -r "../../requirements.txt"
        
        if [ $? -eq 0 ]; then
            echo "[SUCCESS] Dependencies installed successfully"
        else
            echo "[ERROR] Failed to install dependencies"
            exit 1
        fi
    else
        echo "[WARNING] requirements.txt not found, skipping dependency installation"
    fi
}

# 显示使用说明
show_usage() {
    echo ""
    echo "[SUCCESS] Virtual environment setup completed!"
    echo ""
    echo "[INFO] Usage Instructions:"
    echo "   To activate the virtual environment:"
    echo "   > source $VENV_DIR/bin/activate"
    echo ""
    echo "   To deactivate:"
    echo "   > deactivate"
    echo ""
    echo "   To start the service:"
    echo "   > start.sh"
    echo ""
    echo "[TIP] The start.sh script will automatically use this virtual environment"
}

setup_dependencies
show_usage

read -p "Press Enter to continue..."